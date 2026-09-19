# Phase 03 execution review

Status: IN PROGRESS — 2026-09-19. No visual acceptance or phase completion claim.

## Current work

Step 03.1 pose comparison is complete; Steps 03.2/03.3 timing candidates are rendered and ready for moving feedback. New authoring code: `scripts/author_companion_motion.py`; private outputs: `.local/phase-03/`. All work starts from the verified Phase 01 stage and leaves Phase 02 runtime assets unchanged.

The inspected source inventory has unconstrained quaternion controls for arms, hands, head and ears. Eye bones have tracking constraints. Confirm the current stage inventory rather than assuming eyelid or face controls from naming conventions. New posing must preserve leg/foot contacts; successful rendering is not deformation proof.

The first comparison retained the Phase 01 camera/lighting to isolate pose changes. Three 400-pixel renders were inspected: original, soft and tucked. Select **soft** as the working base: arms are lowered with a modest elbow bend/hand curl and mild asymmetry. Reject tucked: at small scale the hands merge into the torso silhouette; original retains the user's stiff open-arm posture. This is an internal artistic selection, not user approval. Source legs were not reposed. The selected stance is not a claim of realistic full-body acting.

The fresh control inventory contains 127 bones and tracked eyes; no named eyelid/lip/jaw control was found by the targeted name scan. This does not prove no facial deformation is possible. No blink or new face rig was added.

## Timing candidates and checks

- Idle candidate: 96 frames at 24 fps (4 seconds), restrained local chest expansion and offset head/ear/arm motion. Frame 97 stores the periodic endpoint for verification and is excluded from playback to avoid repeating the seam frame. This simple periodic cycle needs moving feedback before acceptance.
- Wave candidate: 49 frames at 24 fps (about 2.04 seconds), compared with the Phase 02 73-frame clip. Re-authored lift/return, unequal greeting strokes, wrist lag, hand opening and restrained head/ear response. Same 24 fps; not just globally sped-up playback.
- Current renders are **320-pixel, 6-sample timing drafts**. They are not final 400-pixel assets or the appearance/contrast pass. Frame data and the actual GIF must be reviewed before calling the movement natural.
- The neutral idle pose is also the wave entry/exit. Arbitrary-phase idle interruption is not implemented; do not imply the sequence is ready to drop into the host without transition work.
- `verify_companion_motion.py` reopens the actual saved clips, compares original mesh/rig/weight/UV/material-flag data and original action keys, measures planted toe matrices and the endpoint matrices, and checks a finite-difference idle seam. Initial saved-scene checks PASS; rerun after final wave save so evidence hashes identify delivered scenes.

During preflight, a negative anticipation factor was found in quaternion interpolation. A direct call in installed Blender 5.2.2 reproduced `ValueError: quat.slerp(): interpolation factor must be between 0.0 and 1.0`. The wave's lift factor now stays within the supported interval, with anticipation carried by the head timing. A render-free wave authoring run succeeded and the saved-scene checks passed. The first process completed all 96 idle frames and its idle manifest, then exited with that known error while authoring the old wave code. The corrected wave is rendered separately with `--clip wave`; the failed combined run is not described as a successful full render. The idle implementation is unchanged by the fix.

Fresh saved-scene checks after saving the corrected wave: tracked source fields/action keys match; maximum toe matrix difference is about 1.2e-7; idle frame 97 and wave final frame each match their starts exactly in bone matrices. Idle seam finite-difference discrepancy is about 6.4e-5, below the chosen numeric diagnostic threshold. These measurements establish periodic data, not perceptually natural breathing or fully verified foot/mesh contact. Three idle samples and the raised wave pose were inspected; movement is deliberately small and facial expression remains unchanged.

Tools: `preview_companion_motion.py` validates completion manifests/frame hashes/alpha boundaries and creates private GIF/contact sheets without replacing host assets. The reproducible source and actual checks are the durable record; no additional skill workspace or duplicate planning system is introduced.

## Reproduction

Use the installed Blender 5.2.2 executable with `--background --factory-startup --disable-autoexec --threads 4 --python-exit-code 1`:

- Pose comparison: `--python scripts/author_companion_motion.py -- --mode poses --size 400 --samples 8`.
- Timing candidates: `--python scripts/author_companion_motion.py -- --mode motion --size 320 --samples 6`. `--clip idle` or `--clip wave` limits a retry to the chosen clip. `--no-render` saves authored data only and invalidates that clip's old render manifest.
- Reopen checks: `--python scripts/verify_companion_motion.py`.
- Run `scripts/preview_companion_motion.py` with the local bundled Python containing Pillow/numpy after both manifests exist. This builds private review artifacts; it does not install frames in the native host.

The named pose-study scene is saved at the selected **soft** stance, not the last rejected comparison pose. The original and tucked PNGs remain comparison evidence.

## Rendered checkpoint

The corrected separate wave render exited successfully. All 96 idle and 49 wave frames are present and match their completion-manifest hashes. [Frame checks](phase-03-frame-checks.json) PASS: alpha borders clear, wave first/last pixels identical, idle neutral pixels equal wave entry, and the Phase 02 host's 73-frame sequence/idle still match its baseline. [Saved-scene checks](phase-03-motion-checks.json) PASS with the limits described above. Python syntax and Git whitespace checks passed.

Private artifacts:

- `pose-comparison.png`: original/soft/tucked at 320 display size, with soft selected.
- `idle-wave-review.gif`: the actual 24 fps candidates shown sequentially (idle then wave), light background at native draft 320 pixels and dark background at 240 pixels. GIF delays distribute 40/50 ms to approximate 24 fps. It is a review montage, not a runtime sprite or desktop capture.
- `idle-sheet.png` and `wave-sheet.png`: eight sampled frames per clip, inspected after generation. The sampled hand poses retain visible clearance from the ear; the resting hand stays separate from the torso. Idle movement is restrained; face/expression remains static. This does not establish full moving quality or rule out all between-frame mesh intersections.

Targeted user feedback requested at this checkpoint: (1) whether idle reads as sufficiently alive without being distracting, and (2) whether the revised wave pace/gesture improves on the slow draft. Do not claim final naturalness before that observation. The lighting/outline pass, full 400-pixel quality and arbitrary-idle interruption strategy remain unfinished; retain Phase 03 active. No native host, startup, or dragging-effect changes were made.

## Pending evidence

- Moving idle and improved-wave review.
- Appearance and transition review at supported sizes.
- Fresh preservation, frame-boundary and motion continuity checks for the selected output.
- User observation of moving output before completion.
