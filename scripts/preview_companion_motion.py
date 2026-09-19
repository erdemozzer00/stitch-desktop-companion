"""Validate authored PNG sequences and build a private moving review, no host mutation."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".local/phase-03"
pose_board = Image.new("RGB", (960, 354), "#eef0f2")
pose_draw = ImageDraw.Draw(pose_board)
for i, name in enumerate(("original", "soft", "tucked")):
    with Image.open(OUTPUT / ("pose_" + name + ".png")) as source:
        pose = source.resize((320,320), Image.Resampling.LANCZOS)
        pose_board.paste(pose, (i*320,34), pose)
        pose_draw.text((i*320+16,12), name.upper() + (" - SELECTED" if name == "soft" else ""), fill="#20262e")
pose_board.save(OUTPUT / "pose-comparison.png")
frames = {}
report = {"status": "PASS", "clips": {}}
for clip in ("idle", "wave"):
    folder = OUTPUT / clip
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    paths = [folder / name for name in manifest["frame_sha256"]]
    assert set(p.name for p in folder.glob(clip + "_*.png")) == set(manifest["frame_sha256"])
    frames[clip] = []
    for path in paths:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest["frame_sha256"][path.name]
        with Image.open(path) as image:
            assert image.mode == "RGBA" and image.size == (manifest["size"],) * 2
            alpha = np.asarray(image)[:, :, 3]
            assert not any(edge.any() for edge in (alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]))
            frames[clip].append(image.copy())
    report["clips"][clip] = {"frames": len(paths), "size": manifest["size"], "fps": manifest["fps"],
                              "manifest_hashes_match": True, "alpha_borders_clear": True}
assert np.array_equal(np.asarray(frames["idle"][0]), np.asarray(frames["wave"][0]))
assert np.array_equal(np.asarray(frames["wave"][0]), np.asarray(frames["wave"][-1]))

def board(frame, label):
    result = Image.new("RGB", (800, 452), "#eef0f2")
    draw = ImageDraw.Draw(result)
    draw.rectangle((400, 0, 800, 452), fill="#20262e")
    draw.text((16, 10), label + " | TIMING DRAFT", fill="#20262e")
    draw.text((416, 10), "240 px | dark background", fill="#eef0f2")
    # Keep original 320 pixels rather than upscale the draft to 400.
    result.paste(frame, (40, 90), frame)
    small = frame.resize((240,240), Image.Resampling.LANCZOS)
    result.paste(small, (480, 160), small)
    return result

combined = [board(f, "IDLE") for f in frames["idle"]] + [board(f, "WAVE") for f in frames["wave"]]
durations = [(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(combined))]
combined[0].save(OUTPUT / "idle-wave-review.gif", save_all=True, append_images=combined[1:],
                 duration=durations, loop=0, optimize=False)
for clip in frames:
    indices = [round(i*(len(frames[clip])-1)/7) for i in range(8)]
    sheet = Image.new("RGB", (960, 530), "#eef0f2")
    draw = ImageDraw.Draw(sheet)
    for position, index in enumerate(indices):
        x,y = position%4*240, position//4*265
        pic = frames[clip][index].resize((240,240), Image.Resampling.LANCZOS)
        draw.text((x+10,y+5), f"{clip} {index+1}", fill="#20262e")
        sheet.paste(pic, (x,y+25), pic)
    sheet.save(OUTPUT / (clip + "-sheet.png"))
report["wave_endpoints_pixel_identical"] = True
report["idle_entry_matches_wave_entry"] = True
baseline = json.loads((ROOT / "context/evidence/phase-02-frames.json").read_text(encoding="utf-8"))
host_assets = ROOT / ".local/phase-02/host/assets"
host_frames = sorted(host_assets.glob("wave_*.png"))
assert len(host_frames) == baseline["frames"]
assert hashlib.sha256(b"".join(p.read_bytes() for p in host_frames)).hexdigest() == baseline["sequence_sha256"]
assert (host_assets / "idle.png").read_bytes() == host_frames[0].read_bytes()
report["phase_02_host_assets_still_match_baseline"] = True
report["limits"] = "Timing drafts at 320 pixels, not final 400-pixel assets or visual approval; host untouched."
(ROOT / "context/evidence/phase-03-frame-checks.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report))
