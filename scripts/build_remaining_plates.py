#!/usr/bin/env python3
"""Original vector anatomy plates for the CHORDATA five-unit *QA* application.

Each drawing has an exact diagram ID, English labels, explicit schematic scope,
independently-checkable source links and a retained SVG master. None is declared
scientifically approved and no external source illustration is copied.
"""
from pathlib import Path
import json, hashlib, math, textwrap
import svgwrite, cairosvg

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'app/src/main/assets'
OUT=ASSETS/'pencil_plates'
MASTERS=ROOT/'docs/original_plate_svg'
MASTERS.mkdir(parents=True,exist_ok=True)
W,H=1800,1120
INK='#25363f'; BLUE='#31647a'; RED='#b55e4f'; GREEN='#608a80'; LIGHT='#f1f6f4'; FILL='#e2ece8'; BROWN='#a87b62'; WHITE='#ffffff'; GRAY='#687b83'; EDGE='#bdcfcc'
OPENSTAX='https://openstax.org/books/biology-2e/pages/29-1-chordates'
FROG='https://www.gutenberg.org/cache/epub/77560/pg77560-images.html'
REPT='https://www.egyankosh.ac.in/bitstream/123456789/16528/1/Unit-9.pdf'
BIRD='https://www.kngac.ac.in/elearning-portal/ec/admin/contents/4_18K1B-CHAZ1_2020120708200484.pdf'
WHO='https://www.who.int/teams/control-of-neglected-tropical-diseases/snakebite-envenoming/treatment'
NCDC='https://ncdc.mohfw.gov.in/uploads/pdf/COH9.pdf'
NOAA='https://www.noaa.gov/education/resource-collections/marine-life/marine-mammals'
SHARK='https://gcwgandhinagar.com/econtent/document/15878893641ZOOTC0201-%20Brain%20%20of%20scoliodon%20%281%29-1.pdf'

def xy(pt):return f'{pt[0]},{pt[1]}'
class Plate:
 def __init__(self,title,subtitle,slug):
  self.slug=slug;self.d=svgwrite.Drawing(str(MASTERS/(slug+'.svg')),size=(W,H),viewBox=f'0 0 {W} {H}',profile='full')
  self.d.add(self.d.rect(insert=(0,0),size=(W,H),fill=WHITE))
  self.text(title,75,91,62,True)
  self.text(subtitle,79,138,28,False,GRAY)
  self.line((75,170),(1725,170),BLUE,4)
  self.text('ORIGINAL SCHEMATIC  /  NOT TO SCALE  /  ACADEMIC REVIEW PENDING',77,1080,21,False,GRAY)
 def text(self,t,x,y,size=32,bold=False,color=INK,anchor='start'):
  self.d.add(self.d.text(str(t),insert=(x,y),font_family='DejaVu Sans',font_weight='bold' if bold else 'normal',font_size=size,fill=color,text_anchor=anchor))
 def line(self,a,b,col=INK,w=5,dash=None):
  kw={'stroke':col,'stroke_width':w,'stroke_linecap':'round'}
  if dash: kw['stroke_dasharray']=dash
  self.d.add(self.d.line(a,b,**kw))
 def poly(self,pts,fill=FILL,stroke=INK,w=4):
  self.d.add(self.d.polygon(points=pts,fill=fill,stroke=stroke,stroke_width=w,stroke_linejoin='round'))
 def path(self,d,fill='none',stroke=INK,w=5):
  self.d.add(self.d.path(d=d,fill=fill,stroke=stroke,stroke_width=w,stroke_linejoin='round',stroke_linecap='round'))
 def circle(self,x,y,r,fill=FILL,stroke=INK,w=4):
  self.d.add(self.d.circle(center=(x,y),r=r,fill=fill,stroke=stroke,stroke_width=w))
 def ell(self,c,rx,ry,fill=FILL,stroke=INK,w=4):
  self.d.add(self.d.ellipse(center=c,r=(rx,ry),fill=fill,stroke=stroke,stroke_width=w))
 def box(self,x,y,w,h,title=None,fill=LIGHT):
  self.d.add(self.d.rect(insert=(x,y),size=(w,h),rx=22,ry=22,fill=fill,stroke=EDGE,stroke_width=3))
  if title:self.text(title,x+26,y+50,28,True)
 def arrow(self,a,b,col=BLUE,w=5):
  self.line(a,b,col,w)
  ang=math.atan2(b[1]-a[1],b[0]-a[0]);tip=18
  pts=[b,(b[0]-tip*math.cos(ang-.48),b[1]-tip*math.sin(ang-.48)),(b[0]-tip*math.cos(ang+.48),b[1]-tip*math.sin(ang+.48))]
  self.poly(pts,col,col,1)
 def label(self,t,x,y,end=None,size=29,anchor='start'):
  self.text(t,x,y,size,True,INK,anchor)
  if end:
   width=len(t)*size*.55;start=(x+width+9,y-8) if anchor=='start' and x<end[0] else (x-width-9,y-8) if anchor=='end' else (x-6,y-8)
   self.line(start,end,BLUE,2);self.circle(end[0],end[1],4,BLUE,BLUE,1)
 def note(self,t,x,y,size=24,col=GRAY):self.text(t,x,y,size,False,col)
 def save(self):
  self.d.save();path=OUT/(self.slug+'.png')
  cairosvg.svg2png(url=str(MASTERS/(self.slug+'.svg')),write_to=str(path),output_width=W,output_height=H)
  return path

def fish(p,x=270,y=460,k=1, shark=False):
 # Anatomical orientation: rostral left; caudal right.
 S=lambda a,b:(x+k*a,y+k*b)
 p.path(f'M {xy(S(0,80))} Q {xy(S(105,-30))} {xy(S(325,-14))} Q {xy(S(540,-24))} {xy(S(800,44))} L {xy(S(1040,-95))} L {xy(S(975,94))} L {xy(S(1040,258))} L {xy(S(797,143))} Q {xy(S(495,210))} {xy(S(290,160))} Q {xy(S(125,170))} {xy(S(0,80))} Z',FILL,INK,5)
 p.poly([S(305,-7),S(392,-145),S(445,-6)],FILL,INK,4)
 p.poly([S(498,163),S(590,280),S(622,160)],FILL,INK,4)
 p.poly([S(721,153),S(748,218),S(779,149)],FILL,INK,4)
 p.circle(*S(112,65),9,INK,INK,1)
 p.path(f'M {xy(S(15,109))} Q {xy(S(85,124))} {xy(S(167,109))}',stroke=INK,w=3)
 if shark:
  for i in range(5):p.path(f'M {xy(S(216+i*24,30))} q 14 46 -1 91',stroke=BLUE,w=4)
  p.poly([S(605,-7),S(642,-67),S(674,1)],FILL,INK,4)
 else:
  p.path(f'M {xy(S(221,30))} Q {xy(S(224,111))} {xy(S(241,154))}',stroke=BLUE,w=5)
 return S

