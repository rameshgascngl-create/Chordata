#!/usr/bin/env python3
"""Replace provisional Balanoglossus outline with a credited 1905 external drawing.

Only figure 9 (external morphology) is taken. Figure 10 has outdated
"proto-notochord" interpretations and MUST NOT appear in this lesson.
Academic approval remains pending regardless of successful static audits.
"""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
import csv
import json
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
PNG = ASSETS / "pencil_plates/balanoglossus_external.png"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
PROVENANCE = ROOT / "docs/CHORDATA_SOURCED_BALANOGLOSSUS_QA.md"
EVIDENCE = ROOT / "build/sourced_morphology_qa"
DIAGRAM = "u1-hemichordata-balanoglossus-external"
SOURCE_URL = "https://upload.wikimedia.org/wikipedia/commons/3/39/NIE_1905_Ascidians_and_balanoglossus.png"
SOURCE_PAGE = "https://commons.wikimedia.org/wiki/File:NIE_1905_Ascidians_and_balanoglossus.png"
CREATOR = "Unknown illustrator, New International Encyclopaedia (1905); CHORDATA QA (layout)"
RIGHTS = "Public domain — New International Encyclopaedia, 1905"


def ttf(size, bold=False):
    path = "/usr/share/fonts/truetype/dejavu/" + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    if not Path(path).exists():
        raise RuntimeError("DejaVu Sans font is required for reproducible QA PNG")
    return ImageFont.truetype(path, size)


def retrieve():
    req = Request(SOURCE_URL, headers={
        "User-Agent": "ChordataQAArtImport/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer": "https://commons.wikimedia.org/",
        "Accept": "image/png",
    })
    with urlopen(req, timeout=45) as response:
        raw = response.read(4_000_001)
    if not (100_000 < len(raw) < 4_000_000):
        raise ValueError("Unexpected historical plate byte length")
    im = Image.open(BytesIO(raw))
    im.load()
    if im.format != "PNG" or im.size != (1488, 2387):
        raise ValueError("Historical illustration dimensions or media changed")
    return im.convert("RGB"), sha256(raw).hexdigest()


def stage():
    plate, original_sha = retrieve()
    # Figure 9 is at the lower right of the 1905 encyclopaedia plate.
    # Keep the entire proboscis/collar/trunk silhouette and its historical
    # abbreviations. Figure 10 (on the left) is excluded for science accuracy.
    # The published engraving is a vertical figure near the page's right edge.
    # Isolate the entire proboscis and posterior trunk, excluding annotation
    # fragments and the adjacent (scientifically outdated) figure 10.
    external = plate.crop((1320, 1220, 1488, 2387))
    external = external.rotate(90, expand=True)
    external = ImageOps.expand(external, border=(75, 30, 75, 30), fill="white")
    output = Image.new("RGB", (2200, 1300), "#fffefa")
    draw = ImageDraw.Draw(output)
    draw.text((100, 65), "Balanoglossus — external morphology", font=ttf(66, True), fill="#162a35")
    draw.text((108, 165), "Historic anatomical illustration (1905); anterior at left",
              font=ttf(39), fill="#344857")
    draw.rounded_rectangle((90, 242, 2110, 785), radius=23, outline="#8999a4", width=3, fill="white")
    display = ImageOps.contain(external, (1900, 480), Image.Resampling.LANCZOS)
    output.paste(display, (110 + (1980-display.width)//2, 268 + (490-display.height)//2))
    draw.text((103, 830), "External regions and structures", font=ttf(48, True), fill="#162a35")
    draw.text((103, 905), "pr  Proboscis       co  Collar       br  Branchial region",
              font=ttf(39), fill="#263b46")
    draw.text((103, 972), "gen  Genital ridges       hep  Hepatic caeca region",
              font=ttf(39), fill="#263b46")
    draw.line((105, 1061, 2080, 1061), fill="#bdc8cf", width=3)
    draw.text((103, 1100), "Hemichordates are NOT true chordates.", font=ttf(36, True), fill="#384e5a")
    draw.text((103, 1160), "The stomochord is not homologous to the chordate notochord.",
              font=ttf(33), fill="#384e5a")
    PNG.parent.mkdir(parents=True, exist_ok=True)
    output.save(PNG, "PNG", optimize=True)
    data = PNG.read_bytes()
    if len(data) < 9_000:
        raise ValueError("Unexpected empty derived illustration")
    digest = sha256(data).hexdigest()
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "balanoglossus_candidate.png").write_bytes(data)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    matches = [f for f in manifest["figures"] if f["diagramId"] == DIAGRAM]
    if len(matches) != 1 or matches[0]["lang"] != "shared":
        raise ValueError("Balanoglossus must map to exactly one shared lesson")
    matches[0].update(
        size=len(data), sha256=digest, author=CREATOR, license=RIGHTS,
        sourceUrl=SOURCE_PAGE,
        sourceSha256=[original_sha],
        licenseUrl="https://creativecommons.org/publicdomain/mark/1.0/",
        modifications="Isolated original figure 9, rotated without changing proportions, enlarged and separately keyed in English.",
        keyEn="pr: proboscis; co: collar; br: branchial region; gen: genital ridges; hep: hepatic caeca region.",
        keyTa="pr: துதிக்கை; co: கழுத்துப்பட்டை; br: செவுள் பகுதி; gen: இனப்பெருக்க மேடுகள்; hep: கல்லீரல் நீட்சிகள் உள்ள பகுதி.",
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
    )
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with LEDGER.open(newline="", encoding="utf-8") as inp:
        reader = csv.DictReader(inp, delimiter="\t")
        fields = reader.fieldnames
        records = list(reader)
    rows = [row for row in records if row["diagramId"] == DIAGRAM]
    if len(rows) != 1:
        raise ValueError("Expected exactly one figure-coverage row")
    rows[0]["author"] = CREATOR
    rows[0]["referenceSources"] = SOURCE_PAGE
    with LEDGER.open("w", newline="", encoding="utf-8") as out:
        w = csv.DictWriter(out, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(records)
    subprocess.run(["python3", "scripts/write_figure_review_register.py"], check=True, cwd=ROOT)
    PROVENANCE.write_text(
        "# Balanoglossus — source-credited QA morphology plate\n\n"
        f"Diagram ID: \`{DIAGRAM}\`; Unit I, Hemichordata, page 1.\n\n"
        f"Source: [1905 New International Encyclopaedia illustration]({SOURCE_PAGE}).\n\n"
        f"Creator: {CREATOR}. Copyright: {RIGHTS}.\n"
        f"Original downloaded PNG SHA-256: \`{original_sha}\`.\n"
        f"Adapted PNG SHA-256: \`{digest}\`.\n\n"
        "Cropped **figure 9 only** from a larger multi-taxon original with padded ends, rotated "
        "anti-clockwise to put the proboscis at left, proportionally resized, "
        "and added a modern anatomical key. No original label is represented "
        "as an independent modern anatomical approval.\n\n"
        "**Scientific review pending; Tamil caption review pending; "
        "physical-device readability and zoom acceptance pending.**\n\n"
        "The excluded figure 10 calls the stomochord a supposed notochord, "
        "an obsolete homology claim. It must not be used to explain the "
        "defining notochord of true chordates.\n",
        encoding="utf-8")
    print(f"STAGED provisional Balanoglossus drawing: {len(data)} bytes, sha256 {digest}")
    print("No anatomical approval or release permission granted.")


if __name__ == "__main__":
    stage()
