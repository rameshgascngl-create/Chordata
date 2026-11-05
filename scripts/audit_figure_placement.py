#!/usr/bin/env python3
"""Strict offline figure-to-lesson QA gate for the 39-topic Chordata app.

A provisional specimen outline is never counted as a finished, labelled plate.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"


def require(ok, message):
    if not ok:
        raise SystemExit("FIGURE PLACEMENT FAIL: " + message)


def read_json(name):
    return json.loads((ASSETS / name).read_text(encoding="utf-8"))


def main():
    pack = read_json("chordata_content.json")
    topics = [topic for unit in pack["units"] for topic in unit["topics"]]
    topic_by_id = {topic["id"]: topic for topic in topics}
    required = {diagram_id for topic in topics for diagram_id in topic["diagramIds"]}
    require(len(required) == 64, "course content must contain 64 unique diagram IDs")

    registry = read_json("figure_slots.json")
    require(registry.get("schemaVersion") == 1, "unknown placement schema")
    slots = registry.get("slots", [])
    require(len(slots) == 64, "registry must have 64 slots")
    require(len({slot["id"] for slot in slots}) == 64, "duplicate diagram slots")
    require({slot["id"] for slot in slots} == required, "missing or invented diagram IDs")

    known_statuses = {"PENDING", "ACADEMICALLY_APPROVED"}
    for slot in slots:
        topic = topic_by_id.get(slot.get("topicId"))
        require(topic is not None, "orphan diagram " + slot["id"])
        require(slot["id"] in topic["diagramIds"], "diagram in wrong topic: " + slot["id"])
        page = slot.get("page")
        require(isinstance(page, int) and 1 <= page <= len(topic["sections"]),
                "diagram assigned to intro, quiz, or invalid page: " + slot["id"])
        require(topic["sections"][page - 1]["key"] == slot.get("sectionKey"),
                "wrong lesson section for: " + slot["id"])
        require(slot.get("status") in known_statuses, "invalid review status: " + slot["id"])
        for name in ("captionEn", "captionTa"):
            require(isinstance(slot.get(name), str) and slot[name].strip(),
                    "missing bilingual caption: " + slot["id"])

    provisional = read_json("figures.json")
    require(isinstance(provisional, list), "provisional figure register invalid")
    require(len({f["id"] for f in provisional}) == len(provisional),
            "duplicate provisional figure IDs")
    require(len(provisional) == 7, "QA build must contain exactly 3 original + 4 credited images")
    provisional_by_id = {f["id"]: f for f in provisional}
    draft_slots = [s for s in slots if s.get("provisionalFigureId")]
    require(len(draft_slots) == 7, "expected seven explicitly mapped reference illustrations")
    require({s["provisionalFigureId"] for s in draft_slots} == set(provisional_by_id),
            "provisional illustration not linked to exactly one diagram slot")
    for slot in draft_slots:
        figure = provisional_by_id[slot["provisionalFigureId"]]
        require(figure["topicId"] == slot["topicId"] and figure["page"] == slot["page"],
                "draft illustration placed on wrong page: " + figure["id"])
        require(slot["status"] == "PENDING",
                "unlabelled outline cannot satisfy labelled anatomical plate: " + slot["id"])

    png_dir = ASSETS / "figures"
    digest_records = json.loads((png_dir / "source-hashes.json").read_text(encoding="utf-8"))
    hashes = {v["id"]: v for v in digest_records}
    require(set(hashes) == set(provisional_by_id), "hash inventory mismatch")
    expected_files = {f["file"] for f in provisional}
    actual_files = {p.name for p in png_dir.glob("*.png")}
    require(actual_files == expected_files, "unexpected or absent PNG image assets")
    for figure in provisional:
        name = figure["file"]
        require(name.endswith(".png") and Path(name).name == name, "unsafe figure filename")
        data = (png_dir / name).read_bytes()
        require(len(data) > 10_000 and data.startswith(bytes.fromhex("89504e470d0a1a0a")),
                "invalid PNG file: " + name)
        width, height = struct.unpack(">II", data[16:24])
        require(width >= 1200 and height >= 600, "figure too small: " + name)
        expected_digest = hashes[figure["id"]]["sha256"]
        require(hashlib.sha256(data).hexdigest() == expected_digest, "figure checksum mismatch")
        is_original = figure["id"] in ("scoliodon-external", "columba-external", "rabbit-external")
        if is_original:
            require(figure.get("author") and figure.get("license", "").startswith("Provisional QA artwork"),
                    "original QA figure wrongly credited: " + figure["id"])
        else:
            require(figure["id"].startswith("commons-") and figure.get("origin") == "Wikimedia Commons",
                    "source figure missing Commons provenance: " + figure["id"])
            require(figure.get("sourceUrl", "").startswith("https://commons.wikimedia.org/wiki/File:"),
                    "source image lacks exact owner file page: " + figure["id"])
            require(figure.get("licenseUrl", "").startswith("https://creativecommons.org/"),
                    "source image lacks licence URL: " + figure["id"])
            require(figure.get("reviewStatus") == "REFERENCE_SOURCE_AWAITING_ACADEMIC_REVIEW",
                    "unreviewed figure misrepresented: " + figure["id"])
    unit_counts = Counter(s["topicId"].split("-")[0] for s in slots)
    print("PASS: 64/64 figure slots have unique exact lesson-page assignments")
    print("PASS: 7/7 PNG image assets correctly placed, PNG/hash checked (3 original QA + 4 credited sources)")
    print("PASS: overview contains no figure slot; bilingual captions exist for all slots")
    print("PENDING: 64/64 scientifically approved plates; 57 have no reference image, 7 references unapproved")
    print("BY UNIT:", dict(sorted(unit_counts.items())))


if __name__ == "__main__":
    main()
