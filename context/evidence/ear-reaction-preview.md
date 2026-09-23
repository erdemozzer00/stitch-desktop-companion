# Ear reaction preview — 2026-09-21

## Authorized scope

The user requested a short, cute response for each ear, faster than the hand gestures, and approved the proposed single-ear preview before integration. This checkpoint shows viewer-left only (rig `.R`). No runtime, hit-region, opposite-side, UI or deployment changes.

## Probe and artifacts

- Script: `scripts/preview_ear_motion.py`; review composition: `scripts/review_ear_motion.py`.
- Private source: accepted `.local/phase-03/appearance-final/idle/idle.blend`, opened with scripts disabled. Source SHA-256 stayed unchanged.
- Private output: `.local/ear-motion-preview/ear-motion-v1.blend`, 16 RGBA PNGs at 400px / 16 samples / 24fps.
- Review: `.local/ear-motion-preview/ear-motion-review.gif`, with 400px light and 240px dark views. Neutral pauses between reactions aid review; this is not an integrated idle transition demonstration.
- Ear base folds 13 degrees with a small rearward component; tip follows a frame later with a 9-degree response. A restrained overshoot and 2-degree head tilt return to neutral. These are artistic trial values, not universal animation standards.
- Clip playback lasts 0.667 seconds; complete review loop is 2.17 seconds including neutral pauses.

## Evidence

Saved scene reopened; first/last bone matrices match accepted neutral within 1e-5. All 16 frame hashes verified. RGBA dimensions and alpha bounds checked: no canvas clipping. First/last rendered pixels are identical. GIF fully decoded and total duration verified. Selected frames 1/4/5/8/12/16 visually inspected: viewer-left ear drop/rebound is visible, with no obvious silhouette break in those views. Temporal quality still needs the user's moving review; a contact sheet alone cannot establish it.

The installed `Desktop/Hediye/StitchPet.exe` SHA-256 still matches accepted `23ba69a8f4c7773f44cbc809c62c567a26f32cafa481aeccdd67a1eadf86d142`. No installed assets were edited. No native ear clicks or idle/carry transitions are implemented or validated. Private `checks.json` and `review-checks.json` contain exact numerical/hash evidence.

## Next checkpoint

Show the moving review and wait for feedback on speed, amplitude and character. Only after approval proceed to the opposite side and a bounded integration plan preserving hand clicks, drag intent, alpha click-through and non-interrupting reactions. Do not infer approval from the request to see the preview.

## Approval and integration — 2026-09-21

User approved the moving preview. Mirrored the approved rig-space rotation deltas through the sagittal plane onto the opposite ear; this is not a pixel-flipped character. Both sides rendered at 400px/24 samples, 16 frames each. Saved scenes checked against the accepted idle neutral: maximum endpoint/toe errors left 5.96e-7, right 1.43e-6. All alpha bounds remain inside canvas, and both clips reuse exact accepted neutral endpoint pixels. Inspected paired peak renders: each side folds the intended ear while preserving the character's asymmetry. Paired moving review is private `.local/phase-08/assets/both-ears-review.gif`.

Runtime adds EarLeft/EarRight to the existing reaction selector, using the same four-frame idle entry and no-overlap/carry policy. Total reaction playback is 20 frames / 24fps (0.833s), including entry; authored motion remains 0.667s. Per-idle-frame convex hulls come from ear-weighted control vertices (weight >= .65), plus existing actual sprite alpha gating and inverse carry transform. Hand regions have priority; no face/body click command or UI changes. Complete prior hand-only asset banks still work; any partial ear installation is rejected.

RED: actual ear click failed before runtime changes. GREEN: 16,295 ear assertions across 96 idle phases, 240/320/400px, both sides, actual selected bitmap/frame samples, repeat/opposite presses, no queued press, capture cancellation, resize, immediate drag, carry interruption and residual transform; 14,580 existing hand assertions; 179,452 carry assertions; 156 tray assertions; actual executable duplicate/hidden-restore/concurrent launch test passed. Assertion counts are not independent test cases. Test fixture corrections: drag follow checked before intentional release clamping; expected bitmap uses the same GDI+ Image-to-Bitmap conversion as application loading. Production behavior was not changed to accommodate these fixture errors.

Installed after hash-verifying all 353 previous files in `.local/phase-08/backup-20260921-032739`. Candidate and installation contain 377 verified asset/support files. Updated usage note; position/size, shortcuts, startup and UI preserved. EXE hash and exact measurements: [integration evidence](phase-08-ear-integration.json). Six-second sample observed about 267MiB working set / 263MiB private bytes, GDI 35; compared to the prior separate short sample this is about 23MiB extra, not a controlled or sustained benchmark. 32 new frames are 19.53MiB raw RGBA before native overhead.

Pending: user physically clicks each ear, confirms the intended short reaction, and checks ear dragging and existing hand reactions. Do not claim recipient acceptance of this ear update from the earlier hand update's acceptance.

## Subsequent user acceptance — 2026-09-23

The user reported the ear motion looked slow and briefly requested double speed and overlapping opposite-ear responses, then explicitly withdrew that request and accepted the existing version. Later, after asking whether the ear update was in the desktop gift folder, the user confirmed it works. Optional Phase 08 is closed on that general local user acceptance; it is not a separately observed checklist or recipient Windows 11 acceptance. Keep the installed timing and no-overlap policy. The executable SHA-256 was reverified during nose-smile research and still matches the integration evidence. No runtime or asset changes were made for that research.
