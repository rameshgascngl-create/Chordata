#!/usr/bin/env python3
"""Install an authentic 1909 frog metamorphosis PNG, without changing source pixels.

The 1909 life-cycle figure shows a typical frog; it is not labelled as a
universal life cycle for all amphibian orders. Scientific approval is pending.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import csv
import hashlib
import json
import subprocess
from time import sleep
from io import BytesIO
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
IMAGE=ASSETS/"pencil_plates/frog_metamorphosis.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_FROG_METAMORPHOSIS_1909_PNG_QA.md"
DIAGRAM_ID="u3-amphibia-classification-life-cycle"
PAGE="https://commons.wikimedia.org/wiki/File:The_How_and_Why_Library_-_How_a_frog_grows.png"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/6/63/The_How_and_Why_Library_-_How_a_frog_grows.png"
SOURCE_SHA1="cc105eba2138482f8d9024ba28e0f8bd09b96873"
OLD_SHA256="3394feff79971e0b57a9cb97a1a5bab45ff1ec03606b54a73cbbc57a7e626226"
AUTHOR="The How and Why Library (1909), text by Eleanor Stackhouse Atkinson; original figure illustrator not independently identified"

def fetch_source():
    urls=[
      SOURCE,
      "https://commons.wikimedia.org/wiki/Special:Redirect/file/The_How_and_Why_Library_-_How_a_frog_grows.png",
      SOURCE+"?download=1",
    ]
    problems=[]
    for i,url in enumerate(urls):
        request=Request(url,headers={
            "User-Agent":"CHORDATA-Zoology-Teaching-QA/1.0 (https://github.com/rameshgascngl-create/Chordata; historical-illustration)",
            "Referer":"https://commons.wikimedia.org/",
            "Accept":"image/png,application/octet-stream",
        })
        try:
            with urlopen(request,timeout=90) as response:
                raw=response.read(900001)
            sha1=hashlib.sha1(raw).hexdigest()
            if sha1==SOURCE_SHA1 and len(raw)==626684:
                return raw,url
            problems.append("Unverified bytes "+str(len(raw))+" sha1 "+sha1+" from "+url)
        except (HTTPError,URLError,TimeoutError,OSError) as error:
            problems.append(str(error)+" "+url)
        sleep(3+2*i)
    raise RuntimeError("Cannot verify original Commons artwork; leave app unchanged. "+"; ".join(problems))

def main():
    raw,verified_url=fetch_source()
    decoded=Image.open(BytesIO(raw))
    decoded.load()
    if decoded.format!="PNG" or decoded.size!=(1457,1897):
        raise RuntimeError("Source is not the exact 1457x1897 published PNG")
    if raw[:8]!=bytes.fromhex("89504e470d0a1a0a"):
        raise RuntimeError("Source missing PNG signature")

    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries=[x for x in manifest["figures"] if x.get("diagramId")==DIAGRAM_ID]
    if len(entries)!=1 or entries[0].get("lang")!="shared" or entries[0].get("path")!="pencil_plates/frog_metamorphosis.png":
        raise RuntimeError("Unexpected figure language or lesson mapping")
    entry=entries[0]
    new_sha256=hashlib.sha256(raw).hexdigest()
    if entry["sha256"] not in (OLD_SHA256,new_sha256):
        raise RuntimeError("Previous illustration independently modified; refuse overwrite")

    IMAGE.write_bytes(raw) # Install exact original source; no drawing, crop or upscale.
    for key in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        entry.pop(key,None)
    entry.update({
      "sha256":new_sha256,"size":len(raw),"author":AUTHOR,
      "license":"Public domain — figure originally published in 1909; Wikimedia Commons public-domain record",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "sourceUrl":PAGE,"sourceImageUrl":SOURCE,
      "sourceSha1":SOURCE_SHA1,"sourceSha256":[new_sha256],
      "sourceFormat":"PNG","installedFormat":"PNG",
      "sourceKind":"ORIGINAL_1909_HOW_AND_WHY_FROG_LIFE_CYCLE_PNG",
      "modifications":"No modifications; the original published PNG is stored byte-identically. English/Tamil explanations appear separately in lesson keys.",
      "referenceUrl":PAGE,
      "referenceUrls":[PAGE,"https://en.wikisource.org/wiki/Page:How_and_Why_Library_187.jpg"],
      "keyEn":"Original 1909 frog metamorphosis drawing (not to scale): 1 eggs attached to submerged vegetation; 2 and 2a hatchlings with external gills; 3 external gills no longer visible; 4 developed tadpole; 5 hindlimbs growing; 6 all four limbs visible; 7 tail being resorbed; 8 tailless adult frog. A typical frog example, NOT a universal pattern for all amphibians; source illustrator is unidentified.",
      "keyTa":"1909 ஆம் ஆண்டின் தவளை உருமாற்றப் படம் (அளவுப்படி வரையப்படவில்லை): 1 நீர்த்தாவரத்தில் ஒட்டிய முட்டைகள்; 2, 2a வெளிச்செவுள்களுடன் வெளிவந்த தலைப்பிரட்டைகள்; 3 வெளிச்செவுள்கள் மறையும் நிலை; 4 வளர்ந்த தலைப்பிரட்டை; 5 பின்னங்கால்கள் வளர்தல்; 6 நான்கு கால்களும் தோன்றுதல்; 7 வால் படிப்படியாகச் சுருங்குதல்; 8 வாலற்ற முதிர்ந்த தவளை. இது தவளையின் பொதுவான வளர்ச்சி முறை மட்டுமே; எல்லா இருவாழ்விகளுக்கும் பொருந்தாது.",
      "scope":"Published historical frog metamorphosis artwork, stages 1–8 with 2a; illustrative anuran development, not a universal Amphibia life history.",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "visualReview":"ORIGINAL_1909_PUBLISHED_FROG_LIFECYCLE_PENDING_EXPERT_REVIEW",
      "topicId":"u3-amphibia-classification","page":3,"sectionKey":"reproduction-ecology",
    })
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t")
        columns,rows=reader.fieldnames,list(reader)
    match=[row for row in rows if row["diagramId"]==DIAGRAM_ID]
    if len(match)!=1:raise RuntimeError("Frog development ledger missing/duplicated")
    match[0]["author"]=AUTHOR
    match[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=columns,delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    REPORT.write_text(
      "# CHORDATA — original 1909 frog metamorphosis drawing, PNG QA\n\n"
      "Slot: u3-amphibia-classification-life-cycle; Unit III page 3, reproduction-ecology.\n\n"
      "Published source: *The How and Why Library* (1909), stage illustration 'How a frog grows'.\n"
      "Book text attributed to Eleanor Stackhouse Atkinson; actual artwork illustrator is not established and is not invented.\n"
      "Commons file: "+PAGE+"\n"
      "Original asset: "+SOURCE+"\n"
      "Rights: Public domain (1909 publication; Commons public-domain record).\n"
      "Source SHA-1: "+SOURCE_SHA1+"\n"
      "Installed PNG: 1457x1897, "+str(len(raw))+" bytes, SHA-256 "+new_sha256+".\n"
      "The source PNG is installed byte-for-byte; no resizing, tracing, AI generation, edits or artificial labels.\n\n"
      "Scientific caveat: a typical frog, not all Amphibia. Original stages 1,2,2a,3,4,5,6,7,8 include external gills, hindlimbs before forelimbs and progressive tail resorption; egg positioning is a source-specific illustration, not universal.\n"
      "English labels inside the original are preserved; English and Tamil educational keys are separate from the image.\n"
      "Independent Zoology review, Tamil editorial decision, on-device visual zoom and final release approval remain PENDING. No production merge.\n",
      encoding="utf-8"
    )
    print("PASS exact original historical frog PNG",len(raw),new_sha256,verified_url)
if __name__=="__main__":main()
