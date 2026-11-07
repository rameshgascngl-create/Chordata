#!/usr/bin/env python3
"""Integrate George Howard Parker 1928 pigeon female tract with original male/female schematic.

Exactly one English-labelled lesson PNG changes. The SVG master remains an
editable original; only raster PNGs are installed in the native Android app.
"""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import csv
import json
import subprocess
from urllib.request import Request, urlopen

import cairosvg
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
SRC = ROOT / "docs/original_plate_svg/pigeon_urinogenital_en.svg"
DEST = ASSETS / "pencil_plates/pigeon_urinogenital_en.png"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
REVIEW = ROOT / "docs/qa-image-review/pigeon_urinogenital_1928_review.png"
REPORT = ROOT / "docs/CHORDATA_PARKER_PIGEON_1928_QA.md"
ID = "u5-columba-urinogenital"
URL = "https://upload.wikimedia.org/wikipedia/commons/4/4f/Creation_by_Evolution_%281928%29_p037_reproductive_organs_of_a_female_pigeon.png"
PAGE = "https://commons.wikimedia.org/wiki/File:Creation_by_Evolution_(1928)_p037_reproductive_organs_of_a_female_pigeon.png"
CAPTION = "https://en.wikisource.org/wiki/Creation_by_Evolution/Vestigial_Organs"
AUTHOR = "CHORDATA QA original comparative diagram; George Howard Parker (1928) female pigeon anatomy"
RIGHTS = "Public domain 1928 female source (Parker died 1955); original QA schematic retained"
PDM = "https://creativecommons.org/publicdomain/mark/1.0/"

def ft(size, bold=False):
    file = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + file, size)

def obtain():
    request = Request(URL, headers={
        "User-Agent": "ChordataQAAnatomy/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer": "https://commons.wikimedia.org/",
        "Accept": "image/png",
    })
    with urlopen(request, timeout=50) as response:
        binary = response.read(700001)
    if not (100000 < len(binary) < 700000):
        raise ValueError("Unexpected source file size")
    img = Image.open(BytesIO(binary))
    img.load()
    if img.format != "PNG" or img.size != (720,1200):
        raise ValueError("Parker drawing dimensions or format changed")
    return img.convert("RGB"), sha256(binary).hexdigest()

