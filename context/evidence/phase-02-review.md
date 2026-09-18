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
| Host component checks | PASS | Four groups in [phase-02-host-checks.json](phase-02-host-checks.json); no native input injected |
| Native layered presentation call | PASS | No UpdateLayeredWindow failure logged at launch |
| Visible transparent edges | UNCONFIRMED | Agent desktop capture unavailable; no visual acceptance claimed |
| Native click and release | OBSERVED | Pointer-down followed by reaction-start/end in event log |
| Click versus drag | OBSERVED | Two drag-ended events, saved position 696,218,320; no reaction for those drags |
| Repeated click | OBSERVED | Second pointer sequence during reaction logged repeat-click-ignored |
| Position/size persisted across relaunch | PASS in runtime log | Local position.txt and new launch both report 696,218,320; menu-exit persistence still untested |
| Rough wave loaded and played | PASS for runtime completion | 73 frames loaded; startup preview completed in 3.054 seconds, without logged failure; not a frame-pacing or native-click acceptance claim |
| Pointer-triggered animated wave and drag during playback | OBSERVED | Later native event log has several pointer-down/reaction-start/end sequences with 73 frames loaded; a drag spans a reaction end without starting another reaction on release. Visual smoothness is still unconfirmed |
| Transparent corner reaches underlying window | NOT VERIFIED | Required native test remains open |
| Size and hide/restore controls | COMPONENT CHECKS PASS; PANEL EVENTS OBSERVED | Current session logged hide/show and 240/400 resizing; visual behavior and menu/tray interaction still need observation |
| Tray restoration, close and resource cleanup | NOT VERIFIED | Requires actual interaction |
| Alternative DPI / monitors | NOT TESTED | Prototype is system-DPI aware, not a mixed-DPI acceptance claim |
| Windows 11 recipient PC | DEFERRED | User chose local Windows 10 tests first |

Computer Use screenshot capture failed on the selected probe window and after one fresh selection retry:
`SetIsBorderRequired failed: Böyle bir arabirim desteklenmiyor (0x80004002)`.
Accessibility-only window inspection works, but an element click failed with `coordinate input geometry is unavailable`. No input was sent by that failed click; no repeated geometry guessing or alternate input-injection workaround was attempted. Logs reflect observed native events, not a completed automated desktop test suite. The user requested self-checks first and questions afterwards; the consolidated checklist below replaces the earlier unanswered visibility-only question.

### Follow-up self-checks and fixes

`scripts/check_host_spike.ps1` compiles `host/HostChecks.cs` together with the real host code, selecting its test entry point. It creates no visible window or tray icon and sends no input. Scratch settings remain under ignored `.local/phase-02/host-checks/`; the running pet's settings/assets are not modified by the checks. The test-only constructor option suppresses tray creation; production still creates it.

Four groups PASS: (1) production surfaces at 240/320/400 retain clear alpha borders and valid premultiplied pixels, with alpha-zero/opaque centers matching the manual probe; (2) hidden reaction suppression, size limits and saved geometry round trip; (3) malformed and far off-screen settings; (4) an unavailable log path does not abort settings changes, and repeated disposal succeeds. Pixel assertions are numerous but are not hundreds of distinct behavioral tests. These tests do not replace OS hit-testing or menu/tray acceptance.

Code inspection found hidden `React()` calls would start invisible playback (for example from the tray menu). Hidden reactions are now ignored. Diagnostic I/O exceptions no longer abort behavior, and owned resources are released in `Dispose`, including paths that never raise `FormClosed`. The shared production rasterizer is directly tested; no substitute renderer is used. Menu and probe labels use Turkish; the compiler is explicitly configured for UTF-8 source.

The previous verified pet process was stopped to rebuild, then the revised host was launched with `--probe --preview`. The interactive panel is intentionally visible for the manual check; the one-time preview exercises initial playback, not mouse delivery. No startup, framework installation or animation polish was added.

Subsequent events in that live session include hide/show, several 240/400 resizes, a reaction, a corner-button click and another drag. This supports that the controls are being exercised; it does not supply a visual report. The recorded corner click happened after resizing to 240 without a fresh 320 alignment, so it is not accepted as the prescribed alpha hit-target test. Ask the user to use **Test için hizala** before that check. Do not reposition the pet remotely while the user is testing it.

### Short manual check to close the native gaps

Reply by checklist number with pass/fail and any visible problem. All five remain pending user observation.

1. **Transparency and hit targets:** click **Test için hizala**, wait for the idle pose, then the center of **Boş köşe**. Only its counter should increase. Click Stitch's torso over **Alttaki düğme**: **Tepki** should increase while **Alttaki düğme** stays zero. Report any visible rectangular background around Stitch.
2. **Reaction and dragging:** click twice quickly, then drag during a wave. Expect one uninterrupted reaction and movement without an extra reaction on release. Report visible pose jumps, sticking or unnatural hand/ear motion; this remains a rough animation, not a polish vote.
3. **Size:** try **Küçük** and **Büyük**. Expect no clipped head, ears, hand or feet, and usable clicks/dragging at both sizes.
4. **Hide and restore:** right-click Stitch and select **Gizle**. Restore via the Stitch information icon near the Windows clock (possibly in the overflow area), using a double click or **Göster** in its menu. The panel's **Göster** is a recovery option, not proof that tray restoration worked.
5. **Exit and saved position:** drag to a recognizable position, choose a size, right-click **Çıkış**, then relaunch `.local/phase-02/host/StitchPet.exe`. Expect the character to disappear on exit and return at the saved position/size. Closing only the test panel's X should leave Stitch running. No need to rebuild; avoid relaunching while an instance is still open.

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
