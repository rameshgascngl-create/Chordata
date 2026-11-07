#!/usr/bin/env python3
"""Original educational shark septal-gill plate. No external artwork reproduced."""
import csv,hashlib,json,math,subprocess
from pathlib import Path
from xml.sax.saxutils import escape
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
PNG=ASSETS/"pencil_plates/shark_gill_flow.png"
SVG=ROOT/"docs/original_plate_svg/shark_septal_gills_en.svg"
MANIFEST=ASSETS/"pencil_plates/manifest.json"
LEDGER=ROOT/"docs/figure-coverage.tsv"
REVIEW=ROOT/"docs/qa-image-review/shark_septal_gills_wave4_review.png"
REPORT=ROOT/"docs/CHORDATA_SHARK_SEPTAL_GILLS_WAVE4_QA.md"
TRIAGE=ROOT/"docs/CHORDATA_VISUAL_QUALITY_TRIAGE_64_20261107.md"
ID="u2-scoliodon-gills-labelled"
OLD="2df65ff07a18ba37f84c15e8d1daf038adfd5f113283f5b718fbb77a5479c413"
AUTHOR="CHORDATA QA project — original vector shark septal-gill teaching schematic"
REFS=[
 "https://dlnr.hawaii.gov/sharks/anatomy/gills-respiration/",
 "https://journals.physiology.org/doi/full/10.1152/physrev.00050.2003",
 "https://www.amnh.org/learn-teach/resources-for-learning/hall-of-ocean-life/water-vertebrates-breathing"
]
W,H=3200,2380
INK="#203a4a";BLUE="#1379a3";RED="#bd5363";SOFT="#5b7080";LINE="#d4dee2"
g=[]
def add(v):g.append(v)
def path(d,fill="none",color=INK,width=5):
 add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
def rect(x,y,w,h,color="white",border="none",width=2,r=0):
 add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{color}" stroke="{border}" stroke-width="{width}"/>')
def ellipse(x,y,rx,ry,color,border="none",width=3):
 add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{color}" stroke="{border}" stroke-width="{width}"/>')
