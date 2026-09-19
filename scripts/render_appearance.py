"""Appearance-only comparison/rerender of accepted, saved motion; no re-authoring."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import shutil

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / '.local/phase-03'

def appearance(variant, size, samples):
    scene = bpy.context.scene
    scene.render.resolution_x = scene.render.resolution_y = size
    scene.render.resolution_percentage = 100
    scene.cycles.samples = samples
    if variant != 'baseline':
        height = (bpy.data.objects['Key'].data.energy / 70) ** .5
        center = bpy.data.objects['Key'].location - Vector((-1.1, -1.5, 1.7)) * height
        target = center + Vector((0, 0, -.28)) * height
        data = bpy.data.lights.new('LowerFill', 'AREA')
        data.energy = (20 if variant == 'lifted' else 12) * height * height
        data.shape = 'DISK'
        data.size = 1.6 * height
        light = bpy.data.objects.new('LowerFill', data)
        scene.collection.objects.link(light)
        light.location = center + Vector((0, -1.5, -.12)) * height
        light.rotation_euler = (target - light.location).to_track_quat('-Z', 'Y').to_euler()
    if variant == 'outline':
        for modifier in bpy.data.objects['Stitch_Mesh'].modifiers:
            if modifier.type == 'SOLIDIFY':
                modifier.show_render = modifier.show_viewport = True
    return scene

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['compare', 'quality', 'production'], default='compare')
    parser.add_argument('--variant', choices=['baseline', 'soft', 'lifted', 'outline'], default='soft')
    parser.add_argument('--samples', type=int, default=24)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.mode == 'production':
        output = PHASE / 'appearance-final'
        sys.path.insert(0, str(ROOT / 'scripts'))
        from verify_companion_motion import action_data
        sources = [('idle', 'idle', 96), ('wave', 'wave', 45)] + [('entries', 'entry_%02d' % i, 4) for i in range(24)]
        manifests = {}
        for clip, name, count in sources:
            source = PHASE / clip / (name + '.blend')
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
            rig = bpy.data.objects['Stitch_Armature']
            motion = action_data(rig.animation_data.action)
            scene = appearance(args.variant, 400, args.samples)
            scene.render.use_persistent_data = True
            folder = output / clip
            folder.mkdir(parents=True, exist_ok=True)
            (folder / 'manifest.json').unlink(missing_ok=True)
            scene.frame_set(1)
            bpy.ops.wm.save_as_mainfile(filepath=str(folder / (name + '.blend')), compress=True)
            if clip == 'entries':
                bucket = int(name[-2:])
                shutil.copy2(output / 'idle' / ('idle_%04d.png' % (bucket * 4 + 1)), folder / (name + '_0001.png'))
                shutil.copy2(output / 'wave/wave_0001.png', folder / (name + '_0004.png'))
                frames = [2, 3]
            else:
                frames = range(1, count + 1)
            for frame in frames:
                scene.frame_set(frame)
                scene.render.filepath = str(folder / ('%s_%04d.png' % (name, frame)))
                bpy.ops.render.render(write_still=True)
            assert action_data(rig.animation_data.action) == motion
            assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
            manifest = manifests.setdefault(clip, {'fps': 24, 'size': 400, 'samples': args.samples,
                'appearance': args.variant, 'frame_sha256': {}, 'source_scene_sha256': {}})
            manifest['source_scene_sha256'][name] = digest
            for frame in range(1, count + 1):
                filename = '%s_%04d.png' % (name, frame)
                manifest['frame_sha256'][filename] = hashlib.sha256((folder / filename).read_bytes()).hexdigest()
            manifest['frames'] = len(manifest['frame_sha256'])
            if clip != 'entries' or name == 'entry_23':
                if clip == 'entries':
                    original = json.loads((PHASE / 'entries/manifest.json').read_text(encoding='utf-8'))
                    manifest.update({key: original[key] for key in ['buckets', 'frames_per_entry', 'max_entry_vertex_gap_at_400px']})
                    manifest['idle_sha256'] = hashlib.sha256((output / 'idle/idle.blend').read_bytes()).hexdigest()
                (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        return
    output = PHASE / 'appearance'
    output.mkdir(exist_ok=True)
    report = []
    for clip, frame in [('idle', 1), ('wave', 20)]:
        source = PHASE / clip / (clip + '.blend')
        original = hashlib.sha256(source.read_bytes()).hexdigest()
        for variant in (['soft'] if args.mode == 'quality' else ['baseline', 'soft', 'lifted', 'outline']):
            bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
            scene = appearance(variant, 400, args.samples)
            scene.frame_set(frame)
            name = '%s-%s-%ds.png' % (clip, variant, args.samples)
            scene.render.filepath = str(output / name)
            bpy.ops.render.render(write_still=True)
            report.append({'file': name, 'source_sha256': original, 'frame': frame, 'variant': variant,
                           'sha256': hashlib.sha256((output / name).read_bytes()).hexdigest()})
        assert hashlib.sha256(source.read_bytes()).hexdigest() == original
    (output / ('quality-manifest.json' if args.mode == 'quality' else 'comparison-manifest.json')).write_text(json.dumps(report, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
