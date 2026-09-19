# Current handoff

**Last completed phase:** 03 - Appearance and animation polish, 2026-09-19.

**Status:** Phase 03 COMPLETE; Phase 04 ACTIVE: the user approved the revised carried-toy plan after requesting a full fallback copy. Backup completed and SHA-256 verified before implementation. Godot remains excluded.

**Current cursor:** STOP for visual approval of the tray remote prototype. The user superseded the character-attached toolbar with a panel opened ONLY by clicking the notification-area Stitch icon; independent floating character/animation/drag remain untouched. Research + static design complete: [tray visual checkpoint](evidence/phase-04-tray-visual-prototype.md), private images `.local/phase-04/tray-visual-prototype/`. NO integration authorized until visual approval. Current installed trial remains unchanged at `.local/phase-04/native-trial/StitchPet.exe` / desktop `Stitch - Tasima Denemesi`: 400px carry/release polish plus the old hover toolbar. Exe hash/backup remain in `phase-04-polished-install.json`; PID 27368 may be stale. The latest release fix still needs explicit user feedback. Preserve accepted carry strength and OPEN eyes; no Godot or Phase 05 startup work.

**Preserve:** accepted installed `phase03-appearance-400` at `.local/phase-02/host/StitchPet.exe`. Full fallback: `C:/Users/Erdem/Desktop/stitch-desktop-companion-ragdoll-illuzyonsuz`, 22,666 files SHA-256 verified before changes; see `phase-04-fallback-backup.json`. Treat backup as frozen; work only in this main checkout. Main and backup executable hashes still match accepted installation. The separate trial does not replace that installation. Godot stays excluded. Direct-method Windows rendering and short process measurements exist; physical input, user visual acceptance, arbitrary anatomical grip, sustained resource behavior, production quality, packaging and target Windows 11 remain open.

## Selected appearance and evidence

- Four neutral/wave variants were rendered: baseline, soft lower fill, stronger lower fill and legacy outline. Soft fill improves lower-body separation while retaining shaping. Stronger fill was unnecessarily bright/flat. Legacy outline rendered markedly dark and remains disabled; no root-cause repair is claimed.
- `phase-03-appearance-samples.json`: 24/64-sample static comparisons at 400px, composited on light/dark backgrounds. Mean absolute channel difference around 0.90-1.16/255, p95 around 3-5; outliers remain. This supports a bounded sample choice, not proof of temporal quality.
- `phase-03-motion-checks.json`: reopened appearance scenes preserve original source/action fields, every accepted idle/wave/entry action key and the camera. Feet remain stable; idle periodic endpoint matches; all entry endpoints match expected matrices exactly. Maximum entry toe difference about 2.4e-7.
- `phase-03-runtime-frames.json`: all 237 400px PNG hashes, alpha boundaries and neutral/entry endpoints PASS. All entry starts match sampled idle images. Geometry/camera are unchanged, retaining the measured maximum entry approximation of 0.669px at 400px.
- `phase-03-host-checks.json`: six groups / 1943 assertions PASS with current 400px assets, including all idle click phases, settings/alpha and visible direct-method Windows smoke. Not physical mouse automation or 1943 independent tests.
- `phase-03-host-install.json`: installed executable hash, backup path and settings preservation. Current prior-app backup: `.local/phase-03/host-backup-20260919-152055-087/`. Earlier motion/source backups remain untouched.
- Installed process launch was verified with `motion=phase03-appearance-400 idle=96 wave=45`, 240px size and prior position. PID file may later be stale; inspect the real process/log before future claims. The earlier request to close the old app is resolved; do not ask again for this deployment.

## Private review artifacts and reproduction

The following appearance commands describe the historical Phase 03 baseline. For the current Phase 04 candidate use `render_carry_final.py`, `stage_carry_trial.py --final`, the polished-trial build/checks, then `update_carry_trial.ps1 -Launch`. Do not deploy Phase 04 with the old `update_host_motion.ps1` path, which omits carry assets and launch flags.

Current scenes/PNG manifests: `.local/phase-03/appearance-final/{idle,wave,entries}/`. Review: `appearance-final/supported-sizes-review.gif`, `supported-sizes-neutral.png`, `supported-sizes-wave.png`. These show actual 240/320/400 sizes on light/dark backgrounds. Static outputs were inspected; the user subsequently approved the installed appearance. Historical 320px timing checks/previews remain as earlier evidence, not current runtime assets.

Use Blender 5.2.2 with auto-execution disabled: `render_appearance.py -- --mode production --variant soft --samples 24` loads accepted saved motion and applies appearance only. Completed production render exited successfully; do not rerender it to resume. Verify with `verify_companion_motion.py -- --appearance`; build review with bundled-Python `preview_appearance.py`. Deploy through `update_host_motion.ps1 -Python <Pillow/numpy Python> -Launch`, which targets the appearance-final folder, validates, tests, backs up and preserves settings. Later motion changes require new matching entry and appearance renders before deployment.

## Settled scope and remaining boundaries

Silent offline native C# layered-window host, floating above normal apps; no browser hiding or desktop-shell embedding. Keep the accepted idle/wave and introduce no unrelated gestures. The limited idle polish is accepted: chest +25%, head +20%, same four-second timing. Earlier user observation found no conspicuous jump/stutter when clicking different idle phases. The appearance pass preserves those motion keys; the user subsequently approved its appearance as well.

The active Phase 04 experiment is a bounded authored carry/drag response with ordinary dragging as fallback, not full physics or an engine migration. Phase 03 handoff is complete; research findings now constrain the first experiment. Phase 05 handles startup, packaging, duplicate instances and daily-use checks; recipient Windows 11 acceptance is Phase 06. Exact tray restoration and the covered-body counter remain native integration checklist items.

Official Blender MCP previously worked through the isolated diagnostic stdio client; it is optional for live inspection. Direct scripts/renders are used for repeatability, since hidden viewport capture could be stale. Computer Use desktop capture previously failed; no fresh desktop screenshot proof is claimed. Windows smoke uses app methods and real layered-window calls; physical visual/input acceptance belongs to the user's observations. Keep all model/texture/render assets private under ignored `.local/`.
