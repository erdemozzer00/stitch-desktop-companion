"""Compose private smile review from real Blender renders and verify artifacts."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.local/phase-09/smile-preview-v4'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
report=json.loads((OUT/'motion-checks.json').read_text())
frames=[]
for name,digest in report['frames'].items():
    path=OUT/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
    with Image.open(path) as source:
        assert source.mode=='RGBA' and source.size==(400,400)
        frame=source.copy()
    bounds=frame.getchannel('A').getbbox()
    assert bounds and min(bounds[:2])>0 and max(bounds[2:])<400,(name,bounds)
    frames.append(frame)
assert len(frames)==28
endpoint_error=max(pair[1] for pair in ImageChops.difference(frames[0],frames[-1]).getextrema())
assert endpoint_error==0,endpoint_error
with Image.open(OUT/'neutral.png') as neutral:
    assert not ImageChops.difference(frames[0],neutral).getbbox(alpha_only=False)

# Neutral pauses help review; they are not part of the authored reaction.
sequence=[frames[0]]*12+frames+[frames[-1]]*20
boards=[]
for frame in sequence:
    board=Image.new('RGB',(720,440),'#edf0f3')
    draw=ImageDraw.Draw(board)
    draw.rectangle((400,0,720,440),fill='#19202b')
    draw.text((12,10),'Gülümseme önizlemesi · 400 px',font=font,fill='#20262e')
    draw.text((412,10),'240 px',font=font,fill='#eef0f2')
    board.paste(frame,(0,38),frame)
    small=frame.resize((240,240),Image.Resampling.LANCZOS)
    board.paste(small,(440,118),small)
    boards.append(board)
durations=[(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(boards))]
gif=OUT/'smile-motion-review.gif'
boards[0].save(gif,save_all=True,append_images=boards[1:],duration=durations,
               loop=0,optimize=False,disposal=2)
with Image.open(gif) as encoded:
    total=0
    for index in range(encoded.n_frames):
        encoded.seek(index);encoded.load();total+=encoded.info['duration']
    assert total==sum(durations)

sheet=Image.new('RGB',(1600,840),'#edf0f3')
draw=ImageDraw.Draw(sheet)
for index,number in enumerate([1,4,6,8,12,17,22,28]):
    x,y=(index%4)*400,(index//4)*420
    draw.text((x+10,y+4),'Frame '+str(number),font=font,fill='#20262e')
    sheet.paste(frames[number-1],(x,y+20),frames[number-1])
sheet.save(OUT/'smile-contact-sheet.png')

comparison=Image.new('RGB',(1000,460),'#edf0f3')
draw=ImageDraw.Draw(comparison)
for index,(size,x,y) in enumerate([(400,0,50),(320,400,90),(240,740,130)]):
    small=frames[11].resize((size,size),Image.Resampling.LANCZOS)
    comparison.paste(small,(x,y),small)
    draw.text((x+16,14),str(size)+' px',font=font,fill='#20262e')
comparison.save(OUT/'smile-size-review.png')

checks={'render_hashes_verified':True,'rgba_and_alpha_bounds':'PASS',
        'endpoint_pixel_error':endpoint_error,'matches_standalone_neutral':True,
        'authored_frames':28,'fps':24,'clip_seconds':28/24,
        'gif_fully_decoded':True,'gif_loop_ms':total,
        'limits':'Isolated rendered preview; no native input, idle-entry, carry or recipient validation.'}
(OUT/'review-checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks))
