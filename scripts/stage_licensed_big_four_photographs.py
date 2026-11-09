#!/usr/bin/env python3
"""Replace the weak Big Four snake silhouettes with four real, CC-credited photos.

Scientific intent: taxonomy examples ONLY, not dangerous-snake identification advice.
A 2x2 contact plate is assembled from full, uncropped photographs, with separate
English figure keys and a warning in English/Tamil. No old app art is overwritten
unless the registered prior SHA and lesson location match exactly.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from hashlib import sha1, sha256
from io import BytesIO
import json, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/"app/src/main/assets"
DEST=ASSET/"pencil_plates/india_big_four_snakes_en.png"
MANIFEST=ASSET/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_INDIAN_BIG_FOUR_ORIGINAL_PHOTO_QA.md"
ID="u4-snakes-india-big-four-identification"
PRIOR_SHA="68fa916626a60be5bbfd62cc31b3d8f19534a6913eba12e64d12642c4f3f3edf"
LICENSE="https://creativecommons.org/licenses/by-sa/4.0/"

# Original photography, not copied figures from medical guidelines. Licences
# and photographers checked against each Wikimedia Commons original file page.
SOURCES=[
  dict(name="Indian cobra",taxon="Naja naja",creator="Jayendra Chiplunkar",
       license="CC BY-SA 3.0",licenseUrl="https://creativecommons.org/licenses/by-sa/3.0/",
       sourceUrl="https://commons.wikimedia.org/wiki/File:The_Common_Indian_Cobra_or_Spectacled_Cobra_10.JPG",
       download="https://upload.wikimedia.org/wikipedia/commons/d/d4/The_Common_Indian_Cobra_or_Spectacled_Cobra_10.JPG",
       pixels=[3648,2736],minimum_bytes=1000000),
  dict(name="Common krait",taxon="Bungarus caeruleus",creator="Davidvraju",
       license="CC BY-SA 4.0",licenseUrl="https://creativecommons.org/licenses/by-sa/4.0/",
       sourceUrl="https://commons.wikimedia.org/wiki/File:Common_krait.jpg",
       download="https://upload.wikimedia.org/wikipedia/commons/3/30/Common_krait.jpg",
       pixels=[2193,1466],minimum_bytes=1200000),
  dict(name="Russell's viper",taxon="Daboia russelii",creator="StefanSTS",
       license="CC BY-SA 3.0",licenseUrl="https://creativecommons.org/licenses/by-sa/3.0/",
       sourceUrl="https://commons.wikimedia.org/wiki/File:20090613_Daboia_russelii_Russells_Viper_Kettenviper_Pune.jpg",
       download="https://upload.wikimedia.org/wikipedia/commons/e/e4/20090613_Daboia_russelii_Russells_Viper_Kettenviper_Pune.jpg",
       pixels=[1872,2099],minimum_bytes=1000000),
  dict(name="Saw-scaled viper",taxon="Echis carinatus",creator="Dinesh Valke",
       license="CC BY-SA 2.0",licenseUrl="https://creativecommons.org/licenses/by-sa/2.0/",
       sourceUrl="https://commons.wikimedia.org/wiki/File:Indian_saw-scaled_viper_snake_(6156417004).jpg",
       download="https://upload.wikimedia.org/wikipedia/commons/1/17/Indian_saw-scaled_viper_snake_%286156417004%29.jpg",
       pixels=[2048,1536],minimum_bytes=600000),
]

def download_exact_photo(meta):
    request=Request(meta["download"],headers={
        "User-Agent":"CHORDATA-Zoology-CC-Image-Credit/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/",
        "Accept":"image/jpeg,*/*",
    })
    with urlopen(request,timeout=110) as response:
        data=response.read(10_000_001)
    if not meta["minimum_bytes"]<len(data)<10_000_001:
        raise ValueError(meta["taxon"]+": missing/wrong original byte length "+str(len(data)))
    img=Image.open(BytesIO(data)); img.load()
    if img.format!="JPEG" or list(img.size)!=meta["pixels"]:
        raise ValueError(meta["taxon"]+": original has wrong dimensions/type "+repr((img.size,img.format)))
    return data,img.convert("RGB")


def font(size,bold=False):
    path=("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
          else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    if not Path(path).is_file():
        raise RuntimeError("Pinned DejaVu Sans font missing; refusing non-reproducible composition")
    return ImageFont.truetype(path,size)

def build_plate(sources_and_images):
    # Visual composition retains all of every original photo: no cropping,
    # anatomical retouching, AI reconstruction, silhouettes or artistic tracing.
    width,height=2400,2130
    canvas=Image.new("RGB",(width,height),(248,248,247))
    draw=ImageDraw.Draw(canvas)
    tile_w=1160; tile_h=985
    xpositions=(25,1215); ypositions=(25,1080)
    for i,(entry,img) in enumerate(sources_and_images):
        row,col=divmod(i,2)
        x=xpositions[col];y=ypositions[row]
        draw.rounded_rectangle((x,y,x+tile_w,y+tile_h),radius=18,
                               fill=(255,255,255),outline=(210,210,210),width=3)
        box_w,box_h=tile_w-40,tile_h-145
        img.thumbnail((box_w,box_h),Image.Resampling.LANCZOS)
        px=x+20+(box_w-img.width)//2
        py=y+18+(box_h-img.height)//2
        canvas.paste(img,(px,py))
        draw.line((x+20,y+tile_h-115,x+tile_w-20,y+tile_h-115),
                  fill=(210,210,210),width=2)
        draw.text((x+24,y+tile_h-105),entry["name"],fill=(28,28,28),font=font(42,True))
        draw.text((x+24,y+tile_h-52),entry["taxon"],fill=(64,64,64),font=font(32))
    return canvas

def update_ledger(original:str,author:str,refs:str):
    lines=original.splitlines(keepends=True)
    count=0;result=[]
    for line in lines:
        if line.startswith(ID+"\t"):
            body=line.rstrip("\r\n"); ending=line[len(body):]
            fields=body.split("\t")
            if len(fields)!=9:raise RuntimeError("Unexpected figure ledger columns")
            fields[5]=author;fields[6]=refs
            line="\t".join(fields)+ending
            count+=1
        result.append(line)
    if count!=1:raise RuntimeError("Big Four ledger entry missing or duplicated")
    return "".join(result)

def main():
    current=json.loads(MANIFEST.read_text(encoding="utf-8"))
    figures=[e for e in current["figures"] if e["diagramId"]==ID]
    if len(figures)!=1:raise RuntimeError("Big Four registered figure has ambiguous variants")
    e=figures[0]
    if (e.get("lang"),e.get("path"),e.get("topicId"),e.get("page"),e.get("sectionKey")) != (
        "en","pencil_plates/india_big_four_snakes_en.png","u4-snakes-india",2,"big-four"):
        raise RuntimeError("Big Four exact lesson mapping changed")
    if e.get("sha256")!=PRIOR_SHA or sha256(DEST.read_bytes()).hexdigest()!=PRIOR_SHA:
        raise RuntimeError("Big Four installed PNG changed independently: refusing overwrite")

    fetched=[]
    for data in SOURCES:
        original,image=download_exact_photo(data)
        item={k:v for k,v in data.items() if k!="minimum_bytes"}
        item["sourceSha1"]=sha1(original).hexdigest()
        item["sourceSha256"]=sha256(original).hexdigest()
        item["sourceByteLength"]=len(original)
        fetched.append((item,image))
    output=BytesIO()
    build_plate(fetched).save(output,format="PNG",optimize=True,compress_level=9)
    png=output.getvalue()
    if not png.startswith(bytes.fromhex("89504e470d0a1a0a")):
        raise RuntimeError("Invalid combined PNG signature")

    for k in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        e.pop(k,None)
    author="Jayendra Chiplunkar; Davidvraju; StefanSTS; Dinesh Valke (original photos); CHORDATA QA (collage layout)"
    e.update(
        sha256=sha256(png).hexdigest(),size=len(png),author=author,
        sourceUrl=SOURCES[0]["sourceUrl"],
        license="CC BY-SA 4.0 montage layout; source photographs retain their respective CC BY-SA 3.0, 4.0, 3.0 and 2.0 licences",
        licenseUrl=LICENSE,
        sourceKind="LICENSED_FOUR_AUTHENTIC_INDIAN_SNAKES_2X2_PHOTO_COLLAGE",
        sourceFormat="Four original JPEGs",installedFormat="PNG",
        sourceSha256=[item["sourceSha256"] for item,img in fetched],
        sourceSha1=[item["sourceSha1"] for item,img in fetched],
        componentCredits=[
            {k:v for k,v in item.items() if k in
                ("name","taxon","creator","license","licenseUrl","sourceUrl","sourceSha1","sourceSha256","sourceByteLength","pixels")}
            for item,img in fetched
        ],
        referenceUrls=[item["sourceUrl"] for item,img in fetched]+[
            "https://www.who.int/news-room/questions-and-answers/item/snakebite-envenoming",
            "https://ncdc.mohfw.gov.in/uploads/pdf/COH9.pdf"
        ],
        modifications=("Four original full-frame JPEG photographs from Commons downsampled proportionally "
                       "and arranged as a labelled 2x2 photo comparison onto plain white cards. "
                       "No crops, retouch, AI, copied textbook artwork or anatomical reconstruction. "
                       "Original individual photos and licence links retained in expanded credits. "
                       "The original project schematic remains archived in docs/original_plate_svg."),
        keyEn=("Four photographed examples, in reading order: upper left Indian spectacled cobra (Naja naja); "
               "upper right common krait (Bungarus caeruleus); lower left Russell's viper (Daboia russelii); "
               "lower right saw-scaled viper (Echis carinatus). These are the traditionally named "
               "'Big Four', NOT an exhaustive list of medically important Indian snakes. "
               "Photographs, colours, patterns and hood expansion MUST NOT be used to identify an "
               "unknown snake or to judge whether a bite is dangerous. Do not approach snakes. "
               "Seek immediate professional medical care after any suspected snakebite."),
        keyTa=("இந்தியாவில் மரபாகக் குறிப்பிடப்படும் முக்கிய நச்சுப்பாம்புகளில் நான்கு: "
               "மேல் இடது — இந்திய நாகப்பாம்பு (Naja naja); "
               "மேல் வலது — கட்டுவிரியன் (Bungarus caeruleus); "
               "கீழ் இடது — கண்ணாடி விரியன் (Daboia russelii); "
               "கீழ் வலது — சுருட்டை விரியன் (Echis carinatus). "
               "இவை மட்டுமே ஆபத்தான பாம்புகள் அல்ல. ஒளிப்படம், நிறம், உடல் வடிவம் அல்லது "
               "படக்குறிகளை வைத்து அறியாத பாம்பை அடையாளம் காணவோ, கடியின் ஆபத்தை "
               "மதிப்பிடவோ கூடாது. பாம்பை அணுக வேண்டாம்; பாம்புக்கடி சந்தேகப்பட்டால் "
               "உடனடியாக மருத்துவ உதவியை நாட வேண்டும்."),
        scope=("Authentic representative photographs of four medically important species only. "
               "Not a clinical snake-identification guide, not exhaustive, and not suitable "
               "for deciding treatment or handling of live snakes."),
        visualReview="AUTHENTIC_FOUR_PHOTOS__SOURCE_CREDITS_VERIFIED__SCIENTIFIC_TAMIL_DEVICE_REVIEW_PENDING",
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        topicId="u4-snakes-india",page=2,sectionKey="big-four",
        learningObjective="Recognise four traditionally listed Indian venomous snake species as photographic examples; understand that other species cause medically important bites."
    )
    ledger=LEDGER.read_text(encoding="utf-8")
    revised=update_ledger(ledger,author," | ".join(item["sourceUrl"] for item,img in fetched))
    DEST.write_bytes(png)
    MANIFEST.write_text(json.dumps(current,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    LEDGER.write_bytes(revised.encode("utf-8"))
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    source_rows="\n".join(
        "- "+item["name"]+" ("+item["taxon"]+"), photographer "+item["creator"]+
        ", "+item["license"]+"; "+item["sourceUrl"]+
        "; source SHA-1 "+item["sourceSha1"]+"; SHA-256 "+item["sourceSha256"]
        for item,img in fetched
    )
    REPORT.write_text(
        "# CHORDATA — four original Indian snake photographs (QA only)\n\n"
        "Exact registered slot: "+ID+"; Unit IV, page 2, big-four.\n\n"
        "## Original photographers, respective licences, source hashes\n\n"
        +source_rows+"\n\n"
        "Composition is an original CHORDATA QA 2x2 layout of four authentic licensed "
        "photos. No original anatomical art was invented; full-frame originals retained "
        "in aspect-fitting image panels. Composite PNG bytes: "+str(len(png))+
        "; SHA-256 "+sha256(png).hexdigest()+".\n\n"
        "Composite layout licensed under CC BY-SA 4.0; component authors and their "
        "individual CC BY-SA 3.0, 4.0, 3.0, 2.0 licences are retained and displayed.\n\n"
        "Safety: images are for Zoology classroom comparisons only. A snakebite is a "
        "medical emergency regardless of apparent photo similarity. No handling or "
        "appearance-based treatment decisions. Source checking: WHO/NCDC.\n\n"
        "Biology and Tamil reviewers and real-device visual acceptance remain pending. "
        "No production release or independent academic sign-off.\n",
        encoding="utf-8"
    )
    print("PASS exact licensed Big Four source figures and 2x2 offline PNG",sha256(png).hexdigest(),len(png))

if __name__=="__main__":main()
