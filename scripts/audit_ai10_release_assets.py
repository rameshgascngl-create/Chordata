#!/usr/bin/env python3
"""Reject a Play bundle that silently reverts any of the ten owner-selected AI PNGs.

These exact SHA-256 values identify the owner-requested images integrated in
CHORDATA_AI10_Source_Integration_Patch_20261112.zip. This is a binary identity
gate, NOT certification of anatomical correctness or rights to outside sources.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
REQUIRED = {
    'u2-migration-migration-cycle': ('pencil_plates/fish_migration_cycles.png', 'f9133cf0914059e12e37af0ff3170592b7ae1a42a08875ce4a2dac4782ae7261'),
    'u5-flying-mammals-bat-wing-glider-comparison': ('pencil_plates/bat_glider_comparison_en.png', 'a28bc2f6ea0854067f9e8ab13adc9ccd0a38e34d7cecb9c38a29a6be64d11593'),
    'u2-pisces-classification-fish-groups': ('pencil_plates/fish_major_groups_en.png', '54617d2619e40baac973441d064c123a6b63ceb9d39ff7a743dd70ecb42bfef5'),
    'u2-accessory-respiration-accessory-organs-comparison': ('pencil_plates/fish_accessory_breathing_en.png', '30c841301b6042eebaf128db033fcaf2542c99cd1b4129609721320a641fa274'),
    'u2-parental-care-parental-care-comparison': ('pencil_plates/fish_parental_care_en.png', '8bbd87a865d337f64e537ea25f8010aea6688abd2424730afb31ef75a686137b'),
    'u3-parental-care-parental-care-comparison': ('pencil_plates/amphibian_parental_care_en.png', 'dac94c5386b213c8dc104c8d85cd62c72cbbb994c92bf9ae531e23465dfc67d9'),
    'u4-calotes-digestive-system': ('pencil_plates/calotes_digestive_en.png', '5da6f592cd726621ff5df240ebb506d9dc7142d95c03e6bfc99d89eede55834b'),
    'u4-calotes-respiratory-system': ('pencil_plates/calotes_respiratory_en.png', '5f63ba851ba074880db5ddecf044c24490173327903b9435e793f63f874eeae4'),
    'u4-origin-extinct-extinct-groups': ('pencil_plates/extinct_reptile_lineages_en.png', 'c36f69163bd291ee663f54c1575e6de3dd52caa80d6990cdb5bd81b02a367f18'),
    'u5-columba-urinogenital': ('pencil_plates/pigeon_urinogenital_en.png', 'f0678127364b73f72dff3a857aa61a0fae56715003c1805d86606ad679630404'),
}
manifest = json.loads((ASSETS / "pencil_plates/manifest.json").read_text(encoding="utf-8"))
figures = manifest["figures"]
for figure_id, (path, expected_sha) in REQUIRED.items():
    matches = [x for x in figures if x.get("diagramId") == figure_id and x.get("lang") in ("en", "shared")]
    assert len(matches) == 1, f"Missing or ambiguous figure ID: {figure_id}"
    entry = matches[0]
    assert entry.get("path") == path, f"Wrong image path: {figure_id}"
    assert entry.get("sha256") == expected_sha, f"AI10 manifest mismatch: {figure_id}"
    assert entry.get("author", "").startswith("OpenAI ImageGen"), f"AI10 provenance absent: {figure_id}"
    assert entry.get("ownerQaAcceptance") == "OWNER_DIRECTED_AI_IMAGE_INTEGRATION_2026-11-12", f"Missing owner integration record: {figure_id}"
    raw = (ASSETS / path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected_sha, f"AI10 file mismatch: {figure_id}"
    assert entry.get("size") == len(raw), f"AI10 file length mismatch: {figure_id}"
print("PASS: all 10 owner-selected AI PNGs present in registered lesson slots, exact bytes and attribution")
print("NOTE: release also requires independent biology/Tamil review; this script does not waive it")
