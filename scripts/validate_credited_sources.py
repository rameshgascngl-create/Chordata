#!/usr/bin/env python3
"""Verify the provenance research register without equating 'found' with 'embedded'."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/"docs/research/credited_image_sources.json").read_text(encoding="utf-8"))
assert data["status"] == "RESEARCH_ONLY_NOT_IN_APK"
records=data["sources"]
pack=json.loads((root/"app/src/main/assets/chordata_content.json").read_text(encoding="utf-8"))
required={d for unit in pack["units"] for topic in unit["topics"] for d in topic["diagramIds"]}
assert len(required)==64
assert len(records)>=12
assert len({x["id"] for x in records})==len(records)
assert len({x["sourcePageUrl"] for x in records})==len(records)
for r in records:
    assert r["embeddedInApk"] is False
    assert r["sourceStatus"] == "FOUND_NOT_DOWNLOADED"
    assert r["sourcePageUrl"].startswith("https://commons.wikimedia.org/wiki/File:")
    assert r["licenseUrl"].startswith("https://creativecommons.org/")
    assert all(r[f].strip() for f in ("creator","license","academicNotes","attributionTemplate"))
    if r["diagramId"] is not None: assert r["diagramId"] in required
    if r["suitability"]=="SUPPLEMENT_ONLY": assert r["diagramId"] is None
print(f"PASS {len(records)} credited Commons source records; none marked embedded or approved")
