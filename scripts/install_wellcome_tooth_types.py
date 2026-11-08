#!/usr/bin/env python3
"""Intake of the original Wellcome Tardieu four-type human dentition engraving.

A historical engraving replaces an original simplified computed teaching diagram.
No reproduction of the drawing is traced or redrawn. English/Tamil keys stay
in the app's metadata; licenses and review gates remain explicit.
"""
from pathlib import Path
from io import BytesIO
from time import sleep
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from PIL import Image
import csv
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
PNG=ASSETS/"pencil_plates/human_tooth_types.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_WELLCOME_DENTITION_ORIGINAL_QA.md"
ID="u5-dentition-tooth-types"
PAGE="https://commons.wikimedia.org/wiki/File:The_incisors,_canines,_small_and_large_molars_of_an_adult_hu_Wellcome_V0011998.jpg"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/e/e3/The_incisors%2C_canines%2C_small_and_large_molars_of_an_adult_hu_Wellcome_V0011998.jpg"
ALTERNATE="https://commons.wikimedia.org/wiki/Special:Redirect/file/The_incisors,_canines,_small_and_large_molars_of_an_adult_hu_Wellcome_V0011998.jpg"
OLD_SHA="00f31052fbc9bc5bba7a7a19d99c77d7dd8dea6ccef3748ac759b8ade2543708"
AUTHOR="A. Tardieu (historical engraving, as attributed by Wellcome Collection); Wellcome Collection (digitised image)"

def get_exact_original():
    errors=[]
    for i,url in enumerate((SOURCE, SOURCE+"?download=1", ALTERNATE)):
        request=Request(url,headers={
          "User-Agent":"CHORDATA-College-Zoology-Figure-QA/1.0 (https://github.com/rameshgascngl-create/Chordata; source-attribution)",
          "Referer":"https://commons.wikimedia.org/",
          "Accept":"image/jpeg,*/*"
        })
        try:
            with urlopen(request,timeout=95) as response:
                data=response.read(9_000_001)
            if not 2_000_000 < len(data) < 9_000_000:
                raise ValueError("Wrong archival JPEG byte length")
            im=Image.open(BytesIO(data))
            im.load()
            if im.format!="JPEG" or im.size!=(3540,2316):
                raise ValueError("Unexpected archival dimensions or format: "+str((im.format,im.size)))
            return data,im,url
        except (HTTPError,URLError,TimeoutError,OSError,ValueError) as error:
            errors.append(str(error))
        sleep(2+i*4)
    raise RuntimeError("No original full-resolution Wellcome engraving verified; installed artwork unchanged. "+"; ".join(errors))

