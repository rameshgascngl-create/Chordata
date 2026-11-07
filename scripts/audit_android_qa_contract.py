#!/usr/bin/env python3
"""Offline QA-contract checks, not a substitute for Android compilation.

Cross-check the instrumented tests and figure rendering against the actual
64-slot registry.  Exit non-zero if a source refactor silently invalidates
required tests or the package's reproducible QA entrypoint.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'app/src/main/assets'
registry = json.loads((ASSETS / 'figure_slots.json').read_text(encoding='utf-8'))
slots = registry['slots']
by_id = {s['id']: s for s in slots}
assert len(slots) == 64 and len(by_id) == 64, 'Expected 64 distinct registered diagrams'
manifest = json.loads((ASSETS / 'pencil_plates/manifest.json').read_text(encoding='utf-8'))
entries = manifest['figures']
assert len(entries) == 68, 'Expected 68 annotated drawing variants'
assert {e['diagramId'] for e in entries} == set(by_id), 'Registry/artwork mismatch'

test_file = ROOT / 'app/src/androidTest/java/in/gasc/zoology/chordata/ReaderNavigationTest.kt'
test_text = test_file.read_text(encoding='utf-8')
gallery_text = (ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/FigureGallery.kt').read_text(encoding='utf-8')
workflow = (ROOT / '.github/workflows/android-qa.yml').read_text(encoding='utf-8')
qa_script = (ROOT / 'scripts/qa_all.sh').read_text(encoding='utf-8')

# Literal navigation selectors must be current lesson diagram IDs, never old
# internal Figure IDs.  Dynamic helper IDs are verified at call sites below.
selectors = set(re.findall(r'figure-image-([a-z][a-z0-9-]+)', test_text))
assert selectors <= set(by_id), 'Stale instrumented figure selectors: ' + repr(selectors - set(by_id))
for id in ('u2-scoliodon-brain-labelled', 'u2-scoliodon-external-labelled'):
    assert id in selectors, 'Lost Scoliodon reachability test: ' + id
assert by_id['u2-scoliodon-brain-labelled']['page'] == 4
for id in ('u5-columba-external', 'u5-rabbit-external'):
    assert ('"' + id + '"') in test_text, 'Missing placement verification for ' + id

# The English-labelled PNG variant deliberately appears in BOTH native reader
# languages; captions and lesson text remain individually translated.
assert 'pencilPlates[slot.id to "en"] ?: pencilPlates[slot.id to "shared"]' in gallery_text
assert 'assetDirectory = assetDirectory' in gallery_text, 'Gallery must honour canonical manifest asset path'
assert 'filename = entry.getString("path").substringAfterLast' not in gallery_text
assert all(e['path'].startswith('pencil_plates/') and len(e['path'].split('/')) == 2 for e in entries), 'Manifest still contains staging aliases'
assert 'pencilPlates[slot.id to language]' not in gallery_text
assert 'FigureGallery(topic.id, page, lang' in (ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/ChordataApp.kt').read_text(encoding='utf-8')

# Reproducibility: a ZIP extractor may not restore Unix executable bits.
# The entrypoint must invoke the Kotlin smoke-test shell script explicitly.
assert 'bash "$ROOT/scripts/run_core_tests.sh"' in qa_script
assert 'scripts/audit_android_qa_contract.py' in qa_script
assert 'scripts/audit_preview_bitmap_budget.py' in qa_script
assert 'fun all64ProvisionalPlatesAreBundledAndDecode()' in test_text
assert 'fun all64FigureSlotsAreMappedToActualSectionsInApk()' in test_text
assert 'fun scoliodonBrainPlateIsReachableOnItsExactFourthSection()' in test_text
assert 'captureQaScreen("scoliodon-brain-zoom-en-100")' in test_text

# Confirm that all three remote jobs fail before building an APK if any figure
# asset, source hash or lesson mapping disappears.
assert workflow.count('python3 scripts/audit_pencil_coverage.py') == 3
assert workflow.count('python3 scripts/audit_coverage_report.py') == 3
assert workflow.count('python3 scripts/audit_figure_placement.py') == 3
assert 'python3 scripts/audit_android_qa_contract.py' in workflow
assert 'python3 scripts/write_figure_review_register.py --check' in workflow
assert 'python3 scripts/test_review_signoff_guards.py' in workflow
assert 'app/src/main/assets/pencil_plates/' in workflow
assert workflow.count('bash scripts/verify_sdk37_platform.sh') == 2, 'SDK37 compatibility gate missing from Android jobs'
assert 'python3 scripts/test_sdk37_platform.py' in workflow
assert 'python3 "$ROOT/scripts/test_sdk37_platform.py"' in qa_script
assert 'context.assets.open(path)' in test_text, 'Instrumented tests must decode exact manifest path'
assert 'context.assets.open("pencil_plates/$filename")' not in test_text, 'Legacy basename fallback present in instrumented test'
assert 'python3 scripts/audit_built_apk_assets.py --self-test' in workflow
assert 'python3 scripts/test_apk_source_fixture.py' in workflow
assert 'scripts/test_apk_source_fixture.py' in qa_script
assert workflow.count('python3 scripts/audit_built_apk_assets.py app/build/outputs/apk/debug/app-debug.apk') == 2
assert 'scripts/audit_built_apk_assets.py" --self-test' in qa_script
assert 'All 64 lesson-diagram slots contain provisional illustrations' in (ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/ChordataApp.kt').read_text(encoding='utf-8')
assert ':app:assembleDebug' in workflow
assert ':app:connectedDebugAndroidTest' in workflow
assert 'retention-days:' in workflow
print('PASS: native QA contract — 64 slot IDs, 68 figure variants, actual Compose tags and screenshot test')
print('PASS: English-labelled drawings shared across both languages; no stale literal figure selectors')
print('PASS: all three CI jobs audit the full assets before compilation/emulation')
print('NOTE: static QA only; Android compilation and emulator results not certified')
