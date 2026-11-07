#!/usr/bin/env python3
"""Source-exact 1905 ascidian scientific PNG intake. ZERO synthetic drawing."""
import csv
import hashlib
import json
import subprocess
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
DEST=ASSETS/"pencil_plates/ascidia_metamorphosis.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_1905_ASCIDIAN_PUBLISHED_PNG_QA.md"
ID="u1-urochordata-ascidia-larva-adult"
SOURCE="https://upload.wikimedia.org/wikipedia/commons/3/39/NIE_1905_Ascidians_and_balanoglossus.png"
PAGE="https://commons.wikimedia.org/wiki/File:NIE_1905_Ascidians_and_balanoglossus.png"
BOOK="https://en.wikisource.org/wiki/The_New_International_Encyclop%C3%A6dia/Ascidian"
BIOLOGY="https://pmc.ncbi.nlm.nih.gov/articles/PMC7288498/"
AUTHOR="Unknown illustrator, The New International Encyclopaedia (1905), Vol. 2; historical plate"
OLD_SHA="abb83d6c457ce293edc3a59652e5ff8d2fdf084e8dd3acf70daa93dca4df4ce3"
SOURCE_SHA1="7422e81e0c48f39abcddd87b3b979ac7a12b2b4f"
SOURCE_SHA256="af4f986941cd3b9f65452bde00ef6974e2ce425c01e2d7a988f44986f01dfa00"

def main():
    with urlopen(Request(SOURCE,headers={
        "User-Agent":"ChordataAcademicImageQA/1.0 (original historical primary source)",
        "Referer":"https://commons.wikimedia.org/",
        "Accept":"image/png"
    }),timeout=70) as f:
        raw=f.read(4_500_001)
    img=Image.open(BytesIO(raw));img.load()
    if img.format!="PNG" or img.size!=(1488,2387) or not (700_000<len(raw)<4_500_000):
        raise ValueError(f"Historic original image does not meet genuine-PNG source requirement: {img.format} {img.size} {len(raw)}")
    src_sha1=hashlib.sha1(raw).hexdigest()
    src_sha256=hashlib.sha256(raw).hexdigest()
    if src_sha1 != SOURCE_SHA1 or src_sha256 != SOURCE_SHA256:
        raise ValueError("Unmodified historical source PNG hash changed; refuse substitution")
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    match=[x for x in manifest["figures"] if x["diagramId"]==ID and x["lang"]=="shared"]
    if len(match)!=1 or match[0]["path"]!="pencil_plates/ascidia_metamorphosis.png":
        raise ValueError("Wrong registered larval metamorphosis lesson")
    entry=match[0]
    if entry["sha256"] not in (OLD_SHA,src_sha256):
        raise ValueError("Cannot overwrite independently altered figure")
    # Copy ORIGINAL published PNG bytes. No drawing, resampling or added labels.
    DEST.write_bytes(raw)
    entry.update({
        "sha256":src_sha256,
        "size":len(raw),
        "author":AUTHOR,
        "license":"Public domain historical encyclopaedia illustration (published 1905); exact original scan",
        "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
        "sourceUrl":PAGE,
        "sourceImageUrl":SOURCE,
        "sourceSha1":src_sha1,
        "sourceSha256":[src_sha256],
        "referenceUrl":BOOK,
        "referenceUrls":[PAGE,BOOK,BIOLOGY],
        "modifications":"NONE — existing 1905 plate retained as original PNG bytes; no re-drawing, rasterization, vectorization, crops, overlays, generative AI or upscaling",
        "sourceKind":"AUTHENTIC_1905_PUBLISHED_PNG_NOT_DRAWN_FOR_APP",
        "scope":"Historical compound plate: ascidian adult forms (1–7), larval transformation (8a–d); separate Balanoglossus 9–10 is not an ascidian",
        "keyEn":"Original 1905 historical plate. Figure 1 = solitary adult ascidian; Figure 3 = internal anatomy of Clavellina; Figure 8a = swimming tadpole larva, 8b = recently attached larva, 8c = older attached stage, 8d = tail section with notochord. Figures 9–10 illustrate BALANOGLOSSUS, not Ascidia. Original historic labels, not a newly drawn or species-specific plate.",
        "keyTa":"1905 ஆம் ஆண்டு வெளியான அசல் உடற்கூறியல் விளக்கப்படம். படம் 1: தனித்த அசிடியன் முதிருயிரி; படம் 3: கிளாவெலினாவின் உள்ளமைப்பு; படம் 8a: நீந்தும் தலைப்பிரட்டை இளர்வி; 8b: புதிதாகப் பற்றிய இளர்வி; 8c: வளர்ந்த பற்றிய நிலை; 8d: முதுகுநாண் கொண்ட வாலின் குறுக்குவெட்டு. படங்கள் 9–10 பலனோக்ளாசஸ்; அவை அசிடியன் அல்ல.",
        "visualReview":"SOURCED_HISTORICAL_PNG_PENDING_EXPERT_REVIEW",
        "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        "topicId":"u1-urochordata",
        "page":3,
        "sectionKey":"retrogressive-metamorphosis"
    })
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t")
        cols,rows=reader.fieldnames,list(reader)
    m=[x for x in rows if x["diagramId"]==ID]
    if len(m)!=1:raise ValueError("Ascidian coverage record missing")
    m[0]["author"]=AUTHOR
    m[0]["referenceSources"]=" | ".join([PAGE,BOOK,BIOLOGY])
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
        "# Authentic 1905 ascidian anatomical illustration (PNG-only intake)\n\n"
        f"Figure: {ID} (Unit I, page 3, retrogressive metamorphosis)\n\n"
        f"Source: {PAGE}\nOriginal source image: {SOURCE}\n"
        f"Attribution: {AUTHOR}\nRights: public-domain artwork, published 1905; source Commons record: {PAGE}\n\n"
        f"Original PNG: {img.width} × {img.height} pixels, {len(raw)} bytes\n"
        f"Source PNG SHA-1: {src_sha1}\nSource/embedded PNG SHA-256: {src_sha256}\n\n"
        "No artificial diagram was produced: original public-domain PNG bytes are unmodified.\n"
        "Full historical composite page, **not solely** an ascidian metamorphosis drawing: "
        "1–7 ascidian forms; 8a–d larval attachment and tail/notochord regression; "
        "9–10 Balanoglossus (different taxon). The existing book provides the original "
        f"numbering and abbreviations: {BOOK}\n\n"
        "Visually inspect full-resolution original at zoom. Zoology science review, "
        "Tamil term review, and physical-device acceptance PENDING; production release HOLD.\n",
        encoding="utf-8"
    )
    print("PASS ORIGINAL PUBLISHED PNG",len(raw),"bytes, SHA1",src_sha1,"SHA256",src_sha256)
if __name__=="__main__":
    main()
