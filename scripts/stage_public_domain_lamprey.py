#!/usr/bin/env python3
"""Stage one source-credited, anatomically specific adult/ammocoete plate.

This runs on an isolated QA branch. It never grants scientific acceptance.
The adult illustration and larval illustration depict different lamprey
taxa, and their juxtaposition is explicitly *not to scale*.
"""
from __future__ import annotations
import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
TARGET = ASSETS / "pencil_plates/lamprey_adult_ammocoete.png"
LEDGER = ROOT / "docs/figure-coverage.tsv"
REVIEW = ROOT / "docs/FIGURE_REVIEW_REGISTER_64.csv"
PROVENANCE = ROOT / "docs/CHORDATA_SOURCED_LAMPREY_QA.md"
EVIDENCE = ROOT / "build/sourced_morphology_qa"
ID = "u1-agnatha-petromyzon-adult-larva"

SOURCES = (
    {
        "name": "Adult lamprey",
        "url": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Lamprey_illustration_side.png",
        "page": "https://commons.wikimedia.org/wiki/File:Lamprey_illustration_side.png",
        "size": (3816, 2368), "author": "LadyofHats",
        "license": "Public domain — released by the illustrator, 2005",
    },
    {
        "name": "Ammocoete larva",
        "url": ("https://upload.wikimedia.org/wikipedia/commons/1/1c/"
                "FMIB_48179_Larval_Form_of_Petromyzon_branchialis%2C_Formerly_Known_as_Ammocoetes.jpeg"),
        "page": ("https://commons.wikimedia.org/wiki/File:"
                 "FMIB_48179_Larval_Form_of_Petromyzon_branchialis,_Formerly_Known_as_Ammocoetes.jpeg"),
        "size": (940, 339), "author": "Harry Govier Seeley (1886)",
        "license": "Public domain — University of Washington Freshwater and Marine Image Bank",
    }
)
CREDIT = "LadyofHats (adult); H. G. Seeley, 1886 (larva); CHORDATA QA (layout)"
LICENSE = "Public domain: LadyofHats dedication; Seeley 1886 / UW Image Bank"


def fetch_image(source):
    request = Request(source["url"], headers={
        "User-Agent": "ChordataQAArtImport/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer": "https://commons.wikimedia.org/",
        "Accept": "image/png,image/jpeg,*/*",
    })
    with urlopen(request, timeout=45) as response:
        data = response.read(8_000_001)
    if len(data) > 8_000_000 or len(data) < 30_000:
        raise ValueError("Unexpected source byte length: " + source["name"])
    image = Image.open(BytesIO(data))
    image.load()
    if image.size != source["size"] or image.format not in ("PNG", "JPEG"):
        raise ValueError("Source image changed: " + source["name"] +
                         f" {image.size} {image.format}")
    return image.convert("RGB"), sha256(data).hexdigest()


