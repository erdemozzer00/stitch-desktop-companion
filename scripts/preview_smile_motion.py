"""Isolated nose-smile/soft-eye-closure preview; never changes installed assets."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from author_companion_motion import Character
from author_carry_eyes import create_lids
from prepare_stage import preservation_digests

SOURCE = ROOT / '.local/phase-03/appearance-final/idle/idle.blend'
EXPECTED_SOURCE = '9c5e27504da499b8659285e8a7f56264caa9baae0ab3a935dc3f3d6cd1cbde90'
OUT = ROOT / '.local/phase-09/smile-preview-v4'
COUNT = 28


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sample(frame, keys):
    for (a, av), (b, bv) in zip(keys, keys[1:]):
        if a <= frame <= b:
            u = (frame-a)/(b-a)
            return av+(bv-av)*u*u*(3-2*u)
    raise ValueError(frame)


def close_eyes(lids, amount):
    """Happy arched seam, with no change to original eyeballs or face mesh.

    Both spherical caps meet above the center of the eye. The raised central
    seam differs from the downward-curved seam of the old carry experiment.
    """
    for obj, sign, upper in lids:
        obj.hide_render = amount <= 0
        pole = math.pi/2 if upper else -math.pi/2
        sweep = .52 + .48*amount
        for row in range(17):
            fraction = 0 if row == 0 else .006 if row == 1 else (row-1)/15
            for column in range(65):
                longitude = column*math.tau/64
                target = .28 - .43*math.cos(longitude)**2
                edge = pole + (target-pole)*sweep
                latitude = edge + (pole-edge)*fraction
                radius = .601
                obj.data.vertices[row*65+column].co = (
                    sign*.6829477 + radius*math.cos(latitude)*math.cos(longitude),
                    5.0818467 + radius*math.sin(latitude),
                    .6341138 + radius*math.cos(latitude)*math.sin(longitude))
        obj.data.update()
    bpy.context.view_layer.update()


def add_smile_shape(mesh):
    """Coherent mouth arc after Chin-only trials exposed the lower gum strip.

    Apply the same spatial field to lips, gums and teeth, retaining the original
    basis/topology/weights. Exclude separate eyes/nose components explicitly.
    """
    adjacency=[[] for _ in mesh.data.vertices]
    for edge in mesh.data.edges:
        a,b=edge.vertices
        adjacency[a].append(b); adjacency[b].append(a)
    unseen=set(range(len(adjacency)))
    allowed=set()
    while unseen:
        start=unseen.pop(); component=[start]; queue=[start]
        while queue:
            for neighbor in adjacency[queue.pop()]:
                if neighbor in unseen:
                    unseen.remove(neighbor);component.append(neighbor);queue.append(neighbor)
        if len(component) in (7755,97,459):
            allowed.update(component)
    assert len(mesh.data.vertices)==14886 and len(allowed)==10613
    mesh.shape_key_add(name='Basis')
    key=mesh.shape_key_add(name='WarmSmile')
    def ease(value):
        value=max(0.,min(1.,value))
        return value*value*(3-2*value)
    for vertex,target in zip(mesh.data.vertices,key.data):
        if vertex.index not in allowed:
            continue
        x,y,z=vertex.co
        mask=ease((y-3.65)/.5)*ease((4.8-y)/.3)*ease((z-.1)/.4)*ease((1.6-abs(x))/.35)
        arc=min(abs(x)/1.05,1.)**2
        target.co.y += .21*arc*mask
        target.co.x += .025*x*mask
    return key


def pose(character, smile, head=0):
    character.reset()
    bpy.data.objects['Stitch_Mesh'].data.shape_keys.key_blocks['WarmSmile'].value=smile
    # Avoid pitching the accepted thin lower lip toward the camera: the v3
    # pitch exposed a tiny pre-existing inner-mouth surface beneath the lip.
    character.rotate('Head', (0,1,0), .8*head)
    character.rotate('Ear_B.L', (0,1,0), .8*head)
    character.rotate('Ear_B.R', (0,1,0), -.65*head)
    bpy.context.view_layer.update()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--motion', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    OUT.mkdir(parents=True, exist_ok=True)
    source_hash = sha(SOURCE)
    assert source_hash==EXPECTED_SOURCE, 'Reinspect a changed source before authoring.'
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE), load_ui=False, use_scripts=False)
    scene = bpy.context.scene
    character = Character()
    rig, mesh = character.rig, bpy.data.objects['Stitch_Mesh']
    preserved = preservation_digests(mesh, rig)
    neutral = {b.name:b.matrix.copy() for b in rig.pose.bones}
    camera = [list(row) for row in scene.camera.matrix_world]
    smile_key=add_smile_shape(mesh)
    lids = create_lids(mesh, rig)
    for obj, _, _ in lids:
        obj.name = obj.name.replace('CarryLid', 'SmileLid')
    scene.render.resolution_x = scene.render.resolution_y = 400
    scene.render.resolution_percentage = 100
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.cycles.samples = 16
    scene.render.use_persistent_data = True
    records = {}
    if not args.motion:
        for name, amount, shut in [('neutral',0,0),('smile-open',1,0),('smile-closed',1,1)]:
            pose(character,amount,amount)
            close_eyes(lids,shut)
            path = OUT/(name+'.png')
            scene.render.filepath = str(path)
            bpy.ops.render.render(write_still=True)
            records[path.name] = sha(path)
        bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'smile-pose.blend'),compress=True)
    else:
        rig.animation_data.action = bpy.data.actions.new('NoseSmile_Preview_v1')
        for obj, _, _ in lids:
            close_eyes(lids,0)
            obj.shape_key_add(name='Basis')
        for frame in range(1,COUNT+1):
            scene.frame_set(frame)
            smile = sample(frame,[(1,0),(3,.08),(9,1),(16,1),(COUNT,0)])
            shut = sample(frame,[(1,0),(3,0),(8,1),(17,1),(25,0),(COUNT,0)])
            head = sample(frame,[(1,0),(4,-.3),(11,1),(17,.85),(COUNT,0)])
            pose(character,smile,head)
            smile_key.keyframe_insert(data_path='value',frame=frame)
            close_eyes(lids,shut)
            for bone in rig.pose.bones:
                for prop in ('location','rotation_quaternion','scale'):
                    bone.keyframe_insert(data_path=prop,frame=frame,group=bone.name)
            for obj, _, _ in lids:
                obj.keyframe_insert(data_path='hide_render',frame=frame)
                key = obj.shape_key_add(name='Frame_%02d'%frame,from_mix=False)
                for target,vertex in zip(key.data,obj.data.vertices):
                    target.co = vertex.co
                for at, value in [(max(0,frame-1),0),(frame,1),(frame+1,0)]:
                    key.value=value
                    key.keyframe_insert(data_path='value',frame=at)
        # Linear subframe interpolation, exact authored samples at integer frames.
        for action in bpy.data.actions:
            if action.name.startswith(('NoseSmile','Key')):
                for layer in action.layers:
                    for strip in layer.strips:
                        for bag in strip.channelbags:
                            for curve in bag.fcurves:
                                for key in curve.keyframe_points:
                                    key.interpolation='LINEAR'
        scene.frame_start,scene.frame_end,scene.render.fps = 1,COUNT,24
        scene.frame_set(1)
        saved = OUT/'smile-motion.blend'
        lid_names = [obj.name for obj,_,_ in lids]
        bpy.ops.wm.save_as_mainfile(filepath=str(saved),compress=True)
        bpy.ops.wm.open_mainfile(filepath=str(saved),load_ui=False,use_scripts=False)
        scene = bpy.context.scene
        rig,mesh = bpy.data.objects['Stitch_Armature'],bpy.data.objects['Stitch_Mesh']
        for frame in range(1,COUNT+1):
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            if frame in (1,COUNT):
                error = max(abs(b.matrix[i][j]-neutral[b.name][i][j])
                            for b in rig.pose.bones for i in range(4) for j in range(4))
                assert error < 1e-5, (frame,error)
                assert all(bpy.data.objects[name].hide_render for name in lid_names)
            path=OUT/('smile_%04d.png'%frame)
            scene.render.filepath=str(path)
            bpy.ops.render.render(write_still=True)
            records[path.name]=sha(path)
    assert sha(SOURCE)==source_hash
    assert preservation_digests(mesh,rig)==preserved
    assert [list(row) for row in scene.camera.matrix_world]==camera
    report={'preview_only':True,'source_sha256':source_hash,'source_unchanged':True,
            'original_mesh_rig_weights_uv_unchanged':True,'camera_unchanged':True,
            'fps':24,'samples':16,'frames':records,'added_lid_objects':4,
            'limits':'No runtime integration, native click or transition validation.'}
    (OUT/('motion-checks.json' if args.motion else 'pose-checks.json')).write_text(json.dumps(report,indent=2)+'\n')
    print('SMILE_PREVIEW_DONE',flush=True)


if __name__=='__main__':
    main()
