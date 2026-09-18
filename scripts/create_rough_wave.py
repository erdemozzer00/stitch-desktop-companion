"""Reproducible Phase 02 FK blocking; never modifies the verified stage."""
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
STAGE_HASH = "674f2502a45a478a04285d6374904529ab327cd3dffd6aa37d3b88a685332413"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blocks", action="store_true")
    parser.add_argument("--wrist-twist", type=float, default=70)
    parser.add_argument("--clearance-blocks", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    assert hashlib.sha256(STAGE.read_bytes()).hexdigest() == STAGE_HASH
    output = ROOT / ".local/phase-02/wave"
    output.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(STAGE), load_ui=False, use_scripts=False)
    scene = bpy.context.scene
    rig = bpy.data.objects["Stitch_Armature"]
    scene.frame_set(1)
    bpy.context.view_layer.update()
    base = {b.name: b.matrix_basis.copy() for b in rig.pose.bones}
    orientations = {b.name: b.matrix.to_quaternion() for b in rig.pose.bones}
    source_action = rig.animation_data.action
    source_action.use_fake_user = True
    rig.animation_data.action = None

    def pose(shoulder=0, arm=0, forearm=0, wrist=0, twist=0, head=0, ear=0):
        for bone in rig.pose.bones:
            bone.matrix_basis = base[bone.name]
        def rotate(name, axis, degrees):
            bone = rig.pose.bones[name]
            local_axis = orientations[name].inverted() @ Vector(axis)
            bone.rotation_quaternion = base[name].to_quaternion() @ Quaternion(local_axis, math.radians(degrees))
        rotate("Shoulder.L", (0, 1, 0), shoulder)
        rotate("Arm.L", (0, 1, 0), arm)
        rotate("ForeArm.L", (0, 1, 0), forearm)
        rotate("Wrist.L", (0, 1, 0), wrist)
        rig.pose.bones["Wrist.L"].rotation_quaternion @= Quaternion((0, 1, 0), math.radians(twist))
        rotate("Head", (0, 1, 0), head)
        rotate("Ear_A.R", (0, 1, 0), ear)
        rotate("Ear_A.L", (0, 1, 0), ear * 0.6)
        bpy.context.view_layer.update()

    scene.render.resolution_x = scene.render.resolution_y = 320
    scene.render.resolution_percentage = 100
    scene.cycles.samples = 8
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.fps = 24
    if args.clearance_blocks:
        for label, arm, forearm, wrist in [("low", -8, -52, -30), ("wide", -15, -48, -25), ("middle", -12, -55, -15)]:
            pose(-2, arm, forearm, wrist, 70)
            scene.render.filepath = str(output / f"block_clearance_{label}.png")
            bpy.ops.render.render(write_still=True)
        return
    if args.blocks:
        for twist in (0, 60, 90):
            pose(-5, -27, -66, 0, twist)
            scene.render.filepath = str(output / f"block_twist_{twist:02}.png")
            bpy.ops.render.render(write_still=True)
        return

    # A failed rerender must not leave a stale completion marker.
    (output / "render-report.json").unlink(missing_ok=True)
    action = bpy.data.actions.new("Companion_RoughWave_v1")
    rig.animation_data.action = action
    t = args.wrist_twist
    # Frame, shoulder, upper arm, forearm, wrist, palm-facing twist, head, ear.
    # Values are artistic blocking candidates, not universal anatomical limits.
    keys = [
        (1, 0, 0, 0, 0, 0, 0, 0),
        (7, 1, 2, 4, 0, 0, 1, 0),
        (19, -2, -8, -52, -30, t, -1, 0),
        (25, -2, -8, -56, -38, t, -1.5, -0.8),
        (32, -2, -8, -48, -22, t, -1.3, -0.4),
        (39, -2, -8, -55, -37, t, -1, 0.3),
        (46, -2, -8, -49, -23, t, -0.8, 0.2),
        (52, -2, -8, -52, -30, t, -0.5, 0),
        (66, 0, 0, 0, 0, 0, 0, 0.3),
        (73, 0, 0, 0, 0, 0, 0, 0),
    ]
    for values in keys:
        frame, *angles = values
        scene.frame_set(frame)
        pose(*angles)
        for bone in rig.pose.bones:
            for path in ("location", "rotation_quaternion", "scale"):
                bone.keyframe_insert(data_path=path, frame=frame, group=bone.name)
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for key in curve.keyframe_points:
                        key.interpolation = "BEZIER"
                        key.handle_left_type = key.handle_right_type = "AUTO_CLAMPED"
    scene.frame_start, scene.frame_end = 1, 73
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(output / "stitch-rough-wave.blend"), compress=True)
    scene.render.filepath = str(output / "wave_")
    bpy.ops.render.render(animation=True)
    assert hashlib.sha256(STAGE.read_bytes()).hexdigest() == STAGE_HASH
    report = {"status": "ROUGH_RENDER_ONLY", "stage_sha256": STAGE_HASH,
              "action": action.name, "source_action_retained": source_action.name,
              "frames": 73, "fps": 24, "size": 320, "samples": 8,
              "keys": keys, "visual_approval": False,
              "frame_sha256": {f"wave_{i:04}.png": hashlib.sha256((output / f"wave_{i:04}.png").read_bytes()).hexdigest()
                               for i in range(1, 74)},
              "limitations": ["No final polish", "No automatic intersection or anatomical quality proof"]}
    (output / "render-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
