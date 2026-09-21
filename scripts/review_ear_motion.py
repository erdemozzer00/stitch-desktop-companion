"""Compose and validate the isolated ear probe from Blender-rendered pixels."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'.local/ear-motion-preview'
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
checks = json.loads((OUT/'checks.json').read_text())
frames = []
for name, digest in checks['hashes'].items():
    path = OUT/name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    with Image.open(path) as im:
        assert im.mode == 'RGBA' and im.size == (400,400)
        bounds = im.getchannel('A').getbbox()
        assert bounds and min(bounds[:2])>0 and max(bounds[2:])<400, (name,bounds)
        frames.append(im.copy())
delta = ImageChops.difference(frames[0],frames[-1])
pixel_error = max(p[1] for p in delta.getextrema())
assert pixel_error == 0, pixel_error
# Neutral pauses isolate timing of the proposed reaction; this is not a native
# idle-to-reaction integration demonstration. Each loop contains one 16-frame clip.
sequence = [frames[0]]*12 + frames + [frames[-1]]*24
boards=[]
for frame in sequence:
    board = Image.new('RGB',(720,440),'#edf0f3')
    draw = ImageDraw.Draw(board)
    draw.rectangle((400,0,720,440),fill='#19202b')
    draw.text((12,10),'400 px / ear reaction preview',font=font,fill='#20262e')
    draw.text((412,10),'240 px',font=font,fill='#eef0f2')
    board.paste(frame,(0,38),frame)
    small=frame.resize((240,240),Image.Resampling.LANCZOS)
    board.paste(small,(440,118),small)
    boards.append(board)
durations=[(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(boards))]
gif=OUT/'ear-motion-review.gif'
boards[0].save(gif,save_all=True,append_images=boards[1:],duration=durations,
               loop=0,optimize=False,disposal=2)
with Image.open(gif) as encoded:
    total=0
    for i in range(encoded.n_frames):
        encoded.seek(i)
        encoded.load()
        total+=encoded.info['duration']
    assert total == sum(durations)
sheet=Image.new('RGB',(1200,840),'#edf0f3')
draw=ImageDraw.Draw(sheet)
for i,f in enumerate([1,4,5,8,12,16]):
    x,y=(i%3)*400,(i//3)*420
    draw.text((x+10,y+5),'Frame '+str(f),font=font,fill='#20262e')
    sheet.paste(frames[f-1],(x,y+20),frames[f-1])
sheet.save(OUT/'ear-contact-sheet.png')
report={'hashes_verified':True,'all_alpha_bounds_inside_canvas':True,
        'endpoint_pixel_error':pixel_error,'clip_seconds':16/24,
        'gif_decoded':True,'loop_ms':total,
        'limits':'Isolated animation preview with neutral pauses. No native input, idle-entry, carry or recipient validation.'}
(OUT/'review-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
