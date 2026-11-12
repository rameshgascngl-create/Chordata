#!/usr/bin/env python3
"""Source-verify and integrate a genuine four-group aquatic mammal photo plate.

The symbolic mammal ovals are archived without changing the source SVG.
Only the existing Unit V aquatic-mammal lesson slot is replaced. Each photo
is a real specimen; none represents a phylogenetic ancestor of another.
"""
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
import hashlib,io,json,csv,subprocess,time
import requests
from PIL import Image,ImageOps,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
RETIRED=ROOT/"docs/retired_noninstructional_png/aquatic_mammal_lineages_en.png"
PROV=ROOT/"docs/qa-image-review/AQUATIC_MAMMAL_FOUR_PHOTOGRAPHS_20261112.json"
ID="u5-aquatic-mammals-aquatic-mammal-groups"
OLD_SHA="a330620a0fb6d62fab65caf6c79fd50ee24a686c83bc3a49b034623bfbc987c3"
CC2="https://creativecommons.org/licenses/by/2.0/"
CC4="https://creativecommons.org/licenses/by/4.0/"
SA4="https://creativecommons.org/licenses/by-sa/4.0/"
PD="https://creativecommons.org/publicdomain/mark/1.0/"
UA="ChordataZoologyQA/1.0 (public-domain/CC specimen image verification for biology education)"
SOURCES=[
 {"key":"cetacea","file":"Bottlenose Dolphin (48512426316).jpg","creator":"caroline legg",
  "taxon":"Tursiops truncatus","label":"CETACEANS","common":"Bottlenose dolphin",
  "licence":"CC BY 2.0","licenceUrl":CC2,"size":(4110,2740),
  "summary":("Wholly aquatic toothed cetacean","Forelimbs are flippers; tail flukes","Powerful dorsoventral tail strokes")},
 {"key":"sirenia","file":"Dugong (Dugong dugon) (Ifremer 00617-72913).jpg",
  "creator":"Jerome Paillet (IFREMER)","taxon":"Dugong dugon","label":"SIRENIANS",
  "common":"Dugong","licence":"CC BY 4.0","licenceUrl":CC4,"size":(4000,3000),
  "summary":("Herbivorous, wholly aquatic sirenian","Forelimb flippers and horizontal fluked tail","Seagrass feeding, as pictured")},
 {"key":"pinnipedia","file":"Harbor Seal.jpg","creator":"Arnstein Rønning",
  "taxon":"Phoca vitulina","label":"PINNIPEDS","common":"Harbour seal",
  "licence":"CC BY-SA 4.0","licenceUrl":SA4,"size":(3511,2643),
  "summary":("Marine carnivoran: family Phocidae","Fore- and hindlimbs modified as flippers","Can haul out on land, as pictured")},
 {"key":"mustelidae","file":"Sea otter marine mammal enhydra lutris.jpg",
  "creator":"U.S. Fish and Wildlife Service","taxon":"Enhydra lutris",
  "label":"SEA OTTERS (MUSTELIDAE)","common":"Sea otter",
  "licence":"Public domain","licenceUrl":PD,"size":(1800,1200),
  "summary":("Marine carnivoran, not a pinniped","Dense fur provides insulation","Hind feet are enlarged and webbed")},
]
sha=lambda data:hashlib.sha256(data).hexdigest()
def get(session,url,params=None):
  for n in range(7):
    r=session.get(url,params=params,timeout=85)
    if r.status_code in (429,500,502,503,504):
      time.sleep(min(75,10*(n+1)))
      continue
    r.raise_for_status()
    return r
  raise RuntimeError("Source unavailable after retries: "+url)
def font(px,bold=False):
  return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),px)

manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
found=[e for e in manifest["figures"] if e["diagramId"]==ID]
assert len(found)==1 and found[0]["lang"]=="en"
e=found[0]
assert (e["path"],e["topicId"],e["page"],e["sectionKey"]) == (
  "pencil_plates/aquatic_mammal_lineages_en.png","u5-aquatic-mammals",1,"marine-lineages")
