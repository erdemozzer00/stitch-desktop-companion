"""Review the same final RGBA frames at all supported desktop sizes and backgrounds."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / '.local/phase-03'
for clip in ('idle', 'wave'):
    board = Image.new('RGB', (1000, 540), '#eef0f2')
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 280, 1000, 540), fill='#19202b')
    for column, variant in enumerate(('baseline', 'soft', 'lifted', 'outline')):
        with Image.open(ROOT / 'appearance' / ('%s-%s-24s.png' % (clip, variant))) as source:
            sprite = source.resize((240, 240), Image.Resampling.LANCZOS)
            for y in (32, 292):
                board.paste(sprite, (column * 250 + 5, y), sprite)
        draw.text((column * 250 + 10, 10), variant.upper(), fill='#20262e')
    board.save(ROOT / 'appearance' / (clip + '-appearance-comparison.png'))

final = ROOT / 'appearance-final'
boards = []
for clip in ('idle', 'wave'):
    manifest = json.loads((final / clip / 'manifest.json').read_text(encoding='utf-8'))
    for name, digest in manifest['frame_sha256'].items():
        path = final / clip / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        board = Image.new('RGB', (1000, 864), '#eef0f2')
        draw = ImageDraw.Draw(board)
        draw.rectangle((0, 440, 1000, 864), fill='#19202b')
        with Image.open(path) as source:
            for x, size in ((0, 240), (260, 320), (600, 400)):
                sprite = source.resize((size, size), Image.Resampling.LANCZOS)
                draw.text((x + 10, 10), '%s | %dpx' % (clip.upper(), size), fill='#20262e')
                for baseline in (430, 854):
                    board.paste(sprite, (x, baseline - size), sprite)
        boards.append(board)
durations = [(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(boards))]
boards[0].save(final / 'supported-sizes-review.gif', save_all=True, append_images=boards[1:], duration=durations, loop=0, optimize=False)
boards[0].save(final / 'supported-sizes-neutral.png')
boards[115].save(final / 'supported-sizes-wave.png')
print('Created actual 240/320/400px review on light and dark backgrounds.')
