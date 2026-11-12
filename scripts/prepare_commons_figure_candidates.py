#!/usr/bin/env python3
"""Download openly licensed ORIGINAL figures for human inspection before Android integration.

This script stages candidates in CI artifacts only; it never marks academic
acceptance or silently replaces a source PNG. Each file comes from Wikimedia
Commons and its licence must be checked independently at download time.
"""
import hashlib
import io
import json
from pathlib import Path
import requests
import time
from urllib.parse import urlsplit, urlunsplit
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageOps

OUT = Path("build/commons-figure-candidates")
OUT.mkdir(parents=True, exist_ok=True)
USER_AGENT = "ChordataZoologyQA/1.0 (educational source-rights audit; GitHub CI)"
HTTP = requests.Session()
HTTP.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json,image/*;q=0.9,*/*;q=0.5"})
BASE = "https://commons.wikimedia.org/wiki/File:"
CC4 = "https://creativecommons.org/licenses/by-sa/4.0/"
CC25 = "https://creativecommons.org/licenses/by-sa/2.5/"

SOURCES = [
    {"key": "cobra", "file": "Naja naja 113856920.jpg", "taxon": "Naja naja",
     "name": "Indian cobra", "author": "Dinesh Valke", "license": "CC BY-SA 4.0", "licenseUrl": CC4},
    {"key": "krait", "file": "Bungarus caeruleus 157751749.jpg", "taxon": "Bungarus caeruleus",
     "name": "Common krait", "author": "Manoj Karingamadathil", "license": "CC BY-SA 4.0", "licenseUrl": CC4},
    {"key": "russell", "file": "Daboia russelii (72663).jpg", "taxon": "Daboia russelii",
     "name": "Russell's viper", "author": "Nativeplants garden", "license": "CC BY-SA 4.0", "licenseUrl": CC4},
    {"key": "saw", "file": "Saw-scaled Viper.jpg", "taxon": "Echis carinatus",
     "name": "Saw-scaled viper", "author": "Jnprasad2001", "license": "CC BY-SA 4.0", "licenseUrl": CC4},
    {"key": "wing", "file": "Wing Muscles, color.svg", "taxon": "Aves",
     "name": "Bird flight-muscle anatomy", "author": "L. Shyamal",
     "license": "CC BY-SA 2.5", "licenseUrl": CC25},
    {"key": "marsupial", "file": "Baby kangaroo in pouch.jpg", "taxon": "Macropus",
     "name": "Kangaroo joey in pouch", "author": "Johnscotaus",
     "license": "CC BY-SA 4.0", "licenseUrl": CC4},
]
def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, size)

records=[]
payloads={}
for s in SOURCES:
    p={"action":"query","format":"json","prop":"imageinfo",
       "iiprop":"url|extmetadata|size","titles":"File:"+s["file"]}
    q=HTTP.get("https://commons.wikimedia.org/w/api.php",params=p,timeout=45)
    q.raise_for_status()
    pages=q.json()["query"]["pages"]
    info=next(iter(pages.values())).get("imageinfo")
    if not info:
        raise RuntimeError("No real Wikimedia file information: "+s["file"])
    meta=info[0]["extmetadata"]
    license_short=meta.get("LicenseShortName",{}).get("value","")
    if license_short.casefold()!=s["license"].casefold():
        raise RuntimeError(f"Licensing changed for {s['file']}: {license_short!r}")
    content_url=info[0]["url"]
    # Avoid Commons' tracking query and respect upload.wikimedia.org rate limits.
    clean=urlsplit(content_url)
    content_url=urlunsplit((clean.scheme,clean.netloc,clean.path,"",""))
    response=None
    for attempt in range(6):
        response=HTTP.get(content_url,timeout=70)
        if response.status_code == 429:
            delay=min(90,12*(attempt+1))
            print("WIKIMEDIA RATE LIMIT",s["key"],"retry",attempt+1,"after",delay,"seconds",flush=True)
            time.sleep(delay)
            continue
        response.raise_for_status()
        break
    else:
        raise RuntimeError("Wikimedia source still rate-limited after retries: "+s["file"])
    source_bytes=response.content
    if len(source_bytes)>20_000_000 or len(source_bytes)<7000:
        raise RuntimeError("Unexpected source image bytes for "+s["file"])
    if s["file"].endswith(".svg") and not source_bytes.lstrip().startswith((b"<?xml",b"<svg")):
        raise RuntimeError("Not source SVG: "+s["file"])
    if s["file"].endswith(".jpg") and not source_bytes.startswith(bytes.fromhex("ffd8ff")):
        raise RuntimeError("Not JPEG: "+s["file"])
    payloads[s["key"]]=source_bytes
    record={k:v for k,v in s.items()}
    record.update({
      "sourcePage":BASE+s["file"].replace(" ","_"),
      "originalDownloadUrl":content_url,
      "originalSHA256":hashlib.sha256(source_bytes).hexdigest(),
      "originalBytes":len(source_bytes),
      "verifiedLicence":license_short,
      "modified": "Resized and placed in an original labelled educational comparison (source photo unaltered apart from scaling/padding)." if s["key"] not in ("wing",) else "Original SVG rasterised to an offline PNG; no source anatomy redrawn.",
    })
    records.append(record)
    print("SOURCE OK",s["key"],len(source_bytes),license_short,flush=True)
    time.sleep(3.0)  # Polite pacing before the next Commons metadata/download request.

