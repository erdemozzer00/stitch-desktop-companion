# Current handoff

**Active phase:** Optional 08, integrated ear reactions installed locally; physical mouse acceptance pending. User approved the viewer-left moving preview on 2026-09-21. Do not repeat preview approval. Phase 07 hand gestures work locally and on the recipient computer by user report.

## Current installed application

- Actual executable: `C:/Users/Erdem/Desktop/Hediye/StitchPet.exe`.
- SHA-256: `9560de22be8a5b61a634997fbd5a0b3cfc8318663a9cc1f05059a741643cb360`. Installed and launched with tray panel closed on 2026-09-21; observed PID 9736 may be stale.
- Previous hand-gesture application: `.local/phase-08/backup-20260921-032739`, all 353 files hash-verified. 377 candidate asset/support files installed and hash-verified. Position, size, shortcuts and startup preserved; Turkish usage note updated.
- On 2026-09-23 the current-user Startup `Stitch.lnk` still targets Hediye; the desktop `Stitch.lnk` is absent. Do not assume why or silently recreate it. The executable is available directly in Hediye. `Stitch - Hediye` is a stale path.
- Preserve older `.local/phase-07/backup-20260920-103328`, `.local/phase-02/host/` and frozen `Desktop/stitch-desktop-companion-ragdoll-illuzyonsuz` fallbacks.

## Behavior

- Viewer-right hand waves; viewer-left hand makes peace. Each ear click selects that ear's quick fold/rebound. Face/body clicks do nothing; any opaque part can be dragged.
- Ear authored motion: 16 frames / 24fps, plus four existing entry frames = 0.833s total. Both return to exact accepted neutral pixels.
- Press intent starts on non-drag release; no overlapping/restarted/queued reactions. Existing immediate pointer following, carry interruption and residual-transform mapping preserved.
- Both ear regions use per-idle-frame projected ear hulls plus sprite alpha. Existing hand regions retain priority. UI, accepted hand/carry banks and model appearance are unchanged.

## Evidence and reproduction

- [Ear integration](evidence/phase-08-ear-integration.json), [motion and checkpoints](evidence/ear-reaction-preview.md).
- Ear assertions 16,295; existing hands 14,580; carry 179,452; tray 156; packaged singleton checks passed. These are repeated state/pixel assertions, not independent cases. Native direct-method checks do not replace physical user feedback.
- Both saved Blender scenes checked: endpoint/toe max error < 1.5e-6; no alpha clipping; exact neutral image endpoints. Source hashes preserved.
- `.local/phase-08/assets/`: final 24-sample PNG banks, ear hull CSV, saved scenes and manifest. `.local/phase-08/trial/`: verified candidate and private test outputs. Never transfer the entire trial directory or publish model/render assets.
- `prepare_ear_assets.py` produces both sides; `stage_ear_trial.py` verifies accepted and new assets; `check_ear_gestures.ps1` checks native routing. Production render is complete; do not rerender just to resume.
- Six-second host observation: about 267MiB working set, 263MiB private bytes, GDI 35. No sustained benchmark claim.

## Next step

Ask for physical ear-click acceptance on the updated installed app: each ear reacts on its own side, ear dragging does not trigger the reaction, both hand gestures still work. Record feedback before closing Phase 08. Recipient Windows 11 acceptance of this ear update remains separate; the earlier report covers the hand update only.

Keep installed Hediye synchronized with future fixes after graceful close and verified backup. Preserve position, size, shortcuts and startup. Do not silently add more features.
