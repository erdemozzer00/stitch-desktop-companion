"""Author an isolated raise/hold/return preview from the approved peace pose."""
import hashlib
import json
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.local/peace-motion-preview'
IDLE = ROOT / '.local/phase-03/appearance-final/idle/idle.blend'
POSE = ROOT / '.local/peace-preview/peace-pose-v1.blend'
FPS, COUNT = 24, 60

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def basis(rig):
    return {b.name: b.matrix_basis.copy() for b in rig.pose.bones}

def error(a, b):
    return max(abs(a[n][i][j]-b[n][i][j]) for n in a for i in range(4) for j in range(4))

def smooth(value):
    u = max(0., min(1., value))
    return u*u*(3.-2.*u)

def envelope(frame, rise, fall):
    return smooth((frame-rise[0])/(rise[1]-rise[0])) * (1.-smooth((frame-fall[0])/(fall[1]-fall[0])))

OUT.mkdir(parents=True, exist_ok=True)
source_hashes = {str(p): digest(p) for p in (IDLE, POSE)}
bpy.ops.wm.open_mainfile(filepath=str(POSE), load_ui=False, use_scripts=False)
target = basis(bpy.data.objects['Stitch_Armature'])
bpy.ops.wm.open_mainfile(filepath=str(IDLE), load_ui=False, use_scripts=False)
scene = bpy.context.scene
rig = bpy.data.objects['Stitch_Armature']
scene.frame_set(1)
neutral = basis(rig)
neutral_world = {b.name: b.matrix.copy() for b in rig.pose.bones}
changed = [n for n in target if error({n: target[n]}, {n: neutral[n]}) > 1e-6]
assert all(n.endswith('.R') for n in changed)
idle_samples = []
for frame in range(1, COUNT+1):
    scene.frame_set(frame)
    idle_samples.append(basis(rig))
action = bpy.data.actions.new('Peace_Preview_v1')
rig.animation_data.action = action
for frame in range(1, COUNT+1):
    scene.frame_set(frame)
    # Reuse accepted idle movement during the held pose; settle exactly to its
    # phase-zero endpoint so existing entry assets and idle restart remain valid.
    settle = smooth((frame-44)/16.)
    for bone in rig.pose.bones:
        bone.matrix_basis = idle_samples[frame-1][bone.name].lerp(neutral[bone.name], settle)
    for name in changed:
        if name.startswith(('Finger', 'Thumb')):
            amount = envelope(frame, (7,20), (38,54))
        elif name.startswith('Wrist'):
            amount = envelope(frame, (4,18), (39,59))
        elif name.startswith('ForeArm'):
            amount = envelope(frame, (2,16), (38,59))
        else:
            amount = envelope(frame, (1,14), (38,60))
        rig.pose.bones[name].matrix_basis = neutral[name].lerp(target[name], amount)
    for bone in rig.pose.bones:
        for prop in ('location', 'rotation_quaternion', 'scale'):
            bone.keyframe_insert(data_path=prop, frame=frame, group=bone.name)
for layer in action.layers:
    for strip in layer.strips:
        for bag in strip.channelbags:
            for curve in bag.fcurves:
                for key in curve.keyframe_points:
                    key.interpolation = 'LINEAR'
scene.frame_start, scene.frame_end, scene.render.fps = 1, COUNT, FPS
scene.render.resolution_x = scene.render.resolution_y = 400
scene.render.resolution_percentage = 100
scene.cycles.samples = 16
scene.render.use_persistent_data = True
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'peace-motion-v1.blend'), compress=True)
# Verify the saved file, not merely the authoring loop's last in-memory state.
bpy.ops.wm.open_mainfile(filepath=str(OUT/'peace-motion-v1.blend'), load_ui=False, use_scripts=False)
scene = bpy.context.scene
rig = bpy.data.objects['Stitch_Armature']
checks = {'frames': COUNT, 'fps': FPS, 'source_hashes': source_hashes, 'preview_only': True}
for frame in (1, COUNT):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    gap = error({b.name:b.matrix.copy() for b in rig.pose.bones}, neutral_world)
    assert gap < 1e-5, ('endpoint', frame, gap)
    checks['endpoint_'+str(frame)+'_matrix_error'] = gap
toe_names = [n for n in neutral_world if n.startswith('Toe_')]
max_foot = 0.
for frame in range(1, COUNT+1):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    max_foot = max(max_foot, error({n:rig.pose.bones[n].matrix.copy() for n in toe_names}, {n:neutral_world[n] for n in toe_names}))
assert max_foot < 1e-5
checks['max_toe_matrix_error'] = max_foot
checks['hashes'] = {}
for frame in range(1, COUNT+1):
    scene.frame_set(frame)
    path = OUT/('peace_%04d.png' % frame)
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    checks['hashes'][path.name] = digest(path)
assert all(digest(Path(p)) == value for p,value in source_hashes.items())
(OUT/'checks.json').write_text(json.dumps(checks, indent=2))
print('PEACE_PREVIEW_COMPLETE endpoints and feet verified; source files unchanged.')
