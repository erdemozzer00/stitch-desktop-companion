# Minimal daily-use delivery — 2026-09-19

User explicitly requested automatic Windows start, duplicate prevention, simple personal delivery and continuation. No new design approval was necessary. Existing approved motion/UI preserved. Phase 04 implementation is handed off on the user's request to proceed; the final repaint correction has native technical evidence but no explicit separate user visual acceptance.

## Implemented

Program uses a named local-session mutex scoped by Windows user SID, plus a named auto-reset event. A duplicate signals the event and exits before loading images. The primary checks the event using a 200ms WinForms timer and calls existing ShowPet, leaving the remote closed. Mutex release is in finally; abandoned ownership is recoverable. Event is created before mutex acquisition so concurrent starting duplicates do not lose the signal. No test-only production namespace/flag remains.

Normal double-click launches discover adjacent carry assets, avoiding a special command-line dependency in the package. Explicit --carry remains compatible. Startup uses the standard current-user Startup folder shortcut, no service or administrator permissions. Setup refuses to overwrite an unrelated same-named shortcut and is repeatable. Disable/remove instructions use the existing Windows Startup folder, not a new settings screen.

Private package: `C:/Users/Erdem/Desktop/Stitch - Hediye`, initially 290 files / 26,765,088 bytes. Includes exe/config/icon, assets/carry, Kur.cmd/Kur.ps1 and Turkish Beni oku.txt. It contains no Blender project, source code, test executable or Python/Node requirement. Setup expects the user to place the folder in its permanent location before running it. Moving it afterward requires recreating shortcuts; documented. Runtime logs and position.txt are created locally on use. The developer's position was preserved for this live deployment; copying to another screen uses existing position clamping. Do not share the developer's later events.log/failure.log with the gift recipient.

## Evidence

- Before implementation, real two-process regression failed: duplicate stayed running.
- After implementation, tested actual packaged EXE: duplicate exits within deadline, hidden primary restored; four concurrent extra launches exit; primary remains. Test hides its own window via ShowWindow, does not inject physical mouse input.
- All 284 packaged asset/support files under assets/carry hash-match staged originals.
- Setup run twice without duplicate shortcuts; saved target/icon properties read back.
- Invoked actual Startup shortcut while delivery app running: exactly one Stitch process remains, at the package path. Startup registration verified, not actual sign-in execution.
- Existing UI checks PASS 156 assertions including dirty-buffer repaint regression/native capture; baseline PASS 1,941; carry PASS 179,452. These counts include repeated pixel/state assertions.
- Updated old trial too after graceful backup (`native-backup-20260919-190723-171`), then launched the delivery folder rather than the trial. Original Phase 03/frozen desktop backup untouched.
- Delivery exe SHA-256 `32050b363a250286895109d091905a622ee9012b7992a82fdf6f34f393e656d1`; process at check PID 29440 (may become stale).
- Structured evidence: phase-05-package.json, phase-05-daily-use.json, phase-05-host-checks.json; UI/carry reports include current source hashes.

Primary references: [Windows Startup shortcuts](https://support.microsoft.com/en-US/Windows/Experience/Startup-Boot/configure-startup-applications-in-windows), [.NET named event behavior](https://learn.microsoft.com/en-us/dotnet/standard/threading/eventwaithandle).

## Remaining, without expanding scope

Real sign-in after a user-chosen restart, brief sleep/resume and Explorer recovery observation, then recipient Windows 11 acceptance. No disruptive reboot, session logout or Explorer kill was performed. No new settings panel, updater, account or elaborate installer is needed. Phase 05 remains active until the practical daily-use checks are observed; do not equate registration with verified boot execution.

Future deployments must update the delivery folder as well as the development trial, after backup and graceful closure. The current trial update helper is not a delivery updater. Existing old trial shortcut shares the current singleton but the frozen historical Phase 03 binary predates it; do not launch that rollback build concurrently during ordinary use.
