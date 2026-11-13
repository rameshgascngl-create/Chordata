#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/scripts/audit_content.py"
python3 "$ROOT/scripts/audit_figure_placement.py"
python3 "$ROOT/scripts/audit_pencil_coverage.py"
python3 "$ROOT/scripts/audit_ai10_release_assets.py"
python3 "$ROOT/scripts/audit_coverage_report.py"
python3 "$ROOT/scripts/audit_android_qa_contract.py"
python3 "$ROOT/scripts/audit_preview_bitmap_budget.py"
python3 "$ROOT/scripts/audit_built_apk_assets.py" --self-test
python3 "$ROOT/scripts/test_apk_source_fixture.py"
python3 "$ROOT/scripts/write_figure_review_register.py" --check
python3 "$ROOT/scripts/test_review_signoff_guards.py"
python3 "$ROOT/scripts/test_sdk37_platform.py"
python3 "$ROOT/scripts/test_git_sync_whitespace.py"
python3 "$ROOT/scripts/check_textbook_plates.py"
python3 "$ROOT/scripts/validate_credited_sources.py"
bash "$ROOT/scripts/run_core_tests.sh"
python3 - "$ROOT" <<'PY'
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
root = Path(sys.argv[1])
for f in (root/'app/src/main/AndroidManifest.xml', root/'app/src/main/res/values/strings.xml'):
    ET.parse(f)
print('PASS: Android XML files well-formed')
PY
