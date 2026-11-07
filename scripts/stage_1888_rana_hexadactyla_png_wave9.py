#!/usr/bin/env python3
"""Stage a real 1888 Madras zoological plate as PNG, with no generated anatomy."""
from pathlib import Path
from urllib.request import Request,urlopen
from io import BytesIO
import hashlib,json,csv,subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/"app/src/main/assets/pencil_plates/rana_external_en.png"
MANIFEST=ROOT/"app/src/main/assets/pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_RANA_1888_ORIGINAL_PNG_WAVE9_QA.md"
ID="u3-rana-external"
SOURCE=("https://upload.wikimedia.org/wikipedia/commons/8/8a/"
  "Catalogue_of_the_Batrachia_Salientia_and_Apoda_%28frogs%2C_toads%2C_and_c%C2%BFcilians%29"
  "_of_southern_India_%281888%29_%2820389957728%29.jpg")
PAGE=("https://commons.wikimedia.org/wiki/File:"
  "Catalogue_of_the_Batrachia_Salientia_and_Apoda_(frogs,_toads,_and_c%C2%BFcilians)"
  "_of_southern_India_(1888)_(20389957728).jpg")
BOOK="https://www.biodiversitylibrary.org/bibliography/9107"
TAXON="https://amphibiansoftheworld.amnh.org/Amphibia/Anura/Dicroglossidae/Dicroglossinae/Phrynoderma/Phrynoderma-hexadactylum"
SOURCE_SHA1="cfd4ad24cf279b08f99b1552892e5499fe5d99d5"
PREVIOUS="e229ab4b357e88208145c3b91ab0426b4de203455e716e39d32905ea917d303b"
AUTHOR=("Edgar Thurston (1888, editor and publisher of the Madras catalogue); "
        "original Plate III lithograph, individual lithographer not securely identified")

