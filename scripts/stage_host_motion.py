"""Validate current review frames and prepare a complete native-host asset directory."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
phase = ROOT / '.local/phase-03'
destination = Path(sys.argv[1]).resolve()
assert destination.is_relative_to(phase.resolve()), 'Stage inside the private Phase 03 directory'
assert not destination.exists(), 'Use a new staging directory; do not mix revisions'
sources = {}
for clip, count in [('idle', 96), ('wave', 45), ('entries', 96)]:
    folder = phase / clip
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    hashes = manifest['frame_sha256']
    assert len(hashes) == count and manifest['fps'] == 24
    for name, digest in hashes.items():
        assert Path(name).name == name
        path = folder / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        with Image.open(path) as image:
            assert image.mode == 'RGBA' and image.size == (320, 320)
            alpha = np.asarray(image)[:, :, 3]
            assert not any(edge.any() for edge in (alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]))
        sources[name] = path
    if clip == 'entries':
        assert manifest['buckets'] == 24 and manifest['frames_per_entry'] == 4
        assert manifest['idle_sha256'] == hashlib.sha256((phase / 'idle/idle.blend').read_bytes()).hexdigest()
        assert manifest['max_entry_vertex_gap_at_400px'] < 1
        gap = manifest['max_entry_vertex_gap_at_400px']
with Image.open(sources['wave_0001.png']) as image:
    neutral = np.asarray(image).copy()
for name in ['idle_0001.png', 'wave_0045.png'] + ['entry_%02d_0004.png' % i for i in range(24)]:
    with Image.open(sources[name]) as image:
        assert np.array_equal(neutral, np.asarray(image)), ('Neutral mismatch', name)
for bucket in range(24):
    with Image.open(sources['entry_%02d_0001.png' % bucket]) as entry, Image.open(sources['idle_%04d.png' % (bucket * 4 + 1)]) as idle:
        assert np.array_equal(np.asarray(entry), np.asarray(idle)), ('Entry bucket mismatch', bucket)
destination.mkdir(parents=True)
for name, source in sources.items():
    shutil.copy2(source, destination / name)
shutil.copy2(sources['idle_0001.png'], destination / 'idle.png')
report = {'status': 'PASS', 'revision': 'phase03-idle-polish', 'frames': len(sources),
          'max_entry_vertex_gap_at_400px': gap, 'all_entry_endpoints_pixel_identical_to_wave': True,
          'all_entry_starts_pixel_identical_to_sampled_idle': True, 'alpha_borders_clear': True,
          'limits': '320px drafts; 400px display is currently scaled. Native input/visual transition acceptance pending.',
          'frame_sha256': {name: hashlib.sha256((destination / name).read_bytes()).hexdigest() for name in sources}}
(destination.parent / 'motion-manifest.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
summary = {key: value for key, value in report.items() if key != 'frame_sha256'}
(ROOT / 'context/evidence/phase-03-runtime-frames.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary))
