# Phase 03 execution review

Status: IN PROGRESS — 2026-09-19. User accepts the idle direction for now and likes the revised wave tempo. Final appearance/transition acceptance and phase completion remain open.

**Latest checkpoint:** user accepted the final 45-frame wave and requested keeping the desktop app current. The native review app is now updated with idle/wave/entry playback; see the final section below. Earlier statements that the host is untouched describe the preceding preview checkpoints only.

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

- Review of the small requested wave retiming; idle direction already accepted for now.
- Appearance and transition review at supported sizes.
- Fresh preservation, frame-boundary and motion continuity checks for the selected output.
- User observation of moving output before completion.

## User feedback and tempo adjustment

The user reviewed the moving draft and reports: idle looks alive for now; the new wave tempo is liked, with a request to make it slightly faster. This supersedes the earlier static/slow Phase 02 assessment for these private candidates. Keep idle unchanged. It is not approval of final lighting, supported-size rendering, arbitrary-idle transitions or native integration.

Retiming choice: resample the same authored 49-frame wave timeline onto 45 frames at 24 fps, preserving relative shoulder/wrist/head/ear timing and entry/exit poses. Playback duration decreases from 2.0417 to 1.875 seconds (8.2% shorter). This is a small refinement of the reviewed gesture, not a substitute for the earlier re-authoring. The original candidate is preserved at `.local/phase-03/wave-v2/`; current output remains `.local/phase-03/wave/`. Only wave is rerendered.

The user also asked whether Blender MCP had been forgotten. It has not: the isolated official MCP trial worked through the diagnostic stdio client, without native Codex tool registration. Hidden viewport capture had returned stale imagery, as recorded in the Phase 02 handoff. Repeatable Blender authoring scripts and direct renders currently supply scene and image evidence. MCP remains available for useful live inspection; there is no need to run it solely to produce this timing adjustment.

Retiming verification completed: the 45-frame render exited 0. Fresh saved-scene checks PASS, with idle scene hash unchanged, source data/action preserved, toe delta about 1.2e-7 and zero endpoint matrix delta. All 141 current PNG frames match their manifests and have clear alpha borders; wave endpoints and neutral idle entry remain pixel-identical. Phase 02 host assets remain unchanged. Regenerated the review GIF and inspected the new eight-frame wave contact sheet: sampled hand/ear clearance remains visible. This is not full moving-quality acceptance. Python syntax and Git whitespace checks also passed. Next: appearance and transition work.

## Accepted motion synchronized to desktop

The user now likes the final wave and explicitly asks that the desktop app stay current. Minimal playback integration was brought forward for Phase 03 live review; Phase 04 carry/drag experimentation remains unstarted. No new approval gate was added.

Idle now loops continuously. Click selects the closest of sixteen sampled idle entry poses, plays a four-frame pose-space bridge to neutral, then the accepted 45-frame wave and resumes idle. All clips use 24 fps, so the bridge adds about 0.167 seconds. Repeat clicks during bridge/wave are ignored; hide stops/resets playback and show resumes idle. No image crossfade or waiting for an entire idle cycle. Normal dragging keeps playing animation.

`author_idle_entries.py` measures screen-space displacement across all evaluated mesh vertices at all 96 idle phases. An eight-bucket experiment failed the chosen one-pixel bound at 400px (1.682px); sixteen buckets reduced the maximum to 0.891px. This is a bounded pose approximation, not exact continuity from every phase or proof that no perceptible hitch exists. The actual rendered entry starts match their sampled idle frames exactly, and all sixteen ends match wave neutral pixels exactly.

`stage_host_motion.py` validates and stages 205 hashed frames with clear alpha boundaries. `update_host_motion.ps1` compiles a separate candidate, runs component plus visible direct-method Windows checks, preserves the old installation and installs the checked candidate at the same historical executable path. Original host backup: `.local/phase-03/host-backup-20260919-142436-346/`. Position/size files were retained; launch log confirms the previous 240px setting and position. Subsequent actual drag events changed the position, so a later position-file hash is correctly different from the backup.

Fresh host evidence: six groups / 1943 assertions PASS, including all 96 click phases, complete wave/idle return, repeat suppression, alpha/resizing, settings and hide/show. The live smoke called app methods and exercised `UpdateLayeredWindow` on Windows 10 through a full idle cycle and wave; it did not inject physical mouse events or visually inspect desktop composition. The updated user app launched with `motion=phase03-v3 idle=96 wave=45` and remains available for user testing. Logs subsequently show real pointer/drag events and five completed reactions from different entry buckets; visual acceptance is still requested from the user.