def main():
    req=Request(SOURCE,headers={
        "User-Agent":"ChordataUniversityFigureQA/1.0 (source-authentic historic illustration)",
        "Referer":"https://commons.wikimedia.org/",
        "Accept":"image/jpeg"})
    with urlopen(req,timeout=85) as response:
        original=response.read(2_000_001)
    if len(original)!=928641:
        raise ValueError(f"Unexpected original JPEG byte length {len(original)}")
    sha1=hashlib.sha1(original).hexdigest()
    if sha1!=SOURCE_SHA1:
        raise ValueError(f"Wikimedia historical figure SHA-1 mismatch {sha1}")
    photo=Image.open(BytesIO(original));photo.load()
    if photo.format!="JPEG" or photo.size!=(2020,3296):
        raise ValueError(f"Unrecognised historical plate format/dimensions: {photo.format}/{photo.size}")
    source_sha256=hashlib.sha256(original).hexdigest()
    # Pixel-preserving file-format conversion only, no anatomical redraw, no
    # generated SVG/vector, no added arrows, crop, resampling or upscaling.
    ASSET.parent.mkdir(parents=True,exist_ok=True)
    photo.convert("RGB").save(ASSET,format="PNG",optimize=True)
    installed=ASSET.read_bytes()
    png_sha256=hashlib.sha256(installed).hexdigest()
    if not installed.startswith(bytes.fromhex("89504e470d0a1a0a")):
        raise ValueError("Converted output is not a PNG")
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    matches=[x for x in manifest["figures"] if x["diagramId"]==ID and x["lang"]=="en"]
    if len(matches)!=1 or matches[0]["path"]!="pencil_plates/rana_external_en.png":
        raise ValueError("Wrong Rana green pond frog illustration slot")
    entry=matches[0]
    if entry["sha256"] not in (PREVIOUS,png_sha256):
        raise ValueError("Original slot changed by another reviewer; refuse overwrite")
    for outdated in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        entry.pop(outdated,None)
    entry.update({
      "author":AUTHOR,
      "size":len(installed),
      "sha256":png_sha256,
      "license":"Public domain historical Madras lithograph (1888), faithful scanned original; BHL marks book NOT_IN_COPYRIGHT",
      "licenseUrl":BOOK,
      "sourceUrl":PAGE,
      "sourceImageUrl":SOURCE,
      "sourceSha1":SOURCE_SHA1,
      "sourceSha256":[source_sha256],
      "sourceFormat":"JPEG",
      "installedFormat":"PNG",
      "sourceKind":"AUTHENTIC_1888_MADRAS_RANA_HEXADACTYLA_PLATE_PNG",
      "referenceUrls":[PAGE,BOOK,TAXON],
      "modifications":"Only pixel-preserving JPEG-to-PNG file-format conversion; no artwork newly drawn, AI generated, cropped, labelled, recoloured, traced or upscaled",
      "scope":"Exact green pond frog type-study species, 1888 Plate III Rana hexadactyla (currently Phrynoderma hexadactylum); dorsal external morphology only, not a labelled ventral dissection",
      "keyEn":"Original 1888 Madras Plate III of Rana hexadactyla, now Phrynoderma hexadactylum. Dorsal view of head and trunk, paired protruding eyes, forelimbs with unwebbed fingers, powerful hindlimbs and broad webbed hind feet. This historical plate has NO modern anatomical leader lines; mouth floor and ventral features are not shown.",
      "keyTa":"1888 ஆம் ஆண்டின் சென்னை வெளியீட்டில் இடம் பெற்ற ரானா ஹெக்சாடாக்டைலா (தற்போதைய பெயர்: ப்ரைனோடெர்மா ஹெக்சாடாக்டைலம்) இனத்தின் அசல் விளக்கப்படம். முதுகுப்புறத் தோற்றத்தில் தலை, உடல், கண்கள், வலிமையான பின்னங்கால்கள் மற்றும் வலைச்சவ்வுள்ள பின்னங்கால் விரல்கள் காட்டப்பட்டுள்ளன. இது குறியீட்டுக் கோடுகள் சேர்க்கப்படாத வரலாற்று ஓவியம்; வயிற்றுப்புற உள்ளமைப்பு காட்டப்படவில்லை.",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "visualReview":"SOURCED_HISTORICAL_PNG_PENDING_EXPERT_REVIEW",
      "topicId":"u3-rana",
      "page":1,
      "sectionKey":"external-features"
    })
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t")
        cols,rows=reader.fieldnames,list(reader)
    matching=[x for x in rows if x["diagramId"]==ID]
    if len(matching)!=1:raise ValueError("Unexpected Rana coverage ledger state")
    matching[0]["author"]=AUTHOR
    matching[0]["referenceSources"]=" | ".join([PAGE,BOOK,TAXON])
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
       "# Wave 9 — actual original Rana hexadactyla 1888 plate in PNG format\n\n"
       f"Lesson: {ID} | Unit III, page 1, external morphology.\n\n"
       f"Published by: {AUTHOR}\n"
       f"Original work: Edgar Thurston, Catalogue of Batrachia Salientia and Apoda of Southern India, Madras: Government Press, 1888, Plate III.\n"
       f"Wikimedia figure: {PAGE}\nOriginal book record: {BOOK}\n"
       f"Modern accepted taxon reference: {TAXON}\n\n"
       "Actual name printed on Plate III: Rana hexadactyla (historic usage); modern accepted name: Phrynoderma hexadactylum (Lesson, 1834). NOT Rana temporaria, Rana tigrina or Hoplobatrachus tigerinus.\n\n"
       f"Rights: 1888 illustration is public domain; BHL reports NOT_IN_COPYRIGHT; see {BOOK}.\n"
       f"Original JPEG: {len(original)} bytes, 2020 x 3296, SHA-1 {sha1}, SHA-256 {source_sha256}.\n"
       f"Embedded PNG: {len(installed)} bytes, same source dimensions, SHA-256 {png_sha256}.\n\n"
       "NO new drawing or generated artwork. Converted original published source to PNG using lossless pixel-preserving storage; no crop, upscale, artificial leader lines or anatomical enhancement.\n\n"
       "Pedagogical scope: clearly shows dorsal body contour, extended forefeet and the webbed hind feet; NOT a side or ventral anatomical plate and no modern labels. User requested authentic published art as PNG. The plate is a provisional figure for human acceptance, not a scientific-labelled line-drawing sign-off.\n\n"
       "Independent Zoology, Tamil editorial review, phone-scale inspection and physical-device acceptance are PENDING. Production release HOLD.\n",
       encoding="utf-8")
    print("PASS authentic 1888 green pond frog historical plate",
          "source-sha1",sha1,"source-sha256",source_sha256,
          "PNG-bytes",len(installed),"PNG-sha256",png_sha256)

if __name__=="__main__":
    main()
