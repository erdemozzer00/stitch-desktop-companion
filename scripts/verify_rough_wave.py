"""Compare the saved rough-wave scene with the verified source stage."""
import hashlib
import json
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_stage import preservation_digests


def action_keys(action):
    return [(curve.data_path, curve.array_index,
             [(list(key.co), key.interpolation, list(key.handle_left), list(key.handle_right))
              for key in curve.keyframe_points])
            for layer in action.layers for strip in layer.strips
            for bag in strip.channelbags for curve in bag.fcurves]


def state():
    rig = bpy.data.objects["Stitch_Armature"]
    mesh = next(obj for obj in bpy.data.objects if obj.type == "MESH")
    return rig, preservation_digests(mesh, rig)


stage = ROOT / ".local/phase-01/stitch-stage.blend"
wave = ROOT / ".local/phase-02/wave/stitch-rough-wave.blend"
bpy.ops.wm.open_mainfile(filepath=str(stage), load_ui=False, use_scripts=False)
original_rig, original_data = state()
source_keys = action_keys(bpy.data.actions["Stitch_Anim"])
bpy.ops.wm.open_mainfile(filepath=str(wave), load_ui=False, use_scripts=False)
rig, new_data = state()
assert original_data == new_data, "Geometry, weights, UV, rest rig or material flags changed"
assert source_keys == action_keys(bpy.data.actions["Stitch_Anim"]), "Existing action keys changed"
scene = bpy.context.scene
scene.frame_set(1)
feet = {bone.name: bone.matrix.copy() for bone in rig.pose.bones if bone.name.startswith("Toe_")}
assert len(feet) == 8
start = {bone.name: bone.matrix.copy() for bone in rig.pose.bones}
max_foot_delta = 0.0
for frame in range(1, 74):
    scene.frame_set(frame)
    for name, reference in feet.items():
        actual = rig.pose.bones[name].matrix
        max_foot_delta = max(max_foot_delta, max(abs(actual[r][c] - reference[r][c]) for r in range(4) for c in range(4)))
assert max_foot_delta < 1e-5, "Planted toe transforms drift"
end_delta = max(abs(bone.matrix[r][c] - start[bone.name][r][c]) for bone in rig.pose.bones for r in range(4) for c in range(4))
assert end_delta < 1e-5, "Reaction end does not return to its initial pose"
report = {"status": "PASS", "stage_sha256": hashlib.sha256(stage.read_bytes()).hexdigest(),
          "wave_sha256": hashlib.sha256(wave.read_bytes()).hexdigest(),
          "preservation_digests_match": True, "original_action_key_data_match": True,
          "toe_transforms_checked": len(feet), "max_toe_matrix_delta": max_foot_delta,
          "end_pose_max_matrix_delta": end_delta,
          "limits": ["Not mesh self-intersection or motion-quality proof", "Named data checks, not every Blender setting"]}
(ROOT / "context/evidence/phase-02-wave-verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report))
