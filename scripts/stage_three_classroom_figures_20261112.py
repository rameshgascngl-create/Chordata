#!/usr/bin/env python3
"""Reproducible, attributed classroom figure replacement; never alters 61 other slots."""
from __future__ import annotations
import hashlib, io, json, shutil, time, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
IMAGES=ASSETS/"pencil_plates"
MANIFEST=IMAGES/"manifest.json"
MARKER=ROOT/"docs/qa-image-review/THREE_CLASSROOM_FIGURES_REPLACED_20261112.json"
OLD_DIR=ROOT/"docs/retired_noninstructional_png"
TEAL="#116A67"; NAVY="#173F4E"; GREY="#4D6266"; PAPER="#FFFBF5"; LIGHT="#EDF5F2"
LICENCE="https://creativecommons.org/licenses/by-sa/3.0/"
SOURCE_LIST={
  "scale_triptych":("Fishscales.png","Jon Houseman","CC BY-SA 3.0"),
  "placoid":("PlacoidComp.png","Jon Houseman","CC BY-SA 3.0"),
  "dogfish_comparison":("Squa152p.png","Jon Houseman","CC BY-SA 3.0"),
  "devonian":("Fishapod evolution.jpg","Maija Karala","CC BY-SA 3.0"),
}
def sha(data): return hashlib.sha256(data).hexdigest()
def source_url(name):
    path=name.replace(" ","_")
    digest=hashlib.md5(path.encode("utf-8")).hexdigest()
    from urllib.parse import quote
    return f"https://upload.wikimedia.org/wikipedia/commons/{digest[0]}/{digest[:2]}/{quote(path)}"
