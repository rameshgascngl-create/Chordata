#!/usr/bin/env python3
"""Integrate source-published 1905 bird eye and inner-ear engravings in pigeon QA.

The historical plates are comparative AVIAN anatomy, not verified pigeon
dissections. Both original source illustrations are retained at native pixels.
The eye retains all its published internal labels, and the ear is a documented
rectangular crop around figure 12 (no redraw or AI modification).
"""
from pathlib import Path
from io import BytesIO
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from time import sleep
import csv, hashlib, json, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
TARGET=ASSETS/"pencil_plates/pigeon_eye_ear_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_NIE1905_AVIAN_EYE_EAR_HISTORIC_QA.md"
ID="u5-columba-sense-organs"
OLD_SHA256="9b098710fd9ed904d3fe879b48e466df5c338fc66f02ea081563c489507be611"
ARTIST="Original engraver not identified; The New International Encyclopaedia, vol. 3 (1905), bird anatomy article by Ernest Ingersoll"
SOURCES=[
  dict(role="bird-eye",name="NIE 1905 Bird - eye structure.jpg",
       page="https://commons.wikimedia.org/wiki/File:NIE_1905_Bird_-_eye_structure.jpg",
       url="https://upload.wikimedia.org/wikipedia/commons/f/fd/NIE_1905_Bird_-_eye_structure.jpg",
       size=(721,639),expected_sha1=None,
       caption="Bird eye: lens, cornea, retina, scleral coat and pecten"),
  dict(role="bird-inner-ear",name="NIE 1905 Bird - anatomy.jpg",
       page="https://commons.wikimedia.org/wiki/File:NIE_1905_Bird_-_anatomy.jpg",
       url="https://upload.wikimedia.org/wikipedia/commons/c/cf/NIE_1905_Bird_-_anatomy.jpg",
       size=(1499,2401),
       expected_sha1="046dd4b576fe4fef09e82be84073b99d12e00633",
       caption="Bird inner ear: figure 12, columella auris and canals")
]
CROP=(490,265,1050,710)

def font(size,bold=False):
    name="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+name,size)

def source_record(source):
    issues=[]
    for i,url in enumerate((source["url"],source["url"]+"?download=1",
             "https://commons.wikimedia.org/wiki/Special:Redirect/file/"+source["name"].replace(" ","_"))):
        try:
            request=Request(url,headers={
                "User-Agent":"ChordataGovtCollegeAcademicQA/1.0 (published-1905-bird-anatomy; https://github.com/rameshgascngl-create/Chordata)",
                "Referer":"https://commons.wikimedia.org/",
                "Accept":"image/jpeg,image/*"})
            with urlopen(request,timeout=85) as response:
                raw=response.read(1200000)
            orig=Image.open(BytesIO(raw))
            orig.load()
            sha1=hashlib.sha1(raw).hexdigest()
            if orig.format!="JPEG" or orig.size!=source["size"] or not 50000<len(raw)<1200000:
                raise ValueError("Source JPEG format, size or dimensions mismatch")
            if source["expected_sha1"] and sha1!=source["expected_sha1"]:
                raise ValueError("Archived source SHA-1 mismatch")
            return orig.convert("RGB"),raw,sha1
        except (ValueError,HTTPError,URLError,TimeoutError,OSError) as exc:
            issues.append(str(exc)+" at "+url)
            sleep(min(3+2*i,8))
    raise RuntimeError("Could not verify original "+source["name"]+"; previous app asset unchanged. "+"; ".join(issues))

