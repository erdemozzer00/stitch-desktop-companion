"""Short pose-space bridges from sampled idle phases to the reviewed wave neutral."""
import hashlib
import json
from pathlib import Path

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.local/phase-03/entries'
OUTPUT.mkdir(parents=True, exist_ok=True)
(OUTPUT / 'manifest.json').unlink(missing_ok=True)
source = ROOT / '.local/phase-03/idle/idle.blend'
bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
scene = bpy.context.scene
rig = bpy.data.objects['Stitch_Armature']
mesh = bpy.data.objects['Stitch_Mesh']
idle_action = rig.animation_data.action

def pose():
    return {b.name: (b.location.copy(), b.rotation_quaternion.copy(), b.scale.copy()) for b in rig.pose.bones}

def projected_vertices():
    bpy.context.view_layer.update()
    evaluated = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    data = evaluated.to_mesh()
    try:
        coords = np.empty(len(data.vertices) * 3, dtype=np.float32)
        data.vertices.foreach_get('co', coords)
        transform = np.array(scene.camera.matrix_world.inverted() @ mesh.matrix_world)
        camera = coords.reshape(-1, 3) @ transform[:3, :3].T + transform[:3, 3]
        return camera[:, :2] * 400 / scene.camera.data.ortho_scale
    finally:
        evaluated.to_mesh_clear()

poses, projections = [], []
for index in range(96):
    scene.frame_set(index + 1)
    poses.append(pose())
    projections.append(projected_vertices())
# Match the integer mapping used in the native player, including wrap to phase zero.
max_gap = max(float(np.linalg.norm(projections[i] - projections[((i + 3) // 6 * 6) % 96], axis=1).max()) for i in range(96))
assert max_gap < 1.0, ('Idle entry approximation exceeds one pixel at 400px', max_gap)
print('MAX_ENTRY_GAP_400PX', max_gap, flush=True)
neutral = poses[0]
scene.render.resolution_x = scene.render.resolution_y = 320
scene.cycles.samples = 6
files = {}
for bucket in range(16):
    rig.animation_data.action = bpy.data.actions.new('Companion_Entry_%02d' % bucket)
    for frame in range(1, 5):
        t = (frame - 1) / 3
        t = t * t * (3 - 2 * t)
        for bone in rig.pose.bones:
            start, end = poses[bucket * 6][bone.name], neutral[bone.name]
            bone.location = start[0].lerp(end[0], t)
            bone.rotation_quaternion = start[1].slerp(end[1], t)
            bone.scale = start[2].lerp(end[2], t)
            for prop in ('location', 'rotation_quaternion', 'scale'):
                bone.keyframe_insert(data_path=prop, frame=frame, group=bone.name)
    scene.frame_start, scene.frame_end = 1, 4
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT / ('entry_%02d.blend' % bucket)), compress=True)
    scene.render.filepath = str(OUTPUT / ('entry_%02d_' % bucket))
    bpy.ops.render.render(animation=True)
    for frame in range(1, 5):
        name = 'entry_%02d_%04d.png' % (bucket, frame)
        files[name] = hashlib.sha256((OUTPUT / name).read_bytes()).hexdigest()
manifest = {'buckets': 16, 'frames_per_entry': 4, 'fps': 24,
            'idle_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'max_entry_vertex_gap_at_400px': max_gap, 'frame_sha256': files,
            'limits': 'Subpixel pose approximation, not pixel equality or perceptual acceptance.'}
(OUTPUT / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
