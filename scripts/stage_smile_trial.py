"""Stage verified accepted ear build assets plus the approved smile, never deploy."""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'.local/phase-08/trial';NEW=ROOT/'.local/phase-09/assets';OUT=ROOT/'.local/phase-09/trial'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=json.loads((BASE/'verified-assets.json').read_text())
for name,digest in records.items():
    assert sha(BASE/name)==digest,name
    dest=OUT/name;dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(BASE/name,dest);assert sha(dest)==digest
manifest=json.loads((NEW/'manifest.json').read_text())
for name,digest in manifest['hashes'].items():
    assert sha(NEW/name)==digest,name
    if name.endswith('.png'):
        with Image.open(NEW/name) as image:
            assert image.mode=='RGBA' and image.size==(400,400)
            bounds=image.getchannel('A').getbbox()
            assert bounds and min(bounds[:2])>0 and max(bounds[2:])<400
    shutil.copy2(NEW/name,OUT/'assets'/name)
    assert sha(OUT/'assets'/name)==digest
    records['assets/'+name]=digest
for f in (1,28):assert (NEW/('smile_%04d.png'%f)).read_bytes()==(OUT/'assets/idle_0001.png').read_bytes()
for name in ('stitch.ico','reference.csv','inputs.csv'):shutil.copy2(BASE/name,OUT/name)
(OUT/'verified-assets.json').write_text(json.dumps(records,indent=2)+'\n')
print('SMILE_STAGE_VERIFIED',len(records),'files')
