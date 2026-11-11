#!/usr/bin/env python3
"""Correct two topologically under-specified CHORDATA teaching plates.

Renders original vector schematics, with no third-party illustration copied.
These teach relationships rather than a naturalistic dissection layout.
Both remain PROVISIONAL until independent anatomical review.

References:
  Rana: https://readingroo.ms/7/7/5/6/77560/77560-h/77560-h.htm
  Rana: https://tnou.ac.in/NAAC/SSR/C1/1.1.5/MZON-P1.pdf
  Squamate: https://pmc.ncbi.nlm.nih.gov/articles/PMC3673951/
"""
from pathlib import Path
import hashlib, json
import svgwrite, cairosvg

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'app/src/main/assets/pencil_plates/manifest.json'
PNG_DIR = MANIFEST.parent
SVG_DIR = ROOT / 'docs/original_plate_svg'
W, H = 1800, 1120
BG = '#ffffff'; INK = '#263943'; MUTED = '#617781'; EDGE = '#bdd0cd'
BLUE = '#32728a'; RED = '#b96051'; TEAL = '#4c887d'; GOLD = '#ba8549'
PALE = '#f0f5f3'; LIGHT = '#e3efeb'

def base(title, subtitle):
    d = svgwrite.Drawing(size=(W,H), viewBox=f'0 0 {W} {H}', profile='full')
    d.add(d.rect(insert=(0,0), size=(W,H), fill=BG))
    txt(d,title,75,91,58,True)
    txt(d,subtitle,77,142,27,False,MUTED)
    line(d,[(75,170),(1725,170)],BLUE,4)
    txt(d,'ORIGINAL TOPOLOGICAL SCHEMATIC · NOT TO SCALE · INDEPENDENT BIOLOGY REVIEW PENDING',75,1080,20,False,MUTED)
    return d

def txt(d,s,x,y,size=25,bold=False,col=INK,anchor='start'):
    d.add(d.text(s,insert=(x,y),font_family='DejaVu Sans',font_weight='bold' if bold else 'normal',font_size=size,fill=col,text_anchor=anchor))

def line(d,pts,col=INK,width=5,dashed=False):
    kw=dict(fill='none',stroke=col,stroke_width=width,stroke_linejoin='round',stroke_linecap='round')
    if dashed: kw['stroke_dasharray']='12 10'
    d.add(d.polyline(points=pts,**kw))

def path(d,cmd,col=INK,width=5,dashed=False):
    kw=dict(d=cmd,fill='none',stroke=col,stroke_width=width,stroke_linecap='round',stroke_linejoin='round')
    if dashed: kw['stroke_dasharray']='12 10'
    d.add(d.path(**kw))

def ellipse(d,c,r,fill=LIGHT,stroke=INK,width=4):
    d.add(d.ellipse(center=c,r=r,fill=fill,stroke=stroke,stroke_width=width))

def box(d,x,y,w,h,title,subtitle='',fill=PALE):
    d.add(d.rect(insert=(x,y),size=(w,h),rx=18,ry=18,fill=fill,stroke=EDGE,stroke_width=3))
    txt(d,title,x+20,y+38,24,True)
    if subtitle: txt(d,subtitle,x+20,y+72,19,False,MUTED)

def arrow(d,x,y,dx,dy,col=BLUE):
    # compact arrowhead at a vessel end, tangent to path
    from math import atan2,cos,sin
    a=atan2(dy,dx)
    tri=[(x,y),(x-16*cos(a-.48),y-16*sin(a-.48)),(x-16*cos(a+.48),y-16*sin(a+.48))]
    d.add(d.polygon(points=tri,fill=col))

