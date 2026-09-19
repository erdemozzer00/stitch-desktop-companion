# Detached tray remote integration — 2026-09-19

## Authorization and result

The user approved the revised 312 x 220 dark-purple remote without an El salla command, confirmed launch should show only the character and tray icon, and explicitly requested implementation. This supersedes the static-prototype-only boundary. The integrated trial uses the same desktop shortcut and executable path; no startup registration or packaging work was started.

The character has no attached controls or hover toolbar. Its right-click no longer opens a menu at the character. Clicking the small Stitch notification icon opens the remote near the click, clamped to that monitor's work area. The panel starts closed, closes on deactivation, Escape or its X, and can be opened while the pet is hidden. Commands: three sizes, Gizle/Goster, Cikis. Right-clicking the tray retains a native fallback menu with the same commands and no wave command. The greeting remains triggered by clicking the character. Closing the panel does not close the application; Cikis does.

## Implementation boundaries

- `host/CompanionUi.cs`: replaces the old timed/hover CommandBar with a standalone activating RemotePanel; no hover timer or pet-relative placement remains. No owner link to the pet, so hidden-pet restoration remains available. Native Button controls retain keyboard/focus/accessibility support beneath custom painting. Visible focus outline, accessible names, selected-size description and Escape handling are present; screen-reader and physical keyboard acceptance are not claimed.
- `host/PetSpike.cs`: creates the Stitch face tray icon from the accepted neutral image, routes left-click to the remote, removes character-local menus/reveal calls, refreshes size/visibility state and disposes the panel/icon. Right-click tray menu remains. Tray image is a runtime viewport of the existing render; no new downloaded media.
- Popup positioning uses the tray click coordinate and screen work area, not a hard-coded bottom-right corner or private NotifyIcon reflection. The reflection in checks dispatches only the test event. Overflow-tray and alternate taskbar positions still require physical acceptance. A 200ms deactivation guard avoids immediate reopening on the same tray click; very rapid repeated clicks and long presses need user observation.
- System DPI scaling preserves the app's existing manifest. Do not claim per-monitor DPI or full WinUI behavior. Native drop-shadow style is requested; DrawToBitmap does not prove desktop shadow composition.
- The carried-toy controller file is unchanged: SHA-256 `bc0f111c73d40e2ee5e767bb7c72bf43b842519ac3b86ac9006592d8870fa36a`. No wave/idle keys, sprite bank, response parameters or release handoff changed. There was no Blender render.

Context7 was used for the official WinForms NotifyIcon setup, ProcessCmdKey and Button keyboard semantics. Additional primary source: [NotifyIcon.MouseClick, .NET Framework](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.notifyicon.mouseclick?view=netframework-4.8.1). Visual pattern research remains in [the approved prototype record](phase-04-tray-visual-prototype.md).

## Checks actually run

- Final candidate build: PASS, warnings treated as errors.
- `check_polished_ui.ps1`: PASS, 143 assertions, recorded in `phase-04-tray-ui-checks.json` with source hashes. Includes retained release-tail checks and palette checks, not 143 independent UI tests. Minimum tested text contrast 6.23:1. Existing controlled release remains 0.425s to idle and 0.292s near-static tail removed.
- Actual native forms and message loop: launch leaves panel closed; tray left-click event handler opens it; second toggle closes; native control buttons change size; Escape handler dismisses; activating another native form triggers deactivation dismissal; hidden pet retains tray access and remote restoration; direct character click waves; direct drag moves immediately and hides the remote; fallback menu restores; exit disposes pet and remote. These are programmatic event/method/control tests, not physical shell input.
- `check_host_spike.ps1`: PASS, 1,941 assertions; `phase-04-tray-baseline-checks.json`.
- `check_carry_trial.ps1`: PASS, 179,452 controller/state/pixel assertions; C# vs accepted Python trace maximum angle error remains 3.7183734292764774e-8 rad. These component reports preceded only the final remote-visibility log addition; the UI suite and build were rerun against the final source.
- Real WinForms DrawToBitmap captures inspected: `.local/phase-04/polished-trial/ui-review/tray-remote-visible.png` and `tray-remote-hidden.png`, 390 x 275 pixels at this machine's system DPI. Labels fit, face present, no wave command, selected size distinct, hidden state offers Goster. These are control captures, not desktop screenshots.

## Deployment and handoff

`update_carry_trial.ps1 -Launch` validated all baseline and 45 carry frame hashes, gracefully closed the prior exact trial process, backed it up and preserved its position/size settings. It updated `.local/phase-04/native-trial/StitchPet.exe` and the existing desktop `Stitch - Tasima Denemesi` shortcut, then relaunched it.

- Revision: `phase04-tray-remote`.
- Executable SHA-256: `dce15670a9c0bf1e0e3201c0dcb166ce4e21d77b46cab173b75e3e7bbdf75acd`.
- Backup: `.local/phase-04/native-backup-20260919-175703-839`.
- Process PID at launch: 41748; may become stale.
- Installed log confirms `ui=tray-remote panel=False carry=True idle=96 wave=45 size=400` at 17:57:06 UTC.
- Original Phase 03 executable still hashes to `d0ac9f4d32bc35a8399d0211fba770e4458e9aed7587cdc981ad4a7f03b27771`. Frozen desktop backup untouched.

