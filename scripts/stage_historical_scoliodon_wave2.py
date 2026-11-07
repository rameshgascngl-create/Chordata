#!/usr/bin/env python3
"""Integrate Muller-Henle (1838/1841) Scoliodon laticaudus plate, QA only."""
from pathlib import Path
from hashlib import sha256
from io import BytesIO
from urllib.request import urlopen, Request
import csv, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT/"app/src/main/assets"
DEST = ASSETS/"pencil_plates/scoliodon_external_anatomy_en.png"
MANIFEST = ASSETS/"pencil_plates/manifest.json"
LEDGER = ROOT/"docs/figure-coverage.tsv"
REVIEW = ROOT/"docs/qa-image-review/scoliodon_external_muller_henle_review.png"
REPORT = ROOT/"docs/CHORDATA_SCOLIODON_MULLER_HENLE_QA.md"
ID = "u2-scoliodon-external-labelled"
FILE = "Carcharias_laticaudus_by_muller_and_henle.png"
URL = "https://upload.wikimedia.org/wikipedia/commons/1/16/"+FILE
PAGE = "https://commons.wikimedia.org/wiki/File:"+FILE
SOURCE_REF = "https://sharks.linnaeus.naturalis.nl/linnaeus_ng/app/views/species/nsr_taxon.php?cat=TAB_DESCRIPTION&id=62733"
AUTHOR = "Johannes Muller and Friedrich Henle (1838-1841); CHORDATA QA (teaching layout)"
RIGHTS = "Public domain, original Muller-Henle 1838-1841 plate"
LICENSE_URL = "https://creativecommons.org/publicdomain/mark/1.0/"

def font(n,bold=False):
    name="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+name,n)

def download():
    req=Request(URL,headers={
        "User-Agent":"ChordataQAAcademicIllustrations/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/","Accept":"image/png"})
    with urlopen(req,timeout=50) as response:
        data=response.read(2400001)
    if not 500000<len(data)<2400000:
        raise ValueError("Unexpected historical plate byte size")
    src=Image.open(BytesIO(data));src.load()
    if src.format!="PNG" or src.size!=(1784,1184):
        raise ValueError("Original species plate media/dimensions changed")
    return src.convert("RGBA"),sha256(data).hexdigest()

