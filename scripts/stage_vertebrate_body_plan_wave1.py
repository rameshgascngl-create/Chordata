#!/usr/bin/env python3
"""Replace the misleading generic Vertebrata silhouette with two credited source illustrations.

Source A: Chiswick Chap, Vertebrate_body_plan.svg, CC BY-SA 4.0.
Source B: Uwe Gille, Fish-anatomy.svg, CC BY 2.5 (chosen from dual licence).
The rendered PNG is the ONLY new image shipped in the native Android app.
This is still a provisional teaching illustration, not independent approval.
"""
from __future__ import annotations
import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
TARGET = ASSETS / "pencil_plates/vertebrate_organs_en.png"
PREVIEW = ROOT / "docs/qa-image-review/vertebrate_organs_review.png"
PROVENANCE = ROOT / "docs/CHORDATA_VERTEBRATE_BODY_PLAN_WAVE1_QA.md"
ID = "u1-vertebrata-characters-vertebrate-anatomy"

SOURCES = [
    {
        "name": "General vertebrate body plan",
        "artist": "Chiswick Chap",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/da/Vertebrate_body_plan.svg",
        "page": "https://commons.wikimedia.org/wiki/File:Vertebrate_body_plan.svg",
        "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "dimensions": (1280,302),
    },
    {
        "name": "Teleost internal anatomy",
        "artist": "Uwe Gille",
        "url": "https://upload.wikimedia.org/wikipedia/commons/b/b0/Fish-anatomy.svg",
        "page": "https://commons.wikimedia.org/wiki/File:Fish-anatomy.svg",
        "license": "CC BY 2.5 (selected from multiple available original licences)",
        "license_url": "https://creativecommons.org/licenses/by/2.5/",
        "dimensions": (1038,541),
    },
]
AUTHOR = "Chiswick Chap (vertebrate body plan); Uwe Gille (teleost organs); CHORDATA QA (layout)"
LICENCE = "CC BY-SA 4.0 — composite derivative, both original artists credited"
LICENCE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
KEY = [
    ("1", "Liver"), ("2", "Stomach"), ("3", "Intestine"),
    ("4", "Heart"), ("5", "Swim bladder"), ("6", "Kidney"),
    ("7", "Testis"), ("8", "Ureter"), ("9", "Sperm duct"),
    ("10", "Urinary bladder"), ("11", "Gills"),
]

def font(size, bold=False):
    file = "/usr/share/fonts/truetype/dejavu/" + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(file, size)

def download(source):
    req = Request(source["url"], headers={
        "User-Agent": "ChordataQAAnatomicalPlate/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer": "https://commons.wikimedia.org/",
        "Accept": "image/svg+xml",
    })
    with urlopen(req, timeout=45) as response:
        data = response.read(120_001)
    if not (10_000 < len(data) < 120_000):
        raise ValueError("Unexpected Commons SVG byte length: " + source["name"])
    lowered = data.lower()
    if b"<!doctype" in lowered or b"<!entity" in lowered:
        raise ValueError("SVG DTD or entity declarations are unsupported")
    root = ET.fromstring(data)
    if not root.tag.endswith("}svg"):
        raise ValueError("Source is not namespaced SVG")
    if not root.attrib.get("viewBox") and not root.attrib.get("width"):
        raise ValueError("Source SVG has no geometry")
    for node in root.iter():
        local_name = node.tag.split("}")[-1].lower()
        if local_name in {"script", "foreignobject"}:
            raise ValueError("Active SVG element disallowed: " + local_name)
        if local_name == "image":
            embedded = [value for name, value in node.attrib.items()
                        if name.split("}")[-1].lower() == "href"]
            if len(embedded) != 1 or not embedded[0].startswith(("data:image/png;base64,", "data:image/jpeg;base64,")):
                raise ValueError("Remote or unrecognised image in source SVG")
        for name, value in node.attrib.items():
            if name.split("}")[-1].lower() == "href":
                internal = value.startswith("#")
                embedded_image = (local_name == "image" and
                                  value.startswith(("data:image/png;base64,", "data:image/jpeg;base64,"))
                                  and len(value) < 120_000)
                if not (internal or embedded_image):
                    raise ValueError("External SVG dependency disallowed in " + source["name"])
        if local_name == "style" and node.text:
            css = node.text.lower()
            if "url(" in css or "@import" in css or "expression(" in css:
                raise ValueError("Untrusted SVG stylesheet reference")
    return data, sha256(data).hexdigest()

def svg_to_image(data, width):
    rendered = cairosvg.svg2png(bytestring=data, output_width=width)
    im = Image.open(BytesIO(rendered)).convert("RGBA")
    white = Image.new("RGBA", im.size, "white")
    white.alpha_composite(im)
    return white.convert("RGB")

