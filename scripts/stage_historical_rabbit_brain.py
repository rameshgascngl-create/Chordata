#!/usr/bin/env python3
"""Combine an original rabbit lateral-brain schematic with public-domain dorsal anatomy.

The original raster is recovered byte-for-byte from a PINNED Git commit to
avoid nested re-imports on rerun. Never use the 1875 word 'rodent' for rabbits:
modern rabbits are lagomorphs. Image shipped to Android is PNG only.
"""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
import csv
import json
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
ID="u5-rabbit-brain"
TARGET=ASSETS/"pencil_plates/rabbit_brain_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
PREVIEW=ROOT/"docs/qa-image-review/rabbit_brain_dorsal_comparison_review.png"
PROVENANCE=ROOT/"docs/CHORDATA_RABBIT_BRAIN_1875_QA.md"
BASELINE="e3f3db127861a81dd0a80be3765dba3c93fbcfab"
EXPECTED="1a71def6fdaeb113250b345f645b8f7751de5b10ba2343d296eaa9cb23174b48"
BASE_PATH="app/src/main/assets/pencil_plates/rabbit_brain_en.png"
SOURCE_PAGE="https://commons.wikimedia.org/wiki/File:PSM_V07_D065_Brain_of_rabbit.jpg"
ORIGINAL="https://upload.wikimedia.org/wikipedia/commons/e/ef/PSM_V07_D065_Brain_of_rabbit.jpg"
CONTEXT="https://en.wikisource.org/wiki/Popular_Science_Monthly/Volume_7/May_1875/Evolution_and_the_After-Life"
CREATOR="CHORDATA QA original rabbit lateral schematic; unknown illustrator, Popular Science Monthly (1875), dorsal view"
LICENCE="Public domain — 1875 anatomy figure; CHORDATA QA original schematic"
LICENCE_URL="https://creativecommons.org/publicdomain/mark/1.0/"

def ft(n,bold=False):
    fname="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+fname,n)

def source():
    req=Request(ORIGINAL,headers={
        "User-Agent":"ChordataQAAnatomyIntake/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/",
        "Accept":"image/jpeg"})
    with urlopen(req,timeout=45) as response:
        raw=response.read(180000)
    if not 15000<len(raw)<180000:
        raise ValueError("Unexpected 1875 rabbit-brain source length")
    im=Image.open(BytesIO(raw))
    im.load()
    if im.format!="JPEG" or im.size!=(392,908):
        raise ValueError("Historical rabbit-brain source changed")
    return im.convert("RGB"),sha256(raw).hexdigest()

def original_qa():
    raw=subprocess.run(["git","show",BASELINE+":"+BASE_PATH],
                       cwd=ROOT,check=True,capture_output=True).stdout
    if sha256(raw).hexdigest()!=EXPECTED:
        raise ValueError("Original project brain image digest changed")
    im=Image.open(BytesIO(raw));im.load()
    if im.format!="PNG" or im.size!=(1800,1120):
        raise ValueError("Unexpected original project lateral brain schematic")
    return im.convert("RGB")

