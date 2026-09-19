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
