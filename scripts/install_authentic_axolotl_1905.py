#!/usr/bin/env python3
"""Replace AI-made axolotl neoteny image with a historic, source-authentic 1905 plate.

A 1905 book distinguishes 'larval axolotl' (external gills) and 'adult form'
(metamorphosed salamander). These are NOT stages of the normal adult axolotl
life cycle: aquatic axolotls normally mature while retaining larval anatomy.
The source pixels must be included untouched, and wording must not imply
routine or obligatory metamorphosis.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from time import sleep
import csv,hashlib,json,subprocess
from io import BytesIO
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"app/src/main/assets"
IMG=A/"pencil_plates/axolotl_neoteny_en.png"
M=A/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_AXOLOTL_HISTORIC_NIE1905_SOURCE_QA.md"
ID="u3-neoteny-axolotl-development"
OLD_SHA="592cb6de311f730b21f2a7953cc184d8d441285ca3dfb708a8dc43ed67a273bb"
ORIGINAL="https://upload.wikimedia.org/wikipedia/commons/d/de/NIE_1905_Axolotl.png"
PAGE="https://commons.wikimedia.org/wiki/File:NIE_1905_Axolotl.png"
AUTHOR="Unidentified historical illustrator, The New International Encyclopaedia (1905), vol. 2, after p. 330; published by Dodd, Mead & Co."

def download():
    urls=[ORIGINAL,ORIGINAL+"?download=1","https://commons.wikimedia.org/wiki/Special:Redirect/file/NIE_1905_Axolotl.png"]
    failures=[]
    for n,url in enumerate(urls):
        request=Request(url,headers={"User-Agent":"ChordataAcademicZoologyQA/1.0 (https://github.com/rameshgascngl-create/Chordata; published natural history artwork)","Referer":"https://commons.wikimedia.org/","Accept":"image/png,*/*"})
        try:
            with urlopen(request,timeout=95) as response:
                raw=response.read(3000001)
            im=Image.open(BytesIO(raw))
            im.load()
            if im.format!="PNG" or im.size!=(1487,1046) or not 300000<len(raw)<3000000:
                raise ValueError("Original image size/format mismatch")
            if raw[:8]!=bytes.fromhex("89504e470d0a1a0a"):
                raise ValueError("Invalid PNG signature")
            return raw,url
        except (HTTPError,URLError,ValueError,TimeoutError,OSError) as error:
            failures.append(str(error)+" at "+url)
            sleep(3+n*4)
    raise RuntimeError("No authenticated historic axolotl PNG; keep existing illustration: "+"; ".join(failures))

def main():
    manifest=json.loads(M.read_text(encoding="utf-8"))
    matched=[x for x in manifest["figures"] if x.get("diagramId")==ID and x.get("lang")=="en"]
    if len(matched)!=1 or matched[0].get("path")!="pencil_plates/axolotl_neoteny_en.png":
        raise RuntimeError("Registered axolotl image does not match lesson")
    entry=matched[0]
    if entry["sha256"]!=OLD_SHA:
        if entry.get("sourceKind")=="HISTORICAL_NIE1905_AXOLOTL_METAMORPHOSED_VS_GILLED_PNG":
            print("Authentic axolotl plate already installed; stop without rewriting")
            return
        raise RuntimeError("Concurrent image update detected; refusing overwrite")
    raw,used=download()
    digest=hashlib.sha256(raw).hexdigest()
    # Install exact original PNG bytes: no resizing, redraw, text overlays, or AI.
    IMG.write_bytes(raw)
    for field in ("svgMaster","svgSha256","visualReviewNotes","artworkDisposition","reviewerNote"):
        entry.pop(field,None)
    entry.update({
      "size":len(raw),"sha256":digest,
      "author":AUTHOR,
      "license":"Public domain — original US encyclopaedia illustration published 1905",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "sourceUrl":PAGE,"sourceImageUrl":ORIGINAL,
      "sourceSha1":hashlib.sha1(raw).hexdigest(),
      "sourceSha256":[digest],
      "sourceKind":"HISTORICAL_NIE1905_AXOLOTL_METAMORPHOSED_VS_GILLED_PNG",
      "sourceFormat":"PNG","installedFormat":"PNG",
      "referenceUrl":PAGE,
      "referenceUrls":[PAGE,"https://en.wikisource.org/wiki/The_New_International_Encyclop%C3%A6dia/Axolotl","https://ambystoma.uky.edu/12-educationresources/13-education"],
      "modifications":"None. Byte-identical 1487x1046 source PNG installed; original printed numerals 1 and 2 retained, with explanatory English and Tamil keys outside image. No crop, synthetic fill, recolour, vector or AI drawing.",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "visualReview":"HISTORIC_ORIGINAL_AXOLOTL_TWO_FORMS_PENDING_ZOOLOGY_TAMIL_APPROVAL",
      "scope":"1905 historic two-form comparison of gilled aquatic axolotl (1) and metamorphosed terrestrial salamander-like form (2), NOT a compulsory developmental sequence for normally paedomorphic Ambystoma mexicanum.",
      "keyEn":"Historical 1905 comparison, not a routine axolotl life cycle. Fig. 1: gilled aquatic axolotl with tail fin and limbs; these larval-like external features are retained in sexually mature paedomorphic Ambystoma mexicanum. Fig. 2: metamorphosed salamander-like phenotype with external gills lost; metamorphosis is uncommon in typical axolotls and may be experimentally induced, so the older caption 'adult form' must NOT be interpreted to mean that normal adult axolotls are gill-less. Both forms are historic engravings, not photographic specimen records.",
      "keyTa":"1905 ஆம் ஆண்டின் வரலாற்று ஒப்பீட்டுப் படம்; இது ஆக்சலாட்டிலின் இயல்பான கட்டாய வாழ்க்கைச் சுழற்சி அல்ல. படம் 1: வெளிச்செவுள்களும் வால் துடுப்பும் கொண்ட நீர்வாழ் ஆக்சலாட்டில்; பாலியல் முதிர்ச்சியடைந்த பின்னரும் இவ்விளம்பருவப் பண்புகள் பொதுவாக நீடிக்கின்றன. படம் 2: வெளிச்செவுள்களை இழந்து மாற்றுருவாக்கம் அடைந்த சாலமாண்டரை ஒத்த நிலை. வழக்கமான முதிர்ந்த ஆக்சலாட்டில் அனைத்தும் படம் 2 போல மாற்றுருவாக்கம் அடைவதில்லை. பழைய நூலில் கூறப்பட்ட 'முதிர்நிலை' என்ற சொல்லைத் தவறாகப் பொதுமைப்படுத்தக் கூடாது.",
      "topicId":"u3-neoteny","page":2,"sectionKey":"axolotl"
    })
    M.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t");cols,rows=reader.fieldnames,list(reader)
    matched=[r for r in rows if r["diagramId"]==ID]
    if len(matched)!=1:raise RuntimeError("Review ledger missing/duplicated axolotl figure")
    matched[0]["author"]=AUTHOR
    matched[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t");writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    REPORT.write_text(
      "# CHORDATA — historical published axolotl two-form plate, 1905\n\n"
      "Unit III, topic neoteny; page 2, section axolotl; diagram u3-neoteny-axolotl-development.\n\n"
      "Source "+PAGE+"\nDirect original "+used+"\n"
      "1905, *The New International Encyclopaedia*, 1st ed., vol. 2, after page 330; Dodd, Mead & Company. The specific drawing artist is not independently identified. Public domain in the US, per Commons record.\n\n"
      "Original byte-identical PNG 1487x1046, "+str(len(raw))+" bytes, SHA-1 "+hashlib.sha1(raw).hexdigest()+", SHA-256 "+digest+".\n\n"
      "Biology warning: historical Fig. 1 gilled aquatic, Fig. 2 metamorphosed terrestrial-looking form. The older source's 'adult' label describes the metamorphosed form, not the common adult axolotl; this species usually matures while retaining external gills and tail fin. Metamorphosis is rare or experimentally induced. Compare the forms, never teach obligatory transformation.\n\n"
      "No anatomy was redrawn and no artificial labels added. English labels in the source; English/Tamil explanatory keys are in separate lesson metadata.\n\n"
      "Independent scientific and Tamil review, zoom legibility on a physical phone, and the gated Android build remain PENDING. Production release HOLD.\n",encoding="utf-8")
    print("PASS original 1905 axolotl image installed without changes",len(raw),digest)

if __name__=="__main__":main()
