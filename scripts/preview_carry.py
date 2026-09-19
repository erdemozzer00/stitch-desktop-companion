"""Assemble a private 04A moving review and measured frame-budget evidence."""
import base64
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.local/phase-04/04a'
manifest = json.loads((OUT / 'motion-manifest.json').read_text())
names = ['idle-01', 'idle-25', 'idle-73', 'wave-04', 'wave-18', 'wave-37']
frames = {}
for name, entries in manifest['clips'].items():
    for entry in entries:
        key = f'{name}_{entry["frame"]:03d}'
        with Image.open(OUT / (key+'.png')) as source:
            frames[key] = source.convert('RGBA')
        assert frames[key].size == (240, 240)
        alpha = frames[key].getchannel('A')
        assert not any(alpha.crop(box).getbbox() for box in [(0,0,240,1),(0,239,240,240),(0,0,1,240),(239,0,240,240)])

sequences = {name: [name+'_001']*12 + [f'{name}_{i:03d}' for i in range(1,11)] +
             [name+'_010']*24 + [f'settle_{i:03d}' for i in range(1,13)] + ['settle_012']*12 + [None]*12 for name in names}
labels = ['source']*12 + ['pickup']*10 + ['held']*24 + ['settle']*12 + ['idle endpoint']*12 + ['TEST RESET - not an animation transition']*12
grip_drift = {}
for name in names:
    anchor = manifest['clips'][name][0]['anchor_400px']
    grip_drift[name] = max(sum((a-b)**2 for a,b in zip(entry['anchor_400px'],anchor))**.5
                          for entry in manifest['clips'][name] + manifest['clips']['settle'])

