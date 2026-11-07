#!/usr/bin/env python3
"""High-resolution, source-credited four-type fish-scale teaching plate.

Three sourced examples are Jon Houseman's detailed line-art and stained scales
(CC BY-SA 3.0). The placoid section is ORIGINAL CHORDATA QA vector-like artwork
based on general dermal denticle anatomy and clearly marked diagrammatic.
All lesson IDs, bilingual captions, and human review statuses remain intact.
"""
from __future__ import annotations
import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
from urllib.request import Request,urlopen

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
TARGET=ASSETS/"pencil_plates/fish_scale_types.png"
LEDGER=ROOT/"docs/figure-coverage.tsv"
PROVENANCE=ROOT/"docs/CHORDATA_SOURCE_FISH_SCALES_QA.md"
PREVIEW=ROOT/"docs/qa-image-review/fish_scale_types_review.png"
ID="u2-scales-fins-scale-types-labelled"
SOURCE_URL="https://upload.wikimedia.org/wikipedia/commons/d/d1/Fishscales.png"
SOURCE_PAGE="https://commons.wikimedia.org/wiki/File:Fishscales.png"
AUTHOR="Jon Houseman (ganoid/cycloid/ctenoid); CHORDATA QA (original placoid section and layout)"
LICENCE="CC BY-SA 3.0 Unported — composite derivative, source credited"
LICENCE_URL="https://creativecommons.org/licenses/by-sa/3.0/"

