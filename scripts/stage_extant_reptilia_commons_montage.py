#!/usr/bin/env python3
"""Stage a real, licensed four-order reptile photo montage on an isolated QA branch.

No AI anatomy or generic SVG silhouettes. All original bytes are verified before
downscaling the four-photograph composite for offline Android PNG delivery.
"""
from __future__ import annotations
import csv
import hashlib
import json
import subprocess
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
DEST = ASSETS / "pencil_plates/living_reptile_groups_en.png"
LEDGER = ROOT / "docs/figure-coverage.tsv"
NOTE = ROOT / "docs/CHORDATA_EXTANT_REPTILIA_COMMONS_QA_20261111.md"
DIAGRAM_ID = "u4-reptilia-classification-living-reptile-orders"
PAGE = "https://commons.wikimedia.org/wiki/File:Extant_reptilia.jpg"
URL = "https://upload.wikimedia.org/wikipedia/commons/2/2c/Extant_reptilia.jpg"
SOURCE_SHA1 = "bb98028bb492b30e0d2df2a50cb975d7df455377"
OLD_SHA256 = "04a4ac59719db220585ecb123da5c89ffecb4f46279fc2e2aefcd7ce7288243a"
AUTHOR = ("Petter Bøckman (2012) four-reptile montage; component photos by "
          "Mila Zinkova, TimVickers, Ester Inbar and Donald Macauley")
