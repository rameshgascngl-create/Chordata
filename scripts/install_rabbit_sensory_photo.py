#!/usr/bin/env python3
"""Integrate an actual, credited domestic-rabbit specimen photo, not a pictogram.

One exact registered figure is replaced. The original PNG/SVG are archived
unchanged. The plate is provisionally useful for visible pinna, lateral eye,
and mystacial vibrissae; not an internal ear/eye anatomy diagram.
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import csv
import hashlib
import io
import json
import subprocess
import sys
import time

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
MANIFEST = ASSETS / "pencil_plates/manifest.json"
LEDGER = ROOT / "docs/figure-coverage.tsv"
OLD_ARCHIVE = ROOT / "docs/retired_noninstructional_png/rabbit_senses_en.png"
PROVENANCE = ROOT / "docs/qa-image-review/RABBIT_SENSE_ORGANS_PHOTOGRAPHIC_REPLACEMENT_20261112.json"
DIAGRAM = "u5-rabbit-sense-organs"
EXPECTED_OLD_SHA = "6f4a798edd974efc549163e09bb37727b49b26f77d507e50f9b6a4b628e2788f"
FILE = "Side view of the head of a pet rabbit in Brussels (DSCF0830).jpg"
SOURCE_PAGE = "https://commons.wikimedia.org/wiki/File:Side_view_of_the_head_of_a_pet_rabbit_in_Brussels_(DSCF0830).jpg"
LICENCE = "CC BY 4.0"
LICENCE_URL = "https://creativecommons.org/licenses/by/4.0/"
CREATOR = "Trougnouf (Benoit Brummer)"
USER_AGENT = "ChordataZoologyQA/1.0 (educational illustration source verification)"
sha256 = lambda b: hashlib.sha256(b).hexdigest()

def download(session, url, params=None):
    for attempt in range(7):
        resp = session.get(url, params=params, timeout=85)
        if resp.status_code in (429, 500, 502, 503, 504):
            print("Temporary upstream response", resp.status_code, "attempt", attempt + 1, flush=True)
            time.sleep(min(65, (attempt + 1) * 8))
            continue
        resp.raise_for_status()
        return resp
    raise RuntimeError("Source unavailable after retries: " + url)

def font(size, bold=False):
    family = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + family, size)

def wrapped(draw, xy, lines, fill="#334c52"):
    x,y=xy
    for line in lines:
        draw.text((x,y), line, font=font(29), fill=fill)
        y += 51

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
entries = [f for f in manifest["figures"] if f["diagramId"] == DIAGRAM]
assert len(entries) == 1 and entries[0]["lang"] == "en"
e = entries[0]
assert e["visualReview"] == "USER_REJECTED_REPLACEMENT_REQUIRED"
assert e["pedagogicStatus"].startswith("WITHHELD_")
old_file = ASSETS/e["path"]
old = old_file.read_bytes()
assert sha256(old) == EXPECTED_OLD_SHA == e["sha256"]
assert e["size"] == len(old)
assert e.get("svgMaster") and e.get("svgSha256")
svg_master = ROOT / e["svgMaster"]
assert svg_master.is_file() and sha256(svg_master.read_bytes()) == e["svgSha256"]
assert e["reviewStatus"].startswith("PROVISIONAL_")
old_metadata = {k:e.get(k) for k in ("author", "license", "sha256", "size",
                                     "visualReview", "svgMaster", "svgSha256")}

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json,image/*;q=0.9,*/*;q=0.5"})
params = {"action":"query","format":"json","prop":"imageinfo",
          "iiprop":"url|extmetadata|size","titles":"File:" + FILE}
api = download(session, "https://commons.wikimedia.org/w/api.php", params).json()
metadata = next(iter(api["query"]["pages"].values())).get("imageinfo")
assert metadata, "Source has no verified Commons image metadata"
metadata = metadata[0]
license_short = metadata["extmetadata"].get("LicenseShortName",{}).get("value","")
assert license_short.casefold() == LICENCE.casefold(), ("Unexpected source licence",license_short)
assert metadata.get("width") == 3667 and metadata.get("height") == 3231, "Source resolution changed"
remote = urlsplit(metadata["url"])
source_url = urlunsplit((remote.scheme,remote.netloc,remote.path,"",""))
assert source_url.startswith("https://upload.wikimedia.org/wikipedia/commons/")
source_bytes = download(session, source_url).content
assert source_bytes[:3] == bytes.fromhex("ffd8ff") and 2_500_000 < len(source_bytes) < 15_000_000
with Image.open(io.BytesIO(source_bytes)) as check:
    check.verify()
with Image.open(io.BytesIO(source_bytes)) as original:
    assert original.size == (3667,3231)
    photo = ImageOps.exif_transpose(original).convert("RGB")

# A photograph remains the entire scientific evidence. Only explanatory text
# and small numbered markers are overlaid; no anatomical structures invented.
W,H=2860,1710
panel=Image.new("RGB",(W,H),"#f7f5ec")
d=ImageDraw.Draw(panel)
d.text((65,30),"RABBIT SENSORY ORGANS — EXTERNAL MORPHOLOGY",
       font=font(46,True),fill="#163941")
photo=ImageOps.contain(photo,(1710,1445),Image.Resampling.LANCZOS)
assert photo.width >= 1500 and photo.height >= 1350
x=64+(1710-photo.width)//2
y=105+(1445-photo.height)//2
panel.paste(photo,(x,y))
d.rounded_rectangle((x-3,y-3,x+photo.width+3,y+photo.height+3),
                    radius=12,outline="#647b7f",width=4)
# The high-resolution source was visually reviewed before selecting these
# landmarks. Markers are offset from anatomy so eye/ear/whiskers remain visible.
# Positions are relative to source preview (1000x882), mapped to output photo.
def marker(n, frac_x, frac_y):
    cx = int(x + photo.width*frac_x)
    cy = int(y + photo.height*frac_y)
    r=39
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill="#12383f",outline="#fefdf7",width=5)
    label=str(n)
    bbox=d.textbbox((0,0),label,font=font(42,True))
    d.text((cx-(bbox[2]-bbox[0])/2,cy-(bbox[3]-bbox[1])/2-5),
           label,font=font(42,True),fill="white")
marker(1,.455,.38)   # pinna; numbered marker beside the raised outer ear
marker(2,.645,.48)   # lateral eye; marker is next to, not over, the eyeball
marker(3,.785,.71)   # facial vibrissae at the muzzle, not whisker roots
RX=1860
def card(y,number,title,lines):
    d.rounded_rectangle((RX,y,2800,y+365),radius=24,fill="#e7eeeb",outline="#b8cbc5",width=3)
    d.ellipse((RX+25,y+25,RX+99,y+99),fill="#12383f")
    d.text((RX+47,y+26),str(number),font=font(40,True),fill="white")
    d.text((RX+118,y+26),title,font=font(40,True),fill="#103941")
    wrapped(d,(RX+32,y+120),lines)
card(120,1,"PINNA",[
    "Movable external ear.",
    "Collects and directs sound;",
    "balance receptors lie in",
    "the inner ear, not the pinna."
])
card(514,2,"LATERAL EYE",[
    "Eye located on the side",
    "of the head supports a",
    "broad field of view.",
    "Internal eye not shown."
])
card(908,3,"VIBRISSAE",[
    "Facial tactile whiskers",
    "detect near-field contact.",
    "Follicles contain sensory",
    "nerve endings."
])
d.text((80,1608),"Real domestic rabbit specimen — external features only; not a dissected sensory system.",
       font=font(25,True),fill="#304a50")
d.text((80,1650),"Photo: Trougnouf (Benoit Brummer) | Wikimedia Commons | CC BY 4.0 | Cropped? NO; proportionally resized and labelled.",
       font=font(20),fill="#52666b")
out=io.BytesIO()
panel.save(out,format="PNG",optimize=True)
new=out.getvalue()
assert new[:8] == bytes.fromhex("89504e470d0a1a0a") and len(new) > 300000
assert sha256(new) != EXPECTED_OLD_SHA

OLD_ARCHIVE.parent.mkdir(parents=True,exist_ok=True)
if OLD_ARCHIVE.exists():
    assert sha256(OLD_ARCHIVE.read_bytes()) == EXPECTED_OLD_SHA, "Retired image archive collision"
else:
    OLD_ARCHIVE.write_bytes(old)
old_file.write_bytes(new)
e["retiredSchematicPng"] = str(OLD_ARCHIVE.relative_to(ROOT))
e["retiredSchematicSha256"] = EXPECTED_OLD_SHA
e["retiredSchematicSvg"] = e.pop("svgMaster")
e["retiredSchematicSvgSha256"] = e.pop("svgSha256")
e.update({
    "sha256":sha256(new),
    "size":len(new),
    "author":CREATOR+" (original photograph); CHORDATA QA (original educational labels)",
    "sourceUrl":SOURCE_PAGE,
    "sourceImageUrl":source_url,
    "sourceSha256":[sha256(source_bytes)],
    "license":LICENCE+" — captioned educational derivative with original attribution",
    "licenseUrl":LICENCE_URL,
    "sourceKind":"REAL_DOMESTIC_RABBIT_SPECIMEN_ANNOTATED_PNG",
    "sourceFormat":"JPEG",
    "installedFormat":"PNG",
    "modifications":"Proportional resizing of the complete unmodified photograph with numbered anatomical callouts and explanatory text on a new original canvas; no organ structures redrawn.",
    "keyEn":"External sensory features of a living domestic rabbit: 1 PINNA receives sound and can rotate; the vestibular apparatus for balance lies inside the inner ear and is NOT depicted. 2 LATERAL EYE provides a wide field of view. 3 MYSTACIAL VIBRISSAE are tactile whiskers, with mechanosensory receptors in the follicles. This is NOT a section through the eye or auditory/vestibular apparatus.",
    "keyTa":"வீட்டு முயலின் புற உணர்வு உறுப்புகள்: 1 PINNA — ஒலியைச் சேகரிக்கும் அசையும் வெளிச்செவி; சமநிலை உணர்விகள் உட்செவியில் உள்ளன; படத்தில் காட்டப்படவில்லை. 2 LATERAL EYE — அகன்ற பார்வைப் புலம் பெற உதவும் பக்கவாட்டுக் கண். 3 MYSTACIAL VIBRISSAE — தொடு உணர்விற்கான முக மீசை முடிகள்; முடிக்கால்களில் உணர்வு நரம்பு முடிவுகள் உள்ளன. உள் உறுப்புகளின் வெட்டுத்தோற்றம் இங்கு காட்டப்படவில்லை.",
    "scope":"Authentic external morphology of photographed domestic rabbit, with visible outer pinna, lateral eye and facial vibrissae only.",
    "visualReview":"SOURCED_REAL_RABBIT_SENSORY_PHOTO_QA_PROVISIONAL",
    "pedagogicStatus":"REPLACED_WITH_CC_LICENSED_RABBIT_SENSES_QA_PENDING_2026-11-12",
    "pedagogicReason":"The user-rejected symbolic icons are replaced by a photograph of the relevant living rabbit anatomy; no claim to depict internal eye/ear physiology.",
    "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
})
MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
with LEDGER.open(newline="",encoding="utf-8") as file:
    reader=csv.DictReader(file,delimiter="\t")
    cols=reader.fieldnames;rows=list(reader)
assert len(rows)==64 and cols
for row in rows:
    if row["diagramId"]==DIAGRAM:
        row["author"]=e["author"]
        row["referenceSources"]=SOURCE_PAGE
with LEDGER.open("w",newline="",encoding="utf-8") as file:
    writer=csv.DictWriter(file,fieldnames=cols,delimiter="\t")
    writer.writeheader();writer.writerows(rows)
PROVENANCE.parent.mkdir(parents=True,exist_ok=True)
PROVENANCE.write_text(json.dumps({
    "diagramId":DIAGRAM,
    "sourcePage":SOURCE_PAGE,
    "sourceUrl":source_url,
    "sourceAuthor":CREATOR,
    "license":license_short,
    "licenseUrl":LICENCE_URL,
    "originalJpegSha256":sha256(source_bytes),
    "originalJpegBytes":len(source_bytes),
    "displayPngPath":e["path"],
    "displayPngSha256":sha256(new),
    "displayPngBytes":len(new),
    "outputResolution":[W,H],
    "retiredPng":e["retiredSchematicPng"],
    "retiredPngSha256":EXPECTED_OLD_SHA,
    "retiredSvg":e["retiredSchematicSvg"],
    "retiredSvgSha256":e["retiredSchematicSvgSha256"],
    "modifications":e["modifications"],
    "independentScientificAcceptance":"PENDING",
    "independentTamilAcceptance":"PENDING"
},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
for cmd in (
    ["python3","scripts/write_figure_review_register.py"],
    ["python3","scripts/audit_figure_placement.py"],
    ["python3","scripts/audit_pencil_coverage.py"],
    ["python3","scripts/audit_coverage_report.py"],
    ["python3","scripts/audit_android_qa_contract.py"],
    ["python3","scripts/write_figure_review_register.py","--check"],
    ["python3","scripts/audit_built_apk_assets.py","--self-test"],
):
    subprocess.run(cmd,cwd=ROOT,check=True)
print("PASS: genuine photographed rabbit sensory teaching plate installed",sha256(new),len(new))
print("NOTE: independent biological/Tamil review and emulator screenshot still pending")
