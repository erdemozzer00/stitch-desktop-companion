"""Validate rough frames and assemble private review assets (requires Pillow/numpy)."""
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / ".local/phase-02/wave"
paths = sorted(folder.glob("wave_*.png"))
assert [path.name for path in paths] == [f"wave_{i:04}.png" for i in range(1, 74)], "Incomplete or stale sequence"
render_report = json.loads((folder / "render-report.json").read_text(encoding="utf-8"))
assert render_report["frames"] == len(paths)
if "frame_sha256" in render_report:
    assert render_report["frame_sha256"] == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}, "Frames changed since render completion"
frames = []
boxes = []
for path in paths:
    with Image.open(path) as image:
        assert image.mode == "RGBA" and image.size == (320, 320)
        frame = image.copy()
    alpha = np.asarray(frame)[:, :, 3]
    assert not any(edge.any() for edge in (alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1])), path.name
    assert alpha.max() == 255 and alpha.min() == 0
    frames.append(frame)
    boxes.append(frame.getbbox())
delta = np.abs(np.asarray(frames[0]).astype(int) - np.asarray(frames[-1]).astype(int))
assert np.any(np.asarray(frames[0]) != np.asarray(frames[24])), "The sequence is static"

# GIF backgrounds are deliberately opaque: this is a review board, not the runtime asset.
preview = []
for frame in frames:
    board = Image.new("RGB", (640, 360), "#edf0f2")
    ImageDraw.Draw(board).rectangle((320, 0, 640, 360), fill="#20262e")
    board.paste(frame, (0, 20), frame)
    board.paste(frame, (320, 20), frame)
    preview.append(board)
# GIF stores durations in 10 ms units; distribute 40/50 ms instead of silently speeding up 24 fps.
durations = [(round((i + 1) * 100 / 24) - round(i * 100 / 24)) * 10 for i in range(len(frames))]
preview[0].save(folder / "rough-wave-review.gif", save_all=True, append_images=preview[1:],
                duration=durations, loop=0, optimize=False)
selected = [1, 7, 13, 19, 25, 32, 39, 46, 52, 59, 66, 73]
sheet = Image.new("RGB", (4 * 240, 3 * 268), "#edf0f2")
draw = ImageDraw.Draw(sheet)
for index, frame_number in enumerate(selected):
    x, y = index % 4 * 240, index // 4 * 268
    frame = frames[frame_number - 1].resize((240, 240), Image.Resampling.LANCZOS)
    sheet.paste(frame, (x, y + 24), frame)
    draw.text((x + 12, y + 7), f"Frame {frame_number:02} / 73", fill="#20262e")
sheet.save(folder / "rough-wave-contact-sheet.png")

assets = ROOT / ".local/phase-02/host/assets"
assets.mkdir(parents=True, exist_ok=True)
# Never silently retain obsolete wave frames from a different sequence.
unexpected = {p.name for p in assets.glob("wave_*.png")} - {p.name for p in paths}
assert not unexpected, f"Unexpected runtime frames: {unexpected}"
for path in paths:
    shutil.copy2(path, assets / path.name)
shutil.copy2(paths[0], assets / "idle.png")
assert (assets / "idle.png").read_bytes() == paths[0].read_bytes()
report = {"status": "PASS", "frames": len(frames), "fps": 24, "rgba_size": [320, 320],
          "all_alpha_borders_clear": True, "non_static_sequence": True,
          "first_last_max_channel_difference": int(delta.max()),
          "first_last_mean_channel_difference": float(delta.mean()),
          "idle_matches_first_frame": True,
          "sequence_sha256": hashlib.sha256(b"".join(p.read_bytes() for p in paths)).hexdigest(),
          "bounds_union": [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)],
          "limits": "Image/data checks only. Not motion-quality, native interaction or recipient acceptance."}
(ROOT / "context/evidence/phase-02-frames.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report))
