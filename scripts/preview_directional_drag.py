"""Pointer-linked review using a finite PNG bank and transforms, no live skeleton."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.local/phase-04/directional-v1'
FONT=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
SMALL=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',14)

# Exact constant-target critically damped update. This is a visual controller only.
def spring(value, velocity, target, omega, dt):
    offset=value-target
    j=velocity+omega*offset
    decay=math.exp(-omega*dt)
    return target+(offset+j*dt)*decay, (velocity-omega*j*dt)*decay


def clamp(value, low=-1., high=1.):
    return max(low,min(high,value))


ROUTE=[(0.,200.,270.),(.5,200.,270.),(1.7,335.,270.),(2.1,335.,270.),
       (2.8,155.,270.),(3.15,155.,270.),(3.75,240.,270.),(4.35,240.,210.),
       (4.95,240.,275.),(5.65,345.,230.),(6.65,200.,270.),(8.5,200.,270.)]


def pointer(t):
    for a,b in zip(ROUTE,ROUTE[1:]):
        if a[0]<=t<=b[0]:
            u=(t-a[0])/(b[0]-a[0])
            u=u*u*(3-2*u)
            return a[1]+(b[1]-a[1])*u,a[2]+(b[2]-a[2])*u
    return ROUTE[-1][1:]


def phase(t):
    for end,label in [(.5,'Tut'),(1.7,'Sağa — yavaş'),(2.1,'Dur'),(2.8,'Sola — hızlı'),
        (3.15,'Dur'),(3.75,'Yön değiştir'),(4.35,'Yukarı'),(4.95,'Aşağı'),(6.65,'Çapraz taşı'),
        (7.3,'Bırak / toparlan'),(8.6,'Bırakılan konum')]:
        if t<end:return label


def trace(rate=120):
    body=body_v=ear=ear_v=vertical=vertical_v=vx=vy=0.
    prev=pointer(0)
    records=[]
    for i in range(round(8.5*rate)+1):
        t=i/rate;dt=1/rate;p=pointer(t)
        rawx,rawy=(p[0]-prev[0])/dt/240,(p[1]-prev[1])/dt/240
        smoothing=1-math.exp(-dt/.045)
        vx+=(rawx-vx)*smoothing;vy+=(rawy-vy)*smoothing
        if t>=6.65:vx=vy=0
        goal=clamp(vx*.16,-.18,.18)
        if abs(vx)<.025:goal=0
        body,body_v=spring(body,body_v,goal,26.,dt)
        ear,ear_v=spring(ear,ear_v,body,16.,dt)
        y_goal=clamp(-vy*.9)
        if abs(vy)<.025:y_goal=0
        vertical,vertical_v=spring(vertical,vertical_v,y_goal,22.,dt)
        # Relative ear articulation lags global body swing; no 45 independent looping clips.
        x=clamp((ear-body)/.07+.2*body/.18)
        xi=int(math.floor((x+1)*4+.5));yi=int(math.floor((clamp(vertical)+1)*2+.5))
        if i%(rate//24)==0:
            records.append({'t':t,'pointer':list(p),'angle':body,'x':x,'y':vertical,
                            'file':f'bank_{xi}_{yi}.png','phase':phase(t),'held':t<6.65})
        prev=p
    return records


def projected(sprite,anchor,position,angle,size=(520,450)):
    c,s=math.cos(angle),math.sin(angle)
    px,py=position;ax,ay=anchor
    # Inverse affine mapping keeps this chosen anatomical anchor exactly at the pointer.
    return sprite.transform(size,Image.Transform.AFFINE,(c,s,ax-c*px-s*py,-s,c,ay+s*px-c*py),
                            resample=Image.Resampling.BICUBIC)


def cursor(draw,point,held):
    x,y=point
    draw.ellipse((x-4,y-4,x+4,y+4),outline='#ed9745',width=2)
    if not held:x,y=x+40,y+25
    draw.polygon([(x,y),(x+2,y+19),(x+7,y+14),(x+13,y+23),(x+17,y+21),(x+11,y+12),(x+19,y+11)],fill='white',outline='#1d2630',width=2)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--poses',action='store_true')
    args=parser.parse_args()
    manifest=json.loads((OUT/('poses-manifest.json' if args.poses else 'bank-manifest.json')).read_text())
    if args.poses:
        board=Image.new('RGB',(780,810),'#edf0f3');draw=ImageDraw.Draw(board)
        for row,yi in enumerate((0,2,4)):
            for col,xi in enumerate((0,4,8)):
                with Image.open(OUT/f'bank_{xi}_{yi}.png') as source:
                    board.paste(source,(col*260,row*270+25),source)
                draw.text((col*260+10,row*270+3),f'x={xi/4-1:+.1f} y={yi/2-1:+.1f}',fill='#202730',font=SMALL)
        board.save(OUT/'pose-extremes.png')
        return
    images={}
    for name,entry in manifest['frames'].items():
        assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==entry['sha256']
        with Image.open(OUT/name) as image:
            images[name]=image.convert('RGBA')
        alpha=images[name].getchannel('A')
        assert not any(alpha.crop(box).getbbox() for box in [(0,0,240,1),(0,239,240,240),(0,0,1,240),(239,0,240,240)]),name
    records=trace()
    OUT.joinpath('pointer-trace.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    anchors=manifest['frames'];neutral=images['bank_4_2.png'];neutral_anchor=anchors['bank_4_2.png']['anchor']
    max_frame_anchor=max(math.dist(entry['anchor'],neutral_anchor) for entry in anchors.values())
    # Same analytic route at a finer integration step: a numeric stability check, not a visual gate.
    finer=trace(240)
    dt_difference=max(abs(a['angle']-b['angle']) for a,b in zip(records,finer))
    assert dt_difference<.02,dt_difference
    assert abs(records[-1]['angle'])<.0001 and abs(records[-1]['y'])<.0001
    bounds=[]
    for theme,bg,ink in [('light','#eef0f2','#233140'),('dark','#19202b','#eef0f4')]:
        boards=[]
        for record in records:
            board=Image.new('RGB',(1040,510),bg)
            draw=ImageDraw.Draw(board)
            for column,label in [(0,'NORMAL TAŞIMA'),(1,'TAŞINAN OYUNCAK — TASLAK')]:
                draw.text((column*520+15,10),label,fill=ink,font=FONT)
                name=record['file'];sprite=neutral if column==0 else images[name]
                a=neutral_anchor if column==0 else anchors[name]['anchor']
                angle=0 if column==0 else record['angle']
                layer=projected(sprite,a,record['pointer'],angle)
                bounds.append(layer.getchannel('A').getbbox())
                board.paste(layer,(column*520,35),layer)
                cursor(draw,(column*520+record['pointer'][0],35+record['pointer'][1]),record['held'])
            draw.line((520,0,520,475),fill='#647180',width=1)
            draw.text((16,466),record['phase'],fill=ink,font=FONT)
            draw.text((16,490),'240px hareket taslağı • aynı fare yolu • el sallama / masaüstü uygulaması değişmedi',fill=ink,font=SMALL)
            boards.append(board)
        durations=[(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(boards))]
        # Pause at the settled endpoint; both routes already return to their starting vicinity.
        durations[-1]=900
        boards[0].save(OUT/f'directional-{theme}.gif',save_all=True,append_images=boards[1:],duration=durations,loop=0,optimize=False)
        board=Image.new('RGB',(1040*2,510*3),bg)
        for cell,i in enumerate((25,48,60,92,126,172)):
            board.paste(boards[i],((cell%2)*1040,(cell//2)*510))
        board.save(OUT/f'motion-sheet-{theme}.png')
    assert all(b and b[0]>0 and b[1]>0 and b[2]<520 and b[3]<450 for b in bounds)
    report={'status':'DRAFT_CHECKS_PASS_NOT_VISUAL_ACCEPTANCE','bank_frames':len(images),'size':240,'samples':6,
            'trace_seconds':8.5,'display_samples':len(records),'unique_frames_used':len({r['file'] for r in records}),
            'max_body_angle_degrees':max(abs(r['angle']) for r in records)*180/math.pi,
            'max_uncompensated_anchor_drift_at_240':max_frame_anchor,
            'grip_mapping':'Per-frame selected torso anchor mapped to pointer by inverse affine transform; arbitrary grips not proven.',
            '120_vs_240hz_max_body_angle_difference_degrees':dt_difference*180/math.pi,
            'final_body_angle_degrees':records[-1]['angle']*180/math.pi,
            'raw_bank_mib_at_240':len(images)*240*240*4/2**20,
            'same_bank_raw_mib_at_400':len(images)*400*400*4/2**20,
            'png_disk_mib':sum((OUT/n).stat().st_size for n in images)/2**20,
            'limits':'Only scripted pointer replay; no native mouse input, arbitrary entry/grip, full-resolution alpha or production acceptance.'}
    (ROOT/'context/evidence/phase-04-directional-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
