"""Export idle hand regions and render the approved clip without re-authoring."""
import bpy, hashlib, json, shutil
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'.local/phase-03/appearance-final'
OUT=ROOT/'.local/phase-07/assets'
OUT.mkdir(parents=True,exist_ok=True)
sources=[BASE/'idle/idle.blend',ROOT/'.local/peace-motion-preview/peace-motion-v1.blend']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
bpy.ops.wm.open_mainfile(filepath=str(sources[0]),load_ui=False,use_scripts=False)
scene=bpy.context.scene
mesh=bpy.data.objects['Stitch_Mesh']
# Control-mesh hand bounds after skinning; native alpha still gates actual hits.
for mod in mesh.modifiers:
    if mod.type!='ARMATURE': mod.show_viewport=False
indices={}
for side in ('L','R'):
    groups={g.index for g in mesh.vertex_groups if g.name.endswith('.'+side) and g.name.startswith(('Wrist','Knuckle','Finger','Thumb'))}
    indices[side]=[v.index for v in mesh.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>=.35]
    assert len(indices[side])>100
rows=[]
for frame in range(1,97):
    scene.frame_set(frame)
    evaluated=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    row=[str(frame-1)]
    for side in ('L','R'): # viewer-right wave first, viewer-left peace second
        points=[world_to_camera_view(scene,scene.camera,evaluated.matrix_world@evaluated.data.vertices[i].co) for i in indices[side]]
        bounds=(min(p.x for p in points)-.0075,1-max(p.y for p in points)-.0075,
                max(p.x for p in points)+.0075,1-min(p.y for p in points)+.0075)
        assert all(0<v<1 for v in bounds)
        row += ['%.8f'%v for v in bounds]
    rows.append(','.join(row))
(OUT/'hands.csv').write_text('\n'.join(rows)+'\n')
bpy.ops.wm.open_mainfile(filepath=str(sources[1]),load_ui=False,use_scripts=False)
scene=bpy.context.scene
scene.cycles.samples=24
scene.render.use_persistent_data=True
manifest={'frames':60,'size':400,'fps':24,'samples':24,'source_hashes':hashes,'frame_sha256':{}}
for frame in range(1,61):
    path=OUT/('peace_%04d.png'%frame)
    if frame in (1,60):
        shutil.copy2(BASE/'idle/idle_0001.png',path)
    else:
        scene.frame_set(frame)
        scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
    manifest['frame_sha256'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
manifest['hands_sha256']=hashlib.sha256((OUT/'hands.csv').read_bytes()).hexdigest()
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('PRODUCTION_PEACE_ASSETS_COMPLETE')
