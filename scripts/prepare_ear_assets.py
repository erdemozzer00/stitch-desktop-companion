"""Render the approved ear clip and its rig-mirrored counterpart in isolation."""
import hashlib, json, shutil, sys
from pathlib import Path
import bpy
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from author_companion_motion import Character
OUT=ROOT/'.local/phase-08/assets'
OUT.mkdir(parents=True,exist_ok=True)
IDLE=ROOT/'.local/phase-03/appearance-final/idle/idle.blend'
APPROVED=ROOT/'.local/ear-motion-preview/ear-motion-v1.blend'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources={str(p):sha(p) for p in (IDLE,APPROVED)}
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
bpy.ops.wm.open_mainfile(filepath=str(IDLE),load_ui=False,use_scripts=False)
scene=bpy.context.scene;mesh=bpy.data.objects['Stitch_Mesh']
scene.frame_set(1);bpy.context.view_layer.update()
neutral_world={b.name:b.matrix.copy() for b in bpy.data.objects['Stitch_Armature'].pose.bones}
for mod in mesh.modifiers:
    if mod.type!='ARMATURE':mod.show_viewport=False
indices={}
for side in ('R','L'):
    groups={g.index for g in mesh.vertex_groups if g.name.startswith('Ear_') and g.name.endswith('.'+side)}
    indices[side]=[v.index for v in mesh.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>=.65]
    assert len(indices[side])>20
rows=[]
for f in range(1,97):
    scene.frame_set(f);bpy.context.view_layer.update()
    evaluated=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get());parts=[str(f-1)]
    for side in ('R','L'):
        points=[world_to_camera_view(scene,scene.camera,evaluated.matrix_world@evaluated.data.vertices[i].co) for i in indices[side]]
        polygon=hull([(round(p.x,8),round(1-p.y,8)) for p in points])
        assert len(polygon)>=3 and all(0<x<1 and 0<y<1 for x,y in polygon)
        parts.append(';'.join('%.8f,%.8f'%p for p in polygon))
    rows.append('|'.join(parts))
(OUT/'ears.csv').write_text('\n'.join(rows)+'\n')
manifest={'frames_per_side':16,'samples':24,'size':400,'fps':24,'sources':sources,'hashes':{}}
for side,prefix in [('R','ear_left_'),('L','ear_right_')]:
    bpy.ops.wm.open_mainfile(filepath=str(APPROVED),load_ui=False,use_scripts=False)
    scene=bpy.context.scene;rig=bpy.data.objects['Stitch_Armature']
    # Mirror the approved local rotations through the rig sagittal plane,
    # relative to each side's accepted neutral, rather than flipping pixels.
    if side=='L':
        scene.frame_set(1);character=Character()
        neutral=character.base
        bpy.ops.wm.open_mainfile(filepath=str(APPROVED),load_ui=False,use_scripts=False)
        scene=bpy.context.scene;rig=bpy.data.objects['Stitch_Armature']
        samples=[]
        from mathutils import Matrix
        reflect=Matrix.Diagonal((-1.,1.,1.))
        for f in range(1,17):
            scene.frame_set(f)
            changes={}
            for name in ('Ear_A.R','Ear_B.R','Head'):
                base=neutral[name].to_quaternion()
                delta=base.inverted()@rig.pose.bones[name].rotation_quaternion
                world=character.world[name]
                rotation=world@delta@world.inverted()
                changes[name]=(reflect@rotation.to_matrix()@reflect).to_quaternion()
            samples.append(changes)
        rig.animation_data.action=bpy.data.actions.new('Ear_Right_Mirrored')
        for f,changes in enumerate(samples,1):
            scene.frame_set(f)
            for b in rig.pose.bones:b.matrix_basis=neutral[b.name]
            for source,rotation in changes.items():
                target=source.replace('.R','.L');world=character.world[target]
                rig.pose.bones[target].rotation_quaternion @= world.inverted()@rotation@world
            for b in rig.pose.bones:
                for prop in ('location','rotation_quaternion','scale'):b.keyframe_insert(data_path=prop,frame=f,group=b.name)
    scene.cycles.samples=24;scene.render.use_persistent_data=True
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(prefix+'motion.blend')),compress=True)
    # Validate saved animation before exact accepted neutral PNG substitution.
    bpy.ops.wm.open_mainfile(filepath=str(OUT/(prefix+'motion.blend')),load_ui=False,use_scripts=False)
    scene=bpy.context.scene;rig=bpy.data.objects['Stitch_Armature']
    for endpoint in (1,16):
        scene.frame_set(endpoint);bpy.context.view_layer.update()
        gap=max(abs(b.matrix[i][j]-neutral_world[b.name][i][j]) for b in rig.pose.bones for i in range(4) for j in range(4))
        assert gap<1e-5,(side,endpoint,gap)
    for f in range(1,17):
        path=OUT/(prefix+'%04d.png'%f)
        if f in (1,16):shutil.copy2(IDLE.parent/'idle_0001.png',path)
        else:
            scene.frame_set(f);scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        manifest['hashes'][path.name]=sha(path)
manifest['hashes']['ears.csv']=sha(OUT/'ears.csv')
assert all(sha(Path(p))==h for p,h in sources.items())
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('EAR_ASSETS_COMPLETE')