def download(name):
    urls=[source_url(name), "https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(name.replace(" ","_"))]
    last=None
    for url in urls:
        for tries in range(3):
            try:
                req=urllib.request.Request(url,headers={"User-Agent":"CHORDATA-Zoology-Educational-QA/1.0 (https://github.com/rameshgascngl-create/Chordata)","Accept":"image/avif,image/webp,image/png,image/jpeg,*/*"})
                with urllib.request.urlopen(req,timeout=40) as response:
                    data=response.read(12000000)
                im=Image.open(io.BytesIO(data))
                im.load()
                if im.width<400 or im.height<300: raise ValueError("source too small")
                return im.convert("RGB"),{"sourceOriginalFilename":name,"sourcePage":"https://commons.wikimedia.org/wiki/File:"+name.replace(" ","_"),"sourceDownloadUrl":url,"sha256":sha(data),"size":len(data),"dimensions":[im.width,im.height]}
            except Exception as e:
                last=e
                time.sleep(2*tries+1)
    raise RuntimeError(f"Cannot obtain published Commons image {name}: {last}")
def font(size,bold=False):
    f="/usr/share/fonts/truetype/dejavu/DejaVuSans"+("-Bold" if bold else "")+".ttf"
    return ImageFont.truetype(f,size)
def text(draw,xy,s,size=33,color=NAVY,bold=False):
    draw.text(xy,s,font=font(size,bold),fill=color)
def panel(draw,box):
    draw.rounded_rectangle(box,radius=30,fill="white",outline="#C9DBD5",width=4)
def fitted(canvas,img,box,pad=0,white=True):
    x,y,w,h=box
    pic=ImageOps.contain(img,(w-2*pad,h-2*pad),Image.Resampling.LANCZOS)
    xx=x+(w-pic.width)//2; yy=y+(h-pic.height)//2
    canvas.paste(pic,(xx,yy))
def create_digestive(old,comparison):
    # The old anatomy drawing remains the species-specific basis, but is
    # enlarged rather than reduced to one third of a landscape infographic.
    img=Image.new("RGB",(1840,1900),PAPER)
    d=ImageDraw.Draw(img)
    text(d,(85,36),"SCOLIODON  |  DIGESTIVE ANATOMY",65,bold=True)
    text(d,(86,117),"Scoliodon-type organ relationships + a separately labelled dogfish comparison",30,color=GREY)
    panel(d,(50,180,1235,1660))
    panel(d,(1260,180,1790,1660))
    text(d,(80,205),"A   Scoliodon-type anatomy",45,bold=True)
    w,h=old.size
    crop=old.crop((int(w*.035),int(h*.075),int(w*.56),int(h*.97)))
    fitted(img,crop,(83,270,1120,1300),pad=20)
    text(d,(1300,210),"B   Comparison",43,bold=True)
    text(d,(1300,270),"DOGFISH",36,bold=True,color=TEAL)
    text(d,(1300,315),"Squalus (not Scoliodon)",26,color=GREY)
    fitted(img,comparison,(1290,380,470,355),pad=8)
    text(d,(1300,758),"Liver lobes: A–C",27)
    text(d,(1300,811),"Gall bladder: D",27)
    text(d,(1300,864),"Stomach: F and G",27)
    text(d,(1300,917),"Pancreas: H",27)
    text(d,(1300,970),"Spiral intestine: J",27)
    d.line((1290,1050,1750,1050),fill="#C9DBD5",width=3)
    text(d,(1300,1090),"FUNCTIONAL KEY",34,bold=True,color=TEAL)
    for y,lines in [(1150,["Spiral intestinal fold:","increases absorptive area"]),
                    (1280,["Rectal gland:","salt secretion, not digestion"]),
                    (1410,["Pyloric stomach:","connects to intestine"])]:
        for i,line in enumerate(lines): text(d,(1300,y+i*39),line,25 if i else 28)
    text(d,(74,1722),"Scoliodon diagram: original CHORDATA QA artwork, re-laid out without altering organs.",27,color=GREY)
    text(d,(74,1772),"Comparison: Jon Houseman, Squa152p.png, CC BY-SA 3.0. Species differ.",27,color=GREY)
    return img
def create_scales(triptych,placoid):
    img=Image.new("RGB",(1840,1800),PAPER); d=ImageDraw.Draw(img)
    text(d,(75,38),"FISH SCALES  |  FOUR STRUCTURAL TYPES",62,bold=True)
    text(d,(75,119),"Anatomical comparison: inspect the margin, shape and denticle architecture",29,color=GREY)
    panel(d,(50,185,1790,1035))
    text(d,(85,211),"A   GANOID",38,bold=True,color=TEAL)
    text(d,(665,211),"B   CYCLOID",38,bold=True,color=TEAL)
    text(d,(1250,211),"C   CTENOID",38,bold=True,color=TEAL)
    fitted(img,triptych,(100,272,1640,660),pad=4)
    panel(d,(50,1060,1790,1668))
    text(d,(84,1084),"D   PLACOID / DERMAL DENTICLE — SHARK",37,bold=True,color=TEAL)
    fitted(img,placoid,(100,1152,1635,410),pad=6)
    text(d,(85,1694),"Sources: Jon Houseman, Fishscales.png + PlacoidComp.png (CC BY-SA 3.0).",27,color=GREY)
    text(d,(85,1734),"Ganoid: rhomboid  |  Cycloid: smooth edge  |  Ctenoid: ctenii  |  Placoid: tooth-like",25,color=GREY)
    return img
def create_devonian(source):
    im=Image.new("RGB",(1760,2600),PAPER); d=ImageDraw.Draw(im)
    text(d,(80,34),"DEVONIAN FISH-TO-TETRAPOD TRANSITION",57,bold=True)
    text(d,(80,112),"Fossil-based branching relationships, not a direct ancestor chain",28,color=GREY)
    panel(d,(45,180,1710,2445))
    fitted(im,source,(92,205,1550,2190),pad=10)
    text(d,(77,2480),"Eusthenopteron  |  Panderichthys  |  Tiktaalik  |  Acanthostega",27,color=NAVY)
    text(d,(77,2520),"Ichthyostega  |  Pederpes    •    Maija Karala, CC BY-SA 3.0",26,color=GREY)
    return im
def main():
    previous=json.loads(MARKER.read_text(encoding="utf-8")) if MARKER.exists() else None
    if previous and __import__("os").environ.get("CHORDATA_REBUILD_FIGURES") != "1":
        print("Already staged: preserve existing exact-hash accepted PNGs")
        return
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    fs=manifest["figures"]
    byid={x["diagramId"]:x for x in fs if x["lang"] in ("en","shared")}
    specs=[
      ("u2-scoliodon-digestive-labelled","scoliodon_digestive_en.png"),
      ("u2-scales-fins-scale-types-labelled","fish_scale_types.png"),
      ("u3-origin-devonian-transition","devonian_tetrapod_transition_en.png"),
    ]
    assert len({x["diagramId"] for x in fs})==64
    assert len(fs)==68
    originals={}
    for id,filename in specs:
        x=byid[id]
        assert x["path"]=="pencil_plates/"+filename
        installed=(IMAGES/filename).read_bytes()
        assert sha(installed)==x["sha256"],("unexpected installed image change",filename)
        if previous:
            raw=(OLD_DIR/filename).read_bytes()
            matched=next(z for z in previous["figures"] if z["diagramId"]==id)
            assert sha(raw)==matched["original"]["sha256"],("archived source changed",filename)
        else:
            raw=installed
        originals[id]={"sha256":sha(raw),"size":len(raw),"path":"docs/retired_noninstructional_png/"+filename}
    # An explicit named source record is retained for each Commons original.
    sources={}
    for key,(filename,author,licence) in SOURCE_LIST.items():
        im,metadata=download(filename)
        sources[key]=(im,dict(metadata,author=author,licence=licence))
    original_digestive=(OLD_DIR if previous else IMAGES)/"scoliodon_digestive_en.png"
    old_img=Image.open(original_digestive).convert("RGB")
    rendered={
      specs[0][0]:create_digestive(old_img,sources["dogfish_comparison"][0]),
      specs[1][0]:create_scales(sources["scale_triptych"][0],sources["placoid"][0]),
      specs[2][0]:create_devonian(sources["devonian"][0]),
    }
    mapping={
      specs[0][0]:["dogfish_comparison"],
      specs[1][0]:["scale_triptych","placoid"],
      specs[2][0]:["devonian"],
    }
    full_provenance=[]
    OLD_DIR.mkdir(parents=True,exist_ok=True)
    for id,filename in specs:
        x=byid[id]
        original_path=IMAGES/filename
        archive=OLD_DIR/filename
        if archive.exists(): assert sha(archive.read_bytes())==originals[id]["sha256"]
        else: shutil.copy2(original_path,archive)
        out=io.BytesIO()
        rendered[id].save(out,format="PNG",optimize=True)
        raw=out.getvalue()
        assert len(raw)>25000 and rendered[id].width>=1200 and rendered[id].height>=600
        original_path.write_bytes(raw)
        urls=[sources[k][1]["sourcePage"] for k in mapping[id]]
        x.update(sha256=sha(raw),size=len(raw),
          author=("CHORDATA original Scoliodon anatomy and Jon Houseman" if "scoliodon" in id else
                  "Jon Houseman" if "scale" in id else "Maija Karala"),
          license="CC BY-SA 3.0 Unported (attributed teaching composite)",
          licenseUrl=LICENCE,sourceUrl=urls[0],sourceUrls=urls,
          sourceSha256=[sources[k][1]["sha256"] for k in mapping[id]],
          modifications="The published images were proportionally laid out on a labelled teaching page; original anatomical source pixels were not synthetically invented.",
          reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_DEVICE_REVIEW_PENDING",
          visualReview="SOURCE_BASED_TEACHING_PLATE_QA_PROVISIONAL",
          pedagogicStatus="REPLACED_FROM_LOW_UTILITY_TEACHING_FIGURE_2026-11-12",
          retiredSchematicPng="docs/retired_noninstructional_png/"+filename,
          retiredSchematicSha256=originals[id]["sha256"])
        for k in ("svgMaster","svgSha256","pedagogicReason"):x.pop(k,None)
        if id==specs[0][0]:
            x["keyEn"]="Scoliodon-specific labelled digestive schematic enlarged for reading. Comparative dogfish (Squalus) preparation is explicitly identified as a DIFFERENT genus; never treat this comparison as Scoliodon specimen evidence. Rectal gland secretes salt, not digestive enzymes."
            x["editorialCaution"]="The Houseman inset is Squalus, not Scoliodon. Exact Scoliodon anatomy follows the preserved source original."
        elif id==specs[1][0]:
            x["keyEn"]="Ganoid scales are rhomboid, cycloid scales smooth-edged, ctenoid scales possess posterior ctenii, and placoid denticles are tooth-like structures. Source labels expanded for mobile reading."
        else:
            x["keyEn"]="The Devonian fossils Eusthenopteron, Panderichthys, Tiktaalik, Acanthostega and Ichthyostega illustrate branching tetrapodomorph evolution; the depicted fossils are not necessarily direct ancestors of one another."
        full_provenance.append(dict(diagramId=id,installedPath=x["path"],installedSha256=sha(raw),
            original=originals[id],sources=[sources[k][1] for k in mapping[id]],
            academicReview="PROVISIONAL_QA_NOT_INDEPENDENTLY_APPROVED"))
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    MARKER.parent.mkdir(parents=True,exist_ok=True)
    MARKER.write_text(json.dumps({"figureCount":3,"figures":full_provenance},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGED 3 source-based classroom images, retained 64 slots and archived 3 original PNGs")
if __name__=="__main__":
    import urllib.parse
    main()
