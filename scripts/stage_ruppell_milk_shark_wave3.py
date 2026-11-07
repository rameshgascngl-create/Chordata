#!/usr/bin/env python3
"""Stage Rüppell's actual Carcharias acutus (milk shark) plate XVIII, fig. 4.

Release remains blocked. This crops a public-domain historical print, not
a specimen photograph or a substitute spadenose shark illustration.
"""
import csv
import hashlib
import json
import subprocess
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
DEST = ASSETS / "pencil_plates/scoliodon_external_anatomy_en.png"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
REVIEW = ROOT / "docs/qa-image-review/ruppell_milk_shark_fig4_review.png"
REPORT = ROOT / "docs/CHORDATA_RUPPELL_MILK_SHARK_QA.md"
DIAGRAM_ID = "u2-scoliodon-external-labelled"
SOURCE_PAGE = ("https://commons.wikimedia.org/wiki/File:"
    "Neue_Wirbelthiere_zu_der_Fauna_von_Abyssinien_geh%C3%B6rig_"
    "(Taf._18_Fig.1-4)_BHL37140507.jpg")
SOURCE_IMAGE = ("https://upload.wikimedia.org/wikipedia/commons/a/a7/"
    "Neue_Wirbelthiere_zu_der_Fauna_von_Abyssinien_geh%C3%B6rig_"
    "%28Taf._18_Fig.1-4%29_BHL37140507.jpg")
SOURCE_SHA1 = "884bc3fdcd1dcfe357c51e33f86ecd2a226a78d0"
SOURCE_DIMS = (2117, 3106)
AUTHOR = ("Eduard Rüppell (1837) — historical plate; "
          "Field Museum Library/BHL scan; CHORDATA QA crop/layout")
RIGHTS = "Public domain — Rüppell 1837; faithful historical scan"
LICENSE_URL = "https://creativecommons.org/publicdomain/mark/1.0/"
ITIS = "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=160219"
CAS = "https://researcharchive.calacademy.org/research/ichthyology/catalog/fishcatget.asp?spid=26421"

def font(size, bold=False):
    path = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(path, size)

def get_original():
    request = Request(SOURCE_IMAGE, headers={
        "User-Agent": "ChordataAcademicQA/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer": "https://commons.wikimedia.org/",
        "Accept": "image/jpeg"})
    with urlopen(request, timeout=80) as response:
        raw = response.read(2_000_001)
    if len(raw) != 367199:
        raise ValueError(f"Unexpected source size: {len(raw)}")
    if hashlib.sha1(raw).hexdigest() != SOURCE_SHA1:
        raise ValueError("Public-domain original changed (SHA-1 mismatch)")
    source = Image.open(BytesIO(raw))
    source.load()
    if source.format != "JPEG" or source.size != SOURCE_DIMS:
        raise ValueError(f"Unexpected original plate: {source.format} / {source.size}")
    return source.convert("RGB"), hashlib.sha256(raw).hexdigest()

