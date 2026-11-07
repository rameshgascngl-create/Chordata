#!/usr/bin/env python3
"""Original shark-type digestive-tract study plate, not a copied Scoliodon drawing.

The historic syllabus Scoliodon sorrakowah is the milk shark now assigned to
Rhizoprionodon acutus. Morphology is a teaching synthesis (not dissection).
"""
import argparse,csv,hashlib,json,subprocess
from pathlib import Path
from xml.sax.saxutils import escape
import cairosvg

ID='u2-scoliodon-digestive-labelled'
OLD_SHA='fd561652383a65114ff978b3ae22bbd7666cac33aaace7fd43ef09a69ba5016d'
AUTHOR='CHORDATA QA — original, reference-guided Scoliodon-type digestive anatomy plate'
REFS=[
 'https://www.dfo-mpo.gc.ca/species-especes/sharks/anatomy-eng.html?wbdisable=true',
 'https://www.dfo-mpo.gc.ca/species-especes/skates/anatomy/internal-eng.html',
 'https://egyankosh.ac.in/bitstream/123456789/64072/1/Block-1.pdf',
 'https://www.ntrgdc.ac.in/userfiles/file/Course%20Materials/Semester-2-Digestive%20system%20in%20Scoliodon.pdf',
]
W,H=3200,2400
INK='#1d3949';LIGHT='#59717d';LINE='#cfdee3';BLUE='#1d789e';PINK='#bc6563';GREEN='#627f61';OCHRE='#b58b50'
sh=[]
def tag(s):sh.append(s)
def path(d,fill='none',stroke=INK,sw=5):tag(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
def rect(x,y,w,h,fill='white',stroke='none',sw=0,rx=0):tag(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def ellipse(x,y,rx,ry,fill,stroke='none',sw=0):tag(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def l(x,y,X,Y,col=INK,sw=4):tag(f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>')
def t(x,y,s,size=31,bold=False,col=INK,anchor='start'):tag(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{col}" text-anchor="{anchor}">{escape(s)}</text>')
def dot(x,y,col=INK):ellipse(x,y,7,7,col)
def lead(x,y,pts):
 points=[(x,y)]+pts
 for (xa,ya),(xb,yb) in zip(points,points[1:]):l(xa,ya,xb,yb,LIGHT,3)
 dot(*points[-1])
def arrow(x,y,X,Y,col=BLUE):
 l(x,y,X,Y,col,8)
 if X>=x:tag(f'<polygon points="{X},{Y} {X-24},{Y-14} {X-24},{Y+14}" fill="{col}"/>')
 else:tag(f'<polygon points="{X},{Y} {X+24},{Y-14} {X+24},{Y+14}" fill="{col}"/>')

def draw():
 sh.clear()
 tag(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
 rect(0,0,W,H,'#fcfbf7')
 t(83,110,'SCOLIODON-TYPE SHARK · DIGESTIVE ANATOMY',69,True)
 t(92,174,'J-shaped stomach • liver and pancreas • scroll-valve intestine • rectal gland',34,False,LIGHT)
 l(86,208,3115,208,LINE,4)
 rect(82,247,1815,1990,'white',LINE,3,24)
 rect(1930,247,1187,1067,'white',LINE,3,24)
 rect(1930,1346,1187,560,'white',LINE,3,24)
 rect(1930,1935,1187,302,'white',LINE,3,24)
 t(122,322,'A  ABDOMINAL ORGAN RELATIONSHIPS',43,True)
 t(125,370,'Ventral teaching view; organs selectively separated for clarity',27,False,LIGHT)
 # translucent body-cavity outline — silhouette intentionally has no detailed skeleton
 path('M 986 435 C 725 440 563 655 513 934 C 445 1330 485 1858 978 2174 C 1370 1919 1516 1568 1496 1020 C 1481 678 1283 454 986 435 Z','#faf8f0','#b4c4cb',7)
 # anterior mouth / pharynx and oesophagus
 path('M 905 444 Q 974 415 1042 444 Q 1029 471 982 487 Q 940 481 905 444 Z','#c5b5ab',INK,5)
 path('M 942 486 Q 956 525 948 610 L 951 714 Q 987 750 1028 711 L 1021 603 Q 1017 533 1025 486','#f4e1d6',INK,7)
 for i in range(5):l(957+i*11,517,959+i*10,597,'#ad9b8d',2)
 # liver as paired longitudinal lobes posterior to stomach (behind illustration of tract)
 path('M 855 668 Q 761 670 663 806 C 583 931 566 1209 612 1442 Q 653 1535 735 1490 C 819 1429 819 1162 866 865 Q 883 718 855 668 Z','#c7c9a5',GREEN,7)
 path('M 1050 662 Q 1218 662 1307 816 C 1400 982 1427 1263 1376 1456 Q 1323 1519 1267 1469 Q 1239 1330 1169 1057 Q 1108 797 1050 662 Z','#c7c9a5',GREEN,7)
 path('M 855 675 Q 959 619 1050 667 Q 1044 736 978 759 Q 906 738 855 675 Z','#c7c9a5',GREEN,7)
 # gall bladder embedded adjacent to left liver, follows bile duct to proximal intestine
 path('M 667 1063 Q 664 1001 710 963 Q 760 964 763 1035 Q 767 1105 714 1148 Q 675 1118 667 1063 Z','#9bbd8b',GREEN,6)
 path('M 711 1146 C 693 1210 682 1277 720 1350 Q 733 1372 759 1390',stroke=GREEN,sw=9)
 # J shaped main cardiac stomach: long descending arm, bottom blind region
 path('M 948 695 C 913 749 920 934 924 1166 C 933 1327 972 1493 1102 1550 C 1248 1602 1349 1501 1340 1386 C 1329 1263 1241 1193 1208 1075 C 1158 918 1138 765 1082 702 Q 1025 668 948 695 Z','#f1c7bb',PINK,8)
 # internal longitudinal stomach rugae (non-literal)
 for x in (979,1000,1022):path(f'M {x} 788 Q {x-32} 1050 {x+8} 1269',stroke='#d9978f',sw=4)
 path('M 1098 1551 C 1042 1553 955 1554 878 1501 C 810 1453 783 1376 796 1285 C 804 1239 826 1185 854 1166',stroke=INK,sw=97)
 path('M 1098 1551 C 1042 1553 955 1554 878 1501 C 810 1453 783 1376 796 1285 C 804 1239 826 1185 854 1166',stroke='#efc4b9',sw=82)
 # pyloric valve and proximal duodenum / bursa entiana
 path('M 854 1166 C 827 1128 810 1099 788 1096 C 743 1099 714 1172 748 1211 C 769 1228 790 1236 807 1237',fill='#ecd7c7',stroke=INK,sw=7)
 l(775,1152,826,1181,PINK,9)
 path('M 756 1200 Q 720 1293 755 1388 Q 815 1453 793 1570',stroke=INK,sw=119)
 path('M 756 1200 Q 720 1293 755 1388 Q 815 1453 793 1570',stroke='#e8d6c4',sw=105)
 # duodenum links to intestine, downstream of bile duct and pancreatic secretions
 path('M 793 1567 Q 749 1587 743 1637',stroke=INK,sw=121)
 path('M 793 1567 Q 749 1587 743 1637',stroke='#e8d6c4',sw=107)
 # thick spiral-valve intestine
 path('M 702 1610 Q 646 1628 655 1711 L 668 1939 Q 679 2013 764 2018 L 884 2014 Q 962 2007 965 1912 L 950 1719 Q 946 1634 862 1622 Z','#efdac2',INK,8)
 # illustrative scrolling mucosal fold, drawn as continuous curving ribbon
 path('M 706 1659 C 824 1664 878 1688 908 1734 C 932 1778 802 1800 705 1820 C 657 1833 681 1880 783 1875 C 857 1872 919 1912 910 1958',stroke='#ae7a69',sw=17)
 path('M 706 1659 C 824 1664 878 1688 908 1734 C 932 1778 802 1800 705 1820 C 657 1833 681 1880 783 1875 C 857 1872 919 1912 910 1958',stroke='#ffefda',sw=8)
 # rectum leads posteriorly, last connection to cloaca
 path('M 771 2022 Q 806 2058 810 2093',stroke=INK,sw=49)
 path('M 771 2022 Q 806 2058 810 2093',stroke='#f2d8c7',sw=36)
 path('M 778 2096 Q 783 2133 821 2150 Q 861 2142 858 2096 Z','#ead0c1',INK,6)
 # rectal gland connected to rectum, not part of the digestive lumen
 path('M 1084 1910 Q 1150 1864 1196 1914 Q 1238 1977 1184 2040 Q 1127 2069 1096 2013 Q 1069 1960 1084 1910 Z','#e0c1b8',PINK,6)
 path('M 1095 2008 C 1034 2035 957 2055 827 2059',stroke=PINK,sw=8)
 # pancreas: compact gland on angle of cardiac and pyloric limbs
 path('M 866 1360 Q 911 1283 950 1323 Q 965 1385 917 1444 Q 861 1463 838 1417 Z','#e5cf99',OCHRE,6)
 path('M 858 1430 Q 807 1470 761 1532',stroke=OCHRE,sw=7)
 # label strokes left without crossing depicted organ key contours
 t(125,511,'Pharynx and mouth',32,True);lead(468,507,[(657,507),(948,453)])
 t(125,590,'Oesophagus',32,True);lead(382,585,[(660,585),(963,570)])
 t(125,797,'Left liver lobe',32,True);lead(410,791,[(556,791),(684,915)])
 t(125,1175,'Gallbladder',31,True);lead(383,1168,[(541,1168),(717,1056)])
 t(125,1280,'Bile duct',30,True);lead(324,1277,[(540,1277),(717,1313)])
 t(125,1565,'Pancreas',31,True);lead(345,1564,[(546,1564),(885,1397)])
 t(1297,701,'Cardiac',31,True);t(1297,740,'stomach',31,True);lead(1272,746,[(1197,790),(1103,968)])
 t(1410,1125,'Pyloric',31,True);t(1410,1164,'stomach',31,True);lead(1385,1139,[(1280,1204),(839,1374)])
 t(1239,1582,'Blind sac',30,True);lead(1203,1584,[(1164,1552)])
 t(1048,1724,'Scroll-valve',31,True);t(1048,1765,'intestine',31,True);lead(1022,1740,[(950,1762),(834,1812)])
 t(1270,1910,'Rectal gland',29,True);lead(1233,1902,[(1187,1942)])
 t(1247,2023,'Rectum',30,True);lead(1228,2019,[(983,2019),(804,2059)])
 t(1243,2120,'Cloaca',30,True);lead(1216,2112,[(1023,2112),(827,2126)])
 t(123,2202,'Drawing is anatomically guided, not to scale.',27,False,LIGHT)
 # B scroll/spiral valve enlarged — cut-open intestine with scroll valve rather than disjointed arcs
 t(1975,325,'B  INTESTINAL SCROLL VALVE',42,True)
 t(1977,370,'Opened longitudinally: enlarged mucosal fold',27,False,LIGHT)
 rect(2060,438,937,585,'#fbefdf','#bca78b',5,34)
 path('M 2090 495 Q 2524 420 2967 495 L 2967 951 Q 2544 1035 2090 951 Z','#ead1b7','#9b7e68',6)
 path('M 2120 557 Q 2320 526 2540 580 C 2720 625 2793 710 2630 760 C 2400 819 2250 786 2245 702 C 2245 641 2418 627 2535 665 C 2650 699 2580 727 2485 733',stroke='#a56f5b',sw=50)
 path('M 2120 557 Q 2320 526 2540 580 C 2720 625 2793 710 2630 760 C 2400 819 2250 786 2245 702 C 2245 641 2418 627 2535 665 C 2650 699 2580 727 2485 733',stroke='#efb79d',sw=36)
 path('M 2140 865 Q 2490 808 2940 877',stroke='#ad8670',sw=12)
 arrow(2080,1091,2925,1091,BLUE)
 t(2086,1063,'Longitudinal food movement',29,True,BLUE)
 t(1995,1193,'The scroll fold increases absorption area',29,True)
 t(1995,1232,'and slows passage through a short intestine.',27,False,LIGHT)
 # C connected alimentary flow + gland route
 t(1975,1419,'C  TRACT & GLAND CONNECTIONS',40,True)
 t(1985,1493,'1  Mouth → oesophagus → cardiac stomach',30,True,INK)
 t(1985,1556,'2  Pyloric stomach → duodenum',30,True,INK)
 t(1985,1619,'3  Scroll intestine → rectum → cloaca',30,True,INK)
 l(1986,1666,3066,1666,LINE,3)
 t(1985,1744,'Liver / gallbladder → bile duct → proximal intestine',28,True,GREEN)
 t(1985,1800,'Pancreas → pancreatic duct → proximal intestine',27,True,OCHRE)
 t(1985,1855,'Rectal gland opens into rectum; excretes excess salt.',27,True,PINK)
 # D safety keys
 t(1970,2007,'D  IMPORTANT SCIENTIFIC DISTINCTIONS',37,True)
 t(1982,2060,'• Rectal gland is osmoregulatory, not digestive.',26,False)
 t(1982,2105,'• Arrangement is schematic; sex and species may vary.',26,False)
 t(1982,2150,'• English labels; independent Zoology review pending.',26,False)
 l(84,2292,3114,2292,LINE,4)
 t(93,2345,'ORIGINAL STUDY PLATE · reference-guided, not copied or traced · PROVISIONAL QA',27,False,LIGHT)
 t(3105,2345,ID,25,True,LIGHT,'end')
 tag('</svg>')
 return '\n'.join(sh)+'\n'

def stage(root,svg,png):
 assets=root/'app/src/main/assets'
 man=assets/'pencil_plates/manifest.json'
 manifest=json.loads(man.read_text(encoding='utf-8'))
 ent=[x for x in manifest['figures'] if x['diagramId']==ID and x['lang']=='en']
 assert len(ent)==1 and ent[0]['path']=='pencil_plates/scoliodon_digestive_en.png'
 prev=ent[0]
 s_hash=hashlib.sha256(svg.encode('utf-8')).hexdigest();p_hash=hashlib.sha256(png).hexdigest()
 if prev['sha256'] not in (OLD_SHA,p_hash):raise ValueError('Unexpected pre-existing anatomical asset SHA')
 prev.update(author=AUTHOR,license='Original CHORDATA QA artwork; expert approval pending',
             sourceUrl='',referenceUrls=REFS,
             modifications='Entirely original line drawing; no third-party artwork copied or traced.',
             scope='Type study digestive-system; schematic organs, not a dissection',
             topicId='u2-scoliodon',page=2,sectionKey='digestive-system',
             learningObjective=('Identify the J-shaped cardiac and pyloric stomach, blind sac, '
                                'liver lobes, gallbladder/bile duct, pancreas, scroll-valve intestine, '
                                'rectum and salt-excreting rectal gland in a shark-type model'),
             keyEn=('J-shaped cardiac and pyloric stomach; blind sac; liver lobes, gallbladder and bile duct; '
                    'pancreas and duct to proximal intestine; scroll (spiral) valve; rectum and cloaca. '
                    'Rectal gland opens into rectum and excretes salt; it is NOT a digestive gland.'),
             keyTa=('சுறாவின் J வடிவ இரைப்பையில் கார்டியாக், பைலோரிக் பகுதிகளும் கண்முட்டு நீட்சியும் உள்ளன. '
                    'கல்லீரல், பித்தப்பை, பித்தநாளம், கணையம் மற்றும் அவற்றின் குடல் இணைப்புகள் காட்டப்பட்டுள்ளன. '
                    'குடலின் சுருள் மடிப்பும் மலக்குடலும் பொது வெளியேற்ற அறையும் காணப்படுகின்றன. '
                    'மலக்குடல் சுரப்பி உப்பை வெளியேற்ற உதவுகிறது; அது செரிமானச் சுரப்பி அன்று.'),
             svgMaster='docs/original_plate_svg/scoliodon_digestive_anatomy_en.svg',
             svgSha256=s_hash,sha256=p_hash,size=len(png),
             visualReview='REPLACED_VISUAL_QA_PENDING',
             reviewStatus='PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING')
 man.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 ledger=root/'docs/figure-coverage.tsv'
 with ledger.open(newline='',encoding='utf-8') as f:
  reader=csv.DictReader(f,delimiter='\t');cols=reader.fieldnames;rows=list(reader)
 matches=[z for z in rows if z['diagramId']==ID]
 assert len(matches)==1
 matches[0]['author']=AUTHOR;matches[0]['referenceSources']=' | '.join(REFS)
 with ledger.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(rows)
 subprocess.run(['python3','scripts/write_figure_review_register.py'],cwd=root,check=True)
 report=root/'docs/CHORDATA_SCOLIODON_DIGESTIVE_WAVE5_QA.md'
 report.write_text('# Scoliodon-type digestive-system figure — Wave 5 QA\n\n'
   'Figure ID: '+ID+'\n\n'
   'Original programmatic vector artwork; no source image reproduced or traced. '
   'This is an anatomical study schematic, NOT verified species-specific dissection. '
   'Lesson uses historical Scoliodon sorrakowah, associated with Rhizoprionodon acutus.\n\n'
   'Depicts paired elongated liver lobes, gallbladder, bile duct, J-shaped cardiac/pyloric '
   'stomach with blind sac, duodenum, pancreas, intestine with scroll (spiral) valve, '
   'rectum, cloaca and separately located salt-secreting rectal gland. '
   'The illustration differentiates digestive anatomy from osmoregulatory accessory gland.\n\n'
   'Scientific references:\n'+'\n'.join('- '+ref for ref in REFS)+'\n\n'
   'SVG SHA-256: '+s_hash+'\nPNG SHA-256: '+p_hash+'\n\n'
   'Independent Zoology and Tamil review, label review, real-device legibility and '
   'physical-device acceptance: PENDING. No production release.\n',encoding='utf-8')
 triage=root/'docs/CHORDATA_VISUAL_QUALITY_TRIAGE_64_20261107.md'
 with triage.open('a',encoding='utf-8') as f:
  f.write('\n- **Wave 5 staged (provisional)**: `u2-scoliodon-digestive-labelled` original comparative '
    'digestive anatomy replaces a weak schematic, with J stomach, paired liver lobes, '
    'gallbladder, pancreas, scroll valve and salt-excreting rectal gland. '
    'Of 38 original high-priority candidates, five now have staged replacements '
    'and 33 remain unstaged; all revised figures remain academically unapproved.\n')
 print('WAVE5 STAGED',len(png),p_hash,s_hash)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview-dir',default=None);args=ap.parse_args()
 root=Path(__file__).resolve().parents[1]
 svg=draw()
 if args.preview_dir:
  d=Path(args.preview_dir);d.mkdir(parents=True,exist_ok=True)
  (d/'scoliodon_digestive_wave5.svg').write_text(svg,encoding='utf-8')
  cairosvg.svg2png(bytestring=svg.encode('utf-8'),write_to=str(d/'scoliodon_digestive_wave5.png'))
  print('PREVIEW',d);return
 dest=root/'app/src/main/assets/pencil_plates/scoliodon_digestive_en.png'
 dest.parent.mkdir(parents=True,exist_ok=True)
 master=root/'docs/original_plate_svg/scoliodon_digestive_anatomy_en.svg';master.parent.mkdir(parents=True,exist_ok=True)
 master.write_text(svg,encoding='utf-8')
 cairosvg.svg2png(bytestring=svg.encode('utf-8'),write_to=str(dest),output_width=W,output_height=H)
 image=dest.read_bytes()
 if not image.startswith(b'\x89PNG\r\n\x1a\n') or len(image)<100000:raise ValueError('Poor or invalid PNG')
 review=root/'docs/qa-image-review/scoliodon_digestive_wave5_review.png';review.parent.mkdir(parents=True,exist_ok=True)
 cairosvg.svg2png(bytestring=svg.encode('utf-8'),write_to=str(review),output_width=1200,output_height=900)
 stage(root,svg,image)

if __name__=='__main__':main()