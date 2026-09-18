# Stitch Desktop Companion

A project for a personal Windows 11 desktop companion using a supplied Stitch model. The planned first version is silent, stays on the visible desktop behind application windows, reacts to clicks, and can be dragged into place.

**Status:** Phase 01 is complete. Phase 02 is next. This repository contains verified preparation and evidence; it does not yet contain a working desktop companion or an approved new animation.

Verified public repository: [erdemozzer00/stitch-desktop-companion](https://github.com/erdemozzer00/stitch-desktop-companion).

## Scope and progress

- [Project decisions](context/PROJECT.md)
- [Six-phase roadmap](context/ROADMAP.md)
- [Current phase and handoff](context/ACTIVE.md)
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
