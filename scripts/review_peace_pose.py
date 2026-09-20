"""Composite actual Blender pixels at supported sizes; no generated imagery."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1] / '.local/peace-preview'
source = Image.open(ROOT / 'peace-pose-v1.png').convert('RGBA')
assert source.size == (400, 400)
bounds = source.getchannel('A').getbbox()
assert bounds and min(bounds[:2]) > 0 and max(bounds[2:]) < 400, bounds
board = Image.new('RGB', (1000, 864), '#eef0f2')
draw = ImageDraw.Draw(board)
draw.rectangle((0, 440, 1000, 864), fill='#19202b')
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
for x, size in ((0, 240), (260, 320), (600, 400)):
    sprite = source.resize((size, size), Image.Resampling.LANCZOS)
    draw.text((x+10, 12), str(size)+' px', font=font, fill='#20262e')
    for baseline in (430, 854):
        board.paste(sprite, (x, baseline-size), sprite)
board.save(ROOT / 'supported-sizes-peace.png')
# Inspect the folded fingers at enlarged pixel scale, without synthesizing detail.
detail = Image.new('RGB', (400, 400), '#eef0f2')
crop = source.crop((65, 158, 145, 238)).resize((400, 400), Image.Resampling.NEAREST)
detail.paste(crop, (0, 0), crop)
detail.save(ROOT / 'hand-detail.png')
(ROOT / 'review-checks.json').write_text(json.dumps({
    'alpha_bounds_400': bounds, 'canvas_clipping': False,
    'sizes': [240, 320, 400], 'backgrounds': ['light', 'dark'],
    'resize': 'Pillow Lanczos; not a native GDI+ runtime capture',
    'scope': 'static silhouette review, not animation/intersection certification'
}, indent=2))
print('Static size sheet and alpha-bound checks complete.')
