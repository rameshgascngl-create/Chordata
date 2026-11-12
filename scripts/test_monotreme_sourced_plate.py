#!/usr/bin/env python3
"""Offline QA acceptance boundary for the exact sourced monotreme lesson plate.

This verifies bundled source attribution, a real replacement asset, preserved
original, species distinction and the three distinct published images. It does
not fabricate independent scientific approval or claim device visual review.
"""
from pathlib import Path
import hashlib
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
manifest = json.loads((ASSETS / "pencil_plates/manifest.json").read_text(encoding="utf-8"))["figures"]
provenance = json.loads((ROOT / "docs/qa-image-review/MONOTREME_REPRODUCTION_SOURCE_PLATE_20261112.json").read_text(encoding="utf-8"))
diagram_id = "u5-egg-laying-mammals-monotreme-reproduction"
rows = [r for r in manifest if r["diagramId"] == diagram_id]
assert len(rows) == 1, "Unique shared monotreme slot required"
p = rows[0]
assert p["lang"] == "shared" and p["path"] == "pencil_plates/platypus_reproduction.png"
asset = ASSETS / p["path"]
data = asset.read_bytes()
assert data[:8] == bytes.fromhex("89504e470d0a1a0a") and len(data) == p["size"]
assert hashlib.sha256(data).hexdigest() == p["sha256"] == provenance["installedPngSha256"]
assert provenance["installedPngSize"] == len(data)
dimensions = list(struct.unpack(">II",data[16:24]))
assert dimensions == provenance["sizePx"] == [3000,2100]
assert p["visualReview"] == "SOURCED_REAL_MONOTREME_SPECIMENS_AND_ANATOMY_QA_PROVISIONAL"
assert p["reviewStatus"].startswith("PROVISIONAL_")
assert "PROVISIONAL" in provenance["review"].upper()
assert provenance["sourceArtCreatedOrInvented"] is False
assert p["retiredSchematicPng"] == provenance["retiredOriginalPng"]
old = (ROOT / p["retiredSchematicPng"]).read_bytes()
assert hashlib.sha256(old).hexdigest() == p["retiredSchematicSha256"] == provenance["retiredOriginalSha256"]
assert p["retiredSchematicSha256"] == "5936652b851a5c474cf64db332a49736266039c6f6e8b9e6e507122de6ef0284"

sources = provenance["sourceFiles"]
assert [s["key"] for s in sources] == ["platypus", "puggle", "pouch"]
assert p["sourceUrls"] == [s["sourcePage"] for s in sources]
assert p["sourceSha256"] == [s["sha256"] for s in sources]
assert p["originalLicences"] == [s["licenseUrl"] for s in sources]
assert p["licenseUrl"] == "https://creativecommons.org/licenses/by-sa/4.0/"
assert [s["verifiedLicence"] for s in sources] == ["CC BY 2.0","CC BY-SA 4.0","Public domain"]
assert len({s["sourcePage"] for s in sources}) == 3
assert all(len(s["sha256"]) == 64 and s["originalBytes"] > 100000 for s in sources)
assert "Ian R McCann" in p["author"] and "Eric Chan" in p["author"] and "Beddard" in p["author"]
# The photograph is not a mother feeding young; the label must be accurate.
assert "sex unknown" in p["keyEn"]
assert "NOT a platypus young" in p["keyEn"]
assert "different species" in p["keyEn"] and "not a chronological" in p["keyEn"]
assert "lack teats" in p["keyEn"]
assert "இனங்களின்" in p["keyTa"]
assert p["sourceKind"] == "COMPARATIVE_MONOTREME_SPECIMEN_PHOTOS_AND_PUBLISHED_POUCH_ANATOMY"
assert p["pedagogicStatus"] == "REPLACED_WITH_CC_LICENSED_MONOTREME_SOURCE_QA_PENDING_2026-11-12"
print("PASS: genuine 3000x2100 monotreme visual, three original sources and archived rejected PNG")
print("PASS: species/hatching/feeding caveats preserved, no false scientific acceptance")
