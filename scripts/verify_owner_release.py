#!/usr/bin/env python3
"""Owner-authorised release review of exact CHORDATA figure assets.

This is NOT an independent scientific or Tamil reviewer sign-off. The 64-row
independent-review register remains unmodified and its own release check remains
available. This separate release gate binds the owner's recorded authorisation
to specific image bytes, placement, creators, source URLs and rights statements.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
POLICY = ROOT / "docs/OWNER_FIGURE_APPROVED_ASSETS_20261121.json"
APPROVAL = ROOT / "docs/OWNER_ILLUSTRATION_AUTHORISATION_2026-11-21.md"
SHA_RE = re.compile(r"^[a-f0-9]{64}$")


def verify_manifest(figures, slots, approved, asset_root=ASSETS):
    assert approved.get("policy") == "CHORDATA_OWNER_APPROVAL_V1", "Unknown owner-review policy"
    assert len(figures) == 68 and len(slots) == 64, "Unexpected image or slot count"
    assert len({s["id"] for s in slots}) == 64, "Duplicate/blank registered figure slot"
    lock_slots = [
        {"diagramId": s["id"], "topicId": s["topicId"],
         "page": s["page"], "sectionKey": s["sectionKey"]}
        for s in slots
    ]
    assert lock_slots == approved["slots"], "Lesson slot placement differs from owner-approved snapshot"
    assert len(approved["figures"]) == 68, "Owner snapshot must include all 68 variants"
    locked = {(x["diagramId"], x["lang"]): x for x in approved["figures"]}
    assert len(locked) == 68, "Duplicate figure/lang in owner snapshot"
    assert len({(x["diagramId"], x["lang"]) for x in figures}) == 68, "Duplicate figure/lang in manifest"
    seen = set()
    for figure in figures:
        key = (figure["diagramId"], figure["lang"])
        assert key in locked, "Artwork not included in owner-approved snapshot: " + str(key)
        assert figure["diagramId"] in {s["id"] for s in slots}, "Orphan artwork: " + str(key)
        assert figure["lang"] in ("en", "ta", "shared"), "Unrecognised language: " + str(key)
        assert not figure.get("scientificRiskHold"), "Held figure cannot ship: " + str(key)
        assert not figure.get("userRejected") and not figure.get("rejected"), "Rejected figure: " + str(key)
        assert not (str(figure.get("reviewStatus","")).startswith("REJECTED")), "Rejected status: " + str(key)
        expected = locked[key]
        fields = ("diagramId", "lang", "path", "sha256", "author", "license", "sourceUrl", "modifications")
        actual = {name: figure.get(name) or "" for name in fields}
        assert actual == expected, "Owner approval invalidated by asset/credit/licence change: " + str(key)
        assert SHA_RE.fullmatch(figure["sha256"]), "Invalid SHA-256: " + str(key)
        assert figure["author"].strip() and figure["license"].strip(), "Missing author/rights declaration: " + str(key)
        license_text = figure["license"].lower()
        if ("cc by" in license_text or "public domain" in license_text or "cc0" in license_text):
            assert figure.get("sourceUrl") or figure.get("referenceUrl") or figure.get("referenceUrls"), (
                "External rights claim lacks a source link: " + str(key))
        if "cc by" in license_text:
            assert figure.get("modifications", "").strip(), "CC derivative modification statement missing: " + str(key)
        relpath = Path(figure["path"])
        assert not relpath.is_absolute() and ".." not in relpath.parts, "Unsafe asset path: " + str(key)
        p = asset_root / relpath
        assert p.is_file(), "Missing image bytes: " + str(p)
        assert p.suffix.lower() == ".png", "Unexpected non-PNG lesson image"
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        assert sha == figure["sha256"], "Image bytes differ from recorded SHA: " + str(key)
        seen.add(key)
    assert seen == set(locked), "Owner snapshot contains unused or missing variants"
    coverage = {f["diagramId"] for f in figures if f["lang"] in ("en", "shared")}
    assert coverage == {s["id"] for s in slots}, "64/64 canonical English/shared slots not covered"


def main():
    owner = APPROVAL.read_text(encoding="utf-8")
    assert "I reviewed and approved the illustrations myself as project owner" in owner, (
        "Missing documented owner review")
    assert "alternative release policy" in owner, "Owner has not authorised release-policy change"
    approved = json.loads(POLICY.read_text(encoding="utf-8"))
    assert approved["approval_document"] == "docs/OWNER_ILLUSTRATION_AUTHORISATION_2026-11-21.md"
    figures = json.loads((ASSETS / "pencil_plates/manifest.json").read_text(encoding="utf-8"))["figures"]
    slots = json.loads((ASSETS / "figure_slots.json").read_text(encoding="utf-8"))["slots"]
    verify_manifest(figures, slots, approved)
    print("PASS: owner-authorised figure release: 64 lesson slots, 68 exact image variants")
    print("PASS: recorded image SHA-256, source credits, rights statements, placement and no held/rejected figures")
    print("NOTE: declared source licences still require external permission compliance; this is NOT independent review certification")


if __name__ == "__main__":
    main()
