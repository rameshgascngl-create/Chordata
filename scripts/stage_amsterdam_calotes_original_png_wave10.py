#!/usr/bin/env python3
"""Offline PNG intake from a public-domain historical *Agama versicolor* print.

NO artificial anatomy is drawn: faithful source-pixel TIFF -> PNG conversion.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from io import BytesIO
import hashlib,csv,json,subprocess
from PIL import Image,ImageFile
Image.MAX_IMAGE_PIXELS=60_000_000

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
ASSET=ASSETS/"pencil_plates/calotes_external_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_CALOTES_AMSTERDAM_ORIGINAL_PNG_WAVE10_QA.md"
ID="u4-calotes-external"
PAGE=("https://commons.wikimedia.org/wiki/File:Agama_versicolor_-_1700-1880_-_Print_-"
      "_Iconographia_Zoologica_-_Special_Collections_University_of_Amsterdam_-_UBA01_IZ12700035.tif")
SOURCE=("https://upload.wikimedia.org/wikipedia/commons/1/1e/Agama_versicolor_-_1700-1880_-_Print_-"
        "_Iconographia_Zoologica_-_Special_Collections_University_of_Amsterdam_-_UBA01_IZ12700035.tif")
COLLECTION="https://commons.wikimedia.org/wiki/Category:Calotes_s._str._in_Iconographia_Zoologica"
SOURCE_SHA1="145231082cf3be25f56571dd7c7aa33e84274195"
PREVIOUS_SHA="7164c9593591d1279f32c26ef6d0b86603937479d3643c470b71fae5de958fb8"
AUTHOR=("Unknown historical engraver; Iconographia Zoologica, University of Amsterdam "
        "Special Collections, print dated only between 1700 and 1880")

def main():
    req=Request(SOURCE,headers={
        "User-Agent":"ChordataAcademicFigureQA/1.0 (historical-public-domain-original)",
        "Referer":"https://commons.wikimedia.org/",
        "Accept":"image/tiff,application/octet-stream"})
    with urlopen(req,timeout=115) as res:
        raw=res.read(26_000_001)
    if len(raw)!=24745144:
        raise ValueError("Unknown TIFF original byte length "+str(len(raw)))
    source_sha1=hashlib.sha1(raw).hexdigest()
    if source_sha1!=SOURCE_SHA1:
        raise ValueError("Original Amsterdam print changed SHA-1: "+source_sha1)
    source_sha256=hashlib.sha256(raw).hexdigest()
    image=Image.open(BytesIO(raw));image.load()
    if image.format!="TIFF" or image.size!=(3253,2531):
        raise ValueError(f"Incorrect printed *Agama versicolor* plate format: {image.format}/{image.size}")
    ASSET.parent.mkdir(parents=True,exist_ok=True)
    # Keep every source pixel and original orientation. NO traced contours,
    # generated masks, backgrounds, labels, crops, retouches or resizing.
    rgb=image.convert("RGB")
    rgb.save(ASSET,format="PNG",compress_level=8,optimize=True)
    result=ASSET.read_bytes()
    if not result.startswith(bytes.fromhex("89504e470d0a1a0a")):
        raise ValueError("Converted image is not PNG")
    installed_sha256=hashlib.sha256(result).hexdigest()
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    found=[x for x in manifest["figures"] if x["diagramId"]==ID and x["lang"]=="en"]
    if len(found)!=1 or found[0]["path"]!="pencil_plates/calotes_external_en.png":
        raise ValueError("Incorrect Calotes external features chapter mapping")
    entry=found[0]
    if entry["sha256"] not in (PREVIOUS_SHA,installed_sha256):
        raise ValueError("Calotes figure changed externally; refusing overwrite")
    for k in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        entry.pop(k,None)
    entry.update({
      "size":len(result),"sha256":installed_sha256,
      "author":AUTHOR,
      "license":"Public domain original 18th–19th-century zoological print, faithful Amsterdam university scan",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "sourceUrl":PAGE,
      "sourceImageUrl":SOURCE,
      "sourceSha1":SOURCE_SHA1,
      "sourceSha256":[source_sha256],
      "sourceFormat":"TIFF",
      "installedFormat":"PNG",
      "sourceKind":"AUTHENTIC_AMSTERDAM_AGAMA_VERSICOLOR_TIFF_CONVERTED_PNG",
      "referenceUrls":[PAGE,COLLECTION,"https://reptile-database.reptarium.cz/species?genus=Calotes&species=versicolor"],
      "modifications":"Original print pixels preserved during TIFF-to-PNG conversion only; NO AI, vector, algorithmically drawn anatomy, crop, upscale or added leader labels",
      "scope":"Historical external specimen rendering *Agama versicolor* = *Calotes versicolor*; lateral perspective with visible body scales, nuchal crest, clawed digits and elongated curled tail; tail curl is an artistic pose, not anatomical loop",
      "keyEn":"Authentic historic print of Calotes versicolor, labelled Agama versicolor in the archive. Identify the elongated trunk, granular scales, pointed snout, exposed eye, dorsal and nuchal crest, four clawed limbs and long coiled tail. Tail curvature reflects the artist's composition, not a special anatomical organ. No internal anatomy is illustrated.",
      "keyTa":"பல்கலைக்கழக அரியநூல் தொகுப்பில் உள்ள வரலாற்று ஓணான் (*Calotes versicolor*) ஓவியம்; பழைய பெயர் *Agama versicolor*. நீண்ட உடல், செதில்கள், கூரிய முகப்பு, கண், முதுகுப்புற முள் வரிசை, நகங்களுள்ள நான்கு கால்கள், நீண்ட வால் ஆகியவற்றைக் காணலாம். ஓவியத்தில் வால் வளைந்திருக்கிறது; இது தனி உடற்கூறு அமைப்பு அன்று. உள்ளுறுப்புகள் காட்டப்படவில்லை.",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "visualReview":"SOURCED_HISTORICAL_PNG_PENDING_EXPERT_REVIEW",
      "topicId":"u4-calotes","page":1,"sectionKey":"external-features"
    })
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t");cols,rows=reader.fieldnames,list(reader)
    match=[x for x in rows if x["diagramId"]==ID]
    if len(match)!=1:raise ValueError("Calotes source coverage ID missing")
    match[0]["author"]=AUTHOR
    match[0]["referenceSources"]=" | ".join([PAGE,COLLECTION])
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
        "# Wave 10 — original Amsterdam Agama / Calotes versicolor scientific plate, stored PNG\n\n"
        f"Lesson: {ID}, Unit IV, page 1.\n\n"
        f"Source: {PAGE}\n"
        "Collection: Iconographia Zoologica, Special Collections, University of Amsterdam, catalogue UBA01 IZ12700035.\n"
        "Date range: 1700–1880. Engraver attribution not established (do not invent).\n"
        "Historical name: Agama versicolor. Current identification: Calotes versicolor.\n"
        "Rights: Commons PD-Art, original public-domain zoological print; no licence fees.\n"
        f"Original TIFF bytes: {len(raw)}; source SHA-1 {source_sha1}; source SHA-256 {source_sha256}.\n"
        f"Installed PNG: {rgb.width}x{rgb.height}, {len(result)} bytes, SHA-256 {installed_sha256}.\n"
        "No computer-generated, traced, drawn, stylised or upscaled anatomical illustration. "
        "Only format conversion from original historic TIFF to PNG, maintaining source pixels.\n\n"
        "Scientific scope: lateral external anatomy only. Note artist-curled tail; "
        "students must not mistake the curved pose for anatomical segmentation or a specialised organ. "
        "No stomach, skeletal system or internal anatomy are depicted. English/Tamil captions separate from original plate.\n\n"
        "Independent Zoology/Tamil reviews, phone-zoom and physical-device acceptance PENDING; production HOLD.\n",
        encoding="utf-8")
    print("PASS historic Agama versicolor external PNG",len(result),
          "source_sha1",source_sha1,"PNG_sha256",installed_sha256)

if __name__=="__main__":main()
