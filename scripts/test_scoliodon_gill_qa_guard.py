#!/usr/bin/env python3
"""Protect the accepted QA source of the shared Scoliodon-gill schematic.

This is a factual caption/rights/bitmap invariant test, not independent approval
of the artwork or authorisation to integrate an unverified AI-generated plate.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
DIAGRAM_ID = "u2-scoliodon-gills-labelled"
PNG_PATH = "pencil_plates/shark_gill_flow.png"
PNG_SHA = "675f497ab223df417274b8641bfc09b5a40729a4c74e419208bb08794353a90c"
PNG_BYTES = 442559
SVG_PATH = "docs/original_plate_svg/shark_septal_gills_en.svg"
SVG_SHA = "930f7d9eaa57ab381ea3b20f299c1169b9cb9bda646cd3bb50e2479986a9e2e6"
AUTHOR = "CHORDATA QA project — original vector shark septal-gill teaching schematic"
REVIEW = "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
EN_TERMS = (
    "Five external gill slits", "hyoid arch", "posterior hemibranch",
    "first four branchial arches", "four holobranchs", "fifth branchial arch",
    "abranchial", "interbranchial septa", "secondary lamellae",
    "countercurrent exchange", "spiracle", "ONE generalised gill pouch",
    "NOT accepted as specimen-specific histology",
)
TA_TERMS = (
    "செவுள் இடைத்தடுப்பு", "ஐந்து", "பாதிச்செவுள்", "முழுச்செவுள்",
    "ஹையாய்டு", "ஐந்தாவது செவுள்", "செவுள் இழைகள்", "செவுள் கதிர்கள்",
    "இரண்டாம் நிலைச் செவுள் தகடுகள்", "நீரோட்ட", "எதிர்திசை",
    "ஸ்பைரக்கிள்", "பால் சுறா", "மதிப்பீடுகள் நிலுவையில்",
)
EVIDENCE_URLS = (
    "https://journals.physiology.org/doi/10.1152/physrev.00050.2003",
    "https://researcharchive.calacademy.org/research/ichthyology/catalog/fishcatget.asp?spid=26425",
    "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=160219",
    "https://www.tandfonline.com/doi/full/10.1080/24750263.2025.2537751",
)


def verify(entry: dict, png: bytes, svg: bytes) -> None:
    assert (entry.get("diagramId"), entry.get("lang"), entry.get("path"),
            entry.get("topicId"), entry.get("page"), entry.get("sectionKey")) == (
                DIAGRAM_ID, "shared", PNG_PATH, "u2-scoliodon", 3, "respiratory-system"
            ), "gill lesson page/section/language changed"
    assert png[:8] == bytes.fromhex("89504e470d0a1a0a"), "registered figure not PNG"
    assert len(png) == PNG_BYTES and entry.get("size") == PNG_BYTES, "unexpected source size"
    assert sha256(png).hexdigest() == PNG_SHA and entry.get("sha256") == PNG_SHA, (
        "source PNG replaced or corrupted without independent review"
    )
    assert (entry.get("svgMaster"), entry.get("svgSha256")) == (
        SVG_PATH, SVG_SHA
    ) and sha256(svg).hexdigest() == SVG_SHA, "editable original master was changed"
    assert entry.get("author") == AUTHOR, "historic project author attribution changed"
    assert entry.get("license") == "Original project illustration — scientific review pending", (
        "project source/licence was misrepresented"
    )
    assert not entry.get("sourceUrl") and not entry.get("sourceKind") and not entry.get(
        "aiQaIntegrationDecision"
    ), "an unsourced AI or third-party plate was silently approved"
    assert entry.get("reviewStatus") == REVIEW and entry.get(
        "visualReview"
    ) == "REPLACED_VISUAL_QA_PENDING", "figure review was falsely promoted"
    assert "not an actual Scoliodon" in entry.get("scope", ""), (
        "conceptual illustration described as species-specific dissection"
    )
    assert tuple(entry.get("scientificEvidenceUrls", [])) == EVIDENCE_URLS, (
        "taxon and gill-structure evidence missing or changed"
    )
    assert len(entry.get("referenceUrls", [])) == 3, "original source references changed"
    for term in EN_TERMS:
        assert term in entry.get("keyEn", ""), "English teaching key omitted: " + term
    for term in TA_TERMS:
        assert term in entry.get("keyTa", ""), "Tamil teaching key omitted: " + term


def main() -> None:
    contents = json.loads((ASSETS / "pencil_plates/manifest.json").read_text(encoding="utf-8"))
    matches = [e for e in contents["figures"] if e.get("diagramId") == DIAGRAM_ID]
    assert len(matches) == 1, "missing or duplicate lesson figure"
    original = matches[0]
    png = (ASSETS / PNG_PATH).read_bytes()
    svg = (ROOT / SVG_PATH).read_bytes()
    verify(original, png, svg)
    tests = [
        ("different image", {"sha256": "0" * 64}),
        ("false approval", {"reviewStatus": "ACCEPTED"}),
        ("silent AI green tick", {"aiQaIntegrationDecision": "GREEN_TICK_ALLOW_PROVISIONAL_QA_USE"}),
        ("wrong page", {"page": 4}),
        ("false creator", {"author": "Historical shark atlas"}),
        ("species dissection claim", {"scope": "verified Scoliodon dissection"}),
        ("missing Tamil", {"keyTa": "சுறா செவுள்"}),
        ("missing gill organization", {"keyEn": original["keyEn"].replace("four holobranchs", "several gills")}),
        ("lost references", {"scientificEvidenceUrls": []}),
    ]
    for name, edit in tests:
        modified = deepcopy(original)
        modified.update(edit)
        try:
            verify(modified, png, svg)
        except AssertionError:
            continue
        raise AssertionError("mutation guard failed to reject: " + name)
    print("PASS Scoliodon gill exact original PNG/SVG and Unit II page 3 mapping")
    print("PASS hyoid hemibranch, first four holobranchs, fifth abranchial, absent external spiracle and bilingual keys")
    print("PASS 9 anti-tamper/false-approval negative cases")
    print("HOLD AI gill candidate separately; independent anatomy, Tamil and physical-device approvals pending")


if __name__ == "__main__":
    main()
