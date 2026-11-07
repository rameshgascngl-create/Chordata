#!/usr/bin/env python3
"""Replace synthetic pigeon external diagram with Keulemans's 1873 published illustration.

The source is an actual public-domain zoological plate (JPEG); no anatomy is drawn,
generated, vectorised or upscaled. Only lossless export to app-required PNG.
"""
import csv, hashlib, json, subprocess
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
DEST=ASSETS/"pencil_plates/pigeon_external_anatomy_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_KEULEMANS_1873_ROCK_PIGEON_PNG_QA.md"
ID="u5-columba-external"
PAGE="https://commons.wikimedia.org/wiki/File:Columba_livia_1873.jpg"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/6/62/Columba_livia_1873.jpg"
BOOK="https://archive.org/details/onzevogelsinhuis02schl"
AUTHOR="John Gerrard Keulemans (1842–1912); original Columba livia zoological plate (1873)"
ORIGINAL_SHA1="d40aa5574cd7a2808cd3701c4bbc9c348df1b77a"
PREVIOUS_SHA256="a56801b61bff236a0f0270e6c5df28c32fcbc035b767b921aa4457605f65e367"

def main():
  raw=None
  req=Request(SOURCE,headers={
   "User-Agent":"CHORDATA-Academic-Source-Verification/1.0 (https://github.com/rameshgascngl-create/Chordata)",
   "Referer":"https://commons.wikimedia.org/",
   "Accept":"image/jpeg"
  })
  with urlopen(req,timeout=80) as response:
    raw=response.read(2_000_001)
  source_sha1=hashlib.sha1(raw).hexdigest()
  if source_sha1!=ORIGINAL_SHA1:
    raise ValueError("Original Keulemans published scan differs from Commons-verified SHA-1: "+source_sha1)
  if len(raw)!=683321:
    raise ValueError("Unexpected original JPEG size: "+str(len(raw)))
  original=Image.open(BytesIO(raw));original.load()
  if original.format!="JPEG" or original.size!=(2726,2029):
    raise ValueError("Expected original 2726x2029 JPEG, obtained "+str(original.size))
  source_sha256=hashlib.sha256(raw).hexdigest()
  rgba=original.convert("RGB")
  # File-format conversion only. Preserve original pixels and dimensions,
  # without drawing, labelling, filtering, enhancement, cropping or resizing.
  DEST.parent.mkdir(parents=True,exist_ok=True)
  rgba.save(DEST,format="PNG",optimize=True)
  final=DEST.read_bytes()
  if not final.startswith(bytes.fromhex("89504e470d0a1a0a")) or len(final)<250000:
    raise ValueError("Source PNG conversion invalid")
  png_sha256=hashlib.sha256(final).hexdigest()
  manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
  found=[x for x in manifest["figures"] if x["diagramId"]==ID and x["lang"]=="en"]
  if len(found)!=1 or found[0]["path"]!="pencil_plates/pigeon_external_anatomy_en.png":
    raise ValueError("Wrong rock pigeon lesson figure mapping")
  fig=found[0]
  if fig["sha256"] not in (PREVIOUS_SHA256,png_sha256):
    raise ValueError("Refusing to replace independently modified Columba figure")
  for k in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
    fig.pop(k,None)
  fig.update(
    sha256=png_sha256,size=len(final),author=AUTHOR,
    license="Public domain historical original (1873; artist died 1912), faithful original scan",
    licenseUrl="https://creativecommons.org/publicdomain/mark/1.0/",
    sourceUrl=PAGE,sourceImageUrl=SOURCE,sourceSha1=source_sha1,
    sourceSha256=[source_sha256],sourceFormat="JPEG",installedFormat="PNG",
    referenceUrls=[PAGE,BOOK],
    modifications=("Faithful pixel-preserving JPEG-to-PNG file-format conversion ONLY; "
      "no artwork newly drawn, AI-generated, upscaled, traced, cropped, sharpened or annotated."),
    sourceKind="AUTHENTIC_1873_ROCK_PIGEON_ZOOLOGICAL_PLATE_CONVERTED_TO_PNG",
    reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
    visualReview="SOURCED_HISTORICAL_PNG_PENDING_EXPERT_REVIEW",
    scope=("Original natural-history exterior illustration of Columba livia, "
      "NOT an invasive dissection or modern arrow-labelled anatomical plate; "
      "some toe geometry is partly obscured by the rocky perch."),
    keyEn=("Historic Columba livia (rock pigeon): eye, bill, cere, "
      "contour-feathered head and neck, folded wing with coverts and flight feathers, "
      "tail rectrices, and visible toes. The image is a natural-history plate, "
      "not a schematic labelled dissection; fine feet/toe detail partly obscured."),
    keyTa=("1873 ஆம் ஆண்டில் வெளியான மாடப்புறா (Columba livia) ஓவியம்: "
      "கண், அலகு, அலகின் அடிப்பகுதியிலுள்ள மெழுகுப்படலம், தலை மற்றும் கழுத்தின் "
      "மூடிறகுகள், இறக்கை மூடிறகுகளும் பறத்திறகுகளும், வால் இறகுகள் "
      "மற்றும் காணக்கூடிய கால்விரல்கள். பாறையால் சில கால்விரல்கள் மறைக்கப்பட்டுள்ளன. "
      "இது வரலாற்றுச் சூழல் கொண்ட புறத்தோற்றப் படம்; குறியீட்டு உடற்கூறியல் வரைபடம் அன்று."),
    topicId="u5-columba",page=1,sectionKey="external-features"
  )
  MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  with LEDGER.open(newline="",encoding="utf-8") as f:
    reader=csv.DictReader(f,delimiter="\t");fields,rows=reader.fieldnames,list(reader)
  matching=[x for x in rows if x["diagramId"]==ID]
  if len(matching)!=1:raise ValueError("Unregistered Columba morphology slot")
  matching[0]["author"]=AUTHOR
  matching[0]["referenceSources"]=PAGE+" | "+BOOK
  with LEDGER.open("w",newline="",encoding="utf-8") as f:
    writer=csv.DictWriter(f,fieldnames=fields,delimiter="\t")
    writer.writeheader();writer.writerows(rows)
  subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
  REPORT.write_text(
    "# Original 1873 Columba livia historical study plate — Wave 8\n\n"
    f"Registry: {ID} (Unit V, page 1, external features)\n\n"
    f"Original creator: {AUTHOR}\n"
    f"Original primary source: Keulemans, Onze vogels in huis en tuin (1873), {BOOK}\n"
    f"Source image page: {PAGE}\n"
    f"Original source bytes (JPEG): {len(raw)}; {original.width} x {original.height} pixels\n"
    f"Source SHA-1: {source_sha1}\nSource SHA-256: {source_sha256}\n"
    f"Installed PNG SHA-256: {png_sha256}\nInstalled PNG bytes: {len(final)}\n\n"
    "Rights: public domain — author died 1912, published 1873. "
    "Creative Commons PD mark as described on the exact Commons file page.\n\n"
    "Modifications: JPEG-to-PNG lossless storage conversion, source pixels unchanged "
    "in the decoded RGB sample. No synthetic anatomy, no vector drawing, no AI "
    "artwork, no crop, no resampling, no text overlays.\n\n"
    "Pedagogical limit: this is genuine natural-history exterior artwork of "
    "the rock dove, not a modern numbered anatomical line drawing. "
    "Some hind-toe detail is partly hidden by the perch. The caption explains the "
    "visible features but must not claim that every feature has a leader line.\n\n"
    "Independent Zoology/Tamil review, 100/200% phone-scale inspection, "
    "and physical-device acceptance PENDING. Production release HOLD.\n",
    encoding="utf-8"
  )
  print("PASS: ORIGINAL 1873 ROCK DOVE PNG",len(final),
    "bytes, installed sha256",png_sha256,
    "source JPEG sha256",source_sha256)
if __name__=="__main__":main()