assert e["visualReview"]=="USER_REJECTED_REPLACEMENT_REQUIRED" and e["pedagogicStatus"].startswith("WITHHELD_")
target=ASSETS/e["path"]
old=target.read_bytes()
assert sha(old)==e["sha256"]==OLD_SHA and len(old)==e["size"]
assert e["svgMaster"] and e["svgSha256"]
svg=ROOT/e["svgMaster"]
assert svg.is_file() and sha(svg.read_bytes())==e["svgSha256"]
old_record={k:e.get(k) for k in ("author","license","sha256","size","svgMaster","svgSha256","visualReview","pedagogicStatus")}
session=requests.Session()
session.headers.update({"User-Agent":UA,"Accept":"application/json,image/*;q=0.9,*/*;q=0.5"})
photos={}
sources=[]
for row in SOURCES:
  response=get(session,"https://commons.wikimedia.org/w/api.php",{
    "action":"query","format":"json","prop":"imageinfo","iiprop":"url|size|extmetadata",
    "titles":"File:"+row["file"]
  })
  data=next(iter(response.json()["query"]["pages"].values())).get("imageinfo")
  assert data,("No Wikimedia imageinfo",row["file"])
  data=data[0]
  actual_license=data["extmetadata"].get("LicenseShortName",{}).get("value","")
  if row["licence"]=="Public domain":
    assert "public domain" in actual_license.casefold() or actual_license.lower().startswith(("pd","cc0")),("Not demonstrably public domain",actual_license)
  else:
    assert actual_license.casefold()==row["licence"].casefold(),(row["file"],actual_license)
  assert (data["width"],data["height"])==row["size"],("Unexpected source resolution",row["file"],data["width"],data["height"])
  parsed=urlsplit(data["url"])
  raw_url=urlunsplit((parsed.scheme,parsed.netloc,parsed.path,"",""))
  assert raw_url.startswith("https://upload.wikimedia.org/wikipedia/commons/")
  raw=get(session,raw_url).content
  assert len(raw)>50000 and raw[:3]==bytes.fromhex("ffd8ff")
  with Image.open(io.BytesIO(raw)) as check:
    check.verify()
  with Image.open(io.BytesIO(raw)) as im:
    assert im.size==row["size"]
    photos[row["key"]]=ImageOps.exif_transpose(im).convert("RGB")
  sources.append({k:row[k] for k in ("key","file","creator","taxon","label","common","licence","licenceUrl","size")}|{
    "verifiedLicence":actual_license,
    "sourcePage":"https://commons.wikimedia.org/wiki/File:"+row["file"].replace(" ","_"),
    "directUrl":raw_url,"sourceSha256":sha(raw),"sourceBytes":len(raw)})
  print("VERIFIED:",row["key"],actual_license,len(raw),flush=True)
  time.sleep(2)

W,H=3200,2320
art=Image.new("RGB",(W,H),"#f6f9f7")
d=ImageDraw.Draw(art)
d.text((74,42),"AQUATIC MAMMALS — FOUR DISTINCT LINEAGES",font=font(63,True),fill="#163b43")
d.text((76,122),"Authentic specimen photographs | external morphology | not a phylogenetic tree",
       font=font(31),fill="#3d6168")
CARD_W,CARD_H=1492,968
X=[76,1632];Y=[205,1200]
for ix,row in enumerate(SOURCES):
  col=ix%2;rr=ix//2;x=X[col];y=Y[rr]
  d.rounded_rectangle((x,y,x+CARD_W,y+CARD_H),radius=24,fill="#ffffff",outline="#c1d0ce",width=4)
  d.text((x+29,y+18),row["label"],font=font(40,True),fill="#16454b")
  d.text((x+31,y+81),row["common"]+"  |  "+row["taxon"],font=font(30),fill="#376569")
  # Whole-frame proportional fit, never crop, recolour, stretch or remove actual anatomy.
  photo=ImageOps.contain(photos[row["key"]],(CARD_W-65,555),Image.Resampling.LANCZOS)
  px=x+(CARD_W-photo.width)//2
  py=y+145+(555-photo.height)//2
  art.paste(photo,(px,py))
  d.rectangle((px-2,py-2,px+photo.width+2,py+photo.height+2),outline="#96aba9",width=2)
  d.line((x+26,y+727,x+CARD_W-26,y+727),fill="#d3dfd9",width=3)
  for j,line in enumerate(row["summary"]):
    d.text((x+30,y+750+j*50),"• "+line,font=font(27),fill="#244951")
  d.text((x+30,y+921),"Photo: "+row["creator"]+"  |  "+row["licence"],font=font(20),fill="#4c6870")

