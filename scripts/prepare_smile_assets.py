"""Render the approved smile scene and project the actual nose for each idle frame."""
import hashlib,json,shutil
from pathlib import Path
import bpy
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.local/phase-09/assets'
IDLE=ROOT/'.local/phase-03/appearance-final/idle/idle.blend'
APPROVED=ROOT/'.local/phase-09/smile-preview-v4/smile-motion.blend'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hull(points):
    points=sorted(set(points))
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower=[];upper=[]
    for p in points:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]
OUT.mkdir(parents=True,exist_ok=True)
sources={str(p):sha(p) for p in (IDLE,APPROVED)}
bpy.ops.wm.open_mainfile(filepath=str(IDLE),load_ui=False,use_scripts=False)
scene=bpy.context.scene;mesh=bpy.data.objects['Stitch_Mesh'];rig=bpy.data.objects['Stitch_Armature']
scene.frame_set(1);bpy.context.view_layer.update()
neutral={b.name:b.matrix.copy() for b in rig.pose.bones}
group=mesh.vertex_groups['Nose'].index
seed=max(mesh.data.vertices,key=lambda v:sum(g.weight for g in v.groups if g.group==group)).index
adjacency=[[] for _ in mesh.data.vertices]
for edge in mesh.data.edges:
    a,b=edge.vertices;adjacency[a].append(b);adjacency[b].append(a)
indices={seed};queue=[seed]
while queue:
    for neighbor in adjacency[queue.pop()]:
        if neighbor not in indices:indices.add(neighbor);queue.append(neighbor)
assert 100<len(indices)<1500, 'Expected isolated nose component.'
for mod in mesh.modifiers:
    if mod.type!='ARMATURE':mod.show_viewport=False
rows=[]
for f in range(1,97):
    scene.frame_set(f);bpy.context.view_layer.update()
    evaluated=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    points=[world_to_camera_view(scene,scene.camera,evaluated.matrix_world@evaluated.data.vertices[i].co) for i in indices]
    polygon=hull([(round(p.x,8),round(1-p.y,8)) for p in points])
    assert len(polygon)>=3 and all(.35<x<.65 and .2<y<.45 for x,y in polygon)
    rows.append(str(f-1)+'|'+';'.join('%.8f,%.8f'%p for p in polygon))
(OUT/'nose.csv').write_text('\n'.join(rows)+'\n')
bpy.ops.wm.open_mainfile(filepath=str(APPROVED),load_ui=False,use_scripts=False)
scene=bpy.context.scene;rig=bpy.data.objects['Stitch_Armature']
scene.cycles.samples=24;scene.render.use_persistent_data=True
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'smile-motion.blend'),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'smile-motion.blend'),load_ui=False,use_scripts=False)
scene=bpy.context.scene;rig=bpy.data.objects['Stitch_Armature']
manifest={'frames':28,'fps':24,'size':400,'samples':24,'nose_vertices':len(indices),'sources':sources,'hashes':{}}
for f in range(1,29):
    scene.frame_set(f);bpy.context.view_layer.update()
    path=OUT/('smile_%04d.png'%f)
    if f in (1,28):
        gap=max(abs(b.matrix[i][j]-neutral[b.name][i][j]) for b in rig.pose.bones for i in range(4) for j in range(4))
        assert gap<1e-5
        assert bpy.data.objects['Stitch_Mesh'].data.shape_keys.key_blocks['WarmSmile'].value==0
        assert all(o.hide_render for o in bpy.data.objects if o.name.startswith('SmileLid'))
        manifest['endpoint_'+str(f)+'_error']=gap
        shutil.copy2(IDLE.parent/'idle_0001.png',path)
    else:
        scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
    manifest['hashes'][path.name]=sha(path)
manifest['hashes']['nose.csv']=sha(OUT/'nose.csv')
assert all(sha(Path(p))==h for p,h in sources.items())
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('SMILE_ASSETS_COMPLETE')
