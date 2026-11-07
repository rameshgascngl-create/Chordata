#!/usr/bin/env python3
"""Credited frog buccal-pump anatomy plus original cutaneous-exchange section.

This shows THREE distinct adult respiratory surfaces. The published four-frame
Jon Houseman illustration is treated as a schematic buccal pump sequence;
specific phases A-D are NOT invented. Skin exchange is original precise QA
artwork backed by OpenStax 29.3 and textbook Zoology-I.
"""
import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
from urllib.request import Request,urlopen
from PIL import Image,ImageDraw,ImageFont,ImageOps

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
PNG=ASSETS/"pencil_plates/rana_respiration_en.png"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
DOC=ROOT/"docs/CHORDATA_FROG_RESPIRATION_SOURCE_QA.md"
PREVIEW=ROOT/"docs/qa-image-review/rana_respiration_review.png"
DIAGRAM="u3-rana-respiration"
SOURCE_FILE="https://upload.wikimedia.org/wikipedia/commons/4/42/Amph001B.png"
SOURCE_PAGE="https://commons.wikimedia.org/wiki/File:Amph001B.png"
CREATOR="Jon Houseman (frog buccal-pump sequence); CHORDATA QA (cutaneous section and layout)"
LICENCE="CC BY-SA 3.0 Unported — adapted composite; source credited"
LICENCE_URL="https://creativecommons.org/licenses/by-sa/3.0/"
REFERENCES=[
 "https://openstax.org/books/biology/pages/29-3-amphibians",
 "https://openstax.org/books/biology-ap-courses/pages/30-1-systems-of-gas-exchange",
 "https://bieap.apcfss.in/Uploads/Materials/Zoology-I.pdf",
]

def font(sz,bold=False):
    filename="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+filename,sz)

def get_source():
    request=Request(SOURCE_FILE,headers={
        "User-Agent":"ChordataQAAnatomyIntake/1.0 (https://github.com/rameshgascngl-create/Chordata)",
        "Referer":"https://commons.wikimedia.org/","Accept":"image/png"})
    with urlopen(request,timeout=50) as response:
        raw=response.read(500000)
    if not 10000<len(raw)<500000: raise ValueError("Original frog source byte limit violation")
    im=Image.open(BytesIO(raw));im.load()
    if im.format!="PNG" or im.size!=(559,992):
        raise ValueError("Unexpected frog illustration format or geometry")
    return im.convert("RGB"),sha256(raw).hexdigest()

def draw_skin_panel(im,origin_x,origin_y):
    d=ImageDraw.Draw(im)
    ox,oy=origin_x,origin_y
    dark="#233d4a"
    def point(x,y):return (ox+x,oy+y)
    d.text(point(40,40),"Cutaneous gas exchange",font=font(45,True),fill=dark)
    d.text(point(40,103),"Original simplified skin section",font=font(30),fill="#4a626a")
    # Surface air/water with dissolved gases; thickened for legibility,
    # actual epidermis and capillaries are thinner, not drawn to scale.
    d.rectangle((ox+60,oy+290,ox+915,oy+365),fill="#f0e9d8",outline=dark,width=5)
    d.text(point(80,300),"Moist skin / epidermis",font=font(32),fill=dark)
    d.rectangle((ox+60,oy+370,ox+915,oy+985),fill="#fff7ed",outline=dark,width=5)
    d.text(point(80,912),"Underlying dermis",font=font(34),fill="#6b594e")
    # A capillary loop below moist surface (oxygen uptake, CO2 loss).
    from math import sin,cos,pi
    pts=[]
    for k in range(100):
        t=2*pi*k/99
        xx=ox+465+320*cos(t)
        yy=oy+690+102*sin(t)
        pts.append((round(xx),round(yy)))
    d.line(pts,fill="#90525d",width=39,joint="curve")
    d.line(pts,fill="#c97e81",width=24,joint="curve")
    d.text(point(285,820),"Superficial blood capillary",font=font(29),fill="#633f44")
    # O2 across the moist epidermis into the superficial blood.
    d.line((ox+305,oy+185,ox+305,oy+526),fill="#316f91",width=13)
    d.polygon([(ox+275,oy+505),(ox+335,oy+505),(ox+305,oy+553)],fill="#316f91")
    d.text(point(185,214),"O₂ into blood",font=font(37,True),fill="#316f91")
    # CO2 from capillary towards exterior.
    d.line((ox+680,oy+530,ox+680,oy+187),fill="#a15b34",width=13)
    d.polygon([(ox+650,oy+210),(ox+710,oy+210),(ox+680,oy+167)],fill="#a15b34")
    d.text(point(610,215),"CO₂ out",font=font(37,True),fill="#a15b34")
    d.text(point(100,1055),"Moist surface and vascular skin",font=font(30),fill=dark)
    d.text(point(100,1098),"are both essential for diffusion.",font=font(30),fill=dark)