def main():
    original = [download(item) for item in SOURCES]
    broad = svg_to_image(original[0][0], 2740)
    teleost = svg_to_image(original[1][0], 1370)
    if not (2740 <= broad.width <= 2741 and 630 <= broad.height <= 670):
        raise ValueError("Vertebrate body plan aspect or output width changed")
    if not (1370 <= teleost.width <= 1371 and 690 <= teleost.height <= 740):
        raise ValueError("Teleost rendering dimensions changed")
    plate = Image.new("RGB", (3180, 2260), "#fffefa")
    draw = ImageDraw.Draw(plate)
    ink = "#18313d"
    draw.text((110, 65), "Vertebrate body plan and integrated organ systems",font=font(77,True),fill=ink)
    draw.text((115,170), "Fish-like axial model above; teleost internal anatomy below (taxon-specific)",font=font(40),fill="#49616c")
    draw.rounded_rectangle((86,266,3090,1157),radius=24,outline="#9eabb5",width=4,fill="white")
    draw.text((140,309), "A  Fish-like aquatic vertebrate body-plan model",font=font(49,True),fill=ink)
    plate.paste(broad,(230,435))
    draw.text((160,1071), "Fish-like reference only: gills, fin musculature and tail shape are not universal.",font=font(34),fill="#435a65")
    draw.rounded_rectangle((86,1210,3090,2120),radius=24,outline="#9eabb5",width=4,fill="white")
    draw.text((135,1252), "B  Teleost fish — internal anatomy (example only)",font=font(47,True),fill=ink)
    plate.paste(teleost,(180,1370))
    draw.line((1600,1350,1600,2045),width=3,fill="#cbd5db")
    draw.text((1660,1370), "Original numbered organ key",font=font(48,True),fill=ink)
    for i,(num,label) in enumerate(KEY):
        col = i//6
        row = i%6
        x=1680 + col*665
        y=1490 + row*82
        draw.text((x,y),num,font=font(40,True),fill="#225c7a")
        draw.text((x+86,y),label,font=font(37),fill=ink)
    draw.text((150,2162), "Uwe Gille and Chiswick Chap (credited original illustrations). Compound image: CC BY-SA 4.0.",font=font(31),fill="#4b626c")
    draw.text((150,2210), "A fish is NOT the anatomy of all vertebrates. Image remains provisional.",font=font(30,True),fill="#425a65")
    TARGET.parent.mkdir(parents=True,exist_ok=True)
    plate.save(TARGET,"PNG",optimize=True)
    raw = TARGET.read_bytes()
    if len(raw) < 75_000:
        raise ValueError("Derived plate too small for review")
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    preview = plate.copy()
    preview.thumbnail((1200,850),Image.Resampling.LANCZOS)
    preview.save(PREVIEW,"PNG",optimize=True)
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    matching=[x for x in manifest["figures"] if x["diagramId"]==ID and x["lang"]=="en"]
    if len(matching)!=1 or matching[0]["path"]!="pencil_plates/vertebrate_organs_en.png":
        raise ValueError("Exact intended figure slot not found")
    entry=matching[0]
    if entry.get("author") not in ("CHORDATA QA — original vector anatomical schematic",AUTHOR):
        raise ValueError("Existing asset was independently modified — refuse overwrite")
    entry.pop("svgMaster",None)
    entry.pop("svgSha256",None)
    entry.update(
        size=len(raw),sha256=sha256(raw).hexdigest(),
        author=AUTHOR,license=LICENCE,licenseUrl=LICENCE_URL,
        sourceUrl=SOURCES[0]["page"],sourceUrls=[x["page"] for x in SOURCES],
        sourceSha256=[x[1] for x in original],
        originalLicences=[{"author":x["artist"],"license":x["license"],"url":x["license_url"]} for x in SOURCES],
        modifications=("Rendered two independently attributed source SVGs into one high-resolution "
                       "PNG teaching comparison; original source anatomy unmodified, "
                       "separate English 1–11 teleost organ key added. Source SVGs "
                       "are NOT packaged in the app. Composite offered under CC BY-SA 4.0."),
        keyEn=("A: aquatic fish-like vertebrate model. B: specialised teleost example: "
               "liver, stomach, intestine, heart, swim bladder, kidney, testis, "
               "ureter, sperm duct, urinary bladder and gills. "
               "The teleost arrangement is NOT universal across vertebrates."),
        keyTa=("A: மீனை ஒத்த நீர்வாழ் முதுகெலும்பியின் உடலமைப்பு. B: எலும்பு மீனின் "
               "உடலுறுப்பு அமைப்பு — எடுத்துக்காட்டு மட்டும். "
               "இதன் செவுள்கள், இதயம், சிறுநீரகம், செரிமான உறுப்புகள் ஆகியவை "
               "அனைத்து முதுகெலும்பிகளையும் பிரதிநிதித்துவப்படுத்தாது."),
        visualReview="REPLACED_VISUAL_QA_PENDING",
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
    )
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t");cols=reader.fieldnames;rows=list(reader)
    found=[r for r in rows if r["diagramId"]==ID]
    if len(found)!=1:raise ValueError("Figure ledger mapping not unique")
    found[0]["author"]=AUTHOR
    found[0]["referenceSources"]=" | ".join(x["page"] for x in SOURCES)
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        w.writeheader();w.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    PROVENANCE.write_text(
        "# Vertebrata organ systems — visual replacement Wave 1 (QA)\n\n"
        "Lesson ID: "+ID+"; actual lesson page 2 / organ-systems.\n"
        "The former pale fish silhouette was removed from this English-labelled slot.\n"
        "Two original scientific SVG sources were converted into a single offline PNG:\n\n"
        + "\n".join("- "+v["artist"]+": "+v["page"]+" — "+v["license"]+" "+v["license_url"]+
                    " — raw SHA-256 "+original[i][1]
                    for i,v in enumerate(SOURCES))
        + "\n\n**Derivatives and licence:** both sources were proportionally scaled; "
          "their artwork was not reinterpreted. A separate original numbered key and "
          "two-panel heading were added. Composite derivative licensed CC BY-SA 4.0.\n"
          "PNG SHA-256: "+sha256(raw).hexdigest()+"; dimensions 3180 x 2260.\n\n"
          "**Biological caution:** B is a teleost, not a representative of all "
          "Vertebrata; swim bladders and gills are not universal vertebrate organs. "
          "Panel A also depicts a fish-like body plan; it is not a universal adult vertebrate. \n"
          "**Gates:** independent scientific and Tamil review, image readability "
          "and Android device tests still PENDING.\n",encoding="utf-8")
    print("PASS staged anatomy replacement:",ID,"bytes=",len(raw),"sha256=",sha256(raw).hexdigest())

if __name__=="__main__":
    main()
