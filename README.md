# Stitch Desktop Companion

A project for a personal Windows 11 desktop companion using a supplied Stitch model. The first version is a silent floating character above normal windows, reacts to clicks, and can be dragged into place. The former desktop-only requirement was withdrawn on 2026-09-18.

**Status:** Phases 01–03 are complete. The user accepted the native open-eye carried-toy response. The same trial shortcut now opens a 400px carry revision with improved release handoff and the approved detached purple tray remote. Startup shows only the pet and Stitch tray icon; click the icon for size, hide/show and exit. Click the character to wave. Physical review of this installed UI/release polish is pending. Eye closure was cancelled. The original Phase 03 installation and full desktop fallback remain intact. Packaging and target-PC acceptance remain open.

Verified public repository: [erdemozzer00/stitch-desktop-companion](https://github.com/erdemozzer00/stitch-desktop-companion).

## Scope and progress

- [Project decisions](context/PROJECT.md)
- [Six-phase roadmap](context/ROADMAP.md)
- [Current phase and handoff](context/ACTIVE.md)
- [Approved animation execution plan](context/ANIMATION-PLAN.md)
- [Third-party source notes](THIRD_PARTY.md)
- [Phase 01 results and visual review](context/evidence/phase-01-review.md)

Source models, textures, renders, and local working files are excluded from Git. The public repository tracks the implementation, preparation scripts, decisions, and appropriate evidence. The supplied assets are not redistributed here.

## Local preparation

Run from the repository root in PowerShell. The preparation and verification commands below are tested with **Blender 5.2.2 LTS**. Use the full path to that installed Blender executable and place copies of `stitch.zip` and `stitch.glb` under `.local/input/` as described in the source notes. Do not modify the original downloads. Other Blender versions need a fresh verification run.

```powershell
$blender = 'C:\path\to\blender.exe'
& $blender --background --factory-startup --disable-autoexec --threads 4 --python-exit-code 1 --python scripts/prepare_stage.py -- --input .local/input --output .local/phase-01
if ($LASTEXITCODE -ne 0) { throw 'Stage preparation failed.' }
& $blender --background --factory-startup --disable-autoexec --threads 4 --python-exit-code 1 --python scripts/verify_stage.py
if ($LASTEXITCODE -ne 0) { throw 'Stage verification failed.' }
```

Preparation output belongs under `.local/phase-01/`. Verification reopens the saved Blender file and checks the staged data and rendered frames. Review the generated evidence under `context/evidence/`. A successful preparation or verification process alone does not prove animation quality or desktop integration.

The recipient's eventual packaged application is intended to run without Blender installed. Packaging and verification on her computer are later roadmap phases.

## Local Windows prototype

`./scripts/update_host_motion.ps1 -Python <python-with-Pillow-and-numpy> -Launch` validates rendered manifests, compiles/tests a candidate, backs up the installed host and synchronizes approved review motion. When motion changes, rebuild entries with `scripts/author_idle_entries.py`, then produce matching 400px assets with `scripts/render_appearance.py -- --mode production --variant soft --samples 24`. The updater installs from `.local/phase-03/appearance-final/`. The executable stays at `.local/phase-02/host/StitchPet.exe` so existing launch paths remain valid; the historical directory name does not mean old motion. This is a Windows review build, not an installer. Right-click the character or tray icon for size, hide, restore and exit; double-click the tray icon to restore.

The local executable accepts `--preview` for a single automatic reaction or `--probe` for the interactive test panel. Close an existing instance before launching/rebuilding: duplicate-instance prevention is still pending. Current motion is a four-second idle, a short sampled pose-space entry and the accepted 45-frame wave, all at 24 fps. Current assets are rendered at 400px, with 240/320 downsampling and native 400px display. The user approved this installed appearance; Phase 04 integration and later delivery gates remain open.

See [Phase 02 evidence](context/evidence/phase-02-review.md) for the distinction between native input observations, callback tests, animation review and deferred recipient acceptance.

## Isolated carry trial

Phase 04 updated trial lives in `.local/phase-04/native-trial`, separate from the original Phase 03 installation. To reproduce the candidate, render `scripts/render_carry_final.py` in Blender, stage with `scripts/stage_carry_trial.py --final` using Pillow Python, and build to `.local/phase-04/polished-trial`. Run `scripts/check_carry_trial.ps1 -TrialDirectory .local/phase-04/polished-trial` (add `-Live` for Windows smoke/resources) and `scripts/check_polished_ui.ps1`. `scripts/update_carry_trial.ps1 -Launch` validates, gracefully closes only the old trial, backs it up, preserves settings and updates the same trial path/shortcut. `scripts/start_carry_trial.ps1 -DesktopShortcut` opens the clean UI; add `-Probe` only for the diagnostic panel. All carry/idle/wave frames are now 400px; cancelled eye assets remain excluded. User acceptance and final packaging are separate gates.

Run `./scripts/check_host_spike.ps1` for component/pixel/playback checks; add `-Live` for a short visible Windows rendering smoke test using application methods. Neither replaces physical click-through, menu/tray or visual acceptance. Current evidence is recorded under Phase 03 and in `context/ACTIVE.md`.
