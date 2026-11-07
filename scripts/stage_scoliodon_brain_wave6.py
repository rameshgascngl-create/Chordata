#!/usr/bin/env python3
"""CHORDATA QA Wave 6 original reference-guided dorsal shark brain reconstruction.

Draws an original anatomical interpretation, not copied line-art or verified
milk-shark dissection. Keep anatomy and credits provisional pending review.
"""
from pathlib import Path
from hashlib import sha256
from xml.sax.saxutils import escape
import math,json,csv,subprocess,argparse
import cairosvg

W,H=3200,2400
ink='#233943'; dark='#33464a'; muted='#657b81'; paper='#fbfaf6'; stroke='#4a666d'; organ='#e2e4d6'; olive='#cbd6cb'; cereb='#e0cfb2'; teal='#d2e4df'; minor='#9cb7ae'; gold='#b19b73'
pieces=[]
def add(x):pieces.append(x)
def path(d, fill='none', color=stroke, width=5, extra=''):
 add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def line(x,y,X,Y,color=stroke,width=4, extra=''):
 add(f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" {extra}/>')
def txt(x,y,s,size=30,bold=False,color=ink,align='start'):
 add(f'<text x="{x}" y="{y}" text-anchor="{align}" font-family="DejaVu Sans, Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(s)}</text>')
def ellipse(x,y,rx,ry,fill=organ,color=stroke,width=4,extra=''):
 add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{color}" stroke-width="{width}" {extra}/>')
def rect(x,y,w,h,fill='white',r=0,color='none',width=2):
 add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>')
def leader(side,y,ax,ay,title,subtitle=''):
 x0=720 if side=='L' else 2500
 via=1070 if side=='L' else 2140
 tx=148 if side=='L' else 2520
 path(f'M {x0} {y+7} L {via} {y+7} L {ax} {ay}',color='#69838a',width=3)
 ellipse(ax,ay,7,7,'#365d6a','#365d6a',0)
 txt(tx,y,title,34,True)
 if subtitle:txt(tx,y+44,subtitle,26,False,muted)


def artwork():
 pieces.clear()
 add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
 rect(0,0,W,H,paper)
 txt(100,118,'SCOLIODON-TYPE SHARK BRAIN — DORSAL VIEW',70,True)
 txt(102,185,'Original reference-guided anatomical reconstruction · rostrocaudal orientation · English labels',33,False,muted)
 line(100,223,3095,223,'#b9c6c4',3)
 rect(80,273,3045,1942,'#fffefb',22,'#d1ddda',3)
 # Brain itself is in plane of illustration. Symmetry is only rough; a natural contour is needed.
 # Olfactory sacs, peripheral sensory organs, not brain tissue. Broad lobed lateral paired structures.
 path('M 1178 482 C 1122 433 1082 434 1016 450 C 955 468 922 515 913 560 C 914 617 955 652 1016 652 C 1064 657 1118 630 1152 600 C 1217 644 1304 634 1321 587 C 1339 544 1274 498 1178 482 Z',organ,dark,7)
 path('M 2010 482 C 2066 433 2106 434 2172 450 C 2233 468 2266 515 2275 560 C 2274 617 2233 652 2172 652 C 2124 657 2070 630 2036 600 C 1971 644 1884 634 1867 587 C 1849 544 1914 498 2010 482 Z',organ,dark,7)
 # Olfactory sac visual cues deliberately confined as exterior anatomical context
 for side in (-1,1):
  mid=1594; c=mid+side*510
  for t in range(7):
   ang=t*math.pi/8
   x=c+side*(23+45*math.sin(ang));y=483+t*22
   path(f'M {x:.0f} {y:.0f} q {side*50} 13 {side*95} -2',color='#8b9c91',width=3)
 # Distinct bilobed olfactory bulb embedded medial to sacs; short stems leading to cerebrum
 path('M 1269 531 C 1300 506 1365 516 1405 550 Q 1395 599 1367 620 C 1325 626 1270 597 1269 531 Z',olive,dark,6)
 path('M 1919 531 C 1888 506 1823 516 1783 550 Q 1793 599 1821 620 C 1863 626 1918 597 1919 531 Z',olive,dark,6)
 for x in (1329,1859):
  path(f'M {x-28} 539 Q {x} 572 {x+30} 540',color='#8a9b91',width=4)
  path(f'M {x-26} 579 Q {x} 590 {x+27} 575',color='#8a9b91',width=3)
 # Olfactory peduncles: narrow, continuous anterolateral orientation
 path('M 1391 586 Q 1432 657 1457 755 Q 1470 801 1511 825',color=dark,width=35)
 path('M 1797 586 Q 1756 657 1731 755 Q 1718 801 1677 825',color=dark,width=35)
 path('M 1391 586 Q 1432 657 1457 755 Q 1470 801 1511 825',color='#cdd8ce',width=23)
 path('M 1797 586 Q 1756 657 1731 755 Q 1718 801 1677 825',color='#cdd8ce',width=23)
 for x in (1461,1727):
  path(f'M {x} 707 q -3 42 7 75',color='#8ba197',width=3)
 # Telencephalon broad smooth unpaired organ - not false paired mammalian hemispheres.
 path('M 1519 779 C 1484 763 1448 790 1432 838 C 1416 893 1444 1000 1460 1035 C 1495 1077 1566 1092 1617 1083 C 1695 1076 1745 1025 1755 958 Q 1773 865 1720 818 C 1677 772 1571 756 1519 779 Z',olive,dark,9)
 # Subtle central texture, not a deep false hemispheric median sulcus
 path('M 1504 828 Q 1472 882 1503 1004',color='#9daf9d',width=4)
 path('M 1699 839 Q 1721 911 1685 1024',color='#9daf9d',width=4)
 for y in (854,904,953,1004):
  path(f'M 1496 {y} q 26 -13 61 -3',color='#b5c5b4',width=2)
  path(f'M 1642 {y} q 25 -8 55 5',color='#b5c5b4',width=2)
 # Diencephalon short posterior segment plus midline pineal stalk
 path('M 1515 1062 C 1537 1090 1548 1135 1550 1185 L 1647 1185 C 1644 1137 1664 1089 1682 1055 C 1623 1080 1554 1088 1515 1062 Z',teal,dark,6)
 path('M 1598 1110 Q 1596 1051 1595 1013',color=dark,width=8)
 ellipse(1596,999,15,24,'#edd1a9',dark,3)
 # Optic tectum: two partly exposed broad lobes, MOSTLY concealed by overlap from cerebellum
 path('M 1550 1157 C 1473 1118 1408 1158 1390 1230 C 1374 1296 1410 1358 1472 1352 C 1526 1343 1558 1302 1575 1247 Z',teal,dark,6)
 path('M 1640 1157 C 1717 1118 1782 1158 1800 1230 C 1816 1296 1780 1358 1718 1352 C 1664 1343 1632 1302 1615 1247 Z',teal,dark,6)
 # Cerebellum, enlarged with unmistakable lobulation and longitudinal sulcus.
 path('M 1531 1223 Q 1491 1201 1453 1250 C 1431 1290 1445 1349 1453 1382 Q 1416 1430 1442 1492 C 1436 1566 1507 1659 1587 1680 C 1667 1659 1747 1585 1742 1493 Q 1775 1442 1733 1376 C 1757 1303 1705 1229 1655 1223 C 1601 1194 1553 1208 1531 1223 Z',cereb,dark,9)
 # Lateral auricles and folia (unmistakably cerebellar in dorsal view)
 path('M 1464 1366 Q 1384 1378 1387 1471 C 1400 1541 1433 1580 1460 1539',cereb,dark,6)
 path('M 1725 1366 Q 1805 1378 1802 1471 C 1789 1541 1756 1580 1729 1539',cereb,dark,6)
 for y,amp in [(1297,20),(1360,23),(1435,22),(1517,20),(1594,17)]:
  path(f'M 1474 {y} Q 1520 {y+amp} 1589 {y+6} Q 1662 {y-amp} 1711 {y+1}',color='#987e58',width=7)
  path(f'M 1481 {y+14} Q 1533 {y+amp+18} 1591 {y+20} Q 1658 {y-amp+20} 1704 {y+13}',color='#bbaa8b',width=3)
 path('M 1591 1250 Q 1571 1390 1593 1504 Q 1607 1598 1593 1641',color='#987e58',width=5)
 # Pair of corpora restiformia as lateral ridges on rostral medulla, not true separate circles
 path('M 1467 1612 C 1408 1606 1389 1641 1392 1723 C 1401 1804 1442 1868 1488 1891 C 1507 1837 1512 1724 1467 1612 Z',teal,dark,5)
 path('M 1718 1612 C 1777 1606 1796 1641 1793 1723 C 1784 1804 1743 1868 1697 1891 C 1678 1837 1673 1724 1718 1612 Z',teal,dark,5)
 for x,dx in [(1450,1),(1735,-1)]:
  path(f'M {x} 1664 q {dx*15} 100 {dx*9} 153',color='#8ea79e',width=4)
 # Medulla longitudinal rhomboid taper, central dorsomedian groove + choroid region
 path('M 1520 1677 C 1489 1700 1477 1739 1484 1806 C 1501 1889 1526 2000 1565 2090 L 1619 2090 C 1658 2000 1683 1889 1700 1806 C 1707 1739 1695 1700 1664 1677 C 1614 1698 1571 1698 1520 1677 Z','#e6ebe4',dark,8)
 path('M 1541 1725 L 1592 1823 L 1643 1725 C 1621 1705 1564 1705 1541 1725 Z','#f7f4e7',stroke,4)
 path('M 1592 1830 Q 1585 1936 1592 2048',color='#839b92',width=4)
 for y in (1875,1935,2001):
  path(f'M 1510 {y} q 26 14 50 8',color='#a9bdb0',width=3)
  path(f'M 1674 {y} q -26 14 -50 8',color='#a9bdb0',width=3)
 # Spinal cord narrow without disjoint neck
 path('M 1566 2087 Q 1555 2170 1563 2207 L 1622 2207 Q 1628 2159 1618 2087 Z','#e6ebe4',dark,6)
 path('M 1592 2095 L 1592 2197',color='#8da399',width=3)
 # Delicate cranial nerve root hints only; not falsely number cranial nerves
 for i,y in enumerate((1738,1787,1853,1920)):
  x0=1485+(i//2)*7;x1=1699-(i//2)*7
  path(f'M {x0} {y} q -44 12 -70 45',color='#96876f',width=4)
  path(f'M {x1} {y} q 44 12 70 45',color='#96876f',width=4)
 # Label leaders, robustly separated from anatomy.
 leader('L',500,1115,542,'Olfactory sac','Peripheral sensory epithelium')
 leader('R',595,1857,564,'Olfactory bulb (bilobed)','Distinct from olfactory sac')
 leader('L',749,1444,736,'Olfactory peduncle','Olfactory tract to cerebrum')
 leader('R',923,1709,935,'Cerebrum (telencephalon)','Smooth, massive forebrain')
 leader('L',1084,1572,1164,'Short diencephalon','Pineal stalk visible dorsally')
 leader('R',1192,1783,1263,'Optic lobe (part exposed)','Optic tectum, partly concealed')
 leader('L',1487,1490,1455,'Folded cerebellum','Elongated and enlarged')
 leader('R',1685,1748,1760,'Corpus restiforme','One of paired lateral ridges')
 leader('L',1857,1556,1893,'Medulla oblongata','Dorsal hindbrain / 4th-ventricle region')
 leader('R',2070,1621,2146,'Spinal cord','Continuous with medulla')
 # Overlay orientation axis as minimal discreet elements
 txt(1592,339,'ROSTRAL  /  ANTERIOR',29,True,muted,'middle')
 path('M 1592 363 L 1592 424',color=muted,width=3)
 path('M 1592 363 l -16 22 h32 z',fill=muted,color=muted,width=0)
 # Foot academic traceability
 line(103,2242,3095,2242,'#b9c6c4',3)
 txt(107,2303,'DORSAL ASPECT ONLY · ORIGINAL ANATOMICAL RECONSTRUCTION · NOT SPECIMEN DISSECTION',29,True,muted)
 txt(106,2349,'Shark-type comparison informed by Scoliodon teaching references; biology and label approval pending.',25,False,muted)
 txt(3088,2349,'u2-scoliodon-brain-labelled',24,True,muted,'end')
 add('</svg>')
 return '\n'.join(pieces)+'\n'

ID='u2-scoliodon-brain-labelled'
AUTHOR='CHORDATA QA — original reference-guided shark dorsal brain reconstruction'
REFS=[
 'https://www.bhumipublishing.com/wp-content/uploads/2022/04/Fish-Biology.pdf',
 'https://www.uprtou.ac.in/other_pdf/28062025_UGZY_104.pdf',
 'https://anatomypubs.onlinelibrary.wiley.com/doi/full/10.1002/ar.25028',
 'https://www.sciencedirect.com/topics/veterinary-science-and-veterinary-medicine/olfactory-bulb'
]
OLD='c40c62337fb0798a498d6d87a6edf5bc249e3724054186fc6ab54ad1c000ede9'

def stage(root,svg,png):
 assets=root/'app/src/main/assets';man=assets/'pencil_plates/manifest.json'
 data=json.loads(man.read_text(encoding='utf-8'))
 records=[x for x in data['figures'] if x['diagramId']==ID and x['lang']=='en']
 if len(records)!=1 or records[0]['path']!='pencil_plates/shark_brain_dorsal_en.png':raise ValueError('Figure registry mismatch')
 f=records[0]
 h=sha256(png).hexdigest()
 if f['sha256'] not in (OLD,h):raise ValueError('Refuse independent image modification')
 s=sha256(svg.encode('utf-8')).hexdigest()
 f.update(author=AUTHOR,license='Original CHORDATA QA vector artwork, expert approval pending',sourceUrl='',referenceUrls=REFS,
          modifications='Original SVG reconstruction; no external drawing reproduced/traced; preserved as editable master',
          reviewStatus='PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING',keyEn=(
          'Original Scoliodon-type shark brain (dorsal aspect): paired bilobed olfactory bulbs distinct from olfactory sacs; stout peduncles; smooth cerebrum; short diencephalon and pineal stalk; partly exposed optic lobes; enlarged folded cerebellum; paired corpora restiformia; medulla and spinal cord. Proportions illustrative, not species-specific dissection.'),
          keyTa=('சுறாவகை மூளையின் முதுகுப்புறத் தோற்றம்: மணநுகர்வுப் பைகள், இருமடிப்புடைய மணநுகர்வு முளைகள், மணநுகர்வுத் தண்டுகள், பெருமூளை, இடைமூளை, மேல்நிலை ஒளியுணர்வு மடல்கள், மடிப்புகளுள்ள சிறுமூளை, ரெஸ்டிஃபார்ம் உடல்கள், முகுளம் மற்றும் தண்டுவடம். இது விளக்கப் படம்; மாதிரி உடற்கூறு ஆய்வுப் படம் அல்ல.'),
          svgMaster='docs/original_plate_svg/shark_brain_dorsal_en.svg',svgSha256=s,size=len(png),sha256=h,visualReview='REPLACED_VISUAL_QA_PENDING',
          topicId='u2-scoliodon',page=4,sectionKey='brain',scope='Dorsal shark brain explanatory reconstruction, not a dissected milk-shark specimen',
          learningObjective='Locate paired olfactory bulbs and stalks, smooth telencephalon, pineal stalk, partly hidden optic lobes, folded cerebellum, corpora restiformia, medulla and cord')
 man.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 ledger=root/'docs/figure-coverage.tsv'
 with ledger.open(newline='',encoding='utf-8') as file:
  reader=csv.DictReader(file,delimiter='\t');cols=reader.fieldnames;rows=list(reader)
 m=[r for r in rows if r['diagramId']==ID]; assert len(m)==1
 m[0]['author']=AUTHOR;m[0]['referenceSources']=' | '.join(REFS)
 with ledger.open('w',newline='',encoding='utf-8') as file:
  wr=csv.DictWriter(file,fieldnames=cols,delimiter='\t');wr.writeheader();wr.writerows(rows)
 subprocess.run(['python3','scripts/write_figure_review_register.py'],cwd=root,check=True)
 report=root/'docs/CHORDATA_SCOLIODON_BRAIN_WAVE6_QA.md'
 report.write_text('# Wave 6 — original Scoliodon-type brain dorsal anatomy\n\n'
  'Diagram ID: '+ID+'\n\nOriginal vector illustration, rendered to offline PNG. It is not a copied textbook image or a genuine Rhizoprionodon acutus brain dissection.\n\n'
  'Dorsal anatomy: olfactory sacs separated from bilobed bulbs, elongated tracts, smooth cerebrum, short diencephalon/pineal stalk, partly obscured optic lobes, folded cerebellum, bilateral corpora restiformia, tapering medulla and spinal cord. No ventral-only glands or optic chiasma are misrepresented as dorsal organs.\n\n'
  'References for scientific independent review:\n'+'\n'.join('- '+u for u in REFS)+'\n\n'
  'SVG SHA-256: '+s+'\nPNG SHA-256: '+h+'\n\n'
  'Image creator: '+AUTHOR+'\nRights: original QA project illustration; no external copyrighted source figure reproduced.\n'
  'Editorial and visual status: PROVISIONAL, not independently accepted. Review label target placement at phone-scale and Tamil textbook terms separately. Production HOLD.\n',encoding='utf-8')
 triage=root/'docs/CHORDATA_VISUAL_QUALITY_TRIAGE_64_20261107.md'
 with triage.open('a',encoding='utf-8') as file:
  file.write('\n- **Wave 6 staged (provisional)**: `u2-scoliodon-brain-labelled` rebuilt as original reference-guided dorsal brain with separate sensory sacs and bulbs, smooth forebrain, folded cerebellum, partially exposed optic lobes and paired restiformia; **32 of the original 38 high-priority figures remain unstaged**. Biological and Tamil reviews/real-device QA pending.\n')
 print('Wave 6 staged brain',len(png),h,s)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview-dir',default=None);args=ap.parse_args()
 svg=artwork()
 if args.preview_dir:
  dest=Path(args.preview_dir);dest.mkdir(parents=True,exist_ok=True)
  (dest/'scoliodon_brain_wave6.svg').write_text(svg,encoding='utf-8')
  cairosvg.svg2png(bytestring=svg.encode(),write_to=str(dest/'scoliodon_brain_wave6.png'),output_width=W,output_height=H)
  cairosvg.svg2png(bytestring=svg.encode(),write_to=str(dest/'scoliodon_brain_wave6_preview.png'),output_width=1200,output_height=900)
  print('preview generated');return
 root=Path(__file__).resolve().parents[1]
 dest=root/'app/src/main/assets/pencil_plates/shark_brain_dorsal_en.png'
 dest.parent.mkdir(parents=True,exist_ok=True)
 master=root/'docs/original_plate_svg/shark_brain_dorsal_en.svg';master.parent.mkdir(parents=True,exist_ok=True)
 master.write_text(svg,encoding='utf-8')
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(dest),output_width=W,output_height=H)
 png=dest.read_bytes()
 if not png.startswith(b'\x89PNG\r\n\x1a\n') or len(png)<120000:raise ValueError('Invalid brain plate')
 preview=root/'docs/qa-image-review/shark_brain_dorsal_wave6_review.png';preview.parent.mkdir(parents=True,exist_ok=True)
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(preview),output_width=1200,output_height=900)
 stage(root,svg,png)

if __name__=='__main__':main()