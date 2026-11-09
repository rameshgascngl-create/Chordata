#!/usr/bin/env python3
"""Source-authentic eight-photo marine mammal comparison for Unit V QA.

Replaces only the registered non-anatomical classification schematic.
Preserves the photographs and compositing layout; enlargement is a declared
Lanczos resampling to satisfy the native app's >=1200px figure contract,
NOT an increase in source photographic detail.
"""
from __future__ import annotations

import csv
from hashlib import sha1, sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
DEST = ASSETS / "pencil_plates/aquatic_mammal_lineages_en.png"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
REPORT = ROOT / "docs/CHORDATA_AUTHENTIC_MARINE_MAMMALS_PHOTO_QA.md"

ID = "u5-aquatic-mammals-aquatic-mammal-groups"
OLD_SHA = "a330620a0fb6d62fab65caf6c79fd50ee24a686c83bc3a49b034623bfbc987c3"
SOURCE_SHA1 = "14e680878f8b8e43c4772725a20fbc2c7387eb16"
SOURCE_BYTES = 1776843
PAGE = "https://commons.wikimedia.org/wiki/File:Marine_mammals.png"
ORIGINAL = "https://upload.wikimedia.org/wikipedia/commons/1/1c/Marine_mammals.png"
ALTERNATE = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Marine_mammals.png"
BY_SA4 = "https://creativecommons.org/licenses/by-sa/4.0/"
AUTHOR = "Готлиб XI (2025 marine-mammal photomontage); eight original photographic creators individually credited"

# Gallery order is fixed by the original unmodified montage, two columns x four rows.
CREDITS = [
  ("row 1 left", "Polar bear", "Ursus maritimus", "Ansgar Walk", "CC BY-SA 2.5",
   "https://commons.wikimedia.org/wiki/File:Ursus_maritimus_4_1996-08-04.jpg"),
  ("row 1 right", "Sea otter", "Enhydra lutris", "Mike Baird", "CC BY 2.0",
   "https://commons.wikimedia.org/wiki/File:Kalan_(brownish).jpg"),
  ("row 2 left", "Walrus", "Odobenus rosmarus", "Ansgar Walk", "CC BY-SA 3.0",
   "https://commons.wikimedia.org/wiki/File:7_Walross_1999.jpg"),
  ("row 2 right", "Bearded seal", "Erignathus barbatus",
   "Michael Haferkamp (Mikesegeln); crop by Abyssal",
   "CC BY-SA 3.0 / cropped derivative CC BY-SA 4.0",
   "https://commons.wikimedia.org/wiki/File:Beardedseal2_cropped.jpg"),
  ("row 3 left", "West Indian manatee", "Trichechus manatus", "NOAA",
   "US federal public domain",
   "https://commons.wikimedia.org/wiki/File:Trichechus_manatus,_NOAA.jpg"),
  ("row 3 right", "Dugong", "Dugong dugon", "Camille Ménard",
   "CC BY-SA 3.0",
   "https://commons.wikimedia.org/wiki/File:Dugong_marsa_alam_egypt_2011.jpg"),
  ("row 4 left", "Dolphin", "Cetacea — dolphin (species unspecified)",
   "Gobierno CDMX", "CC0 1.0",
   "https://commons.wikimedia.org/wiki/File:Dolphin_(28425903296).jpg"),
  ("row 4 right", "Humpback whale", "Megaptera novaeangliae",
   "Fritz Geller-Grimm", "CC BY-SA 2.5",
   "https://commons.wikimedia.org/wiki/File:Humpback_Whale_fg1.jpg"),
]


