"""Stage only verified open-eye assets in the isolated Phase 04 trial directory."""
import hashlib
import json
from pathlib import Path
import shutil
import argparse
from PIL import Image
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
    global OUT,BANK
    parser=argparse.ArgumentParser()
    parser.add_argument('--final',action='store_true')
    args=parser.parse_args()
    if args.final:
        OUT=ROOT/'.local/phase-04/polished-trial'
        BANK=ROOT/'.local/phase-04/carry-final'
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
    size=400 if args.final else 240
    assert manifest['size'] == size and len(manifest['frames']) == 45
    if args.final:
        assert manifest['samples']==24
        assert (BANK/'bank_4_2.png').read_bytes()==(assets/'idle_0001.png').read_bytes()
    lines = []
    for y in range(5):
        for x in range(9):
            name = f'bank_{x}_{y}.png'
            record = manifest['frames'][name]
            copy_verified(BANK/name, carry/name, record['sha256'])
            with Image.open(carry/name) as image:
                assert image.mode=='RGBA' and image.size==(size,size)
                bounds=image.getchannel('A').getbbox()
                assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<size and bounds[3]<size
            lines.append(f"{name},{record['anchor'][0]/size:.12f},{record['anchor'][1]/size:.12f}")
    (carry/'anchors.csv').write_text('\n'.join(lines)+'\n')
    # Python reference output is independent of the C# controller and supplied
    # as CSV to the native checks (no JSON library dependency in the pet).
    rows = []
    for record in trace():
        rows.append(','.join(str(v) for v in (record['t'],*record['pointer'],record['angle'],record['x'],record['y'])))
    (OUT/'reference.csv').write_text('\n'.join(rows)+'\n')
    (OUT/'inputs.csv').write_text('\n'.join(','.join(str(v) for v in (i/120,*pointer(i/120))) for i in range(1021))+'\n')
    (OUT/'trial-assets.json').write_text(json.dumps({'baseline_frames':count,'carry_frames':45,
        'carry_source':BANK.name+' (open eyes)', 'size':size,'bank_manifest_sha256':hashlib.sha256((BANK/'bank-manifest.json').read_bytes()).hexdigest(),
        'limits':'Local candidate; physical input and visual acceptance remain separate.'},indent=2))
    print(f'Staged {count} accepted frames and 45 open-eye carry frames ({size}px) at {OUT}')


if __name__ == '__main__':
    main()
