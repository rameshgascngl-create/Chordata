#!/usr/bin/env python3
"""Fail-closed native QA checks for the provisional Scoliodon digestive plate.

The pending image is a schematic. Editorial anatomy corrections do not
authorise replacing the installed PNG or marking artwork academically approved.
This test exercises negative cases to prevent a silent provenance/status drift.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
ID = "u2-scoliodon-digestive-labelled"
PATH = "pencil_plates/scoliodon_digestive_en.png"
SOURCE_SHA256 = "57f1bd87ee5ea529eff8bec7ca5ac4a60c2dca1be6afb62daf52ba024741cf17"
SOURCE_BYTES = 581960
SVG_PATH = "docs/original_plate_svg/scoliodon_digestive_anatomy_en.svg"
SVG_SHA256 = "4730126353f7c18a67cdf45f22ebee5e3669ae0745296d35c98db4735fbcd8bf"

REQUIRED_EN = (
    "cardiac stomach", "pyloric stomach", "blind sac", "pyloric valve",
    "bursa entiana", "gallbladder", "bile duct", "pancreas", "proximal intestine",
    "spiral valve", "longitudinally rolled", "rectal gland", "salt",
    "cloaca", "NOT a species-validated", "NOT a digestive enzyme gland",
)
REQUIRED_TA = (
    "கார்டியாக்", "பைலோரிக்", "குருட்டுப்பை", "பர்சா என்டியானா",
    "பித்தப்பை", "பித்தநாளம்", "கணைய", "சுருள் வால்வு",
    "மலக்குடல்", "குளோயக்கா", "உப்பு", "செரிமானச் சுரப்பி அன்று",
    "அறிவியல் மதிப்பீடு",
)


def reject(message: str) -> None:
    raise ValueError(message)


def validate(entry: dict, *, image: bytes, master: bytes) -> None:
    if (entry.get("diagramId"), entry.get("lang"), entry.get("path")) != (ID, "en", PATH):
        reject("incorrect exact Scoliodon diagram or page-asset binding")
    if (entry.get("topicId"), entry.get("page"), entry.get("sectionKey")) != (
        "u2-scoliodon", 2, "digestive-system"
    ):
        reject("digestive figure placed on wrong textbook section")
    if entry.get("sha256") != SOURCE_SHA256 or len(image) != SOURCE_BYTES:
        reject("provisional installed PNG changed without anatomical review")
    if entry.get("size") != SOURCE_BYTES or hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        reject("PNG file size/content differs from registered accepted baseline")
    if (entry.get("svgMaster"), entry.get("svgSha256")) != (SVG_PATH, SVG_SHA256):
        reject("original editable artwork SHA/master removed or modified")
    if hashlib.sha256(master).hexdigest() != SVG_SHA256:
        reject("master artwork source hash changed")
    if entry.get("author") != (
        "CHORDATA QA — original, reference-guided Scoliodon-type digestive anatomy plate"
    ):
        reject("unapproved replacement or altered original author attribution")
    if entry.get("sourceUrl") or entry.get("aiQaIntegrationDecision"):
        reject("unverified AI/copyright candidate reported as sourced or accepted")
    if entry.get("reviewStatus") != "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING":
        reject("false independent scientific/Tamil signoff")
    if entry.get("visualReview") != "REPLACED_VISUAL_QA_PENDING":
        reject("provisional visual review incorrectly promoted")
    key_en = entry.get("keyEn", "")
    key_ta = entry.get("keyTa", "")
    for expected in REQUIRED_EN:
        if expected not in key_en:
            reject("English anatomy key missing: " + expected)
    for expected in REQUIRED_TA:
        if expected not in key_ta:
            reject("Tamil anatomy key missing: " + expected)
    if not (key_en.startswith("Schematic") and
            "species-level confirmation" not in key_en and
            "species-validated" in key_en and
            "NOT a validated dissection" in entry.get("scope", "")):
        reject("inaccurate species-specific dissection claim")
    if "copyright" in entry.get("license", "").lower() and not entry.get("license"):
        reject("missing project artwork origin")
    if len(entry.get("referenceUrls", [])) < 3:
        reject("original anatomical research references missing")


def main() -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))["figures"]
    found = [x for x in entries if x["diagramId"] == ID]
    if len(found) != 1:
        reject("missing/duplicate Scoliodon digestive slot")
    figure = found[0]
    png = (ASSETS / PATH).read_bytes()
    svg = (ROOT / SVG_PATH).read_bytes()
    validate(figure, image=png, master=svg)
    # Mutation tests: audit must refuse all these incorrect promotions/edits.
    attacks = [
        ("artwork SHA mutation", {"sha256": "0" * 64}),
        ("false academic approval", {"reviewStatus": "ACADEMICALLY_APPROVED"}),
        ("AI green tick", {"aiQaIntegrationDecision": "GREEN_TICK_ALLOW_PROVISIONAL_QA_USE"}),
        ("wrong lesson", {"page": 3}),
        ("false original credit", {"author": "AI-generated original"}),
        ("lost Bengali/Tamil organ key", {"keyTa": "சுறா செரிமான மண்டலம்"}),
        ("lost bursa label", {"keyEn": figure["keyEn"].replace("bursa entiana", "small pouch")}),
    ]
    for name, edit in attacks:
        tampered = copy.deepcopy(figure)
        tampered.update(edit)
        try:
            validate(tampered, image=png, master=svg)
        except ValueError:
            pass
        else:
            reject("negative test failed: " + name)
    print("PASS exact source PNG/SVG retained and registered to Unit II page 2")
    print("PASS corrected bilingual anatomy keys including scroll, bursa, ducts and rectal gland")
    print(f"PASS {len(attacks)} fail-closed tampering tests")
    print("HOLD replacement AI images and independent Biology/Tamil/device signoff")


if __name__ == "__main__":
    main()
