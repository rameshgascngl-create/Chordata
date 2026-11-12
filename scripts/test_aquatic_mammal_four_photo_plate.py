#!/usr/bin/env python3
"""Fail closed if the real four-lineage marine mammal comparison regresses."""
from pathlib import Path
import hashlib,json,struct

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
FIGURE_ID="u5-aquatic-mammals-aquatic-mammal-groups"
manifest=json.loads((ASSETS/"pencil_plates/manifest.json").read_text(encoding="utf-8"))["figures"]
matches=[f for f in manifest if f["diagramId"]==FIGURE_ID]
assert len(matches)==1
e=matches[0]
provenance=json.loads((ROOT/"docs/qa-image-review/AQUATIC_MAMMAL_FOUR_PHOTOGRAPHS_20261112.json").read_text(encoding="utf-8"))
assert provenance["diagramId"]==FIGURE_ID
assert e["lang"]=="en" and e["path"]==provenance["asset"]=="pencil_plates/aquatic_mammal_lineages_en.png"
png=(ASSETS/e["path"]).read_bytes()
assert len(png)==e["size"]==provenance["sizeBytes"] and png[:8]==bytes.fromhex("89504e470d0a1a0a")
assert list(struct.unpack(">II",png[16:24]))==provenance["resolution"]==[3200,2320]
assert hashlib.sha256(png).hexdigest()==e["sha256"]==provenance["sha256"]
assert e["reviewStatus"].startswith("PROVISIONAL_")
assert e["visualReview"]=="SOURCED_FOUR_AQUATIC_MAMMAL_PHOTOGRAPHS_QA_PROVISIONAL"
assert provenance["sourceAnatomyFabricated"] is False
assert provenance["biologyStatus"]=="PROVISIONAL_INDEPENDENT_SIGNOFF_PENDING"

photos=provenance["sources"]
assert [p["key"] for p in photos]==["cetacea","sirenia","pinnipedia","mustelidae"]
assert [p["taxon"] for p in photos]==["Tursiops truncatus","Dugong dugon","Phoca vitulina","Enhydra lutris"]
assert [p["verifiedLicence"] for p in photos]==["CC BY 2.0","CC BY 4.0","CC BY-SA 4.0","Public domain"]
assert [p["licenceUrl"] for p in photos]==e["originalLicences"]
assert [p["sourcePage"] for p in photos]==e["sourceUrls"]
assert [p["sourceSha256"] for p in photos]==e["sourceSha256"]
assert len({p["sourcePage"] for p in photos})==4
assert all(len(p["sourceSha256"])==64 and p["sourceBytes"]>200000 for p in photos)
assert [p["creator"] for p in photos]==[
    "caroline legg","Jerome Paillet (IFREMER)","Arnstein Rønning","U.S. Fish and Wildlife Service"]
assert e["licenseUrl"]=="https://creativecommons.org/licenses/by-sa/4.0/"

original=(ROOT/e["retiredSchematicPng"]).read_bytes()
svg=(ROOT/e["retiredSchematicSvg"]).read_bytes()
assert hashlib.sha256(original).hexdigest()==e["retiredSchematicSha256"]==provenance["retiredSha256"]
assert hashlib.sha256(svg).hexdigest()==e["retiredSchematicSvgSha256"]==provenance["retiredSvgSha256"]
assert e["retiredSchematicSha256"]=="a330620a0fb6d62fab65caf6c79fd50ee24a686c83bc3a49b034623bfbc987c3"
assert e["pedagogicStatus"]=="REPLACED_WITH_CC_LICENSED_AQUATIC_MAMMAL_PHOTOS_QA_PENDING_2026-11-12"
assert "NOT one taxonomic order" in e["keyEn"]
assert all(term in e["keyEn"] for term in ("Cetacea","Sirenia","Pinnipedia","Mustelidae","Carnivora","Afrotheria"))
print("PASS: four actual marine mammal photos, original author/source/licence/hash, 3200x2320 installed PNG")
print("PASS: taxonomy correct; symbolic original and SVG retained; independent approval still pending")