def frog():
    d=base('Adult frog — paired arterial arches','Connection map: two trunks, three arch pairs, joined systemic arches and dorsal aorta')
    d.add(d.rect(insert=(85,206),size=(1630,793),rx=24,ry=24,fill=PALE,stroke=EDGE,stroke_width=3))
    # Pairs labelled on opposite sides, not dissection-sided anatomical coordinates.
    txt(d,'ONE SIDE',404,258,25,True,BLUE,'middle')
    txt(d,'OPPOSITE SIDE',1396,258,25,True,BLUE,'middle')
    # Heart, anatomical sequence, outflow from ventricle not atria.
    ellipse(d,(818,754),(64,49),'#f0dfd9',RED)
    ellipse(d,(982,754),(64,49),'#f0dfd9',RED)
    ellipse(d,(900,859),(123,99),'#f0dfd9',RED,6)
    txt(d,'Right atrium',815,741,18,True,INK,'middle')
    txt(d,'Left atrium',988,741,18,True,INK,'middle')
    txt(d,'Single',900,850,22,True,INK,'middle')
    txt(d,'ventricle',900,881,22,True,INK,'middle')
    # The shared truncus arises from ventricle, divides into bilateral arterial trunks.
    path(d,'M900 772 L900 597 Q900 559 860 546 L744 520',RED,10)
    path(d,'M900 597 Q900 559 940 546 L1056 520',RED,10)
    txt(d,'Truncus arteriosus',900,481,22,True,INK,'middle')
    # Left and right bilateral trunk branch nodes.
    ellipse(d,(730,514),(9,9),BLUE,BLUE,1); ellipse(d,(1070,514),(9,9),BLUE,BLUE,1)
    # CAROTID from each side, directed anteriorly: split internal/external.
    path(d,'M730 514 Q665 453 595 398 Q510 340 455 311',BLUE,8)
    path(d,'M1070 514 Q1135 453 1205 398 Q1290 340 1345 311',BLUE,8)
    # carotid branch bifurcation on each side
    path(d,'M455 311 Q406 288 371 272',BLUE,5); path(d,'M455 311 Q496 288 523 272',BLUE,5)
    path(d,'M1345 311 Q1304 288 1277 272',BLUE,5);path(d,'M1345 311 Q1394 288 1429 272',BLUE,5)
    arrow(d,371,272,-5,-3); arrow(d,523,272,5,-3);arrow(d,1277,272,-5,-3);arrow(d,1429,272,5,-3)
    txt(d,'CAROTID PAIR',899,292,27,True,BLUE,'middle')
    txt(d,'External + internal carotids → head',899,328,20,False,MUTED,'middle')
    # SYSTEMIC: two arches loop caudally and unite into unpaired dorsal aorta.
    path(d,'M730 514 Q607 492 588 566 Q526 726 726 918 L900 968',TEAL,9)
    path(d,'M1070 514 Q1193 492 1212 566 Q1274 726 1074 918 L900 968',TEAL,9)
    path(d,'M900 968 L900 1012',TEAL,10)
    arrow(d,900,1008,0,8,TEAL)
    txt(d,'SYSTEMIC ARCH',390,764,22,True,TEAL,'middle')
    txt(d,'SYSTEMIC ARCH',1410,764,22,True,TEAL,'middle')
    txt(d,'Dorsal aorta',1020,997,23,True,TEAL,'middle')
    # Pulmocutaneous arteries from side trunks, branching individually to lungs/skin.
    path(d,'M730 514 Q653 584 533 651',GOLD,8)
    path(d,'M1070 514 Q1147 584 1267 651',GOLD,8)
    # distal bifurcations
    path(d,'M533 651 Q479 606 382 609',GOLD,6)
    path(d,'M533 651 Q477 700 382 710',GOLD,6)
    path(d,'M1267 651 Q1323 606 1418 609',GOLD,6)
    path(d,'M1267 651 Q1323 700 1418 710',GOLD,6)
    for x,y,v in [(382,609,-1),(382,710,-1),(1418,609,1),(1418,710,1)]: arrow(d,x,y,v,0,GOLD)
    txt(d,'Skin',296,610,23,True,GOLD,'middle');txt(d,'Lung',296,713,23,True,GOLD,'middle')
    txt(d,'Skin',1503,610,23,True,GOLD,'middle');txt(d,'Lung',1503,713,23,True,GOLD,'middle')
    txt(d,'PULMOCUTANEOUS PAIR',900,386,25,True,GOLD,'middle')
    txt(d,'Pulmonary + cutaneous branches on each side',900,418,19,False,MUTED,'middle')
    txt(d,'Diagram shows bilateral connectivity; paths and organ positions are schematic.',900,1044,23,False,MUTED,'middle')
    return d

