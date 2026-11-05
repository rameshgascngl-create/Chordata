#!/usr/bin/env python3
"""Audit every Chordata diagram slot against its lesson page and actual offline PNG.
QA allows explicitly missing figures; --require-complete rejects any missing or unreviewed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
def load(file):
    return json.loads((ASSETS / file).read_text(encoding="utf-8"))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check-png",action="store_true",help="Require and inspect every declared PNG asset")
    p.add_argument("--require-complete",action="store_true",help="Production gate: all 64, individually approved")
    p.add_argument("--out",help="Optional audit report file")
    args=p.parse_args()
    pack, placements, provided=load("chordata_content.json"),load("figure_placements.json"),load("figures.json")
    topics={t["id"]:t for unit in pack["units"] for t in unit["topics"]}
    expected=[(t["id"],d) for t in topics.values() for d in t["diagramIds"]]
    assert len(topics)==39, "Expected 39 topics"
    assert len(expected)==64 and len(set(expected))==64, "Expected 64 unique diagram slots"
    assert len(placements)==64, "Missing lesson-page assignments"
    assert len({x["diagramId"] for x in placements})==64, "Duplicate assignment"
    assert set(expected)=={(x["topicId"],x["diagramId"]) for x in placements}, "Missing or foreign diagram IDs"
    mapping={x["diagramId"]:x for x in placements}
    for x in placements:
        section=topics[x["topicId"]]["sections"][x["page"]-1]
        assert x["page"]>=1 and section["key"]==x["sectionKey"], "Wrong lesson page "+x["diagramId"]
        assert x["titleEn"].strip() and x["titleTa"].strip(), "Untranslated figure placement"
    assert len({x["id"] for x in provided})==len(provided), "Duplicate provided asset ID"
    assert len({x["diagramId"] for x in provided})==len(provided), "Duplicate diagram asset mapping"
    assert len({x["file"] for x in provided})==len(provided), "Duplicate PNG filename"
    assert all(x["file"].endswith(".png") and x["file"]==Path(x["file"]).name for x in provided), "Unsafe filename"
    hash_file=ASSETS/"figures"/"source-hashes.json"
    hashes=json.loads(hash_file.read_text(encoding="utf-8")) if hash_file.exists() else []
    hashes_by_id={x["id"]:x for x in hashes}
    for x in provided:
        assert x["diagramId"] in mapping, "Unregistered art: "+x["id"]
        expected_slot=mapping[x["diagramId"]]
        assert x["topicId"]==expected_slot["topicId"] and x["page"]==expected_slot["page"], "Wrong chapter/page: "+x["id"]
        assert all(x.get(f,"").strip() for f in ("captionEn","captionTa","license","author")), "Missing caption/credit: "+x["id"]
        if args.check_png:
            file=ASSETS/"figures"/x["file"]
            assert file.is_file(), "Image missing: "+x["file"]
            data=file.read_bytes()
            assert data[:8]==bytes.fromhex("89504e470d0a1a0a") and data[12:16]==b"IHDR", "Invalid PNG: "+x["file"]
            width,height=struct.unpack(">II",data[16:24])
            assert width>=800 and height>=600 and len(data)>10000, "Insufficient raster: "+x["file"]
            assert x["id"] in hashes_by_id, "No hash evidence: "+x["id"]
            h=hashes_by_id[x["id"]]
            assert h["file"]==x["file"] and h["size"]==len(data) and h["sha256"]==hashlib.sha256(data).hexdigest(), "Hash mismatch: "+x["file"]
    missing=[dict(x) for x in placements if x["diagramId"] not in {v["diagramId"] for v in provided}]
    unit_counts={u["id"]:{
        "required":sum(len(t["diagramIds"]) for t in u["topics"]),
        "present":sum(v["topicId"] in {t["id"] for t in u["topics"]} for v in provided),
    } for u in pack["units"]}
    report={"expected":len(expected),"provided":len(provided),"missing":len(missing),
            "figures_status":"PROVISIONAL_QA_NOT_ACADEMICALLY_APPROVED",
            "unitCounts":unit_counts,"missingFigures":missing,
            "placements":[dict(x,asset=next((v["file"] for v in provided if v["diagramId"]==x["diagramId"]),None)) for x in placements]}
    if args.out:
        target=Path(args.out);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"PASS: 64/64 diagram IDs have exactly one lesson-page mapping; {len(provided)} provisionally illustrated; {len(missing)} missing")
    for unit,counts in unit_counts.items():
        print(unit,counts)
    if args.require_complete:
        assert not missing, f"RELEASE BLOCKED: {len(missing)} figures missing"
        assert all(x.get("reviewStatus")=="ACCEPTED" for x in provided), "RELEASE BLOCKED: academic sign-off missing"
if __name__=="__main__":
    try: main()
    except (AssertionError, KeyError, IndexError, ValueError) as e:
        print("FAIL:",str(e),file=sys.stderr)
        sys.exit(1)