def main():
    historical,source_hash=source()
    lateral=original_qa()
    canvas=Image.new("RGB",(3360,1810),"#fffefa")
    d=ImageDraw.Draw(canvas)
    ink="#19333f"
    d.text((98,60),"Rabbit brain — complementary anatomical views",font=ft(76,True),fill=ink)
    d.text((104,155),"A: original lateral landmarks  |  B: historical dorsal anatomy (1875)",
           font=ft(38),fill="#46606c")
    d.rounded_rectangle((82,242,1935,1635),radius=23,outline="#9cabb4",width=4,fill="white")
    d.rounded_rectangle((1975,242,3280,1635),radius=23,outline="#9cabb4",width=4,fill="white")
    d.text((118,282),"A  Rabbit brain, lateral schematic",font=ft(42,True),fill=ink)
    original_display=ImageOps.contain(lateral,(1740,1190),Image.Resampling.LANCZOS)
    canvas.paste(original_display,(143+(1740-original_display.width)//2,
                                  385+(1180-original_display.height)//2))
    d.text((2014,284),"B  Rabbit brain, dorsal view",font=ft(42,True),fill=ink)
    historical=ImageOps.autocontrast(ImageOps.grayscale(historical),cutoff=(1,1)).convert("RGB")
    ref=ImageOps.contain(historical,(525,1110),Image.Resampling.LANCZOS)
    canvas.paste(ref,(2020+(540-ref.width)//2,414+(1120-ref.height)//2))
    d.text((2600,450),"1875 source key",font=ft(39,True),fill=ink)
    y=560
    for number,label in [
        ("1","Olfactory bulbs"),("2","Cerebral hemispheres"),
        ("3","Cerebellum"),("4","Spinal cord")
    ]:
        d.text((2600,y),number,font=ft(42,True),fill="#296b87")
        d.text((2658,y),label,font=ft(34),fill=ink)
        y+=175
    d.line((2590,1320,3210,1320),width=4,fill="#c6ced2")
    d.text((2600,1370),"Rabbits belong to",font=ft(34),fill=ink)
    d.text((2600,1420),"Lagomorpha, NOT",font=ft(34,True),fill="#305d70")
    d.text((2600,1470),"Rodentia.",font=ft(34,True),fill="#305d70")
    d.text((100,1690),"Historic caption has a duplicated numeral; key follows the original drawing's labels 1–4.",
           font=ft(32),fill="#465e68")
    d.text((100,1745),"Illustrations are not to scale; independent scientific review remains pending.",
           font=ft(32),fill="#465e68")
    TARGET.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(TARGET,"PNG",optimize=True)
    output=TARGET.read_bytes()
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    small=canvas.copy();small.thumbnail((1200,750),Image.Resampling.LANCZOS)
    small.save(PREVIEW,"PNG",optimize=True)
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    found=[f for f in manifest["figures"] if f["diagramId"]==ID and f["lang"]=="en"]
    if len(found)!=1 or found[0]["path"]!="pencil_plates/rabbit_brain_en.png":
        raise ValueError("Rabbit brain lesson mapping missing")
    e=found[0]
    if e["author"] not in ("CHORDATA QA — original computer-assisted anatomical schematic",CREATOR):
        raise ValueError("Refuse to change independently modified/approved source")
    e.update(
        size=len(output),sha256=sha256(output).hexdigest(),author=CREATOR,
        license=LICENCE,licenseUrl=LICENCE_URL,sourceUrl=SOURCE_PAGE,
        sourceCaptionUrl=CONTEXT,sourceSha256=[source_hash],
        originalBaselineSha256=EXPECTED,
        modifications=("Original QA rabbit-brain lateral schematic restored "
                       "byte-for-byte from pinned baseline commit; 1875 public-domain "
                       "rabbit dorsal outline contrast adjusted and enlarged without "
                       "distortion; modern English key placed outside historical ink. "
                       "Historical misclassification 'rodent' and duplicated caption "
                       "number explicitly corrected."),
        keyEn=("A lateral: olfactory bulbs, hemispheres, cerebellum, "
               "medulla oblongata and spinal cord. B dorsal: 1 olfactory bulbs; "
               "2 cerebral hemispheres; 3 cerebellum; 4 spinal cord. "
               "Modern classification: order Lagomorpha, NOT Rodentia."),
        keyTa=("A பக்கவாட்டுத் தோற்றம்: நுகர்ச்சிக் குமிழ்கள், பெருமூளை அரைக்கோளங்கள், "
               "சிறுமூளை, முகுளம், தண்டுவடம். B முதுகுப்புறத் தோற்றம்: "
               "1 நுகர்ச்சிக் குமிழ்கள், 2 பெருமூளை அரைக்கோளங்கள், "
               "3 சிறுமூளை, 4 தண்டுவடம். முயல் Lagomorpha வரிசையைச் சார்ந்தது."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as file:
        reader=csv.DictReader(file,delimiter="\t")
        fields=reader.fieldnames
        rows=list(reader)
    rows_match=[row for row in rows if row["diagramId"]==ID]
    if len(rows_match)!=1: raise ValueError("Figure ledger mismatch")
    rows_match[0]["author"]=CREATOR
    rows_match[0]["referenceSources"]=SOURCE_PAGE+" | "+CONTEXT
    with LEDGER.open("w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=fields,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    PROVENANCE.write_text(
        "# Provisional historical rabbit brain comparison\n\n"
        "Diagram: "+ID+"\n"
        "Original dorsal drawing: anonymous, Popular Science Monthly 7 (1875): "+
        SOURCE_PAGE+"\nCaption and historical taxonomy: "+CONTEXT+"\n"
        "Public domain: "+LICENCE_URL+"\n"
        "Downloaded source SHA-256: "+source_hash+"\n"
        "Original project lateral PNG SHA-256: "+EXPECTED+"\n"
        "Composite PNG SHA-256: "+sha256(output).hexdigest()+"\n\n"
        "Adaptation: original lateral panel preserved from pinned Git revision; "
        "historical dorsal drawing enhanced in contrast and resized; all labels "
        "placed externally. 1875 caption has duplicated numeral and erroneously "
        "places rabbit among rodents; the updated plate uses modern Lagomorpha.\n"
        "Scientific/Tamil review and Android physical-device approval pending.\n",
        encoding="utf-8")
    print("STAGED rabbit brain QA",len(output),sha256(output).hexdigest())

if __name__=="__main__":
    main()