def font(size, bold=False):
    files = (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
             if bold else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for path in files:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise RuntimeError("Pinned image build requires system DejaVu Sans font")


def contain(image, box):
    w, h = box
    return ImageOps.contain(image, (w, h), Image.Resampling.LANCZOS)


def stage():
    (adult, adult_sha), (larva, larva_sha) = [fetch_image(s) for s in SOURCES]
    # Remove the unrelated prey fish above the adult. Keep the actual external
    # lamprey with its dorsal and caudal fins; published label lines are not
    # used as a replacement for the separate, readable explanatory key.
    adult = adult.crop((70, 1370, 3650, 2100))
    # The 1886 source also contains a detached mouth detail and typeset text.
    # Isolate the continuous larval body, not that separate inset.
    larva = larva.crop((125, 28, 920, 278))
    canvas = Image.new("RGB", (2200, 1530), "#fffefa")
    pen = ImageDraw.Draw(canvas)
    ink = "#162a35"
    pen.text((100, 65), "Lamprey: adult and ammocoete", font=font(71, True), fill=ink)
    pen.text((105, 178), "A  Adult lamprey — representative external anatomy",
             font=font(43, True), fill=ink)
    pen.rounded_rectangle((90, 248, 2110, 709), radius=23, outline="#8c9ba4", width=3, fill="white")
    upper = contain(adult, (1930, 415))
    canvas.paste(upper, (110 + (1980 - upper.width)//2, 265 + (420 - upper.height)//2))

    pen.text((105, 758), "B  Ammocoete — river lamprey (Lampetra fluviatilis)",
             font=font(43, True), fill=ink)
    pen.rounded_rectangle((90, 828, 2110, 1370), radius=23, outline="#8c9ba4", width=3, fill="white")
    lower = contain(larva, (1920, 465))
    canvas.paste(lower, (125 + (1940 - lower.width)//2, 860 + (475 - lower.height)//2))

    pen.text((105, 1400),
             "Different source species and sizes. The two illustrations are NOT to scale.",
             font=font(35), fill="#43535c")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(TARGET, format="PNG", optimize=True)
    png = TARGET.read_bytes()
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "lamprey_candidate.png").write_bytes(png)
    digest = sha256(png).hexdigest()

    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = [x for x in m["figures"] if x["diagramId"] == ID]
    if len(entries) != 1 or entries[0]["lang"] != "shared":
        raise ValueError("Expected exactly one shared adult/larva plate")
    entry = entries[0]
    entry.update(
        sha256=digest, size=len(png), author=CREDIT, license=LICENSE,
        sourceUrl=SOURCES[0]["page"], sourceUrls=[s["page"] for s in SOURCES],
        licenseUrl="https://creativecommons.org/publicdomain/mark/1.0/",
        sourceSha256=[adult_sha, larva_sha],
        modifications=("Adult anatomy region isolated; historic larval body isolated; "
                       "both placed in a labelled comparison without proportional distortion."),
        keyEn=("A: adult lamprey (generalised external anatomy). B: ammocoete larva "
               "illustrated from L. fluviatilis. Different taxa; not to scale."),
        keyTa=("A: வளர்ந்த லாம்ப்ரே மீன் (பொதுவான புற அமைப்பு). B: லாம்ப்ரே இளம் "
               "உயிரி (Lampetra fluviatilis). வெவ்வேறு உயிரினங்களின் படங்கள்; ஒரே அளவுகோல் அல்ல."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
    )
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with LEDGER.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        fields = reader.fieldnames
        rows = list(reader)
    matches = [row for row in rows if row["diagramId"] == ID]
    if len(matches) != 1:
        raise ValueError("Coverage ledger missing precise lamprey slot")
    matches[0]["author"] = CREDIT
    matches[0]["referenceSources"] = " | ".join(s["page"] for s in SOURCES)
    with LEDGER.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    # The existing generator preserves human notes but resets approval whenever
    # any image byte changes. No fabricated scientific or Tamil signatures.
    import subprocess
    subprocess.run(["python3", str(ROOT / "scripts/write_figure_review_register.py")],
                   check=True, cwd=ROOT)
    PROVENANCE.write_text(
        "# CHORDATA — source-credited lamprey comparison (provisional QA)\n\n"
        f"Diagram ID: \`{ID}\` — Unit I, Agnatha, lesson page 2.\n\n"
        "## Source drawings and reuse\n\n"
        + "\n".join(
            f"- **{s['name']}**: {s['author']}; {s['license']}. "
            f"[Original file]({s['page']}); downloaded source SHA-256 \`{h}\`."
            for s, h in zip(SOURCES, (adult_sha, larva_sha))
        )
        + "\n\n## Alterations\n\n"
        "Non-lamprey fish removed from the adult illustration; typesetting and "
        "isolated mouth inset removed from the historical larval illustration. "
        "Two source drawings were assembled on a new white two-panel teaching "
        "plate. Proportions were preserved within each source; panels are "
        "explicitly not to scale. No museum specimen photographs used.\n\n"
        "## Acceptance\n\n"
        f"Output PNG SHA-256: \`{digest}\`.\n\n"
        "**Scientific review pending; Tamil caption review pending; device "
        "legibility and pinch-zoom verification pending.**\n"
        "Note: Adult illustration is generalized; larval example is attributed "
        "to *Lampetra fluviatilis*. Do not present them as two stages of one "
        "verified species.\n", encoding="utf-8")
    print(f"STAGED QA lamprey comparison: {TARGET}, {len(png)} bytes, sha256 {digest}")
    print("Unapproved: dual academic and Android-device acceptance still required")


if __name__ == "__main__":
    stage()
