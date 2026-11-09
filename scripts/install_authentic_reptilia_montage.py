#!/usr/bin/env python3
"""Stage the exact freely licensed 2012 four-reptile photographic montage as an offline QA PNG.

Strictly source-first: same decoded source pixels; no generative image, new drawing,
crop, resize or altered species labels. Fails closed if old figure, remote bytes,
file hash, registered section or permissions evidence is different.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
DEST = ASSETS / "pencil_plates/living_reptile_groups_en.png"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
REPORT = ROOT / "docs/CHORDATA_REPTILIA_2012_PHOTOGRAPHIC_MONTAGE_QA.md"

DIAGRAM_ID = "u4-reptilia-classification-living-reptile-orders"
OLD_SHA256 = "04a4ac59719db220585ecb123da5c89ffecb4f46279fc2e2aefcd7ce7288243a"
SOURCE_SHA1 = "bb98028bb492b30e0d2df2a50cb975d7df455377"
SOURCE_SIZE = 5902997
PAGE = "https://commons.wikimedia.org/wiki/File:Extant_reptilia.jpg"
SOURCE = "https://upload.wikimedia.org/wikipedia/commons/2/2c/Extant_reptilia.jpg"
ALT = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Extant_reptilia.jpg"
LICENSE = "https://creativecommons.org/licenses/by-sa/3.0/"
AUTHOR = ("Petter Bøckman (2012 reptile montage); component photographs by "
          "Mila Zinkova / Brocken Inaglory, TimVickers, Ester Inbar and Donald Macauley")

COMPONENTS = [
    {
        "position": "upper left", "group": "Testudines",
        "species": "Chelonia mydas",
        "creator": "Mila Zinkova (Wikimedia alias Brocken Inaglory)",
        "url": "https://commons.wikimedia.org/wiki/File:Total_internal_reflection_of_Chelonia_mydas.jpg",
        "license": "CC BY-SA 3.0 (among available licences)",
        "licenseUrl": "https://creativecommons.org/licenses/by-sa/3.0/",
    },
    {
        "position": "upper right", "group": "Rhynchocephalia",
        "species": "Sphenodon punctatus",
        "creator": "TimVickers",
        "url": "https://commons.wikimedia.org/wiki/File:Sphenodon_punctatus_(2).jpg",
        "license": "Public domain — released by creator",
        "licenseUrl": "https://creativecommons.org/publicdomain/mark/1.0/",
    },
    {
        "position": "lower left", "group": "Squamata",
        "species": "Pseudotrapelus sinaitus (historically Agama sinaita)",
        "creator": "Ester Inbar (ST)",
        "url": "https://commons.wikimedia.org/wiki/File:AgamaSinaita01_ST_10.jpg",
        "license": "Freely reusable with attribution (creator's explicit Commons permission)",
        "licenseUrl": "https://commons.wikimedia.org/wiki/File:AgamaSinaita01_ST_10.jpg",
    },
    {
        "position": "lower right", "group": "Crocodylia",
        "species": "Crocodilian representative; exact species not asserted",
        "creator": "Donald Macauley",
        "url": "https://commons.wikimedia.org/wiki/File:Flickr_-_don_macauley_-_Crocodile.jpg",
        "license": "CC BY-SA 2.0",
        "licenseUrl": "https://creativecommons.org/licenses/by-sa/2.0/",
    },
]


def verified_original() -> tuple[bytes, Image.Image]:
    errors = []
    for url in (SOURCE, ALT):
        request = Request(url, headers={
            "User-Agent": "CHORDATA-College-Zoology-QA/1.0 (https://github.com/rameshgascngl-create/Chordata)",
            "Referer": "https://commons.wikimedia.org/",
            "Accept": "image/jpeg,*/*",
        })
        try:
            with urlopen(request, timeout=95) as response:
                original = response.read(SOURCE_SIZE + 1)
            if len(original) != SOURCE_SIZE:
                raise ValueError(f"source byte count {len(original)} != {SOURCE_SIZE}")
            digest = hashlib.sha1(original).hexdigest()
            if digest != SOURCE_SHA1:
                raise ValueError(f"source SHA-1 changed: {digest}")
            image = Image.open(io.BytesIO(original))
            image.load()
            if image.format != "JPEG" or image.size != (3000, 2355):
                raise ValueError(f"unverified format/size: {image.format}, {image.size}")
            return original, image
        except (HTTPError, URLError, OSError, TimeoutError, ValueError) as exc:
            errors.append(f"{url}: {exc}")
    raise RuntimeError("No exact licensed source verified; old PNG not touched. " + " | ".join(errors))


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    found = [x for x in manifest["figures"] if x["diagramId"] == DIAGRAM_ID]
    if len(found) != 1:
        raise RuntimeError("Wrong or duplicate registered Reptilia slot")
    figure = found[0]
    if not (figure.get("lang") == "en"
            and figure.get("path") == "pencil_plates/living_reptile_groups_en.png"
            and figure.get("topicId") == "u4-reptilia-classification"
            and figure.get("page") == 2
            and figure.get("sectionKey") == "living-orders"):
        raise RuntimeError("Reptilia mapping does not match registered lesson")

    old_bytes = DEST.read_bytes()
    if figure["sha256"] != OLD_SHA256 or hashlib.sha256(old_bytes).hexdigest() != OLD_SHA256:
        raise RuntimeError("Installed Reptilia PNG changed independently; refusing overwrite")

    original, source_image = verified_original()
    output = io.BytesIO()
    # Decoding JPEG into an RGB PNG preserves every decoded source pixel.
    source_image.convert("RGB").save(output, format="PNG", optimize=True, compress_level=9)
    png = output.getvalue()
    if png[:8] != bytes.fromhex("89504e470d0a1a0a"):
        raise RuntimeError("Converted source is not PNG")
    png_sha = hashlib.sha256(png).hexdigest()

    # Do not remove the historic SVG master itself: it remains archived in docs.
    for field in ("svgMaster", "svgSha256", "artworkDisposition", "reviewerNote"):
        figure.pop(field, None)
    figure.update({
        "size": len(png), "sha256": png_sha,
        "author": AUTHOR,
        "license": "CC BY-SA 3.0 Unported — Petter Bøckman montage; individual photographer credits recorded",
        "licenseUrl": LICENSE,
        "sourceUrl": PAGE, "sourceImageUrl": SOURCE,
        "sourceSha1": SOURCE_SHA1,
        "sourceSha256": [hashlib.sha256(original).hexdigest()],
        "sourceFormat": "JPEG", "installedFormat": "PNG",
        "sourceKind": "AUTHENTIC_2012_REPTILIA_FOUR_GROUPS_MONTAGE_JPEG_TO_PNG",
        "componentCredits": COMPONENTS,
        "referenceUrls": [PAGE] + [x["url"] for x in COMPONENTS],
        "modifications": (
            "Original 2012 four-photo montage converted from source JPEG to RGB PNG "
            "with source pixel dimensions 3000x2355 and composite layout unchanged. "
            "No drawing, AI generation, cropping, labels, retouching or resampling."
        ),
        "keyEn": (
            "Four living NON-AVIAN reptile lineages, clockwise from top left: "
            "Testudines (green sea turtle), Rhynchocephalia (tuatara), "
            "Crocodylia (crocodilian), Squamata (Sinai agama, lower left). "
            "Each photograph shows just one representative, NOT the whole diversity "
            "of its lineage; Squamata also includes snakes and amphisbaenians. "
            "The montage is NOT a phylogenetic tree or an anatomical dissection; "
            "birds are nested within the broader reptile/sauropsid evolutionary lineage."
        ),
        "keyTa": (
            "தற்காலப் பறவையல்லாத ஊர்வனவற்றின் நான்கு முக்கிய மரபுவழிக் குழுக்கள்: "
            "மேல் இடது — பச்சைக் கடலாமை (Testudines); "
            "மேல் வலது — டுவாட்டாரா (Rhynchocephalia); "
            "கீழ் இடது — சினாய் அகாமா பல்லி (Squamata); "
            "கீழ் வலது — முதலை (Crocodylia). "
            "ஒவ்வொரு ஒளிப்படமும் அந்தக் குழுவின் ஓர் எடுத்துக்காட்டே; "
            "Squamata குழுவில் பாம்புகளும் பிற செதிலுடைய ஊர்வனவும் அடங்கும். "
            "இது பரிணாமக் கிளைவரைபடமோ உடற்கூறியல் துண்டாய்வுப் படமோ அன்று. "
            "பறவைகளும் பரந்த Sauropsida பரிணாம மரபில் அடங்குகின்றன."
        ),
        "scope": (
            "Authenticated four-taxon natural-history photomontage for traditional "
            "non-avian reptile orders; does not itself establish phylogenetic branching "
            "or depict every member of Squamata."
        ),
        "visualReview": "AUTHENTIC_MONTAGE_SOURCE_VERIFIED__BIOLOGY_TAMIL_DEVICE_REVIEW_PENDING",
        "reviewStatus": "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        "topicId": "u4-reptilia-classification",
        "page": 2,
        "sectionKey": "living-orders",
        "learningObjective": "Recognise Testudines, Rhynchocephalia, Squamata and Crocodylia in non-avian reptile diversity",
    })

    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames, rows = reader.fieldnames, list(reader)
    matching = [row for row in rows if row["diagramId"] == DIAGRAM_ID]
    if len(matching) != 1:
        raise RuntimeError("Missing or duplicate coverage-ledger entry")
    matching[0]["author"] = AUTHOR
    matching[0]["referenceSources"] = PAGE + " | " + " | ".join(x["url"] for x in COMPONENTS)

    # Runner is ephemeral; none of these changes is pushed until every gate succeeds.
    DEST.write_bytes(png)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    subprocess.run(["python3", "scripts/write_figure_review_register.py"], cwd=ROOT, check=True)
    REPORT.write_text(
        "# Reptilia classification — source-authentic photographed representatives (QA only)\n\n"
        f"Diagram: `{DIAGRAM_ID}`, Unit IV, page 2, living-orders.\n"
        f"Original compound photograph: {PAGE}\n"
        f"Montage compiler: Petter Bøckman, 12 February 2012; CC BY-SA 3.0.\n"
        f"Original JPEG SHA-1: {SOURCE_SHA1}; SHA-256: {hashlib.sha256(original).hexdigest()}; "
        f"size: {len(original)} bytes; 3000x2355 pixels.\n"
        f"App PNG SHA-256: {png_sha}; {len(png)} bytes; same decoded pixels.\n\n"
        "## Four original component credits\n\n"
        + "\n".join(f"- {c['position']}: {c['group']} — {c['species']}; "
                      f"{c['creator']}; {c['license']}; source {c['url']}" for c in COMPONENTS)
        + "\n\nThe composite is a photographic morphology aid, not a phylogenetic tree. "
        "It shows four non-avian reptilian lineages, not the full phylogenetic definition "
        "of sauropsids; birds remain nested within that broader lineage.\n\n"
        "No original photographer work is credited to an AI generator. "
        "Only lossless storage of decoded source pixels as RGB PNG; original arrangement "
        "was not altered.\n\n"
        "Biology, Tamil editorial, 100/200% phone-scale and physical-device reviews PENDING. "
        "No production approval.\n",
        encoding="utf-8",
    )
    print(f"PASS authentic photographed Reptilia PNG {len(png)} bytes sha256 {png_sha}")
    print("PASS original artwork unchanged except one registered figure and exact metadata")


if __name__ == "__main__":
    main()
