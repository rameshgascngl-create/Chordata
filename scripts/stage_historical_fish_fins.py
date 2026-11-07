#!/usr/bin/env python3
"""Replace fish-fin placeholder with an attributed, authentic 1898 line engraving.

This is a *generalised salmon-like bony fish*; the adipose fin is not present
in all fishes. Numbered key uses the source's actual indices, NOT the obsolete
1–5 numbering of the earlier provisional sketch.
"""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import json,csv,subprocess
from urllib.parse import quote
from urllib.request import Request,urlopen
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
TARGET=ASSETS/"pencil_plates/fish_fin_positions.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REVIEW=ROOT/"docs/qa-image-review/fish_fin_positions_review.png"
REPORT=ROOT/"docs/CHORDATA_HISTORICAL_FISH_FINS_QA.md"
DIAGRAM="u2-scales-fins-fins-labelled"
FILENAME=("FMIB_47883_Figure_of_a_Fish,_Showing_the_Location_of_Parts_Usually_"
          "Referred_to_in_Desciption_-_1_Dorsal_fin;_2_Adipose_fin;_3_Caudal_fin;_4.jpeg")
ORIGIN="https://upload.wikimedia.org/wikipedia/commons/5/5b/"+quote(FILENAME,safe="_-")
PAGE="https://commons.wikimedia.org/wiki/File:"+FILENAME
AUTHOR=("Unknown original illustrator (1898), Oregon Fish and Game Protector; "
        "University of Washington Freshwater and Marine Image Bank; CHORDATA QA layout")
RIGHTS="Public domain — 1898 Oregon Fish and Game report, UW Freshwater and Marine Image Bank"

