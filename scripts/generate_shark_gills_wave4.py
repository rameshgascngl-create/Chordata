#!/usr/bin/env python3
"""Draw original shark septal gill teaching plate with explicit anatomy sections."""
import csv, hashlib, json, math, subprocess
from pathlib import Path
from xml.sax.saxutils import escape
import cairosvg

ROOT = Path(__file__).resolve().parents[1] # overridden when committed to scripts/
W,H=3200,2380
INK='#203a4a'; SOFT='#5b7080'; BLUE='#1379a3'; BLUE2='#d9eef4'; RED='#bd5363'; ROSE='#eab3ad'; CREAM='#fcfaf6'; LINE='#d4dee2'; SKIN='#aabfc3'
parts=[]
def add(s):parts.append(s)
def path(d, fill='none',stroke=INK,sw=5,extra=''):
    add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')
def rect(x,y,w,h,fill='white',stroke='none',sw=2,r=0):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def ellipse(cx,cy,rx,ry,fill,stroke='none',sw=3):
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def circle(cx,cy,r,fill,stroke='none',sw=3): add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(x1,y1,x2,y2,c=INK,sw=4,extra=''):
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" {extra}/>')
def text(x,y,s,size=33,weight=400,color=INK,anchor='start'):
    add(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="DejaVu Sans, sans-serif" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')
def arrow(x1,y1,x2,y2,color=BLUE,sw=12,head=25):
    line(x1,y1,x2,y2,color,sw)
    th=math.atan2(y2-y1,x2-x1)
    x,y=x2,y2
    pts=[]
    for delta in [-0.52,0.52]:
        a=th+math.pi+delta
        pts.append(f'{x+head*math.cos(a):.1f},{y+head*math.sin(a):.1f}')
    add(f'<polygon points="{x},{y} {pts[0]} {pts[1]}" fill="{color}"/>')
def tag(x,y,name):text(x,y,name,32,600)

def draw():
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    rect(0,0,W,H,CREAM)
    text(95,118,'SHARK SEPTAL GILLS — STRUCTURE & WATER FLOW',78,700)
    text(98,187,'Scoliodon-type (requiem shark) · original explanatory line plate · English-labelled',39,400,SOFT)
    # four organized plates
    panels=[(80,260,1440,780),(1560,260,1560,1290),(80,1080,1440,1160),(1560,1590,1560,650)]
    for x,y,w,h in panels:
        rect(x,y,w,h,'#ffffff',LINE,3,26)
    # Panel A: lateral anatomical profile with five gill slits
    text(123,338,'A  HEAD & FIVE EXTERNAL GILL SLITS',45,700)
    text(123,390,'Left-side view · not a dissection',31,400,SOFT)
    # head and trunk partial, oriented left
    path('M 205 673 C 252 588, 410 503, 613 478 C 800 459, 1012 461, 1425 507 L 1471 756 C 1212 751, 1111 769, 991 805 C 905 817, 810 770, 706 758 C 510 762, 342 730, 205 673 Z', '#c3d4cf',INK,8)
    path('M 205 673 C 240 640 313 640 370 642 C 424 652 482 671 545 677',stroke='#637e82',sw=7)
    path('M 270 690 C 328 696 380 695 456 701',stroke=INK,sw=7)
    path('M 260 668 C 324 668 375 666 449 672',stroke=INK,sw=4)
    ellipse(542,580,34,26,'#f6f4e9',INK,7)
    circle(544,582,13,'#253742')
    circle(548,574,4,'#ffffff')
    # gill slits are directly posterior to eye; five elongated separate curved streaks
    for i in range(5):
        x=725+i*52
        y=564+i*1.8
        path(f'M {x} {y:.1f} Q {x-22} {y+63:.1f} {x-8} {y+135:.1f}',stroke='#213c4a',sw=13)
        path(f'M {x+9} {y+9:.1f} Q {x-2} {y+64:.1f} {x+1} {y+129:.1f}',stroke='#879aa0',sw=4)
    # pectoral fin after slits
    path('M 1021 719 Q 1093 785 1134 956 Q 1203 912 1192 829 Q 1172 771 1117 733 Z', '#98afb2',INK,7)
    path('M 1062 757 Q 1126 827 1139 901',stroke='#e0e9e6',sw=6)
    # External slit marks are diagnostic; do not imply water flows anteriorly.
    line(787,523,795,460,INK,3)
    text(800,449,'Five paired slits',32,600)
    line(541,541,515,473,INK,3);text(366,455,'Lateral eye',30,500)
    text(126,994,'No bony operculum. Water exits through separate gill slits.',31,500,SOFT)
    # Panel B: true septal gill structural concept section
    text(1603,340,'B  CUTAWAY · ONE GILL POUCH',45,700)
    text(1603,394,'Generalised cross-section; neighbouring septa bound water chamber',31,400,SOFT)
    # pharyngeal side left, epidermis/side skin right
    rect(1618,474,210,820,BLUE2,'#9ac6d4',3,20)
    text(1724,605,'PHARYNX',31,700,BLUE,anchor='middle')
    text(1724,651,'(water in)',30,500,BLUE,anchor='middle')
    # branchial arches at left as strong curved vertical cartilage structures
    path('M 1865 500 Q 1927 567 1916 703 Q 1911 837 1870 1000',stroke='#6c8587',sw=35)
    path('M 1878 502 Q 1938 589 1926 694',stroke='#f0dfc8',sw=8)
    # upper septum horizontal to skin, supports hemibranch
    path('M 1915 538 C 2130 483 2465 504 2831 551 L 2881 600 C 2470 571 2130 570 1921 613 Z','#a9bfc0',INK,6)
    # lower septum
    path('M 1915 1032 C 2121 975 2460 987 2835 1033 L 2882 1094 C 2465 1064 2125 1060 1914 1106 Z','#a9bfc0',INK,6)
    # skin (outer edge) and exit slit (between septa)
    path('M 2881 466 Q 2933 544 2903 639 L 2903 954 Q 2938 1043 2896 1175',stroke='#8aa7a9',sw=25)
    path('M 2895 648 L 2895 951',stroke='#ffffff',sw=18)
    text(2960,770,'GILL',30,700,INK)
    text(2960,810,'SLIT',30,700,INK)
    # gill filaments suspended from upper/lower septa, both face chamber
    for i in range(16):
        x=1970 + i*53
        top=590 - 17*math.sin(i/5)
        path(f'M {x:.1f} {top:.1f} Q {x+15:.1f} {top+65:.1f} {x+8:.1f} {top+130:.1f}',stroke='#c46465',sw=16)
        path(f'M {x+5:.1f} {top+17:.1f} Q {x+20:.1f} {top+61:.1f} {x+11:.1f} {top+109:.1f}',stroke='#f6c5b2',sw=5)
        bottom=994+10*math.sin(i/5)
        path(f'M {x:.1f} {bottom:.1f} Q {x+13:.1f} {bottom-58:.1f} {x+7:.1f} {bottom-119:.1f}',stroke='#c46465',sw=16)
        path(f'M {x+5:.1f} {bottom-15:.1f} Q {x+17:.1f} {bottom-59:.1f} {x+11:.1f} {bottom-102:.1f}',stroke='#f6c5b2',sw=5)
    # water only along open chamber, no false passing through septa
    for y in [767,816,865]:arrow(1820,y,2821,y,BLUE,10,29)
    tag(2150,468,'Interbranchial septum')
    line(2340,476,2390,518,SOFT,4)
    tag(2061,1200,'Gill filaments (hemibranchs)')
    line(2290,1158,2300,978,SOFT,4)
    tag(1645,1376,'Gill arch (cartilage)')
    line(1905,1250,1894,1040,SOFT,4)
    text(1605,1476,'Water: pharynx  →  filaments/lamellae  →  external slit',33,600,BLUE)
    text(1605,1516,'Gill filaments attach to septa; unlike teleosts, the septa persist.',29,400,SOFT)
    # Panel C: filament and secondary lamellae, close-up
    text(124,1162,'C  FILAMENT & SECONDARY LAMELLAE',45,700)
    text(124,1217,'Gas exchange occurs across thin, vascular lamellar surfaces',30,400,SOFT)
    # underlying flattened primary filament horizontally
    path('M 268 1670 Q 338 1560 478 1560 L 1208 1572 Q 1293 1578 1310 1632 Q 1242 1712 1100 1723 L 456 1725 Q 327 1728 268 1670 Z', '#efb6ad',RED,7)
    # secondary lamellae, many thin plates above and below (on paired surfaces)
    for i in range(15):
        x=420+i*51
        path(f'M {x} 1578 C {x-34} 1508 {x-35} 1376 {x+9} 1320 C {x+53} 1370 {x+49} 1509 {x+17} 1584 Z','#f8d7cc',RED,5)
        path(f'M {x+5} 1565 C {x-19} 1500 {x-22} 1406 {x+8} 1365',stroke='#cb6771',sw=5)
        path(f'M {x} 1700 C {x-26} 1762 {x-34} 1885 {x+8} 1928 C {x+49} 1880 {x+48} 1763 {x+18} 1702 Z','#f8d7cc',RED,5)
        path(f'M {x+5} 1710 C {x-13} 1762 {x-22} 1851 {x+9} 1890',stroke='#cb6771',sw=5)
    arrow(273,1286,1288,1286,BLUE,12,35)
    text(285,1260,'Water flow',33,700,BLUE)
    arrow(1203,1642,405,1642,RED,13,36)
    text(145,2008,'Secondary lamellae',31,700)
    line(505,1989,482,1850,INK,3)
    text(790,2008,'Primary gill filament',31,700)
    line(1110,1979,1140,1711,INK,3)
    text(128,2084,'Blood flows opposite to water at exchange surfaces.',31,500,RED)
    text(127,2140,'Opposing streams favour oxygen uptake across the lamellae.',29,500,SOFT)
    # Panel D: intentionally separated, compact teaching legend
    text(1605,1677,'D  STRUCTURAL READING KEY',45,700)
    items=[('1','Gill arch','Cartilage supports the branchial apparatus.'),('2','Interbranchial septum','Tissue partition separating adjacent pouches.'),('3','Hemibranch','Filaments on one side of a supporting arch.'),('4','Secondary lamellae','Thin, vascular surfaces for gas exchange.')]
    for i,(num,name,desc) in enumerate(items):
        y=1748+i*107
        circle(1645,y-13,28,'#e3eff4',BLUE,3)
        text(1645,y-2,num,30,700,BLUE,anchor='middle')
        text(1705,y-14,name,35,700,INK)
        text(1705,y+28,desc,28,400,SOFT)
    # Footer
    line(99,2291,3098,2291,LINE,3)
    text(108,2330,'ORIGINAL QA ILLUSTRATION · anatomy schematic, not a specimen dissection or species-specific micrograph',29,500,SOFT)
    text(3100,2330,'FIGURE u2-scoliodon-gills-labelled',25,600,SOFT,anchor='end')
    add('</svg>')
    return '\n'.join(parts)


def stage():
    svg=draw()
    master=ROOT/"docs/original_plate_svg/scoliodon_septal_gill_structure_en.svg"
    dest=ROOT/"app/src/main/assets/pencil_plates/shark_gill_flow.png"
    preview=ROOT/"docs/qa-image-review/scoliodon_gills_wave4_review.png"
    manifest_path=ROOT/"app/src/main/assets/pencil_plates/manifest.json"
    ledger=ROOT/"docs/figure-coverage.tsv"
    report=ROOT/"docs/CHORDATA_SCOLIODON_GILLS_WAVE4_QA.md"
    for f in (master,dest,preview,report):
        f.parent.mkdir(parents=True,exist_ok=True)
    master.write_text(svg,encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"),write_to=str(dest),output_width=W,output_height=H)
    raw=dest.read_bytes()
    if len(raw)<100000 or not raw.startswith(bytes.fromhex("89504e470d0a1a0a")):
        raise RuntimeError("No substantial original anatomical PNG generated")
    # A matching smaller review sample has the same exact artwork and labels.
    cairosvg.svg2png(bytestring=svg.encode("utf-8"),write_to=str(preview),
                     output_width=1600,output_height=1190)
    sha=hashlib.sha256(raw).hexdigest()
    svgsha=hashlib.sha256(master.read_bytes()).hexdigest()
    data=json.loads(manifest_path.read_text(encoding="utf-8"))
    entries=[z for z in data["figures"] if z["diagramId"]=="u2-scoliodon-gills-labelled"
             and z["lang"]=="shared"]
    if len(entries)!=1 or entries[0]["path"]!="pencil_plates/shark_gill_flow.png":
        raise RuntimeError("Gill slot mapping changed, refusing overwrite")
    entry=entries[0]
    old="2df65ff07a18ba37f84c15e8d1daf038adfd5f113283f5b718fbb77a5479c413"
    if entry["sha256"]!=old:
        raise RuntimeError("Gill source file changed since verified Wave 3; refusing overwrite")
    author="CHORDATA QA — original programmatically drawn shark septal-gill anatomical plate"
    sources=[
      "https://doi.org/10.1152/physrev.00050.2003",
      "https://doi.org/10.1002/jez.10124",
      "https://dlnr.hawaii.gov/sharks/anatomy/gills-respiration/"
    ]
    entry.update(
        author=author,
        size=len(raw),
        sha256=sha,
        license="Original CHORDATA QA illustration (source references cited; no figures copied)",
        reviewStatus="PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
        referenceUrl=sources[0],
        referenceUrls=sources,
        svgMaster="docs/original_plate_svg/scoliodon_septal_gill_structure_en.svg",
        svgSha256=svgsha,
        modifications=("Original vector construction rendered to PNG at 3200 × 2380. "
                       "Four linked views: external five-gill-slit head, one septal "
                       "gill-pouch cross-section, filament/secondary lamellae "
                       "with countercurrent arrows, and explanatory key. "
                       "Scientific reference drawings not reproduced."),
        visualReview="REPLACED_VISUAL_QA_PENDING",
        keyEn=("Sharks have five pairs of external gill slits. Water enters via the mouth "
               "and pharynx, passes over gill filament secondary lamellae supported by "
               "interbranchial septa and exits individual external slits. The gill arch "
               "supports hemibranchs; blood and water flow in opposite directions "
               "across lamellar exchange surfaces. This is a generalised schematic, "
               "not a histological section; sharks lack the bony operculum of teleosts."),
        keyTa=("சுறாக்களில் ஐந்து இணை வெளிச் செவுள் பிளவுகள் உள்ளன. வாயின் வழியாக "
               "உள்நுழையும் நீர் தொண்டைப் பகுதியிலிருந்து செவுள் இழைகளின் இரண்டாம் "
               "நிலைச் சுவாசத் தகடுகளின் மேல் செல்கிறது. செவுள் இடைச்சுவர்கள் "
               "செவுள் இழைகளைத் தாங்குகின்றன. நீரோட்டமும் இரத்த ஓட்டமும் "
               "எதிரெதிர்த் திசைகளில் நடைபெறுவதால் வாயுப் பரிமாற்றம் "
               "திறம்பட நடைபெறுகிறது. இது விளக்கக் கோட்டோவியம்; "
               "எலும்புமீன்களின் எலும்பாலான செவுள் மூடி இச்சுறாவில் இல்லை.")
    )
    manifest_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",
                             encoding="utf-8")
    with ledger.open(newline="",encoding="utf-8") as f:
        rd=csv.DictReader(f,delimiter="\t")
        fields,rows=rd.fieldnames,list(rd)
    matching=[row for row in rows if row["diagramId"]=="u2-scoliodon-gills-labelled"]
    if len(matching)!=1:
        raise RuntimeError("Coverage ledger slot mapping changed")
    matching[0]["author"]=author
    matching[0]["referenceSources"]=" | ".join(sources)
    with ledger.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,delimiter="\t")
        wr.writeheader()
        wr.writerows(rows)
    subprocess.run(["python3","scripts/write_figure_review_register.py"],
                   cwd=ROOT,check=True)
    report.write_text(
      "# Scoliodon respiratory anatomy: septal gills (Wave 4 QA)\n\n"
      "Diagram ID: u2-scoliodon-gills-labelled; lesson page 3, respiratory-system.\n"
      "A genuine multi-panel explanatory anatomical line plate replaces the "
      "original numbered boxes-and-lines flowchart.\n\n"
      "Original illustration by the CHORDATA QA project, constructed using "
      "explicit anatomical geometry. No source image, museum photograph, "
      "or third-party figure is reproduced.\n\n"
      "Teaching references:\n- "+" \n- ".join(sources)+"\n\n"
      "Scientific notes: typical elasmobranch septal gills with four holobranchs "
      "and the first hemibranch, five bilateral slits, filament-bearing "
      "interbranchial septa, thin secondary lamellae, no bony operculum. "
      "Panel B is a teaching cutaway, not a literal histological transverse slice.\n\n"
      "PNG file: app/src/main/assets/pencil_plates/shark_gill_flow.png\n"
      "PNG SHA-256: "+sha+"\n"
      "PNG bytes: "+str(len(raw))+"\n"
      "SVG master: "+str(master.relative_to(ROOT))+"\n"
      "SVG SHA-256: "+svgsha+"\n"
      "Provisional only: independent scientific and Tamil review, full-resolution "
      "labels, and physical-device tests remain pending. Production release on HOLD.\n",
      encoding="utf-8"
    )
    print("PASS: staged original detailed shark septal gill PNG",len(raw),sha)

if __name__=="__main__":
    stage()
