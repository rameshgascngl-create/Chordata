#!/usr/bin/env python3
"""Replace synthetic Dipnoi plate with 3 source-verified published zoological drawings.

All anatomy is retained at exact source pixels; text is placed outside originals.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from io import BytesIO
from time import sleep
from PIL import Image,ImageDraw,ImageFont
import hashlib,csv,json,subprocess

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"app/src/main/assets"
P=A/"pencil_plates/dipnoi_lungfin_comparison_en.png"
M=A/"pencil_plates/manifest.json"
L=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_DIPNOI_AUTHENTIC_THREE_GENERA_PNG_QA.md"
OLD="f1b60d3c8feadd6dfd1ec41d7327554b848c0163f816a690ce1c289d2b8b8917"
F=[
 {"name":"Neoceratodus forsteri","caption":"Australia - paired lobed fins, a single lung","year":"1907",
  "author":"David Starr Jordan, Fishes (1907), fig. 173 (after Dean); original artist not established; University of Washington FMIB",
  "page":"https://commons.wikimedia.org/wiki/File:FMIB_51710_Neoceratodus_forsteri_(Gunther)_Australia_Family_Ceratodontidae.jpeg",
  "src":"https://upload.wikimedia.org/wikipedia/commons/4/4f/FMIB_51710_Neoceratodus_forsteri_%28Gunther%29_Australia_Family_Ceratodontidae.jpeg",
  "dim":(1531,433),"sha1":"b74c9506cdf8ebf81baaaad128761e796474e76e"},
 {"name":"Protopterus annectens","caption":"Africa - elongated body, filamentous fins, paired lungs","year":"1902",
  "author":"J. Green, Proceedings of the Zoological Society of London (1902)",
  "page":"https://commons.wikimedia.org/wiki/File:Protopterus_annectens_1902.jpg",
  "src":"https://upload.wikimedia.org/wikipedia/commons/5/54/Protopterus_annectens_1902.jpg",
  "dim":(1506,500),"sha1":None},
 {"name":"Lepidosiren paradoxa","caption":"South America - female A and breeding male B; paired lungs","year":"1909",
  "author":"Unidentified illustrator, Reptiles, Amphibia, Fishes and Lower Chordata (1909)",
  "page":"https://commons.wikimedia.org/wiki/File:Lepidosiren_paradoxa1.jpg",
  "src":"https://upload.wikimedia.org/wikipedia/commons/0/0b/Lepidosiren_paradoxa1.jpg",
  "dim":(1200,419),"sha1":None},
]

def get(f):
    errors=[]
    for n,u in enumerate((f["src"],f["src"]+"?download=1")):
        try:
            q=Request(u,headers={"User-Agent":"ChordataAcademicZoology/1.0 (historical public-domain figure integration; https://github.com/rameshgascngl-create/Chordata)","Referer":"https://commons.wikimedia.org/"})
            with urlopen(q,timeout=90) as resp: b=resp.read(2000000)
            im=Image.open(BytesIO(b));im.load()
            h=hashlib.sha1(b).hexdigest()
            if im.format!="JPEG" or im.size!=f["dim"] or not 50000<len(b)<2000000:
                raise ValueError("Archive format, bytes or dimensions changed")
            if f["sha1"] and h!=f["sha1"]:raise ValueError("Published source SHA1 mismatch")
            return im.convert("RGB"),b,h
        except (HTTPError,URLError,ValueError,TimeoutError,OSError) as e:
            errors.append(str(e));sleep(3+n*4)
    raise RuntimeError("Could not verify source for "+f["name"]+": "+"; ".join(errors))

def font(n,bold=False):
    suffix="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+suffix,n)

def main():
    manifest=json.loads(M.read_text(encoding="utf-8"))
    entries=[x for x in manifest["figures"] if x["diagramId"]=="u2-dipnoi-lungfish-comparison" and x["lang"]=="en"]
    if len(entries)!=1 or entries[0]["path"]!="pencil_plates/dipnoi_lungfin_comparison_en.png":
        raise RuntimeError("Wrong registered Dipnoi lesson")
    e=entries[0]
    if e["sha256"]!=OLD:raise RuntimeError("Image already changed; refuse overwrite")
    pics=[get(s) for s in F]
    page=Image.new("RGB",(1710,1930),"#fafaf7")
    d=ImageDraw.Draw(page)
    d.text((55,35),"LUNGFISH: THREE LIVING GENERA",font=font(40,True),fill="#1f2e3e")
    d.text((55,95),"Original zoological prints, displayed at unscaled source pixels",font=font(24),fill="#3d5265")
    for i,(s,(im,raw,sha1),y) in enumerate(zip(F,pics,(160,720,1320)),1):
        d.line((55,y-18,1665,y-18),fill="#95a8a9",width=2)
        d.text((60,y),str(i)+". "+s["name"]+" ("+s["year"]+")",font=font(30,True),fill="#1f2e3e")
        d.text((60,y+42),s["caption"],font=font(22),fill="#45545c")
        if y+85+im.height>1840:raise RuntimeError("Figure overlaps caption/footer")
        page.paste(im,((1710-im.width)//2,y+85))
    d.line((55,1855,1660,1855),fill="#95a8a9",width=2)
    d.text((60,1870),"External morphology only - lungs not dissected; reviewer acceptance PENDING",font=font(19),fill="#77403b")
    out=BytesIO();page.save(out,format="PNG",compress_level=9,optimize=True)
    rawpng=out.getvalue();digest=hashlib.sha256(rawpng).hexdigest()
    P.write_bytes(rawpng)
    for k in ("svgMaster","svgSha256"):e.pop(k,None)
    e.update({
      "sha256":digest,"size":len(rawpng),
      "author":"David Starr Jordan (1907), J. Green (1902), unidentified 1909 artist; CHORDATA QA original-image layout",
      "license":"Public domain historical zoological prints; FMIB/Commons provenance",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "sourceUrl":F[0]["page"],"sourceUrls":[s["page"] for s in F],
      "sourceImageUrls":[s["src"] for s in F],
      "sourceSha1s":[h for im,b,h in pics],
      "sourceSha256":[hashlib.sha256(b).hexdigest() for im,b,h in pics],
      "sourceFormat":"JPEG","installedFormat":"PNG",
      "sourceKind":"ORIGINAL_THREE_HISTORIC_DIPNOI_ZOOLOGICAL_PLATES",
      "referenceUrls":[s["page"] for s in F],
      "modifications":"Original historical plates pasted unscaled, with independent English heading and captions, into a 1710x1930 RGB PNG. No crop, vector art, AI, traced anatomy or resizing.",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "visualReview":"ORIGINAL_THREE_DIPNOI_HISTORICAL_ARTWORKS_PENDING_SCIENTIFIC_REVIEW",
      "scope":"External morphological comparison of three extant Dipnoi genera. Lungs, internal gills and relationships are not visible in source artwork.",
      "keyEn":"Source-drawn lungfish external anatomy: 1 Neoceratodus forsteri (Australian lungfish), broad paired lobed fins, one lung; 2 Protopterus annectens (African lungfish), filamentous paired fins, paired lungs; 3 Lepidosiren paradoxa (South American lungfish), female A and breeding male B, paired lungs. No lungs are directly depicted in these external views. Extant lungfish share an evolutionary ancestor with tetrapods; they are not direct living tetrapod ancestors.",
      "keyTa":"மூன்று நுரையீரல் மீன் பேரினங்களின் புறத்தோற்ற ஒப்பீடு: 1 ஆஸ்திரேலிய நியோசெரட்டோடஸ் ஃபோர்ஸ்டெரை — அகன்ற மடல்துடுப்புகள், ஒரு நுரையீரல்; 2 ஆப்பிரிக்க புரோடாப்டெரஸ் அனெக்டென்ஸ் — நூல்போன்ற இணைத் துடுப்புகள், இரண்டு நுரையீரல்கள்; 3 தென் அமெரிக்க லெபிடோசைரன் பாரடாக்சா — பெண் A, இனப்பெருக்கக் கால ஆண் B, இரண்டு நுரையீரல்கள். இப்புறத்தோற்றப் படங்களில் நுரையீரல்கள் நேரடியாகக் காட்டப்படவில்லை. இன்றைய நுரையீரல் மீன்கள் நான்குகாலிகளின் நேரடி மூதாதைகள் அல்ல.",
      "topicId":"u2-dipnoi","page":3,"sectionKey":"affinities"
    })
    M.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with L.open(newline="",encoding="utf-8") as fp:
        reader=csv.DictReader(fp,delimiter="\t");cols,rows=reader.fieldnames,list(reader)
    match=[r for r in rows if r["diagramId"]=="u2-dipnoi-lungfish-comparison"]
    if len(match)!=1:raise RuntimeError("Dipnoi ledger missing or duplicate")
    match[0]["author"]=e["author"]
    match[0]["referenceSources"]="; ".join(s["page"] for s in F)
    with L.open("w",newline="",encoding="utf-8") as fp:
        writer=csv.DictWriter(fp,fieldnames=cols,delimiter="\t");writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    credits="\n".join("- "+f["name"]+": "+f["author"]+
        "; "+f["page"]+"; source SHA-1 "+h+
        "; source SHA-256 "+hashlib.sha256(b).hexdigest()
        for f,(im,b,h) in zip(F,pics))
    REPORT.write_text(
      "# CHORDATA Dipnoi original artwork QA\n\n"
      "Unit II, page 3, affinities; registered diagram u2-dipnoi-lungfish-comparison.\n\n"
      +credits+"\n\n"
      "All three public-domain historical anatomical illustrations are pasted 1:1, no AI art, vector redraw, rescaling or cropping. Separated English captions are added without covering the published artwork.\n\n"
      "Installed 1710x1930 RGB PNG, "+str(len(rawpng))+" bytes, SHA-256 "+digest+".\n"
      "This is EXTERNAL morphology. Lungs are NOT depicted. Source C shows male and female, not developmental stages.\n"
      "Scientific, taxonomic, Tamil-editorial and physical-device approvals PENDING. Production release HOLD.\n",encoding="utf-8")
    print("PASS original Dipnoi three-source PNG",digest,len(rawpng))
if __name__=="__main__":main()
