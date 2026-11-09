#!/usr/bin/env python3
"""Guard the provisional Calotes arterial teaching key and original image provenance.

Species-level arterial anatomy comes from de Silva 1956, not from the
unapproved graphic; the reviewed AI image is deliberately NOT installed.
This is an editorial and negative-test gate, NOT a scientific approval.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
ID = "u4-calotes-arterial-system"
PATH = "pencil_plates/calotes_heart_arteries_en.png"
IMAGE_SHA = "12305ec4249359a17fd4c17f5445fa7ba7e73894d6feea5e701072dc467840ed"
IMAGE_SIZE = 137849
SVG_PATH = "docs/original_plate_svg/calotes_heart_arteries_en.svg"
SVG_SHA = "c70d16457a5329a5c26388f491e20c9eab5fddb1a5b8121a9bb1356b8b658c7b"
SPECIES_SOURCE = "https://eurekamag.com/research/023/819/023819374.php"
KEY_EN_TERMS = (
    "NOT a species-validated",
    "cavum arteriosum", "cavum venosum", "cavum pulmonale",
    "paired systemic arches", "dorsal aorta", "near the ventricular apex",
    "RIGHT systemico-carotid", "vertebral", "subclavian",
    "ductus caroticus", "NOT the left and right carotid arteries",
    "Intercaval flow", "venae cavae", "intercavitary",
)
KEY_TA_TERMS = (
    "ஓணான்", "முன்அறைகளும்", "கீழறை", "காவம் ஆர்டீரியோசம்",
    "காவம் வீனோசம்", "காவம் பல்மோனாலே",
    "பெருந்தமனி", "முதுகுப்புறப்", "வலதுபுற", "தோளடித் தமனிகளும்",
    "கரோட்டிட்", "பக்க இணைப்பு", "Intercaval flow",
    "மகாசிரைகளுக்கிடையேயான", "அறிவியல்", "மதிப்பீடு",
)


def require(condition: bool, description: str) -> None:
    if not condition:
        raise AssertionError(description)


def check_figure(entry: dict, png: bytes, svg: bytes) -> None:
    require((entry.get("diagramId"), entry.get("lang"),
             entry.get("path"), entry.get("topicId"),
             entry.get("page"), entry.get("sectionKey")) ==
            (ID, "en", PATH, "u4-calotes", 4, "arterial-system"),
            "wrong or duplicated Calotes arterial lesson binding")
    require(entry.get("sha256") == IMAGE_SHA
            and entry.get("size") == IMAGE_SIZE
            and len(png) == IMAGE_SIZE
            and hashlib.sha256(png).hexdigest() == IMAGE_SHA,
            "Calotes PNG changed: a different drawing needs explicit review")
    require(entry.get("svgMaster") == SVG_PATH
            and entry.get("svgSha256") == SVG_SHA
            and hashlib.sha256(svg).hexdigest() == SVG_SHA,
            "historic editable Calotes master changed")
    require(entry.get("author") == "CHORDATA QA — original vector anatomical schematic"
            and entry.get("license") == "Original project illustration; no source images copied"
            and entry.get("sourceUrl", "") == ""
            and not entry.get("sourceKind")
            and not entry.get("aiQaIntegrationDecision"),
            "unverified replacement was falsely credited or green-ticked")
    require(entry.get("visualReview") == "SCIENTIFIC_TOPOLOGY_REVISED_PROVISIONAL"
            and entry.get("reviewStatus") == "PROVISIONAL_QA_ANATOMICAL_REVIEW_PENDING",
            "false academic or artwork approval")
    require(SPECIES_SOURCE in entry.get("referenceUrls", []),
            "de Silva 1956 original anatomical evidence link was removed")
    require("Intercaval flow" in entry.get("editorialCaution", "")
            and "No graphics changed" in entry.get("editorialCaution", ""),
            "misleading retained source label not disclosed")
    require("NOT an independently verified" in entry.get("scope", ""),
            "scope improperly claims species-specific authenticity")
    for term in KEY_EN_TERMS:
        require(term in entry.get("keyEn", ""), "English Calotes key missing: " + term)
    for term in KEY_TA_TERMS:
        require(term in entry.get("keyTa", ""), "Tamil Calotes key missing: " + term)


def main() -> None:
    manifest = json.loads((ASSETS / "pencil_plates/manifest.json").read_text(encoding="utf-8"))
    matches = [e for e in manifest["figures"] if e.get("diagramId") == ID]
    require(len(matches) == 1, "duplicate or absent Calotes arterial plate")
    original = matches[0]
    png = (ASSETS / PATH).read_bytes()
    svg = (ROOT / SVG_PATH).read_bytes()
    check_figure(original, png, svg)
    changes = [
        ("wrong PNG SHA", {"sha256": "0" * 64}),
        ("false academic acceptance", {"reviewStatus": "ACADEMICALLY_APPROVED"}),
        ("AI green tick", {"aiQaIntegrationDecision": "GREEN_TICK_ALLOW_PROVISIONAL_QA_USE"}),
        ("false external image rights", {"sourceUrl": SPECIES_SOURCE}),
        ("wrong lesson", {"sectionKey": "digestive-system"}),
        ("unsupported left-right symmetry", {"keyEn": original["keyEn"].replace("RIGHT systemico-carotid", "either systemic")}),
        ("undisclosed Intercaval flow", {"editorialCaution": "none"}),
        ("missing Tamil anatomy", {"keyTa": "ஓணான் இரத்தச் சுழற்சி"}),
    ]
    for label, fields in changes:
        altered = copy.deepcopy(original)
        altered.update(fields)
        try:
            check_figure(altered, png, svg)
        except AssertionError:
            continue
        raise AssertionError("negative assertion failed: " + label)
    print("PASS Calotes unchanged PNG/SVG, original credit and exact chapter section")
    print("PASS de Silva 1956 species-specific outflow/branching qualifications and bilingual key")
    print(f"PASS {len(changes)} rejection cases for false image rights/approval/anatomical claims")
    print("HOLD new arterial illustration pending expert review; no production merge")


if __name__ == "__main__":
    main()