COMPONENTS = [
    "https://commons.wikimedia.org/wiki/File:Total_internal_reflection_of_Chelonia_mydas_.jpg",
    "https://commons.wikimedia.org/wiki/File:Sphenodon_punctatus_(2).jpg",
    "https://commons.wikimedia.org/wiki/File:AgamaSinaita01_ST_10.jpg",
    "https://commons.wikimedia.org/wiki/File:Flickr_-_don_macauley_-_Crocodile.jpg"
]
def main():
    request = Request(URL, headers={
        "User-Agent": "CHORDATA-Zoology-Figure-QA/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer": "https://commons.wikimedia.org/",
        "Accept": "image/jpeg"
    })
    with urlopen(request, timeout=90) as response:
        raw = response.read(8_000_000)
    if len(raw) != 5_902_997:
        raise RuntimeError(f"Source size changed: {len(raw)}")
    if hashlib.sha1(raw).hexdigest() != SOURCE_SHA1:
        raise RuntimeError("Wikimedia source SHA-1 changed: refuse unreviewed file")
    original = Image.open(BytesIO(raw))
    original.load()
    if original.format != "JPEG" or original.size != (3000, 2355):
        raise RuntimeError("Wikimedia montage dimensions or format changed")
    # Resample the complete genuine 4-photo montage to a phone/zoom-friendly
    # 1800px PNG; no cropping, added organ labels or synthetic structures.
    pic = original.convert("RGB").resize((1800, 1413), Image.Resampling.LANCZOS)
    pic.save(DEST, format="PNG", optimize=True)
    png = DEST.read_bytes()
    digest = hashlib.sha256(png).hexdigest()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = [x for x in manifest["figures"] if x["diagramId"] == DIAGRAM_ID and x["lang"] == "en"]
    if len(entries) != 1 or entries[0]["path"] != "pencil_plates/living_reptile_groups_en.png":
        raise RuntimeError("Wrong lesson figure placement")
    entry = entries[0]
    if entry["sha256"] not in (OLD_SHA256, digest):
        raise RuntimeError("Figure was independently changed; refusing overwrite")
    for k in ("svgMaster", "svgSha256", "artworkDisposition"):
        entry.pop(k, None)
    entry.update(
        sha256=digest, size=len(png), author=AUTHOR,
        license="CC BY-SA 3.0 Unported — original photo montage by Petter Bøckman; component rights/credits retained",
        licenseUrl="https://creativecommons.org/licenses/by-sa/3.0/",
        sourceUrl=PAGE, sourceImageUrl=URL, sourceSha1=SOURCE_SHA1,
        sourceSha256=[hashlib.sha256(raw).hexdigest()],
        sourceFormat="JPEG", installedFormat="PNG",
        referenceUrls=[PAGE] + COMPONENTS,
        modifications=("Original four-photo montage scaled proportionally from 3000x2355 to 1800x1413 "
                       "using Lanczos interpolation, encoded as offline RGB PNG; no new anatomical "
                       "content, overlays, cropping or AI-generative alterations."),
        sourceKind="PETTER_BOECKMAN_2012_REAL_FOUR_ORDER_REPTILE_MONTAGE_CC_BY_SA_3",
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        visualReview="REAL_SOURCE_PHOTOMONTAGE_PENDING_EXPERT_AND_DEVICE_REVIEW",
        scope=("Four representative living non-avian reptile orders as photographs, "
               "not a phylogenetic tree, an internal anatomy plate or a complete Squamata sampling."),
        keyEn=("Four living NON-AVIAN reptile orders, clockwise from top left: Testudines "
               "(green sea turtle), Rhynchocephalia (tuatara), Crocodylia (crocodilian), "
               "and Squamata (Sinai agama, lower left). Individual photos are examples "
               "only. A clade-based phylogeny also includes birds within Reptilia/Sauropsida."),
        keyTa=("தற்போது வாழும் பறவைகள் நீங்கலான நான்கு ஊர்வன வரிசைகளுக்கான புகைப்பட எடுத்துக்காட்டுகள்: "
               "மேல் இடது — டெஸ்டுடினிஸ் (கடலாமை); மேல் வலது — ரின்கோசெபாலியா (டுவாட்டாரா); "
               "கீழ் இடது — ஸ்குவாமேட்டா (சினாய் அகமா பல்லி); கீழ் வலது — க்ரோகோடீலியா (முதலை). "
               "இவை பரிணாம மரம் அல்ல; இனத் தொகுப்பின் எடுத்துக்காட்டுப் படங்கள் மட்டுமே. "
               "மரபுவழி சார்ந்த வகைப்பாட்டில் பறவைகளும் சௌரோப்சிடா குழுவில் அடங்குகின்றன."),
        topicId="u4-reptilia-classification", page=2, sectionKey="living-orders",
        learningObjective=("Recognise living non-avian Testudines, Rhynchocephalia, Squamata, "
                           "Crocodylia and understand the limits of the traditional scheme.")
    )
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with LEDGER.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        fields, rows = reader.fieldnames, list(reader)
    matches = [r for r in rows if r["diagramId"] == DIAGRAM_ID]
    if len(matches) != 1:
        raise RuntimeError("Missing coverage ledger row")
    matches[0]["author"] = AUTHOR
    matches[0]["referenceSources"] = " | ".join([PAGE] + COMPONENTS)
    with LEDGER.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(["python3", "scripts/write_figure_review_register.py"], cwd=ROOT, check=True)
    NOTE.write_text(
        "# CHORDATA real reptile-orders montage — provisional QA, 11 November 2026\n\n"
        f"Diagram: {DIAGRAM_ID} / Unit IV / page 2 / living-orders.\n\n"
        f"Composite creator: {AUTHOR}.\nSource page: {PAGE}\nSource binary: {URL}\n"
        f"Original JPEG SHA-1: {SOURCE_SHA1}; SHA-256: {hashlib.sha256(raw).hexdigest()}.\n"
        f"Original size: {len(raw)} bytes; 3000 x 2355 pixels.\n"
        f"Installed PNG SHA-256: {digest}, size {len(png)} bytes; 1800 x 1413 pixels.\n\n"
        "Licence: Creative Commons Attribution-ShareAlike 3.0 Unported; this proportional "
        "downscaled composite remains distributed under CC BY-SA 3.0. No endorsement implied.\n"
        "Component images and credits (top left, top right, lower left, lower right):\n"
        f"1. Mila Zinkova (Brocken Inaglory), turtle: {COMPONENTS[0]} (CC BY-SA 4.0 available).\n"
        f"2. TimVickers, tuatara: {COMPONENTS[1]} (public domain by photographer).\n"
        f"3. Ester Inbar (ST), Sinai agama: {COMPONENTS[2]} (attribution licence).\n"
        f"4. Donald Macauley, crocodile: {COMPONENTS[3]} (CC BY-SA 2.0).\n\n"
        "Scientific scope: examples of four traditional living non-avian orders; no phylogeny "
        "or claim that Squamata consists only of lizards. Phylogenetic reptiles include birds.\n"
        "Review status: independent Zoology/Tamil sign-off, phone-scale legibility and "
        "physical-device acceptance PENDING. Production release HOLD.\n",
        encoding="utf-8"
    )
    print("PASS: authentic Wikimedia reptile-orders montage PNG", len(png), digest)

if __name__ == "__main__":
    main()
