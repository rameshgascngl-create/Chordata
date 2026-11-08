#!/usr/bin/env python3
"""Source-authenticated Fritsch 1878 dogfish brain -> comparative QA plate.

Retains every source anatomy pixel at native 500x941 resolution. Only adds a
separate English contextual panel to satisfy the 1200px app asset contract.
This is NOT represented as an exact-species Scoliodon dissection.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from io import BytesIO
import csv
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
ASSET=ASSETS/"pencil_plates/shark_brain_dorsal_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_AUTHENTIC_FRITSCH_DOGFISH_BRAIN_QA.md"
ID="u2-scoliodon-brain-labelled"
PAGE="https://commons.wikimedia.org/wiki/File:Fritsch_dogfish_shark_brain.png"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/9/99/Fritsch_dogfish_shark_brain.png"
EXPECTED_SHA1="3ccf7de9b4ea765cb606d12f3996f08ca68738ad"
PREVIOUS_SHA256="49d7897c2fe5e413bd49ae6f36ceccc798beca1dc3631be233eb94a72ac7201a"
AUTHOR="Gustav Theodor Fritsch (1838-1927), historical dogfish brain plate (1878); CHORDATA QA contextual panel only"

def label_font(size, bold=False):
    candidates=[
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in candidates:
        if Path(p).exists():return ImageFont.truetype(p,size)
    raise RuntimeError("Missing readable font for comparative QA caption panel")

def main():
    req=Request(SOURCE,headers={"User-Agent":"ChordataNativeAcademicQA/1.0 (historic-original-public-domain)","Accept":"image/png"})
    with urlopen(req, timeout=110) as response:
        raw=response.read(1800000)
    sha1=hashlib.sha1(raw).hexdigest()
    if len(raw)!=1414869 or sha1!=EXPECTED_SHA1:
        raise RuntimeError("Fritsch historical PNG changed: source size/SHA-1 mismatch "+str(len(raw))+"/"+sha1)
    img=Image.open(BytesIO(raw));img.load()
    if img.format!="PNG" or img.size!=(500,941):
        raise RuntimeError(f"Fritsch original format/dimensions invalid {img.format} {img.size}")
    original=img.convert("RGB")
    # Original anatomy is pasted 1:1; never scale, trace, regenerate or annotate it.
    plate=Image.new("RGB",(1420,1010),"#fafaf7")
    plate.paste(original,(40,35))
    d=ImageDraw.Draw(plate)
    ink="#233145"; secondary="#475567"; accent="#375477"
    x=605
    d.line((572,50,572,948),fill="#b7b9b8",width=3)
    d.text((x,75),"DOGFISH BRAIN",font=label_font(44,True),fill=ink)
    d.text((x,142),"DORSAL VIEW - HISTORICAL PLATE",font=label_font(25,True),fill=ink)
    d.line((x,192,1360,192),fill=accent,width=3)
    d.text((x,220),"Original: Gustav T. Fritsch (1878)",font=label_font(25),fill=ink)
    d.text((x,260),"Public-domain anatomical drawing",font=label_font(24),fill=secondary)
    d.text((x,325),"COMPARATIVE ELASMOBRANCH STUDY",font=label_font(24,True),fill=accent)
    lines=[
      "A historic dogfish drawing; NOT a",
      "species-verified Scoliodon specimen.",
      "",
      "Observe the original markings for:",
      "  Olfactory bulbs and tracts",
      "  Cerebral hemispheres",
      "  Optic region",
      "  Cerebellum",
      "  Medulla and cranial nerves",
      "",
      "Refer to the lesson key for context.",
      "Avoid inventing any hidden structures.",
    ]
    y=374
    for ln in lines:
        if ln:d.text((x,y),ln,font=label_font(25),fill=ink)
        y+=43 if ln else 19
    d.line((x,868,1360,868),fill="#b7b9b8",width=2)
    d.text((x,883),"Original 500 x 941 pixels; no enlargement",font=label_font(21),fill=secondary)
    d.text((x,922),"Scientific and Tamil reviews: PENDING",font=label_font(21,True),fill="#8d423c")
    ASSET.parent.mkdir(parents=True,exist_ok=True)
    plate.save(ASSET,format="PNG",optimize=True,compress_level=8)
    result=ASSET.read_bytes()
    installed_sha=hashlib.sha256(result).hexdigest()
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    found=[x for x in manifest["figures"] if x["diagramId"]==ID and x["lang"]=="en"]
    if len(found)!=1 or found[0]["path"]!="pencil_plates/shark_brain_dorsal_en.png":
        raise RuntimeError("Wrong Scoliodon lesson mapping")
    entry=found[0]
    if entry["sha256"] not in (PREVIOUS_SHA256,installed_sha):
        raise RuntimeError("The old shark brain was independently edited; refusing overwrite")
    for k in ("svgMaster","svgSha256"):
        entry.pop(k,None)
    entry.update({
      "size":len(result),"sha256":installed_sha,"author":AUTHOR,
      "license":"Public domain historical anatomical original (1878); independent QA typography panel",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "sourceUrl":PAGE,"sourceImageUrl":SOURCE,"sourceSha1":EXPECTED_SHA1,
      "sourceSha256":[hashlib.sha256(raw).hexdigest()],
      "sourceKind":"FRITSCH_1878_AUTHENTIC_COMPARATIVE_DOGFISH_BRAIN_PNG",
      "sourceFormat":"PNG","installedFormat":"PNG",
      "referenceUrls":[PAGE,"https://www.ncbi.nlm.nih.gov/pubmed/22836597"],
      "modifications":"Original 500x941 image retained at native pixel dimensions on 1420x1010 canvas; English source-context typography in separate panel only; no resizing, anatomical tracing, image generation or leader lines",
      "scope":"Historical dorsal dogfish brain used only as a comparative elasmobranch reference; original species not independently verified as Scoliodon; neither the plate nor proportions is a Scoliodon specimen claim.",
      "keyEn":"Historical 1878 dorsal dogfish brain illustration by Gustav Fritsch, NOT verified to depict Scoliodon. Interpret original markings for olfactory bulbs and tracts, cerebral hemispheres, optic areas, cerebellum, medulla and associated cranial nerves with a vetted comparative atlas. Original art retained at its native 500x941 pixels; verify taxon and abbreviations independently.",
      "keyTa":"குஸ்தாவ் ஃபிரிட்ஷ் 1878-இல் வெளியிட்ட சுறாவகை மூளையின் மேற்புற உடற்கூறியல் ஓவியம். இது ஸ்கோலியோடான் இனத்திற்குரிய மாதிரிப் படம் என உறுதிப்படுத்தப்படவில்லை. மணநுகர்வுக் குமிழ்கள், பெருமூளை, பார்வை மடல்கள், சிறுமூளை, முகுளம் மற்றும் மூளை நரம்புகளை ஒப்பீட்டு உடற்கூறியல் நூலுடன் சரிபார்க்கவும். மூலப் படத்தின் வடிவமும் அளவும் மாற்றப்படவில்லை.",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "visualReview":"AUTHENTIC_1878_COMPARATIVE_PLATE_PENDING_TAXON_AND_ANATOMY_APPROVAL",
      "artworkDisposition":"AUTHENTIC_ARCHIVAL_SOURCE_CANDIDATE_NOT_SPECIES_SPECIFIC",
      "reviewerNote":"The earlier computer-drawn shark brain was rejected. Replaced with authentic 1878 Fritsch art; source species and structure labels require independent checks. No approval, and no exact-Scoliodon claim.",
      "topicId":"u2-scoliodon","page":4,"sectionKey":"brain"
    })
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t");cols,rows=reader.fieldnames,list(reader)
    matching=[r for r in rows if r["diagramId"]==ID]
    if len(matching)!=1:raise RuntimeError("Scoliodon brain ledger missing")
    matching[0]["author"]=AUTHOR
    matching[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
        "# CHORDATA — authentic dogfish brain, comparative plate in Scoliodon unit\n\n"
        "Lesson: u2-scoliodon-brain-labelled (Unit II, page 4, brain).\n\n"
        "Source: "+PAGE+"\n"
        "Historical artist: Gustav Theodor Fritsch (1838-1927); published 1878.\n"
        "Public domain, faithfully digitised via Wikimedia Commons.\n"
        "Original PNG 500x941, 1414869 bytes; SHA-1 "+sha1+"; SHA-256 "+hashlib.sha256(raw).hexdigest()+".\n"
        "App PNG 1420x1010, "+str(len(result))+" bytes; SHA-256 "+installed_sha+".\n\n"
        "NO anatomy pixels have been altered, rescaled, traced or generated. The 500x941 source is displayed at native pixel size on a white canvas with separate English explanatory text to satisfy the app's 1200px minimum width. No artificial leader lines are added.\n\n"
        "CAUTION: This is dogfish comparative anatomy, not a confirmed Scoliodon dissection. The Commons category refers to a galeorhinid dogfish; the original source species and all structure labels require independent zoological verification. The learning objective is comparative brain organisation only; do not claim species-specific proportions.\n\n"
        "Human scientific approval PENDING; Tamil review PENDING; actual-device zoom PENDING. Production HOLD.\n",encoding="utf-8")
    print("PASS source-authenticated 1878 Fritsch dogfish comparison",len(result),installed_sha)

if __name__=="__main__":main()
