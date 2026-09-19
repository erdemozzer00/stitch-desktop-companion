"""Private geometric eyelid study; preserve the accepted directional action and source."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from prepare_stage import preservation_digests
from verify_companion_motion import action_data

OUT = ROOT / '.local/phase-04/directional-eyes-v1'
SOURCE = ROOT / '.local/phase-04/directional-v1'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_lids(mesh, rig):
    """Spherical caps outside the two inspected eye components, weighted to Head.

    Coordinates use the original mesh's Y-up local space. UV samples reuse its
    pale eye-surround and dark-blue crease colors, including its diffuse shader.
    Neither the eyeballs nor the accepted character mesh are deformed.
    """
    lids = []
    for sign in (-1, 1):
        for upper in (False, True):
            vertices = [(0, 0, 0)] * (17 * 65)
            faces = [(r*65+c, r*65+c+1, (r+1)*65+c+1, (r+1)*65+c)
                     for r in range(16) for c in range(64)]
            data = bpy.data.meshes.new('CarryLidGeometry')
            data.from_pydata(vertices, [], faces)
            obj = bpy.data.objects.new(f'CarryLid_{sign}_{upper}', data)
            bpy.context.collection.objects.link(obj)
            obj.matrix_world = mesh.matrix_world.copy()
            data.materials.append(mesh.data.materials[0])
            uv = data.uv_layers.new(name='SourceSkinSample')
            for polygon in data.polygons:
                polygon.use_smooth = True
                row = polygon.index // 64
                # A narrow seam at the moving edge, not a painted line across the face.
                sample = (.482832, .285916) if row == 0 else (.486896, .294577)
                for index in polygon.loop_indices:
                    uv.data[index].uv = sample
            obj.vertex_groups.new(name='Head').add(list(range(len(vertices))), 1., 'REPLACE')
            modifier = obj.modifiers.new('FollowAcceptedHead', 'ARMATURE')
            modifier.object = rig
            lids.append((obj, sign, upper))
    return lids


def closure(lids, amount):
    for obj, sign, upper in lids:
        obj.hide_render = amount == 0
        pole = math.pi/2 if upper else -math.pi/2
        # The socket hides the first half of a pole-to-equator sweep. Start there
        # so the visible close spans the whole authored transition.
        sweep = .52 + .48*amount
        edge = pole + (-.14-pole)*sweep
        for row in range(17):
            # First ring is a fine dark-blue rim; other rings cover the sphere.
            fraction = (0 if row == 0 else .006 if row == 1 else (row-1)/15)
            for column in range(65):
                longitude = column*math.tau/64
                curved_edge = edge + .12*math.cos(longitude)**2*amount
                latitude = curved_edge + (pole-curved_edge)*fraction
                radius = .601
                obj.data.vertices[row*65+column].co = (
                    sign*.6829477 + radius*math.cos(latitude)*math.cos(longitude),
                    5.0818467 + radius*math.sin(latitude),
                    .6341138 + radius*math.cos(latitude)*math.sin(longitude))
        obj.data.update()
    bpy.context.view_layer.update()


def main():
    global OUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if not args.bank:
        OUT = OUT / 'study'
    OUT.mkdir(parents=True, exist_ok=True)
    source = SOURCE / 'drag-bank.blend'
    source_hash = sha(source)
    bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
    scene = bpy.context.scene
    scene.frame_set(23)
    mesh, rig = bpy.data.objects['Stitch_Mesh'], bpy.data.objects['Stitch_Armature']
    before = preservation_digests(mesh, rig)
    action = action_data(rig.animation_data.action)
    camera = [list(row) for row in scene.camera.matrix_world]
    lids = create_lids(mesh, rig)
    scene.render.resolution_x = scene.render.resolution_y = 240 if args.bank else 400
    scene.cycles.samples = 6 if args.bank else 24
    records = {}
    targets = [('blink_%d.png' % i, 23, i/6) for i in range(7)]
    if args.bank:
        manifest = json.loads((SOURCE/'bank-manifest.json').read_text())
        targets += [(name, record['frame'], 1.) for name, record in manifest['frames'].items()]
    for name, frame, amount in targets:
        scene.frame_set(frame)
        closure(lids, amount)
        scene.render.filepath = str(OUT/name)
        bpy.ops.render.render(write_still=True)
        records[name] = {'frame': frame, 'closure': amount, 'sha256': sha(OUT/name)}
    closure(lids, 1.)
    scene.frame_set(23)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'closed-eyes.blend'), compress=True)
    assert before == preservation_digests(mesh, rig)
    assert action == action_data(rig.animation_data.action)
    assert camera == [list(row) for row in scene.camera.matrix_world]
    assert sha(source) == source_hash
    report = {'source_sha256': source_hash, 'size': scene.render.resolution_x,
              'samples': scene.cycles.samples, 'added_lid_objects': 4, 'frames': records,
              'preservation': 'PASS: accepted source bytes, mesh/rig fields, directional action and camera',
              'limits': 'Geometric cap prototype; eye opening during arbitrary moving native entries remains unproven.'}
    (OUT/('eyes-manifest.json' if args.bank else 'eye-study.json')).write_text(json.dumps(report, indent=2))
    print('CARRY_EYES_DONE', flush=True)


if __name__ == '__main__':
    main()