def font(sz,bold=False):
    path="/usr/share/fonts/truetype/dejavu/"+("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(path,sz)

def get_source():
    req=Request(SOURCE_URL,headers={"User-Agent":"ChordataQAArtIntake/1.0 (https://github.com/rameshgascngl-create/Chordata)",
                                    "Referer":"https://commons.wikimedia.org/","Accept":"image/png"})
    with urlopen(req,timeout=50) as res:
        raw=res.read(1800000)
    if len(raw)<80000 or len(raw)>=1800000:
        raise ValueError("Unexpected source length")
    image=Image.open(BytesIO(raw))
    image.load()
    if image.format!="PNG" or image.size!=(841,576):
        raise ValueError("Source image changed; do not stage unknown artwork")
    return image.convert("RGB"),sha256(raw).hexdigest()

def placoid_panel():
    width,height=1100,1210
    image=Image.new("RGB",(width,height),"white")
    d=ImageDraw.Draw(image)
    ink="#243845"; petrol="#3a6471"
    d.text((60,40),"D  Placoid scale",font=font(58,True),fill=ink)
    d.text((60,116),"(shark dermal denticle)",font=font(37),fill=petrol)
    d.text((60,176),"Enlarged lateral section — schematic",font=font(30),fill="#52646c")
    # Crown / dentine with a backward-pointing cusp. Base plate is distinct
    # from the projecting odontode. Internal canal is not open to seawater.
    basal=[(165,900),(260,879),(370,883),(505,872),(670,881),(780,882),(910,907),
           (915,962),(780,986),(640,983),(486,974),(325,990),(170,982)]
    d.polygon(basal,fill="#e9e4d7")
    d.line(basal+[basal[0]],fill=ink,width=8,joint="curve")
    crown=[(320,879),(385,797),(428,612),(440,450),(486,350),(531,320),
           (589,341),(634,421),(658,535),(732,645),(904,718),(927,748),
           (796,740),(659,682),(594,625),(563,569),(541,668),(528,789),(531,876)]
    d.polygon(crown,fill="#d7e6df")
    d.line(crown+[crown[0]],fill=ink,width=8,joint="curve")
    cap=[(440,450),(486,350),(531,320),(589,341),(634,421),(658,535),
         (732,645),(904,718),(927,748),(800,735),(681,675),(610,601),
         (596,528),(569,423),(530,391),(493,438)]
    d.polygon(cap,fill="#b9d2d6")
    d.line([(440,450),(486,350),(531,320),(589,341),(634,421),(658,535),
            (732,645),(904,718),(927,748)],fill=ink,width=9,joint="curve")
    pulp=[(477,877),(484,775),(487,668),(490,573),(505,496),
          (525,450),(543,490),(555,576),(556,697),(558,874)]
    d.polygon(pulp,fill="#fff5da")
    d.line(pulp+[pulp[0]],fill="#9b6f53",width=6,joint="curve")
    # Expert interpretable leader lines keep labels OUTSIDE the anatomy.
    d.line([(574,334),(710,262),(825,262)],fill=ink,width=5)
    d.text((720,220),"Enameloid",font=font(37,True),fill=ink)
    d.line([(625,590),(768,500),(875,500)],fill=ink,width=4)
    d.text((780,449),"Dentine",font=font(35),fill=ink)
    d.line([(511,683),(370,697),(95,697)],fill=ink,width=4)
    d.text((88,640),"Pulp cavity",font=font(35),fill=ink)
    d.line([(453,954),(365,1060),(88,1060)],fill=ink,width=4)
    d.text((88,1084),"Basal plate",font=font(36),fill=ink)
    return image

def main():
    sourced,sourced_hash=get_source()
    out=Image.new("RGB",(3500,1690),"#fffefa")
    draw=ImageDraw.Draw(out)
    ink="#17323e"
    draw.text((115,66),"Fish scales — anatomical comparison",font=font(90,True),fill=ink)
    draw.text((118,183),"Placoid  ·  Ganoid  ·  Cycloid  ·  Ctenoid",font=font(49),fill="#355769")
    draw.rounded_rectangle((94,280,1247,1550),radius=25,outline="#9badb5",width=4,fill="white")
    panel=placoid_panel()
    out.paste(panel,(123,306))
    draw.rounded_rectangle((1290,280,3410,1550),radius=25,outline="#9badb5",width=4,fill="white")
    draw.text((1365,322),"A  Ganoid       B  Cycloid       C  Ctenoid",font=font(54,True),fill=ink)
    resized=sourced.resize((1700,1165),Image.Resampling.LANCZOS)
    out.paste(resized,(1490,381))
    # Bottom line also prevents claiming the two panels show equal size.
    draw.text((120,1600),
              "Source A–C: Jon Houseman, CC BY-SA 3.0  |  D: original anatomical schematic  |  Not to scale",
              font=font(33),fill="#4e626c")
    TARGET.parent.mkdir(parents=True,exist_ok=True)
    out.save(TARGET,"PNG",optimize=True)
    raw=TARGET.read_bytes()
    if len(raw)<100000: raise ValueError("Unexpectedly empty teaching plate")
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    small=out.copy()
    small.thumbnail((1200,850),Image.Resampling.LANCZOS)
    small.save(PREVIEW,"PNG",optimize=True)

    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    arr=[x for x in m["figures"] if x["diagramId"]==ID]
    if len(arr)!=1 or arr[0]["lang"]!="shared" or arr[0]["path"]!="pencil_plates/fish_scale_types.png":
        raise ValueError("Expected exact shared fish-scale lesson registration")
    e=arr[0]
    old_author=e["author"]
    if old_author not in ("Chordata QA project — original numbered schematic", AUTHOR):
        raise ValueError("Unexpected author; potential overwrite of independently revised asset")
    e.update(
        size=len(raw),sha256=sha256(raw).hexdigest(),author=AUTHOR,license=LICENCE,
        sourceUrl=SOURCE_PAGE,licenseUrl=LICENCE_URL,sourceSha256=[sourced_hash],
        modifications=("Original Jon Houseman scale photograph/engraving panel proportionally "
                       "upscaled and composed beside new CHORDATA QA placoid denticle "
                       "section; no original scale letters A–C altered. Entire derivative "
                       "available under CC BY-SA 3.0."),
        keyEn=("D Placoid: basal plate, dentine, pulp cavity and enameloid cap "
               "(original schematic, lateral section). "
               "A Ganoid: rhomboid interlocking scales. B Cycloid: smooth posterior "
               "edge. C Ctenoid: comb-like posterior projections. Not to scale."),
        keyTa=("D பிளாக்காய்டு: அடித்தட்டு, டென்டின், கூழ்க்குழி, எனாமலாய்டு மேலுறை. "
               "A கேனாய்டு; B சைக்ளாய்டு (வழுவழுப்பான பின்விளிம்பு); "
               "C டீனாய்டு (சீப்புப் பற்கள் போன்ற நீட்சிகள்). "
               "படங்கள் ஒரே அளவுகோலில் வரையப்படவில்லை."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as file:
        rd=csv.DictReader(file,delimiter="\t")
        fields=rd.fieldnames
        rows=list(rd)
    match=[r for r in rows if r["diagramId"]==ID]
    if len(match)!=1: raise ValueError("Figure ledger mismatch")
    match[0]["author"]=AUTHOR
    match[0]["referenceSources"]=SOURCE_PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=fields,delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    PROVENANCE.write_text(
        "# Fish-scale teaching plate — source-credited QA\n\n"
        "Lesson ID: "+ID+"\n\n"
        "## Third-party source and attribution\n"
        "Artist: Jon Houseman; artwork: Fishscales.png (A ganoid, B cycloid, "
        "C ctenoid); page: "+SOURCE_PAGE+"\n"
        "Source original SHA-256: "+sourced_hash+"\n"
        "Licence: "+LICENCE_URL+" (CC BY-SA 3.0).\n\n"
        "## Adaptation\n"
        "The three labelled source illustrations are rendered together with "
        "a separately illustrated placoid denticle section drawn for this "
        "project. No copied placoid image and no species-specific external "
        "photographs. Entire composite is distributed under CC BY-SA 3.0; "
        "original Houseman source remains separately credited.\n"
        "Result PNG SHA-256: "+sha256(raw).hexdigest()+"\n\n"
        "## Review gates\n"
        "Scientific anatomical review, Tamil label-key review and physical "
        "Android device tests are all PENDING; 64/64 slot count unchanged.\n",
        encoding="utf-8")
    print(f"PASS: sourced four-scale plate {len(raw)} bytes ({out.width}x{out.height}), sha256={sha256(raw).hexdigest()}")
    print("No independent anatomy or Tamil approval implied.")

if __name__=="__main__":
    main()