def stage():
    historical, source_hash = obtain()
    svg = SRC.read_bytes()
    if b"<svg" not in svg[:1000] or b"<script" in svg.lower():
        raise ValueError("Original SVG source invalid")
    original_sha = sha256(svg).hexdigest()
    rendered = cairosvg.svg2png(bytestring=svg, output_width=1800, output_height=1120)
    overview = Image.open(BytesIO(rendered)).convert("RGB")
    if overview.size != (1800,1120):
        raise ValueError("Original comparison layout changed")
    # Crop only duplicate title, retaining both species panels and the bottom note.
    overview = overview.crop((75,210,1740,1050))
    out = Image.new("RGB", (3360,1900), "#fffefa")
    d = ImageDraw.Draw(out)
    ink = "#1b3440"
    d.text((100,65), "Pigeon urinogenital anatomy — both sexes", font=ft(76,True), fill=ink)
    d.text((105,165), "Male/female comparison and a historical female-tract detail", font=ft(39),fill="#455e6b")
    d.rounded_rectangle((80,255,2230,1710), radius=24, outline="#9eafb8", width=4, fill="white")
    d.text((120,292), "A  Original comparative anatomy schematic", font=ft(43,True), fill=ink)
    large = ImageOps.contain(overview,(2060,1260),Image.Resampling.LANCZOS)
    out.paste(large,(120+(2060-large.width)//2,365+(1250-large.height)//2))
    d.rounded_rectangle((2280,255,3285,1710), radius=24, outline="#9eafb8", width=4, fill="white")
    d.text((2320,297), "B  Female pigeon (1928)", font=ft(43,True), fill=ink)
    d.text((2320,350), "George Howard Parker", font=ft(33), fill="#455e6b")
    detailed = ImageOps.contain(historical,(845,1110),Image.Resampling.LANCZOS)
    out.paste(detailed,(2340+(860-detailed.width)//2,410+(1120-detailed.height)//2))
    d.text((2320,1560), "O    Left ovary", font=ft(35,True),fill=ink)
    d.text((2320,1604), "Od   Left oviduct", font=ft(35,True),fill=ink)
    d.text((2320,1648), "V    Vestigial right oviduct", font=ft(30,True),fill=ink)
    d.text((105,1767), "Original project schematic + Parker (1928), public domain. Not to scale.",
           font=ft(35), fill="#46606c")
    d.text((105,1823), "Urinary bladder absent in pigeons. Independent scientific review pending.",
           font=ft(33),fill="#46606c")
    out.save(DEST,format="PNG",optimize=True)
    png = DEST.read_bytes()
    REVIEW.parent.mkdir(parents=True,exist_ok=True)
    small = out.copy()
    small.thumbnail((1200,800),Image.Resampling.LANCZOS)
    small.save(REVIEW,"PNG",optimize=True)
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    matches = [v for v in m["figures"] if v["diagramId"] == ID and v["lang"] == "en"]
    if len(matches)!=1 or matches[0]["path"]!="pencil_plates/pigeon_urinogenital_en.png":
        raise ValueError("Wrong lesson or asset")
    entry=matches[0]
    if entry["author"] not in ("CHORDATA QA — original vector anatomical schematic",AUTHOR):
        raise ValueError("Refusing to replace unknown edited source")
    entry.update(
        size=len(png), sha256=sha256(png).hexdigest(), author=AUTHOR,
        license=RIGHTS, licenseUrl=PDM, sourceUrl=PAGE,
        sourceSha256=[source_hash], originalSvgSha256=original_sha,
        sourceCaptionUrl=CAPTION,
        modifications=("The original male/female diagram was rasterised and cropped to anatomical panels from its retained SVG "
                       "master; a public-domain 1928 female pigeon drawing was separately "
                       "scaled without changing labels, and O/Od/V English key placed outside "
                       "historical ink; full composite saved as offline PNG."),
        keyEn=("Male: paired testes and vasa deferentia. Both sexes: paired kidneys "
               "and ureters, cloaca; no urinary bladder. Female: functional left "
               "ovary and left oviduct. Historical panel O: left ovary; Od: left "
               "oviduct; V: vestigial right oviduct."),
        keyTa=("ஆண்: இணை விரைகளும் விந்துக்குழாய்களும். பெண்: செயல்படும் இடது "
               "அண்டகமும் இடது அண்டநாளமும். இருபாலிலும் இணைச் சிறுநீரகங்களும் "
               "சிறுநீர்க்குழாய்களும் கழிவறையும் உள்ளன; சிறுநீர்ப்பை இல்லை. "
               "வரலாற்றுப் படத்தில் O இடது அண்டகம், Od இடது அண்டநாளம், "
               "V எச்சமான வலது அண்டநாளம்."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as stream:
        reader=csv.DictReader(stream,delimiter="\t")
        fields=reader.fieldnames
        rows=list(reader)
    found=[row for row in rows if row["diagramId"]==ID]
    if len(found)!=1: raise ValueError("Figure coverage ID not unique")
    found[0]["author"]=AUTHOR
    found[0]["referenceSources"]=PAGE+" | "+CAPTION
    with LEDGER.open("w",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
        "# Provisional pigeon male/female reproductive anatomy\n\n"
        "Exact diagram: "+ID+"\nSource detail: "+PAGE+
        "\nCaption evidence: "+CAPTION+
        "\nArtist: George Howard Parker (1928), original QA male/female SVG.\n"
        "Public domain source in USA (published 1928) and India (Parker died 1955).\n"
        "Parker PNG source SHA-256: "+source_hash+
        "\nExisting SVG master SHA-256: "+original_sha+
        "\nAdapted lesson PNG SHA-256: "+sha256(png).hexdigest()+
        "\nModifications: SVG rasterised, female scan resized proportionally, "
        "original O/Od/V annotations retained, explanatory English key separated.\n"
        "Scientific review, Tamil editorial review and physical-device tests: PENDING.\n",
        encoding="utf-8")
    print("STAGED PIGEON QA", len(png), sha256(png).hexdigest())

if __name__=="__main__":
    stage()
