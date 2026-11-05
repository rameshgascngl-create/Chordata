#!/usr/bin/env python3
"""Stage downloaded and credited Commons reference images for a QA-only APK.

The 64 anatomy requirements remain PENDING; these five sources are not academic approvals.
"""
import json, hashlib, pathlib, shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
ASSET=ROOT/"app/src/main/assets"
INTAKE=ROOT/"build/commons_image_intake"
FIGDIR=ASSET/"figures"
def read(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
records=read(INTAKE/"SOURCE_CREDITS.json")["sources"]
slots=read(ASSET/"figure_slots.json")
original=read(ASSET/"figures.json")
hashes=read(FIGDIR/"source-hashes.json")
reference=read(ROOT/"docs/research/credited_image_sources.json")["sources"]
refs={r["id"]:r for r in reference}
expected={"lancelet-labelled","frog-arteries","bird-respiration","pigeon-skeleton","rabbit-skeleton"}
assert {r["id"] for r in records}==expected
assert len(original)==3 and len(hashes)==3
slotById={x["id"]:x for x in slots["slots"]}
assert len(slotById)==64
assert all(x["provisionalFigureId"] is None for x in slots["slots"] if x["id"] in {r["diagramId"] for r in records})
for r in records:
    verified=refs[r["id"]]
    assert r["sha256"] and r["creator"]==verified["creator"] and r["license"]==verified["license"]
    slot=slotById[r["diagramId"]]
    assert slot["status"]=="PENDING" and r["diagramId"]==verified["diagramId"]
    assert r["reviewStatus"]=="SOURCE_ONLY_AWAITING_INDEPENDENT_ANATOMICAL_REVIEW"
    figId="commons-"+r["id"]
    filename=r["localFile"]
    source=INTAKE/"figures"/filename
    data=source.read_bytes()
    assert data.startswith(bytes.fromhex("89504e470d0a1a0a")) and len(data)>10000
    assert hashlib.sha256(data).hexdigest()==r["sha256"]
    shutil.copy2(source,FIGDIR/filename)
    slot["provisionalFigureId"]=figId
    isComparable=r["suitability"] in ("COMPARATIVE_ONLY","PARTIAL_SCOPE")
    suffixEn=" (comparative source; species-specific review pending)" if isComparable else " (credited reference; anatomical approval pending)"
    suffixTa=" (ஒப்பீட்டு ஆதாரம்; இனச்சிறப்புச் சரிபார்ப்பு நிலுவை)" if isComparable else " (பட உரிமையாளர் குறிப்பிடப்பட்ட ஆதாரம்; உடற்கூறியல் ஒப்புதல் நிலுவை)"
    original.append({
        "id":figId,"topicId":slot["topicId"],"page":slot["page"],"file":filename,
        "captionEn":slot["captionEn"]+suffixEn,"captionTa":slot["captionTa"]+suffixTa,
        "author":r["creator"],"license":r["license"],"sourceUrl":r["sourcePageUrl"],
        "licenseUrl":r["licenseUrl"],"modifications":r["modifications"],
        "originalFilename":r["originalFilename"],"origin":"Wikimedia Commons",
        "reviewStatus":"REFERENCE_SOURCE_AWAITING_ACADEMIC_REVIEW"
    })
    hashes.append({"id":figId,"file":filename,"size":len(data),"sha256":r["sha256"],
                   "status":"LICENSED_SOURCE_REFERENCE_NOT_ACADEMICALLY_APPROVED"})
    print("STAGED",figId,"topic",slot["topicId"],"page",slot["page"],"owner",r["creator"])
assert len(original)==8 and len(hashes)==8
assert len([s for s in slots["slots"] if s["provisionalFigureId"]])==8
write(ASSET/"figure_slots.json",slots)
write(ASSET/"figures.json",original)
write(FIGDIR/"source-hashes.json",hashes)
shutil.copy2(INTAKE/"SOURCE_CREDITS.json",ASSET/"source_reference_credits.json")
print("PASS 8 offline PNGs staged, 5 licensed references credited, 64 slots still PENDING")