def main():
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    rec=[x for x in m["figures"] if x.get("diagramId")==ID and x.get("lang")=="en"]
    if len(rec)!=1 or rec[0].get("path")!="pencil_plates/pigeon_eye_ear_en.png":
        raise RuntimeError("Wrong pigeon sense organ lesson/image mapping")
    entry=rec[0]
    if entry["sha256"]!=OLD_SHA256:
        if entry.get("sourceKind")=="NIE1905_PUBLISHED_BIRD_EYE_AND_INNER_EAR_ORIGINAL_PNG":
            print("Already original-published figure; preserving existing image")
            return
        raise RuntimeError("Competing pigeon-eye editing detected; refusing overwrite")

    originals=[source_record(s) for s in SOURCES]
    eye=originals[0][0]
    ear_full=originals[1][0]
    ear=ear_full.crop(CROP)
    if ear.size!=(560,445):
        raise RuntimeError("Unexpected source-crop dimensions")

    # Historical anatomical art is never resized or computer-redrawn; this
    # composite adds only typography outside its original pixels.
    canvas=Image.new("RGB",(1600,1260),"#faf9f6")
    draw=ImageDraw.Draw(canvas)
    dark="#1b2c3a"
    subtle="#4c5d69"
    draw.text((65,37),"AVIAN EYE AND INNER EAR",font=font(44,True),fill=dark)
    draw.text((65,102),"Published zoological engravings (1905) - comparative bird anatomy",font=font(23),fill=subtle)
    draw.line((65,157,1530,157),fill="#a1b1b8",width=2)
    draw.text((65,177),"1  EYE - transverse section",font=font(27,True),fill=dark)
    draw.text((900,177),"2  INNER EAR - Fig. 12 detail",font=font(26,True),fill=dark)
    canvas.paste(eye,(70,232))
    canvas.paste(ear,(905,240))
    draw.text((905,707),"Source figure 12, cropped only; no art added",font=font(19),fill=subtle)
    draw.line((70,926,1532,926),fill="#a1b1b8",width=2)
    notes=[
      "EYE (original abbreviations): P, pecten; L, lens;",
      "C, cornea; R, retina; Sc, sclera. Verify against print.",
      "",
      "EAR (source figure 12): Co, columella auris;",
      "H, horizontal canal; S, sagittal semicircular canal;",
      "L, lagena. Other letters refer to adjacent skull bones.",
      "",
      "These are typical AVIAN drawings, not a verified",
      "Columba livia individual. Zoology review: PENDING."
    ]
    y=952
    for note in notes:
        if note:
            draw.text((78,y),note,font=font(23),fill=dark)
        y+=35 if note else 12
    out=BytesIO()
    canvas.save(out,format="PNG",compress_level=9,optimize=True)
    png=out.getvalue()
    digest=hashlib.sha256(png).hexdigest()
    if not png.startswith(bytes.fromhex("89504e470d0a1a0a")):
        raise RuntimeError("Output is not a PNG")

    TARGET.write_bytes(png)
    for tag in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        entry.pop(tag,None)
    entry.update({
      "sha256":digest,"size":len(png),
      "author":ARTIST,
      "license":"Public domain; two published bird-anatomy engravings from the New International Encyclopaedia (1905)",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "sourceUrl":SOURCES[0]["page"],
      "sourceUrls":[s["page"] for s in SOURCES],
      "sourceImageUrls":[s["url"] for s in SOURCES],
      "sourceSha1s":[x[2] for x in originals],
      "sourceSha256":[hashlib.sha256(x[1]).hexdigest() for x in originals],
      "sourceFormat":"JPEG","installedFormat":"PNG",
      "sourceKind":"NIE1905_PUBLISHED_BIRD_EYE_AND_INNER_EAR_ORIGINAL_PNG",
      "sourceCropRect":list(CROP),
      "referenceUrls":[s["page"] for s in SOURCES],
      "modifications":"Both public-domain 1905 anatomical JPEG scans placed at native pixel scale on 1600x1260 RGB PNG; bird inner ear isolated by documented x=490..1050, y=265..710 source crop of figure 12; captions only OUTSIDE art. No SVG drawing, anatomy redrawing, AI, or visual interpolation.",
      "scope":"Comparative avian transverse eye section and avian inner-ear anatomy including columella and vestibular canals. 1905 generalized BIRD figures, NOT verified Columba livia dissections.",
      "keyEn":"Original bird eye: P pecten oculi, L lens, C cornea, R retina and Sc sclera. Original inner ear Fig. 12 from the 1905 bird-anatomy plate: Co columella auris (the single middle-ear ossicle); H horizontal and S sagittal semicircular canals; L lagena. The original figure also marks adjacent skull bones. This is comparative avian anatomy, not a confirmed pigeon dissection. Modern descriptions distinguish the bird's uncoiled cochlear duct and vestibular apparatus.",
      "keyTa":"1905 ஆம் ஆண்டின் பறவைப் புலனுறுப்பு உடற்கூறியல் ஓவியங்கள். கண்ணின் குறியீடுகள்: P — பெக்டென் ஓகுலை, L — விழிவில்லை, C — விழிவெண்படலத்தின் முன்பகுதியான கார்னியா, R — விழித்திரை, Sc — ஸ்கிளீரா. உட்செவியின் படம் 12: Co — ஒலியை கடத்தும் ஒற்றை நடுச்செவி எலும்பான கொலுமெல்லா ஆரிஸ்; H — கிடைமட்ட அரைவட்டக் குழாய்; S — செங்குத்து அரைவட்டக் குழாய்; L — லஜீனா. இவை பொதுவான பறவை உடற்கூறியல் படங்கள்; தனிப்பட்ட கொலும்பா லிவியா மாதிரியின் பிரித்தாய்வுப் படம் என உறுதிப்படுத்தப்படவில்லை.",
      "visualReview":"ORIGINAL_1905_AVIAN_EYE_EAR_PENDING_ZOOLOGY_REVIEW",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "topicId":"u5-columba","page":4,"sectionKey":"sense-organs"
    })
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as file:
        reader=csv.DictReader(file,delimiter="\t");headers,rows=reader.fieldnames,list(reader)
    matching=[row for row in rows if row["diagramId"]==ID]
    if len(matching)!=1:raise RuntimeError("Pigeon sense organ ledger record missing/duplicated")
    matching[0]["author"]=ARTIST
    matching[0]["referenceSources"]="; ".join(s["page"] for s in SOURCES)
    with LEDGER.open("w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=headers,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    source_lines="\n".join(
        "- "+s["role"]+": "+s["page"]+"; original "+str(orig[0].size)+
        "; SHA-1 "+orig[2]+"; SHA-256 "+hashlib.sha256(orig[1]).hexdigest()
        for s,orig in zip(SOURCES,originals)
    )
    REPORT.write_text(
      "# CHORDATA — Published bird eye and ear engravings (1905)\n\n"
      "Unit V Columba lesson, page 4 (sense-organs); figure u5-columba-sense-organs.\n\n"
      "Original source: The New International Encyclopaedia, vol. 3, published 1905; bird article by Ernest Ingersoll; individual artist not credited. Public-domain Commons scans.\n\n"+
      source_lines+"\n\n"
      "The eye JPEG is pasted at native 721x639 source pixels. Original bird plate Fig. 12 inner ear is taken from source pixels crop rectangle (490,265,1050,710), 560x445, no scaling. Both on a 1600x1260 lossless PNG. No source artwork is redrawn, traced or modified aside from cropping the ear figure from the multi-figure published page; labels outside artwork explain anatomy.\n\n"
      "Installed PNG size "+str(len(png))+", SHA-256 "+digest+".\n\n"
      "CRITICAL SPECIES LIMITATION: these are original published generic bird illustrations; they are not confirmed Columba livia dissection plates. Bird eye structures include the pecten; inner-ear figure shows columella auris and labyrinthine canal structures. Eye and ear original symbols should be reviewed by a zoologist against the printed book caption. The original 1905 drawing predates current microscopic anatomy; do not teach it as a complete modern avian ear atlas.\n\n"
      "Independent scientific and Tamil review: PENDING. Physical device zoom and Android QA: PENDING. Production release: HOLD.\n",encoding="utf-8"
    )
    print("PASS original 1905 bird eye and ear composite",len(png),digest)

if __name__=="__main__": main()
