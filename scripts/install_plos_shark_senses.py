#!/usr/bin/env python3
"""Install peer-reviewed 2012 elasmobranch sensory anatomy as full-res PNG.

PLOS ONE Fig. 2: original *Hemiscyllium ocellatum* peer-reviewed panels
separately map lateral-line canals and ampullary pores. This is comparative
ANATOMY only; it is not a verified *Scoliodon* specimen.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from io import BytesIO
from time import sleep
import csv, hashlib, json, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
IMAGE=ASSETS/"pencil_plates/shark_sensory_systems_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_PLOS2012_ELASMOBRANCH_SENSORY_FIGURE_QA.md"
ID="u2-scoliodon-sense-organs-labelled"
OLD_SHA="869f266b9448e5a1821f6a7cbb1e193553f7237166c11e18367a057eeb033752"
PAGE="https://pmc.ncbi.nlm.nih.gov/articles/PMC3511481/figure/pone-0049857-g002/"
ARTICLE="https://pmc.ncbi.nlm.nih.gov/articles/PMC3511481/"
DOI="https://doi.org/10.1371/journal.pone.0049857"
ORIGINAL="https://journals.plos.org/plosone/article/figure/image?size=large&id=10.1371/journal.pone.0049857.g002"
ALTERNATIVES=[
    ORIGINAL,
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC3511481/bin/pone.0049857.g002.jpg",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3511481/bin/pone.0049857.g002.jpg",
]
AUTHOR="Marit Winther-Janson, Barbara E. Wueringer and Jamie E. Seymour (2012), PLOS ONE 7(11):e49857, original Fig. 2"

def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/"+("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(p,size)

def fetch_published_figure():
    issues=[]
    for number, url in enumerate(ALTERNATIVES):
        try:
            req=Request(url,headers={
               "User-Agent":"CHORDATA-Scientific-Figure-QA/1.0 (https://github.com/rameshgascngl-create/Chordata; peer-reviewed anatomy with source credits)",
               "Accept":"image/png,image/jpeg,image/*",
               "Referer":"https://journals.plos.org/"})
            with urlopen(req,timeout=85) as response:
                content=response.read(8_500_001)
            img=Image.open(BytesIO(content))
            img.load()
            if img.format not in ("PNG","JPEG") or not 120000<len(content)<8_500_000:
                raise ValueError("Not an adequate original published figure")
            if img.width<950 or img.height<650 or img.width>6000 or img.height>6000:
                raise ValueError("Original figure too low-resolution or unusually large: "+str(img.size))
            return img.convert("RGB"),content,img.format,url
        except (HTTPError,URLError,OSError,ValueError,TimeoutError) as exc:
            issues.append(url+": "+str(exc))
            sleep(min(2+number*4,12))
    raise RuntimeError("Original research figure inaccessible; old figure preserved. "+" | ".join(issues))

def main():
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries=[x for x in m["figures"] if x.get("diagramId")==ID]
    if len(entries)!=1 or entries[0].get("lang")!="en" or entries[0].get("path")!="pencil_plates/shark_sensory_systems_en.png":
        raise RuntimeError("Incorrect target lesson: shark sense-organs must be Unit II, page 5")
    entry=entries[0]
    if entry["sha256"]!=OLD_SHA:
        raise RuntimeError("A competing replacement altered shark sensory asset; do not overwrite")
    source,raw,format_used,url=fetch_published_figure()
    w,h=source.size
    # All published figure pixels remain untouched. Add context beside figure
    # on separate, neutral RGB canvas, no tracing/cropping/relabeling art.
    width=max(w+610,1690)
    height=max(h+90,980)
    image=Image.new("RGB",(width,height),"#faf9f6")
    image.paste(source,(30,40))
    d=ImageDraw.Draw(image)
    x=w+65
    dark="#27384b"
    d.line((x-20,50,x-20,height-50),fill="#aab7bc",width=2)
    d.text((x,78),"SHARK SENSORY ANATOMY",font=font(25,True),fill=dark)
    d.text((x,124),"Published anatomical study (2012)",font=font(20),fill=dark)
    d.line((x,164,width-35,164),fill="#aab7bc",width=2)
    y=198
    notes=[
      "Hemiscyllium ocellatum",
      "Epaullette shark - comparative only",
      "",
      "A: lateral-line canal pattern",
      "   Water displacement / mechanosense",
      "",
      "B: ampullary pore distribution",
      "   Weak electric fields / electroreception",
      "",
      "C: ampulla photomicrograph",
      "   Ampullary canal, bulb and nerve",
      "",
      "D: pore fields and ampullary clusters",
      "",
      "NOT a Scoliodon dissection.",
      "Do not equate the two receptor systems.",
    ]
    for line in notes:
        if line:d.text((x,y),line,font=font(18,False),fill=dark)
        y+=32 if line else 16
    d.text((x,height-78),"Scientific / Tamil sign-off: PENDING",font=font(17,True),fill="#7e4742")
    mem=BytesIO()
    image.save(mem,format="PNG",compress_level=9,optimize=True)
    png=mem.getvalue()
    output_sha=hashlib.sha256(png).hexdigest()
    IMAGE.write_bytes(png)
    for k in ("svgMaster","svgSha256","artworkDisposition","reviewerNote"):
        entry.pop(k,None)
    entry.update({
      "size":len(png),"sha256":output_sha,
      "author":AUTHOR,
      "license":"CC BY; 2012 PLOS ONE original research Figure 2, credited to Winther-Janson, Wueringer and Seymour",
      "licenseUrl":"https://creativecommons.org/licenses/by/4.0/",
      "sourceUrl":PAGE,
      "sourceImageUrl":url,
      "sourceSha1":hashlib.sha1(raw).hexdigest(),
      "sourceSha256":[hashlib.sha256(raw).hexdigest()],
      "sourceKind":"PLOS2012_ORIGINAL_EPAULETTE_SHARK_SENSORY_ANATOMY",
      "sourceFormat":format_used,
      "installedFormat":"PNG",
      "referenceUrls":[ARTICLE,PAGE,DOI,
       "https://dlnr.hawaii.gov/sharks/about-sharks/senses/"],
      "modifications":"Published full Fig. 2 reproduced pixel-identically in 1:1 scale on "+str(width)+"x"+str(height)+" RGB PNG, with separate English comparison notes to the RIGHT. Source artwork never cropped, rescaled, recoloured, recreated or AI-generated.",
      "scope":"Research Fig. 2 of Hemiscyllium ocellatum, NOT Scoliodon: A lateral-line mechanosensory canal system, B electrosensory ampullary pores, C microscope ampullary structure, D ampullary fields/clusters.",
      "keyEn":"Original peer-reviewed 2012 anatomical Fig. 2 of the EPAULETTE SHARK Hemiscyllium ocellatum, not Scoliodon sorrakowah. Panel A maps mechanosensory lateral-line canals detecting water displacement; panel B maps electroreceptive ampullary pores sensing weak external bioelectric fields. C shows microscopic ampullary canal, bulb and nerve; D maps ampullary fields/clusters. These two sensory pathways are distinct. Do not transfer pore-field geometry or counts from Hemiscyllium to Scoliodon without species-specific evidence.",
      "keyTa":"வின்தர்-யான்சன் குழுவினரின் 2012 ஆய்வுக் கட்டுரையில் உள்ள ஹெமிஸ்சிலியம் ஒசெல்லாட்டம் என்ற சுறா இனத்தின் ஒப்பீட்டு உடற்கூறியல் படம்; இது ஸ்கோலியோடான் வகைமாதிரிப் படம் அல்ல. A — நீரின் அசைவுகளை உணரும் பக்கக்கோட்டு மண்டலக் கால்வாய்கள் (இயந்திர உணர்தல்); B — மெல்லிய உயிர்மின்னியல் புலங்களை உணரும் லோரென்சினியின் ஆம்புலாக்களின் துளைகள் (மின்னுணர்தல்); C — ஆம்புலாக் கால்வாய், குமிழ் மற்றும் நரம்பின் நுண்ணோக்கித் தோற்றம்; D — துளைகளின் பரவலும் ஆம்புலாக்களின் குழுக்களும். இரண்டு உணர்வு மண்டலங்களின் பணிகளைக் குழப்பக் கூடாது. இந்தச் சுறாவின் துளை எண்ணிக்கையையும் இடஅமைப்பையும் ஸ்கோலியோடானுக்கு நேரடியாகப் பொருத்தக் கூடாது.",
      "visualReview":"PLOS2012_ORIGINAL_PEER_REVIEWED_COMPARATIVE_ANATOMY_PENDING_HUMAN_SIGNOFF",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "topicId":"u2-scoliodon","page":5,"sectionKey":"sense-organs"
    })
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f,delimiter="\t")
        cols,rows=reader.fieldnames,list(reader)
    matches=[r for r in rows if r["diagramId"]==ID]
    if len(matches)!=1:raise RuntimeError("Missing/duplicated Scoliodon sensory figure ledger entry")
    matches[0]["author"]=AUTHOR
    matches[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t");writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    REPORT.write_text(
      "# CHORDATA Unit II — original shark sensory anatomy, peer-reviewed 2012\n\n"
      "Scoliodon lesson, page 5, sense-organs; figure ID u2-scoliodon-sense-organs-labelled.\n\n"
      "Original Fig. 2 by M. Winther-Janson, B. E. Wueringer and J. E. Seymour, PLOS ONE 7(11): e49857 (2012), DOI 10.1371/journal.pone.0049857.\n"
      "Public-access research figure: "+PAGE+"\nOriginal source fetched from: "+url+"\n"
      "Rights: Creative Commons Attribution (CC BY), original authors retain copyright. Provide this attribution in app credits and indicate added text context.\n"
      "Source "+format_used+" "+str(w)+"x"+str(h)+"; bytes "+str(len(raw))+
      "; source SHA1 "+hashlib.sha1(raw).hexdigest()+"; source SHA256 "+hashlib.sha256(raw).hexdigest()+".\n"
      "Installed PNG "+str(width)+"x"+str(height)+", bytes "+str(len(png))+
      ", SHA256 "+output_sha+".\n\n"
      "Source original is displayed at its native pixels, never cropped or enlarged. Added side panel only explains original A/B/C/D captions. Panels A and B DISTINCT: lateral-line mechanoreception vs electroreceptive ampullae. Panel C is original micrograph. D distinguishes pore fields and clusters.\n"
      "IMPORTANT: This is Hemiscyllium ocellatum, NOT Scoliodon. Species-specific counts or head geometry cannot be inferred for Scoliodon. Source is neither an AI illustration nor an original project vector drawing.\n"
      "Independent scientific and Tamil signoff PENDING, device zoom PENDING, production release HOLD.\n",encoding="utf-8")
    print("PASS original peer-reviewed Figure 2 integrated",str(source.size),len(png),output_sha)

if __name__=="__main__":main()
