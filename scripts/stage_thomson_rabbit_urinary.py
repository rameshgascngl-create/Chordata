#!/usr/bin/env python3
"""Rabbit urinary passages, authentic 1916 species-specific male/female engravings.

Source: J. Arthur Thomson, Outlines of Zoology (1916), Figs 393/394.
The 1916 original is in the public domain in both the USA and India.
Female vestibule and male urethra are DIFFERENT anatomically; do not label
both as a shared urethra or conflate genital and urinary structures.
"""
import csv,json,subprocess
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import Request,urlopen
from PIL import Image,ImageDraw,ImageOps,ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
ID="u5-rabbit-excretory-system"
PNG=ASSETS/"pencil_plates/rabbit_urinary_tract.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
DOC=ROOT/"docs/CHORDATA_RABBIT_URINARY_HISTORICAL_QA.md"
PREVIEW=ROOT/"docs/qa-image-review/rabbit_urinary_tract_review.png"
ORIGINAL="https://upload.wikimedia.org/wikipedia/commons/e/e7/Image_from_page_743_of_%22Outlines_of_zoology%22_%281916%29_%2814597351000%29.jpg"
SOURCE="https://commons.wikimedia.org/wiki/File:Image_from_page_743_of_%22Outlines_of_zoology%22_(1916)_(14597351000).jpg"
CREATOR="J. Arthur Thomson, Outlines of Zoology (1916), Figs 393/394; original illustrator unidentified; CHORDATA QA layout"
RIGHTS="Public domain — J. Arthur Thomson (died 1933), published 1916"

def ft(size,bold=False):
    name="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+name,size)

def fetch():
    req=Request(ORIGINAL,headers={
        "User-Agent":"ChordataQAAnatomyImport/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/","Accept":"image/jpeg"})
    with urlopen(req,timeout=45) as r:
        raw=r.read(700000)
    if not 80000<len(raw)<700000: raise ValueError("Unknown historical source bytes")
    picture=Image.open(BytesIO(raw));picture.load()
    if picture.format!="JPEG" or picture.size!=(1048,1068):
        raise ValueError(f"Wrong rabbit source dimensions {picture.size} or format")
    return picture.convert("RGB"),sha256(raw).hexdigest()

