#!/usr/bin/env python3
"""Source-credited CC0 replacement of five weak chordate-character sketches."""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import Request,urlopen
import csv,json,subprocess
from PIL import Image,ImageDraw,ImageFont,ImageOps
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
OUTPUT=ASSETS/"pencil_plates/chordate_features.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
PREVIEW=ROOT/"docs/qa-image-review/five_chordate_characters_review.png"
PROVENANCE=ROOT/"docs/CHORDATA_FIVE_CHARACTERS_MICROVIPERA_QA.md"
DIAGRAM="u1-general-characters-five-chordate-characters"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/7/7c/General_chordate_morphology.svg"
PAGE="https://commons.wikimedia.org/wiki/File:General_chordate_morphology.svg"
AUTHOR="Microvipera (generalised chordate morphology); CHORDATA QA (layout)"
LICENSE="CC0 1.0 — original artwork dedicated to public domain"
LICENSE_URL="https://creativecommons.org/publicdomain/zero/1.0/"
KEY=[
 "1  Dorsal hollow nerve cord",
 "2  Notochord beneath nerve cord",
 "3  Pharyngeal slits",
 "4  Endostyle (thyroid homologue)",
 "5  Muscular post-anal tail",
]
def font(sz,bold=False):
    file="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+file,sz)
def source():
    req=Request(SOURCE,headers={
        "User-Agent":"ChordataQAAcademicPlate/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/","Accept":"image/svg+xml"})
    with urlopen(req,timeout=45) as response:
        raw=response.read(90000)
    if not 30000<len(raw)<90000:raise ValueError("Unexpected original source length")
    lowered=raw.lower()
    if b"<!doctype" in lowered or b"<!entity" in lowered or b"<script" in lowered or b"<foreignobject" in lowered:
        raise ValueError("Unsafe SVG active content")
    # The source is a multilingual CC0 vector with an embedded language
    # switch. CairoSVG uses its non-language fallback when needed.
    output=cairosvg.svg2png(bytestring=raw,output_width=2660)
    im=Image.open(BytesIO(output)).convert("RGBA")
    if not (2660<=im.width<=2661 and 970<=im.height<=1050):
        raise ValueError("Unexpected vector rendering proportions")
    bg=Image.new("RGBA",im.size,"white")
    bg.alpha_composite(im)
    return bg.convert("RGB"),sha256(raw).hexdigest()
def main():
    illustration,source_hash=source()
    plate=Image.new("RGB",(3100,1790),"#fffefa")
    d=ImageDraw.Draw(plate)
    ink="#1d3540"
    d.text((90,55),"Five defining characters of Chordata",font=font(83,True),fill=ink)
    d.text((94,165),"Present at some stage of the life cycle — not necessarily all in the adult",font=font(42),fill="#4d6571")
    d.rounded_rectangle((76,264,3035,1280),radius=24,fill="white",outline="#9eafb7",width=4)
    fig=ImageOps.contain(illustration,(2770,915),Image.Resampling.LANCZOS)
    plate.paste(fig,(155+(2780-fig.width)//2,304+(940-fig.height)//2))
    d.text((110,1340),"Anatomical identification key",font=font(53,True),fill=ink)
    for i,line in enumerate(KEY):
        c=i//3;r=i%3
        x=135+c*1500;y=1438+r*79
        d.text((x,y),line,font=font(39),fill=ink)
    d.text((107,1720),"Original artwork: Microvipera (CC0 1.0). This overview is schematic, not species-specific.",font=font(32),fill="#50646e")
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    plate.save(OUTPUT,"PNG",optimize=True)
    raw=OUTPUT.read_bytes()
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    preview=plate.copy();preview.thumbnail((1200,770),Image.Resampling.LANCZOS)
    preview.save(PREVIEW,"PNG",optimize=True)
    m=json.loads(MANIFEST.read_text("utf-8"))
    matches=[x for x in m["figures"] if x["diagramId"]==DIAGRAM]
    if len(matches)!=1 or matches[0]["lang"]!="shared" or matches[0]["path"]!="pencil_plates/chordate_features.png":
        raise ValueError("Wrong chordate characteristics source slot")
    e=matches[0]
    if e.get("author") not in ("Chordata QA project — original numbered schematic",AUTHOR):
        raise ValueError("Refuse overwrite of separately reviewed artwork")
    e.update(
        size=len(raw),sha256=sha256(raw).hexdigest(),author=AUTHOR,license=LICENSE,
        licenseUrl=LICENSE_URL,sourceUrl=PAGE,sourceSha256=[source_hash],
        modifications=("CC0 2025 vector morphology rendered at 2660px width into offline "
                       "PNG with proportions and original anatomical mark-up intact; "
                       "additional standalone five-feature key placed below."),
        keyEn=("Notochord; dorsal hollow nerve cord; pharyngeal slits; "
               "endostyle (homologue of thyroid gland); muscular post-anal tail. "
               "Characters may be present only in the larva or embryo."),
        keyTa=("முதுகுநாண்; முதுகுப்புறக் குழல் நரம்பு வடம்; தொண்டைப் பிளவுகள்; "
               "எண்டோஸ்டைல் (தைராய்டு சுரப்பியின் ஒத்தமை உறுப்பு); "
               "மலவாய்க்குப் பின்புறத் தசை வால். "
               "சில பண்புகள் கரு அல்லது இளவுயிரி நிலையில் மட்டுமே காணப்படலாம்."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        visualReview="REPLACED_VISUAL_QA_PENDING")
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t");fields=reader.fieldnames;rows=list(reader)
    match=[x for x in rows if x["diagramId"]==DIAGRAM]
    if len(match)!=1:raise ValueError("Figure coverage ID not unique")
    match[0]["author"]=AUTHOR;match[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t");w.writeheader();w.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    PROVENANCE.write_text(
        "# Five chordate characters — source replacement (QA only)\n\n"
        "Figure ID: "+DIAGRAM+"\n"
        "Original drawing: Microvipera (16 September 2025).\n"
        "Original file: "+PAGE+"\n"
        "Rights: CC0 1.0, "+LICENSE_URL+"\n"
        "Downloaded source SHA-256: "+source_hash+"\n"
        "Installed source-credited PNG SHA-256: "+sha256(raw).hexdigest()+"\n\n"
        "Changes: SVG source rendered into a 2660 px-wide image; enlarged "
        "at the same aspect ratio; added English five-character key and scope "
        "note outside source illustration. No third-party fonts or SVGs shipped.\n"
        "All 64 slots unchanged. Anatomy/Tamil/device sign-off PENDING.\n",
        encoding="utf-8")
    print(f"STAGED: five chordate characters ({len(raw)} bytes, SHA256={sha256(raw).hexdigest()})")
if __name__=="__main__":
    main()
