"""Static peace-pose checkpoint; writes only private preview assets, never deploys."""
import bpy, math, json, hashlib
from pathlib import Path
from mathutils import Matrix, Quaternion, Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.local/peace-preview'
SRC=ROOT/'.local/phase-03/appearance-final'
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SRC/'idle/idle.blend',SRC/'wave/wave.blend']}
bpy.ops.wm.open_mainfile(filepath=str(SRC/'wave/wave.blend'),load_ui=False,use_scripts=False)
bpy.context.scene.frame_set(20)
rig=bpy.data.objects['Stitch_Armature']
mirror=Matrix.Diagonal((-1,1,1,1))
target={}
for stem in ['Shoulder','Arm','ForeArm','Wrist']:
    left=rig.pose.bones[stem+'.L']
    right=rig.pose.bones[stem+'.R']
    target[stem+'.R']=mirror@left.matrix@left.bone.matrix_local.inverted()@mirror@right.bone.matrix_local
OUT.mkdir(parents=True,exist_ok=True)
reports=[]
for name,roll,fold,thumb in [('peace-pose-v1',15,90,120)]:
    bpy.ops.wm.open_mainfile(filepath=str(SRC/'idle/idle.blend'),load_ui=False,use_scripts=False)
    scene=bpy.context.scene
    scene.frame_set(1)
    rig=bpy.data.objects['Stitch_Armature']
    basis={b.name:b.matrix_basis.copy() for b in rig.pose.bones}
    rig.animation_data.action=None
    for b in rig.pose.bones: b.matrix_basis=basis[b.name]
    bpy.context.view_layer.update()
    for n,m in target.items():
        rig.pose.bones[n].matrix=m
        bpy.context.view_layer.update()
    wrist=rig.pose.bones['Wrist.R']
    axis=rig.matrix_world.to_3x3().inverted()@(scene.camera.matrix_world.to_quaternion()@Vector((0,0,-1)))
    p=wrist.head.copy()
    wrist.matrix=Matrix.Translation(p)@Quaternion(axis,math.radians(roll)).to_matrix().to_4x4()@Matrix.Translation(-p)@wrist.matrix
    def local(n,axis,angle):
        rig.pose.bones[n].rotation_quaternion @= Quaternion(axis,math.radians(angle))
    # Three-finger hand: fold A, extend B/C; preserve the model's digit count.
    for digit in 'BC':
        local('Finger_'+digit+'.R',(1,0,0),-9)
        local('FingerTip_'+digit+'.R',(1,0,0),-6)
    local('Finger_A.R',(1,0,0),fold)
    local('FingerTip_A.R',(1,0,0),90)
    local('Thumb_A.R',(1,0,0),thumb)
    local('Thumb_B.R',(1,0,0),70)
    bpy.context.view_layer.update()
    scene.render.resolution_x=scene.render.resolution_y=400
    scene.render.resolution_percentage=100
    scene.cycles.samples=24
    scene.render.filepath=str(OUT/(name+'.png'))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(name+'.blend')),compress=True)
    bpy.ops.render.render(write_still=True)
    changed=[b.name for b in rig.pose.bones if max(abs(b.matrix_basis[i][j]-basis[b.name][i][j]) for i in range(4) for j in range(4))>1e-6]
    assert all(n.endswith('.R') for n in changed), changed
    reports.append({'name':name,'roll':roll,'fold':fold,'thumb':thumb,'changed_basis_bones':changed,'png_sha256':hashlib.sha256((OUT/(name+'.png')).read_bytes()).hexdigest()})
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
(OUT/'manifest.json').write_text(json.dumps({'source_hashes':hashes,'variants':reports,'scope':'static pose only; not deployed'},indent=2))
