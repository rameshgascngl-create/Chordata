#!/usr/bin/env python3
"""Stage a fully credited, anatomically labelled avian flight-muscle PNG.

L. Shyamal, Wing Muscles, color.svg (2012), CC BY-SA 2.5 Generic.
The source is retained by SHA-256 and the lesson PNG derivative is under
the same licence. The existing original vector source stays untouched.
"""
from pathlib import Path
from urllib.request import urlopen, Request
from io import BytesIO
from hashlib import sha256
import csv, json, subprocess

import cairosvg
from PIL import Image, ImageDraw, ImageOps, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
OUTPUT=ASSETS/"pencil_plates/avian_flight_muscles_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
PREVIEW=ROOT/"docs/qa-image-review/avian_flight_muscles_review.png"
PROVENANCE=ROOT/"docs/CHORDATA_AVIAN_FLIGHT_MUSCLES_QA.md"
DIAGRAM="u5-flight-adaptations-flight-muscles"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/0/02/Wing_Muscles%2C_color.svg"
PAGE="https://commons.wikimedia.org/wiki/File:Wing_Muscles,_color.svg"
CREATOR="L. Shyamal (2012), Wing Muscles, color.svg; CHORDATA QA (layout and explanatory key)"
LICENCE="CC BY-SA 2.5 Generic — derived PNG and annotations"
LICENCE_URL="https://creativecommons.org/licenses/by-sa/2.5/"

def ft(n,bold=False):
    name="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+name,n)

def fetch():
    req=Request(SOURCE,headers={
        "User-Agent":"ChordataQAAnatomicalPlate/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/",
        "Accept":"image/svg+xml",
    })
    with urlopen(req,timeout=45) as stream: raw=stream.read(100001)
    if not (12000<len(raw)<100000):
        raise ValueError("Unexpected wing-muscle SVG size")
    lower=raw.lower()
    if b"<svg" not in lower[:3000]:
        raise ValueError("Original is not SVG")
    if any(term in lower for term in [b"<script",b"<foreignobject",b"javascript:",b"<!doctype",b"<image",b"@import",b"<use href="]):
        raise ValueError("Embedded active or external graphics not accepted")
    return raw

def stage():
    src=fetch()
    image_png=cairosvg.svg2png(bytestring=src,output_width=2720)
    im=Image.open(BytesIO(image_png));im.load()
    if im.width!=2720 or im.height<1100:
        raise ValueError("Source drawing raster dimensions unexpected")
    rgba=im.convert("RGBA")
    neutral=Image.new("RGBA",rgba.size,"white")
    neutral.alpha_composite(rgba)
    source_rgb=neutral.convert("RGB")
    canvas=Image.new("RGB",(3450,1790),"#fffefa")
    d=ImageDraw.Draw(canvas)
    dark="#18313d"
    d.text((100,58),"Bird flight muscles and wing mechanics",font=ft(81,True),fill=dark)
    d.text((100,157),"Pectoralis (downstroke) and supracoracoideus (upstroke)",font=ft(43),fill="#415a65")
    d.rounded_rectangle((85,260,3270,1330),radius=25,outline="#a3b1b8",width=4,fill="white")
    fit=ImageOps.contain(source_rgb,(3150,1000),Image.Resampling.LANCZOS)
    canvas.paste(fit,(105+(3150-fit.width)//2,289+(1010-fit.height)//2))
    d.rounded_rectangle((85,1370,3270,1670),radius=22,outline="#a3b1b8",width=3,fill="#f7f9f9")
    d.text((130,1410),"Pectoralis",font=ft(50,True),fill="#923d42")
    d.text((130,1480),"Powerful downstroke: humerus pulled downwards.",font=ft(33),fill=dark)
    d.text((1710,1410),"Supracoracoideus",font=ft(50,True),fill="#be7c32")
    d.text((1710,1480),"Upstroke: tendon redirects pull over shoulder.",font=ft(33),fill=dark)
    d.text((115,1720),"Original art: L. Shyamal (CC BY-SA 2.5). Source anatomy preserved; English teaching key added.",
           font=ft(29),fill="#526873")
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(OUTPUT,format="PNG",optimize=True)
    raw=OUTPUT.read_bytes()
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    thumb=canvas.copy();thumb.thumbnail((1200,680),Image.Resampling.LANCZOS)
    thumb.save(PREVIEW,"PNG",optimize=True)
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    arr=[f for f in manifest["figures"] if f["diagramId"]==DIAGRAM and f["lang"]=="en"]
    if len(arr)!=1 or arr[0]["path"]!="pencil_plates/avian_flight_muscles_en.png":
        raise ValueError("Exact lesson registration missing")
    entry=arr[0]
    if entry["author"] not in ("CHORDATA QA — original vector anatomical schematic",CREATOR):
        raise ValueError("Refusing to replace unexpected artwork")
    entry.pop("svgMaster",None);entry.pop("svgSha256",None)
    entry.update(
        size=len(raw),sha256=sha256(raw).hexdigest(),author=CREATOR,
        license=LICENCE,licenseUrl=LICENCE_URL,sourceUrl=PAGE,
        sourceSha256=[sha256(src).hexdigest()],
        modifications=("Original L. Shyamal CC BY-SA 2.5 SVG converted to RGB PNG "
                       "at 2720px width with white background; anatomy, English "
                       "original labels, arrows and muscle geometry unchanged. "
                       "Separate classroom caption added below source drawing; "
                       "composite derivative retains CC BY-SA 2.5."),
        keyEn=("The pectoralis powers the downstroke. Supracoracoideus contraction "
               "lifts the humerus through a tendon redirected around the "
               "shoulder/triosseal pulley. Coracoid, furcula, scapula and "
               "keel of sternum support flight musculature."),
        keyTa=("பெக்டோராலிஸ் தசை இறக்கையின் கீழ்நோக்கிய அசைவுக்கு உதவுகிறது. "
               "சுப்ராகோரக்காய்டியஸ் தசையின் தசைநாண் தோள்பகுதியில் "
               "திசைமாற்றப்பட்டு இறக்கையை மேலே உயர்த்துகிறது. "
               "படத்தினுள் ஆங்கிலப் பெயரிடல் மட்டும் உள்ளது."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t")
        fields=reader.fieldnames
        rows=list(reader)
    found=[r for r in rows if r["diagramId"]==DIAGRAM]
    if len(found)!=1: raise ValueError("Figure ledger mapping changed")
    found[0]["author"]=CREATOR
    found[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    PROVENANCE.write_text(
        "# Bird flight-muscle anatomical plate — CHORDATA QA\n\n"
        "Diagram ID: "+DIAGRAM+"\n"
        "Illustrator: L. Shyamal (2012), original colour muscle anatomy SVG.\n"
        "Original source: "+PAGE+"\n"
        "Licence: "+LICENCE_URL+" (Creative Commons BY-SA 2.5, applies to modified PNG).\n"
        "Original SVG SHA-256: "+sha256(src).hexdigest()+"\n"
        "Derived PNG SHA-256: "+sha256(raw).hexdigest()+"\n"
        "Modification: original source labels and arrows remain unchanged, "
        "rasterised as 2720px-wide drawing, white background, added English "
        "classification of pectoralis downstroke and supracoracoideus upstroke.\n"
        "No independent scientific or Tamil editor approval, no physical device acceptance.\n",
        encoding="utf-8")
    print("PASS: source-credited avian flight muscle PNG",len(raw),sha256(raw).hexdigest())
    print("Rights: L. Shyamal, CC BY-SA 2.5; 64 placements preserved; REVIEW PENDING.")

if __name__=="__main__":
    stage()
