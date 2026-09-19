"""04A private pose/transition study. Never updates the installed companion."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from author_companion_motion import Character
from prepare_stage import preservation_digests
from verify_companion_motion import action_data


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pose(rig):
    return {b.name: (b.location.copy(), b.rotation_quaternion.copy(), b.scale.copy()) for b in rig.pose.bones}


def apply(rig, values):
    for bone in rig.pose.bones:
        bone.location, bone.rotation_quaternion, bone.scale = values[bone.name]
    bpy.context.view_layer.update()


def ease(t):
    t = max(0, min(1, t))
    return t*t*(3-2*t)


def mix(start, end, t):
    return {name: (a[0].lerp(end[name][0], t), a[1].slerp(end[name][1], t),
                   a[2].lerp(end[name][2], t)) for name, a in start.items()}


def transition(start, end, progress):
    # Small authored follow-through, finishing at the same held/neutral endpoint.
    result = {}
    for name in start:
        delay = .15 if name.startswith('Ear_') else .08 if name == 'Head' else 0
        t = ease((progress-delay)/(1-delay))
        result[name] = mix({name: start[name]}, {name: end[name]}, t)[name]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['poses', 'motion'], default='poses')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out = ROOT / '.local/phase-04/04a'
    out.mkdir(parents=True, exist_ok=True)
    sources = {clip: ROOT / f'.local/phase-03/appearance-final/{clip}/{clip}.blend' for clip in ('idle', 'wave')}
    hashes = {clip: digest(path) for clip, path in sources.items()}
    sampled = {}
    for clip, frames in [('wave', [4, 18, 37]), ('idle', [1, 25, 73])]:
        bpy.ops.wm.open_mainfile(filepath=str(sources[clip]), load_ui=False, use_scripts=False)
        for frame in frames:
            bpy.context.scene.frame_set(frame)
            sampled[f'{clip}-{frame:02d}'] = pose(bpy.data.objects['Stitch_Armature'])
    scene = bpy.context.scene
    rig, mesh = bpy.data.objects['Stitch_Armature'], bpy.data.objects['Stitch_Mesh']
    scene.frame_set(1)
    neutral = sampled['idle-01']
    baseline = preservation_digests(mesh, rig)
    original = action_data(bpy.data.actions['Stitch_Anim'])
    camera = [list(row) for row in scene.camera.matrix_world]
    character = Character()
    apply(rig, neutral)
    # Use the existing leg IK controls; do not rotate constrained shins directly.
    height = mesh.dimensions.z
    for side, sign in [('L', 1), ('R', -1)]:
        character.rotate('Arm.'+side, (0, 1, 0), sign * 4)
        character.rotate('ForeArm.'+side, (1, 0, 0), 7)
        character.rotate('Wrist.'+side, (0, 1, 0), -sign * 3)
        character.rotate('Ear_A.'+side, (0, 1, 0), -sign * 3)
        character.rotate('Ear_B.'+side, (0, 1, 0), -sign * 2)
        control = rig.pose.bones['CTRL_leg.'+side]
        # Armature-space delta converted to the control's rest-local translation.
        delta = Vector((-sign * .012 * height, .012 * height, .018 * height))
        control.location += control.bone.matrix_local.to_quaternion().inverted() @ delta
    character.rotate('Head', (1, 0, 0), 2)
    bpy.context.view_layer.update()
    held = pose(rig)
    scene.render.resolution_x = scene.render.resolution_y = 240
    scene.render.resolution_percentage = 100
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.render.use_persistent_data = True
    scene.cycles.samples = 6
    scene.render.fps = 24

    # Choose an actual front torso mesh vertex, not just a window or bone origin.
    apply(rig, neutral)
    def vertices():
        obj = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
        data = obj.to_mesh()
        try:
            return [mesh.matrix_world @ v.co for v in data.vertices]
        finally:
            obj.to_mesh_clear()
    def project(point):
        p = world_to_camera_view(scene, scene.camera, point)
        return Vector((p.x*400, (1-p.y)*400))
    coords = vertices()
    candidates = [(i, project(v), (scene.camera.matrix_world.inverted() @ v).z) for i,v in enumerate(coords)]
    center = Vector((200, 270))
    near = [item for item in candidates if (item[1]-center).length < 8]
    assert near, 'No front torso anchor near requested screen point'
    anchor = max(near, key=lambda item: item[2])[0]
    report = {'mode': args.mode, 'sources': hashes, 'size': 240, 'samples': 6, 'fps': 24,
              'anchor_vertex': anchor, 'anchor_neutral_400px': list(project(coords[anchor])),
              'clips': {}, 'limits': 'Draft visual study; no host integration, arbitrary-grip guarantee or visual acceptance.'}
    clips = {'neutral': [neutral], 'held': [held]} if args.mode == 'poses' else {
        name: [transition(start, held, i/9) for i in range(10)] for name,start in sampled.items()}
    if args.mode == 'motion':
        # Controlled return; no physics flight or added idle gesture.
        clips['settle'] = [transition(held, neutral, i/11) for i in range(12)]
    for name, frames in clips.items():
        action = bpy.data.actions.new('CarryStudy_'+name)
        rig.animation_data.action = action
        data = []
        for index, values in enumerate(frames, 1):
            scene.frame_set(index)
            apply(rig, values)
            for bone in rig.pose.bones:
                for prop in ('location', 'rotation_quaternion', 'scale'):
                    bone.keyframe_insert(data_path=prop, frame=index, group=bone.name)
            points = vertices()
            data.append({'frame': index, 'anchor_400px': list(project(points[anchor]))})
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for key in curve.keyframe_points:
                            key.interpolation = 'LINEAR'
        scene.frame_start, scene.frame_end = 1, len(frames)
        scene.frame_set(1)
        bpy.ops.wm.save_as_mainfile(filepath=str(out / (name+'.blend')), compress=True)
        for index in range(1, len(frames)+1):
            scene.frame_set(index)
            scene.render.filepath = str(out / f'{name}_{index:03d}.png')
            bpy.ops.render.render(write_still=True)
        report['clips'][name] = data
    assert preservation_digests(mesh, rig) == baseline
    assert action_data(bpy.data.actions['Stitch_Anim']) == original
    assert camera == [list(row) for row in scene.camera.matrix_world]
    assert hashes == {clip: digest(path) for clip,path in sources.items()}
    report['preserved'] = 'Source file hashes, original action, mesh/rig preservation fields and camera PASS'
    (out / (args.mode+'-manifest.json')).write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('CARRY_STUDY_DONE', args.mode, flush=True)


if __name__ == '__main__':
    main()
