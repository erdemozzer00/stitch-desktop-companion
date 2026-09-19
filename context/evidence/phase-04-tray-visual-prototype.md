# Tray remote visual checkpoint — 2026-09-19

## User decision and boundary

The user explicitly withdrew controls attached to or below the character. Keep Stitch's appearance, animation, drag response and standalone floating behavior unchanged. Launching from a normal Windows desktop shortcut should create the pet and its notification-area icon. Clicking that icon opens the remote panel; it is not persistently open and there is no second launcher in a screen corner. Respect the user's Windows shortcut activation settings.

Only research and a visual prototype are authorized at this checkpoint. The user requires visual approval BEFORE integration. The currently installed trial still has its earlier hover toolbar. Do not confuse these review images with a deployed feature or silently remove that toolbar before approval.

## Research and design decision

Primary references inspected on 2026-09-19:

- [Raycast Action Panel](https://manual.raycast.com/action-panel): primary action first, logically grouped secondary commands, Escape dismissal. Apply command hierarchy; do not copy search, AI, keyboard-shortcut machinery or its full launcher.
- [WinUI Flyouts](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/flyouts): transient content with anchor placement and light dismissal. This fits mixed action and size-selection controls.
- [WinUI TeachingTip](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/teaching-tip): feature discovery and teaching, not the right primary command surface here.
- Context7 resolved `/microsoft/microsoft-ui-xaml`; queried flyout placement, light dismiss and TeachingTip comparison. Returned the official FlyoutBase light-dismiss implementation and windowed-popup focus design notes. This reinforces the interaction pattern, not a requirement to migrate the existing WinForms host to WinUI.

Selected visual direction: one 312 x 284 logical-pixel surface, 16-pixel radius, 16–20-pixel gutters, near-black purple gradient (#18151F to #281D31), faint one-pixel edge, restrained shadow, Segoe UI white text. Main El salla command, inline three-choice Boyut selector, lower-priority Gizle/Goster and Cikis actions. No nested menus, search, navigation rail, decorative cards or normal title bar. The small X dismisses only the panel; Cikis terminates the app. Startup preferences remain Phase 05 and are intentionally absent from this prototype.

States: visible pet (wave enabled, Gizle), hidden pet (wave disabled, Goster), panel closed (only pet and tray icon). Opening should follow an explicit tray click, never hover or automatic launch. On later integration: outside click/Escape dismiss; keyboard focus and accessibility remain necessary even with minimal visual chrome. Preserve existing click-to-wave and drag behaviors. Right-click tray fallback should remain available. Clamp against actual taskbar/work-area placement, rather than hard-coding the illustrated bottom-right location.

## Artifacts and reproducibility

Run `scripts/render_tray_prototype.ps1`. Its standalone System.Drawing renderer `scripts/TrayVisualPrototype.cs` references no host code and opens no interactive window. Outputs are private under `.local/phase-04/tray-visual-prototype/`:

- `desktop-open.png`: designed desktop composition, panel open near a simulated taskbar icon.
- `desktop-closed.png`: same composition with the remote closed.
- `panel-states-2x.png`: enlarged visible/hidden panel comparison.
- `tray-icon-sizes.png`: 16/20/24/32-pixel face viewports on dark and light backgrounds.

These are STATIC DESIGN COMPOSITIONS, not screenshots of the installed application, real Windows taskbar or working WinUI controls. Review headings, background and simulated taskbar are presentation scaffolding, not application UI. Character artwork is the unmodified accepted idle_0001.png. The model face is displayed through an aspect-preserving source viewport for the icon; no internet photo, new model or animation was introduced. At 16px the face details are weak; actual-tray legibility is unresolved and may need a simplified dedicated icon. Model-derived images remain ignored/private.

## Verification and next step

Renderer compilation and four image exports passed. Outputs visually inspected: no layout overlap, Turkish labels fit, controls detached from character, open/hidden hierarchy visible. Replaced unsuitable/missing font glyphs with drawn hand and eye outlines after first inspection. No application regression test run: no runtime code/build/deployment was changed.

Preservation hashes checked before and after this work:

- Current trial exe: `d2e0230381aba8d2c58c30fefec094d49e6c8307cd99e87599594e0dd9e5c881`.
- PetSpike.cs: `90c7a8b7b69218b2311d14306947b4445bd07c95f307a16bd645278c0502e07a`.
- CarryMotion.cs: `bc0f111c73d40e2ee5e767bb7c72bf43b842519ac3b86ac9006592d8870fa36a`.
- CompanionUi.cs: `0d57144ea61de96cbd8d8468f1d753b9dbda300870a34df6b78fc74111f4ae94`.

STOP for the user's visual review. If approved, integrate the tray remote and remove the character-attached command bar while keeping animation/drag untouched. Verify real tray activation/dismissal, hidden restore, keyboard focus, command states, working-area edges and installed-app preservation; update the same accessible trial shortcut. Do not claim those checks from this static prototype. Phase 05 packaging/startup/single-instance and Phase 06 Windows 11 acceptance remain later work. The latest release-pixelation/settle fix still needs explicit user feedback; do not infer acceptance from their new UI direction.
