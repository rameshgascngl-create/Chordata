#!/usr/bin/env python3
"""Stage exactly three new source-credited CHORDATA QA anatomy illustrations."""
import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageOps, ImageDraw, ImageFont

root=Path(__file__).resolve().parents[1]
assets=root/"app/src/main/assets"
manifest_file=assets/"pencil_plates/manifest.json"
credits_file=assets/"source_reference_credits.json"
ledger_file=root/"docs/figure-coverage.tsv"
report_file=root/"docs/CHORDATA_HISTORICAL_ANATOMY_BATCH2_QA.md"
preview_dir=root/"build/sourced_morphology_qa"
preview_dir.mkdir(parents=True,exist_ok=True)
review_dir=root/"docs/qa-image-review"
review_dir.mkdir(parents=True,exist_ok=True)
def preview(png_path, outfile, max_side=980):
    image=Image.open(png_path).convert("RGB")
    image.thumbnail((max_side,max_side),Image.Resampling.LANCZOS)
    image.save(review_dir/outfile,format="PNG",optimize=True)
frog_url="https://upload.wikimedia.org/wikipedia/commons/b/bc/The_biology_of_the_frog_%281927%29_%2820356465586%29.jpg"
frog_page="https://commons.wikimedia.org/wiki/File:The_biology_of_the_frog_(1927)_(20356465586).jpg"

def digest(data): return hashlib.sha256(data).hexdigest()
def font(size,bold=False):
    name="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+name,size)
def get_entry(manifest, diagram, fname):
    found=[x for x in manifest["figures"] if x["diagramId"]==diagram and x["lang"]=="en"]
    assert len(found)==1 and found[0]["path"]=="pencil_plates/"+fname,(diagram,fname)
    assert found[0]["reviewStatus"].startswith("PROVISIONAL_")
    return found[0]

manifest=json.loads(manifest_file.read_text(encoding="utf-8"))
credits=json.loads(credits_file.read_text(encoding="utf-8"))
source_by_id={r["id"]:r for r in credits["sources"]}
changed=[]

