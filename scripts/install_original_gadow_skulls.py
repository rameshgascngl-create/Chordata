#!/usr/bin/env python3
"""Install authentic 1901 Gadow Fig 54 skull illustrations in the textbook QA slot.

Reproduces a published multiple-taxon historical print at native resolution.
The app keys distinguish structural temporal patterns from modern clade history.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from io import BytesIO
from time import sleep
import csv,hashlib,json,subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
IMAGE=ASSETS/"pencil_plates/temporal_fenestrae.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_GADOW_1901_SKULL_TEMPORAL_ENGRAVING_QA.md"
DIAGRAM_ID="u4-skull-temporal-skull-types"
OLD_HASH="39dc897b5563216f6a44ecfde87da300c18cc05f5dd556964e73bf3792c8b274"
COMMONS="https://commons.wikimedia.org/wiki/File:Amphibia_and_reptiles_(1901)_(17979294289).jpg"
COMMONS_REDIRECT="https://commons.wikimedia.org/wiki/Special:Redirect/file/Amphibia_and_reptiles_(1901)_(17979294289).jpg"
GUTENBERG="https://www.gutenberg.org/cache/epub/73885/images/fig54.jpg"
AUTHOR="Hans Gadow, Amphibia and Reptiles, The Cambridge Natural History, vol. VIII (1901), Fig. 54; individual original draughtsperson not established"
KEY_EN=(
    "Authentic historical Fig. 54 (Gadow 1901), lateral skulls A–K. The orbit "
    "is O; openings and arches BEHIND the orbit are the temporal region. "
    "B Sphenodon, G Palaeohatteria and F crocodilian illustrate diapsid-related "
    "temporal construction. C Cynognathus, D Gordonia and E Dicynodon are "
    "synapsid examples, with temporal space below the skull roof. "
    "H Chelydra, I Chrysemys and K Cistudo depict turtle skulls with modified "
    "temporal roofing or emarginations; turtles are nested within Diapsida "
    "according to modern phylogeny, NOT surviving primitively anapsid reptiles. "
    "A Elginia is a parareptile, NOT a synapsid although grouped with "
    "'Theromorpha' in this old book. Historical skulls are not an idealised "
    "one-to-one numerical anapsid/synapsid/diapsid sequence. Cross-check "
    "the original A–K labels and O (orbit) against Fig. 54 caption."
)
KEY_TA=(
    "ஹான்ஸ் காடோவின் 1901 ஆம் ஆண்டின் 54-ஆம் படத்தில் A–K எனக் குறிக்கப்பட்ட "
    "பல்வேறு ஊர்வன மற்றும் சினாப்சிட் மண்டையோட்டுப் பக்கவாட்டுத் தோற்றங்கள் உள்ளன. "
    "O என்பது கண்குழி; அதன் பின்புறம் மண்டையோட்டுப் பக்கவாட்டுத் திறப்புகள் அமைந்துள்ளன. "
    "B ஸ்பீனோடான், G பாலியோஹட்டேரியா, F முதலை ஆகியவை டையாப்சிட் தொடர்புடைய "
    "மண்டையோட்டு அமைப்புகளைக் காட்டுகின்றன. C சைனோக்நாதஸ், D கோர்டோனியா, "
    "E டைசைனோடான் ஆகியவை சினாப்சிட் எடுத்துக்காட்டுகள். H, I, K ஆகியவை "
    "மாற்றமடைந்த பக்கவாட்டுப் பகுதிகளைக் கொண்ட ஆமை மண்டையோடுகள். இன்றைய "
    "பரிணாம ஆதாரங்களின்படி ஆமைகள் டையாப்சிட் மரபைச் சேர்ந்தவை; அவற்றை "
    "மாற்றமில்லாத மூதாதை அனாப்சிட்கள் எனக் கூறக் கூடாது. A எல்ஜினியா "
    "ஒரு பாராரெப்டைல்; பழைய நூலின் வகைப்பாட்டைப் பின்பற்றி அதை "
    "சினாப்சிட் எனக் கருதக் கூடாது. இப்பழைய படத்தின் வகைப்பாட்டுச் சொற்கள் "
    "நவீன பரிணாம மரபுவழியுடன் முற்றிலும் ஒத்திருக்காது."
)

def download_verified():
    options=[COMMONS_REDIRECT,
             COMMONS_REDIRECT+"?download=1"]
    failures=[]
    for i,url in enumerate(options):
        req=Request(url,headers={
          "User-Agent":"CHORDATA-academic-anatomy-QA/1.0 (historical artwork verification; https://github.com/rameshgascngl-create/Chordata)",
          "Accept":"image/jpeg,image/*",
          "Referer":"https://commons.wikimedia.org/"
        })
        try:
            with urlopen(req,timeout=95) as response:
                raw=response.read(4_000_001)
            source=Image.open(BytesIO(raw))
            source.load()
            if source.format!="JPEG" or source.size!=(1628,2136):
                raise ValueError("Historical Fig 54 scan changed: "+str((source.format,source.size)))
            if not 100_000<len(raw)<4_000_000:
                raise ValueError("Unexpected published source JPEG size")
            return raw,url
        except (HTTPError,URLError,OSError,ValueError,TimeoutError) as exc:
            failures.append(url+": "+str(exc))
            sleep(4+4*i)
    raise RuntimeError("No source-authenticated 1901 scan; preserve old figure. "+"; ".join(failures))

def main():
    registry=json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries=[item for item in registry["figures"] if item.get("diagramId")==DIAGRAM_ID]
    if len(entries)!=1 or entries[0].get("lang")!="shared" or entries[0].get("path")!="pencil_plates/temporal_fenestrae.png":
        raise RuntimeError("Historic skull image targeted at wrong lesson or language")
    e=entries[0]
    if e["sha256"]!=OLD_HASH:
        if e.get("sourceKind")=="GADOW_1901_ORIGINAL_SKULL_FIG54_JPEG_TO_PNG":
            print("Already installed verified skull illustration; not overwriting")
            return
        raise RuntimeError("Existing skull figure independently modified; refusing overwrite")
    orig,retrieved=download_verified()
    source=Image.open(BytesIO(orig)); source.load()
    converted=BytesIO()
    source.convert("RGB").save(converted,format="PNG",optimize=True,compress_level=9)
    png=converted.getvalue()
    if png[:8]!=bytes.fromhex("89504e470d0a1a0a"):raise RuntimeError("Invalid RGB PNG output")
    digest=hashlib.sha256(png).hexdigest()
    # Exact image pixels preserved at full 1628x2136 resolution. No typesetter
    # or overlay is added; lesson keys hold all additional explanations.
    IMAGE.write_bytes(png)
    for key in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        e.pop(key,None)
    e.update({
        "size":len(png),"sha256":digest,
        "author":AUTHOR,
        "license":"Public domain — original published 1901 natural-history skull engravings",
        "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
        "sourceUrl":COMMONS,"sourceImageUrl":retrieved,
        "sourceSha1":hashlib.sha1(orig).hexdigest(),
        "sourceSha256":[hashlib.sha256(orig).hexdigest()],
        "sourceKind":"GADOW_1901_ORIGINAL_SKULL_FIG54_JPEG_TO_PNG",
        "sourceFormat":"JPEG","installedFormat":"PNG",
        "referenceUrl":COMMONS,
        "referenceUrls":[COMMONS,
           "https://www.gutenberg.org/cache/epub/73885/pg73885-images.html",
           "https://www.biodiversitylibrary.org/bibliography/12620",
           "https://pmc.ncbi.nlm.nih.gov/articles/PMC3970585/"],
        "modifications":"Authenticated original published Fig 54 scan, 1628x2136 JPEG decoded to RGB PNG at identical pixel dimensions, without crop, enlargement, artificial labels, traced or AI anatomy.",
        "scope":"Published comparative skulls A–K illustrating temporal arches and foramina in historically assigned reptiles and synapsids. Includes Elginia, Sphenodon, Palaeohatteria, Cynognathus, Dicynodon, crocodilian and modern turtles, whose phylogenetic interpretation has changed since 1901.",
        "keyEn":KEY_EN,"keyTa":KEY_TA,
        "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        "visualReview":"ORIGINAL_GADOW_1901_SKULL_PLATE_PENDING_EXPERT_TAXONOMY_REVIEW",
        "topicId":"u4-skull","page":1,"sectionKey":"temporal-fenestrae"
    })
    MANIFEST.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as fh:
        reader=csv.DictReader(fh,delimiter="\t");headers,rows=reader.fieldnames,list(reader)
    matching=[row for row in rows if row["diagramId"]==DIAGRAM_ID]
    if len(matching)!=1:raise RuntimeError("Skull temporal-fenestra figure missing from coverage ledger")
    matching[0]["author"]=AUTHOR
    matching[0]["referenceSources"]=COMMONS
    with LEDGER.open("w",newline="",encoding="utf-8") as fh:
        writer=csv.DictWriter(fh,fieldnames=headers,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    REPORT.write_text(
      "# CHORDATA original historical skull temporal morphology — Gadow 1901\n\n"
      "Unit IV / skull / page 1 / temporal-fenestrae. Registered plate: u4-skull-temporal-skull-types.\n\n"
      "Book: Hans Gadow, *Amphibia and Reptiles*, *The Cambridge Natural History*, volume VIII, first edition 1901, figure 54. "
      "Drawings are historical primary zoological illustrations, not contemporary phylogeny.\n"
      "Public domain: originally published in 1901; original specific illustrator not firmly attributed. "
      "Wikimedia Commons original: "+COMMONS+"\n"
      "Cross-check caption: https://www.gutenberg.org/cache/epub/73885/pg73885-images.html (Fig. 54).\n"
      "Archive documentation: https://www.biodiversitylibrary.org/bibliography/12620\n\n"
      "Original JPEG resolution 1628x2136, "+str(len(orig))+" bytes; SHA1 "+hashlib.sha1(orig).hexdigest()+
      "; SHA256 "+hashlib.sha256(orig).hexdigest()+".\n"
      "Installed RGB PNG original pixel dimensions 1628x2136, "+str(len(png))+" bytes; SHA256 "+digest+".\n"
      "Modifications: format conversion ONLY; no image crop, scaling, annotation, AI generation or SVG rendering.\n\n"
      "Modern interpretation: B/G/F diapsid-related examples, C/D/E synapsids; H/I/K are turtles with modified temporal regions "
      "but turtle phylogeny is within Diapsida. A Elginia is a parareptile, not synapsid despite the original 'Theromorpha' grouping. "
      "This figure must not be presented as a simple universal numerical anapsid/synapsid/diapsid sequence.\n"
      "Scientific reviewer, independent Tamil reviewer, physical-device zoom, and production release PENDING.\n",
      encoding="utf-8"
    )
    print("PASS Gadow published skull plate original pixels to PNG",len(orig),len(png),digest)

if __name__=="__main__":main()
