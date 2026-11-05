#!/usr/bin/env python3
"""Conservative, owner-credited Commons intake; not approval or replacement of syllabus figures."""
import hashlib, io, json, os, pathlib, time, urllib.parse, urllib.request
from PIL import Image, ImageOps

ROOT=pathlib.Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'docs/research/credited_image_sources.json').read_text(encoding='utf-8'))['sources']
by_id={r['id']:r for r in records}
SELECTED=['lancelet-labelled','frog-arteries','bird-respiration','pigeon-skeleton','rabbit-skeleton']
DEST=ROOT/'build/commons_image_intake'
OUT=DEST/'figures'
OUT.mkdir(parents=True,exist_ok=True)
credits=[]
for id in SELECTED:
    entry=by_id[id]
    if not entry['diagramId'] or entry['embeddedInApk'] or entry['sourceStatus']!='FOUND_NOT_DOWNLOADED':
        raise SystemExit('Unsafe source record: '+id)
    name=entry['originalFilename'].replace(' ','_')
    digest=hashlib.md5(name.encode('utf-8')).hexdigest()
    url='https://upload.wikimedia.org/wikipedia/commons/'+digest[0]+'/'+digest[:2]+'/'+urllib.parse.quote(name)
    data=None
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={
              'User-Agent':'ChordataZoologyEducationalResearch/0.1 (https://github.com/rameshgascngl-create/Chordata)',
              'Accept':'image/jpeg,image/png'})
            with urllib.request.urlopen(req,timeout=50) as resp:
                if resp.geturl().split('/')[2] not in ('upload.wikimedia.org','commons.wikimedia.org'):
                    raise RuntimeError('Unexpected redirect')
                data=resp.read(12*1024*1024+1)
            if len(data)>12*1024*1024: raise RuntimeError('Image exceeds size cap')
            break
        except Exception as err:
            if attempt==2: raise RuntimeError('Failed to download '+id+': '+repr(err)) from err
            time.sleep(2**attempt)
    assert data is not None
    with Image.open(io.BytesIO(data)) as img:
        if img.format not in ('JPEG','PNG'): raise RuntimeError('Wrong media type '+id)
        img=ImageOps.exif_transpose(img)
        orig=img.size
        img.thumbnail((2200,2200),Image.Resampling.LANCZOS)
        filename=id.replace('-','_')+'.png'
        path=OUT/filename
        img.convert('RGB').save(path,format='PNG',optimize=True)
        output=path.read_bytes()
        if output[:8]!=bytes.fromhex('89504e470d0a1a0a') or len(output)<10000:
            raise RuntimeError('PNG output invalid: '+id)
        changes='Converted to PNG, original aspect ratio retained'
        if img.size!=orig: changes+=', downsampled from '+str(orig)+' to '+str(img.size)
        rec={**entry,'localFile':filename,'originalUrl':url,'originalWidth':orig[0],'originalHeight':orig[1],
             'width':img.width,'height':img.height,'sha256':hashlib.sha256(output).hexdigest(),
             'modifications':changes,'bytes':len(output),
             'reviewStatus':'SOURCE_ONLY_AWAITING_INDEPENDENT_ANATOMICAL_REVIEW'}
        credits.append(rec)
        print('FETCHED',id,orig,'->',img.size,'bytes',len(output))
(DEST/'SOURCE_CREDITS.json').write_text(json.dumps({'sources':credits,'status':'QA_CANDIDATES_NOT_APPROVED'},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
with (DEST/'SOURCE_CREDITS.md').open('w',encoding='utf-8') as f:
    f.write('# Chordata image intake — creators, licences, changes\n\n')
    f.write('**NOT anatomically signed off. Not yet integrated into the production APK.**\n\n')
    for e in credits:
        f.write('## '+e['id']+'\n\n')
        f.write('- Image: '+e['originalFilename']+'\n')
        f.write('- Creator: '+e['creator']+'\n')
        f.write('- Original: '+e['sourcePageUrl']+'\n')
        f.write('- Licence: '+e['license']+' — '+e['licenseUrl']+'\n')
        f.write('- Changes: '+e['modifications']+'\n')
        f.write('- SHA-256: '+e['sha256']+'\n')
        f.write('- Required syllabus diagram: '+e['diagramId']+'\n')
        f.write('- Review: pending, do not count as approved anatomy.\n\n')
print('PASS: '+str(len(credits))+' PNG source images with author/licence/hash inventory')
