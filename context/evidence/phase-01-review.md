# Phase 01 review — 2026-09-18

## Result

Source verification and reproducible preparation are complete. Confidence is
high for the structural checks below. This does not establish natural animation
quality, desktop behavior, or compatibility with the recipient's PC.

## Executed checks

- Ran `scripts/prepare_stage.py` in Blender 5.2.2 LTS with auto-execution disabled,
  four CPU threads and a nonzero exit code on Python failure. The final run exited 0.
- Ran `scripts/verify_stage.py` in a fresh Blender process. It reopened the saved
  stage and exited 0 with `status: PASS`.
- Verified 14,886 source vertices and 127 bones. No source vertex lacked a
  positive weight to a deform bone. This is not a deformation-quality test.
- Compared mesh-coordinate and bone-rest-matrix digests before preparation and
  after reopening the stage. They match. Existing action names/ranges match;
  the verifier does not compare every animation keyframe.
- Verified two used 4096 x 4096 texture images are packed and load after reopening.
- Verified local input ZIP and GLB hashes match the inspected originals.
- Rendered source action frames 1, 20 and 40 to 768 x 768 RGBA PNGs. All have
  transparent borders and fully opaque character pixels; none reaches the frame edge.
- Viewed the three-frame inspection board and 180 px assets composited against
  light and dark backgrounds. This is a still-image review, not a timing review.
- Verified GitHub account `erdemozzer00` (user id 248475779), repository owner
  `erdemozzer00`, repository id 1375139754 and visibility `public` through the
  GitHub connector. The browser's created-repository page also showed Public.

## Visual observations

- Textures load without the missing-image magenta appearance. Ears, hands and
  feet fit inside the selected camera framing in all three inspected samples.
- The slight front angle keeps the face and both hands readable at the larger
  inspection size. This camera remains a candidate rather than approved art.
- At 180 px, the lower body and feet blend into the dark test background.
  Improve their separation in Phase 03; do not call the current lighting final.
- The original rest/action pose holds the arms away from the torso. Review a
  relaxed idle pose and shoulder deformation during the Phase 02 motion spike.
- The Cycles inspection without the legacy outline shell avoided the earlier
  darkening. The modifier remains present but disabled; final outline treatment
  is open. Disabling it is not claimed as the final artistic solution.

## Resolved preparation issues

- Packing initially found an obsolete texture path retained outside material
  shader nodes. Relinking all matching supplied PNG datablocks resolved it.
- Independent script review found that an empty image set could pass `all()`,
  custom input paths were not honored by verification, and stale PASS evidence
  could survive a failed rerun. The final scripts check the expected nonempty
  image inventory, record the input path, and invalidate old success first.
- Blender reported a legacy UI-region migration warning and a deprecation notice
  for `World.use_nodes`. Neither caused the final run to fail. Recheck the API
  before a future Blender major-version upgrade.

## Local artifacts

The packed Blender file, source copies, render samples, inspection board and
raw logs are in `.local/`, excluded from public Git. Original downloads were
not edited. The public repository contains metadata and original scripts only.

## Documentation consulted

- [Blender file packing API](https://docs.blender.org/api/current/bpy.ops.file.html)
- [Blender file-saving API](https://docs.blender.org/api/current/bpy.ops.wm.html)
- [Blender image color modes](https://docs.blender.org/api/current/bpy_types_enum_items/image_color_mode_items.html)

These APIs were checked through Context7 and exercised with installed Blender.
Source attribution and licensing observations are in `THIRD_PARTY.md`.
