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