def main():
    source,source_sha=get_source()
    art=Image.new("RGB",(3400,1840),"#fffefa")
    d=ImageDraw.Draw(art)
    dark="#19313e"
    d.text((90,60),"Frog respiration — three respiratory surfaces",font=font(78,True),fill=dark)
    d.text((93,157),"Published frog buccal-pump line art plus original cutaneous detail",
           font=font(38),fill="#526773")
    for a,b in [((70,245),(1110,1680)),((1150,245),(2230,1680)),((2270,245),(3335,1680))]:
        d.rounded_rectangle((*a,*b),radius=25,outline="#9fadb4",width=4,fill="white")
    d.text((115,278),"Buccal pressure pump",font=font(46,True),fill=dark)
    d.text((115,343),"A–D: published frog sequence",font=font(33),fill="#46616a")
    display=ImageOps.contain(source,(915,1240),Image.Resampling.LANCZOS)
    art.paste(display,(135+(915-display.width)//2,415+(1240-display.height)//2))
    draw_skin_panel(art,1200,293)
    d.text((2318,290),"Adult frog: three modes",font=font(48,True),fill=dark)
    d.text((2330,420),"1  Cutaneous",font=font(44,True),fill="#26526a")
    d.text((2330,489),"Moist skin and capillaries",font=font(32),fill=dark)
    d.text((2330,540),"exchange O₂ and CO₂.",font=font(32),fill=dark)
    d.line((2300,640,3290,640),fill="#c5cdd2",width=3)
    d.text((2330,680),"2  Buccopharyngeal",font=font(43,True),fill="#26526a")
    d.text((2330,752),"The vascular moist lining",font=font(32),fill=dark)
    d.text((2330,800),"of mouth/pharynx exchanges",font=font(32),fill=dark)
    d.text((2330,850),"respiratory gases.",font=font(32),fill=dark)
    d.line((2300,950,3290,950),fill="#c5cdd2",width=3)
    d.text((2330,990),"3  Pulmonary",font=font(43,True),fill="#26526a")
    d.text((2330,1062),"Lungs are ventilated by a",font=font(32),fill=dark)
    d.text((2330,1110),"buccal force-pump mechanism.",font=font(32),fill=dark)
    d.line((2300,1225,3290,1225),fill="#c5cdd2",width=3)
    d.text((2330,1270),"A–D are not assigned",font=font(32,True),fill="#485f69")
    d.text((2330,1315),"individual breathing phases",font=font(32),fill="#485f69")
    d.text((2330,1360),"without source confirmation.",font=font(32),fill="#485f69")
    d.text((93,1752),"Original frog figures: Jon Houseman (CC BY-SA 3.0)  |  Cutaneous section: CHORDATA QA  |  Diagrams not to scale",
           font=font(31),fill="#4f636b")
    PNG.parent.mkdir(parents=True,exist_ok=True)
    art.save(PNG,"PNG",optimize=True)
    raw=PNG.read_bytes()
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    small=art.copy();small.thumbnail((1220,780),Image.Resampling.LANCZOS)
    small.save(PREVIEW,"PNG",optimize=True)
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    hits=[x for x in m["figures"] if x["diagramId"]==DIAGRAM and x["lang"]=="en"]
    if len(hits)!=1 or hits[0]["path"]!="pencil_plates/rana_respiration_en.png":
        raise ValueError("Frog respiratory lesson ID changed")
    e=hits[0]
    if e["author"] not in ("CHORDATA QA — original computer-assisted anatomical schematic",CREATOR):
        raise ValueError("Refuse overwrite of previously approved source")
    e.update(
        sha256=sha256(raw).hexdigest(),size=len(raw),
        author=CREATOR,license=LICENCE,sourceUrl=SOURCE_PAGE,
        licenseUrl=LICENCE_URL,sourceSha256=[source_sha],
        referenceUrls=REFERENCES,
        modifications=("Original Jon Houseman frog breathing A–D PNG "
                       "was enlarged preserving proportions and displayed beside "
                       "new CHORDATA QA skin-capillary gas-exchange section and "
                       "separate teaching key. No A–D phase functions invented. "
                       "Composite distributed under CC BY-SA 3.0."),
        keyEn=("Cutaneous: moist skin/capillaries. Buccopharyngeal: vascular "
               "lining of mouth/pharynx. Pulmonary: lungs ventilated through "
               "buccal pressure pumping. Published A–D frames are not assigned "
               "individual inspiration/expiration phases."),
        keyTa=("தோல் வழிச் சுவாசம்: ஈரமான தோல், இரத்த நுண்குழாய்கள். "
               "வாய்த்தொண்டைச் சுவாசம்: இரத்தநாளங்கள் நிறைந்த ஈரமான உள்ளுறை. "
               "நுரையீரல் சுவாசம்: வாய்த்தொண்டை அழுத்தப்பம்பு இயக்கம். "
               "A–D படிநிலைகளுக்குத் துல்லியமான கட்டப்பெயர்கள் வழங்கப்படவில்லை."),
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING"
    )
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with LEDGER.open(newline="",encoding="utf-8") as f:
        rdr=csv.DictReader(f,delimiter="\t");fields=rdr.fieldnames;rows=list(rdr)
    match=[r for r in rows if r["diagramId"]==DIAGRAM]
    assert len(match)==1
    match[0]["author"]=CREATOR
    match[0]["referenceSources"]=SOURCE_PAGE+" | "+" | ".join(REFERENCES)
    with LEDGER.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t");w.writeheader();w.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
    DOC.write_text(
        "# CHORDATA frog respiration — credited teaching plate (QA)\n\n"
        "Lesson diagram: "+DIAGRAM+"\n"
        "Original frog buccal pumping drawings: Jon Houseman, "+SOURCE_PAGE+
        "\nCC BY-SA 3.0: "+LICENCE_URL+
        "\nOriginal source SHA-256: "+source_sha+"\n"
        "Derivative PNG SHA-256: "+sha256(raw).hexdigest()+"\n\n"
        "Three respiratory surfaces are explicitly separated; cutaneous "
        "detail was drawn for CHORDATA QA using the following factual sources:\n"+
        "\n".join("- "+u for u in REFERENCES)+"\n"
        "No exact A–D mechanism stage is attributed without evidence.\n\n"
        "Biological and Tamil editorial reviews are pending. "
        "Android emulator/device acceptance not implied.\n",
        encoding="utf-8")
    print(f"PASS: frog respiratory QA source plate {len(raw)} bytes, SHA-256={sha256(raw).hexdigest()}")

if __name__=="__main__":
    main()
