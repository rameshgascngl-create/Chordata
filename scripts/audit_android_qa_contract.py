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

# English/shared variants remain the default in both native reader languages.
# Only an explicitly green-ticked Tamil AI PNG may override that fallback in Tamil.
assert 'val fallback = entries[diagramId to "en"] ?: entries[diagramId to "shared"]' in gallery_text
assert 'entries[diagramId to "ta"]' in gallery_text
assert 'GREEN_TICK_ALLOW_PROVISIONAL_QA_USE' in gallery_text
assert 'selectProvisionalPlate(pencilPlates, slot.id, lang)' in gallery_text
assert 'assetDirectory = assetDirectory' in gallery_text, 'Gallery must honour canonical manifest asset path'
assert 'filename = entry.getString("path").substringAfterLast' not in gallery_text
assert all(e['path'].startswith('pencil_plates/') and len(e['path'].split('/')) == 2 for e in entries), 'Manifest still contains staging aliases'
assert 'pencilPlates[slot.id to language]' not in gallery_text
assert 'FigureGallery(topic.id, sectionIndex + 1, lang' in (ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/ChordataApp.kt').read_text(encoding='utf-8')

# Reproducibility: a ZIP extractor may not restore Unix executable bits.
# The entrypoint must invoke the Kotlin smoke-test shell script explicitly.
assert 'bash "$ROOT/scripts/run_core_tests.sh"' in qa_script
assert 'scripts/audit_android_qa_contract.py' in qa_script
assert 'scripts/audit_preview_bitmap_budget.py' in qa_script
assert 'fun all64ProvisionalPlatesAreBundledAndDecode()' in test_text
assert 'fun all64FigureSlotsAreMappedToActualSectionsInApk()' in test_text
brain_entry = next(e for e in entries if e['diagramId'] == 'u2-scoliodon-brain-labelled' and e['lang'] == 'en')
if brain_entry.get('visualReview') == 'USER_REJECTED_REPLACEMENT_REQUIRED':
    # The user rejected this unscientific illustration; preserving a test
    # requiring its display would silently defeat the quality-control gate.
    assert 'fun rejectedScoliodonBrainIsWithheldOnItsExactFourthSection()' in test_text
    assert 'captureQaScreen("scoliodon-brain-rejected-en-100")' in test_text
    assert 'figure-rejected-quality' in gallery_text
    assert 'USER_REJECTED_REPLACEMENT_REQUIRED' in gallery_text
else:
    assert 'fun scoliodonBrainPlateIsReachableOnItsExactFourthSection()' in test_text
    assert 'captureQaScreen("scoliodon-brain-zoom-en-100")' in test_text

# Additional lessons live outside the immutable syllabus course pack.
# Validate their exact page anchors and bilingual completeness before Android QA.
extras = json.loads((ASSETS / 'chordata_learning_points.json').read_text(encoding='utf-8'))
course = json.loads((ASSETS / 'chordata_content.json').read_text(encoding='utf-8'))
course_topics = [topic for unit in course['units'] for topic in unit['topics']]
known_sections = {(topic['id'], section['key']) for topic in course_topics
                  for section in topic['sections']}
seen_enrichment = set()
assert extras['schemaVersion'] == 1 and len(extras['sections']) == len(course_topics) == 39
for block in extras['sections']:
    name = (block['topicId'], block['sectionKey'])
    assert name in known_sections and name not in seen_enrichment, ('Bad supplemental anchor', name)
    seen_enrichment.add(name)
    assert len(block['points']) == 3, ('Exactly three points required', name)
    assert all(len(p['en'].strip()) >= 50 and len(p['ta'].strip()) >= 45
               for p in block['points']), ('Incomplete bilingual point', name)
assert len({topicId for topicId, _ in seen_enrichment}) == 39
assert 'fun bilingualPointwiseEnrichmentPreservesOriginalChapterStructure()' in test_text
assert 'PointwiseExplanation(section.keyPoints, lang, scale)' in (
    ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/ChordataApp.kt').read_text(encoding='utf-8')

# Confirm that all four remote jobs audit image source integrity before QA
# publication; the fourth job is gated on compilation AND instrumentation.
assert workflow.count('python3 scripts/audit_pencil_coverage.py') == 4
assert workflow.count('python3 scripts/audit_coverage_report.py') == 4
assert workflow.count('python3 scripts/audit_figure_placement.py') == 4
assert 'python3 scripts/audit_android_qa_contract.py' in workflow
assert 'python3 scripts/write_figure_review_register.py --check' in workflow
assert 'python3 scripts/test_review_signoff_guards.py' in workflow
assert 'app/src/main/assets/pencil_plates/' in workflow
assert workflow.count('bash scripts/verify_sdk37_platform.sh') == 3, 'SDK37 compatibility gate missing from compile, emulator or gated publication'
assert 'python3 scripts/test_sdk37_platform.py' in workflow
assert 'python3 "$ROOT/scripts/test_sdk37_platform.py"' in qa_script
assert 'context.assets.open(path)' in test_text, 'Instrumented tests must decode exact manifest path'
assert 'context.assets.open("pencil_plates/$filename")' not in test_text, 'Legacy basename fallback present in instrumented test'
assert 'python3 scripts/audit_built_apk_assets.py --self-test' in workflow
assert 'python3 scripts/test_apk_source_fixture.py' in workflow
assert 'scripts/test_apk_source_fixture.py' in qa_script
assert workflow.count('python3 scripts/audit_built_apk_assets.py app/build/outputs/apk/debug/app-debug.apk') == 2
assert 'scripts/audit_built_apk_assets.py" --self-test' in qa_script
# Student-facing pages should not expose internal QA status and build jargon.
# The first reader page is now guide + first real section; figure register
# remains 1-based by section and is not rewritten or duplicated.
app_ui = (ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/ChordataApp.kt').read_text(encoding='utf-8')
gallery_ui = (ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/FigureGallery.kt').read_text(encoding='utf-8')
assert 'All 64 lesson-diagram slots contain provisional illustrations' not in app_ui
assert 'home-book-layout' in app_ui and 'subject-title' in app_ui
privacy_ui = (ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/PrivacyPolicyScreen.kt').read_text(encoding='utf-8')
assert 'privacy-policy-entry' in app_ui and 'privacy-policy-back' in app_ui
assert 'tab == "privacy" -> PrivacyPolicyPage(lang, textScale,' in app_ui
assert 'onEraseLocalData = {' in app_ui
assert 'fun eraseLearningDataRequiresConfirmationAndPersistsDeletion()' in test_text
assert 'fun PrivacyPolicyPage(language: ReadingLanguage, textScale: Float,' in privacy_ui
assert 'textScale.coerceIn(1f, 2f)' in privacy_ui
assert 'fontSize = (16f * scale).sp' in privacy_ui
assert 'privacy-policy-heading' in privacy_ui
assert 'privacy-policy-page' in privacy_ui
assert 'fun privacyPolicyIsAvailableInEnglishWithoutNetwork()' in test_text
assert 'fun privacyPolicyIsAccessibleInTamilAt200Percent()' in test_text
assert 'scripts/audit_store_preflight.py' in workflow
assert ':app:bundleRelease :app:lintRelease' in workflow
assert '<html lang="en">' in (ROOT / 'docs/privacy-policy.html').read_text(encoding='utf-8')
# The owner requested a book-style reader: justify body paragraphs in both
# paged and continuous modes; keep headings, keys and controls start-aligned.
assert app_ui.count('base = 16f, alignment = TextAlign.Justify)') == 2, 'Both lesson reading modes must justify body paragraphs'
assert 'alignment = TextAlign.Start' in app_ui, 'Keep explanatory lists start-aligned'
assert 'reader-next' in app_ui and 'reader-previous' in app_ui, 'Full-width reader navigation tags absent'
assert 'fun tamilPagerRemainsWideAt200Percent()' in test_text, 'Tamil 200% pager regression test missing'
assert 'if (currentTopic == null) {' in app_ui and 'app-bottom-navigation' in app_ui, (
    'Student lesson view must use the reclaimed bottom-bar area')
assert 'fun lessonHidesBottomNavigationAndRestoresItOnBack()' in test_text, (
    'Missing Android navigation/reading-area regression test')
assert 'FigureGallery(topic.id, sectionIndex + 1, lang' in app_ui
assert 'figure-credits-toggle-' in gallery_ui, 'Image credits must remain accessible'
assert 'Image source and credits' in gallery_ui
# Student pages must not repeat internal QA and sign-off notices beneath
# each correctly placed illustration. Source credits and failure diagnostics stay.
assert 'figure-pending-page' not in gallery_ui, 'Redundant internal QA panel returned to lesson pages'
assert 'figure-overview-status' not in gallery_ui, 'Non-subject figure status returned to chapter outline'
# Six original screenshots exposed a pedagogic problem, not a PNG-file
# problem. Keep the three sourced replacements and four marine-mammal photos
# active alongside the corrected Calotes functional schematic.
sourced_ids = {
    'u4-snakes-india-big-four-identification',
    'u5-flight-adaptations-flight-muscles',
    'u5-marsupials-marsupial-life-history',
}
sourced = [v for v in entries if v['diagramId'] in sourced_ids]
assert len(sourced) == 3
assert all(v['visualReview'] == 'SOURCED_TEACHING_FIGURE_QA_PROVISIONAL'
           and v.get('pedagogicStatus') ==
               'REPLACED_WITH_CC_LICENSED_SOURCE_QA_PENDING_2026-11-12'
           and v['sourceUrl'].startswith('https://commons.wikimedia.org/wiki/File:')
           and len(v.get('sourceSha256', [])) >= 1
           and v.get('retiredSchematicPng') and v.get('retiredSchematicSvg')
           for v in sourced), 'Sourced replacements need genuine provenance and retained originals'
assert len(next(v for v in sourced if v['diagramId'] ==
    'u4-snakes-india-big-four-identification')['sourceUrls']) == 4
calotes_photo = next(x for x in entries if x['diagramId'] == 'u4-calotes-external')
assert calotes_photo.get('visualReview') == 'SOURCED_REAL_SPECIMEN_PHOTO_QA_PROVISIONAL'
assert calotes_photo.get('sourceUrl') == 'https://commons.wikimedia.org/wiki/File:Oriental_Lizard.jpg'
heart = next(x for x in entries if x['diagramId'] == 'u4-calotes-arterial-system')
assert heart.get('visualReview') == 'SOURCE_CHECKED_FUNCTIONAL_SCHEMATIC_QA_PROVISIONAL'
assert not heart.get('scientificRiskHold')
assert heart.get('pedagogicStatus') == 'REPLACED_WITH_SOURCE_CHECKED_FUNCTIONAL_SCHEMATIC_2026-11-13'
assert 'selectedPlateNeedsReplacement(pencilPlates, slot.id, lang)' in gallery_ui
assert heart.get('reviewStatus', '').startswith('PROVISIONAL_')
assert heart.get('sha256') == '937660abab533455b91cf1e0935c12d635f6df20fef63750d62e65efafbc1b7e'
assert heart.get('retiredSchematicPng') and heart.get('retiredSchematicSvg')
assert 'RIGHT atrium' in heart.get('editorialCaution', '')
rabbit = next(x for x in entries if x['diagramId'] == 'u5-rabbit-sense-organs')
assert rabbit.get('visualReview') == 'SOURCED_REAL_RABBIT_SENSORY_PHOTO_QA_PROVISIONAL'
assert rabbit.get('sourceUrl', '').endswith('File:Side_view_of_the_head_of_a_pet_rabbit_in_Brussels_(DSCF0830).jpg')
assert rabbit.get('retiredSchematicPng') and rabbit.get('retiredSchematicSvg')
monotreme = next(x for x in entries if x['diagramId'] == 'u5-egg-laying-mammals-monotreme-reproduction')
assert monotreme['lang'] == 'shared' and len(monotreme.get('sourceUrls',[])) == 3
assert monotreme.get('visualReview') == 'SOURCED_REAL_MONOTREME_SPECIMENS_AND_ANATOMY_QA_PROVISIONAL'
assert monotreme.get('retiredSchematicPng') and monotreme.get('retiredSchematicSha256')
aquatic = next(x for x in entries if x['diagramId'] == 'u5-aquatic-mammals-aquatic-mammal-groups')
assert aquatic['lang'] == 'en'
assert aquatic['visualReview'] == 'SOURCED_FOUR_AQUATIC_MAMMAL_PHOTOGRAPHS_QA_PROVISIONAL'
assert len(aquatic.get('sourceUrls', [])) == 4
assert aquatic.get('retiredSchematicPng') and aquatic.get('retiredSchematicSvg')
assert 'additionalSourceUrls' in gallery_ui and 'figure-extra-source-' in gallery_ui
assert 'correctedCalotesHeartAndSourcedPlatesAreAvailableInBothLanguages()' in test_text
assert 'figure-image-' in gallery_ui and 'figure-credits-toggle-' in gallery_ui
assert 'figure-rejected-quality' in gallery_ui and 'figure-error-' in gallery_ui
assert 'Draft anatomical plate · scientific review pending' not in gallery_ui
# Technical QA terminology must be retained in provenance fields, not in student keys.
for figure in entries:
    student_key = (figure.get('keyEn', '') + ' ' + figure.get('keyTa', '')).lower()
    for phrase in ('scientific review pending', 'anatomical signoff pending',
                   'requires independent zoology review', 'provisional:',
                   'உடற்கூறியல் ஒப்புதல் நிலுவையில்', 'அறிவியல் சரிபார்ப்பு நிலுவையில்',
                   'பெயரிடல் சரிபார்ப்பு நிலுவையில்'):
        assert phrase not in student_key, ('Internal review note leaked into figure caption', figure['diagramId'], phrase)
assert 'needs: [prepare-figures, native-qa, android-instrumentation]' in workflow, 'APK publication must depend on BOTH compilation and emulator instrumentation'
assert "needs.native-qa.result == 'success' && needs.android-instrumentation.result == 'success'" in workflow, 'Final published APK must use explicit success gates'
assert workflow.index('publish-tested-qa-apk:') > workflow.index('android-instrumentation:'), 'Final publication must occur after instrumentation job'
assert 'Chordata_Parker_Pigeon_Tested_QA_APK' in workflow, 'Final QA artifact name missing'
assert 'name: Chordata_Native_QA_Debug' not in workflow, 'Premature ungated APK upload still present'
assert ':app:assembleDebug' in workflow
assert ':app:connectedDebugAndroidTest' in workflow
assert 'retention-days:' in workflow
print('PASS: native QA contract — 64 slot IDs, 68 figure variants, actual Compose tags and screenshot test')
print('PASS: green-ticked Tamil AI variants selectable; English/shared fallback preserved')
print('PASS: four CI jobs audit the full assets; tested QA APK only published after emulator success')
print('NOTE: static QA only; Android compilation and emulator results not certified')
