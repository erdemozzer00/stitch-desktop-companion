"""Compare the prior and restrained revised idle at actual 240px display size."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / '.local/phase-03'
folders = [ROOT / 'idle-before-idle-polish', ROOT / 'idle']
manifests = [json.loads((folder / 'manifest.json').read_text(encoding='utf-8')) for folder in folders]
boards = []
for frame in range(1, 97):
    board = Image.new('RGB', (520, 540), '#eef0f2')
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 280, 520, 540), fill='#19202b')
    for column, folder in enumerate(folders):
        name = 'idle_%04d.png' % frame
        path = folder / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifests[column]['frame_sha256'][name]
        with Image.open(path) as source:
            sprite = source.resize((240, 240), Image.Resampling.LANCZOS)
            for y in (32, 292):
                board.paste(sprite, (10 + column * 260, y), sprite)
        draw.text((12 + column * 260, 10), ['PREVIOUS', 'REFINED - SAME TIMING'][column], fill='#20262e')
    boards.append(board)
durations = [(round((i+1)*100/24)-round(i*100/24))*10 for i in range(96)]
boards[0].save(ROOT / 'idle-polish-comparison.gif', save_all=True, append_images=boards[1:], duration=durations, loop=0, optimize=False)
boards[24].save(ROOT / 'idle-polish-comparison.png')
print('Created 4-second comparison at 240px on light/dark backgrounds.')
