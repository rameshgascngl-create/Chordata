#!/usr/bin/env python3
"""Intake a precisely attributed Branchiostoma internal-anatomy drawing.

The English-labelled figure is replaced; the legacy Tamil variant remains
unaltered for source-history integrity. The Android gallery deliberately uses
the English diagram in both separate lesson-language modes.
"""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
import csv
import json
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
TARGET = ASSETS / "pencil_plates/branchiostoma_en.png"
LEDGER = ROOT / "docs/figure-coverage.tsv"
PROVENANCE = ROOT / "docs/CHORDATA_SOURCED_BRANCHIOSTOMA_QA.md"
PREVIEW = ROOT / "build/sourced_morphology_qa/branchiostoma_candidate.png"
DIAGRAM = "u1-cephalochordata-branchiostoma-labelled"
SOURCE_PAGE = "https://commons.wikimedia.org/wiki/File:Branchiostoma_anatomy.jpg"
SOURCE_URL = "https://upload.wikimedia.org/wikipedia/commons/3/31/Branchiostoma_anatomy.jpg"
CREATOR = "Hans Hillewaert — original 32-label Branchiostoma lanceolatum drawing"
LICENCE = "CC BY-SA 4.0 (drawing and PNG adaptation)"
LICENCE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"

NUMERIC_KEY = (
    "1 Buccal cirrus; 2 Buccal cavity; 3 Wheel organ; 4 Velum; "
    "5 Velar tentacle; 6 Pharynx; 7 Atrium; 8 Gill slit; "
    "9 Endostyle; 10 Gill bar; 11 Ventral aorta; 12 Dorsal aorta; "
    "13 Branchial skeleton; 14 Oesophagus; 15 Stomach; 16 Atriopore; "
    "17 Hepatic caecum; 18 Iliocolon; 19 Intestine; 20 Anus; "
    "21 Hatschek's pit; 22 Ocellus; 23 Rostrum; 24 Cerebral vesicle; "
    "25 Nerve cord; 26 Notochord; 27 Myoseptum; 28 Myomere; "
    "29 Caudal fin; 30 Ventral fin; 31 Metapleural fold; 32 Dorsal fin."
)


def fetch_source():
    request = Request(SOURCE_URL, headers={
        "User-Agent": "ChordataQAArtImport/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer": "https://commons.wikimedia.org/",
        "Accept": "image/jpeg",
    })
    with urlopen(request, timeout=45) as result:
        data = result.read(5_000_001)
    if len(data) < 300_000 or len(data) > 5_000_000:
        raise ValueError("Unexpected Wikimedia Branchiostoma original byte length")
    im = Image.open(BytesIO(data))
    im.load()
    if im.format != "JPEG" or im.size != (4952, 2512):
        raise ValueError(f"Unexpected original image: {im.format}, {im.size}")
    return im.convert("RGB"), sha256(data).hexdigest()


def stage():
    image, original_sha = fetch_source()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    # Retain the exact original raster dimensions; no extra re-labelling on
    # the image itself. The 32-number key is stored in the manifest and shown
    # alongside the bilingual caption. No false scientific sign-off is made.
    image.save(TARGET, format="PNG", optimize=True)
    data = TARGET.read_bytes()
    digest = sha256(data).hexdigest()
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    # A smaller review preview is not used as the in-app image.
    image.thumbnail((1800, 950), Image.Resampling.LANCZOS)
    image.save(PREVIEW, format="PNG", optimize=True)
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    en = [f for f in m["figures"] if f["diagramId"] == DIAGRAM and f["lang"] == "en"]
    ta = [f for f in m["figures"] if f["diagramId"] == DIAGRAM and f["lang"] == "ta"]
    if len(en) != 1 or len(ta) != 1 or en[0]["path"] != "pencil_plates/branchiostoma_en.png":
        raise ValueError("Source manifest lacks the exact English / retained Tamil variants")
    entry = en[0]
    entry.update(
        sha256=digest, size=len(data), author=CREATOR,
        license=LICENCE, sourceUrl=SOURCE_PAGE, licenseUrl=LICENCE_URL,
        sourceSha256=[original_sha],
        modifications=("Full original annotated drawing converted from JPEG to lossless "
                       "PNG with geometry and numerical labels unchanged; original "
                       "is distributed under the same CC BY-SA 4.0 licence."),
        keyEn="Numbers from the original (English): " + NUMERIC_KEY,
        keyTa="படத்திலுள்ள எண்களுக்கான விளக்கம் (ஆங்கிலத்தில்): " + NUMERIC_KEY,
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
    )
    MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with LEDGER.open(newline="", encoding="utf-8") as stream:
        rd = csv.DictReader(stream, delimiter="\t")
        fields = rd.fieldnames
        rows = list(rd)
    matched = [x for x in rows if x["diagramId"] == DIAGRAM]
    if len(matched) != 1:
        raise ValueError("Expected one Branchiostoma lesson mapping")
    matched[0]["author"] = CREATOR
    matched[0]["referenceSources"] = SOURCE_PAGE
    with LEDGER.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(["python3", "scripts/write_figure_review_register.py"], check=True, cwd=ROOT)
    PROVENANCE.write_text(
        "# Branchiostoma labelled internal anatomy — source-credited QA\n\n"
        f"Diagram ID: \`{DIAGRAM}\`.\n\n"
        f"Image: [Hans Hillewaert's anatomical plate]({SOURCE_PAGE}); "
        f"source JPEG SHA-256: \`{original_sha}\`.\n"
        f"Derivative lossless PNG SHA-256: \`{digest}\`.\n\n"
        f"Author attribution: {CREATOR}.\n\n"
        f"Licence: [{LICENCE}]({LICENCE_URL}). The converted PNG derivative "
        "remains under CC BY-SA 4.0.\n\n"
        "Modifications: JPEG decoded and losslessly encoded as PNG; original "
        "dimensions, anatomy and label locations retained. Added English key "
        "to the lesson metadata (not stamped over source illustration). "
        "Existing Tamil-language image variant is retained unchanged but "
        "not chosen by the app, which uses English diagrams in both modes.\n\n"
        "**Pending:** anatomy/proportion review, Tamil narrative and caption "
        "review, mobile legibility at 100% and 200%, pinch zoom and Android "
        "physical-device acceptance. No medical or academic approval inferred.\n",
        encoding="utf-8")
    print(f"PASS: staged attributed full-res Branchiostoma plate {len(data)} bytes / {digest}")
    print("No academic approval granted.")


if __name__ == "__main__":
    stage()
