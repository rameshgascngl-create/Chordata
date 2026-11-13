#!/usr/bin/env python3
"""Editorial-intake gate: expanded bilingual textbook content; original syllabus untouched."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1] / "app/src/main/assets"
course = json.loads((ROOT / "chordata_content.json").read_text(encoding="utf-8"))
book = json.loads((ROOT / "chordata_textbook_chapters.json").read_text(encoding="utf-8"))
assert book["schemaVersion"] == 1
assert "DRAFT" in book["status"], "Unreviewed academic text must not claim sign-off"
topics = {t["id"] for u in course["units"] for t in u["topics"]}
chapter_ids = set()
keys = set()
assert book["chapters"]
for chapter in book["chapters"]:
    assert chapter["topicId"] in topics
    assert chapter["id"] not in chapter_ids
    chapter_ids.add(chapter["id"])
    assert len(chapter["sections"]) >= 5
    for section in chapter["sections"]:
        key = (chapter["id"], section["key"])
        assert key not in keys
        keys.add(key)
        for field in ("heading", "body"):
            assert all(section[field][lang].strip() for lang in ("en", "ta"))
        assert len(section["body"]["en"]) >= 150
        assert len(section["body"]["ta"]) >= 150
        assert re.search(r"[\u0b80-\u0bff]", section["body"]["ta"])
    assert chapter.get("sources"), "Every chapter needs reference leads"
# This is now a full undergraduate digital textbook. A clean partial chapter
# audit is not sufficient: enforce a one-to-one mapping to every syllabus topic.
covered = [chapter["topicId"] for chapter in book["chapters"]]
missing = sorted(topics - set(covered))
duplicates = sorted({topic_id for topic_id in covered if covered.count(topic_id) > 1})
assert not missing, f"Unexpanded syllabus topic(s): {missing}"
assert not duplicates, f"Duplicate textbook topic coverage: {duplicates}"
assert len(covered) == len(topics), f"Expected {len(topics)} chapters, found {len(covered)}"
print(f"PASS: {len(chapter_ids)}/{len(topics)} syllabus topics, {len(keys)} extended bilingual sections, "
      "source references, explicit draft review status")
