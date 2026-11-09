#!/usr/bin/env python3
"""Make one credited, original-photo-based classroom montage of India's Big Four snakes.

All source photographs are individually licensed on Wikimedia Commons. This script
never draws/generates snakes, modifies source morphology, diagnoses bites or approves
the provisional QA figure for production.
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

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
DEST = ASSETS / "pencil_plates/india_big_four_snakes_en.png"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
REPORT = ROOT / "docs/CHORDATA_BIG_FOUR_AUTHENTIC_PHOTOS_QA_20261109.md"

DIAGRAM = "u4-snakes-india-big-four-identification"
BEFORE = "68fa916626a60be5bbfd62cc31b3d8f19534a6913eba12e64d12642c4f3f3edf"
CC4 = "https://creativecommons.org/licenses/by-sa/4.0/"

# Source taxonomy, creator and copyright records were individually checked
# on each original Commons page; a downloaded file must match its published
# dimensions and, for the krait, the structured-data SHA-1.
SOURCES = [
    {
      "name": "Indian cobra", "taxon": "Naja naja", "creator": "Holger Krisp",
      "sourceUrl": "https://commons.wikimedia.org/wiki/File:Naja-naja-kobra.jpg",
      "downloadUrl": "https://upload.wikimedia.org/wikipedia/commons/3/35/Naja-naja-kobra.jpg",
      "width": 3414, "height": 2250, "sourceLicense": "CC BY 3.0 Unported",
      "sourceLicenseUrl": "https://creativecommons.org/licenses/by/3.0/",
      "sourceSha1Expected": None,
      "visualLimit": "Coiled live cobra close-up; an expanded hood is not shown",
    },
    {
      "name": "Common krait", "taxon": "Bungarus caeruleus", "creator": "Raju Kidoor",
      "sourceUrl": "https://commons.wikimedia.org/wiki/File:Common_Krait.jpg",
      "downloadUrl": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Common_Krait.jpg",
      "width": 3264, "height": 2448, "sourceLicense": "CC BY-SA 4.0 International",
      "sourceLicenseUrl": CC4,
      "sourceSha1Expected": "630871ba03d9a1bff99816d41fb9378c22304b61",
      "visualLimit": "Live specimen at a wall; white cross-bands are specimen-specific",
    },
    {
      "name": "Russell's viper", "taxon": "Daboia russelii", "creator": "Billyakhtar",
      "sourceUrl": "https://commons.wikimedia.org/wiki/File:Russell%27s_viper.jpg",
      "downloadUrl": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Russell%27s_viper.jpg",
      "width": 1959, "height": 1102, "sourceLicense": "CC BY-SA 4.0 International",
      "sourceLicenseUrl": CC4,
      "sourceSha1Expected": None,
      "visualLimit": "Live curled specimen showing chain-like ocelli, not full body length",
    },
    {
      "name": "Saw-scaled viper", "taxon": "Echis carinatus", "creator": "Jnprasad2001",
      "sourceUrl": "https://commons.wikimedia.org/wiki/File:Saw-scaled_Viper.jpg",
      "downloadUrl": "https://upload.wikimedia.org/wikipedia/commons/c/c0/Saw-scaled_Viper.jpg",
      "width": 4000, "height": 2256, "sourceLicense": "CC BY-SA 4.0 International",
      "sourceLicenseUrl": CC4,
      "sourceSha1Expected": None,
      "visualLimit": "Live small viper; close-up scaled body, not a universal identification key",
    },
]


def exact_photo(source: dict) -> tuple[bytes, Image.Image]:
    req = Request(source["downloadUrl"], headers={
        "User-Agent": "CHORDATA-Original-Photo-QA/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer": "https://commons.wikimedia.org/",
        "Accept": "image/jpeg,*/*",
    })
    try:
        with urlopen(req, timeout=90) as response:
            raw = response.read(12_000_001)
    except (HTTPError, URLError, OSError, TimeoutError) as exc:
        raise RuntimeError("Source download failed without changing app: "
                           + source["sourceUrl"] + ": " + str(exc)) from exc
    if not 120_000 <= len(raw) < 12_000_000:
        raise RuntimeError("Unexpected original photo byte count: " + source["sourceUrl"])
    if source.get("sourceSha1Expected") and sha1(raw).hexdigest() != source["sourceSha1Expected"]:
        raise RuntimeError("Krait original Commons SHA-1 changed, do not use altered photo")
    image = Image.open(BytesIO(raw))
    image.load()
    if image.format != "JPEG" or image.size != (source["width"], source["height"]):
        raise RuntimeError("Unexpected photographer's original dimensions or format: "
                           + source["sourceUrl"] + str((image.format, image.size)))
    return raw, ImageOps.exif_transpose(image).convert("RGB")


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    raise RuntimeError("No required legible TrueType font on runner; artwork not changed")


def compose(records: list[tuple[dict, Image.Image]]) -> bytes:
    W, H = 2400, 1900
    margin, gap, title_h, foot_h = 30, 20, 100, 145
    card_w = (W - 2 * margin - gap) // 2
    card_h = (H - title_h - foot_h - 2 * margin - gap) // 2
    canvas = Image.new("RGB", (W, H), (249, 249, 247))
    draw = ImageDraw.Draw(canvas)
    header = font(60)
    caption = font(42)
    small = font(35)
    draw.text((margin, 19), "FOUR MEDICALLY IMPORTANT SNAKES OF INDIA", font=header, fill=(22, 28, 29))
    for ix, (source, image) in enumerate(records):
        col, row = ix % 2, ix // 2
        x = margin + col * (card_w + gap)
        y = title_h + margin + row * (card_h + gap)
        draw.rectangle((x, y, x + card_w, y + card_h), fill=(255, 255, 255), outline=(180, 180, 180), width=3)
        photo_h = card_h - 96
        thumb = ImageOps.contain(image, (card_w - 24, photo_h - 16), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (x + (card_w - thumb.width) // 2,
                             y + 8 + (photo_h - 16 - thumb.height) // 2))
        label = f"{source['name']}  ({source['taxon']})"
        draw.text((x + 18, y + card_h - 80), label, font=caption, fill=(18, 24, 28))
    fy = H - foot_h + 8
    draw.text((margin, fy), "TEACHING PHOTO MONTAGE — NOT A FIELD IDENTIFICATION OR TREATMENT GUIDE", font=small, fill=(110, 30, 30))
    draw.text((margin, fy + 59), "Do not approach or handle snakes. Suspected bite: immobilise and seek urgent medical care.", font=small, fill=(50, 50, 50))
    out = BytesIO()
    canvas.save(out, format="PNG", optimize=True, compress_level=9)
    return out.getvalue()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    matches = [x for x in manifest["figures"] if x.get("diagramId") == DIAGRAM]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one registered Big Four diagram")
    figure = matches[0]
    if not (figure.get("lang") == "en"
            and figure.get("path") == "pencil_plates/india_big_four_snakes_en.png"
            and figure.get("topicId") == "u4-snakes-india"
            and figure.get("page") == 2
            and figure.get("sectionKey") == "big-four"
            and figure.get("sha256") == BEFORE
            and sha256(DEST.read_bytes()).hexdigest() == BEFORE):
        raise RuntimeError("The original Big Four figure changed or mapping is wrong; no overwrite")

    verified = []
    for source in SOURCES:
        raw, im = exact_photo(source)
        verified.append((source, im))
        source["sourceSha1"] = sha1(raw).hexdigest()
        source["sourceSha256"] = sha256(raw).hexdigest()
        source["originalSize"] = len(raw)
    out = compose(verified)
    if out[:8] != bytes.fromhex("89504e470d0a1a0a"):
        raise RuntimeError("Composite PNG encoding invalid")
    composite_sha = sha256(out).hexdigest()

    for key in ("svgMaster", "svgSha256", "artworkDisposition", "reviewerNote"):
        figure.pop(key, None)
    figure.update({
        "sha256": composite_sha, "size": len(out),
        "author": "CHORDATA QA (photo montage layout); originals by Holger Krisp, Raju Kidoor, Billyakhtar and Jnprasad2001",
        "license": "CC BY-SA 4.0 derivative photo montage; cobra source CC BY 3.0; source creator credits retained",
        "licenseUrl": CC4,
        "sourceUrl": SOURCES[0]["sourceUrl"],
        "sourceUrls": [s["sourceUrl"] for s in SOURCES],
        "sourceSha256": [s["sourceSha256"] for s in SOURCES],
        "sourceSha1List": [s["sourceSha1"] for s in SOURCES],
        "photoCredits": SOURCES,
        "sourceKind": "AUTHENTIC_FOUR_SNAKE_PHOTO_MONTAGE__CC_BY_SA_4",
        "installedFormat": "PNG",
        "sourceFormat": "Four original Wikimedia Commons JPEG photographs",
        "referenceUrls": [s["sourceUrl"] for s in SOURCES] + [
            "https://www.who.int/teams/control-of-neglected-tropical-diseases/snakebite-envenoming/treatment",
            "https://ncdc.mohfw.gov.in/wp-content/uploads/2024/07/NATIONAL-ACTION-PLAN-FOR-PREVENTION-AND-CONTROL-OF-SNAKEBITE-ENVENOMING-NAPSE.pdf",
        ],
        "modifications": (
            "Four individually credited JPEG photos proportionally reduced into 2x2 white-background "
            "PNG teaching poster with English name captions and a safety warning. No crop, "
            "anatomical redraw, image generation, photo retouching or false labelling."
        ),
        "keyEn": (
            "Photographs (clockwise from upper left): Indian cobra (Naja naja), "
            "common krait (Bungarus caeruleus), saw-scaled viper (Echis carinatus), "
            "Russell's viper (Daboia russelii). These are illustrative examples, "
            "NOT reliable identification criteria after a bite; other dangerous Indian snakes also occur. "
            "Never attempt to catch or approach a snake. Snakebite assessment must not wait for "
            "identification: immobilise the person, avoid tourniquets/incisions/suction and seek "
            "urgent medical care regardless of suspected species (WHO; NCDC India)."
        ),
        "keyTa": (
            "இந்தியாவில் மருத்துவ முக்கியத்துவம் வாய்ந்த நான்கு விஷப்பாம்புகளின் ஒளிப்படத் தொகுப்பு: "
            "மேல் இடது — நாகப்பாம்பு (Naja naja); மேல் வலது — கட்டுவிரியன் (Bungarus caeruleus); "
            "கீழ் இடது — கண்ணாடிவிரியன் (Daboia russelii); கீழ் வலது — சுருட்டைவிரியன் (Echis carinatus). "
            "பாம்பின் நிறம், வடிவம், உடற்குறிகள் மட்டும் கடித்த பாம்பை உறுதியாக இனங்காண உதவாது. "
            "இந்த நான்கு இனங்கள் தவிரவும் ஆபத்தான பாம்புகள் இந்தியாவில் உள்ளன. "
            "கடித்த பாம்பைப் பிடிக்கவோ நெருங்கவோ கூடாது. பாம்புக்கடியில் உடல் அசைவைக் கட்டுப்படுத்தி "
            "உடனடியாக மருத்துவமனைக்கு அழைத்துச் செல்ல வேண்டும்; கயிற்றால் இறுக்கிக் கட்டுதல், "
            "காயத்தை வெட்டுதல், விஷத்தை உறிஞ்சுதல் ஆகியவற்றைச் செய்யக்கூடாது."
        ),
        "scope": "Four living snake species illustrated as source-credit images; education only, not diagnosis or clinical species ID.",
        "visualReview": "SOURCE_VERIFIED_FOUR_LIVE_SNAKES__ACADEMIC_TAMIL_MOBILE_REVIEW_PENDING",
        "reviewStatus": "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        "topicId": "u4-snakes-india", "page": 2, "sectionKey": "big-four",
        "learningObjective": "Recognise cobra, krait, Russell's viper, saw-scaled viper; state why photo-based snakebite triage is unsafe",
    })

    with LEDGER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fields, rows = reader.fieldnames, list(reader)
    match = [r for r in rows if r["diagramId"] == DIAGRAM]
    if len(match) != 1:
        raise RuntimeError("Big Four provenance ledger mismatch")
    match[0]["author"] = figure["author"]
    match[0]["referenceSources"] = " | ".join(s["sourceUrl"] for s in SOURCES)

    # Ephemeral CI workspace: only commit after every quality gate passes.
    DEST.write_bytes(out)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(["python3", "scripts/write_figure_review_register.py"], cwd=ROOT, check=True)
    REPORT.write_text(
        "# CHORDATA — India Big Four live snake photographs; provisional classroom photo montage\n\n"
        f"Registered diagram: {DIAGRAM}; Unit IV, page 2, big-four.\n"
        f"Installed PNG: 2400x1900 px; {len(out)} bytes; SHA-256 {composite_sha}.\n"
        "Photographs are authentic natural animal photographs, not museum jars or AI renderings.\n\n"
        "## Source photographs\n"
        + "\n".join(f"- {s['name']} (*{s['taxon']}*): {s['creator']}, {s['sourceLicense']}, "
                      f"{s['sourceUrl']}, JPEG SHA-1 {s['sourceSha1']}, "
                      f"SHA-256 {s['sourceSha256']}; {s['width']}x{s['height']}; "
                      f"{s['visualLimit']}" for s in SOURCES)
        + "\n\nComposite attribution: photos by the four named creators, CHORDATA QA arranged "
        "the poster and added text. Layout derivative is CC BY-SA 4.0. "
        "No anatomy was redrawn or inferred from photographs.\n\n"
        "This is a comparative teaching montage, NOT a snakebite field identification, "
        "diagnosis or first-aid decision tool. In India, professional snakebite care "
        "must not wait for identification. Reference: WHO snakebite guidance and Indian "
        "NCDC national action plan, linked in the figure manifest.\n\n"
        "Biology, Tamil, 100/200% viewport, zoom, physical device and production approvals PENDING.\n",
        encoding="utf-8",
    )
    print("PASS authentic Big Four live-photo PNG SHA-256", composite_sha, "bytes", len(out))


if __name__ == "__main__":
    main()
