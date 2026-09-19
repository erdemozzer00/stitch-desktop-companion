"""Reopen Phase 03 candidates and check preservation and animation boundaries."""
import hashlib
import json
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_stage import preservation_digests


def action_data(action):
    return [(c.data_path, c.array_index, [(list(k.co), k.interpolation, list(k.handle_left), list(k.handle_right))
             for k in c.keyframe_points]) for layer in action.layers for strip in layer.strips
            for bag in strip.channelbags for c in bag.fcurves]


def matrices(rig):
    bpy.context.view_layer.update()
    return {b.name: b.matrix.copy() for b in rig.pose.bones}


def delta(a, b):
    return max(abs(a[n][r][c] - b[n][r][c]) for n in a for r in range(4) for c in range(4))


def main():
    output = ROOT / '.local/phase-03'
    appearance_pass = '--appearance' in sys.argv
    if appearance_pass:
        output /= 'appearance-final'
    stage = ROOT / ".local/phase-01/stitch-stage.blend"
    bpy.ops.wm.open_mainfile(filepath=str(stage), load_ui=False, use_scripts=False)
    rig = bpy.data.objects["Stitch_Armature"]
    baseline = preservation_digests(bpy.data.objects["Stitch_Mesh"], rig)
    original_action = action_data(bpy.data.actions["Stitch_Anim"])
    bpy.context.scene.frame_set(1)
    source_pose = matrices(rig)
    feet = {n: value for n, value in source_pose.items() if n.startswith("Toe_")}
    assert len(feet) == 8
    report = {"status": "PASS", "artifact_directory": str(output.relative_to(ROOT)), "stage_sha256": hashlib.sha256(stage.read_bytes()).hexdigest(), "clips": {}}
    idle_start = None
    for clip, count in [("idle", 96), ("wave", 45)]:
        path = output / clip / (clip + '.blend')
        if appearance_pass:
            source = ROOT / f'.local/phase-03/{clip}/{clip}.blend'
            bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
            accepted_motion = action_data(bpy.data.objects['Stitch_Armature'].animation_data.action)
            accepted_camera = [list(row) for row in bpy.context.scene.camera.matrix_world]
            accepted_scale = bpy.context.scene.camera.data.ortho_scale
        bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False, use_scripts=False)
        rig = bpy.data.objects["Stitch_Armature"]
        assert preservation_digests(bpy.data.objects["Stitch_Mesh"], rig) == baseline
        assert action_data(bpy.data.actions["Stitch_Anim"]) == original_action
        scene = bpy.context.scene
        if appearance_pass:
            assert action_data(rig.animation_data.action) == accepted_motion
            assert [list(row) for row in scene.camera.matrix_world] == accepted_camera
            assert scene.camera.data.ortho_scale == accepted_scale
            assert scene.render.resolution_x == scene.render.resolution_y == 400
        assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, count, 24)
        poses = []
        max_foot = 0
        for frame in range(1, count + 2 if clip == "idle" else count + 1):
            scene.frame_set(frame)
            pose = matrices(rig)
            poses.append(pose)
            max_foot = max(max_foot, delta(feet, pose))
        assert max_foot < 1e-5, "Toe transforms moved"
        boundary = delta(poses[0], poses[-1])
        assert boundary < 1e-5, "Endpoint poses differ"
        if clip == "idle":
            idle_start = poses[0]
            idle_poses = poses
            # Compare sampled finite differences across the periodic seam.
            left = {n: poses[-1][n] - poses[-2][n] for n in poses[0]}
            right = {n: poses[1][n] - poses[0][n] for n in poses[0]}
            seam_velocity_delta = delta(left, right)
            assert seam_velocity_delta < .002, "Unexpected idle seam acceleration"
        else:
            assert delta(idle_start, poses[0]) < 1e-5, "Idle neutral and wave entry differ"
        report["clips"][clip] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                  "frames": count, "fps": 24,
                                  "preservation_and_source_action_match": True,
                                  "max_toe_matrix_delta": max_foot, "endpoint_matrix_delta": boundary,
                                  "distinct_motion": delta(poses[0], poses[count // 3])}
        assert report["clips"][clip]["distinct_motion"] > .001
        if clip == "idle":
            report["clips"][clip]["seam_finite_difference_delta"] = seam_velocity_delta
    report["idle_neutral_matches_wave_entry"] = True
    entry_folder = output / 'entries'
    entry_manifest = json.loads((entry_folder / 'manifest.json').read_text(encoding='utf-8'))
    assert entry_manifest['idle_sha256'] == report['clips']['idle']['sha256'], 'Entries belong to a different idle'
    assert entry_manifest['buckets'] == 24
    max_entry_pose_error = max_entry_foot_error = 0.0
    for bucket in range(24):
        if appearance_pass:
            accepted_entry = ROOT / '.local/phase-03/entries' / ('entry_%02d.blend' % bucket)
            bpy.ops.wm.open_mainfile(filepath=str(accepted_entry), load_ui=False, use_scripts=False)
            accepted_entry_motion = action_data(bpy.data.objects['Stitch_Armature'].animation_data.action)
        bpy.ops.wm.open_mainfile(filepath=str(entry_folder / ('entry_%02d.blend' % bucket)), load_ui=False, use_scripts=False)
        rig = bpy.data.objects['Stitch_Armature']
        if appearance_pass:
            assert action_data(rig.animation_data.action) == accepted_entry_motion
            assert [list(row) for row in bpy.context.scene.camera.matrix_world] == accepted_camera
            assert bpy.context.scene.camera.data.ortho_scale == accepted_scale
        assert preservation_digests(bpy.data.objects['Stitch_Mesh'], rig) == baseline
        assert action_data(bpy.data.actions['Stitch_Anim']) == original_action
        for frame in range(1, 5):
            bpy.context.scene.frame_set(frame)
            current = matrices(rig)
            max_entry_foot_error = max(max_entry_foot_error, delta(feet, current))
            if frame in (1, 4):
                expected = idle_poses[bucket * 4] if frame == 1 else idle_start
                max_entry_pose_error = max(max_entry_pose_error, delta(expected, current))
    assert max_entry_pose_error < 1e-5 and max_entry_foot_error < 1e-5
    report['entry_checks'] = {'clips': 24, 'source_and_action_preserved': True,
                              'max_endpoint_matrix_delta': max_entry_pose_error,
                              'max_toe_matrix_delta': max_entry_foot_error,
                              'max_projected_entry_gap_400px': entry_manifest['max_entry_vertex_gap_at_400px']}
    report['appearance_preserves_accepted_motion_and_camera'] = appearance_pass
    report["limits"] = ["Toe matrix stability is not full mesh contact/intersection proof",
                        "Sampled idle entries are approximate; perceptual transition acceptance is separate",
                        "No visual naturalness or target-PC acceptance"]
    (ROOT / "context/evidence/phase-03-motion-checks.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
