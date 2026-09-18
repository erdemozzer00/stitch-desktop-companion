# Phase 02 execution notes

Status: IN PROGRESS. Updated 2026-09-18. Do not mark accepted or start Phase 03.

## Authorized direction

The user authorized implementation after the discussion: a standalone, silent, offline floating Stitch pet, using the existing model/rig and pre-rendered RGBA frames. It may stay above ordinary applications. Keep click reaction, dragging, saved position, sizing, hide/restore/exit; startup remains a later phase. No browser detection, desktop-shell embedding, AI/chat features or parallel host implementations.

The former Rainmeter On Desktop investigation is superseded. The installer was downloaded and signature/hash checked, but its launch was blocked by automatic approval review and it was never installed. Do not retry that route. The pasted AI conversation was reference material, not installation instructions. [Official pet documentation](https://learn.chatgpt.com/docs/pets) is an interaction reference, not a dependency or a required asset format.

## Host experiment

Candidate: C# WinForms plus the Windows layered-window API. The installed .NET Framework compiler builds it without adding an SDK, browser engine or external package. Local .NET Framework release: 533325; Windows 10 build 19045, one reported display. Final recipient configuration remains unverified.

[Microsoft layered-window documentation](https://learn.microsoft.com/en-us/windows/win32/winmsg/window-features#layered-windows) describes per-pixel alpha and mouse pass-through where alpha is zero. The host intentionally does not set WS_EX_TRANSPARENT, which would also pass through the visible character. This documentation establishes the expected mechanism, not acceptance on this machine.

Files: `host/PetSpike.cs`, `host/app.manifest`, `scripts/build_host_spike.ps1`.
Local executable/state/event log: `.local/phase-02/host/`.
Run `./scripts/build_host_spike.ps1 -Probe` for the controlled test panel. Normal executable launch shows only the pet and tray icon. No startup registration, wallpaper changes, network calls or source assets are involved.

The spike loads a static idle and optional ordered 24 fps PNG reaction. Clicks during a reaction are ignored. Dragging uses the Windows drag threshold and mouse capture. Size/position are clamped to a working area and stored locally. This is a feasibility implementation, not a packaged or hardened release; mixed-DPI handling and instance control remain later work.

### Observed results and limits

| Check | Result | Evidence / remaining gap |
|---|---|---|
| Build with warnings as errors | PASS | Installed Framework C# compiler; executable launched |
| Native layered presentation call | PASS | No UpdateLayeredWindow failure logged at launch |
| Visible transparent edges | UNCONFIRMED | Agent desktop capture unavailable; no visual acceptance claimed |
| Native click and release | OBSERVED | Pointer-down followed by reaction-start/end in event log |
| Click versus drag | OBSERVED | Two drag-ended events, saved position 696,218,320; no reaction for those drags |
| Repeated click | OBSERVED | Second pointer sequence during reaction logged repeat-click-ignored |
| Position/size persisted across relaunch | PASS in runtime log | Local position.txt and new launch both report 696,218,320; menu-exit persistence still untested |
| Rough wave loaded and played | PASS for runtime completion | 73 frames loaded; startup preview completed in 3.054 seconds, without logged failure; not a frame-pacing or native-click acceptance claim |
| Transparent corner reaches underlying window | NOT VERIFIED | Required native test remains open |
| Size and hide/restore controls | IMPLEMENTED, NOT VERIFIED | Test-panel/menu callbacks exist; callback existence is not input proof |
| Tray restoration, close and resource cleanup | NOT VERIFIED | Requires actual interaction |
| Alternative DPI / monitors | NOT TESTED | Prototype is system-DPI aware, not a mixed-DPI acceptance claim |
| Windows 11 recipient PC | DEFERRED | User chose local Windows 10 tests first |

Computer Use screenshot capture failed on the selected probe window and after one fresh selection retry:
`SetIsBorderRequired failed: Böyle bir arabirim desteklenmiyor (0x80004002)`.
Accessibility-only window inspection works, but an element click failed with `coordinate input geometry is unavailable`. No input was sent by that failed click; no repeated geometry guessing or alternate input-injection workaround was attempted. Logs reflect observed native events, not a completed automated desktop test suite. An asynchronous user question about visibility/dragging is pending.

### Short manual check to close the native gaps

1. Click **Align pet for test**. Click **Transparent corner**: corner count should increase without a pet reaction.
2. Click the visible character over **Covered body**: pet reaction should increase while covered-body count stays unchanged.
3. Drag the character and release: it should move without starting a reaction. Click it twice quickly: one reaction should finish smoothly.
4. Try Small/Large, then Hide/Show. Close the probe panel to leave just the pet. Hide using the pet menu; restore by double-clicking its tray icon.
5. Exit from its menu, relaunch the executable, and check its size/position. Record actual results before changing this table.

## Rough wave

Reproducible authoring: `scripts/create_rough_wave.py`. Source: verified `.local/phase-01/stitch-stage.blend`; new action: `Companion_RoughWave_v1`. Existing `Stitch_Anim` retained. No re-rig or source overwrite.

Blocking inspection rejected the first high arm pose because the hand overlapped the ear silhouette. Three lower-arm alternatives were rendered; the lower pose gave visible separation. The sequence uses restrained forearm/wrist oscillation, slight head tilt, small ear lag, and a return to the original pose. Angles and timing are artistic candidates, not anatomical guarantees. No professional-quality or final-naturalness claim.

Current render target: 73 frames at 24 fps, 320 square RGBA, Cycles 8 samples with denoising. Low-sample feasibility output, not final appearance. Local scene/frames/review GIF/contact sheet belong under `.local/phase-02/wave/`; the preview packer validates and copies frames into the private host asset folder.

Saved-scene verification PASS in [phase-02-wave-verification.json](phase-02-wave-verification.json): geometry, topology, weights, UVs, rest rig and tracked material flags match; original action key data match; eight toe matrices remain unchanged over all 73 frames; all bone matrices return exactly to the initial pose. These checks do not prove mesh self-intersection freedom or visual motion quality.

All 73 frames rendered. [Frame checks](phase-02-frames.json) PASS: clear alpha borders on every frame, non-static sequence, exact decoded first/last equality, idle equal to first frame. The frame bounds union is (46,26)-(278,292) in the 320-square canvas. Six blocking poses, three actual wave frames and the 12-pose contact sheet were visually inspected: the revised raised hand clears the ear in the inspected views; feet remain planted. Static views do not establish natural timing or exclude between-frame intersections. The face/torso are largely static and the wave is restrained; expression, overlap and lighting remain Phase 03 work.

The private review GIF shows the sequence on light/dark backgrounds; its duration uses distributed 40/50 ms GIF delays to approximate 24 fps. The native host uses the original RGBA PNG frames, not the quantized GIF. Moving visual acceptance is pending. Review artifact: `.local/phase-02/wave/rough-wave-review.gif`; contact sheet: `rough-wave-contact-sheet.png`.

The old static probe process was stopped by verified executable/PID and replaced with the rebuilt host using `--preview` (one automatic playback for inspection). Saved location and size were restored; all 73 frames loaded and the reaction completed without a logged error. This tests application playback, not a new native click on the animated version. The pet remains running, the test panel is closed, and startup remains unregistered. A single idle-process sample after playback was about 56 MiB working set; this is not a performance benchmark or a leak test. Keep final motion acceptance open and preserve the Phase 03 lower-body contrast/outline decisions.

Reproduce from the repository root using Blender 5.2.2 with `--background --factory-startup --disable-autoexec --threads 4 --python-exit-code 1 --python scripts/create_rough_wave.py`. Run `scripts/verify_rough_wave.py` with the same Blender safety flags. Run `scripts/package_wave_preview.py` with Python plus Pillow/numpy, then build the host. Close an existing host before rebuilding/reloading assets. The local bundled Python used here is recorded in the tooling notes; no global Python packages were installed. Later render reports include per-frame checksums and are invalidated before rerendering; the initial completed run predates that extra manifest field.

## Animation research applied

- [Anticipation](https://www.animationmentor.com/blog/anticipation-the-12-basic-principles-of-animation/), [arcs](https://www.animationmentor.com/blog/arc-the-12-basic-principles-of-animation/) and [overlap](https://www.animationmentor.com/blog/follow-through-and-overlapping-action-the-12-basic-principles-of-animation/): clear poses, controlled timing and restrained secondary motion.
- [Pose appeal/readability](https://www.animationmentor.com/blog/tutorial-building-appealing-character-poses-for-animation/): inspect hand clearance from the large head and ears at intended display size.
- Existing rig inspection found quaternion rotations and no arm-chain constraints; retain the rig. Do not import unrelated game-export rules.
- Review motion, small-size silhouette, wrist/shoulder deformation and return continuity; static images and numeric checks are insufficient for final animation acceptance.

## Prior maintenance and optional tooling

Phase 01 corrections and preserved baseline are complete. Stage SHA-256 remains `674f2502a45a478a04285d6374904529ab327cd3dffd6aa37d3b88a685332413`. The old/new Phase 01 samples have identical decoded RGBA pixels. Details: [Phase 01 verification](phase-01-verification.json).

The [official Blender MCP trial](phase-02-tooling-research.md) succeeded in isolation through a diagnostic stdio client; native Codex registration and third-party Blender skills were not installed. The MCP trial process/listener is closed. Hidden viewport screenshots can be stale; use real renders for pose evidence. Scripted rendering remains reproducible without MCP.

## Next checkpoint

Rendering, data/image checks, pose inspection and initial host playback are complete. Resolve native-interaction gaps through working computer-use capture or the short manual check, and obtain a moving-preview observation. The C# layered-window approach remains the sole candidate; transparency and menu usability are not yet accepted. Finish Phase 02 only after its evidence is recorded; do not silently move to Phase 03.