def save_png(im,name):
    dest=OUT/name
    im.convert("RGB").save(dest,format="PNG",optimize=True)
    print("STAGED",str(dest),im.size,hashlib.sha256(dest.read_bytes()).hexdigest())
    return {"path":dest.name,"width":im.width,"height":im.height,
        "sha256":hashlib.sha256(dest.read_bytes()).hexdigest()}

def specimen(data):
    return ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")

def paste_fit(bg,source,box):
    x0,y0,x1,y1=box
    target=(x1-x0,y1-y0)
    fitted=ImageOps.contain(source,target,method=Image.Resampling.LANCZOS)
    bg.paste(fitted,(x0+(target[0]-fitted.width)//2,y0+(target[1]-fitted.height)//2))

# Four actual snakes. This is NOT a safe field identification key.
panel=Image.new("RGB",(2500,1770),"#f8faf8")
d=ImageDraw.Draw(panel)
d.text((88,53),"India's four medically important 'Big Four' snakes",
       font=font(58,True),fill="#183338")
d.text((90,118),"Comparative photographs of genuine specimens - not safe identification advice",
       font=font(26),fill="#455b5d")
for index,key in enumerate(("cobra","krait","russell","saw")):
    s=next(z for z in SOURCES if z["key"]==key)
    col=index%2
    row=index//2
    x=80+col*1210
    y=182+row*717
    d.rounded_rectangle((x,y,x+1140,y+675),radius=22,fill="#edf3f3",outline="#ccd6d6",width=3)
    paste_fit(panel,specimen(payloads[key]),(x+18,y+18,x+1122,y+510))
    d.text((x+22,y+525),s["name"],font=font(36,True),fill="#1b3439")
    d.text((x+22,y+570),s["taxon"],font=font(29),fill="#24646a")
    d.text((x+22,y+618),f"Photo: {s['author']}  |  CC BY-SA 4.0",
           font=font(20),fill="#526769")
d.text((88,1636),"Never approach, handle or attempt medical identification of a snake based on a picture.",
       font=font(26,True),fill="#984d36")
d.text((88,1687),"Adapted from Wikimedia Commons images; individual creator/source pages and licence recorded in provenance.json.",
       font=font(19),fill="#465b5b")
output={}
output["snake"]=save_png(panel,"india_big_four_scientific_candidate.png")

# Original anatomically labelled avian skeletal/muscle figure. No hand-drawn substitute.
wing_bytes=cairosvg.svg2png(bytestring=payloads["wing"],output_width=2500)
wing=Image.open(io.BytesIO(wing_bytes)).convert("RGB")
output["wing"]=save_png(wing,"avian_flight_muscle_source_candidate.png")

# Representative real pouch-bearing marsupial, NOT an invented life cycle.
marsupial=Image.new("RGB",(2450,1520),"#f8faf8")
d=ImageDraw.Draw(marsupial)
d.text((68,54),"Marsupial reproduction: actual young in pouch",font=font(55,True),fill="#183338")
paste_fit(marsupial,specimen(payloads["marsupial"]),(70,162,1430,1360))
d.text((1470,270),"Kangaroo (representative)",font=font(32,True),fill="#16353c")
for i,line in enumerate((
  "Marsupial young are born",
  "at a relatively immature stage.",
  "In pouch-bearing species,",
  "further development is closely",
  "associated with teat attachment.",
  "Not all marsupials have",
  "a fully enclosed pouch.",
)):
    d.text((1470,350+i*95),line,font=font(28),fill="#284c51")
d.text((80,1410),"Photo: Johnscotaus  |  CC BY-SA 4.0; Wikimedia Commons; resized and captioned.",
       font=font(22),fill="#4c686a")
output["marsupial"]=save_png(marsupial,"marsupial_pouch_photographic_candidate.png")

(OUT/"provenance.json").write_text(json.dumps({
  "status":"CANDIDATE_REQUIRES_SCIENTIFIC_VISUAL_AND_LICENCE_REVIEW",
  "sources":records,
  "outputs":output,
  "notice":"These are staged images, not accepted/replaced Android assets."
},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("CANDIDATE SOURCE PREPARATION PASSED")
