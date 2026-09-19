"""Reopen the bounded bank and check accepted neutral, source fields and anchors."""
import hashlib
import json
from pathlib import Path
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from verify_companion_motion import matrices,delta,action_data
from prepare_stage import preservation_digests

out=ROOT/'.local/phase-04/directional-v1'
manifest=json.loads((out/'bank-manifest.json').read_text())
source=ROOT/'.local/phase-03/appearance-final/idle/idle.blend'
assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
bpy.context.scene.frame_set(1)
rig=bpy.data.objects['Stitch_Armature']
neutral=matrices(rig)
preserve=preservation_digests(bpy.data.objects['Stitch_Mesh'],rig)
original=action_data(bpy.data.actions['Stitch_Anim'])
camera=[list(row) for row in bpy.context.scene.camera.matrix_world]
bpy.ops.wm.open_mainfile(filepath=str(out/'drag-bank.blend'),load_ui=False,use_scripts=False)
scene=bpy.context.scene
rig,mesh=bpy.data.objects['Stitch_Armature'],bpy.data.objects['Stitch_Mesh']
assert preserve==preservation_digests(mesh,rig)
assert original==action_data(bpy.data.actions['Stitch_Anim'])
assert camera==[list(row) for row in scene.camera.matrix_world]
scene.frame_set(23)
neutral_error=delta(neutral,matrices(rig))
assert neutral_error<1e-5
error=0
for name,entry in manifest['frames'].items():
    scene.frame_set(entry['frame'])
    bpy.context.view_layer.update()
    obj=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    data=obj.to_mesh()
    try:
        p=world_to_camera_view(scene,scene.camera,mesh.matrix_world@data.vertices[manifest['anchor_vertex']].co)
        error=max(error,abs(p.x*240-entry['anchor'][0]),abs((1-p.y)*240-entry['anchor'][1]))
    finally:obj.to_mesh_clear()
    assert hashlib.sha256((out/name).read_bytes()).hexdigest()==entry['sha256']
assert error<.001
report={'status':'PASS','frames':45,'neutral_max_matrix_error':neutral_error,'max_anchor_reopen_error_px':error,
        'source_action_mesh_rig_camera':'PASS','limits':'Reopened pose/data and selected-anchor checks, not visual or native interaction acceptance.'}
(ROOT/'context/evidence/phase-04-directional-pose-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
