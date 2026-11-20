#!/usr/bin/env python3
"""One-time, fail-closed scientific correction for registered figure 49.

Render the corrected SVG using CairoSVG, update only this PNG's provenance
hashes and invalidate the earlier, exact-PNG owner display decision. Do not
silently confer independent Zoology, Tamil, or legal/rights approval.
"""
from __future__ import annotations

from hashlib import sha256
from io import BytesIO
from pathlib import Path
import json

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
SVG = ROOT / "docs/original_plate_svg/avian_aerofoil_en.svg"
PNG = ASSETS / "pencil_plates/avian_aerofoil_en.png"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
ID = "u5-flight-adaptations-wing-aerodynamics"
OLD_PNG_HASH = "7021e9247f61ba90587567bcbeadc3b0dea05e74ada0adf39cc393cf338a20bf"
OLD_SVG_HASH = "bd773222bd66837571907053ada51309fa4cf6e275c293a1475e95cfb1c31412"

old_svg = SVG.read_bytes()
old_png = PNG.read_bytes()
doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
matches = [f for f in doc["figures"] if f["diagramId"] == ID and f["lang"] == "en"]
assert len(matches) == 1, "Figure 49 must be exactly one English registered variant"
figure = matches[0]
assert sha256(old_png).hexdigest() == figure["sha256"] == OLD_PNG_HASH
assert sha256(old_svg).hexdigest() == figure["svgSha256"] == OLD_SVG_HASH
assert figure["svgMaster"] == "docs/original_plate_svg/avian_aerofoil_en.svg"
assert figure["topicId"] == "u5-flight-adaptations"
assert figure["sectionKey"] == "wing-aerodynamics"

source = old_svg.decode("utf-8")
assert source.count("Lift (net aerodynamic force)") == 1
assert source.count("Camber, leading edge, trailing edge and net aerodynamic force") == 1
source = source.replace("Lift (net aerodynamic force)", "Lift (perpendicular to airflow)")
source = source.replace(
    "Camber, leading edge, trailing edge and net aerodynamic force",
    "Camber, leading edge, trailing edge and lift vector (drag omitted)"
)
# The original artwork's flow field and wing geometry remain unchanged.
# Clarify the vector decomposition and the known equal-transit-time fallacy.
assert source.count("Lift (perpendicular to airflow)") == 1
assert "Lift (net aerodynamic force)" not in source
svg_data = source.encode("utf-8")
png_rgba = cairosvg.svg2png(bytestring=svg_data, output_width=1800, output_height=1120)
with Image.open(BytesIO(png_rgba)) as image:
    assert image.size == (1800, 1120)
    canvas = image.convert("RGB")
    out = BytesIO()
    canvas.save(out, format="PNG", optimize=True)
    png_data = out.getvalue()
assert png_data[:8] == bytes.fromhex("89504e470d0a1a0a")
assert len(png_data) > 9000

figure["sha256"] = sha256(png_data).hexdigest()
figure["size"] = len(png_data)
figure["svgSha256"] = sha256(svg_data).hexdigest()
figure["modifications"] = (
    "2026-11-20 scientific correction: lifted vector now labelled as the "
    "component perpendicular to airflow; total force must include drag. "
    "Original wing and streamlines retained, SVG regenerated to PNG."
)
figure["visualReview"] = "SOURCE_LABEL_ERROR_CORRECTED_PENDING_INDEPENDENT_QA"
figure["reviewStatus"] = "PROVISIONAL_QA_ANATOMICAL_REVIEW_PENDING"
# Owner's old approval belongs to the old SHA; never transfer it.
assert figure.pop("ownerQaAcceptedSha256") == OLD_PNG_HASH
assert figure.pop("ownerQaDisplayDecision") == "OWNER_APPROVED_PROVISIONAL_QA_USE_2026-11-13"
figure["ownerQaDisplayScope"] = (
    "Earlier display approval was hash-bound to the retired PNG. Revised "
    "image pending renewed owner display approval and independent review."
)
SVG.write_bytes(svg_data)
PNG.write_bytes(png_data)
MANIFEST.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("PASS: Figure 49 corrected; all original diagram slots preserved")
print("SVG SHA-256", figure["svgSha256"])
print("PNG SHA-256", figure["sha256"])
print("PNG bytes", figure["size"])
print("Owner QA display decision: revoked for changed pixels; independent sign-off pending")