for background, color, ink in [('light','#eef0f2','#20262e'),('dark','#19202b','#f1f4f8')]:
    boards = []
    for index in range(len(labels)):
        board = Image.new('RGB',(780,570),color)
        draw = ImageDraw.Draw(board)
        draw.text((10,5),'04A DRAFT | 240px / 6 samples | '+labels[index],fill=ink)
        for cell,name in enumerate(names):
            x,y = (cell%3)*260, 28+(cell//3)*270
            draw.text((x+10,y),name+' -> held -> idle',fill=ink)
            if sequences[name][index] is None:
                continue
            board.paste(frames[sequences[name][index]],(x+10,y+20),frames[sequences[name][index]])
            # Fixed source grip marker exposes mesh drift instead of correcting/hiding it.
            ax,ay=manifest['clips'][name][0]['anchor_400px']
            px,py=x+10+ax*.6,y+20+ay*.6
            draw.ellipse((px-2,py-2,px+2,py+2),fill='#ff9944')
        boards.append(board)
    durations=[(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(boards))]
    boards[0].save(OUT/f'review-{background}.gif',save_all=True,append_images=boards[1:],duration=durations,loop=0,optimize=False)
    boards[30].save(OUT/f'held-{background}.png')

board=Image.new('RGB',(1440,1008),'#eef0f2')
draw=ImageDraw.Draw(board)
for row,name in enumerate(names+['settle']):
    for column,entry in enumerate(manifest['clips'][name]):
        key=f'{name}_{entry["frame"]:03d}'
        sprite=frames[key].resize((120,120),Image.Resampling.LANCZOS)
        board.paste(sprite,(column*120,row*144+20),sprite)
        draw.text((column*120+2,row*144+3),name+' '+str(column+1),fill='#20262e')
board.save(OUT/'all-transition-frames.png')

# Self-contained review with exact frame stepping, avoiding GIF-only timing inspection.
payload={k:'data:image/png;base64,'+base64.b64encode((OUT/(k+'.png')).read_bytes()).decode() for k in frames}
html='''<!doctype html><meta charset="utf-8"><title>Stitch 04A — private draft review</title>
<style>body{font:16px system-ui;background:#19202b;color:#edf1f4;margin:24px}button,select,input{margin:6px;padding:8px}canvas{display:block;background:#eef0f2;border-radius:8px}p{max-width:850px}small{color:#aeb8c4}</style>
<h2>04A: tutma ve bırakma hareket denemesi</h2><p>240px / 6 örnek taslak. Masaüstü uygulaması değişmedi. Turuncu nokta sabit gövde tutma referansı; yön/hız tepkisi henüz yok.</p>
<select id="clip"></select><button id="toggle">Duraklat</button><button id="back">Önceki kare</button><button id="next">Sonraki kare</button><button id="bg">Arka plan</button>
<select id="size"><option>240</option><option>320</option><option>400</option></select><small>320/400 bu taslağın büyütülmüş görünümü; üretim çözünürlüğü değil.</small>
<input id="scrub" type="range" min="0" max="81" value="0"><span id="label"></span><canvas id="canvas" width="520" height="470"></canvas>
<p>İncele: el sallama ortasında kolun inişi, ayakların toplanması, bırakınca dönüş ve turuncu noktanın gövdede kayması. Bu önizleme gerçek fare sürüklemesini veya Windows etkileşimini test etmez.</p>
<script>const data=PAYLOAD, seq=SEQUENCES, anchors=ANCHORS, stages=STAGES;const images={};let ready=0;for(const[k,v]of Object.entries(data)){let im=new Image();im.onload=()=>ready++;im.src=v;images[k]=im}
const clip=document.getElementById('clip'),canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d'),scrub=document.getElementById('scrub');for(const name of Object.keys(seq))clip.add(new Option(name,name));let playing=true,dark=false,index=0,previous=0,acc=0;
document.getElementById('toggle').onclick=()=>{playing=!playing;document.getElementById('toggle').textContent=playing?'Duraklat':'Oynat'};
function step(d){playing=false;document.getElementById('toggle').textContent='Oynat';index=(index+d+82)%82;acc=0}
document.getElementById('back').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('bg').onclick=()=>dark=!dark;scrub.oninput=()=>{step(0);index=+scrub.value};clip.onchange=()=>{index=0;acc=0};
function tick(now){const dt=Math.min((now-previous)/1000,.1);previous=now;if(playing&&ready===Object.keys(data).length){acc+=dt;while(acc>=1/24){index=(index+1)%82;acc-=1/24}}ctx.fillStyle=dark?'#19202b':'#eef0f2';ctx.fillRect(0,0,520,470);let s=+document.getElementById('size').value,x=(520-s)/2,y=(470-s)/2,im=images[seq[clip.value][index]];if(im&&im.complete){ctx.drawImage(im,x,y,s,s);let a=anchors[clip.value];ctx.fillStyle='#ff9944';ctx.beginPath();ctx.arc(x+a[0]*s/400,y+a[1]*s/400,3,0,Math.PI*2);ctx.fill()}scrub.value=index;document.getElementById('label').textContent=stages[index]+' | '+(index+1)+'/82';requestAnimationFrame(tick)}requestAnimationFrame(tick);
</script>'''
html=html.replace('PAYLOAD',json.dumps(payload)).replace('SEQUENCES',json.dumps(sequences)).replace('ANCHORS',json.dumps({n:manifest['clips'][n][0]['anchor_400px'] for n in names})).replace('STAGES',json.dumps(labels))
(OUT/'review.html').write_text(html,encoding='utf-8')
unique=set(hashlib.sha256((OUT/(key+'.png')).read_bytes()).digest() for key in frames)
disk=sum((OUT/(key+'.png')).stat().st_size for key in frames)
report={'status':'DRAFT_CHECKS_PASS_NOT_VISUAL_ACCEPTANCE','rendered_frames':len(frames),'byte_unique_pngs':len(unique),
        'draft_disk_mib':disk/2**20,'raw_pixel_mib_at_240':len(frames)*240*240*4/2**20,
        'same_frame_count_raw_pixel_mib_at_400':len(frames)*400*400*4/2**20,
        'naive_all_entry_expansion':{'idle_buckets':24,'wave_frames':45,'intermediate_frames_per_entry':8,
            'shared_held':1,'settle_intermediates':10,'added_unique_frames':563,'added_raw_pixel_mib_400':563*400*400*4/2**20,
            'decision':'Do not adopt this expansion; entry policy and compression/reuse need a bounded design before production.'},
        'max_anchor_drift_400px_by_source':grip_drift,'alpha_border_check':'all 240px draft frames PASS',
        'production_budget':'Not authorized. Counts cover six sampled pickups plus settle, not every runtime interruption.',
        'limits':'No process-memory delta, full-resolution alpha proof, runtime interruption tests or arbitrary-point grip guarantee.'}
(ROOT/'context/evidence/phase-04-preview-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
