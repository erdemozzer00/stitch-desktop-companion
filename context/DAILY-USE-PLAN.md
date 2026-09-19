# Personal delivery implementation plan

Goal: automatic sign-in start, a single Stitch per Windows user/session, and a simple private gift folder.
Spec: PROJECT.md latest user decisions. User explicitly requested these behaviors and continuation; no new approval required.
Implementation: execute inline, preserve approved motion and tray UI. No new framework, settings screen or installer service.

- [x] Add process-level regression: a second executable must exit promptly, signal an existing instance, and restore hidden pet without opening remote.
- [x] Implement named mutex plus event scoped to user/session; resolve packaged carry folder automatically for normal double-click launches. Keep probe behavior.
- [x] Build a clean private folder containing only exe/config/icon and validated frame assets. Include a short Turkish usage note and an idempotent shortcut setup script/launcher.
- [x] Setup creates desktop Stitch shortcut and current-user Startup shortcut pointing to the folder, with Stitch icon; no administrator rights, registry settings, service, or automatic updater.
- [x] Verify actual processes and shortcuts; run existing regression checks, deploy and launch. Keep previous trial backup and full frozen backup untouched.
- [x] Record evidence and limitations: actual sign-out/reboot and recipient Windows 11 acceptance remain unproven. No unsolicited session interruption.

Review focus: simultaneous launches; repeat while hidden; folder paths containing spaces; startup target and icon persistence; removal instructions that do not delete unrelated files. Phase 05 is active on explicit user continuation. Latest UI fix is technically verified; do not fabricate explicit visual acceptance from the user's request to move on.
