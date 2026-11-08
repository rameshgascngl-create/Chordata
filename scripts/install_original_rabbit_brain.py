#!/usr/bin/env python3
"""Reproducible candidate intake of an authentic 1907 rabbit-brain engraving.

The original printed illustration is not redrawn, resized, traced or labelled over.
It is displayed at original image pixels beside an English context panel.
This historical image remains academically unapproved.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError,URLError
from io import BytesIO
from time import sleep
import csv,hashlib,json,subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
ASSET=ASSETS/"pencil_plates/rabbit_brain_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REPORT=ROOT/"docs/CHORDATA_RABBIT_1907_BRAIN_ORIGINAL_QA.md"
ID="u5-rabbit-brain"
PAGE="https://www.flickr.com/photos/internetarchivebookimages/20481807000/"
OLD_SHA="1a71def6fdaeb113250b345f645b8f7751de5b10ba2343d296eaa9cb23174b48"
FILESTEM="https://live.staticflickr.com/617/20481807000_12ee61551d"
CANDIDATES=[FILESTEM+"_b.jpg",FILESTEM+"_h.jpg",FILESTEM+".jpg"]
AUTHOR="Robert Wiedersheim (1848–1923) and William Newton Parker (1857–1923), Comparative Anatomy of Vertebrates (1907), fig. 170; Internet Archive Book Images scan"

def font(size,bold=False):
    base="/usr/share/fonts/truetype/dejavu/"
    path=base+("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(path,size)

def retrieve():
    errors=[]
    for n,url in enumerate(CANDIDATES):
        req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; ChordataZoologyQA/1.0; academic original image intake)","Accept":"image/jpeg","Referer":"https://www.flickr.com/"})
        try:
            with urlopen(req,timeout=65) as response:
                raw=response.read(8_000_001)
            image=Image.open(BytesIO(raw));image.load()
            if image.format!="JPEG" or image.width<650 or image.height<420 or image.width>5000 or image.height>5000:
                errors.append(url+": unexpected format/resolution "+str(image.format)+"/"+str(image.size))
                continue
            return raw,image.convert("RGB"),url
        except (HTTPError,URLError,TimeoutError,OSError) as e:
            errors.append(url+": "+str(e))
            sleep(2+n*3)
    raise RuntimeError("No adequate verified 1907 figure reachable; original QA asset unchanged: "+" | ".join(errors))

def main():
    raw,img,url=retrieve()
    width=max(img.width+675,1450)
    height=max(img.height+85,840)
    canvas=Image.new("RGB",(width,height),"#fafaf7")
    canvas.paste(img,(24,24))
    draw=ImageDraw.Draw(canvas)
    x=img.width+65
    draw.line((x-20,60,x-20,height-50),fill="#b7c0c8",width=3)
    ink="#1c3244"
    draw.text((x,78),"RABBIT BRAIN",font=font(36,True),fill=ink)
    draw.text((x,128),"Historical anatomical plate",font=font(23),fill=ink)
    draw.text((x,170),"Fig. 170 | Wiedersheim & Parker, 1907",font=font(19),fill="#33495a")
    draw.line((x,214,width-40,214),fill="#b7c0c8",width=2)
    notes=[
      "Original published views:",
      "A — dorsal",
      "B — ventral",
      "C — lateral",
      "",
      "Observe in the original:",
      "• Olfactory bulbs",
      "• Cerebral hemispheres",
      "• Cerebellum",
      "• Medulla oblongata",
      "",
      "Historical abbreviations should be",
      "cross-checked with the lesson key.",
      "No specimen-specific proportions",
      "are inferred beyond the source.",
    ]
    y=240
    for line in notes:
        if line:draw.text((x,y),line,font=font(21,line.startswith("Original")),fill=ink)
        y+=38 if line else 17
    draw.text((x,height-70),"Scientific / Tamil review: PENDING",font=font(18,True),fill="#923a34")
    ASSET.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(ASSET,format="PNG",optimize=True,compress_level=9)
    output=ASSET.read_bytes()
    sha=hashlib.sha256(output).hexdigest()
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    matches=[entry for entry in manifest["figures"] if entry["diagramId"]==ID and entry["lang"]=="en"]
    if len(matches)!=1 or matches[0]["path"]!="pencil_plates/rabbit_brain_en.png":
        raise RuntimeError("Rabbit brain mapping changed; stop intake")
    item=matches[0]
    if item["sha256"] not in (OLD_SHA,sha):
        raise RuntimeError("Rabbit brain already changed on another branch; no overwrite")
    for k in ("svgMaster","svgSha256"):item.pop(k,None)
    item.update({
      "sha256":sha,"size":len(output),"author":AUTHOR,
      "license":"Original illustration published 1907, public domain; scan via Internet Archive Book Images (Flickr)",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "sourceUrl":PAGE,"sourceImageUrl":url,"sourceSha256":[hashlib.sha256(raw).hexdigest()],
      "sourceFormat":"JPEG","installedFormat":"PNG",
      "sourceKind":"WIEDERSHEIM_PARKER_1907_HISTORIC_RABBIT_BRAIN_PLATE",
      "referenceUrls":[PAGE,"https://archive.org/details/comparativeanato00wied"],
      "modifications":"Original high-resolution historic cropped scan pasted at native pixel dimensions onto a larger PNG canvas; a separate English contextual panel was added. No crop, AI, rescale or drawn anatomical feature.",
      "scope":"Historic rabbit brain plate in dorsal, ventral and lateral views; a historical reference illustration, not a contemporary specimen dissection.",
      "keyEn":"Original 1907 rabbit brain drawing, fig. 170: A dorsal, B ventral, C lateral. Identify paired olfactory bulbs, cerebral hemispheres, cerebellum, medulla oblongata, pineal and cranial nerve labels as visible. Cross-check the source abbreviations, not an AI reconstruction; anatomical signoff pending.",
      "keyTa":"1907-இல் வெளியான முயலின் மூளைப் படம் (படம் 170). A — மேற்புறம்; B — கீழ்ப்புறம்; C — பக்கவாட்டுத் தோற்றம். மணநுகர்வுக் குமிழ்கள், பெருமூளை அரைக்கோளங்கள், சிறுமூளை, முகுளம் மற்றும் மூளை நரம்புகளின் குறியீடுகளை மூலப் படத்துடன் ஒப்பிட்டு அறிக. உடற்கூறியல் ஒப்புதல் நிலுவையில் உள்ளது.",
      "reviewStatus":"PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
      "visualReview":"ORIGINAL_1907_RABBIT_PLATE_PENDING_INDEPENDENT_SCIENTIFIC_REVIEW",
      "topicId":"u5-rabbit","page":4,"sectionKey":"brain"
    })
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t");cols,rows=reader.fieldnames,list(reader)
    match=[row for row in rows if row["diagramId"]==ID]
    if len(match)!=1:raise RuntimeError("Rabbit brain ledger missing")
    match[0]["author"]=AUTHOR
    match[0]["referenceSources"]=PAGE
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        writer.writeheader();writer.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],check=True,cwd=ROOT)
    REPORT.write_text(
      "# CHORDATA — original 1907 rabbit brain illustration\n\n"
      "Unit V rabbit brain, historical anatomical drawing, fig. 170. NOT independently approved.\n"
      "Work: *Comparative Anatomy of Vertebrates* (1907), by Robert Wiedersheim and William Newton Parker.\n"
      "Source: "+PAGE+"\n"
      "Original scan: "+url+"\n"
      "Public domain illustration (1907), Internet Archive Book Images collection.\n"
      "Original JPEG "+str(img.width)+"×"+str(img.height)+", "+str(len(raw))+" bytes, SHA-256 "+hashlib.sha256(raw).hexdigest()+".\n"
      "Installed full-resolution source with separate English contextual panel: PNG "+str(canvas.width)+"×"+str(canvas.height)+", "+str(len(output))+" bytes, SHA-256 "+sha+".\n"
      "The image was never traced, redrawn or scaled. 3 original orientations (A dorsal, B ventral, C lateral). Source-level figure labels require independent academic checking.\n"
      "Reviewer decisions reset to PENDING for modified image. Tamil and physical-device acceptance PENDING. Production HOLD.\n",encoding="utf-8")
    print("PASS original 1907 rabbit brain converted with native pixels",sha,img.size,canvas.size)

if __name__=="__main__":main()