def main():
    source,original_sha=download()
    out=Image.new("RGB",(3200,2530),"#fffefa")
    d=ImageDraw.Draw(out)
    ink="#1b3440"
    d.text((93,62),"Scoliodon laticaudus — external morphology",font=font(75,True),fill=ink)
    d.text((98,163),"Muller and Henle's original species plate (1838–1841)",font=font(39),fill="#536774")
    d.rounded_rectangle((76,252,3120,1810),radius=22,outline="#93a4ac",width=4,fill="white")
    illustration=ImageOps.contain(source,(2880,1470),Image.Resampling.LANCZOS)
    bg=Image.new("RGBA",illustration.size,"white")
    bg.alpha_composite(illustration)
    art=bg.convert("RGB")
    out.paste(art,(160+(2880-art.width)//2,294+(1460-art.height)//2))
    d.text((115,1840),"Diagnostic structures — modern identification key",font=font(48,True),fill=ink)
    pairs=[
      "Depressed, spade-shaped snout",
      "Small lateral eyes, no spiracles",
      "Five pairs of gill slits",
      "First dorsal fin much larger",
      "Second dorsal fin is small",
      "Pectoral and pelvic fins paired",
      "Anal fin; heterocercal tail",
      "Ventral mouth not clear in side view",
    ]
    for i,label in enumerate(pairs):
        col,row=divmod(i,4);x=126+col*1520;y=1935+row*100
        d.ellipse((x,y+14,x+26,y+39),fill="#39728c")
        d.text((x+48,y),label,font=font(32),fill=ink)
    d.line((95,2410,3090,2410),fill="#bdc8ce",width=3)
    d.text((110,2444),"Historical plate preserved without inferred leader lines or invented anatomical detail.",font=font(30),fill="#536674")
    DEST.parent.mkdir(parents=True,exist_ok=True)
    out.save(DEST,"PNG",optimize=True)
    data=DEST.read_bytes()
    if len(data)<180000:raise ValueError("Output lacks expected engraving detail")
    REVIEW.parent.mkdir(parents=True,exist_ok=True)
    small=out.copy();small.thumbnail((1200,1000),Image.Resampling.LANCZOS)
    small.save(REVIEW,"PNG",optimize=True)

    m=json.loads(MANIFEST.read_text("utf-8"))
    matches=[x for x in m["figures"] if x["diagramId"]==ID and x["lang"]=="en"]
    assert len(matches)==1 and matches[0]["path"]=="pencil_plates/scoliodon_external_anatomy_en.png"
    entry=matches[0]
    if entry["author"] not in ("CHORDATA QA — original vector anatomical schematic",AUTHOR):
        raise ValueError("Refusing to overwrite independently modified figure")
    entry.pop("svgMaster",None);entry.pop("svgSha256",None)
    entry.update(
       author=AUTHOR,license=RIGHTS,licenseUrl=LICENSE_URL,sourceUrl=PAGE,
       sourceSha256=[original_sha],referenceUrls=[PAGE,SOURCE_REF],
       modifications=("Whole unaltered historical species engraving fitted proportionally "
                      "to a white page; a modern identification key was placed outside "
                      "the engraving, with no invented arrows or anatomical relabelling."),
       keyEn=("Scoliodon laticaudus: depressed spade-shaped snout, small eyes, "
              "five paired gill slits, two dorsal fins, paired pectoral and pelvic "
              "fins, anal fin and heterocercal caudal fin. Spiracles absent. "
              "The ventral mouth cannot be verified from the lateral engraving alone."),
       keyTa=("Scoliodon laticaudus: அகன்ற தட்டையான முன்மூக்கு, சிறிய கண்கள், "
              "ஐந்து இணை செவுள் பிளவுகள், இரு முதுகுத் துடுப்புகள், "
              "மார்பு மற்றும் இடுப்புத் துடுப்புகள், மலவாய்த் துடுப்பு, "
              "சமமற்ற இருமடல் வால்துடுப்பு. பக்கத்தோற்றத்தில் கீழ்நோக்கிய "
              "வாய் தெளிவாகக் காணப்படாது."),
       visualReview="REPLACED_VISUAL_QA_PENDING",
       reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
       size=len(data),sha256=sha256(data).hexdigest(),
    )
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        rd=csv.DictReader(f,delimiter="\t");columns=rd.fieldnames;rows=list(rd)
    found=[x for x in rows if x["diagramId"]==ID]
    assert len(found)==1
    found[0]["author"]=AUTHOR
    found[0]["referenceSources"]=PAGE+" | "+SOURCE_REF
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=columns,delimiter="\t")
        wr.writeheader();wr.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
       "# Scoliodon external morphology – original historic plate (QA)\n\n"
       "Lesson diagram: "+ID+"\nOriginal artwork: Muller and Henle, Systematische "
       "Beschreibung der Plagiostomen, plate 8 (1838–1841).\nOriginal image: "+PAGE+
       "\nPublic-domain rights: "+LICENSE_URL+"\nOriginal PNG SHA-256: "+original_sha+
       "\nAdapted teaching PNG SHA-256: "+sha256(data).hexdigest()+"\n"
       "Drawing kept whole and undistorted, with separate modern English "
       "identification key. Reproductive and respiratory internal organs "
       "are not shown in this external-anatomy view. Scientific/Tamil "
       "review and physical-device acceptance are pending.\n",
       encoding="utf-8")
    print("PASS staged Scoliodon species plate:",len(data),sha256(data).hexdigest())

if __name__=="__main__":
    main()
