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
# Unit V textbook extensions must remain complete in both languages and
# appear exactly once in the book reader without dropping established sections.
by_topic = {chapter["topicId"]: chapter for chapter in book["chapters"]}
unit5_required = {
    "u5-columba": {
        "skin-feather-tracts-preening-moult",
        "thoracic-pump-and-ventilation",
        "renal-microanatomy-water-balance",
        "comparative-anatomy-laboratory-workflow",
    },
    "u5-flight-adaptations": {
        "wing-loading-aspect-ratio",
        "wingbeat-phases-and-control",
        "flight-modes-and-ecological-specialisation",
        "flight-fuel-and-muscle-energetics",
        "thermal-water-balance-in-flight",
        "comparative-flight-investigation",
    },
}
for topic, required in unit5_required.items():
    sections = by_topic[topic]["sections"]
    keys_found = [section["key"] for section in sections]
    assert required.issubset(keys_found), (topic, "missing required scientific topics", required - set(keys_found))
    assert len(keys_found) == len(set(keys_found)), (topic, "duplicate page keys")
    assert all(len(section["body"][lang]) >= 450 for section in sections
               if section["key"] in required for lang in ("en", "ta")), (topic, "incomplete long-form bilingual section")
assert len(by_topic["u5-columba"]["sections"]) >= 20
assert len(by_topic["u5-flight-adaptations"]["sections"]) >= 12
avian_expectations = {
    "u5-aves-classification": {
        "historical-vs-genomic-bird-classification",
        "genomic-neoaves-evidence-and-uncertainty",
    },
    "u5-bird-migration": {"migratory-annual-cycle-and-survey-inference"},
}
for topic_id, required_keys in avian_expectations.items():
    chapter = by_topic[topic_id]
    section_by_key = {section["key"]: section for section in chapter["sections"]}
    assert required_keys <= set(section_by_key), f"Missing new Aves sections for {topic_id}"
    for key in required_keys:
        section = section_by_key[key]
        assert len(section["body"]["en"]) >= 500 and len(section["body"]["ta"]) >= 500, (topic_id, key, "shortened")
        assert section["heading"]["en"] and section["heading"]["ta"], (topic_id, key, "heading missing")
assert len(by_topic["u5-aves-classification"]["sections"]) >= 9
assert len(by_topic["u5-bird-migration"]["sections"]) >= 7
assert len(by_topic["u5-columba"]["sections"]) >= 20
assert len(by_topic["u5-flight-adaptations"]["sections"]) >= 12
mammal_keys = {
    "jaw-joint-to-middle-ear-fossils",
    "placental-root-phylogenomics-and-fossil-dating",
}
mammal_sections = {s["key"]: s for s in by_topic["u5-mammalia-classification"]["sections"]}
assert mammal_keys <= set(mammal_sections), "Missing mammalian evolutionary anatomy"
assert len(by_topic["u5-mammalia-classification"]["sections"]) >= 8
assert all(len(mammal_sections[k]["body"][lang]) >= 750
           for k in mammal_keys for lang in ("en", "ta")), "Mammal bilingual depth"
mammalian_additions = {
    "u5-marsupials": {"diapause-and-asynchronous-lactation"},
    "u5-flying-mammals": {"cf-fm-biosonar-and-range-finding"},
}
for topic_id, names in mammalian_additions.items():
    sections = {s["key"]: s for s in by_topic[topic_id]["sections"]}
    assert names <= set(sections), ("Missing Mammalia lesson", topic_id)
    assert all(len(sections[k]["body"][lang]) >= 700
               for k in names for lang in ("en", "ta")), ("Abbreviated Mammalia lesson", topic_id)
assert len(by_topic["u5-mammalia-classification"]["sections"]) == 8
assert len(by_topic["u5-marsupials"]["sections"]) == 7
assert len(by_topic["u5-flying-mammals"]["sections"]) == 7
new_mammal_sections = {
    "u5-rabbit": "duplex-uterus-induced-ovulation-and-placenta",
    "u5-aquatic-mammals": "alveolar-compression-nitrogen-and-dive-risk",
}
for topic_id, section_key in new_mammal_sections.items():
    sections = {section["key"]: section
                for section in by_topic[topic_id]["sections"]}
    assert section_key in sections, ("Missing new mammal physiology", topic_id)
    assert all(len(sections[section_key]["body"][lang]) >= 800
               for lang in ("en", "ta")), ("Insufficient bilingual anatomy", topic_id)
    assert all(sections[section_key]["heading"][lang].strip()
               for lang in ("en", "ta")), ("Missing translated heading", topic_id)
assert len(by_topic["u5-rabbit"]["sections"]) == 17
assert len(by_topic["u5-aquatic-mammals"]["sections"]) == 9
assert len(keys) >= 319, f"Expected >=319 full bilingual textbook sections, found {len(keys)}"
# Anatomical safeguards for the two evidence-based Unit V corrections. These
# tests protect both student languages, not just exact English phrasing.
pigeon_egg = {s["key"]: s for s in by_topic["u5-columba"]["sections"]}["reproductive-organs-and-egg-formation"]
for term in ("infundibulum", "magnum", "isthmus", "shell gland", "vagina", "ureters", "no urinary bladder"):
    assert term in pigeon_egg["body"]["en"], ("Pigeon urinogenital teaching anatomy missing", term)
for term in ("இன்பண்டிபுலம்", "மேக்னம்", "இஸ்த்மஸ்", "ஓட்டுச் சுரப்பி", "யோனி", "சிறுநீர்க்குழாய்", "சிறுநீர்ப்பை இல்லை"):
    assert term in pigeon_egg["body"]["ta"], ("Pigeon Tamil anatomical equivalent missing", term)
avian_air = {s["key"]: s for s in by_topic["u5-flight-adaptations"]["sections"]}["respiratory-system"]
for term in ("palaeopulmonic", "neopulmonic", "bidirectional"):
    assert term in avian_air["body"]["en"], ("Avian lung physiological distinction missing", term)
for term in ("பேலியோபுல்மோனிக்", "நியோபுல்மோனிக்", "இரு திசை"):
    assert term in avian_air["body"]["ta"], ("Avian lung Tamil physiological distinction missing", term)
print("PASS: bilingual pigeon urinogenital anatomy and avian palaeo-/neopulmonic airflow")
print(f"PASS: {len(chapter_ids)}/{len(topics)} syllabus topics, {len(keys)} extended bilingual sections, "
      "source references, explicit draft review status")
