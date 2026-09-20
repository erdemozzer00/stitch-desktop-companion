"""Stage only verified accepted + peace assets in the isolated hand trial."""
import hashlib, json, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.local/phase-07/trial'
BASE=ROOT/'.local/phase-03/appearance-final'
NEW=ROOT/'.local/phase-07/assets'
BANK=ROOT/'.local/phase-04/carry-final'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(source,target,expected):
    assert digest(source)==expected,source
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)
    assert digest(target)==expected,target
records={}
for clip in ('idle','wave','entries'):
    manifest=json.loads((BASE/clip/'manifest.json').read_text())
    for name,sha in manifest['frame_sha256'].items():
        copy(BASE/clip/name,OUT/'assets'/name,sha);records['assets/'+name]=sha
manifest=json.loads((NEW/'manifest.json').read_text())
assert manifest['frames']==60 and manifest['samples']==24 and manifest['size']==400
for name,sha in manifest['frame_sha256'].items():
    copy(NEW/name,OUT/'assets'/name,sha);records['assets/'+name]=sha
copy(NEW/'hands.csv',OUT/'assets/hands.csv',manifest['hands_sha256'])
records['assets/hands.csv']=manifest['hands_sha256']
bank=json.loads((BANK/'bank-manifest.json').read_text())
assert bank['samples']==24 and bank['size']==400
rows=[]
for y in range(5):
    for x in range(9):
        name='bank_%d_%d.png'%(x,y);record=bank['frames'][name]
        copy(BANK/name,OUT/'carry'/name,record['sha256']);records['carry/'+name]=record['sha256']
        rows.append('%s,%.12f,%.12f'%(name,record['anchor'][0]/400,record['anchor'][1]/400))
(OUT/'carry/anchors.csv').write_text('\n'.join(rows)+'\n')
records['carry/anchors.csv']=digest(OUT/'carry/anchors.csv')
assert (OUT/'assets/peace_0001.png').read_bytes()==(OUT/'assets/idle_0001.png').read_bytes()
assert (OUT/'assets/peace_0060.png').read_bytes()==(OUT/'assets/idle_0001.png').read_bytes()
for name in ('stitch.ico','reference.csv','inputs.csv'):
    shutil.copy2(ROOT/'.local/phase-04/polished-trial'/name,OUT/name)
(OUT/'verified-assets.json').write_text(json.dumps(records,indent=2))
print('Verified and staged',len(records),'asset/support files; accepted neutral endpoints reused.')
