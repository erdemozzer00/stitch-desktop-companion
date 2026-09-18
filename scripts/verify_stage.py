"""Reopen the prepared Blender file and check the actual saved asset."""

import json
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_stage import (EXPECTED, RENDER_FRAMES, local_path, preservation_digests,
                           require_preservation, sha256, used_images)


def main():
    verification = ROOT / "context/evidence/phase-01-verification.json"
    verification.parent.mkdir(parents=True, exist_ok=True)
    verification.write_text('{"status": "RUNNING"}\n', encoding="utf-8")
    report_path = ROOT / "context/evidence/phase-01.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "PREPARED"
    assert report.get("rendered_frames") == list(RENDER_FRAMES), "Expected rendered frames are exactly [1, 20, 40]"
    stage = local_path(report["local_stage"])
    stage_hash = sha256(stage)
    assert stage_hash == report.get("stage_sha256"), "Saved stage does not match its preparation report"
    bpy.ops.wm.open_mainfile(filepath=str(stage), load_ui=False, use_scripts=False)
    mesh, rig = bpy.data.objects["Stitch_Mesh"], bpy.data.objects["Stitch_Armature"]
    require_preservation(preservation_digests(mesh, rig), report)
    assert len(rig.data.bones) == report["bones"] == 127
    assert len(mesh.data.vertices) == report["vertices"] == 14886
    assert bpy.context.scene.camera and bpy.context.scene.render.film_transparent
    assert bpy.context.scene.render.image_settings.color_mode == "RGBA"
    assert [{"name": a.name, "range": list(a.frame_range)} for a in bpy.data.actions] == report["actions"]
    images = used_images()
    assert images, "The staged materials have no texture images"
    assert [{"name": i.name, "size": list(i.size), "packed": bool(i.packed_file)}
            for i in sorted(images, key=lambda x: x.name)] == report["used_images"]
    assert all(i.packed_file and min(i.size) > 0 for i in images)
    assert all(sha256(ROOT / report["local_input"] / name) == expected for name, expected in EXPECTED.items())
    frames = []
    for frame in RENDER_FRAMES:
        path = stage.parent / f"frame_{frame:02}.png"
        assert path.is_file() and path.stat().st_size > 0, f"Expected rendered frame is missing or empty: {path.name}"
        image = bpy.data.images.load(str(path), check_existing=False)
        assert list(image.size) == [768, 768] and image.channels == 4
        alpha = list(image.pixels)[3::4]
        assert min(alpha) == 0 and max(alpha) > 0.99
        width = image.size[0]
        border = alpha[:width] + alpha[-width:] + alpha[::width] + alpha[width - 1::width]
        assert max(border) == 0, "Character reaches the frame edge"
        frames.append({"frame": frame, "sha256": sha256(path), "alpha_border_clear": True})
        bpy.data.images.remove(image)
    assert sha256(stage) == stage_hash, "Saved stage changed during verification"
    result = {
        "status": "PASS", "stage_reopened": True, "packed_textures_verified": True,
        "stage_sha256": stage_hash, "stage_matches_preparation": True,
        "mesh_vertex_positions_preserved": True, "mesh_topology_preserved": True,
        "vertex_group_definitions_and_weights_preserved": True, "mesh_uv_data_preserved": True,
        "bone_names_parents_and_rest_matrices_preserved": True,
        "material_backface_culling_preserved": True,
        "existing_action_names_and_ranges_preserved": True,
        "local_inputs_unchanged": True, "renders": frames,
        "limits": "Checks cover the named fields, not every constraint, shader or action keyframe property. "
                  "Rendered frames do not prove animation quality, desktop behavior or target-PC compatibility.",
    }
    verification.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PHASE_01_VERIFIED " + json.dumps(result))


if __name__ == "__main__":
    main()
