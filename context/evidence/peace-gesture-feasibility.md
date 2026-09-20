# Optional hand-specific peace gesture — feasibility

Date: 2026-09-20. Inspected code: `443906ed3d5c842184118dcc7daefe9d46e69b29`.

## Request and current boundary

The user reports that the gift works and the recipient likes it. This is recipient feedback, not direct observation of Windows 11, reboot, sleep/resume or Explorer-restart tests.

The new request is discussion/research: clicking the currently waving hand should wave; clicking the other hand should make a two-finger peace/V sign inspired by the supplied hamster meme. No implementation, new pose render or deployment is approved by this feasibility discussion. Preserve the delivered gift and its accepted motion.

## Research

- The image circulates under [Hamster peace sign](https://imgflip.com/memetemplate/412284803/Hamster-peace-sign).
- A [2019 user post](https://www.reddit.com/r/memes/comments/d0lawm/shh_be_cool/) uses the gesture for posing calmly/coolly when a roller-coaster camera approaches. This is evidence of one use, not a universal meaning or proof of the original creator.
- Original creator/first publication were not reliably established. For this application, translate the visible pose and its restrained, playful character; do not reproduce the hamster or add unrelated expressions.

## Source and Blender inspection

Opened accepted `appearance-final/idle/idle.blend` and `wave/wave.blend` with Blender 5.2.2, background mode and file auto-execution disabled. No scene was saved and no animation was changed. Private report and inspection script: `.local/peace-feasibility/`.

- Both hands have independently weighted `Finger_A/B/C`, `FingerTip_A/B/C`, `KnuckleThumb`, `Thumb_A/B` and thumbnail bones. Inspected finger/thumb pose bones have no constraints. This supports posing two extended fingers with the remaining finger/thumb folded; it does not prove deformation or visual quality.
- Current wave animates rig `.L`, which projects on the viewer's RIGHT. The other hand is rig `.R`, on the viewer's LEFT. Use screen-side language with the user; do not reverse the existing accepted wave because of anatomical naming.
- On the 400px canvas, idle wrist heads are approximately x=260 (.L) and x=137 (.R). The raised wave wrist is approximately x=288 at frame 20. Idle frames 1/25/49/73 and wave frames 1/20/32 were inspected. These samples do not establish bounds for every frame or visible mesh masks.
- Existing 240/320/400 wave review was inspected. Small hand size and projected finger overlap are the principal visual risks. Need a pose preview at actual supported sizes before promising a readable V sign.

## Runtime assessment and proposed behavior

`PetSpike.cs` already distinguishes click from drag. `PointerUp()` currently calls `React()` for every non-drag opaque-character click. No hand-specific regions currently exist. `MotionPlayback` and frame selection currently assume one wave clip and its fixed duration; adding the peace clip needs a small explicit reaction selection and duration change, not only two rectangles.

Recommended contract (proposal, not implemented):

- Viewer-right hand: existing wave. Viewer-left hand: new peace gesture.
- Head/body non-drag clicks: no greeting. All existing opaque-character drag starts remain available.
- Resolve the hand from the actually displayed frame at pointer-down, retain that intent for the press, and trigger only on a non-drag release. Cancel it when dragging or capture loss occurs.
- Use a forgiving, bounded palm/hand region, not an individual fingertip or a whole half of the character. Preserve transparent desktop click-through; do not enlarge the native hit area into the empty canvas.
- Account for canvas padding, current size, and residual carry rotation/offset when mapping a click back to the sprite. Use frame-aware hand data or validated bounds over all eligible frames; bone head coordinates alone are not usable hit masks.
- Preserve the no-overlap policy: clicks during a reaction do not interrupt, restart or queue another gesture. A gesture in progress can finish while the window follows a drag immediately, then transition into the carry bank, consistent with the existing wave policy. Check the resulting delay visually for the new clip.
- Reuse the existing idle-to-neutral entry bank only if the new clip starts at the exact accepted neutral pose; return to that same pose. This avoids duplicating entry assets unnecessarily.

## Proposed next checkpoint

First preview a modest raised-hand V pose, palm facing the viewer, with the other finger and thumb folded. Keep camera, materials, model proportions, eyes and accepted wave unchanged. Review silhouette, finger separation, intersections and readability at 240/320/400px on light/dark backgrounds. Then author the short raise/hold/return motion and review transitions before host integration. Keep the delivered build untouched during the experiment.

Confidence: high that the current rig and sprite host can support the feature; medium for final small-size visual quality until the actual pose is rendered. No new engine, real-time skeleton, AI service or toolchain addition is indicated.

## Authorized static checkpoint — 2026-09-20

The user subsequently approved continuing with the proposed static preview. The earlier research-only boundary above is historical; runtime integration remains a later step after visual review.

- Created eight inexpensive private pose studies; rejected wrist angles that put the fingers into the face silhouette or pointed them sideways/downward. The selected pose uses a mirrored arm lift from the existing wave, a 15-degree wrist adjustment around camera view direction, two extended fingers, and folded third finger/thumb. No additional facial movement was introduced.
- Selected output: `.local/peace-preview/peace-pose-v1.blend` / `.png`. Final render: 400px, 24 Cycles samples, existing accepted camera/lights/materials. Render script: `scripts/preview_peace_pose.py`.
- Review: `.local/peace-preview/supported-sizes-peace.png`, composed from real render pixels by `scripts/review_peace_pose.py`. Viewed 240/320/400px on light/dark backgrounds and a nearest-neighbor hand detail. The V silhouette is distinguishable in this static review, but the 240px hand is small. User pose feedback is pending. Downscaling uses Pillow Lanczos, not the native GDI+ renderer; this is not native input or animation proof.
- Source idle/wave SHA-256 hashes matched before/after. The script asserted all changed bone basis matrices are on rig `.R` (viewer-left); the accepted opposite hand, facial pose and body controls were not authored anew. No source mesh edits, new runtime frames, hit regions or host changes were made. Alpha-bound check passed without canvas clipping. These checks do not certify all mesh intersections or animated deformation.
- Final PNG SHA-256: `042aa9ab5f64a4d94f4710b0485480714589bbf4fbd923bb66a86979e2516e1f`. Machine-readable private evidence: `manifest.json`, `review-checks.json`, `render-final.log` in the preview folder.
- The historical delivery executable path was absent, so an installed-executable hash comparison was unavailable. No deployment or running-process changes were attempted. Locate the current delivery folder before any future installation.

Next: obtain feedback on this concrete pose, then author the short raise/hold/return clip using the exact accepted neutral endpoint. Check moving continuity and the existing carry-interruption policy before adding hand-specific clicks. Keep the gift and accepted asset banks untouched.

## Static approval and motion checkpoint — 2026-09-20

The user approved the static pose. Motion preview is now authorized and isolated under `.local/peace-motion-preview/`.

Planned motion: 60 frames at 24fps (2.5s), staggered arm/wrist/finger rise, approximately 0.8s full V pose, eased return. Reuse the accepted idle movement in the rest of the body during the hold, then return exactly to phase-zero neutral. No new facial expression or extra gesture. Existing sampled entry bank is reusable because both boundaries match the accepted neutral pose.

Render preview at 400px/16 samples; production quality is not asserted. A 60-frame 400px RGBA bank is approximately 36.6MiB raw before image/GDI overhead. Reuse entry assets; measure actual process memory before deployment rather than treating that estimate as application cost.

Reproduction: Blender background/disabled auto-execution with `scripts/preview_peace_motion.py`, then bundled Python/Pillow with `scripts/review_peace_motion.py`. Do not run either preview script as a deployment procedure. No host changes at this checkpoint.

Motion preview completed successfully. Output `.local/peace-motion-preview/peace-motion-review.gif` shows the accepted idle/entry transition, peace clip and return, on light/dark backgrounds at 320px. The input sequence is 185 frames / 7.71s, including the 2.5s gesture. A 12-frame contact sheet and individual rise/return images were visually inspected. The user must judge moving timing; no native input or carry behavior has been tested for this new gesture.

Verified evidence:

- Saved scene was reopened before checking/rendering; both endpoint world-matrix errors versus accepted idle neutral are approximately 1.07e-6 (tolerance 1e-5). Maximum toe error across all 60 frames is 2.38e-7.
- Independent saved-scene inspection at held frame 24 matches approved hand/arm local matrices within 3.58e-7. Highest arm/wrist per-frame rotation is approximately 8.12 degrees; this is a continuity diagnostic, not a perceptual quality threshold.
- All 60 PNG hashes and alpha bounds checked; none touch the canvas boundary. First/last rendered images are pixel-identical. Source idle and approved static-pose hashes remained unchanged.
- Private reports: `checks.json`, `pose-audit.json`, `review-checks.json`, `render.log`. This is a 16-sample preview, not the final 24-sample asset bank.

Next pending checkpoint: user feedback on rise/hold/return timing. Then add wave/peace selection and hand regions without changing the existing drag behavior; verify carry interruption, repeated clicks, supported sizes and actual memory cost before deployment.

## Motion approval and native integration — 2026-09-20

The user approved the moving preview and explicitly requested continuation. Integrated in `host/PetSpike.cs`: reaction selection, 60-frame peace playback, per-idle-frame hand regions, inverse display-transform mapping and alpha gating, press-time intent and no queued/repeated gestures. New bank absence supports legacy comparisons; any partial peace bank is rejected. Existing carry controller and tray UI implementation are unchanged.

Production: 60 frames at 400px/24 samples; exact accepted neutral images reused at both ends. Hand regions use hand-weighted projected control-mesh vertices with a 3px source-space margin, then current-frame alpha limits actual hits. All 96 idle phases at 240/320/400 were exercised at independent palm fixtures. Existing 237 idle/wave/entry and 45 carry frames hash-match accepted sources. New bank adds approximately 36.6MiB raw pixels; six-second live host observations measured about 38-39MiB added working/private memory with GDI count steady at 35. CPU values are short observations, not a reliable before/after benchmark.

Checks: hand assertions 14,580, baseline 1,941, carry 179,452, UI 156, singleton/hidden-restore/concurrent launch PASS. Initial body-click regression failed as expected before implementation. Existing UI check was updated to click the waving hand because whole-body greeting was deliberately removed. Independent review found no material bug; its partial-bank sentinel edge was reproduced (RED), corrected and verified (GREEN). Scope is direct-method native testing; physical user input and new Windows 11 acceptance remain separate.

Deployment location resolved to `C:/Users/Erdem/Desktop/Hediye`. An already-running original binary explained the first singleton-check failure; it was correctly activated by the candidate instead of a duplicate. Original EXE hash matched the known accepted build. Gracefully closed only that process and verified a full 292-file backup at `.local/phase-07/backup-20260920-103328`. After successful isolated singleton checks, installed the verified candidate and 344 asset/support files, preserved position/size and existing desktop/Startup shortcuts, updated Turkish usage instructions and launched the actual Hediye executable. Current EXE hash and short resource samples are in [integration evidence](phase-07-hand-integration.json). Visible window confirmed; no recipient-machine update performed.

Pending: user's native hand-click/drag feedback. Do not repeat static-pose or animation approval questions. Preserve the new backup and original frozen Phase 03 fallback.
