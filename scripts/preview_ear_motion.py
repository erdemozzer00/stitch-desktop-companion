"""Isolated viewer-left ear reaction probe; never deploys or edits source assets."""
import hashlib
import json
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from author_companion_motion import Character

OUT = ROOT / '.local/ear-motion-preview'
SOURCE = ROOT / '.local/phase-03/appearance-final/idle/idle.blend'
COUNT = 16


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sample(frame, keys):
    for (a, av), (b, bv) in zip(keys, keys[1:]):
        if a <= frame <= b:
            u = (frame-a)/(b-a)
            return av+(bv-av)*u*u*(3-2*u)
    raise ValueError(frame)


OUT.mkdir(parents=True, exist_ok=True)
source_hash = sha(SOURCE)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE), load_ui=False, use_scripts=False)
scene = bpy.context.scene
character = Character()
rig = character.rig
neutral = {b.name: b.matrix.copy() for b in rig.pose.bones}
action = bpy.data.actions.new('Ear_Reaction_Probe_v1')
rig.animation_data.action = action
for frame in range(1, COUNT+1):
    scene.frame_set(frame)
    character.reset()
    # Rig-space axes, transformed into each bone's accepted neutral basis.
    # Ear tip follows its base one frame later, then settles with a small overshoot.
    base = sample(frame, [(1,0),(4,-13),(8,4),(12,-1.5),(16,0)])
    tip = sample(frame, [(1,0),(2,0),(5,-9),(9,3),(13,-1),(16,0)])
    tilt = sample(frame, [(1,0),(5,-2),(10,.6),(16,0)])
    character.rotate('Ear_A.R', (0,1,0), base)
    character.rotate('Ear_A.R', (0,0,1), base*.35)
    character.rotate('Ear_B.R', (0,1,0), tip)
    character.rotate('Head', (0,1,0), tilt)
    for bone in rig.pose.bones:
        for prop in ('location','rotation_quaternion','scale'):
            bone.keyframe_insert(data_path=prop, frame=frame, group=bone.name)
for layer in action.layers:
    for strip in layer.strips:
        for bag in strip.channelbags:
            for curve in bag.fcurves:
                for key in curve.keyframe_points:
                    key.interpolation = 'LINEAR'
scene.frame_start, scene.frame_end, scene.render.fps = 1, COUNT, 24
scene.render.resolution_x = scene.render.resolution_y = 400
scene.render.resolution_percentage = 100
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True
scene.cycles.samples = 16
scene.render.use_persistent_data = True
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ear-motion-v1.blend'), compress=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'ear-motion-v1.blend'), load_ui=False, use_scripts=False)
scene = bpy.context.scene
rig = bpy.data.objects['Stitch_Armature']
checks = {'preview_only':True,'frames':COUNT,'fps':24,'samples':16,
          'source_sha256':source_hash,'side':'viewer-left / rig .R','hashes':{}}
for frame in (1,COUNT):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    gap = max(abs(b.matrix[i][j]-neutral[b.name][i][j])
              for b in rig.pose.bones for i in range(4) for j in range(4))
    assert gap < 1e-5, (frame,gap)
    checks['endpoint_'+str(frame)+'_error'] = gap
for frame in range(1,COUNT+1):
    scene.frame_set(frame)
    path = OUT/('ear_%04d.png'%frame)
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    checks['hashes'][path.name] = sha(path)
assert sha(SOURCE) == source_hash
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('EAR_PREVIEW_COMPLETE; saved-scene endpoints verified; source unchanged.')
