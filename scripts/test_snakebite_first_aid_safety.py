#!/usr/bin/env python3
"""Fail-closed safety and rights audit for India's provisional snakebite flowchart.

The PNG and its SVG master are NOT modified. This is a semantic-source test
and cannot substitute for medical review or real-world clinical protocols.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
ID = "u4-poison-apparatus-first-aid-flowchart"
PNG_PATH = "pencil_plates/snakebite_first_aid_en.png"
PNG_SHA = "1ace57d4694bace1b0da1e5f41b2693a99bb50429f7699f18e4a3377debf52a7"
PNG_SIZE = 115692
SVG_PATH = "docs/original_plate_svg/snakebite_first_aid_en.svg"
SVG_SHA = "ef08bed905d6616dd512011a212bbd3c1ef27c87605d53b482f20105fb4bbfa2"
EXPECTED_SOURCES = (
    "https://www.who.int/teams/control-of-neglected-tropical-diseases/snakebite-envenoming/treatment",
    "https://www.who.int/news-room/questions-and-answers/item/snakebite-envenoming",
    "https://www.ncdc.mohfw.gov.in/wp-content/uploads/2024/07/NATIONAL-ACTION-PLAN-FOR-PREVENTION-AND-CONTROL-OF-SNAKEBITE-ENVENOMING-NAPSE.pdf",
    "https://www.ifrc.org/sites/default/files/2026-03/IFRC%20International%20First%20Aid%2C%20Resuscitation%20and%20Education%20Guidelines%202025.pdf",
)
EN = (
    "medical emergency", "absent", "call emergency services",
    "Immobilise the bitten limb", "non-constricting splint",
    "monitor breathing", "recovery position", "Do NOT apply a tight tourniquet",
    "cut or suck", "use ice", "herbal remedies", "Pressure-immobilisation",
    "NOT universally appropriate", "India", "Hospital clinicians",
)
TA = (
    "அவசர மருத்துவ நிலை", "சிகிச்சை வசதியுள்ள மருத்துவமனை",
    "அசைவின்றியும்", "இறுக்கமில்லாத துணைக்கட்டையால்",
    "வீக்கத்திற்கு முன்னர்", "சுவாசத்தைக்", "பக்கவாட்டுப் படுக்கை",
    "இரத்தத்தடுப்புக் கட்டு", "விஷத்தை உறிஞ்சுதல்",
    "பனிக்கட்டி", "மூலிகை மருந்து", "அனைத்து பாம்புக்கடிகளுக்கும்",
    "எதிர்நஞ்சு மருந்து", "மருத்துவ வழிகாட்டுதலுக்கு மாற்றாகாது",
)

def validate(e: dict, png: bytes, svg: bytes) -> None:
    assert (e.get("diagramId"),e.get("lang"),e.get("path"),
            e.get("topicId"),e.get("page"),e.get("sectionKey")) == (
        ID,"en",PNG_PATH,"u4-poison-apparatus",3,"evidence-based-first-aid"
    ), "figure was moved to wrong reading section"
    assert png.startswith(bytes.fromhex("89504e470d0a1a0a"))
    assert len(png)==PNG_SIZE and e.get("size")==PNG_SIZE
    assert hashlib.sha256(png).hexdigest()==PNG_SHA and e.get("sha256")==PNG_SHA
    assert e.get("svgMaster")==SVG_PATH and e.get("svgSha256")==SVG_SHA
    assert hashlib.sha256(svg).hexdigest()==SVG_SHA
    assert e.get("author")=="CHORDATA QA — original vector anatomical schematic"
    assert e.get("license")=="Original project illustration; no source images copied"
    assert not e.get("sourceUrl") and not e.get("aiQaIntegrationDecision")
    assert e.get("reviewStatus")=="PROVISIONAL_QA_ANATOMICAL_REVIEW_PENDING"
    assert e.get("visualReview")=="SELF_INSPECTED_PROVISIONAL"
    assert tuple(e.get("scientificEvidenceUrls", []))==EXPECTED_SOURCES
    assert "No instructions to catch" in e.get("scope","")
    assert "Existing English PNG remains unchanged" in e.get("editorialCaution","")
    for t in EN:
        assert t in e.get("keyEn",""), "English safety instruction missing: "+t
    for t in TA:
        assert t in e.get("keyTa",""), "Tamil safety instruction missing: "+t
    assert "Pressure-immobilisation bandaging is NOT universally" in e["keyEn"]
    assert "அனைத்து பாம்புக்கடிகளுக்கும் பொதுவான முதலுதவி முறை அன்று" in e["keyTa"]

def main():
    m=json.loads((ASSETS/"pencil_plates/manifest.json").read_text(encoding="utf-8"))
    found=[e for e in m["figures"] if e.get("diagramId")==ID]
    assert len(found)==1, "duplicate or absent first-aid figure"
    e=found[0]
    png=(ASSETS/PNG_PATH).read_bytes()
    svg=(ROOT/SVG_PATH).read_bytes()
    validate(e,png,svg)
    changes=[
        ("mutated figure",{"sha256":"0"*64}),
        ("false scientific approval",{"reviewStatus":"APPROVED"}),
        ("false image AI approval",{"aiQaIntegrationDecision":"GREEN_TICK_ALLOW_PROVISIONAL_QA_USE"}),
        ("false WHO artwork credit",{"sourceUrl":EXPECTED_SOURCES[0]}),
        ("missing pressure-immobilisation exception",{"keyEn":e["keyEn"].replace("NOT universally appropriate","always appropriate")}),
        ("unsafe omission of no tourniquet",{"keyEn":e["keyEn"].replace("Do NOT apply a tight tourniquet","Apply a tight tourniquet")}),
        ("missing Tamil warning",{"keyTa":"முதலுதவி"}),
        ("wrong page",{"page":2}),
        ("removed WHO source",{"scientificEvidenceUrls":EXPECTED_SOURCES[1:]}),
    ]
    for name, change in changes:
        variant=copy.deepcopy(e)
        variant.update(change)
        try:
            validate(variant,png,svg)
        except AssertionError:
            pass
        else:
            raise AssertionError("Unsafe mutation was accepted: "+name)
    print("PASS unchanged first-aid PNG/SVG, original image credit and Unit IV page 3")
    print("PASS WHO/NCDC/IFRC evidence, bilingual immediate referral and no harmful interventions")
    print(f"PASS {len(changes)} mutation rejection tests")
    print("HOLD independent clinical/Tamil approval and physical device acceptance")

if __name__=="__main__":
    main()
