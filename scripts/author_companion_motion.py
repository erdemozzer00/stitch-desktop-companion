"""Phase 03 authored motion candidates, isolated from the accepted host prototype."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Quaternion, Vector

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / ".local/phase-01/stitch-stage.blend"
EXPECTED_STAGE = "674f2502a45a478a04285d6374904529ab327cd3dffd6aa37d3b88a685332413"


class Character:
    def __init__(self):
        self.rig = bpy.data.objects["Stitch_Armature"]
        bpy.context.scene.frame_set(1)
        bpy.context.view_layer.update()
        self.base = {b.name: b.matrix_basis.copy() for b in self.rig.pose.bones}
        self.world = {b.name: b.matrix.to_quaternion() for b in self.rig.pose.bones}
        self.rig.animation_data.action.use_fake_user = True
        self.rig.animation_data.action = None
        self.reset()

    def reset(self):
        for bone in self.rig.pose.bones:
            bone.matrix_basis = self.base[bone.name]

    def rotate(self, name, axis, degrees):
        bone = self.rig.pose.bones[name]
        local_axis = self.world[name].inverted() @ Vector(axis)
        bone.rotation_quaternion @= Quaternion(local_axis, math.radians(degrees))

    def local(self, name, axis, degrees):
        self.rig.pose.bones[name].rotation_quaternion @= Quaternion(axis, math.radians(degrees))

    def relaxed(self, variant="soft"):
        self.reset()
        if variant == "original":
            return
        amount = {"soft": 1.0, "tucked": 1.5}[variant]
        for side, sign, asymmetry in [("L", 1, 1.0), ("R", -1, 0.85)]:
            self.rotate("Shoulder." + side, (0, 1, 0), sign * 3 * amount)
            self.rotate("Arm." + side, (0, 1, 0), sign * 14 * amount * asymmetry)
            self.rotate("Arm." + side, (0, 0, 1), -sign * 9 * amount)
            self.rotate("ForeArm." + side, (1, 0, 0), -16 * amount)
            self.rotate("ForeArm." + side, (0, 1, 0), -sign * 6 * amount)
            self.rotate("Wrist." + side, (0, 1, 0), sign * 5)
            for digit in "ABC":
                self.local("Finger_" + digit + "." + side, (1, 0, 0), 9 * amount)
                self.local("FingerTip_" + digit + "." + side, (1, 0, 0), 6 * amount)
        self.rotate("Head", (0, 1, 0), -1.8 * amount)
        self.rotate("Ear_A.L", (0, 1, 0), 3 * amount)
        self.rotate("Ear_A.R", (0, 1, 0), -1 * amount)
        bpy.context.view_layer.update()

    def idle(self, phase):
        self.relaxed()
        angle = phase * math.tau
        # Local ribcage motion, not uniform scaling of the entire character.
        breath = math.sin(angle)
        self.rig.pose.bones["Spine.003"].scale.x *= 1 + .009 * breath
        self.rig.pose.bones["Spine.003"].scale.z *= 1 + .006 * breath
        self.rotate("Spine.002", (1, 0, 0), .45 * breath)
        self.rotate("Head", (1, 0, 0), -.6 * math.sin(angle - .25))
        self.rotate("Head", (0, 1, 0), .55 * math.sin(angle))
        for side, sign in [("L", 1), ("R", -1)]:
            lag = math.sin(angle - .5) - math.sin(-.5)
            self.rotate("Ear_A." + side, (0, 1, 0), sign * .65 * lag)
            self.rotate("Ear_B." + side, (0, 1, 0), sign * .4 * (math.sin(angle - .75) - math.sin(-.75)))
            self.rotate("Arm." + side, (0, 1, 0), sign * .45 * math.sin(angle - .15))
        bpy.context.view_layer.update()

    def wave(self, frame):
        self.idle(0)
        # Shorter rise and return, with unequal greeting strokes and wrist lag.
        def sample(keys):
            for (a, av), (b, bv) in zip(keys, keys[1:]):
                if a <= frame <= b:
                    u = (frame - a) / (b - a)
                    u = u * u * (3 - 2 * u)
                    return av + (bv - av) * u
            return keys[0][1] if frame < keys[0][0] else keys[-1][1]
        lift = sample([(1, 0), (4, 0), (12, 1), (33, 1), (45, 0), (49, 0)])
        neutral = {b.name: b.rotation_quaternion.copy() for b in self.rig.pose.bones}
        for name, deg in [("Shoulder.L", -2), ("Arm.L", -8), ("ForeArm.L", -52), ("Wrist.L", -30)]:
            self.rig.pose.bones[name].matrix_basis = self.base[name]
            self.rotate(name, (0, 1, 0), deg)
            if name == "Wrist.L":
                self.local(name, (0, 1, 0), 70)
            target = self.rig.pose.bones[name].rotation_quaternion.copy()
            self.rig.pose.bones[name].rotation_quaternion = neutral[name].slerp(target, lift)
        fore = sample([(1,0),(12,0),(16,-7),(22,6),(27,-6),(33,3),(37,0),(49,0)])
        wrist = sample([(1,0),(13,0),(18,-11),(24,10),(29,-9),(35,5),(39,0),(49,0)])
        self.rotate("ForeArm.L", (0, 1, 0), fore)
        self.rotate("Wrist.L", (0, 1, 0), wrist)
        # Open the raised hand as it lifts; keep the resting hand softly curled.
        for digit in "ABC":
            self.local("Finger_" + digit + ".L", (1,0,0), -9 * max(lift, 0))
            self.local("FingerTip_" + digit + ".L", (1,0,0), -6 * max(lift, 0))
        nod = sample([(1,0),(7,-1),(15,1.5),(29,1),(43,0),(49,0)])
        self.rotate("Head", (1,0,0), nod)
        self.rotate("Head", (0,1,0), -.65 * lift)
        self.rotate("Ear_B.R", (0,1,0), sample([(1,0),(12,0),(19,1.2),(28,-.7),(37,.4),(47,0),(49,0)]))
        bpy.context.view_layer.update()


def render(scene, path):
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["poses", "motion"], default="poses")
    parser.add_argument("--size", type=int, default=320)
    parser.add_argument("--samples", type=int, default=6)
    parser.add_argument("--clip", choices=["both", "idle", "wave"], default="both")
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    assert hashlib.sha256(STAGE.read_bytes()).hexdigest() == EXPECTED_STAGE
    output = ROOT / ".local/phase-03"
    output.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(STAGE), load_ui=False, use_scripts=False)
    scene = bpy.context.scene
    character = Character()
    inventory = [{"name": b.name, "parent": b.parent.name if b.parent else None,
                  "mode": b.rotation_mode, "constraints": [c.type for c in b.constraints]}
                 for b in character.rig.pose.bones]
    (output / "controls.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print("CONTROLS " + json.dumps([b for b in inventory if any(term in b["name"].lower() for term in ("lid", "eye", "mouth", "lip"))]))
    scene.render.resolution_x = scene.render.resolution_y = args.size
    scene.render.resolution_percentage = 100
    scene.cycles.samples = args.samples
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    if args.mode == "poses":
        for name in ("original", "soft", "tucked"):
            character.relaxed(name)
            if not args.no_render:
                render(scene, output / ("pose_" + name + ".png"))
        character.relaxed("soft")
        scene.render.engine = "CYCLES"
        bpy.ops.wm.save_as_mainfile(filepath=str(output / "pose-study.blend"), compress=True)
    else:
        scene.render.fps = 24
        for clip, count in [("idle", 96), ("wave", 49)]:
            if args.clip not in ("both", clip):
                continue
            folder = output / clip
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "manifest.json").unlink(missing_ok=True)
            action = bpy.data.actions.new("Companion_" + clip.title() + "_v2")
            character.rig.animation_data.action = action
            action.use_fake_user = True
            for frame in range(1, (count + 2) if clip == "idle" else (count + 1)):
                scene.frame_set(frame)
                if clip == "idle":
                    character.idle((frame - 1) / count)
                else:
                    character.wave(frame)
                for bone in character.rig.pose.bones:
                    for prop in ("location", "rotation_quaternion", "scale"):
                        bone.keyframe_insert(data_path=prop, frame=frame, group=bone.name)
            for layer in action.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        for curve in bag.fcurves:
                            for key in curve.keyframe_points:
                                key.interpolation = "LINEAR"
            # The idle endpoint at frame 97 validates the seam, but is not duplicated in playback.
            scene.frame_start, scene.frame_end = 1, count
            scene.frame_set(1)
            bpy.ops.wm.save_as_mainfile(filepath=str(folder / (clip + ".blend")), compress=True)
            if args.no_render:
                continue
            scene.render.filepath = str(folder / (clip + "_"))
            bpy.ops.render.render(animation=True)
            manifest = {"clip": clip, "frames": count, "fps": 24, "size": args.size,
                        "samples": args.samples, "visual_approval": False,
                        "frame_sha256": {f"{clip}_{i:04}.png": hashlib.sha256((folder / f"{clip}_{i:04}.png").read_bytes()).hexdigest()
                                         for i in range(1, count + 1)}}
            (folder / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    assert hashlib.sha256(STAGE.read_bytes()).hexdigest() == EXPECTED_STAGE


if __name__ == "__main__":
    main()