Next: user checks actual notification-icon click, outside-click/Escape dismissal, small-icon legibility and hide/show on their Windows 10 desktop. Do not infer acceptance from subsequent pointer log events. Explicit feedback on the prior release polish remains open. Phase 04 stays ACTIVE pending these observations; Phase 05 startup/single-instance/packaging and Phase 06 recipient Windows 11 remain deferred. The existing trial shortcut name stays as-is until delivery naming/packaging; do not confuse this updated trial with a finished distributable.

## Repaint regression and desktop icon — 2026-09-19

User physically confirmed all three tray flows (open; outside-click/Escape close; hide then restore). Their screenshot also demonstrates overlapping text and unrelated button content during repaint. Prior whole-panel DrawToBitmap checks did not cover the translated/clipped drawing context used by transparent child repaint.

Root cause: GDI TextRenderer calls did not preserve the Graphics translation and clipping used to draw the panel/transparent buttons into subregions. Added a regression in PolishChecks that renders each actual button through an offset and clipped Graphics and checks that sentinel pixels outside its target remain untouched. Before production edits it FAILED on the Small button with 300 escaped pixels. Added PreserveGraphicsClipping and PreserveGraphicsTranslateTransform to all remote TextRenderer calls, including panel background labels. Afterward all six button cases and existing UI checks PASS (149 assertions). Official contract: https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.textformatflags?view=netframework-4.8.1 . No layout redesign, motion, controller or source sprites changed.

Rebuilt candidate; baseline 1,941 and carry 179,452 assertions PASS. UI contrast and release metrics unchanged. Inspected fresh native visible/hidden control captures. Physical user confirmation of this repaint fix remains pending; the regression is stronger evidence than the original static capture but does not establish all desktop painting cases.

Added BuildShortcutIcon.cs / build_shortcut_icon.ps1: creates private model-face ICO with embedded PNG sizes 16,20,24,32,48,64,128,256. The first validation attempt discovered .NET Framework Icon size selection caps below 256; revised verification decodes every PNG and verifies managed ICO selection through 128. Generated face preview inspected. start_carry_trial.ps1 assigns the ICO to the existing desktop shortcut and reads the saved IconLocation back. Updater now deploys stitch.ico with the trial. No image assets published.

Installed after backup `.local/phase-04/native-backup-20260919-185539-888`, preserving position/size settings. Exe SHA-256 `9e1a716735dd5b50c444352a2dacf833992b0537ff2f9a02b36a6cf66dffcd84`; PID at launch 40412 (may be stale). Saved shortcut `C:/Users/Erdem/Desktop/Stitch - Tasima Denemesi.lnk` has IconLocation pointing to the existing `.local/phase-04/native-trial/stitch.ico,0`. Actual Explorer rendering/cache refresh is user acceptance, not inferred from the property readback.

Remaining: confirm repaint fix visually, prior release-pixelation fix feedback, then Phase 04 closure. Phase 05 remains sign-in startup with off switch, single instance, sleep/resume/Explorer/settings recovery, standalone packaging and instructions. Phase 06 remains recipient Windows 11 acceptance.

## Correction: first repaint fix did NOT resolve live UI — 2026-09-19

User reported unchanged overlap after the previous fix. The translate/clip test caught a real drawing contract issue but did not establish the root cause of the live accumulation. Retract the previous claim of full resolution.

Attempted Computer Use @oai/sky through its supported node_repl; tool transport was closed before initialization. No desktop input was injected through a fallback. Instead extended the native test harness to repeatedly call the existing mouse-enter/leave event methods and Control.Refresh, then capture the real displayed panel client DC with GetDC/BitBlt. This is an actual HWND raster capture, unlike prior DrawToBitmap. Before the fix, captured stale hover fills on all buttons and black corner remnants, matching part of the user's reported corruption. Not a physical pointer/tray test.

Cause: the custom transparent Button subclass painted only current text/icons/highlights and relied on ButtonBase/background handling to erase old content. Partial native foreground repaints reused dirty pixels. New regression paints each real button over deliberately contaminated content and compares against a clean-buffer render, without relying on OnPaintBackground. Failed on Small with 491 residual pixels. Buttons now own opaque backgrounds on every OnPaint; selected size controls use their strip background and other buttons use the correctly aligned panel gradient. Initial antialiased background rectangle retained 151 boundary pixels, corrected by disabling antialiasing during complete rectangular erasure and re-enabling it for foreground shapes. Final dirty-buffer comparison passes all six buttons. No redesign, input behavior or motion changes.

Final UI suite PASS 156 assertions; baseline 1,941 and carry 179,452 PASS; build PASS. Native capture after 10 enter/leave rounds over six controls inspected clean: `.local/phase-04/polished-trial/ui-review/native-repaint.png`. Final captures are reproducible via check_polished_ui.ps1. Do not claim physical user acceptance until reported.

Installed same trial after backup `native-backup-20260919-190144-636`; exe SHA-256 `c3166569eddf556911bfadefa3ce45105a5e4db32b8b6c3402f701a83ba012d4`, launch PID 35348 (may be stale). Settings and Stitch desktop icon preserved. User also confirmed the prior release/pixelation issue resolved, requested startup enabled directly, agreed to duplicate prevention, and explicitly limited delivery to one girlfriend: no excessive settings or installer engineering. Record these as authorized Phase 05 decisions, not implemented features in this UI bugfix.