for diagram, filename, ref_id, old_filename in [
    ("u5-columba-endoskeleton","columba_skeleton_en.png","pigeon-skeleton","pigeon_endoskeleton_line_art.png"),
    ("u5-rabbit-endoskeleton","rabbit_skeleton_en.png","rabbit-skeleton","rabbit_endoskeleton_line_art.png"),
]:
    record=source_by_id[ref_id]
    assert record["localFile"]==old_filename and record["academicStatus"]=="PENDING"
    original=(assets/"figures"/old_filename).read_bytes()
    assert digest(original)==record["sha256"],"Unmodified legacy source required"
    assert original[:8]==bytes.fromhex("89504e470d0a1a0a")
    (assets/"pencil_plates"/filename).write_bytes(original)
    preview(assets/"pencil_plates"/filename, filename.replace(".png","_review.png"))
    e=get_entry(manifest,diagram,filename)
    e.update(size=len(original),sha256=digest(original),
        author=record["creator"],license=record["license"],
        sourceUrl=record["sourcePageUrl"],licenseUrl=record["licenseUrl"],
        sourceAsset="figures/"+old_filename,sourceAssetSha256=record["sha256"],
        modifications="Unmodified historical line-engraving PNG copied from existing credited reference. No redrawing or false contemporary specimen labels.",
        keyEn="Historical skeletal line engraving. Bone labelling requires independent Zoology review.",
        keyTa="வரலாற்றுக் கால எலும்புக்கூட்டு கோட்டோவியம்; உறுப்புகளின் பெயரிடல் சரிபார்ப்பு நிலுவையில் உள்ளது.",
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING")
    changed.append((diagram,filename,e["sha256"],e["author"],e["sourceUrl"],e["license"]))
    record["attributionTemplate"]=(
        record["originalFilename"]+" — "+record["creator"]+"; "+record["license"]
        +"; source: "+record["sourcePageUrl"]
        +"; modifications: contrast-adjusted historical reference PNG reused unmodified in QA lesson.")
    print("STAGED:",diagram,digest(original))

request=Request(frog_url,headers={"User-Agent":"ChordataQAArtImport/1.0 (https://github.com/rameshgascngl-create/Chordata)","Referer":"https://commons.wikimedia.org/","Accept":"image/jpeg"})
with urlopen(request,timeout=45) as response:
    bytes_original=response.read(3000001)
assert 100000<len(bytes_original)<3000000
im=Image.open(io.BytesIO(bytes_original))
im.load()
assert im.format=="JPEG" and im.size==(1834,2904)
# Source Fig. 101 contains A-D views; A is the dorsal upper-left.
a=im.convert("RGB").crop((5,2,895,1615))
canvas=Image.new("RGB",(2400,1840),"#fffefa")
d=ImageDraw.Draw(canvas)
d.text((95,58),"Frog brain — dorsal view",font=font(77,True),fill="#18323e")
d.text((105,165),"Historical textbook anatomy — Fig. 101A (1927)",font=font(40),fill="#18323e")
d.rounded_rectangle((88,242,1210,1740),radius=20,outline="#9aaab5",width=3,fill="white")
art=ImageOps.contain(a,(1025,1425),Image.Resampling.LANCZOS)
canvas.paste(art,(130+(1040-art.width)//2,267+(1440-art.height)//2))
d.text((1290,285),"Original label key",font=font(50,True),fill="#18323e")
y=405
for abbr,meaning in [
    ("Olf.l","Olfactory lobe"),("Cer.H","Cerebral hemispheres"),
    ("Di","Diencephalon"),("Opt.l","Optic lobes"),
    ("Cb","Cerebellum"),("Med.obl","Medulla oblongata"),
    ("Sp.cd","Spinal cord"),("pin","Pineal body"),
    ("v4","Fourth ventricle"),
]:
    d.text((1290,y),abbr,font=font(38,True),fill="#24516a")
    d.text((1580,y),meaning,font=font(34),fill="#18323e")
    y+=120
d.text((1290,1600),"Provisional — scientific review pending",font=font(29),fill="#18323e")
frog_path=assets/"pencil_plates/frog_brain_dorsal_en.png"
canvas.save(frog_path,format="PNG",optimize=True)
data=frog_path.read_bytes()
(preview_dir/"frog_brain_dorsal_qa.png").write_bytes(data)
preview(frog_path,"frog_brain_dorsal_review.png")
e=get_entry(manifest,"u3-rana-brain","frog_brain_dorsal_en.png")
e.pop("svgMaster",None)
e.pop("svgSha256",None)
author="The biology of the frog, S. J. Holmes (1927), fig. 101 (after Newman and Parker & Parker); CHORDATA QA (layout)"
licence="Public domain (1927 U.S. publication; Holmes died 1964)"
e.update(size=len(data),sha256=digest(data),author=author,license=licence,
    sourceUrl=frog_page,licenseUrl="https://creativecommons.org/publicdomain/mark/1.0/",
    sourceSha256=[digest(bytes_original)],
    modifications="Only the original dorsal brain view (Fig. 101A) was cropped; historical ink preserved; separate English abbreviation key and heading composed outside the drawing.",
    keyEn="Olf.l: olfactory lobe; Cer.H: cerebral hemispheres; Di: diencephalon; Opt.l: optic lobes; Cb: cerebellum; Med.obl: medulla; Sp.cd: spinal cord.",
    keyTa="தவளையின் மூளை—முதுகுப்புறத் தோற்றம்; ஆங்கில விளக்கக் குறியீடுகள் இணைக்கப்பட்டுள்ளன.",
    reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING")
changed.append(("u3-rana-brain",frog_path.name,e["sha256"],author,frog_page,licence))
manifest_file.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
credits_file.write_text(json.dumps(credits,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

with ledger_file.open(newline="",encoding="utf-8") as f:
    rd=csv.DictReader(f,delimiter="\t")
    fieldnames=rd.fieldnames
    rows=list(rd)
for diagram,_,_,creator,source,_ in changed:
    match=[r for r in rows if r["diagramId"]==diagram]
    assert len(match)==1
    match[0]["author"]=creator
    match[0]["referenceSources"]=source
with ledger_file.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=fieldnames,delimiter="\t")
    w.writeheader()
    w.writerows(rows)
subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=root)
lines=["# CHORDATA Historical Anatomy — Batch 2 (QA only)","",
       "64 lesson slots are unchanged; scientific, Tamil and device acceptance PENDING.","",
       "Frog brain: 1927 Holmes textbook, Fig 101A, derived from Newman/Parker and Parker & Parker.",
       "Downloaded source SHA-256: "+digest(bytes_original),
       "Cropped dorsal panel only; separate English key; no medical or scientific approval.","",
       "Pigeon/rabbit: existing licensed public-domain historical reference PNGs copied byte-identically into actual lesson slots.",""]
for diagram,filename,sha,creator,source,licence in changed:
    lines.extend([diagram+" — "+filename,"Creator: "+creator,"Source: "+source,"Rights: "+licence,
                  "Installed PNG SHA-256: "+sha,""])
report_file.write_text("\n".join(lines),encoding="utf-8")
print("PASS: batch 2 staged exactly 3 historical zoology drawings, no human reviewer decisions fabricated")