def bird(p,x=280,y=430,k=1):
 S=lambda a,b:(x+a*k,y+b*k)
 p.ell(S(500,165),k*312,k*144,FILL)
 p.path(f'M {xy(S(272,115))} Q {xy(S(194,-60))} {xy(S(110,-80))} Q {xy(S(40,-85))} {xy(S(30,-20))} Q {xy(S(100,60))} {xy(S(272,160))}',FILL,INK,5)
 p.circle(*S(67,-45),k*55,FILL)
 p.poly([S(14,-48),S(-65,-17),S(12,-1)],FILL,INK,4)
 p.circle(*S(47,-55),7,INK,INK,1)
 p.poly([S(692,103),S(1030,245),S(990,298),S(665,215)],LIGHT,INK,4)
 p.path(f'M {xy(S(325,117))} Q {xy(S(585,27))} {xy(S(747,158))} Q {xy(S(577,280))} {xy(S(334,191))} Z',LIGHT,INK,6)
 for i in range(7):p.line(S(500+i*29,128+i*8),S(520+i*31,223+i*4),GRAY,2)
 for ax in [440,570]:
  p.line(S(ax,276),S(ax-20,430),INK,9)
  for j in [-1,0,1]:p.line(S(ax-20,430),S(ax-23+j*33,445),INK,4)
 return S

def rabbit(p,x=270,y=360,k=1):
 S=lambda a,b:(x+a*k,y+b*k)
 p.ell(S(600,305),k*410,k*183,FILL)
 p.ell(S(210,240),k*180,k*139,FILL)
 p.path(f'M {xy(S(110,140))} Q {xy(S(15,-180))} {xy(S(118,-154))} Q {xy(S(182,-110))} {xy(S(196,132))} Z',FILL,INK,5)
 p.path(f'M {xy(S(198,136))} Q {xy(S(215,-180))} {xy(S(302,-123))} L {xy(S(308,138))} Z',FILL,INK,5)
 p.circle(*S(132,207),11,INK,INK,2)
 p.circle(*S(28,286),9,BROWN,BROWN,2)
 for j in [-1,0,1]:p.line(S(25,274+j*13),S(-115,260+j*36),GRAY,2)
 p.ell(S(990,304),k*51,k*56,WHITE)
 p.ell(S(798,431),k*165,k*123,LIGHT)
 p.ell(S(438,430),k*89,k*75,LIGHT)
 for a,b in [(440,500),(798,530)]:p.line(S(a,b),S(a+182,b+16),INK,7)
 return S

