# Current handoff

**Active phase:** None. Optional Phase 07 is complete with local Windows 10 user acceptance on 2026-09-20. The user tested and liked the installed update: viewer-left hand makes peace and viewer-right hand waves. General use was reported working. Do not repeat completed approval questions.

## Current installed application

- Actual path: `C:/Users/Erdem/Desktop/Hediye/StitchPet.exe`. The former `Stitch - Hediye` path is stale. Desktop `Stitch.lnk` and current-user Startup `Stitch.lnk` already point to the actual Hediye path and were preserved.
- Current EXE SHA-256: `23ba69a8f4c7773f44cbc809c62c567a26f32cafa481aeccdd67a1eadf86d142`. Launched and confirmed visible with tray panel closed; observed PID 3664 may become stale.
- Full previous installed version backed up and all 292 files hash-verified at `.local/phase-07/backup-20260920-103328`. Installed assets/support files: 344 verified against the candidate manifest. Position and size preserved; installer unchanged; Turkish usage note updated.
- Original Phase 03 fallback remains `.local/phase-02/host/`. Older frozen full backup remains `C:/Users/Erdem/Desktop/stitch-desktop-companion-ragdoll-illuzyonsuz`. Never overwrite those fallbacks.
- Recipient liked the original gift and reported it working. This new update has only been installed on the developer's Windows 10 PC, not remotely on the recipient's Windows 11 PC.

## Current behavior

- Viewer-right hand click waves; viewer-left hand click makes the approved peace/V gesture. These are screen sides: rig `.L` waves, `.R` makes peace.
- Body/head non-drag clicks do nothing. Drag remains available from any opaque part. No extra panel commands, facial changes, sounds or physics engine.
- Snapshot hand intent at pointer-down; trigger on non-drag release. Ignore reaction-time presses, repeated/opposite clicks and cancelled presses. Size/alpha/padding/residual carry transform are accounted for.
- Existing gesture finishes while the window follows dragging immediately, then hands over to the carry bank. Keep this accepted transition policy; do not reset the raised hand mid-motion.
- New gesture starts/ends at exact accepted neutral pixels; existing idle/entry/wave/carry banks are unchanged. Complete old asset banks still work in legacy mode for baseline comparisons; partial peace banks are rejected.

## Evidence and reproduction

- [Integration record](evidence/phase-07-hand-integration.json): hand checks 14,580 assertions; baseline 1,941; carry 179,452; tray UI 156. Counts include repeated pixel/state assertions, not independent tests. Packaged singleton/hidden-restore/concurrent-launch checks passed.
- First singleton attempt encountered the already-running old Hediye application and correctly activated it. Located and verified that binary, gracefully closed it, backed it up, and reran successfully. Do not mislabel this as a singleton regression.
- Independent read-only review found no material issues. Its minor partial-bank edge was reproduced, fixed and retested. User-facing mouse acceptance is still distinct from these checks.
- Six-second host/tray observations: about 38-39MiB additional private/working memory; GDI objects stayed at 35. This is not sustained resource certification.
- Research, approvals and motion evidence: [peace gesture record](evidence/peace-gesture-feasibility.md). Approved pose: `.local/peace-preview/peace-pose-v1.blend`. Approved motion: `.local/peace-motion-preview/peace-motion-v1.blend` (60 frames / 24fps).
- Production output already completed: `.local/phase-07/assets/` (400px, 24 samples, 60 PNGs and 96-frame hand regions). Do not rerender to resume. Candidate: `.local/phase-07/trial/`.
- `prepare_peace_assets.py` exports hand regions/renders saved motion; `stage_hand_trial.py` hash-verifies/stages the candidate. Neither deploys. `build_host_spike.ps1 -OutputDirectory .local/phase-07/trial` builds it.
- Focused checks: `check_hand_gestures.ps1`; existing host/carry/UI scripts now accept phase-specific evidence destinations. Preserve historical evidence files. Model assets and renders stay private under ignored `.local/`.

## Next step

Stop at the completed Phase 07 handoff. The installed Hediye application is current. Prepare a clean transfer package if a recipient update is requested; recipient Windows 11 acceptance of this new version remains unobserved. The user explicitly confirmed both hand actions and broad satisfaction, not a separately enumerated all-size/drag/reboot checklist. If a future hit is missed, reproduce against the actual visible hand/size before widening regions.

Keep the installed application synchronized with future fixes after graceful close and verified backup. Updating only the trial does not update Hediye. Preserve the user's position, size, shortcuts and startup preference.