def font(sz,bold=False):
    p="/usr/share/fonts/truetype/dejavu/"+("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(p,sz)

def source():
    req=Request(ORIGIN,headers={
        "User-Agent":"ChordataQAAnatomyIntake/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/","Accept":"image/jpeg"})
    with urlopen(req,timeout=45) as r:
        raw=r.read(1000001)
    if not (110000<len(raw)<1000000): raise ValueError("Unexpected source length")
    im=Image.open(BytesIO(raw));im.load()
    if im.format!="JPEG" or im.size!=(1369,815):
        raise ValueError("Wrong source image dimensions or format: do not stage")
    return im.convert("RGB"),sha256(raw).hexdigest()

def main():
    im,source_hash=source()
    # Isolate the numbered fish but retain all 1–19 leader anchors.
    # The original typeset caption remains available from the credited source link.
    fish=im.crop((27,4,1355,570))
    fish=ImageOps.autocontrast(ImageOps.grayscale(fish),cutoff=(2,2)).convert("RGB")
    plate=Image.new("RGB",(3200,1500),"#fffefa")
    d=ImageDraw.Draw(plate)
    ink="#18323e"
    d.text((90,62),"Fish fins — external anatomy",font=font(82,True),fill=ink)
    d.text((92,163),"Historical line engraving (1898) — generalised bony fish",
           font=font(39),fill="#43606c")
    d.rounded_rectangle((75,244,2230,1340),radius=22,outline="#a2b1ba",width=4,fill="white")
    enlarged=ImageOps.contain(fish,(2070,1020),Image.Resampling.LANCZOS)
    plate.paste(enlarged,(115+(2070-enlarged.width)//2,285+(1030-enlarged.height)//2))
    d.rounded_rectangle((2270,244,3130,1340),radius=22,outline="#a2b1ba",width=4,fill="white")
    x=2310
    d.text((x,289),"Median fins",font=font(51,True),fill=ink)
    y=374
    for key,term in [("1","Dorsal"),("2","Adipose*"),("3","Caudal"),("4","Anal")]:
        d.text((x,y),key,font=font(42,True),fill="#2b6480")
        d.text((x+85,y),term,font=font(42),fill=ink);y+=95
    d.line((x,770,3090,770),fill="#c3cbd1",width=4)
    d.text((x,800),"Paired fins",font=font(51,True),fill=ink)
    d.text((x,899),"5    Pectoral",font=font(42),fill=ink)
    d.text((x,976),"6    Pelvic (ventral)",font=font(40),fill=ink)
    d.text((x,1100),"* Adipose fin",font=font(32,True),fill="#385362")
    d.text((x,1145),"is not universal",font=font(32),fill="#385362")
    d.text((x,1191),"among fishes.",font=font(32),fill="#385362")
    d.text((92,1390),"Numbers follow the original 1898 drawing; posterior pelvic-fin position varies among taxa.",
           font=font(32),fill="#405969")
    plate.save(TARGET,"PNG",optimize=True)
    data=TARGET.read_bytes()
    REVIEW.parent.mkdir(parents=True,exist_ok=True)
    preview=plate.copy();preview.thumbnail((1100,650),Image.Resampling.LANCZOS)
    preview.save(REVIEW,"PNG",optimize=True)
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    hits=[x for x in m["figures"] if x["diagramId"]==DIAGRAM]
    if len(hits)!=1 or hits[0]["lang"]!="shared" or hits[0]["path"]!="pencil_plates/fish_fin_positions.png":
        raise ValueError("Exact lesson slot mismatch")
    e=hits[0]
    if e["author"] not in ("Chordata QA project — original numbered schematic",AUTHOR):
        raise ValueError("Refuse to replace unrecognised reviewed asset")
    e.update(
        size=len(data),sha256=sha256(data).hexdigest(),author=AUTHOR,
        license=RIGHTS,sourceUrl=PAGE,sourceSha256=[source_hash],
        licenseUrl="https://creativecommons.org/publicdomain/mark/1.0/",
        modifications=("Cropped original numbered fish from 1898 print, converted "
                       "to greyscale/high contrast and enlarged proportionally. "
                       "New English fin legend outside original engraving; "
                       "original 1–19 anatomical leaders not modified."),
        keyEn=("Original numerals: 1 dorsal, 2 adipose (not all fishes), "
               "3 caudal, 4 anal = median fins. 5 pectoral and 6 pelvic = "
               "paired fins. Other numbers in the source indicate landmarks, "
               "jaws, operculum, lateral line and body measurements."),
        keyTa=("மூலப்பட எண்கள்: 1 முதுகுத் துடுப்பு, 2 கொழுப்புத் துடுப்பு "
               "(எல்லா மீன்களிலும் இல்லை), 3 வால் துடுப்பு, "
               "4 மலவாய்த் துடுப்பு — நடுக்கோட்டுத் துடுப்புகள். "
               "5 மார்புத் துடுப்பு, 6 இடுப்புத் துடுப்பு — இணைத் துடுப்புகள்."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        rd=csv.DictReader(f,delimiter="\t"); fields=rd.fieldnames; rows=list(rd)
    found=[r for r in rows if r["diagramId"]==DIAGRAM]
    assert len(found)==1
    found[0]["author"]=AUTHOR
    found[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,delimiter="\t");wr.writeheader();wr.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
        "# CHORDATA — historic fish fins plate (QA only)\n\n"
        "Exact lesson diagram: "+DIAGRAM+"\n\n"
        "Original print (1898): Annual Reports of the Fish and Game Protector of "
        "the State of Oregon, Fifth and Sixth. University of Washington FMIB "
        "accession 47883.\nOriginal page: "+PAGE+"\nSource SHA-256: "+source_hash+"\n"
        "Author: unknown original illustrator; publisher Oregon state; "
        "distribution rights: public domain.\n"
        "Adaptation: cropped historic fish diagram and separated old small caption, "
        "converted to greyscale, enlarged proportionally; added legible English "
        "legend without overwriting the source figure. Numerals retain original "
        "meaning. Adipose fin labelled as not universal.\n"
        "PNG SHA-256: "+sha256(data).hexdigest()+"\n\n"
        "Not academically approved; no Tamil editorial approval; "
        "Android device acceptance pending. Source drawing is bony fish "
        "and is not a Scoliodon shark anatomical drawing.\n",
        encoding="utf-8")
    print(f"PASS: 1898 fish-fins line drawing staged ({plate.size}, {len(data)} bytes, sha256={sha256(data).hexdigest()})")

if __name__=="__main__":
    main()
