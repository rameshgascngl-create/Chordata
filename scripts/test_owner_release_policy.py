#!/usr/bin/env python3
"""Regression tests: owner release authorisation cannot silently cover changed art."""
import copy
import json
from pathlib import Path
from verify_owner_release import verify_manifest, ROOT, ASSETS

def must_reject(label, figures, slots, approval):
    try:
        verify_manifest(figures, slots, approval)
    except (AssertionError, KeyError, ValueError):
        return
    raise AssertionError("Owner release gate accepted " + label)

def main():
    figures = json.loads((ASSETS/"pencil_plates/manifest.json").read_text(encoding="utf-8"))["figures"]
    slots = json.loads((ASSETS/"figure_slots.json").read_text(encoding="utf-8"))["slots"]
    approved = json.loads((ROOT/"docs/OWNER_FIGURE_APPROVED_ASSETS_20261121.json").read_text(encoding="utf-8"))
    verify_manifest(figures, slots, approved)
    tampered = copy.deepcopy(figures)
    tampered[0]["sha256"] = "0"*64
    must_reject("changed image SHA", tampered, slots, approved)
    tampered = copy.deepcopy(figures)
    tampered[0]["license"] = ""
    must_reject("missing rights", tampered, slots, approved)
    tampered = copy.deepcopy(figures)
    tampered[0]["author"] = "Rewritten credit"
    must_reject("changed creator credit", tampered, slots, approved)
    tampered = copy.deepcopy(figures)
    tampered[0]["scientificRiskHold"] = "MATERIAL_ANATOMY_ERROR"
    must_reject("held image", tampered, slots, approved)
    tampered = copy.deepcopy(figures)
    tampered[0]["sourceUrl"] = "https://invalid.example/replaced"
    must_reject("source change", tampered, slots, approved)
    tampered_slots = copy.deepcopy(slots)
    tampered_slots[0]["page"] = 999
    must_reject("lesson placement change", figures, tampered_slots, approved)
    tampered = copy.deepcopy(figures)
    tampered.pop()
    must_reject("removed language variant", tampered, slots, approved)
    print("PASS: owner release gate rejects changed sha, rights, credit, held plate, source, placement, removed variant")
if __name__ == "__main__":
    main()