def brain_shape(p,kind):
 # A rostrocaudal sequence of paired neural structures. Dorsal schematic.
 x=850
 if kind=='shark':
  sequence=[('Olfactory bulbs',310,115,77),('Olfactory tracts',446,22,19),('Cerebrum',590,155,106),('Optic lobes',798,90,93),('Cerebellum',995,130,109),('Medulla',1188,78,80)]
 elif kind=='frog':
  sequence=[('Olfactory bulbs',323,54,40),('Cerebral hemispheres',480,125,76),('Optic lobes',700,110,98),('Cerebellum',894,20,48),('Medulla',1055,81,83)]
 else:
  sequence=[('Olfactory bulbs',319,55,41),('Cerebrum',490,112,73),('Optic lobes',697,95,91),('Cerebellum',886,96,91),('Medulla',1071,81,83)]
 p.path('M 170 609 L 1555 609',stroke=EDGE,w=3)
 for idx,(t,c,rx,ry) in enumerate(sequence):
  y=609;p.ell((c,y),rx,ry,LIGHT if idx%2 else FILL,INK,4)
  if idx in [0,2,3]:p.line((c,y-ry+6),(c,y+ry-6),GRAY,2)
  p.label(t,250+(idx%2)*875,292+(idx//2)*145,(c,y+(0 if idx%2 else -ry//2)),24)
 p.path(f'M {sequence[-1][1]+sequence[-1][2]} 610 L 1370 610',stroke=INK,w=23)
 p.label('Spinal cord',1294,792,(1334,609),27)
 p.note('Rostral / anterior',175,938,27);p.note('Caudal / posterior',1350,938,27)
 p.arrow((590,939),(1180,939),BLUE,5)

ROWS=[]
def record(slot,slug,title,subtitle,make,refs,key):
 p=Plate(title,subtitle,slug);make(p);file=p.save()
 ROWS.append(dict(diagramId=slot,figure=slug.removesuffix('_en'),lang='en',path='pencil_plates/'+file.name,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),size=file.stat().st_size,author='CHORDATA QA — original vector anatomical schematic',license='Original project illustration; no source images copied',sourceUrl='',referenceUrls=refs,modifications='Original drawing in retained editable SVG; rendered PNG with English labels.',reviewStatus='PROVISIONAL_QA_ANATOMICAL_REVIEW_PENDING',keyEn=key,keyTa='',scope='Exact registered lesson section; visual study aid only',visualReview='SELF_INSPECTED_PROVISIONAL',svgMaster='docs/original_plate_svg/'+slug+'.svg'))

# Units I–II

def u1_body(p):
 s=fish(p,245,382,1.20)
 p.path('M 410 484 Q 800 435 1190 530',stroke=BLUE,w=10) # vertebral axis
 for i in range(15):p.line((490+i*46,474+i*2),(490+i*46,499+i*2),BLUE,3)
 p.ell((430,465),61,39,LIGHT);p.ell((555,647),47,36,'#d2deda')
 p.ell((864,654),104,43,LIGHT);p.ell((1044,573),104,49,LIGHT)
 p.label('Cranium + brain',80,270,(430,463));p.label('Spinal cord / vertebral axis',770,300,(838,491));p.label('Heart (ventral)',95,836,(555,647));p.label('Digestive tract',902,864,(1008,573));p.label('Paired kidneys',1248,726,(1068,640));p.label('Respiratory surface (gills here)',80,947,(540,560))
 p.note('Representative jawed fish plan — organs vary in other vertebrates.',320,1018,26)
record('u1-vertebrata-characters-vertebrate-anatomy','vertebrate_organs_en','Vertebrate body plan: integrated organ systems','Representative aquatic jawed vertebrate, lateral schematic',u1_body,[OPENSTAX],'Spinal cord, heart, kidneys, respiration, digestion and paired sensory structures are integrated.')

def fish_groups(p):
 for i,(title,kind,info) in enumerate([('CHONDRICHTHYES','shark','Cartilaginous; exposed gill slits'),('ACTINOPTERYGII','ray','Ray fins; operculum common'),('SARCOPTERYGII','lobe','Lobed paired fins; includes lungfish')]):
  x=80+i*573;p.box(x,230,550,704,title)
  s=fish(p,x+52,480,.38,kind=='shark')
  if kind=='lobe':p.ell((x+297,631),51,31,LIGHT,BLUE,4)
  p.note(info,x+23,811,23)
  p.note({'shark':'Sharks and rays','ray':'Most familiar bony fishes','lobe':'Coelacanths, lungfishes + tetrapods'}[kind],x+23,861,23)
 p.note('Fishes are not a single exclusive evolutionary clade.',500,1001,25)
record('u2-pisces-classification-fish-groups','fish_major_groups_en','Major living fish lineages','Comparative teaching categories; not proportional portraits',fish_groups,[OPENSTAX],'Chondrichthyans, ray-finned and lobe-finned fish lineages are distinguished.')

def shark_ext(p):
 s=fish(p,205,414,1.25,True)
 p.label('First dorsal fin',714,238,s(415,-60));p.label('Second dorsal fin',1300,309,s(634,-38))
 p.label('Five gill slits',90,789,s(264,78));p.label('Eye',180,314,s(113,63));p.label('Ventral mouth',80,925,s(95,122));p.label('Pectoral fin',660,897,s(550,221));p.label('Pelvic fin',1280,874,s(746,192));p.label('Heterocercal tail',1360,714,s(1030,-53))
 p.note('Scoliodon (historical syllabus name); shark form schematic.',350,1010,24)
record('u2-scoliodon-external-labelled','scoliodon_external_anatomy_en','Scoliodon: external anatomy and fins','Lateral anatomical outline · anterior head left · tail right',shark_ext,[OPENSTAX],'Five gill slits, paired fins, ventral mouth and heterocercal caudal fin.')

def shark_brain(p):brain_shape(p,'shark');p.note('Broad brain regions only; individual neural lobes shown schematically.',265,996,24)
record('u2-scoliodon-brain-labelled','shark_brain_dorsal_en','Shark brain: dorsal divisions','Relative regions simplified; no cranial nerve dissection implied',shark_brain,[SHARK],'Olfactory system, forebrain, optic regions, cerebellum and medulla ordered rostrocaudally.')

def accessory(p):
 names=[('Anabas','Labyrinth organ','Folded suprabranchial cavity'),('Clarias','Arborescent organ','Branching air-breathing tissue'),('Heteropneustes','Air sacs','Paired elongated air sacs'),('Mudskipper','Moist surfaces','Cutaneous + buccopharyngeal')]
 for i,(nm,lab,desc) in enumerate(names):
  x=78+i*427;p.box(x,232,406,726,nm)
  p.text(lab,x+22,339,29,True,BLUE)
  cx=x+204
  if i==0:
   for j in range(5):p.path(f'M {cx-90+j*35} 555 Q {cx-30+j*15} 435 {cx-70+j*26} 650',stroke=BLUE,w=6)
  elif i==1:
   p.line((cx,698),(cx,459),BLUE,11)
   for y in [489,551,618]:
    for sg in [-1,1]:
     p.line((cx,y),(cx+sg*92,y-44),BLUE,8);p.line((cx+sg*92,y-44),(cx+sg*127,y-89),BLUE,4)
  elif i==2:
   for q in [-1,1]:p.ell((cx+q*77,566),52,185,FILL,BLUE,7)
  else:
   p.ell((cx,557),137,89,FILL)
   for j in range(20):p.circle(cx-110+j*12,558+18*math.sin(j),3,BLUE,BLUE,1)
   p.note('moist skin',x+110,717,23)
  p.note(desc,x+17,850,22)
 p.note('These are accessory routes of gas exchange; gills remain present.',286,1023,26)
record('u2-accessory-respiration-accessory-organs-comparison','fish_accessory_breathing_en','Accessory air-breathing organs of fishes','Different tissues and mechanisms; four named examples',accessory,[OPENSTAX],'Labyrinth, arborescent organs, air sacs and moist skin are different adaptations.')

def care_fish(p):
 for i,(title,desc) in enumerate([('Stickleback','Male builds and guards nest'),('Mouthbrooding cichlid','Eggs / young sheltered in mouth'),('Seahorse','Male brood pouch holds embryos')]):
  x=82+i*568;p.box(x,228,542,730,title);s=fish(p,x+63,450,.39)
  if i==0:
   p.path(f'M {x+155} 743 Q {x+280} 650 {x+430} 739',stroke=GREEN,w=14)
   for j in range(5):p.circle(x+210+j*43,722+int(8*math.sin(j)),12,WHITE,BLUE,3)
  elif i==1:
   for j in range(4):p.circle(x+140+j*26,517+((j%2)*19),9,WHITE,BLUE,2)
  else:
   p.path(f'M {x+294} 590 Q {x+330} 654 {x+305} 742 Q {x+285} 801 {x+345} 822',stroke=INK,w=17)
   p.ell((x+321,721),55,105,LIGHT,BLUE,4)
   for j in range(5):p.circle(x+305+(j%3)*10,x and 692+(j*19),5,WHITE,BLUE,1)
  p.note(desc,x+26,864,23)
record('u2-parental-care-parental-care-comparison','fish_parental_care_en','Parental care among fishes','Contrasting nests, oral incubation and male brood pouches',care_fish,[OPENSTAX],'Which parent provides care and how depends on the species; these are not universal traits.')

def fisheries(p):
 labels=[('CAPTURE','Wild fisheries'),('AQUACULTURE','Cultured fish'),('LANDING','Sorting + ice'),('COLD CHAIN','Safe transport'),('PROCESSING','Quality control'),('MARKET','Retail / nutrition')]
 for i,(title,sub) in enumerate(labels):
  c=i%3;r=i//3;x=100+c*574;y=255+r*352
  p.box(x,y,522,276,title)
  p.text(sub,x+34,y+123,27,False,GRAY)
  if c<2:p.arrow((x+522,y+140),(x+570,y+140),BLUE,6)
  if c==2 and r==0:p.arrow((x+240,y+280),(x+240,y+350),BLUE,5)
 p.note('Capture and aquaculture are different supply origins; both need hygiene and cold-chain handling.',145,1020,25)
record('u2-economic-importance-fishery-value-chain','fishery_value_chain_en','Fisheries: from production to consumers','Schematic value-chain flow for capture fisheries and aquaculture',fisheries,[OPENSTAX],'Fisheries support nutrition, handling, processing, transport and livelihoods.')

def devonian(p):
 phases=[('LOBED-FIN FISH','Sarcopterygian lineage'),('TIKTAALIK','Mosaic of fish and tetrapod traits'),('EARLY TETRAPODS','Limbs with digits')]
 for i,(title,desc) in enumerate(phases):
  x=85+i*571;p.box(x,234,541,724,title)
  if i==0:fish(p,x+60,455,.37)
  elif i==1:
   p.path(f'M {x+77} 555 Q {x+175} 426 {x+332} 480 L {x+430} 545 Q {x+330} 614 {x+75} 610 Z',FILL,INK,5)
   p.poly([(x+220,575),(x+269,739),(x+333,750),(x+357,703),(x+284,668)],FILL,INK,4)
  else:
   p.path(f'M {x+63} 528 Q {x+198} 408 {x+368} 516 Q {x+428} 574 {x+382} 620 Q {x+156} 666 {x+60} 574 Z',FILL,INK,5)
   for q in (162,362):
    p.path(f'M {x+q} 594 L {x+q-11} 718 L {x+q+70} 742',stroke=INK,w=15)
    for j in range(4):p.line((x+q+68,740),(x+q+76+j*15,766+j*5),INK,3)
  p.note(desc,x+22,860,21)
  if i<2:p.arrow((x+530,797),(x+571,797),BLUE,5)
 p.note('Fossil mosaics document evolutionary changes; none is asserted to be a direct frog ancestor.',115,1017,23)
record('u3-origin-devonian-transition','devonian_tetrapod_transition_en','Devonian fish-to-tetrapod transition','Simplified evolutionary sequence; not a direct ancestor chain',devonian,[OPENSTAX],'Lobe-fin lineages, stem-tetrapod mosaics and later digit-bearing limbs document the transition.')

def frog_arterial(p):
 p.box(110,236,1579,746,'PAIRED CAROTID, SYSTEMIC AND PULMOCUTANEOUS ARCHES')
 # Left: three-chambered heart; right: strictly connected branching pathways.
 p.ell((323,510),77,72,'#eeded8',RED,5)
 p.ell((524,510),77,72,'#eeded8',RED,5)
 p.ell((422,701),138,137,'#f1ddd6',RED,7)
 p.path('M 372 572 L 385 619 M 479 572 L 466 620',stroke=RED,w=11)
 p.label('Right atrium',142,406,(321,502),26)
 p.label('Left atrium',535,389,(528,499),26)
 p.label('Single ventricle',184,889,(409,715),26)
 # The truncus arises from the ventricular complex and gives rise to each pair.
 p.path('M 420 581 L 420 344 L 725 344 L 725 839',stroke=RED,w=15)
 p.label('Truncus arteriosus',748,329,(623,343),24)
 items=[(452,'CAROTID ARCHES','Head and oral region'),(648,'SYSTEMIC ARCHES','Join posteriorly: dorsal aorta'),(841,'PULMOCUTANEOUS ARCHES','Branch to lungs and skin')]
 for y,head,sub in items:
  p.arrow((726,y),(908,y),BLUE,8)
  p.box(928,y-73,671,149,None,WHITE)
  p.text(head,956,y-20,30,True)
  p.text(sub,960,y+29,25,False,GRAY)
 p.note('Each named arch is paired (left and right). Flow routes are schematic; the ventricle is not fully separated.',157,1028,23)
record('u3-rana-arterial-system','frog_arterial_system_en','Adult frog: arterial arches','Carotid, systemic and pulmocutaneous pathways; schematic',frog_arterial,[FROG,'https://journals.physiology.org/doi/10.1152/advan.00087.2012'],'Three arterial pairs leave the truncus and supply head, systemic tissues, lungs and skin.')

def frog_brain(p):brain_shape(p,'frog');p.note('Dorsal view; paired optic lobes and short cerebellar band.',350,1001,25)
record('u3-rana-brain','frog_brain_dorsal_en','Adult frog brain: dorsal view','Forebrain, midbrain and hindbrain anatomical landmarks',frog_brain,[FROG],'Olfactory bulbs, cerebral hemispheres, optic lobes, cerebellum, medulla and cord.')

def frog_parent(p):
 entries=[('Alytes','Male carries egg strings'),('Tree frogs','Foam nest protects embryos'),('Dendrobatids','Tadpoles carried to water')]
 for i,(name,desc) in enumerate(entries):
  x=85+i*567;p.box(x,228,535,728,name);p.ell((x+280,536),125,103,FILL)
  for j in range(4):p.line((x+212+j*42,615),(x+155+j*68,730),INK,10)
  if i==0:
   for j in range(10):p.circle(x+180+j*29,x and 744+int(18*math.sin(j)),13,WHITE,BLUE,3)
  elif i==1:
   p.ell((x+274,760),169,65,'#eff5ec',GREEN,3)
   for j in range(11):p.circle(x+158+j*24,745+int(16*math.sin(j)),9,WHITE,GREEN,2)
  else:
   for j in range(3):p.ell((x+223+j*48,443),23,36,LIGHT,BLUE,3)
  p.note(desc,x+30,871,22)
 p.note('Examples from different amphibian lineages; not typical of every frog.',369,1019,25)
record('u3-parental-care-parental-care-comparison','amphibian_parental_care_en','Amphibian parental care: three strategies','Male egg transport, foam nests and tadpole carrying',frog_parent,[OPENSTAX],'Care ranges from carrying eggs to defending nests or transporting offspring.')

def reptile_tree(p):
 p.box(94,222,1605,770,'LIVING SAUROPSID LINEAGES — illustrative topology')
 x0=250;p.line((x0,349),(x0,850),BLUE,12)
 groups=[('Testudines','Turtles + tortoises'),('Lepidosauria','Squamata + Rhynchocephalia'),('Archosauria','Crocodilians + birds')]
 for i,(a,b) in enumerate(groups):
  y=388+i*205;p.line((x0,y),(585,y),BLUE,9);p.circle(586,y,11,BLUE,BLUE,1)
  p.box(620,y-58,912,124);p.text(a,662,y-8,33,True);p.text(b,1000,y-8,27)
 p.note('“Traditional reptiles” omit birds; in phylogenetic classification birds belong within reptiles.',170,1020,24)
record('u4-reptilia-classification-living-reptile-orders','living_reptile_groups_en','Living reptiles: important evolutionary groups','Conventional named orders within modern sauropsid diversity',reptile_tree,[OPENSTAX],'Testudines, Squamata, Rhynchocephalia and Crocodylia; birds belong within sauropsids.')

def calotes_digest(p):
 # A continuous canal with paired digestive glands; no invented cecum.
 p.box(145,233,1511,754,'DIGESTIVE TRACT — lumen continuous from mouth to cloaca')
 p.path('M 365 380 Q 446 359 491 389 L 603 438 L 666 499 Q 670 544 751 528 Q 877 502 917 605 Q 958 692 856 743 Q 750 803 819 841 L 1098 833 L 1184 890',stroke=INK,w=24)
 p.path('M 745 529 Q 837 458 941 513 Q 1014 575 972 659 Q 943 696 871 710',stroke=INK,w=9)
 p.ell((700,690),149,67,'#dcd9bc',BROWN,5)
 p.ell((1000,773),85,46,LIGHT,BLUE,4)
 p.label('Mouth and tongue',185,315,(395,379));p.label('Oesophagus',535,377,(625,460));p.label('Stomach',1100,387,(887,544));p.label('Coiled small intestine',1025,596,(878,697));p.label('Liver',325,834,(694,688));p.label('Pancreas',1195,744,(1028,774));p.label('Large intestine -> cloaca',1110,945,(1181,877),25)
record('u4-calotes-digestive-system','calotes_digestive_en','Calotes: alimentary canal and glands','Continuous digestive pathway with simplified relative positions',calotes_digest,[REPT],'Mouth, oesophagus, stomach, intestine, liver, pancreas and cloaca.')

def calotes_lung(p):
 p.box(150,231,1500,754,'VENTILATION BY RIB-CAGE MOVEMENT')
 p.path('M 867 317 L 867 482 L 715 543 M 867 482 L 1021 543',stroke=INK,w=18)
 for i,x in enumerate([647,1081]):
  p.ell((x,710),169,210,FILL,INK,6)
  for j in range(6):p.path(f'M {x-124} {590+j*44} Q {x} {646+j*32} {x+127} {590+j*44}',stroke=BLUE,w=3)
 for j in range(5):
  y=480+j*90;p.path(f'M 480 {y} Q 355 {y+90} 450 {y+180}',stroke=GRAY,w=5)
  p.path(f'M 1255 {y} Q 1405 {y+92} 1303 {y+180}',stroke=GRAY,w=5)
 p.label('Naris -> glottis -> trachea',156,325,(868,429),27);p.label('Left lung',286,744,(619,703));p.label('Right lung',1191,744,(1088,711));p.label('Internal exchange surfaces',1074,473,(1060,601),27)
 p.note('Paired lungs exchange gases; ribs and trunk muscles change thoracic volume.',251,1015,25)
record('u4-calotes-respiratory-system','calotes_respiratory_en','Calotes: lung ventilation','Paired lungs, airway and thoracic expansion mechanisms',calotes_lung,[REPT],'Air reaches paired internally subdivided lungs; ventilatory movements involve the ribs.')

def calotes_heart(p):
 p.box(119,240,1554,735,'SQUAMATE HEART — FUNCTIONAL VENTRICULAR PARTITIONING')
 # This is a connectivity model, avoiding the false impression that major arteries arise from atria.
 p.ell((335,501),92,73,'#eadcd5',RED,5)
 p.ell((577,501),92,73,'#eadcd5',RED,5)
 p.path('M 331 574 Q 308 626 344 673 M 565 573 Q 586 637 564 679',stroke=RED,w=9)
 p.path('M 335 653 Q 305 828 455 887 Q 599 842 583 655 Q 473 584 335 653 Z','#f3ded7',RED,7)
 p.path('M 403 661 Q 363 740 423 849',stroke=BROWN,w=5)
 p.path('M 512 663 Q 559 742 485 848',stroke=BROWN,w=5)
 p.label('Right atrium',148,392,(334,496),28)
 p.label('Left atrium',593,390,(578,497),28)
 p.label('Ventricular complex',149,952,(472,769),28)
 p.note('Ventricle has differentiated cavum regions',170,914,23)
 # Three major outflows are explicitly traced from the ventricle itself.
 for i,(c,name,desc) in enumerate([(535,'RIGHT SYSTEMIC AORTA','Systemic circulation'),(690,'LEFT SYSTEMIC AORTA','Systemic circulation'),(845,'PULMONARY ARTERY','Lung circulation')]):
  p.path(f'M 574 741 Q 690 {c} 801 {c}',stroke=[RED,BROWN,BLUE][i],w=10)
  p.arrow((801,c),(940,c),[RED,BROWN,BLUE][i],6)
  p.box(957,c-61,624,116,None,WHITE)
  p.text(name,977,c-7,28,True)
  p.text(desc,980,c+30,23,False,GRAY)
 p.note('Colour separates pathways only; it does not imply completely unmixed oxygenated blood.',159,1019,23)
record('u4-calotes-arterial-system','calotes_heart_arteries_en','Calotes: heart and arterial pathways','Simplified squamate circulation; not a crocodilian heart',calotes_heart,[REPT],'Two atria, functionally partitioned ventricle, systemic and pulmonary pathways.')

def calotes_brain(p):brain_shape(p,'lizard');p.note('Schematic dorsal regions with expanded forebrain relative to amphibians.',230,1001,23)
record('u4-calotes-brain','calotes_brain_dorsal_en','Calotes: brain (dorsal schematic)','Major forebrain, midbrain and hindbrain landmarks',calotes_brain,[REPT],'Forebrain, optic lobes, cerebellum, medulla and spinal cord.')

# Unit IV: deep time, medically important snakes, venom and evidence-based first aid

def fossil_groups(p):
 for i,(name,desc) in enumerate([('PAREIASAURS','Extinct parareptilian forms'),('PTEROSAURS','Flying archosaur relatives'),('NON-AVIAN DINOSAURS','Theropods and other dinosaur clades')]):
  x=77+i*573;p.box(x,232,547,723,name)
  if i==0:
   p.ell((x+260,568),170,111,FILL,INK,5)
   p.path(f'M {x+119} 525 Q {x+75} 462 {x+97} 422 Q {x+188} 412 {x+215} 511',FILL,INK,5)
   for q in (145,370):p.line((x+q,647),(x+q-22,762),INK,15)
  elif i==1:
   p.poly([(x+259,510),(x+45,627),(x+75,730),(x+259,624),(x+468,732),(x+494,624)],FILL,INK,5)
   p.path(f'M {x+255} 620 L {x+255} 420 Q {x+339} 397 {x+358} 431',stroke=INK,w=10)
   p.line((x+255,555),(x+75,730),BLUE,4);p.line((x+255,555),(x+469,732),BLUE,4)
  else:
   p.ell((x+240,591),162,93,FILL,INK,5)
   p.path(f'M {x+362} 566 Q {x+429} 475 {x+425} 447',stroke=INK,w=24)
   p.ell((x+435,431),69,45,FILL,INK,4)
   p.path(f'M {x+103} 604 L {x+39} 523',stroke=INK,w=20)
   for q in (208,319):p.path(f'M {x+q} 656 L {x+q-12} 777 L {x+q+45} 793',stroke=INK,w=13)
  p.note(desc,x+21,865,21)
 p.note('Illustrative extinct groups are not all one evolutionary branch; pterosaurs are not dinosaurs.',95,1012,23)
record('u4-origin-extinct-extinct-groups','extinct_reptile_lineages_en','Extinct reptiles: selected lineages','Simplified body silhouettes for comparison, not fossil reconstructions',fossil_groups,[OPENSTAX],'Pareiasaurs, pterosaurs and non-avian dinosaurs are distinct extinct lineages.')

def snakes_four(p):
 names=[('Indian cobra','Naja naja','Hood may be displayed'),('Common krait','Bungarus caeruleus','Often narrow pale crossbands'),("Russell's viper",'Daboia russelii','Heavy body, oval blotches'),('Saw-scaled viper','Echis carinatus','Small viper, keeled scales')]
 for i,(common,scientific,note) in enumerate(names):
  x=78+(i%2)*855;y=224+(i//2)*389;p.box(x,y,806,371,common)
  p.text(scientific,x+30,y+100,26,False,BLUE)
  cy=y+213
  if i==0:
   p.path(f'M {x+535} {cy+100} Q {x+443} {cy-31} {x+552} {cy-82} Q {x+660} {cy-16} {x+565} {cy+100}',FILL,INK,6)
   p.ell((x+551,cy-10),68,90,LIGHT,INK,5)
  elif i==1:
   p.path(f'M {x+420} {cy+56} C {x+542} {cy-154} {x+686} {cy+35} {x+567} {cy+92} C {x+520} {cy+118} {x+477} {cy+98} {x+477} {cy+84}',stroke=INK,w=24)
   for q in range(6):p.line((x+506+q*26,cy-44+int(40*math.sin(q))),(x+520+q*26,cy-32+int(40*math.sin(q))),WHITE,5)
  elif i==2:
   p.path(f'M {x+365} {cy+85} C {x+477} {cy-109} {x+652} {cy+54} {x+520} {cy+91}',stroke=INK,w=59)
   for q in range(4):p.ell((x+485+q*47,cy+3+int(24*math.sin(q))),25,17,LIGHT,BROWN,3)
  else:
   p.path(f'M {x+390} {cy+75} C {x+512} {cy-131} {x+648} {cy+56} {x+498} {cy+100}',stroke=INK,w=43)
   for q in range(12):p.line((x+455+q*10,cy+33+int(18*math.sin(q))),(x+463+q*10,cy+14+int(18*math.sin(q))),GRAY,3)
  p.note(note,x+29,y+332,24)
 p.note('Unsafe to identify a live snake from a pattern alone. Do not approach or handle any snake.',183,1030,24,RED)
record('u4-snakes-india-big-four-identification','india_big_four_snakes_en',"India's 'Big Four' venomous snakes",'Names and general appearance cues only · NOT a field-identification key',snakes_four,['https://www.who.int/news-room/questions-and-answers/item/snakebite-envenoming',NCDC],'Cobra, common krait, Russell’s viper and saw-scaled viper; other dangerous species occur.')

def snake_venom(p):
 p.box(94,223,768,768,'ELAPID — FIXED FRONT FANG')
 p.box(943,223,763,768,'VIPER — ROTATING FANG')
 # Two sections: paired gland, single traced duct to fang; gland behind eye.
 for i,x in enumerate((102,951)):
  p.path(f'M {x+108} 657 Q {x+330} 353 {x+585} 563 Q {x+630} 609 {x+571} 672 Q {x+312} 780 {x+108} 657 Z',FILL,INK,6)
  p.ell((x+324,456),107,55,'#d6e7de',GREEN,5)
  p.path(f'M {x+419} 472 Q {x+490} 494 {x+499} 558',stroke=BLUE,w=9)
  if i==0:
   p.path(f'M {x+500} 555 Q {x+519} 704 {x+494} 750',stroke=INK,w=21)
   p.path(f'M {x+495} 738 L {x+500} 774',stroke=BLUE,w=5)
   p.label('Fixed hollow fang',x+123,862,(x+500,707),25)
  else:
   p.path(f'M {x+495} 555 Q {x+602} 586 {x+634} 709',stroke=INK,w=21)
   p.path(f'M {x+634} 705 L {x+645} 771',stroke=BLUE,w=5)
   p.circle(x+488,555,16,WHITE,INK,3)
   p.label('Hinged fang',x+119,863,(x+629,694),25)
  p.label('Venom gland',x+78,361,(x+312,458),26)
  p.label('Venom duct',x+465,392,(x+493,500),26)
 p.note('Functional system: gland secretion -> duct -> front fang -> injection during bite.',205,1030,26)
record('u4-poison-apparatus-venom-apparatus','snake_venom_delivery_en','Snake venom delivery: gland, duct and fang','Functional comparison of elapid and viperid front fangs',snake_venom,[NCDC,'https://www.who.int/news-room/questions-and-answers/item/snakebite-envenoming'],'Elapids have fixed front fangs; vipers have long hinged front fangs.')

def snakebite(p):
 blocks=[('1  MOVE AWAY','Leave the snake; do not try to catch it.'),('2  CALL EMERGENCY CARE','Arrange rapid transfer to a hospital.'),('3  KEEP PERSON STILL','Reassure; avoid walking and exertion.'),('4  IMMOBILISE LIMB','Support limb with a splint, without constriction.'),('5  REMOVE TIGHT ITEMS','Remove rings, anklets, watches before swelling.'),('6  MONITOR + TRANSPORT','Observe breathing; hand over to medical team.')]
 for i,(h,desc) in enumerate(blocks):
  y=226+i*116;p.box(117,y,1566,103,None,WHITE if i%2 else LIGHT)
  p.text(h,154,y+43,29,True,BLUE);p.text(desc,617,y+44,25)
  if i<5:p.arrow((915,y+96),(915,y+113),GREEN,4)
 p.box(120,948,1560,80,None,'#fff4f0')
 p.text('AVOID: TOURNIQUET · CUTTING · SUCTION · ICE · HERBAL REMEDIES · DELAY',172,1003,27,True,RED)
record('u4-poison-apparatus-first-aid-flowchart','snakebite_first_aid_en','Snakebite: evidence-based first aid','WHO / Indian public-health recommendations — emergency care required',snakebite,[WHO,NCDC],'Immobilise, remove tight items and transport promptly; no tourniquets, incision or suction.')

# Unit V: Aves and Mammalia

def birds_tree(p):
 p.box(105,236,1597,751,'NEORNITHES — LIVING BIRDS')
 p.line((292,395),(292,783),BLUE,11)
 for i,(name,desc) in enumerate([('PALAEOGNATHAE','Ostriches, emus and tinamous'),('NEOGNATHAE','Most other living birds')]):
  y=445+i*248;p.line((294,y),(550,y),BLUE,9)
  p.box(577,y-80,962,168,name)
  p.text(desc,626,y+24,26,False,GRAY)
 p.note('Flight ability does not define Palaeognathae: tinamous can fly.',298,970,27)
record('u5-aves-classification-bird-lineages','living_bird_phylogeny_en','Living bird lineages','A major split among modern birds; simplified lineage diagram',birds_tree,[OPENSTAX],'Palaeognathae includes ratites and tinamous; Neognathae includes most birds.')

def pigeon_ext(p):
 s=bird(p,276,428,1.08)
 p.label('Beak without teeth',86,321,s(-21,-20),27);p.label('Eye',414,285,s(48,-48),27)
 p.label('Contour feathers / wing',1141,338,s(530,140),28)
 p.label('Primary flight feathers',1119,571,s(770,173),26)
 p.label('Tail feathers',1250,794,s(1023,266),27)
 p.label('Scaly hind limb',200,883,s(445,373),27)
 p.label('Anisodactyl toes',813,968,s(568,438),27)
record('u5-columba-external','pigeon_external_anatomy_en','Rock pigeon: external features','Columba livia, lateral schematic showing flight and perching structures',pigeon_ext,[OPENSTAX,BIRD],'Beak, wings, flight feathers, tail and scaled perching feet.')

def pigeon_uro(p):
 for i,(label0,x) in enumerate([('MALE',94),('FEMALE',940)]):
  p.box(x,230,772,752,label0)
  if i==0:
   for side in [-1,1]:
    cx=x+382+side*165
    p.ell((cx,570),59,122,FILL,INK,4) # kidney
    p.ell((cx,395),44,55,'#eddbd1',RED,5) # testis
    p.path(f'M {cx} 451 Q {cx+side*75} 558 {cx+side*63} 694 Q {cx+side*61} 770 {x+380} 863',stroke=RED,w=7)
    p.path(f'M {cx+side*17} 650 Q {cx+side*7} 730 {x+380} 863',stroke=BLUE,w=6)
   p.label('Paired testes',x+27,327,(x+217,392),25)
   p.label('Kidneys',x+30,550,(x+217,583),25)
   p.label('Vasa deferentia',x+29,744,(x+286,727),23)
  else:
   for side in [-1,1]:
    cx=x+385+side*174;p.ell((cx,577),54,123,FILL,INK,5)
    p.path(f'M {cx} 670 L {x+385} 866',stroke=BLUE,w=7)
   for j in range(6):p.circle(x+247+(j%2)*40,x and 360+j*30,21,'#eadac7',BROWN,3)
   p.path(f'M {x+293} 443 C {x+460} 410 {x+371} 576 {x+447} 608 C {x+537} 690 {x+407} 750 {x+390} 859',stroke=RED,w=16)
   p.label('Left ovary',x+26,318,(x+280,432),25)
   p.label('Left oviduct',x+466,381,(x+443,573),25)
   p.label('Kidneys',x+31,750,(x+233,602),25)
  p.ell((x+382,886),90,42,LIGHT,INK,4)
  p.text('Cloaca',x+465,895,26,True)
 p.note('Urinary bladder absent; each ureter drains to cloaca. Functional right ovary usually absent.',143,1023,24)
record('u5-columba-urinogenital','pigeon_urinogenital_en','Pigeon urinogenital systems: male vs female','Paired kidneys and ureters; sexually different reproductive ducts',pigeon_uro,[BIRD,REPT],'Males: paired testes; females: left ovary and oviduct; normally no urinary bladder.')

def pigeon_sense(p):
 p.box(91,233,772,756,'EYE — SECTION (SCHEMATIC)')
 p.box(934,233,773,756,'EAR — SOUND + BALANCE')
 p.circle(472,617,245,LIGHT,INK,7);p.ell((266,617),65,110,WHITE,BLUE,5)
 p.path('M 626 418 Q 477 604 634 800',stroke=GREEN,w=22)
 p.circle(488,613,81,'#e7dad0',BROWN,5)
 p.circle(472,615,30,INK,INK,2)
 p.label('Cornea',113,393,(268,573),27);p.label('Lens',140,887,(488,615),27);p.label('Retina',577,348,(639,452),27)
 # Ear canal, columella, cochlear duct, semicircular canals
 p.ell((1162,602),155,134,FILL,INK,5)
 p.path('M 1014 600 L 1216 601 L 1278 558',stroke=INK,w=17)
 p.path('M 1278 558 Q 1395 475 1479 545 Q 1550 613 1471 676',stroke=BLUE,w=12)
 for i in range(3):p.ell((1490+i*20,444+i*32),92-i*11,86-i*11,'none',BLUE,5)
 p.label('Ear opening',956,370,(1022,597),25)
 p.label('Columella',1210,801,(1263,568),26)
 p.label('Semicircular canals',1237,340,(1502,431),24)
 p.note('Hearing + equilibrium (inner ear)',1090,908,25)
record('u5-columba-sense-organs','pigeon_eye_ear_en','Pigeon sensory organs: eye and ear','Two anatomical sections · visually based orientation and equilibrium',pigeon_sense,[BIRD],'Visual structures, middle-ear columella and inner-ear balance organs.')

def aerofoil(p):
 p.box(106,237,1590,736,'AIRFLOW ABOUT A CAMBERED WING SECTION')
 p.path('M 288 655 Q 573 464 1190 548 Q 1383 592 1500 640 Q 1064 743 574 705 Z',FILL,INK,7)
 for y in [362,426,497]:
  p.path(f'M 185 {y} C 490 {y-47} 765 {y-105} 1540 {y-35}',stroke=BLUE,w=7)
  p.arrow((1380,y-40),(1540,y-35),BLUE,5)
 for y in [789,853]:
  p.path(f'M 185 {y} C 580 {y+25} 1070 {y+80} 1537 {y+11}',stroke=GREEN,w=7)
  p.arrow((1367,y+34),(1540,y+11),GREEN,5)
 p.arrow((863,680),(863,315),RED,9)
 p.label('Lift (net aerodynamic force)',919,324,(866,365),29)
 p.label('Leading edge',123,604,(301,655),27)
 p.label('Trailing edge',1234,706,(1494,640),26)
 p.note('Lift arises from air deflection and pressure distribution; not from an equal-transit-time rule.',130,1017,23)
record('u5-flight-adaptations-wing-aerodynamics','avian_aerofoil_en','Bird wing aerofoil: airflow and lift','Camber, leading edge, trailing edge and net aerodynamic force',aerofoil,['https://doi.org/10.1016/j.cub.2022.06.079'],'Lift involves circulation, deflection of airflow, pressure and wing angle of attack.')

def flight_muscle(p):
 p.box(128,224,1530,767,'PECTORAL GIRDLE / WING CROSS-SECTIONAL SCHEMATIC')
 p.path('M 721 432 L 912 679 L 1092 435',stroke=INK,w=34)
 p.path('M 908 680 L 911 890',stroke=INK,w=20)
 p.path('M 915 701 Q 630 677 587 487 Q 591 411 683 386 Q 773 356 869 480',FILL,RED,6)
 p.path('M 910 706 Q 1012 666 1079 570 Q 1092 518 1031 469 Q 956 426 912 505',LIGHT,BLUE,6)
 p.path('M 1065 536 Q 1184 335 1312 371 L 1501 434',stroke=BLUE,w=17)
 p.path('M 1076 539 Q 1096 443 1191 411',stroke=GREEN,w=8)
 p.circle(1180,407,27,WHITE,INK,4)
 p.label('Pectoralis: downstroke',165,346,(700,554),29)
 p.label('Supracoracoideus: upstroke',1105,286,(1021,557),26)
 p.label('Tendon through triosseal canal',1128,678,(1179,411),24)
 p.label('Keeled sternum',1320,873,(909,796),28)
 p.label('Humerus',1350,503,(1405,414),27)
 p.note('Supracoracoideus is deep to pectoralis; its tendon acts around a shoulder pulley.',210,1020,25)
record('u5-flight-adaptations-flight-muscles','avian_flight_muscles_en','Flight muscles and keeled sternum','Pectoralis downstroke versus deep supracoracoideus upstroke',flight_muscle,['https://doi.org/10.1016/j.cub.2022.06.079','https://doi.org/10.1111/jzo.13043'],'Pectoralis lowers the wing; supracoracoideus tendon elevates it via triosseal canal.')

def bird_migrate(p):
 p.box(106,230,1590,760,'ILLUSTRATIVE BREEDING / NON-BREEDING / STOPOVER NETWORK')
 p.ell((386,474),167,112,'#e1efe6',GREEN,5)
 p.ell((863,705),182,99,'#e2edf4',BLUE,5)
 p.ell((1354,475),164,111,'#e1efe6',GREEN,5)
 p.text('Breeding habitat',386,463,28,True,INK,'middle')
 p.text('Wetland stopover',863,695,28,True,INK,'middle')
 p.text('Non-breeding habitat',1354,461,27,True,INK,'middle')
 p.path('M 539 516 C 621 680 673 721 674 721',stroke=BLUE,w=12)
 p.arrow((674,721),(685,725),BLUE,5)
 p.path('M 1060 709 C 1210 600 1198 536 1215 512',stroke=BLUE,w=12)
 p.arrow((1201,521),(1217,503),BLUE,5)
 p.path('M 1275 373 Q 893 180 439 370',stroke=GREEN,w=10)
 p.arrow((582,316),(445,370),GREEN,6)
 p.note('Stopovers provide food and resting sites; exact routes differ among species.',276,896,27)
 p.note('Many migrants cross South Asia, including Indian coastal and inland wetlands.',230,940,24)
record('u5-bird-migration-flyway-stopovers','bird_migration_stopovers_en','Migratory birds: breeding, stopover and wintering','Conceptual migration network; no species-specific route inferred',bird_migrate,[OPENSTAX],'Seasonal routes often require wetland stopovers; not every bird migrates.')

def mammal_tree(p):
 p.box(111,230,1576,742,'THERIA AND MONOTREMATA — LIVING MAMMALS')
 p.text('MAMMALIA',214,389,44,True,BLUE)
 p.line((410,425),(411,819),BLUE,10)
 p.line((411,493),(571,493),BLUE,8)
 p.box(599,427,920,130,'MONOTREMATA  — egg laying')
 p.line((411,657),(509,657),BLUE,8);p.text('THERIA',521,666,34,True,BLUE)
 p.line((674,657),(674,847),BLUE,8)
 p.line((674,729),(762,729),BLUE,7);p.box(775,673,738,112,'MARSUPIALIA  — short gestation / teat')
 p.line((674,848),(762,848),BLUE,7);p.box(775,792,738,112,'PLACENTALIA  — diverse placentas')
 p.note('The diagram is branching, not a sequence from “lower” to “higher” mammals.',177,1018,25)
record('u5-mammalia-classification-mammal-lineages','living_mammal_lineages_en','Living mammals: evolutionary lineages','Monotremata and the two major therian lineages',mammal_tree,[OPENSTAX],'Monotremes lay eggs; marsupials and placentals are distinct therian lineages.')

def rabbit_ext(p):
 s=rabbit(p,238,295,1.09)
 p.label('Pinna (external ear)',530,214,s(151,0));p.label('Laterally placed eye',106,393,s(128,205))
 p.label('Cleft upper lip',96,791,s(40,296));p.label('Vibrissae (whiskers)',92,872,s(12,275));p.label('Short tail',1407,474,s(988,302))
 p.label('Fur-covered trunk',1246,333,s(694,178));p.label('Strong hindlimb',1260,838,s(798,474));p.label('Hind foot',1192,951,s(950,538))
 p.note('Lagomorph, not rodent; a second pair of small upper incisors is diagnostic.',290,1029,24)
record('u5-rabbit-external','rabbit_external_anatomy_en','Rabbit: external anatomy','Oryctolagus cuniculus · lateral anatomical outline',rabbit_ext,[OPENSTAX],'Pinna, large hindlimbs, vibrissae, fur, cleft upper lip and short tail.')

def rabbit_sense(p):
 panels=[(92,'SIDE-PLACED EYES'),(650,'MOBILE PINNAE'),(1207,'VIBRISSAE')]
 for x,name in panels:p.box(x,238,511,721,name)
 p.ell((352,592),139,95,FILL,INK,5)
 p.circle(351,589,72,WHITE,BLUE,6);p.circle(352,589,33,INK,INK,1)
 p.arrow((280,488),(196,420),BLUE,5);p.arrow((423,488),(504,418),BLUE,5)
 p.note('Broad visual field',205,842,26)
 p.path('M 893 763 Q 691 442 812 327 Q 980 301 1008 672 Q 998 772 893 763 Z',FILL,INK,6)
 p.path('M 898 701 Q 799 432 853 397 Q 950 398 945 701',stroke=BROWN,w=8)
 p.note('Directed sound capture',681,842,24)
 p.ell((1459,588),140,100,FILL,INK,5)
 for i in range(9):
  y=544+i*15;p.path(f'M 1369 {y} Q 1273 {y-70} 1249 {y-60}',stroke=GRAY,w=2)
 p.circle(1484,567,14,INK,INK,2)
 p.note('Touch receptors at roots',1235,842,23)
 p.note('Mammals also have three middle-ear ossicles and an inner-ear vestibular system.',243,1021,25)
record('u5-rabbit-sense-organs','rabbit_senses_en','Rabbit: sight, hearing and touch','Lateral eyes, mobile pinnae and facial vibrissae',rabbit_sense,[OPENSTAX],'Eye placement gives broad view; large pinnae detect sound; vibrissae support touch.')

def marsupial(p):
 boxes=[('MATERNAL GESTATION','Develops in uterus'),('EARLY BIRTH','Small underdeveloped young'),('TEAT ATTACHMENT','Milk-fuelled development'),('JUVENILE','Growth beyond teat attachment')]
 for i,(h,txt) in enumerate(boxes):
  x=70+(i%2)*862;y=222+(i//2)*388;p.box(x,y,819,350,h)
  p.text(txt,x+32,y+115,25,False,GRAY)
  if i==0:p.ell((x+440,y+232),91,64,FILL,INK,4)
  if i==1:
   p.ell((x+426,y+219),55,37,FILL,INK,4)
   p.path(f'M {x+453} {y+242} Q {x+520} {y+298} {x+469} {y+312}',stroke=INK,w=12)
  if i==2:
   p.path(f'M {x+353} {y+273} Q {x+427} {y+138} {x+531} {y+273}',stroke=INK,w=5)
   p.ell((x+439,y+250),53,37,FILL,INK,4)
   p.circle(x+440,y+216,14,'#ead5cc',RED,4)
  if i==3:
   p.ell((x+431,y+214),95,74,FILL,INK,4)
   p.circle(x+354,y+157,39,FILL,INK,4)
  if i==0:p.arrow((x+800,y+267),(x+858,y+267),BLUE,5)
  if i==2:p.arrow((x+800,y+267),(x+858,y+267),BLUE,5)
 p.note('Pouch presence and form vary widely; many marsupials form a placenta of some kind.',217,1035,23)
record('u5-marsupials-marsupial-life-history','marsupial_life_cycle_en','Marsupial reproduction: life-history stages','Short gestation and development after birth; not all species have a permanent pouch',marsupial,[OPENSTAX],'Young are often born early and continue development attached to a teat.')

def marine_groups(p):
 entries=[('CETACEA','Whales / dolphins','Fluked tail + foreflippers'),('SIRENIA','Dugongs / manatees','Herbivores, paddle flippers'),('PINNIPEDIA','Seals / sea lions','Carnivorans with flippers'),('SEA OTTERS','Aquatic mustelids','Carnivorans; fur insulation')]
 for i,(name,ex,feature) in enumerate(entries):
  x=87+(i%2)*856;y=220+(i//2)*389;p.box(x,y,807,366,name)
  p.text(ex,x+30,y+96,26,False,BLUE)
  # distinctive anatomical feature concept icons: tail/flipper, paddle, flippers, fur
  cx=x+460;cy=y+226
  if i==0:
   p.ell((cx-45,cy),158,55,FILL,INK,5)
   p.poly([(cx+82,cy),(cx+204,cy-79),(cx+180,cy+7),(cx+209,cy+78)],FILL,INK,4)
   p.poly([(cx-60,cy+43),(cx+19,cy+140),(cx+35,cy+33)],FILL,INK,4)
  elif i==1:
   p.ell((cx-22,cy),173,78,FILL,INK,5)
   p.ell((cx-65,cy+62),72,39,FILL,INK,4)
  elif i==2:
   p.ell((cx-22,cy),165,76,FILL,INK,5)
   p.poly([(cx-6,cy+39),(cx+51,cy+155),(cx+130,cy+74)],FILL,INK,5)
  else:
   p.ell((cx-10,cy),169,70,FILL,INK,5)
   p.circle(cx-161,cy-31,55,FILL,INK,4)
   for j in range(25):p.line((cx-100+j*9,cy-25+(j%4)*14),(cx-97+j*9,cy-8+(j%4)*14),GRAY,2)
  p.note(feature,x+25,y+324,23)
 p.note('Similar aquatic body shapes evolved independently in several mammalian lineages.',221,1015,25)
record('u5-aquatic-mammals-aquatic-mammal-groups','aquatic_mammal_lineages_en','Aquatic mammals: distinct evolutionary origins','Comparative forms of cetaceans, sirenians and aquatic carnivorans',marine_groups,[NOAA],'Streamlining arose repeatedly; aquatic mammals do not form one taxonomic order.')

if __name__=='__main__':
 # Dynamically include records without discarding pre-existing approved/QA files.
 manifest_path=OUT/'manifest.json'
 registry=json.loads((ASSETS/'figure_slots.json').read_text(encoding='utf-8'))
 existing=json.loads(manifest_path.read_text(encoding='utf-8'))
 known={s['id'] for s in registry['slots']}
 assert len(ROWS)==32, ('Expected 32 missing slots',len(ROWS))
 assert len({r['diagramId'] for r in ROWS})==len(ROWS)
 assert all(r['diagramId'] in known for r in ROWS)
 earlier={r['diagramId'] for r in existing['figures']}
 new_ids={r['diagramId'] for r in ROWS}
 assert all(r['reviewStatus'].startswith('PROVISIONAL_') for r in existing['figures'] if r['diagramId'] in new_ids), 'Refusing to overwrite independently approved drawings'
 slotdata={item['id']:item for item in registry['slots']}
 for r in ROWS:
  info=slotdata[r['diagramId']]
  r['topicId']=info['topicId'];r['page']=info['page'];r['sectionKey']=info['sectionKey']
  r['learningObjective']=r['keyEn']
  r['svgSha256']=hashlib.sha256((ROOT/r['svgMaster']).read_bytes()).hexdigest()
 existing['figures']=[r for r in existing['figures'] if r['diagramId'] not in new_ids]+ROWS
 existing['status']='PROVISIONAL_QA_NOT_ACADEMICALLY_APPROVED'
 existing['displayPolicy']='All anatomical drawings have English labels in both language modes; bilingual lesson text and caption remain separate; independent scientific and Tamil sign-off pending.'
 manifest_path.write_text(json.dumps(existing,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('ADDED',len(ROWS),'SLOTS',len({r['diagramId'] for r in existing['figures']}),'VARIANTS',len(existing['figures']))