def main():
    src,source_sha=fetch()
    # Correctly isolate male (Fig 393) and female (Fig 394) as different
    # structures, retaining ureter/bladder and their printed leader letters.
    male=src.crop((0,0,515,1065))
    female=src.crop((516,0,1048,1065))
    out=Image.new("RGB",(3300,1780),"#fffefa")
    d=ImageDraw.Draw(out)
    ink="#213641"
    d.text((100,60),"Rabbit urinary passages — male and female",font=ft(77,True),fill=ink)
    d.text((105,167),"Historical anatomy, 1916 • Figs 393 and 394 • not to scale",
           font=ft(42),fill="#425c69")
    for x,caption,part in [
        (85,"A  Male rabbit — Fig. 393",male),
        (905,"B  Female rabbit — Fig. 394",female),
    ]:
        d.rounded_rectangle((x,265,x+775,1600),radius=24,outline="#94a7b0",width=4,fill="white")
        d.text((x+24,295),caption,font=ft(38,True),fill=ink)
        gray=ImageOps.autocontrast(ImageOps.grayscale(part),cutoff=(1,1)).convert("RGB")
        fitted=ImageOps.contain(gray,(710,1160),Image.Resampling.LANCZOS)
        out.paste(fitted,(x+32+(710-fitted.width)//2,371+(1160-fitted.height)//2))
    x=1760
    d.rounded_rectangle((x,265,3220,1600),radius=24,outline="#94a7b0",width=4,fill="white")
    d.text((x+45,305),"Original anatomical labels",font=ft(54,True),fill=ink)
    d.text((x+50,400),"Male urinary route",font=ft(43,True),fill="#2b667e")
    y=475
    for line in ["A  Kidney", "U  Ureter", "Bl  Urinary bladder", "Ur  Urethra"]:
        d.text((x+65,y),line,font=ft(41),fill=ink);y+=82
    d.line((x+48,805,3170,805),width=4,fill="#c1ccd1")
    d.text((x+50,850),"Female urinary route",font=ft(43,True),fill="#2b667e")
    y=932
    for line in ["K  Kidney", "U  Ureter", "Bl  Urinary bladder", "Ve  Vestibule (urogenital)"]:
        d.text((x+65,y),line,font=ft(41),fill=ink);y+=82
    d.line((x+48,1310,3170,1310),width=4,fill="#c1ccd1")
    d.text((x+48,1355),"Reproductive organs are also",font=ft(36),fill="#465e67")
    d.text((x+48,1415),"shown for anatomical context.",font=ft(36),fill="#465e67")
    d.text((110,1660),"The male urethra and female vestibule are anatomically distinct.",font=ft(40),fill="#405865")

    out.save(PNG,"PNG",optimize=True)
    raw=PNG.read_bytes()
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    small=out.copy();small.thumbnail((1200,780),Image.Resampling.LANCZOS)
    small.save(PREVIEW,"PNG",optimize=True)
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    hits=[e for e in m["figures"] if e["diagramId"]==ID]
    if len(hits)!=1 or hits[0]["lang"]!="shared" or hits[0]["path"]!="pencil_plates/rabbit_urinary_tract.png":
        raise ValueError("Rabbit excretory lesson mapping changed")
    e=hits[0]
    if e["author"] not in ("Chordata QA project — original numbered schematic",CREATOR):
        raise ValueError("Refuse to replace previously edited/accepted illustration")
    e.update(
        sha256=sha256(raw).hexdigest(),size=len(raw),
        author=CREATOR,license=RIGHTS,sourceUrl=SOURCE,
        licenseUrl="https://creativecommons.org/publicdomain/mark/1.0/",
        sourceSha256=[source_sha],
        modifications=("1916 Figs 393 and 394 separated at centre and proportionally "
                       "scaled with contrast adjustment; English urinary-system key "
                       "placed outside the historical ink. Both genders retained. "
                       "Reproductive structures explicitly labelled as context."),
        keyEn=("Male: A kidney, U ureter, Bl bladder, Ur urethra. "
               "Female: K kidney, U ureter, Bl bladder, Ve vestibule. "
               "Other structures in the historical source belong to the "
               "reproductive systems and are not urinary organs."),
        keyTa=("ஆண் முயல்: A சிறுநீரகம், U சிறுநீர்க்குழாய், Bl சிறுநீர்ப்பை, "
               "Ur சிறுநீர்ப்புறக்குழாய். பெண் முயல்: K சிறுநீரகம், U சிறுநீர்க்குழாய், "
               "Bl சிறுநீர்ப்பை, Ve முன்கூடம் (சிறுநீர்–இனப்பெருக்க வழி). "
               "மற்ற பகுதிகள் இனப்பெருக்க மண்டலத்தைச் சார்ந்தவை."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        rdr=csv.DictReader(f,delimiter="\t"); fields=rdr.fieldnames; rows=list(rdr)
    found=[x for x in rows if x["diagramId"]==ID]
    assert len(found)==1
    found[0]["author"]=CREATOR
    found[0]["referenceSources"]=SOURCE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t");w.writeheader();w.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    DOC.write_text(
        "# CHORDATA historical rabbit excretory-system illustration\n\n"
        "Exact lesson ID: "+ID+"\n\n"
        "Source: "+SOURCE+"\n"
        "Originally published 1916 by J. Arthur Thomson, Outlines of Zoology; "
        "figs 393/394; illustrator not identified, source now public domain. "
        "Thomson died in 1933.\n"
        "Original scan SHA-256: "+source_sha+"\n"
        "Adapted PNG SHA-256: "+sha256(raw).hexdigest()+"\n\n"
        "Adaptation: male and female source anatomical views separated, "
        "enlarged without distortion, contrast adjusted and placed alongside "
        "a separate English legend. The female vestibule is not mislabelled "
        "as the male urethra; reproductive structures are shown as contextual.\n\n"
        "Academic and Tamil review: pending. Android/device check pending. "
        "All 64 slot IDs retained; no approval signatures fabricated.\n",
        encoding="utf-8")
    print(f"PASS: 1916 rabbit urinary anatomy staged, {len(raw)} bytes, {sha256(raw).hexdigest()}")

if __name__=="__main__":
    main()
