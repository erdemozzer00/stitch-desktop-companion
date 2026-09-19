# Stitch Desktop Companion

A project for a personal Windows 11 desktop companion using a supplied Stitch model. The first version is a silent floating character above normal windows, reacts to clicks, and can be dragged into place. The former desktop-only requirement was withdrawn on 2026-09-18.

**Status:** Phases 01–02 are complete as preparation/feasibility work. Phase 03's approved plan is ready; new animation production has not started. The order is relaxed stance/idle, improved wave, then a bounded drag-reaction trial in Phase 04. This is not a finished companion or approved animation; target-PC and release acceptance remain open.

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

`./scripts/build_host_spike.ps1 -Probe` compiles the Phase 02 prototype using the installed .NET Framework compiler and opens an interactive test panel. Omit `-Probe` to build only. The executable and private rendered assets stay under `.local/phase-02/host/`. This is a Windows-only experiment, not an installer. It does not register startup or change the wallpaper. Right-click the character or its tray icon for size, hide, restore and exit; double-click the tray icon to restore.

The local executable accepts `--preview` for a single automatic reaction on launch. Close an existing instance before launching/rebuilding: duplicate-instance prevention is not implemented in this spike. Ordinary idle is still a static pose; an animated idle and final motion polish are later work.

See [Phase 02 evidence](context/evidence/phase-02-review.md) for the distinction between native input observations, callback tests, animation review and deferred recipient acceptance.

Run `./scripts/check_host_spike.ps1` for the bounded host component checks. These use the real rendering/settings/hidden-state code without visible windows or input injection; they do not prove native click-through, menu/tray usability or animation quality. The manual checklist and current local runtime state are recorded in the Phase 02 evidence and handoff.
