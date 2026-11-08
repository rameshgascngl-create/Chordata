#!/usr/bin/env python3
"""Install original public-domain 1874 Indian-snake venom apparatus illustration.

Original illustration is Edward Nicholson's plate III (BHL page 4390486).
The 2428x3906 source scan is decoded to RGB and saved as PNG with neither
resizing nor traced/generated anatomy. Independent review is not asserted.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from io import BytesIO
from time import sleep
from PIL import Image
import csv,hashlib,json,subprocess

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
ASSET=ASSETS/"pencil_plates/snake_venom_delivery_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_NICHOLSON_1874_COBRA_VENOM_PLATE_QA.md"
ID="u4-poison-apparatus-venom-apparatus"
PAGE="https://commons.wikimedia.org/wiki/File:Indian_snakes_(Plate_III)_BHL4390486.jpg"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/1/15/Indian_snakes_%28Plate_III%29_BHL4390486.jpg"
FALLBACK="https://commons.wikimedia.org/wiki/Special:Redirect/file/Indian_snakes_(Plate_III)_BHL4390486.jpg"
OLD_SHA="cb4ee6227f902267c5d625ea69f5c365f8a5e1700bd4471dc0d19d47670d164e"
AUTHOR="Edward Nicholson, Indian Snakes (1874), Plate III; original plate illustrator unidentified; Biodiversity Heritage Library scan"
def download():
    problems=[]
    for i,url in enumerate((SOURCE,SOURCE+"?download=1",FALLBACK)):
        req=Request(url,headers={
          "User-Agent":"CHORDATA-Zoology-Teaching-QA/1.0 (https://github.com/rameshgascngl-create/Chordata; publicly-credited-source)",
          "Referer":"https://commons.wikimedia.org/",
          "Accept":"image/jpeg,*/*"
        })
        try:
            with urlopen(req,timeout=95) as resp:
                raw=resp.read(1_500_001)
            if not 500_000<len(raw)<1_500_000:
                raise RuntimeError("Source file byte count not within 500KB–1.5MB")
            scan=Image.open(BytesIO(raw))
            scan.load()
            if scan.format!="JPEG" or scan.size!=(2428,3906):
                raise RuntimeError("Exact BHL source format/dimensions mismatch")
            return raw,scan
        except (HTTPError,URLError,TimeoutError,OSError,RuntimeError) as e:
            problems.append(url+" "+str(e))
        sleep(3+i*3)
    raise RuntimeError("Unable to verify original public-domain plate, no asset replaced: "+" | ".join(problems))
def main():
    raw,scan=download()
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    found=[x for x in manifest["figures"] if x.get("diagramId")==ID and x.get("lang")=="en"]
    if len(found)!=1 or found[0].get("path")!="pencil_plates/snake_venom_delivery_en.png":
        raise RuntimeError("Venom apparatus figure not mapped to the correct lesson")
    item=found[0]
    original_hash=hashlib.sha256(raw).hexdigest()
    b=BytesIO()
    scan.convert("RGB").save(b,format="PNG",optimize=True,compress_level=9)
    png=b.getvalue()
    installed=hashlib.sha256(png).hexdigest()
    if item.get("sha256") not in (OLD_SHA,installed):
        raise RuntimeError("Existing figure has independent modifications, refusing overwrite")
    ASSET.write_bytes(png)
    for k in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        item.pop(k,None)
    item.update({
      "size":len(png),"sha256":installed,"author":AUTHOR,
      "license":"Public domain original 1874 anatomical plate; BHL mechanical source scan",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "sourceUrl":PAGE,"sourceImageUrl":SOURCE,
      "sourceSha1":hashlib.sha1(raw).hexdigest(),"sourceSha256":[original_hash],
      "sourceFormat":"JPEG","installedFormat":"PNG",
      "sourceKind":"NICHOLSON_1874_AUTHENTIC_COBRA_VENOM_PLATE_PNG",
      "referenceUrls":[PAGE,"https://www.biodiversitylibrary.org/page/4390486","https://www.who.int/news-room/questions-and-answers/item/snakebite-envenoming"],
      "modifications":"Original 2428x3906 Biodiversity Heritage Library JPEG decoded to RGB and encoded as PNG; same source pixel dimensions, no cropping, tracing, AI-generated anatomy, stylisation, labels or upscaling.",
      "scope":"Historical Indian cobra (Naja-type) poison gland/jaw muscle anatomy and fang sections; includes a Daboia viper fang. Fang hinge movement is NOT shown and should not be inferred from the plate.",
      "keyEn":"Original Indian cobra and viper anatomical drawings, Nicholson (1874), Plate III: Fig. 1 opened cobra jaws; Fig. 2 superficial jaw muscles and poison gland; Fig. 3 deeper muscles after gland removal; Fig. 4 palate and pterygoid muscles; Fig. 5 skull base; Fig. 6 cobra poison fang with views and cross-section; Fig. 7 Daboia viper fang. Historical engraving: not a complete movement sequence for the hinged viper fang. Elapid fixed-front and viper hinged-front fang mechanics require additional verified instruction; do not infer current first-aid recommendations from historic art.",
      "keyTa":"எட்வர்டு நிக்கல்சனின் 1874 ஆம் ஆண்டு இந்தியப் பாம்புகளின் உடற்கூறியல் ஓவியம் (படத்தொகுப்பு III): படம் 1 நாகப்பாம்பின் திறந்த தாடை; படம் 2 மேலோட்டத் தாடைத் தசைகளும் நஞ்சுச் சுரப்பியும்; படம் 3 சுரப்பி அகற்றப்பட்ட ஆழ்தசைகள்; படம் 4 அண்ணம் மற்றும் தாடைத் தசைகள்; படம் 5 மண்டையோட்டின் அடிப்பகுதி; படம் 6 நாகப்பாம்பின் நஞ்சுப்பல் மற்றும் குறுக்குவெட்டுத் தோற்றம்; படம் 7 டபோயா விரியனின் நஞ்சுப்பல். விரியன் நஞ்சுப்பல் மடங்கும் இயக்கம் இவ்வோவியத்தில் காட்டப்படவில்லை. பழைய படத்தைக் கொண்டு தற்போதைய முதலுதவி முறைகளைத் தீர்மானிக்கக் கூடாது.",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "visualReview":"AUTHENTIC_NICHOLSON_1874_COBRA_VENOM_PLATE_PENDING_REVIEW",
      "topicId":"u4-poison-apparatus","page":1,"sectionKey":"venom-apparatus"
    })
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t")
        cols,rows=reader.fieldnames,list(reader)
    record=[r for r in rows if r["diagramId"]==ID]
    if len(record)!=1: raise RuntimeError("Missing or duplicated venom lesson coverage record")
    record[0]["author"]=AUTHOR
    record[0]["referenceSources"]=PAGE+" | https://www.biodiversitylibrary.org/page/4390486"
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
      "# CHORDATA — venom apparatus authentic 1874 Indian cobra illustration\n\n"
      "Slot: u4-poison-apparatus-venom-apparatus; Unit IV, page 1 (venom-apparatus).\n"
      "Publication: Edward Nicholson, Indian Snakes (1874), Plate III. Illustrator not independently identified.\n"
      "Biodiversity Heritage Library page: https://www.biodiversitylibrary.org/page/4390486\n"
      "Commons file: "+PAGE+"\n"
      "Source image: "+SOURCE+"\n"
      "Rights: public domain historical work, mechanically scanned by BHL, Commons PD Mark.\n"
      "Source JPEG: 2428x3906, "+str(len(raw))+" bytes, SHA-1 "+hashlib.sha1(raw).hexdigest()+", SHA-256 "+original_hash+".\n"
      "Installed PNG (same dimensions): "+str(len(png))+" bytes, SHA-256 "+installed+".\n"
      "No anatomical redraw, crop, resizing, AI or graphic embellishment. Original printed English notes and numbered figures are retained.\n"
      "Fig. 2 shows cobra poison gland; Fig. 6 cobra fang; Fig. 7 Daboia viper fang. The figure does NOT display the complete hinged-viper fang mechanism. Modern Indian first aid comes from separate clinical guidelines, not this historic image.\n\n"
      "Independent biological accuracy/legibility check, Tamil notes and physical-device zoom approval PENDING. Production HOLD.\n",encoding="utf-8")
    print("PASS source-authenticated Indian cobra venom apparatus JPEG-to-PNG",len(png),installed)
if __name__=="__main__":main()
