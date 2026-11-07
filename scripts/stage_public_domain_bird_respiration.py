#!/usr/bin/env python3
"""Convert L. Shyamal's public-domain avian respiration SVG to Android QA PNG.

Preserves the exact anatomy/labels and registers the converted PNG. Native
Android uses offline PNG artwork, NOT the SVG source or a webview.
"""
from hashlib import sha256
from io import BytesIO
import csv
import json
from pathlib import Path
from urllib.request import Request, urlopen
import subprocess

import cairosvg
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
TARGET=ASSETS/"pencil_plates/avian_respiration_en.png"
LEDGER=ROOT/"docs/figure-coverage.tsv"
DOC=ROOT/"docs/CHORDATA_AVIAN_RESPIRATION_SOURCE_QA.md"
PREVIEW=ROOT/"docs/qa-image-review/avian_respiration_review.png"
DIAGRAM="u5-flight-adaptations-avian-lung"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/f/f2/BirdRespiration.svg"
SOURCE_PAGE="https://commons.wikimedia.org/wiki/File:BirdRespiration.svg"
AUTHOR="L. Shyamal (2007; updated 2012), after R. McNeill Alexander; CHORDATA QA (raster rendering)"
LICENCE="Public domain — dedicated by L. Shyamal"

def fetch_svg():
    req=Request(SOURCE,headers={
        "User-Agent":"ChordataQAArtImport/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/",
        "Accept":"image/svg+xml",
    })
    with urlopen(req,timeout=45) as response:
        raw=response.read(120000)
    if not 25000<len(raw)<120000:
        raise ValueError("Source SVG size outside known range")
    low=raw.lower()
    if b"<svg" not in low[:3000] or any(term in low for term in [
        b"<!doctype",b"<script",b"javascript:",b"@import",b"<foreignobject"
    ]):
        raise ValueError("Untrusted or unsupported active SVG content")
    return raw

def main():
    raw=fetch_svg()
    # Wikimedia rendering source is SVG; the app receives only the PNG output.
    png=cairosvg.svg2png(bytestring=raw,output_width=2400)
    image=Image.open(BytesIO(png))
    image.load()
    if image.width<1200 or image.height<600:
        raise ValueError("SVG PNG conversion too small")
    # White background for legible offline reading on light and dark Android themes.
    if image.mode!="RGBA":
        image=image.convert("RGBA")
    out=Image.new("RGBA",image.size,"white")
    out.alpha_composite(image)
    TARGET.write_bytes(b"")
    out.convert("RGB").save(TARGET,"PNG",optimize=True)
    data=TARGET.read_bytes()
    digest=sha256(data).hexdigest()
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    smaller=out.convert("RGB")
    smaller.thumbnail((800,1100),Image.Resampling.LANCZOS)
    smaller.save(PREVIEW,"PNG",optimize=True)

    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    variants=[x for x in m["figures"] if x["diagramId"]==DIAGRAM and x["lang"]=="en"]
    assert len(variants)==1 and variants[0]["path"]=="pencil_plates/avian_respiration_en.png"
    e=variants[0]
    for k in ("svgMaster","svgSha256"):
        e.pop(k,None)
    e.update(
        author=AUTHOR,license=LICENCE,licenseUrl="https://creativecommons.org/publicdomain/mark/1.0/",
        sourceUrl=SOURCE_PAGE,sourceSha256=[sha256(raw).hexdigest()],
        modifications=("Original publicly released vector rendered as a 2400-pixel-wide "
                       "lossless PNG on white background; anatomy and labels unchanged; "
                       "source SVG is not embedded in the Android APK."),
        sha256=digest,size=len(data),
        keyEn=("Avian respiration: posterior air sacs, parabronchial lungs and anterior "
               "air sacs; fresh air traverses the parabronchi during both phases."),
        keyTa="பறவைகளின் நுரையீரல் மற்றும் காற்றுப்பைகள்; ஆங்கிலப் படக்குறியீடுகள் மட்டும்.",
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t")
        fields=reader.fieldnames
        rows=list(reader)
    match=[row for row in rows if row["diagramId"]==DIAGRAM]
    assert len(match)==1
    match[0]["author"]=AUTHOR
    match[0]["referenceSources"]=SOURCE_PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    DOC.write_text(
        "# CHORDATA — Avian respiration anatomical plate (QA)\n\n"
        "Diagram: "+DIAGRAM+"\n"
        "Original: "+SOURCE_PAGE+"\n"
        "Artist: L. Shyamal; based on R. McNeill Alexander; original artwork dedicated to public domain.\n"
        "Rendered PNG: "+TARGET.as_posix()+"\n"
        "SVG source SHA-256: "+sha256(raw).hexdigest()+"\n"
        "PNG SHA-256: "+digest+"\n"
        "Changes: rendered the vector at 2400px width, flattened white background and "
        "saved PNG; no anatomy/label edits, all existing Tamil variants retained.\n\n"
        "No independent scientific, Tamil or physical-device approval. 64 lesson slots unchanged.\n",
        encoding="utf-8")
    print("PASS: converted avian respiratory textbook diagram from CC/public-domain SVG to offline PNG")
    print("dimensions:",out.size,"SHA-256:",digest)
    print("HOLD: 0/64 independent anatomical and Tamil dual sign-offs; no production release")

if __name__=="__main__":
    main()