d.line((76,2210,3124,2210),fill="#a8c2c0",width=3)
d.text((76,2230),"Cetacea: Artiodactyla   |   Sirenia: Afrotheria   |   Pinnipeds: Carnivora   |   Sea otter: Carnivora / Mustelidae",
       font=font(23,True),fill="#244951")
d.text((76,2270),"Convergent aquatic adaptation; not a single mammalian order. The seal and sea otter both belong to Carnivora.",
       font=font(22),fill="#41606a")
out=io.BytesIO()
art.save(out,format="PNG",optimize=True)
png=out.getvalue()
assert png[:8]==bytes.fromhex("89504e470d0a1a0a") and len(png)>350000 and sha(png)!=OLD_SHA

RETIRED.parent.mkdir(parents=True,exist_ok=True)
if RETIRED.exists():
  assert sha(RETIRED.read_bytes())==OLD_SHA, "Existing original archive differs"
else:
  RETIRED.write_bytes(old)
target.write_bytes(png)
e["retiredSchematicPng"]=str(RETIRED.relative_to(ROOT))
e["retiredSchematicSha256"]=OLD_SHA
e["retiredSchematicSvg"]=e.pop("svgMaster")
e["retiredSchematicSvgSha256"]=e.pop("svgSha256")
e["retiredSchematicMetadata"]=old_record
e.update({
  "sha256":sha(png),"size":len(png),
  "author":"; ".join(x["creator"] for x in sources)+"; CHORDATA QA (educational comparison captions)",
  "license":"Composite educational figure: CC BY-SA 4.0 derivative with separately attributed CC BY 2.0, CC BY 4.0, CC BY-SA 4.0 and public-domain original photographs",
  "licenseUrl":SA4,
  "sourceUrl":sources[0]["sourcePage"],
  "sourceUrls":[x["sourcePage"] for x in sources],
  "sourceSha256":[x["sourceSha256"] for x in sources],
  "originalLicences":[x["licenceUrl"] for x in sources],
  "sourceKind":"FOUR_AUTHENTIC_AQUATIC_MAMMAL_PHOTOGRAPHS_CC_LICENSED",
  "installedFormat":"PNG",
  "visualReview":"SOURCED_FOUR_AQUATIC_MAMMAL_PHOTOGRAPHS_QA_PROVISIONAL",
  "pedagogicStatus":"REPLACED_WITH_CC_LICENSED_AQUATIC_MAMMAL_PHOTOS_QA_PENDING_2026-11-12",
  "pedagogicReason":"Four separate actual species photographs replace generic ovals and show distinct Cetacea, Sirenia, Pinnipedia and Mustelidae external morphology.",
  "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
  "modifications":"Each original licensed photograph fitted proportionally and without cropping to a clearly credited four-card teaching comparison, with explanatory taxonomy. No specimens or anatomy invented, removed or redrawn.",
  "scope":"Four authentic photographed groups, one cetacean, one sirenian, one pinniped and one sea otter; convergence of aquatic adaptation across different mammalian lineages. Not an evolutionary tree or comprehensive guide.",
  "keyEn":"A Cetacea: bottlenose dolphin (Tursiops truncatus); forelimb flippers and horizontal tail flukes, completely aquatic. B Sirenia: dugong (Dugong dugon); marine seagrass-grazing herbivore with flippers and horizontally fluked tail. C Pinnipedia (Carnivora): harbour seal (Phoca vitulina); flipper-modified limbs, capable of hauling out on land. D Mustelidae (Carnivora): sea otter (Enhydra lutris); dense insulating fur, enlarged webbed hind feet; not a pinniped. Cetaceans are nested in Artiodactyla, sirenians in Afrotheria, and both seals and sea otters in Carnivora. Aquatic mammals are NOT one taxonomic order. Figure panels are real photographs, not a phylogenetic branching diagram.",
  "keyTa":"நீர்வாழ் பாலூட்டிகளின் உண்மையான ஒளிப்பட ஒப்பீடு: A Cetacea — டால்பின் (Tursiops truncatus); துடுப்புபோன்ற முன்கால்களும் கிடைமட்ட வால் துடுப்புகளும் உள்ளன. B Sirenia — கடற்பசு (Dugong dugon); கடற்புற்களை மேயும் தாவர உண்ணி. C Pinnipedia — கடல்நாய் (Phoca vitulina); துடுப்பு வடிவில் மாற்றமடைந்த கால்களைக் கொண்டது; நிலத்திலும் ஓய்வெடுக்கிறது. D Mustelidae — கடல் நீர்நாய் (Enhydra lutris); அடர்ந்த உரோமமும் விரலிடைச் சவ்வுள்ள பின்னங்கால்களும் உள்ளன; இது கடல்நாய் அன்று. Cetacea, Sirenia ஆகியவை வேறுபட்ட பரிணாமக் கிளைகளில் இடம்பெறுகின்றன; Pinnipedia, Mustelidae ஆகிய இரண்டும் Carnivora வகைப்பாட்டில் உள்ளன. நீர்வாழ் பாலூட்டிகள் ஒரே வரிசையினவை அல்ல; இது பரிணாம மரம் அன்று."
})
MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

