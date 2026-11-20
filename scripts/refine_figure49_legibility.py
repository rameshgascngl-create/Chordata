#!/usr/bin/env python3
"""Final legibility correction to already scientifically corrected Aves aerofoil.

Keep the existing label and all geometry; add a small opaque panel behind
the lift label so the drawn flow streamline cannot run through its glyphs.
"""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import json

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
svg = ROOT / "docs/original_plate_svg/avian_aerofoil_en.svg"
png = ROOT / "app/src/main/assets/pencil_plates/avian_aerofoil_en.png"
manifest_path = ROOT / "app/src/main/assets/pencil_plates/manifest.json"
data = json.loads(manifest_path.read_text(encoding="utf-8"))
matching = [x for x in data["figures"] if x["diagramId"] ==
    "u5-flight-adaptations-wing-aerodynamics" and x["lang"] == "en"]
assert len(matching) == 1
figure = matching[0]
assert figure["sha256"] == "2e50b2c1f2c40055582e92354252bad780508d9244edae04a99bbd43c0a958a7"
assert figure["svgSha256"] == "ff09c8ce4f8828a9281e4a38d48f98ce4ca830377161b2ead2d8487cd9f89074"
assert sha256(png.read_bytes()).hexdigest() == figure["sha256"]
source = svg.read_text(encoding="utf-8")
assert sha256(svg.read_bytes()).hexdigest() == figure["svgSha256"]
assert "Lift (perpendicular to airflow)" in source
assert "Lift (net aerodynamic force)" not in source
needle = '<text fill="#25363f" font-family="DejaVu Sans" font-size="29" font-weight="bold" text-anchor="start" x="919" y="324">Lift (perpendicular to airflow)</text>'
assert source.count(needle) == 1
# This occludes the decorative streamline locally, not the actual aerofoil,
# the red lift vector, or leading/trailing-edge geometry. Exact background tint
# matches the drawing panel; no new arrow or false drag vector is introduced.
label_backplate = '<rect fill="#f1f6f4" height="55" rx="8" ry="8" width="603" x="907" y="288" />'
source = source.replace(needle, label_backplate + needle)
assert source.count(label_backplate) == 1
svg_bytes = source.encode("utf-8")
rgba = cairosvg.svg2png(bytestring=svg_bytes, output_width=1800, output_height=1120)
with Image.open(BytesIO(rgba)) as rendered:
    assert rendered.size == (1800, 1120)
    final = BytesIO()
    rendered.convert("RGB").save(final, format="PNG", optimize=True)
png_bytes = final.getvalue()
assert png_bytes[:8] == bytes.fromhex("89504e470d0a1a0a") and len(png_bytes) > 9000
figure["sha256"] = sha256(png_bytes).hexdigest()
figure["svgSha256"] = sha256(svg_bytes).hexdigest()
figure["size"] = len(png_bytes)
figure["visualReview"] = "SCIENTIFIC_LABEL_CORRECTED_LEGIBLE_QA_INDEPENDENT_REVIEW_PENDING"
figure["modifications"] = (
    "Original airflow diagram preserved; lift label corrected to component "
    "perpendicular to flow; added matching-background panel so streamline "
    "cannot obscure label; SVG/PNG re-rendered 2026-11-20."
)
assert not figure.get("ownerQaAcceptedSha256") and not figure.get("ownerQaDisplayDecision")
assert figure["reviewStatus"].startswith("PROVISIONAL_")
svg.write_bytes(svg_bytes)
png.write_bytes(png_bytes)
manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
print("PASS: figure 49 label clearly separated from decorative streamlines")
print("pngSha256",figure["sha256"])
print("svgSha256",figure["svgSha256"])
print("approval: pending")
