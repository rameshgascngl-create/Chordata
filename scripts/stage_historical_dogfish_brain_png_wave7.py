#!/usr/bin/env python3
"""Intake UNMODIFIED authenticated historical PNG. Never generate anatomical artwork."""
from pathlib import Path
from urllib.request import Request, urlopen
import csv, hashlib, json, subprocess
from PIL import Image
from io import BytesIO

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/"app/src/main/assets/pencil_plates/shark_brain_dorsal_en.png"
MANIFEST=ROOT/"app/src/main/assets/pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_BRAIN_HISTORICAL_PNG_INTAKE_QA.md"
ID="u2-scoliodon-brain-labelled"
URL="https://upload.wikimedia.org/wikipedia/commons/9/99/Fritsch_dogfish_shark_brain.png"
PAGE="https://commons.wikimedia.org/wiki/File:Fritsch_dogfish_shark_brain.png"
SOURCE_SHA1="3ccf7de9b4ea765cb606d12f3996f08ca68738ad"
AUTHOR="Gustav Theodor Fritsch (1878) — historical dogfish brain illustration"
REFS=[PAGE, "https://gcwgandhinagar.com/econtent/document/15878893641ZOOTC0201-%20Brain%20%20of%20scoliodon%20%281%29-1.pdf"]
OLD="49d7897c2fe5e413bd49ae6f36ceccc798beca1dc3631be233eb94a72ac7201a"

def main():
    req=Request(URL,headers={
      "User-Agent":"ChordataFigureAcademicQA/1.0 (https://github.com/rameshgascngl-create/Chordata)",
      "Referer":"https://commons.wikimedia.org/",
      "Accept":"image/png"})
    with urlopen(req,timeout=75) as response:
      data=response.read(3_000_001)
    sha1=hashlib.sha1(data).hexdigest()
    if sha1!=SOURCE_SHA1:
      raise ValueError(f"Original Wikimedia image changed SHA1: {sha1}")
    img=Image.open(BytesIO(data));img.load()
    if img.format!="PNG" or img.size!=(500,941) or len(data)<500_000:
      raise ValueError(f"Image fails expected PNG integrity: {img.format}/{img.size}/{len(data)}")
    sha=hashlib.sha256(data).hexdigest()
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    choices=[x for x in manifest["figures"] if x["diagramId"]==ID and x["lang"]=="en"]
    if len(choices)!=1:raise ValueError("Wrong or ambiguous registered brain figure")
    item=choices[0]
    if item["path"]!="pencil_plates/shark_brain_dorsal_en.png":
      raise ValueError("Unexpected brain figure path")
    if item["sha256"] not in (OLD,sha):
      raise ValueError("Original drawing changed; do not overwrite")
    ASSET.write_bytes(data) # ORIGINAL PNG BYTES UNMODIFIED. NO RE-RENDER OR NEW DRAWING.
    for obsolete in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
      item.pop(obsolete,None)
    item.update({
     "sha256":sha,"size":len(data),"author":AUTHOR,
     "license":"Public domain — historical figure (1878), Commons PD-Art",
     "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
     "sourceUrl":PAGE,"sourceImageUrl":URL,"sourceSha1":SOURCE_SHA1,
     "sourceSha256":[sha],"referenceUrls":REFS,
     "modifications":"None: unmodified, existing 1878 historical artwork in the published PNG source format",
     "scope":"Galeorhinus galeus / comparative dogfish dorsal brain anatomy, NOT Scoliodon sorrakowah or Rhizoprionodon acutus dissection",
     "historicTaxon":"Dogfish comparative shark brain, historically illustrated by Fritsch (1878)",
     "keyEn":"Historical DOGFISH comparison (NOT milk shark / Scoliodon). Shows olfactory expansions, forebrain, optic region, cerebellum and medulla, with original historical abbreviations and nerves. Use only for comparative anatomy, not as species-specific Scoliodon proof.",
     "keyTa":"இது 1878 ஆம் ஆண்டின் வரலாற்று நாய்ச்சுறா மூளைப் படம்; பாடத்திலுள்ள பால் சுறா (Rhizoprionodon acutus) இனத்தின் நேரடி உடற்கூறாய்வுப் படம் அன்று. மூளையின் பகுதிகளை ஒப்பிட்டு அறிய மட்டுமே பயன்படுத்தவும்.",
     "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
     "visualReview":"SOURCED_COMPARATIVE_HISTORICAL_PNG_PENDING_EXPERT_REVIEW",
     "sourceKind":"AUTHENTIC_HISTORICAL_PNG_NOT_GENERATED",
     "topicId":"u2-scoliodon","page":4,"sectionKey":"brain"
    })
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
      reader=csv.DictReader(f,delimiter="\t");cols=reader.fieldnames;rows=list(reader)
    matches=[row for row in rows if row["diagramId"]==ID]
    if len(matches)!=1:raise ValueError("Missing brain coverage record")
    matches[0]["author"]=AUTHOR
    matches[0]["referenceSources"]=" | ".join(REFS)
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
      writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
      writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
      "# Wave 7 — original published PNG intake, not synthetic artwork\n\n"
      f"Figure ID: {ID}\n\n"
      f"Author: {AUTHOR}\nSource file: {PAGE}\n"
      "Legal status: public-domain historical artwork (Commons PD-Art designation).\n"
      f"Original SHA-1: {SOURCE_SHA1}\nEmbedded PNG SHA-256: {sha}\n"
      f"Original dimensions: {img.width} × {img.height} pixels; {len(data)} bytes.\n"
      "MODIFICATIONS: NONE. Existing PNG bytes preserved verbatim; no SVG, procedural raster, generated image, drawn labels or AI art.\n\n"
      "ANATOMICAL LIMIT: This is a real historical DOGFISH study figure, NOT a verified "
      "Scoliodon sorrakowah / Rhizoprionodon acutus dissection. Its old abbreviations "
      "and cranial-nerve course are for comparative study only; label mapping must "
      "be checked by a human zoologist. The previous Wave 6 synthetic brain image "
      "was rejected by the user and is not the displayed asset.\n\n"
      "Expert anatomy/Tamil editorial acceptance and physical-device legibility "
      "PENDING. Do not release to production.\n",encoding="utf-8")
    print(f"PASS source-authentic original PNG: {len(data)} bytes, SHA256={sha}")
if __name__=="__main__":main()