# Preserve unrelated ledger rows' original EOL, encoding and fields.
raw_led=LEDGER.read_text(encoding="utf-8")
new_lines=[];count=0
for line in raw_led.splitlines(keepends=True):
  if line.startswith(ID+"\t"):
    core=line.rstrip("\r\n");ending=line[len(core):]
    fields=core.split("\t")
    headings=raw_led.splitlines()[0].split("\t")
    assert len(fields)==len(headings)
    fields[headings.index("author")]=e["author"]
    fields[headings.index("referenceSources")]=" | ".join(e["sourceUrls"])
    line="\t".join(fields)+ending
    count+=1
  new_lines.append(line)
assert count==1
LEDGER.write_bytes("".join(new_lines).encode("utf-8"))

PROV.parent.mkdir(parents=True,exist_ok=True)
PROV.write_text(json.dumps({
  "diagramId":ID,"sources":sources,"asset":e["path"],"sha256":sha(png),
  "sizeBytes":len(png),"resolution":[W,H],
  "retiredSymbolicPng":e["retiredSchematicPng"],"retiredSha256":OLD_SHA,
  "retiredSvg":e["retiredSchematicSvg"],"retiredSvgSha256":e["retiredSchematicSvgSha256"],
  "sourceAnatomyFabricated":False,"modifications":e["modifications"],
  "biologyStatus":"PROVISIONAL_INDEPENDENT_SIGNOFF_PENDING",
  "tamilStatus":"PROVISIONAL_INDEPENDENT_SIGNOFF_PENDING",
},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
for cmd in (
  ["python3","scripts/write_figure_review_register.py"],
  ["python3","scripts/audit_figure_placement.py"],
  ["python3","scripts/audit_pencil_coverage.py"],
  ["python3","scripts/audit_coverage_report.py"],
  ["python3","scripts/audit_android_qa_contract.py"],
  ["python3","scripts/audit_built_apk_assets.py","--self-test"],
  ["python3","scripts/write_figure_review_register.py","--check"],
):
  subprocess.run(cmd,cwd=ROOT,check=True)
print("INTEGRATED: genuine marine mammal four-photo plate",sha(png),len(png),"bytes")
