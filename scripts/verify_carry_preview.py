"""Reopen 04A scenes and verify evaluated transition endpoints, not just keys."""
import json
import sys
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_companion_motion import matrices, delta, action_data
from prepare_stage import preservation_digests

OUT=ROOT/'.local/phase-04/04a'
report={'status':'PASS', 'endpoints':{}, 'limits':'Evaluated pose endpoints, source fields and camera only; not full deformation or host input acceptance.'}
expected={}
for clip,frames in [('idle',[1,25,73]),('wave',[4,18,37])]:
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'.local/phase-03/appearance-final/{clip}/{clip}.blend'),load_ui=False,use_scripts=False)
    rig=bpy.data.objects['Stitch_Armature']
    for frame in frames:
        bpy.context.scene.frame_set(frame)
        expected[f'{clip}-{frame:02d}']=matrices(rig)
baseline=preservation_digests(bpy.data.objects['Stitch_Mesh'],rig)
original=action_data(bpy.data.actions['Stitch_Anim'])
camera=[list(row) for row in bpy.context.scene.camera.matrix_world]
bpy.ops.wm.open_mainfile(filepath=str(OUT/'held.blend'),load_ui=False,use_scripts=False)
held=matrices(bpy.data.objects['Stitch_Armature'])
for name in list(expected)+['settle']:
    bpy.ops.wm.open_mainfile(filepath=str(OUT/(name+'.blend')),load_ui=False,use_scripts=False)
    scene=bpy.context.scene
    rig=bpy.data.objects['Stitch_Armature']
    assert preservation_digests(bpy.data.objects['Stitch_Mesh'],rig)==baseline
    assert action_data(bpy.data.actions['Stitch_Anim'])==original
    assert camera==[list(row) for row in scene.camera.matrix_world]
    scene.frame_set(1)
    start=delta(matrices(rig),held if name=='settle' else expected[name])
    scene.frame_set(scene.frame_end)
    end=delta(matrices(rig),expected['idle-01'] if name=='settle' else held)
    assert max(start,end)<1e-5,(name,start,end)
    report['endpoints'][name]={'start_max_matrix_error':start,'end_max_matrix_error':end,'frames':scene.frame_end}
(ROOT/'context/evidence/phase-04-pose-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('CARRY_ENDPOINT_CHECKS_PASS',flush=True)