Limits: render resolution remains 320px, scaled at the 400px setting. Contrast/outline/final rendering and perceptual transition acceptance remain open. Do not claim Phase 03 complete. Every later selected asset revision must be synchronized to the app through the update pipeline, not left only in a preview.

## Research-only checkpoint: improve the existing idle

Latest user observation: updated idle/wave are visible and clicks at different idle phases produce no conspicuous jump or stutter. They request slightly more noticeable idle. Subsequent explicit steering: add quality to the existing animation only; no unrelated/silly gestures. Finish research and report confidence before implementing. No motion code, render assets or running application was changed at this checkpoint.

Primary sources consulted on 2026-09-19:

- [Disney: lead animator Alex Kupershmidt on creating Stitch](https://thewaltdisneycompany.com/news/video-lilo-stitch-626-day-disney-animator/): contrasts the character's soft toy-like design with reptilian movement. This is original-character context, not a prescription to add reptile actions to a quiet desktop idle. The article was read; no frame-by-frame video analysis is claimed.
- [Disney Animation's animation process](https://www.disneyanimation.com/process/animation/): acting relies on timing, staging, weight and coordinated supporting movement. More movement alone is not a quality criterion.
- [Shawn Kelly: moving holds](https://www.animationmentor.com/blog/why-all-animators-need-to-master-the-moving-hold/): retain life while mostly still, avoid both freezing and floating; ambient movement should be purposeful rather than random.
- [Drew Adams: overlap and follow-through](https://www.animationmentor.com/blog/follow-through-and-overlapping-action-the-12-basic-principles-of-animation/): establish the driver first, then proportionate delayed response; avoid torso/head moving as one rigid unit.
- [Disney 2025 production notes](https://lumiere-a.akamaihd.net/v1/documents/lilo_stitch_final_production_notes_bios_7f0b3116.pdf): adaptation-specific design/character context, kept separate from the original stylized-model target. Do not borrow its fur/realism pipeline or claim that it establishes idle angles/timings.

Local inspection: idle already contains periodic chest, head, ear and arm motion with offsets. Therefore this is a readability/polish adjustment, not missing animation. Proposal only: keep the four-second rhythm and relaxed stance, try a modest selective amplitude increase (roughly 20-30% as an artistic starting range, not a research-derived formula), prioritize chest/head readability at 240px, and tune existing ear lag only as needed. Do not uniformly scale every motion channel or add new gestures. Preserve phase-zero neutral so the accepted wave is unchanged. Rebuild and measure entry transitions if idle changes; previous entry-gap evidence cannot be reused for a new idle.

Confidence: high in a bounded polish-first approach; medium in any specific amplitude choice until moving A/B comparison at 240/320/400. If percentages are requested, approximate subjective confidence is 85% for direction and 60-70% for getting the exact amplitude right on the first candidate; these are not measured success probabilities. No production-quality guarantee. Report findings now and await the user's response before implementation.

## Approved limited idle polish (implementation)

The user approved the recommendation and asked that the next roadmap item not be forgotten. Scope is selective chest/head readability only, no new actions. Chest expansion and its existing spine rotation are increased 25%; existing head movement is increased 20%, with the additional offset anchored to zero at the wave neutral. Four-second timing and the original ear/arm channels remain unchanged. The accepted 45-frame wave is not rerendered or re-authored. Prior idle/entry files are preserved in `idle-before-idle-polish/` and `entries-before-idle-polish/`.

Preflight found that the previous sixteen-entry approximation now measured 1.002px at 400px and missed the existing one-pixel diagnostic bound. Twenty-four sampled entry phases reduce this to 0.669px without changing the four-frame entry duration. The native selection formula and its all-96-phase checks are updated together. Entry endpoints reuse the corresponding existing idle/wave PNGs; only the two intermediate poses require rendering. Saved entry scene endpoints and toe matrices will also be checked so copied images do not hide a scene mismatch.

The user closed the running app through its own menu; the close event was observed. Render/check/install are pending at this note. Completion requires refreshed evidence and actual deployment/relaunch, not only a preview.

**Next-step lock:** after this small polish checkpoint, return to Phase 03 Step 03.4: compare restrained lower-body illumination on dark backgrounds and the legacy outline, choose a consistent appearance, then render genuine 400px assets at a justified sample quality. Preserve camera, scale, foot baseline and accepted motions across all clips. Rebuild matching entry renders and update the native app. No new gestures or Phase 04 carry experiment before the Phase 03 handoff.

Completed: idle and 24 entry variants rendered; all 237 frames pass manifest/alpha/neutral checks. Saved-scene verification passes for original source/action, planted toes, periodic idle and all entry endpoints. Entry endpoint matrix error is zero, maximum toe difference about 2.4e-7; projected entry approximation is 0.669px at 400px. Wave scene hash remains `b3454e160a3ef281845a6cc895f1e9abae8bf8458399b87fa66ccabb0355e65f`. The new `preview_idle_polish.py` produces an aligned four-second, 240px side-by-side GIF and a static comparison on light/dark backgrounds. Static inspection retains silhouette; dark lower-body separation remains a next-step defect. Moving aesthetic acceptance is left to the user.

First Windows smoke run failed its exact reaction-count assertion after two real pointer clicks interfered with the scheduled direct-method test. Events showed completed reactions, not an animation exception. The test-only pet now sets `Enabled=false` to isolate the direct-method scenario from physical input; the production pet is unchanged. The rerun passed all six groups / 1943 assertions. The checked candidate was installed and relaunched (`phase03-idle-polish`), preserving settings by hash, with prior app backed up at `.local/phase-03/host-backup-20260919-145239-447/`. This is current developer-PC evidence, not Windows 11 acceptance or completed appearance work.

## Appearance and native-resolution pass

The user likes the limited idle polish and authorized continuation. Preserve the accepted motion and do not add gestures. `render_appearance.py` compares four variants using actual saved idle-neutral and raised-hand wave poses, all at 400px/24 samples: unchanged lighting, soft lower fill, stronger lower fill and the legacy Solidify outline enabled with soft fill.

Select **soft lower fill**: a broad disk area light aimed at the lower torso, scaled to the original character height, improves foot/lower-body separation on dark backgrounds. The stronger alternative brightens/flattens the torso more than needed. The legacy outline comparison substantially darkens the character and is rejected as rendered; do not claim a diagnosed material/root-cause fix. Keep it disabled. Existing camera, material nodes, mesh and primary lights are retained. The selected new light uses energy `12 * height^2`, size `1.6 * height`, with position/target recorded in the script; these are scene-specific artistic choices, not universal lighting rules.

Two representative poses were also rendered at 64 samples. `phase-03-appearance-samples.json` compares composited visible pixels at 24 versus 64 samples on both backgrounds. Mean absolute channel differences are about 0.90-1.16 on a 0-255 scale; 95th-percentile differences about 3-5. Outliers exist (max 46); these aggregate measures do not prove temporal stability. Retain 24 samples with the existing denoiser as the current quality/cost choice, subject to moving review. Static 400px neutral/wave renders and 240px contact comparisons were inspected.

Production candidate is rendering separately under `.local/phase-03/appearance-final/`. It loads accepted baked scenes, applies appearance settings and saves new copies; action data and source-file hashes are checked before/after rendering. Entry endpoints reuse the corresponding new idle/wave images, with new intermediate frames. The final verifier additionally checks reopened idle/wave action keys and camera against the accepted source scenes, plus all entry endpoints and feet. Manifest/staging requires consistent 400px/24-sample/soft-fill output. The prior installed app remains unchanged until rendering and checks finish; final deployment and user appearance review are pending at this note.

Reproduction: Blender `--python scripts/render_appearance.py -- --mode compare` for the four variants; `--mode quality --samples 64` for reference samples; `--mode production --variant soft --samples 24` for the complete appearance candidate. Then `verify_companion_motion.py -- --appearance`, bundled-Python `preview_appearance.py`, and `update_host_motion.ps1 -Python <Pillow/numpy Python> -Launch`. All character output remains private. Phase 03 remains active until its visual handoff; Phase 04 has not started.

Completion of this implementation checkpoint: production render exited 0. Reopened idle, wave and all 24 entry scenes preserve accepted action keys/camera and original source fields. Idle seam and planted-toe diagnostics PASS; entry endpoint matrix discrepancy is zero. All 237 400px images pass manifest hashes, clear borders, neutral equality and entry endpoint checks. Fresh Windows host checks PASS (six groups / 1943 assertions). `phase03-appearance-400` was installed/relaunched at the existing executable path, retaining settings by hash; prior app backup is `.local/phase-03/host-backup-20260919-152055-087/`. Launch log and running process were checked. The prior close request is resolved.

Neutral and raised-hand output were visually inspected at 240/320/400 on both backgrounds; feet/lower-body separation improved without adopting the stronger fill or dark outline. The moving review GIF uses these actual final frames. This is an installed appearance candidate, not final user visual acceptance. A targeted appearance/temporal-artifact question is pending. Keep Phase 03 active until that response is recorded; do not start carry effects yet.