def fetch_source():
    failures = []
    for url in (ORIGINAL, ALTERNATE):
        request = Request(url, headers={
            "User-Agent": "CHORDATA-College-Zoology-QA/1.0 (https://github.com/rameshgascngl-create/Chordata)",
            "Referer": "https://commons.wikimedia.org/",
            "Accept": "image/png",
        })
        try:
            with urlopen(request, timeout=85) as response:
                data = response.read(SOURCE_BYTES + 1)
            if len(data) != SOURCE_BYTES or sha1(data).hexdigest() != SOURCE_SHA1:
                raise ValueError(f"mismatched source length/SHA1: {len(data)} {sha1(data).hexdigest()}")
            source = Image.open(BytesIO(data))
            source.load()
            if source.format != "PNG" or source.size != (794, 1305):
                raise ValueError(f"wrong source dimensions or type: {source.size}/{source.format}")
            return data, source, url
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            failures.append(f"{url}: {exc}")
    raise RuntimeError("Original source cannot be byte-verified; no app image replaced. " + " | ".join(failures))


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    matches = [x for x in manifest["figures"] if x["diagramId"] == ID]
    if len(matches) != 1:
        raise ValueError("Marine-mammal figure registry requires exactly one entry")
    figure = matches[0]
    if (figure.get("lang"), figure.get("path"), figure.get("topicId"),
        figure.get("page"), figure.get("sectionKey")) != (
        "en", "pencil_plates/aquatic_mammal_lineages_en.png",
        "u5-aquatic-mammals", 1, "marine-lineages"):
        raise ValueError("Source image would be placed in wrong lesson")
    if figure["sha256"] != OLD_SHA or sha256(DEST.read_bytes()).hexdigest() != OLD_SHA:
        raise ValueError("Installed marine-mammal plate changed independently; overwrite refused")

    source_bytes, image, actual_source = fetch_source()
    # Existing audit requires 1200px minimum width. This is storage resampling,
    # not restored resolution and not fabrication of new photographic detail.
    rgb = image.convert("RGB")
    resized = rgb.resize((1588, 2610), Image.Resampling.LANCZOS)
    output = BytesIO()
    resized.save(output, format="PNG", optimize=True, compress_level=9)
    installed = output.getvalue()
    if not installed.startswith(bytes.fromhex("89504e470d0a1a0a")):
        raise ValueError("Invalid output PNG")
    actual_sha = sha256(installed).hexdigest()

    for field in ("svgMaster", "svgSha256", "artworkDisposition", "reviewerNote"):
        figure.pop(field, None)
    figure.update({
        "sha256": actual_sha, "size": len(installed),
        "author": AUTHOR,
        "license": "CC BY-SA 4.0 — original photographic montage; all eight component creators credited",
        "licenseUrl": BY_SA4,
        "sourceUrl": PAGE, "sourceImageUrl": ORIGINAL, "sourceSha1": SOURCE_SHA1,
        "sourceSha256": [sha256(source_bytes).hexdigest()],
        "sourceKind": "AUTHENTIC_2025_EIGHT_MARINE_MAMMAL_PHOTOMONTAGE_SCALED_PNG",
        "sourceFormat": "PNG", "installedFormat": "PNG",
        "sourceOriginalDimensions": "794x1305",
        "installedDimensions": "1588x2610",
        "componentCredits": [
            {"position":pos, "name":name, "taxon":taxon, "creator":creator,
             "license":license_name, "sourceUrl":url}
            for pos, name, taxon, creator, license_name, url in CREDITS
        ],
        "referenceUrls": [PAGE, "https://www.noaa.gov/education/resource-collections/marine-life/marine-mammals"]
                         + [x[5] for x in CREDITS],
        "modifications": (
            "Original eight photograph collage, its grid, colours, positions and photographs "
            "retained; image enlarged uniformly from 794x1305 to 1588x2610 pixels with "
            "Lanczos resampling only to meet existing Android minimum PNG width. "
            "The source photographic resolution is still 794x1305; upscaling adds "
            "NO genuine anatomical detail. No AI, tracing, cropping, redrawing or labels."
        ),
        "keyEn": (
            "PHOTO KEY: Row 1 polar bear (left), sea otter (right); "
            "row 2 walrus (left), bearded seal (right); "
            "row 3 West Indian manatee (left), dugong (right); "
            "row 4 dolphin (left), humpback whale (right). "
            "These examples represent distinct mammalian evolutionary branches: "
            "Cetacea, Sirenia and marine Carnivora (including pinnipeds). "
            "Polar bears are semi-aquatic marine-associated carnivorans, not obligate "
            "fully aquatic mammals. Similar streamlining evolved independently; "
            "this photo montage is NOT a taxonomic phylogenetic tree."
        ),
        "keyTa": (
            "ஒளிப்பட விளக்கம்: முதல் வரிசை — இடது துருவக் கரடி, வலது கடல் நீர்நாய்; "
            "இரண்டாம் வரிசை — இடது வால்ரஸ், வலது தாடியுள்ள கடல் நாய்; "
            "மூன்றாம் வரிசை — இடது மானாட்டி, வலது கடற்பசு (டுகாங்); "
            "நான்காம் வரிசை — இடது டால்பின், வலது கூன்முதுகுத் திமிங்கிலம். "
            "Cetacea, Sirenia, Pinnipedia போன்ற குழுக்கள் ஒரே பரிணாமக் கிளையிலிருந்து "
            "தோன்றியவை அல்ல. நீர்வாழ்விற்கு ஏற்ற நெறிப்பட்ட உடலமைப்பு "
            "வெவ்வேறு பாலூட்டிகளிலும் தனித்தனியாக உருவாகியுள்ளது. "
            "துருவக் கரடி முற்றிலும் நீர்வாழ் உயிரினம் அன்று. "
            "இது பரிணாமக் கிளைவரைபடம் அன்று."
        ),
        "scope": (
            "Eight authentic photographs illustrate convergent aquatic and semi-aquatic "
            "adaptations among Cetacea, Sirenia, pinnipeds and other carnivorans; "
            "not a complete phylogenetic or morphological atlas."
        ),
        "visualReview": "AUTHENTIC_MONTAGE_PROVISIONAL__SOURCE_RESOLUTION_794PX__PHONE_AND_HUMAN_QA_PENDING",
        "reviewStatus": "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        "topicId": "u5-aquatic-mammals", "page": 1, "sectionKey": "marine-lineages",
        "learningObjective": "Illustrate convergent aquatic adaptation in diverse mammalian lineages",
    })

    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        columns, rows = reader.fieldnames, list(reader)
    hit = [row for row in rows if row["diagramId"] == ID]
    if len(hit) != 1:
        raise RuntimeError("Marine-mammal coverage ledger wrong or duplicated")
    hit[0]["author"] = AUTHOR
    hit[0]["referenceSources"] = PAGE + " | " + " | ".join(x[5] for x in CREDITS)

    # Modifications stay local to the ephemeral CI runner until ALL audits pass.
    DEST.write_bytes(installed)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Preserve untouched ledger rows byte-for-byte. csv.DictWriter's default
    # CRLF line endings would rewrite all 64 rows and fail git diff --check.
    # Only the one registered row is permitted to change here.
    original_ledger = LEDGER.read_bytes().decode("utf-8")
    old_lines = original_ledger.splitlines(keepends=True)
    amended = []
    changed_rows = 0
    for line in old_lines:
        if line.startswith(ID + "\t"):
            body = line.rstrip("\r\n")
            ending = line[len(body):]
            fields = body.split("\t")
            if len(fields) != len(columns):
                raise ValueError("Existing marine-mammal ledger row has invalid columns")
            fields[columns.index("author")] = AUTHOR
            fields[columns.index("referenceSources")] = hit[0]["referenceSources"]
            line = "\t".join(fields) + ending
            changed_rows += 1
        amended.append(line)
    if changed_rows != 1:
        raise ValueError("Could not find the unique marine-mammal ledger row")
    LEDGER.write_bytes("".join(amended).encode("utf-8"))
    subprocess.run(["python3", "scripts/write_figure_review_register.py"], cwd=ROOT, check=True)

    REPORT.write_text(
        "# CHORDATA — Source-credited aquatic mammal photomontage (QA only)\n\n"
        f"Registered diagram: `{ID}`; Unit V, page 1, marine-lineages.\n"
        f"Montage by Готлиб XI (26 April 2025): {PAGE} — CC BY-SA 4.0.\n"
        f"Exact source: {actual_source}; PNG original size: 794 x 1305, "
        f"{len(source_bytes)} bytes; original SHA-1: {SOURCE_SHA1}; "
        f"SHA-256: {sha256(source_bytes).hexdigest()}.\n"
        f"Installed PNG SHA-256: {actual_sha}; {len(installed)} bytes; "
        "1588 x 2610 by proportional 2x Lanczos interpolation. "
        "**The resize does not restore detail absent in the original.**\n\n"
        "## Image component rights (eight separate original photographs)\n\n"
        + "\n".join(f"- {pos}: {name}, {taxon} — {creator} — {licence}, {url}"
                      for pos, name, taxon, creator, licence, url in CREDITS)
        + "\n\n**Scientific scope:** distinct evolutionary groups, not a monophyletic "
          "aquatic-mammal order. Polar bears are marine-associated and semi-aquatic. "
          "Photomontage shows no phylogenetic branching or species-specific dissection.\n\n"
          "**Hold:** independent biology review, Tamil wording, 360-pixel phone readability, "
          "100/200% scaling, pinch zoom and physical-device assessment. This is NOT "
          "academic approval or production release.\n",
        encoding="utf-8"
    )
    print(f"PASS 2025 marine mammal photo source ({len(source_bytes)} original bytes); "
          f"installed PNG {len(installed)} bytes SHA-256 {actual_sha}")


if __name__ == "__main__":
    main()
