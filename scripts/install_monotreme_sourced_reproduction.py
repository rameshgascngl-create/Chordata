#!/usr/bin/env python3
"""Integrate reproducible, genuine monotreme specimen and anatomical evidence.

The old symbolic three-stage PNG is retained outside the APK and replaced in
its one exact shared-language lesson slot. The new image includes two genuine
photographs and a real published historical echidna pouch/mammary anatomical
plate. It explicitly does NOT pretend these are photographed sequential life
stages, and never draws an invented milk teat or hatchling.
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
RETIRED = ROOT / "docs/retired_noninstructional_png/platypus_reproduction.png"
PROVENANCE = ROOT / "docs/qa-image-review/MONOTREME_REPRODUCTION_SOURCE_PLATE_20261112.json"
DIAGRAM_ID = "u5-egg-laying-mammals-monotreme-reproduction"
OLD_SHA256 = "5936652b851a5c474cf64db332a49736266039c6f6e8b9e6e507122de6ef0284"
UA = "ChordataZoologyQA/1.0 (educational original-source verification)"
CC_BY_20 = "https://creativecommons.org/licenses/by/2.0/"
CC_BY_SA_40 = "https://creativecommons.org/licenses/by-sa/4.0/"
PD_MARK = "https://creativecommons.org/publicdomain/mark/1.0/"

SOURCES = [
    {
        "key": "platypus",
        "file": "Platypus (4848256613).jpg",
        "creator": "Eric Chan",
        "subject": "Adult platypus; sex not established by the image",
        "license": "CC BY 2.0",
        "licenseUrl": CC_BY_20,
        "width": 4256,
        "height": 2832,
    },
    {
        "key": "puggle",
        "file": "Tachyglossus aculeatus baby Museums Victoria.jpg",
        "creator": "Ian R McCann; Museums Victoria",
        "subject": "Juvenile short-beaked echidna (puggle), not a baby platypus",
        "license": "CC BY-SA 4.0",
        "licenseUrl": CC_BY_SA_40,
        "width": 1500,
        "height": 1013,
    },
    {
        "key": "pouch",
        "file": "Cambridge Natural History Mammalia Fig 003.png",
        "creator": "Frank E. Beddard (1902), after Wiedersheim and W. Haacke",
        "subject": "Echidna female ventral pouch and dorsal view of mammary glands",
        "license": "Public domain",
        "licenseUrl": PD_MARK,
        "width": 955,
        "height": 639,
    },
]
sha256 = lambda data: hashlib.sha256(data).hexdigest()

def request(session, url, params=None):
    for attempt in range(7):
        response = session.get(url, params=params, timeout=80)
        if response.status_code in (429, 500, 502, 503, 504):
            print("Source rate limit/transient", response.status_code, attempt + 1, flush=True)
            time.sleep(min(75, (attempt + 1) * 9))
            continue
        response.raise_for_status()
        return response
    raise RuntimeError("Upstream source unavailable: " + url)

def font(size, bold=False):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/" + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

def text_lines(draw, xy, lines, size=26, step=42, color="#344d55", bold=False):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font(size, bold), fill=color)
        y += step

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
matches = [x for x in manifest["figures"] if x["diagramId"] == DIAGRAM_ID]
assert len(matches) == 1 and matches[0]["lang"] == "shared", "Unexpected image slot or variant"
entry = matches[0]
assert entry["path"] == "pencil_plates/platypus_reproduction.png"
assert entry["visualReview"] == "USER_REJECTED_REPLACEMENT_REQUIRED"
assert entry["pedagogicStatus"].startswith("WITHHELD_")
assert entry["reviewStatus"].startswith("PROVISIONAL_")
target = ASSETS / entry["path"]
old_bytes = target.read_bytes()
assert sha256(old_bytes) == entry["sha256"] == OLD_SHA256
assert len(old_bytes) == entry["size"]
old_details = {k: entry.get(k) for k in (
    "author", "license", "sha256", "size", "referenceUrl", "keyEn", "keyTa",
    "visualReview", "pedagogicStatus", "pedagogicReason")}

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept": "application/json,image/*;q=0.9,*/*;q=0.5"})
originals = {}
record = []
for s in SOURCES:
    params = {"action": "query", "format": "json", "prop": "imageinfo",
              "iiprop": "url|size|extmetadata", "titles": "File:" + s["file"]}
    response = request(session, "https://commons.wikimedia.org/w/api.php", params)
    info = next(iter(response.json()["query"]["pages"].values())).get("imageinfo")
    assert info, ("Missing Commons source image", s["file"])
    info = info[0]
    lic = info["extmetadata"].get("LicenseShortName", {}).get("value", "")
    if s["key"] != "pouch":
        assert lic.casefold() == s["license"].casefold(), ("Source licence changed", s["file"], lic)
    else:
        # Published 1902; author Beddard died 1925. Cross-border public domain.
        assert "public domain" in lic.casefold() or lic.lower().startswith(("pd","cc0")), (
            "Historical published anatomical figure not clearly public domain", lic)
    assert (info["width"], info["height"]) == (s["width"], s["height"]), ("Changed source dimensions", s["file"])
    u = urlsplit(info["url"])
    real_url = urlunsplit((u.scheme, u.netloc, u.path, "", ""))
    assert real_url.startswith("https://upload.wikimedia.org/wikipedia/commons/")
    raw = request(session, real_url).content
    assert len(raw) > 50000
    if s["file"].endswith(".jpg"):
        assert raw.startswith(bytes.fromhex("ffd8ff"))
    else:
        assert raw.startswith(bytes.fromhex("89504e470d0a1a0a"))
    with Image.open(io.BytesIO(raw)) as im:
        im.verify()
    with Image.open(io.BytesIO(raw)) as im:
        assert im.size == (s["width"], s["height"])
        originals[s["key"]] = ImageOps.exif_transpose(im).convert("RGB")
    record.append({
        **s, "sourcePage": "https://commons.wikimedia.org/wiki/File:" + s["file"].replace(" ", "_"),
        "verifiedLicence": lic, "originalDownloadUrl": real_url,
        "sha256": sha256(raw), "originalBytes": len(raw),
        "transform": "Original whole frame proportionally resized into labelled comparison panel; no anatomical artwork redrawn",
    })
    print("SOURCE VERIFIED", s["key"], lic, len(raw), flush=True)
    time.sleep(2)

# Device-friendly teaching plate; all biological forms sourced rather than
# fabricated. Text boxes deliberately distinguish observed material from
# reproductive events that the images do not actually depict.
W, H = 3000, 2100
canvas = Image.new("RGB", (W, H), "#f7f7f0")
d = ImageDraw.Draw(canvas)
d.text((60, 28), "MONOTREME REPRODUCTION", font=font(60, True), fill="#173c45")
d.text((60, 102), "REAL SPECIMENS + PUBLISHED ANATOMY  |  Not a photographed life-cycle sequence",
       font=font(27), fill="#425f64")

def section(x,y,w,h,heading,subheading,source_key,image_bounds,notes):
    d.rounded_rectangle((x,y,x+w,y+h),radius=22,fill="#ffffff",outline="#c5d4d0",width=4)
    d.text((x+24,y+18),heading,font=font(39,True),fill="#18434a")
    d.text((x+24,y+73),subheading,font=font(23),fill="#35616a")
    xx0,yy0,xx1,yy1=image_bounds
    image=ImageOps.contain(originals[source_key], (xx1-xx0,yy1-yy0),Image.Resampling.LANCZOS)
    px=xx0+(xx1-xx0-image.width)//2
    py=yy0+(yy1-yy0-image.height)//2
    canvas.paste(image,(px,py))
    d.rectangle((px-1,py-1,px+image.width+1,py+image.height+1),outline="#a1b7b5",width=2)
    text_lines(d,(x+24,y+h-129),notes,size=24,step=37)

# Source photograph is an adult specimen; do NOT claim sex, egg laying or
# milk secretion is seen in this frame.
section(48,175,1430,760,
        "A  PLATYPUS", "Ornithorhynchus anatinus - original photograph",
        "platypus",(80,300,1440,735),(
            "Eggs develop and hatch in a nesting burrow.",
            "The female incubates her eggs; no pouch is present.",
            "Shown: adult specimen only (sex not determined)."))

section(1522,175,1430,760,
        "B  ECHIDNA PUGGLE", "Tachyglossus aculeatus - Museums Victoria",
        "puggle",(1555,300,2905,735),(
            "Actual young echidna; not a platypus hatchling.",
            "Echidna egg incubates in a temporary pouch.",
            "Young subsequently receives milk without a teat."))

section(48,970,1430,900,
        "C  ECHIDNA POUCH + MAMMARY GLANDS",
        "Published anatomical plate (Beddard, 1902)",
        "pouch",(85,1090,1430,1680),(
            "A: ventral surface of brooding female.",
            "B: pouch and mammary-gland groups.",
            "Historical labels preserved; anatomy, not icons."))

# Student-readable synthesis, not a fake "egg laid" illustration.
d.rounded_rectangle((1522,970,2952,1870),radius=22,fill="#e8f0ed",outline="#c0d0cc",width=4)
d.text((1564,1002),"REPRODUCTIVE COMPARISON",font=font(40,True),fill="#163c45")
d.text((1564,1080),"ECHIDNA",font=font(34,True),fill="#275e58")
text_lines(d,(1564,1132),(
    "Single leathery egg usually held in a temporary pouch.",
    "After hatching, the puggle uses mammary milk patches.",
    "No nipple or teat is present."
),size=27,step=48)
d.text((1564,1328),"PLATYPUS",font=font(34,True),fill="#275e58")
text_lines(d,(1564,1380),(
    "Female lays eggs in a lined nesting burrow.",
    "The hatchlings remain in the burrow and drink milk",
    "from mammary secretions onto the abdominal skin."
),size=27,step=48)
d.line((1570,1592,2880,1592),fill="#a0b6b1",width=3)
text_lines(d,(1564,1620),(
    "Both are egg-laying MAMMALS (order Monotremata).",
    "Milk secretion is a mammalian trait; neither has teats.",
    "No image above directly shows an egg being laid."
),size=25,step=54,color="#183940",bold=True)

d.line((55,1910,2940,1910),fill="#bdd0ca",width=3)
d.text((60,1930),"IMAGE SOURCES: Eric Chan (CC BY 2.0) | Ian R McCann / Museums Victoria (CC BY-SA 4.0)",
       font=font(22),fill="#345257")
d.text((60,1970),"Echidna pouch anatomy: F. E. Beddard, 1902 (public domain). Credits and original files: figure-source register.",
       font=font(21),fill="#345257")
d.text((60,2021),"Comparative study: different individuals and different monotreme species; images are not sequential evidence.",
       font=font(21,True),fill="#49656b")
out=io.BytesIO()
canvas.save(out,format="PNG",optimize=True)
png=out.getvalue()
assert len(png)>250000 and png.startswith(bytes.fromhex("89504e470d0a1a0a"))
assert sha256(png)!=OLD_SHA256

RETIRED.parent.mkdir(parents=True,exist_ok=True)
if RETIRED.exists():
    assert sha256(RETIRED.read_bytes()) == OLD_SHA256, "Retired image collision"
else:
    RETIRED.write_bytes(old_bytes)
target.write_bytes(png)
entry.update({
    "sha256": sha256(png),
    "size": len(png),
    "retiredSchematicPng": str(RETIRED.relative_to(ROOT)),
    "retiredSchematicSha256": OLD_SHA256,
    "retiredSchematicMetadata": old_details,
    "author": "Eric Chan (platypus photograph); Ian R McCann, Museums Victoria (echidna puggle photograph); F. E. Beddard (1902 anatomical plate); CHORDATA QA (comparison captions)",
    "license": "Composite educational adaptation under CC BY-SA 4.0; source platypus CC BY 2.0, echidna puggle CC BY-SA 4.0, historical anatomy public domain",
    "licenseUrl": CC_BY_SA_40,
    "sourceUrl": record[0]["sourcePage"],
    "sourceUrls": [x["sourcePage"] for x in record],
    "sourceSha256": [x["sha256"] for x in record],
    "originalLicences": [x["licenseUrl"] for x in record],
    "referenceUrls": [
        "https://platypus.asn.au/platypus-reproduction/",
        "https://nre.tas.gov.au/wildlife-management/fauna-of-tasmania/mammals/echidnas-and-platypus/platypus/platypus-in-tasmania",
        "https://fieldofmar-e.schools.nsw.gov.au/fact-sheets/mammals/short-beaked-echidna-fact-sheet",
        "https://en.wikisource.org/wiki/Page:Mammalia_(Beddard).djvu/35"
    ],
    "sourceKind": "COMPARATIVE_MONOTREME_SPECIMEN_PHOTOS_AND_PUBLISHED_POUCH_ANATOMY",
    "installedFormat": "PNG",
    "modifications": "Two authentic specimen photographs and one complete 1902 published anatomical panel resized proportionally on new background with English titles and accurate explanatory text; no fictitious eggs, hatchlings, milk teats or anatomical structures drawn.",
    "visualReview": "SOURCED_REAL_MONOTREME_SPECIMENS_AND_ANATOMY_QA_PROVISIONAL",
    "pedagogicStatus": "REPLACED_WITH_CC_LICENSED_MONOTREME_SOURCE_QA_PENDING_2026-11-12",
    "pedagogicReason": "Three authentic verifiable sources make the platypus, echidna young, and pouch/mammary structure recognisable; captions distinguish two species and prevent invented life-cycle depictions.",
    "reviewStatus": "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
    "scope": "Two real monotreme species and a published echidna pouch/mammary anatomical figure, with accurate comparative egg-incubation and milk-feeding explanations; not one documented sequence.",
    "keyEn": "Monotreme reproduction: A adult platypus, Ornithorhynchus anatinus (sex unknown in specimen photo); female lays leathery eggs in a burrow, where they hatch. B photographed echidna puggle, Tachyglossus aculeatus (NOT a platypus young): the female incubates a typically single egg in a temporary ventral pouch. C published comparative anatomical drawing of echidna pouch and paired mammary-gland regions (Beddard 1902). Both monotreme lineages lack teats; milk reaches offspring through specialised skin glandular openings. Images depict different species and different observations, not a chronological photographic life-cycle.",
    "keyTa": "முட்டையிடும் பாலூட்டிகளின் இனப்பெருக்கம்: A பிளாட்டிபஸ் (Ornithorhynchus anatinus) — பெண் வளைப்பொந்தில் முட்டையிட்டு அடைகாக்கிறது; புகைப்படத்தில் உயிரினத்தின் பாலினம் உறுதிப்படுத்தப்படவில்லை. B எகிட்னா (Tachyglossus aculeatus) குட்டியின் உண்மைப் புகைப்படம்; இது பிளாட்டிபஸ் குட்டி அன்று. பெண் எகிட்னா பொதுவாக ஒற்றை முட்டையைத் தற்காலிக வயிற்றுப்புறப் பையில் அடைகாக்கிறது. C எகிட்னாவின் பை மற்றும் பால்சுரப்பிகளை வெளிப்படுத்தும் 1902 ஆம் ஆண்டு வெளியான உடற்கூறியல் படம். இவ்விரண்டு இனங்களுக்கும் பால்முலைக் காம்புகள் இல்லை; தோலில் உள்ள சிறப்பான திறப்புகள் வழியாக பால் சுரந்து குட்டிகளுக்குக் கிடைக்கிறது. வெவ்வேறு இனங்களின் ஆதாரப்படங்கள்; தொடர்ச்சியான வாழ்க்கைச் சுழற்சிப் புகைப்படங்கள் அன்று."
})
MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

with LEDGER.open(newline="",encoding="utf-8") as file:
    reader=csv.DictReader(file,delimiter="\t")
    headers=reader.fieldnames
    rows=list(reader)
assert len(rows)==64 and headers
for row in rows:
    if row["diagramId"]==DIAGRAM_ID:
        row["author"]=entry["author"]
        row["referenceSources"]=" | ".join(entry["sourceUrls"])
with LEDGER.open("w",newline="",encoding="utf-8") as file:
    w=csv.DictWriter(file,fieldnames=headers,delimiter="\t")
    w.writeheader()
    w.writerows(rows)
PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
PROVENANCE.write_text(json.dumps({
    "diagramId": DIAGRAM_ID, "sourceFiles": record,
    "installedAsset": entry["path"], "installedPngSha256": sha256(png),
    "installedPngSize": len(png), "sizePx": [W,H],
    "retiredOriginalPng": str(RETIRED.relative_to(ROOT)),
    "retiredOriginalSha256": OLD_SHA256,
    "sourceArtCreatedOrInvented": False,
    "scientificCaution": "Platypus and echidna are separate taxa; images not a chronological photo series; no nipples, and no photograph depicts oviposition.",
    "review": "QA provisional; biological and Tamil independent sign-off pending",
},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
for command in (
    ["python3","scripts/write_figure_review_register.py"],
    ["python3","scripts/audit_figure_placement.py"],
    ["python3","scripts/audit_pencil_coverage.py"],
    ["python3","scripts/audit_coverage_report.py"],
    ["python3","scripts/audit_android_qa_contract.py"],
    ["python3","scripts/audit_built_apk_assets.py","--self-test"],
    ["python3","scripts/write_figure_review_register.py","--check"],
):
    subprocess.run(command,cwd=ROOT,check=True)
print("SOURCE-BASED MONOTREME REPLACEMENT INSTALLED",sha256(png),len(png),(W,H))
print("NOT ACADEMICALLY ACCEPTED: physical device and independent review still pending")