def calotes():
    d=base('Calotes — functionally subdivided heart','Squamate circulation: three communicating ventricular regions; three major outflow vessels')
    d.add(d.rect(insert=(85,209),size=(1630,812),rx=22,ry=22,fill=PALE,stroke=EDGE,stroke_width=3))
    # Atria isolated: left receives pulmonary venous blood, right systemic venous return.
    ellipse(d,(465,368),(170,74),'#f4e2dc',RED,5)
    ellipse(d,(1260,368),(170,74),'#e1ecf0',BLUE,5)
    txt(d,'Left atrium',465,361,28,True,INK,'middle')
    txt(d,'Pulmonary venous return',465,398,18,False,MUTED,'middle')
    txt(d,'Right atrium',1260,361,28,True,INK,'middle')
    txt(d,'Systemic venous return',1260,398,18,False,MUTED,'middle')
    # Single ventricular outline; cava are communicating regions not separate true ventricles.
    d.add(d.rect(insert=(230,527),size=(1260,315),rx=132,ry=132,fill='#f4e5e0',stroke=RED,stroke_width=8))
    # Incomplete septa are dashed to show communications.
    path(d,'M676 557 Q716 626 698 683',TEAL,5,True)
    path(d,'M698 732 Q681 781 676 813',TEAL,5,True)
    path(d,'M1088 556 Q1028 620 1060 689',TEAL,5,True)
    path(d,'M1060 744 Q1090 775 1100 813',TEAL,5,True)
    txt(d,'Cavum',488,641,30,True,INK,'middle')
    txt(d,'arteriosum',488,682,30,True,INK,'middle')
    txt(d,'Cavum',872,641,30,True,INK,'middle')
    txt(d,'venosum',872,682,30,True,INK,'middle')
    txt(d,'Cavum',1249,641,30,True,INK,'middle')
    txt(d,'pulmonale',1249,682,30,True,INK,'middle')
    txt(d,'Vertical',692,865,20,False,MUTED,'middle')
    txt(d,'septal region',692,891,20,False,MUTED,'middle')
    txt(d,'Muscular ridge',1059,865,20,False,MUTED,'middle')
    # Overtly schematic flow routes inside the ventricle.
    path(d,'M465 444 L465 530',RED,8); arrow(d,465,530,0,8,RED)
    path(d,'M1260 444 Q1113 466 972 528',BLUE,8);arrow(d,972,528,-7,4,BLUE)
    path(d,'M642 748 Q800 801 914 748',RED,7);arrow(d,914,748,9,-1,RED)
    txt(d,'Intercavitary flow',784,818,19,False,MUTED,'middle')
    path(d,'M980 738 Q1100 805 1208 738',BLUE,7);arrow(d,1208,738,8,-2,BLUE)
    # Systemic arches arise from central cavum venosum outflow region, not separate atria.
    path(d,'M875 531 Q887 464 907 439 L904 311',TEAL,9)
    path(d,'M904 310 Q825 285 795 280',TEAL,7)
    path(d,'M904 310 Q991 285 1008 280',TEAL,7)
    arrow(d,795,280,-8,-2,TEAL);arrow(d,1008,280,8,-2,TEAL)
    txt(d,'Right + left systemic aortae',902,251,22,True,TEAL,'middle')
    # Pulmonary artery emerges from the cavum pulmonale side.
    path(d,'M1380 624 Q1500 605 1540 513',BLUE,9);arrow(d,1540,513,6,-9,BLUE)
    txt(d,'Pulmonary',1544,460,23,True,BLUE,'middle')
    txt(d,'artery',1544,490,23,True,BLUE,'middle')
    txt(d,'The three ventricular regions are not fully separated.',900,936,25,True,INK,'middle')
    txt(d,'Arrows show predominant routes; intracardiac shunting varies with physiology.',900,972,23,False,MUTED,'middle')
    return d

SPECS={
    'u3-rana-arterial-system': ('frog_arterial_system_en',frog, [
        'https://readingroo.ms/7/7/5/6/77560/77560-h/77560-h.htm',
        'https://tnou.ac.in/NAAC/SSR/C1/1.1.5/MZON-P1.pdf'
    ],'Bilateral carotid, systemic, and pulmocutaneous branches arise from the truncus; the systemic arches join into the dorsal aorta.'),
    'u4-calotes-arterial-system':('calotes_heart_arteries_en',calotes,[
        'https://pmc.ncbi.nlm.nih.gov/articles/PMC3673951/',
        'https://www.dcceew.gov.au/sites/default/files/env/pages/dc11235d-8b3b-43f7-b991-8429f477a1d4/files/24-fauna-2a-squamata-morphology.pdf'
    ],'Functionally subdivided ventricle: cavum arteriosum, cavum venosum, cavum pulmonale; two systemic aortae and pulmonary artery.'),
}

def main():
    SVG_DIR.mkdir(parents=True,exist_ok=True)
    records=json.loads(MANIFEST.read_text(encoding='utf-8'))
    for entry in records['figures']:
        if entry['diagramId'] not in SPECS or entry['lang'] != 'en': continue
        stem,fn,refs,objective=SPECS[entry['diagramId']]
        svg=SVG_DIR/(stem+'.svg'); png=PNG_DIR/(stem+'.png')
        svg.write_text(fn().tostring(),encoding='utf-8')
        cairosvg.svg2png(url=str(svg),write_to=str(png),output_width=W,output_height=H)
        entry['sha256']=hashlib.sha256(png.read_bytes()).hexdigest()
        entry['size']=png.stat().st_size
        entry['svgSha256']=hashlib.sha256(svg.read_bytes()).hexdigest()
        entry['svgMaster']='docs/original_plate_svg/'+svg.name
        entry['referenceUrls']=refs
        entry['keyEn']=objective
        entry['visualReview']='SCIENTIFIC_TOPOLOGY_REVISED_PROVISIONAL'
        entry['reviewStatus']='PROVISIONAL_QA_ANATOMICAL_REVIEW_PENDING'
        entry['modifications']='Rebuilt as original topological schematic with bilateral/compartment relationships; no source images reproduced.'
        print(entry['diagramId'],png.name,entry['sha256'])
    MANIFEST.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