def render(source):
    # Original plate contains four DIFFERENT shark species. Only FIGURE 4
    # in the bottom register is Carcharias acutus, now Rhizoprionodon acutus.
    # Keep the whole fish and its geometry; crop away figs 1-3.
    crop = source.crop((20, 1950, 2080, 2502))
    page = Image.new("RGB", (3200, 2070), "#fffdf9")
    draw = ImageDraw.Draw(page)
    navy, muted = "#203744", "#4e6978"
    draw.text((92, 67), "Rhizoprionodon acutus — milk shark", font=font(73, True), fill=navy)
    draw.text((99, 170), "Syllabus: Scoliodon sorrakowah  |  Original: Carcharias acutus (Rüppell, 1837)",
              font=font(36), fill=muted)
    draw.rounded_rectangle((65, 260, 3138, 1275), radius=18, fill="#ffffff",
                           outline="#a7b3b9", width=4)
    art = ImageOps.contain(crop, (3000, 940), Image.Resampling.LANCZOS)
    page.paste(art, (100 + (3000 - art.width)//2, 295 + (945 - art.height)//2))
    draw.text((102, 1318), "External identification — teaching key", font=font(46, True), fill=navy)
    features = [
        "Long, pointed snout and elongated labial furrows",
        "Five external gill slits behind each side of head",
        "First dorsal origin near the pectoral rear tips",
        "Small second dorsal and well-developed anal fin",
        "Paired pectoral and pelvic fins",
        "Asymmetrical (heterocercal) caudal fin",
    ]
    for i, value in enumerate(features):
        col = i // 3
        row = i % 3
        x = 103 + col * 1525
        y = 1410 + row * 105
        draw.ellipse((x, y + 16, x + 22, y + 38), fill="#3f7c93")
        draw.text((x + 37, y), value, font=font(30), fill=navy)
    draw.line((98, 1785, 3080, 1785), fill="#aebdc5", width=3)
    draw.text((101, 1814), "Source: Rüppell, Plate XVIII, Fig. 4 (1837) | Field Museum Library / BHL via Wikimedia Commons",
              font=font(27), fill=muted)
    draw.text((101, 1870), "Only the fourth species was used; other sharks on the historic plate were excluded.",
              font=font(27), fill=muted)
    draw.text((101, 1926), "Historical illustration; diagnostic characters and phone-scale legibility await independent review.",
              font=font(27), fill=muted)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    page.save(DEST, "PNG", optimize=True)
    raw = DEST.read_bytes()
    if len(raw) < 150_000:
        raise ValueError("Figure too small for an authentic historical anatomical drawing")
    REVIEW.parent.mkdir(parents=True, exist_ok=True)
    preview = page.copy()
    preview.thumbnail((1200, 1000), Image.Resampling.LANCZOS)
    preview.save(REVIEW, "PNG", optimize=True)
    return raw

def update_metadata(raw, source_hash):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    matches = [x for x in manifest["figures"]
               if x["diagramId"] == DIAGRAM_ID and x["lang"] == "en"]
    if len(matches) != 1:
        raise ValueError("Figure not uniquely registered")
    entry = matches[0]
    if entry["path"] != "pencil_plates/scoliodon_external_anatomy_en.png":
        raise ValueError("Wrong manifest asset path")
    expected_previous = "b59c7c95fa45ff49363333414c875e82934303873d19227d581d6b4069892af5"
    if entry["sha256"] != expected_previous:
        raise ValueError("Refusing to overwrite different/independently modified figure")
    entry.pop("svgMaster", None)
    entry.pop("svgSha256", None)
    entry.update({
        "author": AUTHOR,
        "license": RIGHTS,
        "licenseUrl": LICENSE_URL,
        "sourceUrl": SOURCE_PAGE,
        "sourceSha1": SOURCE_SHA1,
        "sourceSha256": [source_hash],
        "referenceUrls": [SOURCE_PAGE, ITIS, CAS],
        "modifications": ("Original full-page historic colour scan cropped to Plate XVIII "
                          "Figure 4 (milk shark) only; proportional resizing, separate "
                          "external English identification key; no organ anatomy invented."),
        "keyEn": ("Milk shark (Rhizoprionodon acutus): pointed snout, developed labial "
                  "furrows, five pairs of gill slits, first dorsal near pectoral rear "
                  "tips, smaller second dorsal, anal fin and heterocercal caudal fin. "
                  "Historic Scoliodon sorrakowah is a synonym in this syllabus, "
                  "NOT Scoliodon laticaudus."),
        "keyTa": ("பால் சுறா — Rhizoprionodon acutus. நீண்ட கூரிய முகப்பு, "
                  "வாய்மூலை மடிப்புப் பள்ளங்கள், ஐந்து இணைச் செவுள் பிளவுகள், "
                  "முதல் முதுகுத் துடுப்பு, சிறிய இரண்டாம் முதுகுத் துடுப்பு, "
                  "குதத் துடுப்பு, சமச்சீரற்ற வால் துடுப்பு காணப்படும். "
                  "பாடத்திட்டத்தின் Scoliodon sorrakowah என்னும் பழைய பெயர் "
                  "இவ்வினத்தைக் குறிக்கிறது; Scoliodon laticaudus அல்ல."),
        "size": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "reviewStatus": "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        "visualReview": "REPLACED_VISUAL_QA_PENDING",
        "taxon": "Rhizoprionodon acutus (Rüppell, 1837)",
        "historicLessonName": "Scoliodon sorrakowah",
        "historicalPlateFigure": "Plate XVIII, Figure 4 only",
    })
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with LEDGER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        cols, rows = reader.fieldnames, list(reader)
    matching = [x for x in rows if x["diagramId"] == DIAGRAM_ID]
    if len(matching) != 1:
        raise ValueError("Coverage ledger figure must be unique")
    matching[0]["author"] = AUTHOR
    matching[0]["referenceSources"] = SOURCE_PAGE + " | " + ITIS + " | " + CAS
    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(["python3", "scripts/write_figure_review_register.py"],
                   check=True, cwd=ROOT)
    REPORT.write_text(
        "# Milk shark: corrected Rüppell figure (isolated QA)\n\n"
        "Lesson figure: " + DIAGRAM_ID + "\n\n"
        "Current taxon: Rhizoprionodon acutus (Rüppell, 1837), milk shark.\n\n"
        "Historic syllabus name: Scoliodon sorrakowah (see ITIS/Catalog of Fishes).\n\n"
        "Prior image was Scoliodon laticaudus (spadenose shark), a DIFFERENT species. "
        "That image is not scientifically applicable as the milk-shark type study.\n\n"
        "Original: Eduard Rüppell, Neue Wirbelthiere, Fische des Rothen Meeres (1837), "
        "Plate XVIII, Fig. 4 only. Source: " + SOURCE_PAGE + "\n\n"
        "Rights: public domain (Rüppell died 1884; faithful PD-scan) — " + LICENSE_URL + "\n\n"
        "Original JPEG SHA-1: " + SOURCE_SHA1 + "\n\n"
        "Original JPEG SHA-256: " + source_hash + "\n\n"
        "Final cropped teaching PNG SHA-256: " + hashlib.sha256(raw).hexdigest() + "\n\n"
        "Changes: accurately cropped figure 4 only, preserved shape/proportions, "
        "resized and put a modern English key outside the historic illustration. "
        "No anatomical leader lines drawn over the source.\n\n"
        "Research: " + ITIS + " | " + CAS + "\n\n"
        "Visual approval, independent Zoology reviewer, Tamil editorial reviewer and "
        "physical-device acceptance: ALL PENDING. QA only; production on HOLD.\n",
        encoding="utf-8")
    print("PASS: correct Rhizoprionodon acutus plate XVIII fig. 4 staged; "
          "PNG bytes:", len(raw), "SHA-256:", hashlib.sha256(raw).hexdigest())

if __name__ == "__main__":
    source, original_sha = get_original()
    png = render(source)
    update_metadata(png, original_sha)
