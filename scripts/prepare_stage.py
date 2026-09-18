"""Prepare a local Blender stage from the supplied assets; never edit inputs."""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import zipfile

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "stitch.zip": "a6611ed74fb85c07cf2f79c4f0a24699bde71bc0b79441bc4102229a26a847c6",
    "stitch.glb": "22cbb36ea9023e109c534a7d1eab7b06cdb0e3da124d4888020ca639b8550942",
}
MEMBERS = (
    "source/Stitch_sketchfab.blend",
    "textures/Stitch_texture_v2.png",
    "textures/Stitch_texture_v3.png",
)
RENDER_FRAMES = (1, 20, 40)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_path(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT / ".local"):
        raise ValueError("Inputs and generated assets must stay under .local/")
    return path


def geometry_digest(mesh):
    digest = hashlib.sha256()
    for vertex in mesh.vertices:
        digest.update(struct.pack("<3f", *vertex.co))
    return digest.hexdigest()


def rig_digest(armature):
    data = [(b.name, b.parent.name if b.parent else None,
             [list(row) for row in b.matrix_local]) for b in armature.bones]
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def data_digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def preservation_digests(mesh, rig):
    """Describe only the source data that this preparation promises to preserve."""
    return {
        "mesh_geometry_sha256": geometry_digest(mesh.data),
        "rig_rest_sha256": rig_digest(rig.data),
        "mesh_topology_sha256": data_digest({
            "edges": [list(edge.vertices) for edge in mesh.data.edges],
            "loops": [(loop.vertex_index, loop.edge_index) for loop in mesh.data.loops],
            "polygons": [(polygon.loop_start, polygon.loop_total)
                         for polygon in mesh.data.polygons],
        }),
        "vertex_group_definitions_sha256": data_digest([
            (group.index, group.name, group.lock_weight) for group in mesh.vertex_groups
        ]),
        "vertex_group_weights_sha256": data_digest([
            sorted((group.group, group.weight) for group in vertex.groups)
            for vertex in mesh.data.vertices
        ]),
        "mesh_uv_sha256": data_digest({
            "active_index": mesh.data.uv_layers.active_index,
            "layers": [(layer.name, layer.active_render, [list(loop.uv) for loop in layer.data])
                       for layer in mesh.data.uv_layers],
        }),
        "material_backface_culling_sha256": data_digest([
            (material.name, material.use_backface_culling)
            for material in sorted(bpy.data.materials, key=lambda item: item.name)
        ]),
    }


def require_preservation(actual, expected):
    changed = [name for name, digest in actual.items() if expected.get(name) != digest]
    if changed:
        raise AssertionError("Source preservation check failed: " + ", ".join(changed))