def main():
    raw,source_image,retrieval_url=get_exact_original()
    current=json.loads(MANIFEST.read_text(encoding="utf-8"))
    items=[x for x in current["figures"] if x.get("diagramId")==ID]
    if len(items)!=1 or items[0]["lang"]!="shared" or items[0]["path"]!="pencil_plates/human_tooth_types.png":
        raise RuntimeError("Unexpected adult tooth-types placement")
    e=items[0]
    if e["sha256"]!=OLD_SHA:
        raise RuntimeError("Tooth-types asset changed independently; refusing overwrite")
    # Source image is JPEG: only decode and re-encode to RGB PNG.
    out=BytesIO()
    source_image.convert("RGB").save(out,format="PNG",optimize=True,compress_level=9)
    data=out.getvalue()
    if data[:8]!=bytes.fromhex("89504e470d0a1a0a"):
        raise RuntimeError("Invalid PNG encoding")
    new_sha=hashlib.sha256(data).hexdigest()
    PNG.write_bytes(data)
    for name in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        e.pop(name,None)
    e.update({
      "size":len(data),"sha256":new_sha,"author":AUTHOR,
      "license":"CC BY 4.0 — image from Wellcome Collection, historical A. Tardieu engraving",
      "licenseUrl":"https://creativecommons.org/licenses/by/4.0/",
      "sourceUrl":PAGE,"sourceImageUrl":SOURCE,
      "sourceSha1":hashlib.sha1(raw).hexdigest(),
      "sourceSha256":[hashlib.sha256(raw).hexdigest()],
      "sourceKind":"WELLCOME_TARDIEU_AUTHENTIC_ADULT_DENTITION_JPEG_TO_PNG",
      "sourceFormat":"JPEG","installedFormat":"PNG",
      "modifications":"Original 3540x2316 Wellcome engraving decoded from JPEG and encoded as lossless RGB PNG; no cropping, resizing, overlays, tracing, AI or anatomical redrawing.",
      "referenceUrl":PAGE,"referenceUrls":[PAGE,"https://wellcomecollection.org/works/yjyb4df5"],
      "keyEn":"Original A. Tardieu engraving of adult HUMAN teeth (not rabbit): A upper-jaw teeth, B lower-jaw teeth; letter a = incisors (cutting), b = canine (grasping/tearing), c = smaller molars or premolars (crushing), d = large molars (grinding). Historical French engraving labels are retained, with this separate English key. Tooth roots and crown shapes vary by position and jaw; no absolute fixed number of roots should be inferred.",
      "keyTa":"ஏ. டார்டியூவின் முதிர்ந்த மனிதரின் பற்களைக் காட்டும் வரலாற்று உடற்கூறியல் ஓவியம் (முயலின் பற்கள் அல்ல). A — மேல்தாடைப் பற்கள்; B — கீழ்த்தாடைப் பற்கள். a — வெட்டுப்பற்கள்; b — கோரைப்பல்; c — முன்கடைவாய்ப்பற்கள்; d — கடைவாய்ப்பற்கள். பற்களின் வெட்டுதல், பற்றுதல், நசுக்குதல், அரைத்தல் ஆகிய செயல்களை ஒப்பிடுக. பல் வேர்களின் எண்ணிக்கையும் வடிவமும் இடத்திற்கேற்ப மாறுபடும்.",
      "scope":"Authentic historical adult human dentition engraving, upper and lower teeth, four morphological classes. It does not depict rabbit dentition or rabbit peg teeth.",
      "visualReview":"AUTHENTIC_WELLCOME_TOOTH_PLATE_PENDING_EXPERT_REVIEW",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "topicId":"u5-dentition","page":1,"sectionKey":"tooth-types"
    })
    MANIFEST.write_text(json.dumps(current,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t")
        headers,rows=reader.fieldnames,list(reader)
    matches=[r for r in rows if r["diagramId"]==ID]
    if len(matches)!=1: raise RuntimeError("Tooth figure missing or duplicated in coverage ledger")
    matches[0]["author"]=AUTHOR
    matches[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=headers,delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
      "# CHORDATA — authentic A. Tardieu adult human dentition engraving\n\n"
      "Exact lesson: u5-dentition-tooth-types, Unit V, page 1, tooth-types.\n\n"
      "Original catalogue: Wellcome Collection, iconographic item V0011998.\n"
      "Commons file: "+PAGE+"\nOriginal image: "+retrieval_url+"\n"
      "Creator: A. Tardieu, as attributed in the Wellcome Collection record; photographic/digital attribution Wellcome Collection.\n"
      "Rights: Creative Commons Attribution 4.0. Creator, source and modifications must appear in the app's credits.\n"
      "Scope: Adult human teeth only, not rabbit teeth.\n"
      "Original JPEG resolution: 3540x2316; bytes: "+str(len(raw))+"; sha1: "+hashlib.sha1(raw).hexdigest()+"; sha256: "+hashlib.sha256(raw).hexdigest()+".\n"
      "Installed RGB PNG same dimensions: "+str(len(data))+" bytes; sha256: "+new_sha+".\n\n"
      "No crop or drawing was performed; JPEG was decoded to RGB and re-encoded as PNG. French original marks a,b,c,d and jaw rows A/B are interpreted with the separate English/Tamil source key.\n"
      "Independent anatomy, Tamil editorial and physical-device zoom reviews are PENDING. This is a QA candidate only; production release on HOLD.\n",
      encoding="utf-8"
    )
    print("PASS authentic Wellcome anatomical engraving integrated as PNG",len(data),new_sha)

if __name__=="__main__":main()
