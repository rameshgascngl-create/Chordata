#!/usr/bin/env python3
"""Generate original provisional anatomy teaching plates for the CHORDATA native app.

No copied source images. English labels appear in both language modes. Figures are
schematic and require independent expert acceptance prior to production release.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, random, hashlib, json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/pencil_plates'
W,H=1800,1120
DARK='#24333a'; MUTED='#60717a'; LIGHT='#edf1ee'; MID='#c8d5d1'; ACC='#305c6c'; WHITE='#ffffff'; FILL='#e4ebea'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def f(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)

def new(title,subtitle):
    im=Image.new('RGB',(W,H),WHITE);d=ImageDraw.Draw(im)
    d.text((78,35),title,font=f(64,True),fill=DARK);d.text((82,116),subtitle,font=f(31),fill=MUTED)
    d.line([(78,172),(1722,172)],fill=ACC,width=4)
    d.text((82,1070),'ORIGINAL SCHEMATIC • NOT TO SCALE • ACADEMIC REVIEW PENDING',font=f(22),fill=MUTED)
    return im,d

def line(d,coords,width=6,color=DARK,joint='curve'):d.line(coords,fill=color,width=width,joint=joint)
def ellipse(d,coords,fill=FILL,outline=DARK,width=5):d.ellipse(coords,fill=fill,outline=outline,width=width)
def poly(d,coords,fill=FILL,width=6):d.polygon(coords,fill=fill);d.line(coords+[coords[0]],fill=DARK,width=width,joint='curve')
def arrow(d,a,b,color=ACC,width=6):
    line(d,[a,b],width,color); ang=math.atan2(b[1]-a[1],b[0]-a[0]);r=19
    d.polygon([b,(b[0]-r*math.cos(ang-0.45),b[1]-r*math.sin(ang-0.45)),(b[0]-r*math.cos(ang+0.45),b[1]-r*math.sin(ang+0.45))],fill=color)
def label(d,s,x,y,to=None,side='left',size=33):
    d.text((x,y),s,font=f(size,True),fill=DARK)
    if to:
        bbox=d.textbbox((x,y),s,font=f(size,True)); beg=(bbox[2]+13,y+19) if side=='right' else (x-17,y+19)
        line(d,[beg,to],3,ACC);d.ellipse((to[0]-6,to[1]-6,to[0]+6,to[1]+6),fill=ACC)

def caption(d,s,x,y,size=30):d.text((x,y),s,font=f(size),fill=MUTED)
def save(im,n):
    p=OUT/(n+'.png');im.save(p,optimize=True);return p

def shark_sense():
    im,d=new('Scoliodon: major sensory systems','Lateral line (mechanoreception) and ampullae (electroreception) are distinct')
    # Profile, cephalic region at left. Features indicative, not a taxonomic specimen plate.
    outline=[(145,460),(215,412),(340,382),(510,365),(675,372),(818,397),(947,386),(1080,416),(1170,451),(1227,436),(1260,469),(1222,496),(1070,521),(903,535),(726,565),(548,573),(365,548),(203,512)]
    poly(d,outline,fill='#e2e8e6',width=7)
    poly(d,[(551,367),(631,270),(660,378)],fill='#dae3e1',width=6)
    poly(d,[(600,554),(702,707),(733,550)],fill='#d1dedc',width=6)
    ellipse(d,(305,421,342,458),fill=DARK,width=3)
    line(d,[(172,469),(251,488),(306,485)],4)
    # Note external nares are ventral, drawn schematic as ventral inset.
    line(d,[(188,502),(229,494)],5)
    for j in range(5):
        x=401+j*24
        d.arc((x,428,x+28,532),257,82,fill=DARK,width=5)
    # Lateral-line canal follows the trunk; dotted pores communicate with water.
    line(d,[(341,404),(485,402),(658,408),(823,418),(1000,440),(1146,454)],7,ACC)
    for x,y in [(386,404),(435,402),(485,402),(540,404),(600,406),(670,410),(739,414),(805,417),(880,426),(955,434),(1012,442),(1090,449)]:d.ellipse((x-5,y-5,x+5,y+5),fill=WHITE,outline=ACC,width=3)
    # Snout pores shown only on anterior rostrum.
    for x,y in [(215,443),(241,431),(256,451),(289,458),(277,478),(307,486),(333,473),(345,501)]:d.ellipse((x-4,y-4,x+4,y+4),fill=ACC)
    label(d,'Eye',96,241,(321,441),'right')
    label(d,'Lateral-line canal',842,245,(782,416),'left')
    label(d,'Electroreceptor pores',95,656,(271,468),'right')
    label(d,'Gill slits',655,670,(487,486),'left')
    # Inset distinguishes their respective internal structure / modality.
    d.rounded_rectangle((990,605,1700,1008),radius=24,fill='#f4f7f5',outline=MID,width=4)
    d.text((1033,626),'AMPULLA (section)',font=f(35,True),fill=DARK)
    d.line([(1042,747),(1635,747)],fill=DARK,width=11)
    for x in [1155,1295,1450]:
        d.ellipse((x-12,733,x+12,755),fill=WHITE,outline=ACC,width=4)
        d.line([(x,758),(x,850)],fill=ACC,width=9)
        ellipse(d,(x-26,834,x+26,899),fill='#d1e0e0',outline=ACC,width=4)
        line(d,[(x,901),(x+26,945)],3,MUTED)
    caption(d,'skin pores',1024,770,25);caption(d,'gel-filled ducts',1467,814,25)
    caption(d,'receptor bulbs',1450,863,25);caption(d,'nerve fibres',1295,946,25)
    caption(d,'Mechanosensory neuromasts ≠ electroreceptor ampullae',96,949,27)
    return save(im,'shark_sensory_systems_en')

def rana_external():
    im,d=new('Indian green pond frog: external features','Phrynoderma hexadactylum (syllabus: Rana hexadactyla)')
    # Lateral illustration. Hind-limb joints are mapped anatomically: thigh, crus, tarsus.
    ellipse(d,(450,405,1236,751),fill='#e3e9e5',width=7)
    ellipse(d,(275,352,590,597),fill='#e3e9e5',width=7)
    # Snout, mandibular line, nostril, eye and tympanic membrane.
    poly(d,[(284,450),(177,476),(213,520),(347,551),(441,563)],fill='#e2e9e4',width=5)
    ellipse(d,(387,394,460,463),fill='#f7f8f4',width=5);ellipse(d,(414,405,440,438),fill=DARK,width=2)
    ellipse(d,(502,474,568,538),fill='#d3dbd7',width=4)
    ellipse(d,(267,469,282,484),fill=DARK,width=2)
    line(d,[(214,517),(324,525),(421,519)],3)
    # Forelimbs support trunk; all toes stop within frame.
    poly(d,[(562,635),(625,658),(611,802),(577,833),(557,811)],fill='#d0dcd6',width=5)
    for a,b in [((577,830),(494,848)),((582,833),(551,884)),((588,833),(624,866)),((590,834),(650,845))]:line(d,[a,b],8)
    # Thigh, shank, ankle and webbed toes.
    poly(d,[(960,616),(1174,662),(1328,774),(1277,844),(1116,755),(980,734)],fill='#d6e1db',width=6)
    poly(d,[(1268,813),(1443,725),(1493,761),(1365,873)],fill='#d8e1db',width=5)
    poly(d,[(1350,862),(1512,866),(1620,935),(1448,955)],fill='#e5ebe6',width=4)
    for tip in [(1535,905),(1617,949),(1590,981),(1514,986),(1468,963)]:line(d,[(1440,898),tip],5)
    # Interdigital membrane, not joined to all toe tips.
    d.polygon([(1450,914),(1535,911),(1590,950),(1532,963),(1474,956)],fill='#d7e4e0')
    # Subtle skin stippling.
    rng=random.Random(7406)
    for _ in range(470):
        x=rng.randrange(505,1168);y=rng.randrange(460,711)
        if ((x-840)/390)**2+((y-578)/169)**2<.88:d.ellipse((x,y,x+2,y+2),fill=MUTED)
    label(d,'External nostril',88,252,(274,475),'right')
    label(d,'Eye',566,261,(430,421),'left')
    label(d,'Tympanic membrane',835,306,(536,500),'left')
    label(d,'Moist glandular skin',1070,393,(1050,552),'left')
    label(d,'Forelimb',88,671,(585,723),'right')
    label(d,'Hindlimb',1213,589,(1230,736),'left')
    label(d,'Webbed hind foot',1221,997,(1496,942),'left',30)
    return save(im,'rana_external_en')

def rana_respiration():
    im,d=new('Frog respiration: three adult surfaces','Cutaneous, buccopharyngeal and pulmonary gas exchange')
    # Three compartmental figures; emphasize separate structures without invented connections.
    blocks=[(70,207,604,991),(633,207,1170,991),(1199,207,1736,991)]
    for b in blocks:d.rounded_rectangle(b,radius=22,fill='#f5f8f7',outline=MID,width=4)
    d.text((111,239),'A  CUTANEOUS',font=f(38,True),fill=DARK)
    d.text((669,239),'B  BUCCOPHARYNGEAL',font=f(32,True),fill=DARK)
    d.text((1237,239),'C  PULMONARY',font=f(36,True),fill=DARK)
    # Skin barrier and dense superficial capillaries (section)
    d.polygon([(110,474),(564,459),(564,570),(110,589)],fill='#dbe6df')
    for x in range(128,557,34):
        d.line([(x,459+8*math.sin(x/30)),(x+24,472+7*math.sin(x/30))],fill=DARK,width=3)
    for x in range(170,560,90):d.ellipse((x,528,x+19,547),fill=ACC)
    d.arc((144,610,538,792),185,355,fill='#527886',width=14)
    for x in (190,270,360,450):arrow(d,(x,413),(x,505),width=4)
    for x in (230,395):arrow(d,(x,628),(x,581),width=4)
    caption(d,'Moist skin',176,364,30)
    caption(d,'Capillary network',125,799,30)
    caption(d,'O₂ inward  |  CO₂ outward',120,876,28)
    # Buccal cavity as surface lined with capillaries.
    d.arc((690,403,1108,705),25,160,fill=DARK,width=11)
    line(d,[(734,553),(788,594),(946,613),(1030,573)],9)
    d.arc((745,567,1019,687),6,171,fill=ACC,width=11)
    for x in range(780,994,34):
        d.ellipse((x,661,x+17,677),fill=ACC)
    arrow(d,(791,400),(791,500));arrow(d,(883,412),(883,515));arrow(d,(989,400),(989,520))
    caption(d,'Buccal mucosa',725,743,31)
    caption(d,'Capillaries beneath mucosa',681,808,24)
    caption(d,'Gas exchange with moist lining',681,880,24)
    # Pulmonary system is branching paired sacs from a glottis; *not* direct from nostrils to lungs.
    ellipse(d,(1406,360,1470,417),fill='#d9e3e0')
    line(d,[(1435,419),(1435,530)],15)
    line(d,[(1435,528),(1355,597),(1321,627)],11)
    line(d,[(1435,528),(1509,597),(1545,627)],11)
    ellipse(d,(1241,618,1420,848),fill='#dee7e3',width=7)
    ellipse(d,(1456,618,1639,848),fill='#dee7e3',width=7)
    for x0 in (1260,1476):
        for k in range(5):d.arc((x0+9,655+k*30,x0+137,698+k*30),5,170,fill=ACC,width=3)
    arrow(d,(1435,345),(1435,466),width=6)
    caption(d,'Glottis',1485,420,29)
    caption(d,'Air passage',1247,522,28)
    caption(d,'Paired lungs',1298,907,31)
    return save(im,'rana_respiration_en')

def calotes_external():
    im,d=new('Calotes versicolor: external anatomy','Oriental garden lizard • characteristic agamid body plan')
    # Adult lateral profile with crest, four pentadactyl limbs, tail.
    path=[(192,497),(271,456),(344,452),(410,481),(595,487),(762,483),(917,506),(1067,513),(1227,523),(1386,537),(1657,569),(1386,583),(1197,606),(1018,633),(888,653),(673,653),(500,620),(355,574),(252,546)]
    poly(d,path,fill='#e3e8e1',width=7)
    # Dorsal crest increases over the back; avoid implying uniform spikes to tail.
    for k in range(18):
        x=450+k*33;y=481+8*math.sin(k/2)
        poly(d,[(x-12,y+8),(x+6,y-26-(13 if 5<k<10 else 3)),(x+22,y+8)],fill='#cdd8d0',width=2)
    ellipse(d,(256,477,295,516),fill='#f9f9f4',width=3);ellipse(d,(268,487,282,504),fill=DARK,width=2)
    ellipse(d,(330,511,369,548),fill='#d7ded6',width=3)
    d.ellipse((207,513,222,522),fill=DARK)
    line(d,[(196,531),(274,543),(354,550)],3)
    # Two visible pairs of limbs, segmented and clawed toes.
    for (top,elbow,foot) in [((555,610),(491,742),(388,836)),((902,619),(933,779),(1004,833))]:
        line(d,[top,elbow,foot],29,'#cbd5cc');line(d,[top,elbow,foot],6,DARK)
        for j in range(5):
            toe=(foot[0]+(j-2)*28,foot[1]+(j%2)*18+20)
            line(d,[foot,toe],6);line(d,[toe,(toe[0]-6,toe[1]+11)],2)
    # scales: diamond schematic, aligned and sparse.
    for y in (552,582,612):
        for x in range(455,912,35):
            if ((x-695)/280)**2+((y-563)/112)**2<1:d.arc((x,y,x+20,y+16),190,355,fill=MUTED,width=2)
    label(d,'External naris',82,292,(219,519),'right')
    label(d,'Eye',505,295,(275,495),'left')
    label(d,'Tympanum',745,346,(349,532),'left')
    label(d,'Dorsal crest',996,304,(761,475),'left')
    label(d,'Keratinised scales',112,695,(628,580),'right')
    label(d,'Five clawed digits',87,931,(401,851),'right')
    label(d,'Long tail',1339,708,(1354,558),'left')
    return save(im,'calotes_external_en')

def rabbit_brain():
    im,d=new('Rabbit brain: lateral landmarks','Schematic regions, not an MRI or a specimen dissection')
    # Rostral is left. Smooth cerebral hemispheres comprise front/central brain.
    ellipse(d,(389,415,1050,770),fill='#e3ebe8',width=8)
    ellipse(d,(954,497,1259,741),fill='#d1deda',width=8)
    # Olfactory bulbs at anterior portion
    ellipse(d,(252,508,448,610),fill='#e9efeb',width=7)
    ellipse(d,(1281,574,1430,668),fill='#d9e4e0',width=7)
    line(d,[(1240,613),(1305,617),(1390,624),(1557,629)],25,'#d7e2de')
    line(d,[(1240,613),(1305,617),(1390,624),(1557,629)],5)
    # Cerebral sulci few shallow curved grooves, not excessive artificial folds.
    for x in (562,661,762,857):
        d.arc((x,480,x+140,694),145,246,fill=MUTED,width=4)
    for y in (535,565,598,629,660):
        d.arc((989,y,1211,y+70),0,159,fill=MUTED,width=3)
    # Midbrain under cerebrum, medulla before cord.
    poly(d,[(892,742),(988,727),(1131,743),(1230,701),(1297,670),(1300,712),(1156,789),(952,790)],fill='#d2dfda',width=5)
    label(d,'Olfactory bulbs',76,279,(325,558),'right')
    label(d,'Cerebral hemispheres',646,255,(720,494),'left')
    label(d,'Cerebellum',1233,350,(1108,570),'left')
    label(d,'Medulla oblongata',1092,854,(1251,717),'left')
    label(d,'Spinal cord',1430,746,(1512,632),'left')
    d.text((92,955),'Anterior / rostral',font=f(32,True),fill=ACC)
    d.text((1317,955),'Posterior / caudal',font=f(32,True),fill=ACC)
    arrow(d,(520,969),(1002,969))
    return save(im,'rabbit_brain_en')

def bat_glider():
    im,d=new('Powered flight and gliding: wing support','Bat hand skeleton versus patagium supported by body and limbs')
    d.rounded_rectangle((83,228,861,992),radius=24,fill='#f4f7f5',outline=MID,width=4)
    d.rounded_rectangle((935,228,1711,992),radius=24,fill='#f4f7f5',outline=MID,width=4)
    d.text((132,258),'A  BAT — POWERED FLIGHT',font=f(36,True),fill=DARK)
    d.text((987,258),'B  GLIDING MAMMAL',font=f(37,True),fill=DARK)
    # Bat wing hand from shoulder at lower left radiates to right. Finger I free and clawed.
    shoulder=(252,744);wrist=(455,657);elbow=(336,694)
    membrane=[shoulder,(328,543),(479,379),(626,327),(812,408),(815,662),(666,803),(452,760)]
    poly(d,membrane,fill='#e2eae7',width=6)
    line(d,[shoulder,elbow,wrist],19,'#9baba7');line(d,[shoulder,elbow,wrist],5,DARK)
    for tip in [(479,379),(626,327),(812,408),(815,662)]:line(d,[wrist,tip],10,'#8ba49d');line(d,[wrist,tip],3,DARK)
    line(d,[wrist,(383,591),(367,562)],10,'#9aaca5')
    d.arc((343,540,379,582),100,260,fill=DARK,width=4)
    label(d,'Elongated digits II–V',117,851,(668,482),'right',25)
    label(d,'Free thumb (digit I)',120,914,(371,572),'right',25)
    # Schematic glider: four limbs at four corners and broad edge membrane.
    body=[(1272,456),(1322,466),(1357,580),(1334,753),(1290,755),(1266,590)]
    poly(d,body,fill='#d7e2dd',width=6)
    poly(d,[(1308,460),(1009,523),(1024,845),(1282,770),(1329,773),(1667,841),(1649,528)],fill='#e1e9e6',width=6)
    # limb bones support patagium near corners rather than extended fingers.
    for a,b in [((1283,526),(1026,569)),((1340,528),(1642,566)),((1297,714),(1036,812)),((1337,711),(1639,805))]:line(d,[a,b],16,'#98aaa4');line(d,[a,b],4,DARK)
    ellipse(d,(1276,391,1363,479),fill='#d2ddd6',width=5)
    label(d,'Patagium',1474,886,(1503,686),'left',28)
    label(d,'Four limbs',963,905,(1073,788),'right',28)
    caption(d,'Not a bird wing: digit rays carry the membrane.',129,947,22)
    caption(d,'Membrane stretched between limbs; no powered flight.',978,953,21)
    return save(im,'bat_glider_comparison_en')

def dipnoi():
    im,d=new('Lungfish: paired fins and lungs','Living Dipnoi share a common ancestor with tetrapods; they are not their direct ancestors')
    # upper panel lobed fins
    d.rounded_rectangle((90,222,852,992),radius=20,fill='#f5f8f7',outline=MID,width=4)
    d.rounded_rectangle((889,222,1706,992),radius=20,fill='#f5f8f7',outline=MID,width=4)
    d.text((126,258),'A  LOBED FIN (SCHEMATIC)',font=f(32,True),fill=DARK)
    d.text((935,258),'B  RESPIRATORY ORGANS',font=f(33,True),fill=DARK)
    # Fin cross section: basal axis from body supports rays, not an amphibian limb.
    ellipse(d,(145,492,453,766),fill='#e0e7e2',width=6)
    poly(d,[(385,567),(718,350),(765,381),(482,716)],fill='#d5e0db',width=5)
    line(d,[(403,620),(698,402)],19,'#8ea49b')
    for j in range(9):
        x=445+j*27;y=588-j*24
        line(d,[(x,y),(x+92,y-65)],3,MUTED)
    label(d,'Fleshy base',140,379,(415,646),'right',28)
    label(d,'Internal supporting axis',110,826,(604,471),'right',26)
    label(d,'Fin rays',556,764,(700,372),'left',28)
    # Right panel paired lungs generalised; note species differences.
    line(d,[(1292,378),(1292,535)],15)
    line(d,[(1292,524),(1194,593),(1180,640)],12)
    line(d,[(1292,524),(1390,592),(1406,642)],12)
    ellipse(d,(1098,634,1267,843),fill='#dbe5df',width=7)
    ellipse(d,(1322,631,1501,840),fill='#dbe5df',width=7)
    for x in (1128,1350):
        for y in (688,734,775):d.arc((x,y,x+95,y+70),5,167,fill=MUTED,width=3)
    label(d,'Air passage',1394,388,(1293,448),'left',27)
    label(d,'Paired lung sacs',987,871,(1390,735),'right',28)
    caption(d,'*Diagram represents paired-lung condition.',964,925,24)
    caption(d,'Neoceratodus has a single lung.',964,959,24)
    return save(im,'dipnoi_lungfin_comparison_en')

def shark_digestive():
    im,d=new('Scoliodon: digestive tract and spiral intestine','Diagram of the digestive pathway; simplified relative sizes')
    # Continuous foregut: oral cavity -> oesophagus -> J-shaped stomach -> pylorus.
    poly(d,[(258,340),(340,315),(440,339),(431,387),(345,411)],fill='#e6ece7',width=6)
    # Points create a continuous anatomical pathway. Double stroke outlines the lumen.
    def cubic(p0,p1,p2,p3,n=24):
        return [((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0],
                 (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1])
                for t in (i/n for i in range(n+1))]
    tract=(cubic((413,366),(504,355),(615,354),(665,415))+
           cubic((665,415),(702,520),(615,702),(753,721))+
           cubic((753,721),(876,757),(939,538),(1038,581)))
    # Deep stroke is organ border; light inner stroke gives a visibly uninterrupted tract.
    line(d,tract,70,DARK)
    line(d,tract,58,'#dbe6e0')
    # Internal stomach curve; no impression that stomach is an open ring.
    line(d,cubic((691,509),(710,601),(674,660),(752,678)),4,MUTED)
    # Spiral valve intestine large continuous tube with internal spiral not transverse villi.
    poly(d,[(1042,549),(1230,559),(1261,646),(1231,838),(1081,837),(1049,743)],fill='#e2e9e4',width=6)
    for k in range(5):
        y=594+k*46
        d.arc((1079,y,1235,y+54),5,168,fill=ACC,width=5)
    line(d,[(1154,838),(1154,932)],18,'#c4d5d0')
    # Liver drawn lateral to tract without false direct connection.
    ellipse(d,(568,775,895,1008),fill='#e2e8df',width=6)
    d.ellipse((828,923,873,977),fill='#f1f3e3',outline=DARK,width=3)
    line(d,[(848,924),(921,790),(1058,637)],5,ACC)
    # Pancreas near pylorus attached symbolically with label.
    ellipse(d,(865,667,1010,737),fill='#dce5dd',width=4)
    label(d,'Mouth / buccal cavity',92,222,(317,354),'right',29)
    label(d,'Oesophagus',538,221,(499,369),'left',31)
    label(d,'Stomach',774,284,(711,550),'left',30)
    label(d,'Pyloric region',963,347,(967,559),'left',27)
    label(d,'Spiral-valve intestine',1293,560,(1179,678),'left',30)
    label(d,'Rectum → cloaca',1305,881,(1154,910),'left',29)
    label(d,'Liver',220,845,(713,856),'right',31)
    label(d,'Gall bladder',282,975,(853,956),'right',27)
    label(d,'Pancreas',814,794,(946,705),'right',27)
    return save(im,'scoliodon_digestive_en')

GENERATORS=[shark_sense,rana_external,rana_respiration,calotes_external,rabbit_brain,bat_glider,dipnoi,shark_digestive]

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    for fn in GENERATORS:
        p=fn(); print(p.name,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
