#!/usr/bin/env python3
"""Replace the obsolete Calotes engraving with a source-licensed real photograph.

Intentionally narrow: exactly one registered EN figure. Keep the original
historical illustration in a non-APK archive, revoke no human review silently,
and preserve exact creator/licence/source/hash evidence.
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import csv
import hashlib
import io
import json
import subprocess
import sys
import time

import requests
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
ARCHIVE = ROOT / "docs/retired_noninstructional_png/calotes_external_en.png"
PROVENANCE = ROOT / "docs/qa-image-review/CALOTES_PHOTOGRAPHIC_REPLACEMENT_20261112.json"
DIAGRAM = "u4-calotes-external"
ORIGINAL_SHA = "5fcd2cc2ae68d0adda0b406934a9c07aa857bd53dbda19d99abdb5ef0cc14a2f"
COMMONS_FILE = "Oriental Lizard.jpg"
SOURCE_PAGE = "https://commons.wikimedia.org/wiki/File:Oriental_Lizard.jpg"
EXPECTED_LICENCE = "CC BY-SA 4.0"
LICENCE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
AUTHOR = "Azim Khan Ronnie"
UA = "ChordataZoologyQA/1.0 (college education; Commons photograph attribution)"
sha = lambda data: hashlib.sha256(data).hexdigest()

def get_with_retry(session, url, params=None):
    for attempt in range(7):
        response = session.get(url, params=params, timeout=90)
        if response.status_code in (429, 500, 502, 503, 504):
            time.sleep(min(90, 10 * (attempt + 1)))
            continue
        response.raise_for_status()
        return response
    raise RuntimeError("Source retrieval did not succeed after seven attempts: " + url)

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
figures = [f for f in manifest["figures"] if f["diagramId"] == DIAGRAM]
assert len(figures) == 1 and figures[0]["lang"] == "en"
entry = figures[0]
target = ASSETS / entry["path"]
old_bytes = target.read_bytes()
assert old_bytes[:8] == bytes.fromhex("89504e470d0a1a0a")
assert sha(old_bytes) == ORIGINAL_SHA and entry["sha256"] == ORIGINAL_SHA, "Source branch unexpectedly changed"
assert entry["size"] == len(old_bytes)
assert "Amsterdam" in entry["author"]
assert entry["reviewStatus"].startswith("PROVISIONAL_")
prior = {key: entry.get(key) for key in
         ("author", "license", "licenseUrl", "sourceUrl", "sourceImageUrl", "sha256", "size", "sourceSha1",
          "sourceSha256", "sourceKind", "modifications")}

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept": "application/json,image/*;q=0.9,*/*;q=0.5"})
params = {"action": "query", "format": "json", "prop": "imageinfo",
          "iiprop": "url|extmetadata|size", "titles": "File:" + COMMONS_FILE}
pages = get_with_retry(session, "https://commons.wikimedia.org/w/api.php", params).json()["query"]["pages"]
info = next(iter(pages.values())).get("imageinfo")
assert info, "No Commons imageinfo for licensed source"
info = info[0]
licence = info["extmetadata"].get("LicenseShortName", {}).get("value", "")
assert licence.casefold() == EXPECTED_LICENCE.casefold(), ("Licence differs", licence)
urlparts = urlsplit(info["url"])
remote_url = urlunsplit((urlparts.scheme, urlparts.netloc, urlparts.path, "", ""))
assert remote_url.startswith("https://upload.wikimedia.org/")
original = get_with_retry(session, remote_url).content
assert original.startswith(bytes.fromhex("ffd8ff")) and len(original) > 250000
with Image.open(io.BytesIO(original)) as im:
    im.verify()
with Image.open(io.BytesIO(original)) as im:
    assert im.width >= 3500 and im.height >= 1800
    photograph = ImageOps.exif_transpose(im).convert("RGB")
    # Keep the entire organism: no invented anatomical annotations, stretching,
    # background removal or crops. English figure key remains in the reader.
    photograph = ImageOps.contain(photograph, (2500, 1600), Image.Resampling.LANCZOS)
    assert photograph.width >= 2200 and photograph.height >= 1200
    buffer = io.BytesIO()
    photograph.save(buffer, format="PNG", optimize=True)
    png = buffer.getvalue()
assert png[:8] == bytes.fromhex("89504e470d0a1a0a") and len(png) > 80000
assert sha(png) != ORIGINAL_SHA

ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
if ARCHIVE.exists():
    assert sha(ARCHIVE.read_bytes()) == ORIGINAL_SHA, "Archive collision"
else:
    ARCHIVE.write_bytes(old_bytes)
target.write_bytes(png)

entry["retiredHistoricalPlate"] = {
    "path": str(ARCHIVE.relative_to(ROOT)),
    "sha256": ORIGINAL_SHA,
    "metadata": prior,
}
for key in ("sourceSha1",):
    entry.pop(key, None)
entry.update({
    "sha256": sha(png),
    "size": len(png),
    "author": AUTHOR + " (original photograph); CHORDATA QA (lossless PNG adaptation)",
    "sourceUrl": SOURCE_PAGE,
    "sourceImageUrl": remote_url,
    "sourceSha256": [sha(original)],
    "sourceFormat": "JPEG",
    "installedFormat": "PNG",
    "sourceKind": "AUTHENTIC_COMMONS_CALOTES_SPECIMEN_PHOTO_ADAPTED",
    "license": EXPECTED_LICENCE + " — adapted photographic PNG; attribution and share-alike apply",
    "licenseUrl": LICENCE_URL,
    "referenceUrls": [SOURCE_PAGE, "https://reptile-database.reptarium.cz/species?genus=Calotes&species=versicolor"],
    "modifications": "EXIF orientation corrected; entire photograph proportionally resized and losslessly encoded as PNG. No biological features invented or digitally redrawn.",
    "keyEn": "Photographed oriental garden lizard, identified by its source as Calotes versicolor. Observe the spiny nuchal crest, tympanum, scales, eye, four limbs and long tail where visible. This is an external specimen photograph, NOT an internal-anatomy diagram. Species-complex identification and variable coloration require caution; no scale is implied.",
    "keyTa": "வெளிப்புறத் தோற்றப் புகைப்படம்: மூலத்தில் Calotes versicolor என அடையாளமிடப்பட்ட ஓணான். கழுத்து மற்றும் முதுகு முள் வரிசை, செவிப்பறை, செதில்கள், கண், நான்கு கால்கள், நீண்ட வால் ஆகியவற்றைக் கவனிக்கவும். இது உள்ளுறுப்பியல் படம் அன்று. நிறம் மாறுபடலாம்; அளவுகோல் இல்லை.",
    "scope": "Original documentary photograph of a live garden lizard; visible external morphology only. No claim to illustrate circulatory or digestive organs.",
    "visualReview": "SOURCED_REAL_SPECIMEN_PHOTO_QA_PROVISIONAL",
    "pedagogicStatus": "REPLACED_WITH_CC_LICENSED_CALOTES_SPECIMEN_PHOTO_QA_PENDING_2026-11-12",
    "reviewStatus": "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
})
MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

with LEDGER.open(newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter="\t")
    columns = reader.fieldnames
    rows = list(reader)
assert columns and len(rows) == 64
for row in rows:
    if row["diagramId"] == DIAGRAM:
        row["author"] = entry["author"]
        row["referenceSources"] = SOURCE_PAGE
with LEDGER.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=columns, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
PROVENANCE.write_text(json.dumps({
    "diagramId": DIAGRAM, "sourcePage": SOURCE_PAGE, "originalDownloadUrl": remote_url,
    "author": AUTHOR, "verifiedLicence": licence, "licenceUrl": LICENCE_URL,
    "originalJpegSha256": sha(original), "originalJpegBytes": len(original),
    "installedPngPath": entry["path"], "installedPngSha256": sha(png),
    "installedPngBytes": len(png), "dimensions": list(photograph.size),
    "previousHistoricalPlateSha256": ORIGINAL_SHA,
    "previousHistoricalPlateArchive": str(ARCHIVE.relative_to(ROOT)),
    "edits": entry["modifications"],
    "scienceStatus": "PROVISIONAL_QA_NOT_INDEPENDENTLY_APPROVED",
}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

commands = (
    ["python3", "scripts/write_figure_review_register.py"],
    ["python3", "scripts/audit_pencil_coverage.py"],
    ["python3", "scripts/audit_figure_placement.py"],
    ["python3", "scripts/audit_coverage_report.py"],
    ["python3", "scripts/write_figure_review_register.py", "--check"],
    ["python3", "scripts/audit_android_qa_contract.py"],
)
for command in commands:
    subprocess.run(command, cwd=ROOT, check=True)
print("REPLACED Calotes external photograph", sha(png), len(png), photograph.size)
print("PROVISIONAL ONLY: anatomy/editorial sign-off and device screenshot still required")