def line(x,y,X,Y,color=INK,width=4):
 add(f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')
def text(x,y,s,size=31,bold=False,color=INK,anchor="start"):
 add(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="DejaVu Sans, sans-serif" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(s)}</text>')
def arrow(x,y,X,Y,color=BLUE,width=10,head=26):
 line(x,y,X,Y,color,width)
 t=math.atan2(Y-y,X-x)
 a=t+math.pi-0.52;b=t+math.pi+0.52
 add(f'<polygon points="{X},{Y} {X+head*math.cos(a):.1f},{Y+head*math.sin(a):.1f} {X+head*math.cos(b):.1f},{Y+head*math.sin(b):.1f}" fill="{color}"/>')

def draw():
 g.clear()
 add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
 rect(0,0,W,H,"#fcfaf6")
 text(94,120,"SHARK SEPTAL GILLS — STRUCTURE & WATER FLOW",75,True)
 text(100,190,"Requiem-shark model · original explanatory line art · English-labelled",38,False,SOFT)
 for x,y,w,h in ((80,260,1440,780),(1560,260,1560,1290),(80,1080,1440,1160),(1560,1590,1560,650)):
  rect(x,y,w,h,"white",LINE,3,25)
 # A. External morphology; five separate lateral gill slits.
 text(122,337,"A  HEAD & FIVE EXTERNAL GILL SLITS",43,True)
 text(123,396,"Lateral view · simplified, not a dissection",30,False,SOFT)
 path("M 205 674 C 254 584 410 503 613 478 C 800 459 1012 462 1425 507 L 1471 756 C 1212 751 1111 768 991 805 C 907 814 810 771 706 758 C 510 762 342 730 205 674 Z","#c3d4cf",INK,8)
 path("M 206 674 C 274 641 346 644 387 655 C 441 668 497 678 545 677",color="#638186",width=6)
 path("M 272 694 L 457 707",width=7)
 ellipse(543,580,35,27,"#f5f4ee",INK,6);ellipse(545,583,13,13,"#203a4a")
 for i in range(5):
  x=724+i*52;y=565+i*2
  path(f"M {x} {y} Q {x-22} {y+62} {x-8} {y+135}",color=INK,width=13)
  path(f"M {x+9} {y+8} Q {x-2} {y+64} {x+1} {y+129}",color="#829ba1",width=4)
 path("M 1021 719 Q 1094 785 1134 955 Q 1205 912 1192 829 Q 1172 770 1117 733 Z","#98afb2",INK,7)
 line(793,526,800,460,INK,3);text(803,449,"Five external slits",31,True)
 line(540,538,514,470,INK,3);text(356,451,"Lateral eye",29)
 text(128,991,"Water exits separately; no bony operculum.",31,False,SOFT)
 # B. Pouch/septa cutaway with water channel visible.
 text(1600,339,"B  CUTAWAY · ONE GILL POUCH",43,True)
 text(1602,393,"Generalised section; adjacent septa form a water chamber",29,False,SOFT)
 rect(1617,477,211,815,"#d9eef4","#9ac6d4",3,18)
 text(1723,606,"PHARYNX",30,True,BLUE,"middle")
 text(1723,652,"water enters",28,False,BLUE,"middle")
 path("M 1865 501 Q 1927 573 1917 704 Q 1911 836 1870 1000",color="#6e888a",width=35)
 path("M 1915 539 C 2130 483 2465 504 2831 551 L 2881 600 C 2470 571 2130 570 1921 614 Z","#aabfc0",INK,6)
 path("M 1915 1032 C 2121 976 2460 988 2835 1033 L 2882 1094 C 2465 1064 2125 1060 1914 1106 Z","#aabfc0",INK,6)
 path("M 2881 467 Q 2933 544 2903 639",color="#92abad",width=24)
 path("M 2903 954 Q 2938 1043 2896 1174",color="#92abad",width=24)
 for i in range(16):
  x=1970+i*53;top=590-17*math.sin(i/5);bottom=994+10*math.sin(i/5)
  path(f"M {x} {top:.1f} Q {x+15} {top+65:.1f} {x+8} {top+130:.1f}",color="#c46465",width=15)
  path(f"M {x} {bottom:.1f} Q {x+13} {bottom-58:.1f} {x+7} {bottom-119:.1f}",color="#c46465",width=15)
 for y in (767,814,861):arrow(1820,y,2821,y,BLUE,9,27)
 text(2150,467,"Interbranchial septum",32,True);line(2335,475,2380,518,SOFT,3)
 text(2056,1196,"Gill filaments (hemibranchs)",30,True);line(2290,1165,2300,986,SOFT,3)
 text(1647,1373,"Gill arch (cartilage)",30,True);line(1900,1250,1892,1040,SOFT,3)
 text(2950,790,"GILL",30,True);text(2950,829,"SLIT",30,True)
 text(1608,1474,"Water: pharynx → filaments/lamellae → external slit",31,True,BLUE)
 text(1608,1519,"Interbranchial septa persist in sharks.",28,False,SOFT)
 # C. Enlarged primary filament with multiple secondary lamellae.
 text(123,1160,"C  GILL FILAMENT & SECONDARY LAMELLAE",40,True)
 text(123,1218,"Diagrammatic enlargement of vascular gas-exchange surfaces",29,False,SOFT)
 path("M 268 1670 Q 338 1560 478 1560 L 1208 1572 Q 1293 1578 1310 1632 Q 1242 1712 1100 1723 L 456 1725 Q 327 1728 268 1670 Z","#efb6ad",RED,7)
 for i in range(15):
  x=420+i*51
  path(f"M {x} 1578 C {x-34} 1508 {x-35} 1376 {x+9} 1320 C {x+53} 1370 {x+49} 1509 {x+17} 1584 Z","#f8d7cc",RED,5)
  path(f"M {x} 1700 C {x-26} 1762 {x-34} 1885 {x+8} 1928 C {x+49} 1880 {x+48} 1763 {x+18} 1702 Z","#f8d7cc",RED,5)
 arrow(273,1286,1288,1286,BLUE,12,35);text(284,1260,"Water over lamellar surfaces",30,True,BLUE)
 text(130,2004,"Secondary lamellae",28,True);line(505,1986,482,1847,INK,3)
 text(784,2004,"Primary gill filament",28,True);line(1110,1979,1140,1711,INK,3)
 arrow(304,2064,669,2064,BLUE,8,23);text(701,2078,"Water direction",26,True,BLUE)
 arrow(1160,2141,791,2141,RED,8,23);text(303,2146,"Blood in lamellae: countercurrent",27,True,RED)
 # D. Structural reading key.
 text(1603,1678,"D  STRUCTURAL READING KEY",44,True)
 legend=(("1","Gill arch","Cartilaginous support for the branchial apparatus."),
         ("2","Interbranchial septum","Partition between adjacent branchial pouches."),
         ("3","Hemibranch","Filaments on one side of a supporting gill arch."),
         ("4","Secondary lamellae","Thin vascular surfaces for gas exchange."))
 for i,(num,label,desc) in enumerate(legend):
  y=1750+i*108
  ellipse(1645,y-13,27,27,"#e3eff4",BLUE,3)
  text(1645,y,num,29,True,BLUE,"middle")
  text(1704,y-13,label,34,True);text(1704,y+27,desc,28,False,SOFT)
 line(99,2290,3098,2290,LINE,3)
 text(107,2331,"ORIGINAL QA SCHEMATIC · not a specimen dissection or species-specific micrograph",27,False,SOFT)
 text(3095,2331,ID,25,True,SOFT,"end")
 add("</svg>")
 return "\n".join(g)+"\n"

def main():
 drawing=draw()
 SVG.parent.mkdir(parents=True,exist_ok=True)
 SVG.write_text(drawing,encoding="utf-8")
 PNG.parent.mkdir(parents=True,exist_ok=True)
 cairosvg.svg2png(bytestring=drawing.encode(),write_to=str(PNG),output_width=W,output_height=H)
 raw=PNG.read_bytes()
 if not(raw[:8]==b"\x89PNG\r\n\x1a\n" and len(raw)>120000):
  raise ValueError("Detailed anatomical PNG absent")
 image_sha=hashlib.sha256(raw).hexdigest()
 svg_sha=hashlib.sha256(drawing.encode()).hexdigest()
 manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
 matches=[x for x in manifest["figures"] if x["diagramId"]==ID and x["lang"]=="shared"]
 if len(matches)!=1 or matches[0]["path"]!="pencil_plates/shark_gill_flow.png":
  raise ValueError("Gill diagram placement changed")
 entry=matches[0]
 if entry["sha256"] not in (OLD,image_sha):
  raise ValueError("Refusing to overwrite independently modified image")
 entry.update(
  author=AUTHOR,license="Original project illustration — scientific review pending",
  sourceUrl="",referenceUrl=REFS[0],referenceUrls=REFS,
  modifications="Original programmatic educational drawing, not copied from any reference figure",
  keyEn=("Shark septal-gill overview: five gill slits, interbranchial septa, "
    "gill arches, hemibranchs, primary filaments, secondary lamellae, "
    "and conceptual countercurrent exchange. This is not species-specific dissection."),
  keyTa=("சுறாக்களின் இடைத்தடுப்புடைய செவுள்கள்: ஐந்து இணை வெளிப்புறச் செவுள் "
    "பிளவுகள், செவுள் வளைவுகள், இடைச்செவுள் தடுப்புகள், செவுள் இழைகள், "
    "இரண்டாம் நிலைச் செவுள் தகடுகள் ஆகியன. வாயுப் பரிமாற்றத்தில் "
    "எதிரோட்டம் நிகழ்கிறது. இது திட்ட விளக்கப்படம் மட்டுமே."),
  topicId="u2-scoliodon",page=3,sectionKey="respiratory-system",
  learningObjective="Identify shark septal gill arches, interbranchial septa, hemibranchs, lamellae and pharynx-to-gill-slit water flow",
  svgMaster="docs/original_plate_svg/shark_septal_gills_en.svg",svgSha256=svg_sha,
  size=len(raw),sha256=image_sha,visualReview="REPLACED_VISUAL_QA_PENDING",
  reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING")
 MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 with LEDGER.open(newline="",encoding="utf-8") as f:
  reader=csv.DictReader(f,delimiter="\t");columns=reader.fieldnames;rows=list(reader)
 found=[x for x in rows if x["diagramId"]==ID]
 if len(found)!=1:raise ValueError("Coverage register mismatch")
 found[0]["author"]=AUTHOR
 found[0]["referenceSources"]=" | ".join(REFS)
 with LEDGER.open("w",newline="",encoding="utf-8") as f:
  writer=csv.DictWriter(f,fieldnames=columns,delimiter="\t");writer.writeheader();writer.writerows(rows)
 subprocess.run(["python3","scripts/write_figure_review_register.py"],cwd=ROOT,check=True)
 REVIEW.parent.mkdir(parents=True,exist_ok=True)
 cairosvg.svg2png(bytestring=drawing.encode(),write_to=str(REVIEW),output_width=1200,output_height=893)
 REPORT.write_text(
  "# CHORDATA Scoliodon gill structure — original Wave 4 diagram\n\n"
  "Diagram ID: "+ID+"\n\nThis original vector schematic is drawn by the CHORDATA QA project. "
  "It is not a copied figure, or a species-specific dissection. "
  "The detailed diagram depicts the five external gill slits, persistent interbranchial septa, "
  "gill arches, hemibranchs, primary filaments, secondary lamellae, and conceptual water/blood "
  "countercurrent flow. It does not map intralamellar microvasculature.\n\n"
  "Original SVG SHA-256: "+svg_sha+"\nPNG SHA-256: "+image_sha+"\n\n"
  "Anatomical references:\n"+"\n".join("- "+u for u in REFS)+"\n\n"
  "Biology/Tamil independent review and physical-device testing remain pending. "
  "English image labels shared in both reading modes. Production release HOLD.\n",
  encoding="utf-8")
 with TRIAGE.open("a",encoding="utf-8") as f:
  f.write("\n- **Wave 4 staged (provisional)**: original septal shark gill plate replaced "
    "the placeholder u2-scoliodon-gills-labelled. Now 34 of 38 initial high-priority "
    "replacement candidates remain unstaged. All figure approvals are pending.\n")
 print("PASS original Scoliodon septal gills",len(raw),"bytes",image_sha)

if __name__=="__main__":main()
