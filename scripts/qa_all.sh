#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/scripts/audit_content.py"
"$ROOT/scripts/run_core_tests.sh"
python3 - "$ROOT" <<'PY'
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
root = Path(sys.argv[1])
for f in (root/'app/src/main/AndroidManifest.xml', root/'app/src/main/res/values/strings.xml'):
    ET.parse(f)
print('PASS: Android XML files well-formed')
PY