def used_images():
    return {node.image for material in bpy.data.materials if material.node_tree
            for node in material.node_tree.nodes
            if node.type == "TEX_IMAGE" and node.image}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=".local/input")
    parser.add_argument("--output", default=".local/phase-01")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    evidence = ROOT / "context/evidence/phase-01.json"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text('{"status": "PREPARING"}\n', encoding="utf-8")
    (evidence.parent / "phase-01-verification.json").write_text(
        '{"status": "NOT_RUN", "reason": "Preparation started"}\n', encoding="utf-8")
    inputs, output = local_path(args.input), local_path(args.output)
    hashes = {name: sha256(inputs / name) for name in EXPECTED}
    if hashes != EXPECTED:
        raise ValueError("Input asset hashes differ from the inspected source")
    source = ROOT / ".local/source"
    with zipfile.ZipFile(inputs / "stitch.zip") as archive:
        for member in MEMBERS:
            target = source / member
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
    output.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(source / MEMBERS[0]), load_ui=False, use_scripts=False)
    original_version = list(bpy.data.version)
    mesh = bpy.data.objects["Stitch_Mesh"]
    rig = bpy.data.objects["Stitch_Armature"]
    source_digests = preservation_digests(mesh, rig)
    deform_names = {b.name for b in rig.data.bones if b.use_deform}
    deform_groups = {g.index for g in mesh.vertex_groups if g.name in deform_names}
    unweighted = sum(sum(g.weight for g in v.groups if g.group in deform_groups) <= 1e-6
                     for v in mesh.data.vertices)
    if unweighted:
        raise ValueError(f"Source contains {unweighted} unweighted vertices")

    # Old files can retain image references outside shader nodes (for example UV editors).
    for image in bpy.data.images:
        if ".png" in image.name:
            texture = source / "textures" / (image.name.split(".png")[0] + ".png")
            if texture.is_file():
                image.filepath = str(texture)
                image.reload()
    for material in bpy.data.materials:
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.type == "TEX_IMAGE" and node.image:
                    name = node.image.name.split(".png")[0] + ".png"
                    texture = source / "textures" / name
                    if not texture.is_file():
                        raise FileNotFoundError(name)
                    node.image = bpy.data.images.load(str(texture), check_existing=True)
    images = used_images()
    for image in list(bpy.data.images):
        if image not in images and image.users == 0:
            bpy.data.images.remove(image)
    for modifier in mesh.modifiers:
        if modifier.type == "SOLIDIFY":
            modifier.show_render = False
            modifier.show_viewport = False

    scene = bpy.context.scene
    scene.frame_set(1)
    bpy.context.view_layer.update()
    evaluated = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    corners = [evaluated.matrix_world @ Vector(v) for v in evaluated.bound_box]
    low = Vector(tuple(min(v[i] for v in corners) for i in range(3)))
    high = Vector(tuple(max(v[i] for v in corners) for i in range(3)))
    center = (low + high) / 2
    height = high.z - low.z
    camera_data = bpy.data.cameras.new("CompanionCamera")
    camera = bpy.data.objects.new("CompanionCamera", camera_data)
    scene.collection.objects.link(camera)
    camera.location = center + Vector((height * 0.18, -height * 2.7, height * 0.04))
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = max(height, high.x - low.x) * 1.22
    scene.camera = camera
    for name, offset, power, size in [
        ("Key", (-1.1, -1.5, 1.7), 70, 1.3),
        ("Fill", (1.2, -0.8, 0.8), 30, 1.4),
        ("Rim", (0.2, 1.2, 1.5), 45, 1.0),
    ]:
        light_data = bpy.data.lights.new(name, "AREA")
        light_data.energy = power * height * height
        light_data.shape = "DISK"
        light_data.size = size * height
        light = bpy.data.objects.new(name, light_data)
        scene.collection.objects.link(light)
        light.location = center + Vector(offset) * height
        light.rotation_euler = (center - light.location).to_track_quat("-Z", "Y").to_euler()
    world = bpy.data.worlds.new("CompanionWorld")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.16, 0.16, 0.16, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.35
    scene.world = world
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.render.resolution_x = scene.render.resolution_y = 768
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.view_transform = "Standard"
    scene.render.fps = 24
    bpy.ops.file.pack_all()
    for image in images:
        if not image.packed_file or min(image.size) == 0:
            raise ValueError(f"Texture is missing or unpacked: {image.name}")
        image.filepath = "//textures/" + image.name
    scene.frame_set(20)
    scene.render.filepath = "//frame_20.png"
    stage = output / "stitch-stage.blend"
    require_preservation(preservation_digests(mesh, rig), source_digests)
    bpy.ops.wm.save_as_mainfile(filepath=str(stage), compress=True)
    stage_hash = sha256(stage)
    report = {
        "phase": "01", "status": "PREPARED", "blender_version": bpy.app.version_string,
        "local_input": inputs.relative_to(ROOT).as_posix(),
        "source_blend_version": original_version, "source_sha256": hashes,
        "vertices": len(mesh.data.vertices), "bones": len(rig.data.bones),
        "unweighted_vertices": unweighted,
        **source_digests,
        "shape_keys": [k.name for k in mesh.data.shape_keys.key_blocks] if mesh.data.shape_keys else [],
        "constraints": {b.name: [c.type for c in b.constraints] for b in rig.pose.bones if b.constraints},
        "actions": [{"name": a.name, "range": list(a.frame_range)} for a in bpy.data.actions],
        "fps": scene.render.fps, "new_animation_created": False,
        "used_images": [{"name": i.name, "size": list(i.size), "packed": bool(i.packed_file)}
                        for i in sorted(images, key=lambda x: x.name)],
        "outline": "Legacy Solidify preserved but disabled in viewport and render",
        "camera": "Orthographic, slightly off center; candidate, not visual approval",
        "render": {"size": [768, 768], "samples": 32, "engine": "CYCLES", "alpha": True},
        "local_stage": stage.relative_to(ROOT).as_posix(),
        "stage_sha256": stage_hash,
        "rendered_frames": [],
        "limitations": ["No new animation or timing evaluation", "No desktop runtime or target-PC validation",
                        "Preservation digests do not cover every constraint, shader or action keyframe property"],
    }
    for frame in RENDER_FRAMES:
        scene.frame_set(frame)
        frame_path = output / f"frame_{frame:02}.png"
        scene.render.filepath = str(frame_path)
        bpy.ops.render.render(write_still=True)
        if not frame_path.is_file() or frame_path.stat().st_size == 0:
            raise RuntimeError(f"Expected rendered frame is missing or empty: {frame_path.name}")
        report["rendered_frames"].append(frame)
    if sha256(stage) != stage_hash:
        raise AssertionError("Saved stage changed after preparation")
    if {name: sha256(inputs / name) for name in EXPECTED} != hashes:
        raise AssertionError("Input assets changed")
    evidence.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("PHASE_01_PREPARED " + json.dumps(report))


if __name__ == "__main__":
    main()
