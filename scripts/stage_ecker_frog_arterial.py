#!/usr/bin/env python3
"""Stage a legally reusable, source-attributed frog arterial system figure.

Extract precisely Fig. 143 from Ecker/Haslam's 1889 Frog Anatomy eBook,
not an arbitrary adjacent image; keep the current image if mapping fails.
"""
import csv
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
PNG=ASSETS/"pencil_plates/frog_arterial_system_en.png"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_ECKER_FROG_ARTERIAL_QA.md"
PREVIEW=ROOT/"docs/qa-image-review/frog_arterial_system_review.png"
DIAGRAM="u3-rana-arterial-system"
PAGE="https://www.gutenberg.org/cache/epub/77560/pg77560-images.html"
CREATOR="Alexander Ecker, The Anatomy of the Frog (1889), English trans. George Haslam; CHORDATA QA (layout)"
RIGHTS="Public domain — illustrated zoological text published 1889"

def digest(data): return hashlib.sha256(data).hexdigest()

def fetch(url):
    req=Request(url,headers={
        "User-Agent":"ChordataQAAcademicIntake/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Accept":"text/html,image/png,image/jpeg,*/*",
    })
    with urlopen(req,timeout=50) as response:
        raw=response.read(7000001)
    if len(raw)>7000000 or len(raw)<1000:
        raise ValueError("Unexpected Ecker source file length")
    return raw

def locate_img(html):
    soup=BeautifulSoup(html,"html.parser")
    candidates=[]
    for textnode in soup.find_all(string=re.compile(r"Fig[.]?\s*143\b",re.I)):
        node=textnode.parent
        for _ in range(4):
            if node is None: break
            img=node.find("img")
            if img and img.get("src"):
                surrounding=node.get_text(" ",strip=True)
                if "arterial system" in surrounding.lower() and "esculenta" in surrounding.lower():
                    candidates.append((img.get("src"),surrounding[:240]))
                    break
            node=node.parent
    candidates=list(dict.fromkeys(candidates))
    if len(candidates)!=1:
        raise ValueError("Expected exactly one illustration connected to Ecker fig. 143, got "+repr(candidates))
    return urljoin(PAGE,candidates[0][0]),candidates[0][1]

def font(size,bold=False):
    fn="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+fn,size)

def main():
    html=fetch(PAGE)
    src,caption=locate_img(html.decode("utf-8",errors="replace"))
    picture_bytes=fetch(src)
    image=Image.open(BytesIO(picture_bytes))
    image.load()
    if image.format not in ("PNG","JPEG") or min(image.size)<250:
        raise ValueError("Fig 143 source image missing adequate legibility")
    original=image.convert("RGB")
    # Preserve historical arterial branching; explanatory key is separate
    # rather than overwriting fine arteries or posing as a new dissection.
    canvas=Image.new("RGB",(2500,2060),"#fffefa")
    draw=ImageDraw.Draw(canvas)
    draw.text((94,62),"Frog arterial system",font=font(83,True),fill="#172f3b")
    draw.text((103,162),"Rana esculenta — Ecker & Haslam, 1889, Fig. 143",
              font=font(39),fill="#304956")
    draw.rounded_rectangle((85,240,1360,1960),radius=22,
                           outline="#8ea1ab",width=3,fill="white")
    art=ImageOps.contain(original,(1200,1600),Image.Resampling.LANCZOS)
    canvas.paste(art,(125+(1190-art.width)//2,275+(1640-art.height)//2))
    x=1440
    draw.text((x,270),"Lettered structures",font=font(52,True),fill="#172f3b")
    key=[
        ("I","Carotid arch"),("II","Systemic arch"),
        ("III","Pulmocutaneous arch"),("T","Truncus arteriosus"),
        ("A","Dorsal aorta"),("ca","Carotid artery"),
        ("P","Pulmonary artery"),("c","Cutaneous artery"),
        ("s","Subclavian artery"),("v","Vertebral artery"),
        ("ic","Iliac arteries"),("ug","Urinogenital arteries"),
        ("J","Mesenteric artery"),("d","Carotid gland")
    ]
    y=377
    for abbrev,label in key:
        draw.text((x,y),abbrev,font=font(38,True),fill="#25566e")
        draw.text((x+195,y),label,font=font(34),fill="#2c424e")
        y+=102
    draw.text((x,1880),"Historical species-specific schema.",font=font(29),fill="#465a62")
    draw.text((x,1920),"Scientific review pending.",font=font(29),fill="#465a62")
    canvas.save(PNG,"PNG",optimize=True)
    output=PNG.read_bytes()
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    short=canvas.copy()
    short.thumbnail((950,950),Image.Resampling.LANCZOS)
    short.save(PREVIEW,"PNG",optimize=True)
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    found=[f for f in m["figures"] if f["diagramId"]==DIAGRAM and f["lang"]=="en"]
    assert len(found)==1 and found[0]["path"]=="pencil_plates/frog_arterial_system_en.png"
    entry=found[0]
    for k in ("svgMaster","svgSha256"):
        entry.pop(k,None)
    entry.update(
        size=len(output),sha256=digest(output),author=CREATOR,
        license=RIGHTS,sourceUrl=PAGE,
        licenseUrl="https://www.gutenberg.org/policy/license.html",
        sourceImageUrl=src,sourceSha256=[digest(picture_bytes)],
        modifications="Isolated historically published Fig. 143, proportionally resized with Lanczos and placed alongside an English key; historical branching ink unchanged.",
        keyEn="Carotid, systemic and pulmocutaneous arches in Rana esculenta; exact historical source diagram, not a modern medical protocol.",
        keyTa="ராணா எஸ்குலென்டா: தலைத் தமனி வளைவு, உடல் தமனி வளைவு, நுரையீரல்-தோல் தமனி வளைவு; வரைபடத்தில் ஆங்கிலக் குறியீடுகள்.",
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(m,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        rd=csv.DictReader(f,delimiter="\t"); fields=rd.fieldnames; rows=list(rd)
    matches=[x for x in rows if x["diagramId"]==DIAGRAM]
    assert len(matches)==1
    matches[0]["author"]=CREATOR
    matches[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,delimiter="\t")
        wr.writeheader();wr.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    REPORT.write_text(
        "# CHORDATA Frog arterial system — source-credited 1889 QA\n\n"
        "Figure ID: "+DIAGRAM+"\nSource: "+PAGE+"\nSpecific image: "+src+
        "\nCaption recovered: "+caption+"\n"
        "Author: Alexander Ecker (1889), English translation by George Haslam.\n"
        "Reuse: public domain historical original, Gutenberg digitisation/terms acknowledged.\n"
        "Image SHA-256: "+digest(picture_bytes)+"\n"
        "Derivative PNG SHA-256: "+digest(output)+"\n"
        "Changes: original Fig. 143 isolated, scaled proportionally, and separate English label key added.\n\n"
        "Provisional morphology only; exact lesson section, all figure mappings and Tamil lesson narrative unchanged.\n"
        "Human scientific, Tamil and Android device acceptance remain pending.\n",
        encoding="utf-8")
    print("PASS: credited Ecker/Haslam 1889 frog arterial plate from",src)
    print("PNG:",len(output),"bytes",digest(output),"source:",image.size)

if __name__=="__main__":
    main()
