"""Stage hash-verified accepted banks plus both new ear clips, never deploy."""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'.local/phase-07/trial'
NEW=ROOT/'.local/phase-08/assets'
OUT=ROOT/'.local/phase-08/trial'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=json.loads((BASE/'verified-assets.json').read_text())
for name,digest in records.items():
    assert sha(BASE/name)==digest,name
    dest=OUT/name;dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(BASE/name,dest);assert sha(dest)==digest
manifest=json.loads((NEW/'manifest.json').read_text())
for name,digest in manifest['hashes'].items():
    assert sha(NEW/name)==digest,name
    shutil.copy2(NEW/name,OUT/'assets'/name)
    assert sha(OUT/'assets'/name)==digest
    records['assets/'+name]=digest
for name in ('stitch.ico','reference.csv','inputs.csv'):shutil.copy2(BASE/name,OUT/name)
boards=[]
for f in range(1,17):
    board=Image.new('RGB',(800,425),'#edf0f3');draw=ImageDraw.Draw(board)
    for x,side in [(0,'left'),(400,'right')]:
        with Image.open(NEW/('ear_%s_%04d.png'%(side,f))) as im:
            assert im.size==(400,400) and im.mode=='RGBA'
            bounds=im.getchannel('A').getbbox()
            assert bounds and min(bounds[:2])>0 and max(bounds[2:])<400
            board.paste(im,(x,25),im)
        draw.text((x+12,8),'Viewer-'+side+' ear',fill='#20262e')
    boards.append(board)
for side in ('left','right'):
    for f in (1,16):assert (NEW/('ear_%s_%04d.png'%(side,f))).read_bytes()==(OUT/'assets/idle_0001.png').read_bytes()
seq=[boards[0]]*12+boards+[boards[-1]]*24
duration=[(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(seq))]
seq[0].save(NEW/'both-ears-review.gif',save_all=True,append_images=seq[1:],loop=0,duration=duration,disposal=2)
boards[4].save(NEW/'both-ears-peak.png')
(OUT/'verified-assets.json').write_text(json.dumps(records,indent=2)+'\n')
print('EAR_STAGE_VERIFIED',len(records),'files; all bounds and exact neutral endpoints pass.')
