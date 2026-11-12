#!/usr/bin/env python3
"""Stage three reviewed, Commons-licensed, genuine-teaching PNGs in exact lesson slots.

This is provisional QA usage, not independent academic acceptance. Preserve
each superseded symbolic PNG outside Android assets, with original SVG and
SHA-256; do not touch unrelated images or the immutable curriculum.
"""
from pathlib import Path
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
CAND=ROOT/"build/commons-figure-candidates"
ARCHIVE=ROOT/"docs/retired_noninstructional_png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
PROVENANCE=ROOT/"docs/CHORDATA_LICENSED_SOURCE_PROVENANCE_20261112.json"
PENDING="USER_REJECTED_REPLACEMENT_REQUIRED"
VERIFIED="SOURCED_TEACHING_FIGURE_QA_PROVISIONAL"
STATUS="REPLACED_WITH_CC_LICENSED_SOURCE_QA_PENDING_2026-11-12"
specs={
    "u4-snakes-india-big-four-identification":{
        "key":"snake","file":"india_big_four_scientific_candidate.png",
        "sources":("cobra","krait","russell","saw"),
        "keyEn":"Four medically important venomous snakes in India: Indian cobra (Naja naja), common krait (Bungarus caeruleus), Russell's viper (Daboia russelii) and saw-scaled viper (Echis carinatus). Photographs are for academic comparison ONLY, not field identification or snakebite decisions.",
        "modifications":"Four original Commons specimen photographs resized and arranged into a new annotated comparison plate, with distinct creator attributions. No anatomy fabricated.",
    },
    "u5-flight-adaptations-flight-muscles":{
        "key":"wing","file":"avian_flight_muscle_source_candidate.png",
        "sources":("wing",),
        "keyEn":"Source-labelled avian flight musculature and shoulder skeleton: pectoralis and supracoracoideus, coracoid, humerus, furcula and keeled sternum. Anatomical comparison; inspect the source labels before teaching.",
        "modifications":"Unmodified Wikimedia Commons source anatomy rasterised from original SVG at 2500 px width with white background for label legibility.",
    },
    "u5-marsupials-marsupial-life-history":{
        "key":"marsupial","file":"marsupial_pouch_photographic_candidate.png",
        "sources":("marsupial",),
        "keyEn":"Genuine photograph of a kangaroo with joey inside the pouch. A representative pouch-bearing marsupial, NOT a complete life-cycle or evidence that every marsupial has a pouch.",
        "modifications":"Photograph proportionally scaled on a new educational plate, with text captions and biological caveat.",
    },
}
def digest(b):return hashlib.sha256(b).hexdigest()
manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
provenance=json.loads((CAND/"provenance.json").read_text(encoding="utf-8"))
source_by_key={s["key"]:s for s in provenance["sources"]}
assert {s for info in specs.values() for s in info["sources"]} <= set(source_by_key)
assert provenance["status"]=="CANDIDATE_REQUIRES_SCIENTIFIC_VISUAL_AND_LICENCE_REVIEW"
for diagram_id,spec in specs.items():
    found=[e for e in manifest["figures"] if e["diagramId"]==diagram_id]
    assert len(found)==1,(diagram_id,"Wrong number of variants")
    e=found[0]
    assert e["visualReview"]==PENDING,(diagram_id,"Not a rejected drawing")
    assert e["reviewStatus"].startswith("PROVISIONAL_")
    assert e["pedagogicStatus"]=="WITHHELD_BIOLOGICALLY_NON_INSTRUCTIVE_2026-11-12"
    old_path=ASSETS/e["path"]
    assert old_path.is_file()
    original=old_path.read_bytes()
    assert digest(original)==e["sha256"],"Original source modified"
    assert e.get("svgMaster") and e.get("svgSha256"),"Missing original master provenance"
    orig_svg_path=ROOT/e["svgMaster"]
    assert orig_svg_path.is_file() and digest(orig_svg_path.read_bytes())==e["svgSha256"]
    new_path=CAND/spec["file"]
    assert new_path.is_file()
    new_png=new_path.read_bytes()
    rec=provenance["outputs"][spec["key"]]
    assert rec["sha256"]==digest(new_png)
    assert new_png[:8]==bytes.fromhex("89504e470d0a1a0a")
    with Image.open(new_path) as photo:
        photo.verify()
    with Image.open(new_path) as photo:
        assert photo.width>=2300 and photo.height>=1200,(diagram_id,photo.size)
    originals=[source_by_key[k] for k in spec["sources"]]
    assert all(s["verifiedLicence"]==s["license"] and
               s["license"].startswith("CC BY-SA") and
               len(s["originalSHA256"])==64 and
               s["sourcePage"].startswith("https://commons.wikimedia.org/wiki/File:")
               for s in originals)
    if diagram_id=="u4-snakes-india-big-four-identification":
        assert all(s["licenseUrl"].endswith("by-sa/4.0/") for s in originals)
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    legacy=ARCHIVE/old_path.name
    if legacy.exists():
        assert digest(legacy.read_bytes())==e["sha256"],"Archive collision"
    else:
        legacy.write_bytes(original)
    e["retiredSchematicPng"]="docs/retired_noninstructional_png/"+old_path.name
    e["retiredSchematicSha256"]=e["sha256"]
    e["retiredSchematicSvg"]=e.pop("svgMaster")
    e["retiredSchematicSvgSha256"]=e.pop("svgSha256")
    old_path.write_bytes(new_png)
    e["sha256"]=digest(new_png)
    e["size"]=len(new_png)
    e["visualReview"]=VERIFIED
    e["pedagogicStatus"]=STATUS
    e["pedagogicReason"]="Provisional user-facing teaching replacement using real photographs/published original anatomy; independent scientific editorial approval pending."
    e["sourceUrl"]=originals[0]["sourcePage"]
    e["sourceUrls"]=[s["sourcePage"] for s in originals]
    e["sourceSha256"]=[s["originalSHA256"] for s in originals]
    e["originalLicences"]=[s["licenseUrl"] for s in originals]
    e["licenseUrl"]=originals[0]["licenseUrl"]
    e["license"]="; ".join(sorted(set(s["license"] for s in originals)))+" — derivative layout credited to all source creators"
    e["author"]="; ".join(s["author"] for s in originals)+"; CHORDATA QA (educational presentation)"
    e["modifications"]=spec["modifications"]
    e["keyEn"]=spec["keyEn"]
    e["scope"]="Original source/specimen comparison for the exact registered lesson section; QA scientific review pending."
    print("REPLACED",diagram_id,"sha",e["sha256"],"bytes",e["size"],flush=True)
MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
provenance["status"]="INTEGRATED_PROVISIONAL_QA_NOT_INDEPENDENTLY_CERTIFIED"
provenance["integration"]={diagram:{"registeredAssetPath":next(e["path"] for e in manifest["figures"] if e["diagramId"]==diagram),
    "registeredSha256":next(e["sha256"] for e in manifest["figures"] if e["diagramId"]==diagram)}
    for diagram in specs}
PROVENANCE.write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
subprocess.run([sys.executable,"scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
for cmd in (
    [sys.executable,"scripts/audit_pencil_coverage.py"],
    [sys.executable,"scripts/audit_figure_placement.py"],
    [sys.executable,"scripts/write_figure_review_register.py","--check"],
    [sys.executable,"scripts/audit_android_qa_contract.py"],
):
    subprocess.run(cmd,check=True,cwd=ROOT)
print("PASS: all 3 source-credited PNGs staged, 3 figure holds retained, review status provisional")
