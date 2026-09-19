"""Stage only verified open-eye assets in the isolated Phase 04 trial directory."""
import hashlib
import json
from pathlib import Path
import shutil
from preview_directional_drag import pointer, trace

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'.local/phase-04/native-trial'
BASE = ROOT/'.local/phase-03/appearance-final'
BANK = ROOT/'.local/phase-04/directional-v1'


def copy_verified(source, target, digest):
    assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, source
    if target.exists():
        assert hashlib.sha256(target.read_bytes()).hexdigest() == digest, target
    else:
        shutil.copy2(source, target)


def main():
    assets = OUT/'assets'
    carry = OUT/'carry'
    assets.mkdir(parents=True, exist_ok=True)
    carry.mkdir(parents=True, exist_ok=True)
    count = 0
    for clip in ('idle', 'wave', 'entries'):
        manifest = json.loads((BASE/clip/'manifest.json').read_text(encoding='utf-8'))
        for name, digest in manifest['frame_sha256'].items():
            assert Path(name).name == name
            copy_verified(BASE/clip/name, assets/name, digest)
            count += 1
    shutil.copy2(assets/'idle_0001.png', assets/'idle.png')
    manifest = json.loads((BANK/'bank-manifest.json').read_text())
    assert manifest['size'] == 240 and len(manifest['frames']) == 45
    lines = []
    for y in range(5):
        for x in range(9):
            name = f'bank_{x}_{y}.png'
            record = manifest['frames'][name]
            copy_verified(BANK/name, carry/name, record['sha256'])
            lines.append(f"{name},{record['anchor'][0]/240:.12f},{record['anchor'][1]/240:.12f}")
    (carry/'anchors.csv').write_text('\n'.join(lines)+'\n')
    # Python reference output is independent of the C# controller and supplied
    # as CSV to the native checks (no JSON library dependency in the pet).
    rows = []
    for record in trace():
        rows.append(','.join(str(v) for v in (record['t'],*record['pointer'],record['angle'],record['x'],record['y'])))
    (OUT/'reference.csv').write_text('\n'.join(rows)+'\n')
    (OUT/'inputs.csv').write_text('\n'.join(','.join(str(v) for v in (i/120,*pointer(i/120))) for i in range(1021))+'\n')
    (OUT/'trial-assets.json').write_text(json.dumps({'baseline_frames':count,'carry_frames':45,
        'carry_source':'directional-v1 (open eyes)', 'bank_manifest_sha256':hashlib.sha256((BANK/'bank-manifest.json').read_bytes()).hexdigest(),
        'limits':'240px carry drafts, accepted 400px idle/wave. Isolated trial only.'},indent=2))
    print(f'Staged {count} accepted frames and 45 open-eye carry drafts at {OUT}')


if __name__ == '__main__':
    main()
