"""Render the accepted open-eye bank at the same quality as the installed idle."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from prepare_stage import preservation_digests
from verify_companion_motion import action_data

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

source=ROOT/'.local/phase-04/directional-v1'
out=ROOT/'.local/phase-04/carry-final'
out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((source/'bank-manifest.json').read_text())
original_hash=sha(source/'drag-bank.blend')
bpy.ops.wm.open_mainfile(filepath=str(source/'drag-bank.blend'),load_ui=False,use_scripts=False)
scene=bpy.context.scene
rig,mesh=bpy.data.objects['Stitch_Armature'],bpy.data.objects['Stitch_Mesh']
baseline=preservation_digests(mesh,rig)
action=action_data(rig.animation_data.action)
camera=[list(row) for row in scene.camera.matrix_world]
scene.render.resolution_x=scene.render.resolution_y=400
scene.cycles.samples=24
scene.render.use_persistent_data=True
scene.frame_set(23)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'drag-bank.blend'),compress=True)
for name,record in manifest['frames'].items():
    scene.frame_set(record['frame'])
    # Same neutral geometry was verified in phase-04-directional-pose-checks.
    # Reuse the accepted endpoint bytes to remove sampling differences at handoff.
    if name=='bank_4_2.png':
        shutil.copy2(ROOT/'.local/phase-03/appearance-final/idle/idle_0001.png',out/name)
    else:
        scene.render.filepath=str(out/name)
        bpy.ops.render.render(write_still=True)
    record['anchor']=[v*400/240 for v in record['anchor']]
    record['sha256']=sha(out/name)
manifest.update(size=400,samples=24,neutral_anchor=[v*400/240 for v in manifest['neutral_anchor']],
    accepted_bank_sha256=original_hash,neutral_reused_from='phase-03/appearance-final/idle/idle_0001.png',
    limits='Accepted action/camera unchanged; 400px carry candidate requires moving user review.')
assert preservation_digests(mesh,rig)==baseline
assert action_data(rig.animation_data.action)==action
assert [list(row) for row in scene.camera.matrix_world]==camera
assert sha(source/'drag-bank.blend')==original_hash
manifest['preservation']='PASS: accepted action, mesh/rig fields, camera and source bytes'
(out/'bank-manifest.json').write_text(json.dumps(manifest,indent=2))
print('CARRY_FINAL_DONE',flush=True)
