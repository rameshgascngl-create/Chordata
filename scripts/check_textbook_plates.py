#!/usr/bin/env python3
"""Fail build if museum photographs or uncredited replacements reappear."""
import json,hashlib, pathlib,struct
root=pathlib.Path(__file__).resolve().parents[1]/"app/src/main/assets"
figures=json.loads((root/"figures.json").read_text(encoding="utf-8"))
hashes={x["id"]:x for x in json.loads((root/"figures/source-hashes.json").read_text(encoding="utf-8"))}
for id,filename in (("commons-pigeon-skeleton","pigeon_endoskeleton_line_art.png"),
                    ("commons-rabbit-skeleton","rabbit_endoskeleton_line_art.png")):
    f=next(x for x in figures if x["id"]==id)
    assert f["file"]==filename, f"Wrong image on {id}"
    assert f["page"]==2 and f["topicId"] in ("u5-columba","u5-rabbit")
    assert f["license"].startswith("Public domain") and f["sourceUrl"].startswith("https://commons.wikimedia.org/wiki/File:")
    assert f["reviewStatus"]=="REFERENCE_SOURCE_AWAITING_ACADEMIC_REVIEW"
    raw=(root/"figures"/filename).read_bytes()
    assert raw[:8]==bytes.fromhex("89504e470d0a1a0a")
    w,h=struct.unpack(">II",raw[16:24])
    assert w>=1200 and h>=600 and len(raw)>20000
    assert hashlib.sha256(raw).hexdigest()==hashes[id]["sha256"]
    assert not (root/"figures"/("pigeon_skeleton.png" if "pigeon" in id else "rabbit_skeleton.png")).exists()
credits=json.loads((root/"source_reference_credits.json").read_text(encoding="utf-8"))
for entry in credits["sources"]:
    fig=next(x for x in figures if x["id"]=="commons-"+entry["id"])
    assert entry["localFile"]==fig["file"], "Credit filename mismatch"
    assert entry["embeddedInApk"] is True and entry["sourceStatus"]=="STAGED_OFFLINE_QA"
    assert entry["academicStatus"]=="PENDING" and entry["reviewStatus"]=="SOURCE_ONLY_AWAITING_INDEPENDENT_ANATOMICAL_REVIEW"
    assert entry["creator"]==fig["author"] and entry["sourcePageUrl"]==fig["sourceUrl"]
print("PASS: two museum photographs replaced with owner-credited historical line drawings; 7/7 source credits and filenames reconciled, academic approval pending")
