"""Build an idle-entry-peace-idle review using actual rendered assets."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'.local/peace-motion-preview'
BASE = ROOT/'.local/phase-03/appearance-final'
checks = json.loads((OUT/'checks.json').read_text())
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)
alpha_bounds = []
for filename, digest in checks['hashes'].items():
    path = OUT/filename
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    with Image.open(path) as frame:
        assert frame.size == (400,400) and frame.mode == 'RGBA'
        bounds = frame.getchannel('A').getbbox()
        assert bounds and min(bounds[:2]) > 0 and max(bounds[2:]) < 400, (filename,bounds)
        alpha_bounds.append(bounds)

# Show the existing idle phase and corresponding entry bucket, followed by the
# new clip and a full accepted idle cycle. Closing the GIF preserves that cycle.
paths = [BASE/'idle'/('idle_%04d.png'%i) for i in range(1,26)]
paths += [BASE/'entries'/('entry_06_%04d.png'%i) for i in range(1,5)]
paths += [OUT/('peace_%04d.png'%i) for i in range(1,61)]
paths += [BASE/'idle'/('idle_%04d.png'%i) for i in range(1,97)]
boards = []
for path in paths:
    board = Image.new('RGB',(640,350),'#eef0f2')
    draw = ImageDraw.Draw(board)
    draw.rectangle((320,0,640,350),fill='#19202b')
    draw.text((12,8),'320 px / light',font=font,fill='#20262e')
    draw.text((332,8),'320 px / dark',font=font,fill='#eef0f2')
    with Image.open(path) as source:
        sprite = source.convert('RGBA').resize((320,320),Image.Resampling.LANCZOS)
        board.paste(sprite,(0,28),sprite)
        board.paste(sprite,(320,28),sprite)
    boards.append(board)
durations = [(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(boards))]
boards[0].save(OUT/'peace-motion-review.gif',save_all=True,append_images=boards[1:],
               duration=durations,loop=0,optimize=False,disposal=2)
selected = [1,6,11,16,21,30,38,43,48,53,57,60]
strip = Image.new('RGB',(960,810),'#eef0f2')
draw = ImageDraw.Draw(strip)
for index,frame in enumerate(selected):
    x,y = (index%4)*240,(index//4)*270
    draw.text((x+8,y+5),'Frame %02d'%frame,font=font,fill='#20262e')
    with Image.open(OUT/('peace_%04d.png'%frame)) as source:
        sprite=source.resize((240,240),Image.Resampling.LANCZOS)
        strip.paste(sprite,(x,y+28),sprite)
strip.save(OUT/'motion-contact-sheet.png')
first=Image.open(OUT/'peace_0001.png').convert('RGBA')
last=Image.open(OUT/'peace_0060.png').convert('RGBA')
difference=ImageChops.difference(first,last)
report={'clip_frames':60,'clip_seconds':2.5,'review_frames':len(paths),
        'review_milliseconds':sum(durations),'all_frame_hashes_match':True,
        'all_alpha_bounds_inside_canvas':True,'endpoint_pixel_max_difference':max(v[1] for v in difference.getextrema()),
        'resize':'Pillow Lanczos; not native GDI+','user_motion_acceptance':'pending'}
(OUT/'review-checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
