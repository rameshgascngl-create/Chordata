#!/usr/bin/env python3
"""Targeted repair of one demonstrably erroneous Calotes arterial label.

Changes only the registered Calotes SVG master, its raster PNG, their manifest
SHA/size records, and reviewer sheet. No other figures may be rebuilt.
"""
from pathlib import Path
import hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "app/src/main/assets/pencil_plates"
SVG = ROOT / "docs/original_plate_svg/calotes_heart_arteries_en.svg"
PNG = DIR / "calotes_heart_arteries_en.png"
MANIFEST = DIR / "manifest.json"
OLD = "Intercaval flow"
NEW = "Intercavitary flow"
FIGURE_ID = "u4-calotes-arterial-system"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    import cairosvg
    master = SVG.read_text(encoding="utf-8")
    if master.count(OLD) == 1:
        master = master.replace(OLD, NEW)
        SVG.write_text(master, encoding="utf-8")
    elif master.count(NEW) != 1:
        raise ValueError("Unexpected Calotes master; no image modified")
    old_png_sha = digest(PNG.read_bytes())
    if old_png_sha != "12305ec4249359a17fd4c17f5445fa7ba7e73894d6feea5e701072dc467840ed":
        raise ValueError("Source PNG differs from verified baseline; abort")
    png = cairosvg.svg2png(bytestring=master.encode("utf-8"),
                           output_width=1800, output_height=1120)
    assert png[:8] == bytes.fromhex("89504e470d0a1a0a")
    PNG.write_bytes(png)
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    matches = [x for x in data["figures"]
               if x["diagramId"] == FIGURE_ID and x["lang"] == "en"]
    if len(matches) != 1 or matches[0]["path"] != "pencil_plates/calotes_heart_arteries_en.png":
        raise ValueError("Registered figure is not uniquely mapped")
    fig = matches[0]
    fig["sha256"] = digest(png)
    fig["size"] = len(png)
    fig["svgSha256"] = digest(master.encode("utf-8"))
    fig["modifications"] = (
        "Targeted academic label correction: the erroneous 'Intercaval flow' "
        "was changed to 'Intercavitary flow'. Original topology and all "
        "other figure pixels remain unchanged. Original SVG rendered to PNG."
    )
    fig["reviewStatus"] = "PROVISIONAL_QA_ANATOMICAL_REVIEW_PENDING"
    data["status"] = "PROVISIONAL_QA_NOT_ACADEMICALLY_APPROVED"
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts/write_figure_review_register.py")],
                   check=True, cwd=ROOT)
    print("Corrected figure:", FIGURE_ID)
    print("Old PNG SHA-256:", old_png_sha)
    print("New PNG SHA-256:", fig["sha256"])
    print("SVG SHA-256:", fig["svgSha256"])
    print("Figure review status:", fig["reviewStatus"])

if __name__ == "__main__":
    main()
