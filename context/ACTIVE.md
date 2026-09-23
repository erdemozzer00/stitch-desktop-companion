# Current handoff

**Active phase:** Optional 09, approved smile integrated and installed locally on 2026-09-23; physical user acceptance pending. The user approved v4 with "uyuyor"; do not repeat visual approval. Closed eyes apply to this reaction only; accepted carry remains open-eyed. See [integration](evidence/phase-09-smile-integration.json) and [preview/history](evidence/nose-smile-preview.md).

## Current installed application

- Actual executable: `C:/Users/Erdem/Desktop/Hediye/StitchPet.exe`.
- SHA-256: `c07c9fbbe13d6a25a9859adb4ac46c1ef0ff2ff495e144d474da2a4d0b442812`. Installed and launched on 2026-09-23, observed PID 18376 may become stale. Tray panel remains closed on startup.
- Previous accepted ear-enabled gift: `.local/phase-09/backup-20260923-180927`, all 386 files hash-verified. Current installation has 406 verified asset/support files; accepted banks retained byte-for-byte. Position/size and shortcut state preserved at installation, Turkish usage note updated. User movement after launch is expected to change position.txt.
- Previous hand-gesture application: `.local/phase-08/backup-20260921-032739`, all 353 files hash-verified. 377 candidate asset/support files installed and hash-verified. Position, size, shortcuts and startup preserved; Turkish usage note updated.
- On 2026-09-23 the current-user Startup `Stitch.lnk` still targets Hediye; the desktop `Stitch.lnk` is absent. Do not assume why or silently recreate it. The executable is available directly in Hediye. `Stitch - Hediye` is a stale path.
- Preserve older `.local/phase-07/backup-20260920-103328`, `.local/phase-02/host/` and frozen `Desktop/stitch-desktop-companion-ragdoll-illuzyonsuz` fallbacks.

## Behavior

- Viewer-right hand waves; viewer-left hand makes peace. Each ear click selects that ear's quick fold/rebound. Nose click smiles with soft full eye closure; other face/body clicks do nothing. Any opaque part can be dragged.
- Smile: 28 authored frames / 24fps plus four existing entry frames = 1.333 seconds total. The 301-vertex nose component is projected to a convex hull for each of 96 idle frames. Existing hand/ear priority, alpha gating and inverse carry mapping apply.
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

The user accepted the current ear behavior and subsequently confirmed the installed ear update works (2026-09-23). The intermediate requests for double speed and overlapping ear reactions were withdrawn; do not implement them or repeat acceptance questions. This is general local user acceptance, not a separately observed regression checklist. Recipient Windows 11 acceptance of this ear update remains separate; the earlier report covers the hand update only.

Ask for physical feedback on installed nose click and nose dragging; keep hand/ear behavior intact. The smile checks (36,918 assertions), existing ear/hand/carry/tray suites and actual duplicate-launch check passed; these are repeated state/pixel/direct-method assertions, not independent cases or physical user acceptance. Production `.local/phase-09/assets` and verified `.local/phase-09/trial` are complete; do not rerender to resume. `prepare_smile_assets.py`, `stage_smile_trial.py`, `check_smile_gesture.ps1` reproduce the work. `install_smile_update.ps1` intentionally requires the previous ear EXE hash; do not blindly rerun it on this updated package. Recipient acceptance remains separate.

Six-second sequential observations using the same host and peace gesture: current roughly 285MiB working set / 281MiB private bytes, about 17MiB/18MiB above the prior asset bank; GDI 35. This is a short memory observation, not a sustained benchmark or smile-specific CPU measurement. No UI change, full facial rig, Tripo replacement or Godot.

Keep installed Hediye synchronized with future fixes after graceful close and verified backup. Preserve position, size, shortcuts and startup. Do not silently add more features.
