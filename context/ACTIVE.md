# Current handoff

**Last completed phase:** 02 - Motion and Windows feasibility spikes, 2026-09-19.

**Status:** Feasibility handoff complete. No active implementation phase. Phase 03 is next; it has not started. Animation quality is explicitly not approved.

## Latest user feedback

The user reports alignment and six corner-counter clicks work; rapid/repeated clicks and dragging across the desktop do not interrupt or glitch the wave; both sizes work without clipping and preserve animation; hide/show works; closing/reopening restores the same position and size.

The user also says the wave is much too slow and low quality, and the static idle looks robotic. Treat these as concrete Phase 03 defects to address, not as approval of the current motion. Existing logs support repeated-click suppression, dragging, hide/show, resizing and close/relaunch. Exact tray restoration and the covered-body counter were not separately confirmed; retain them as explicit integration checklist items rather than inventing full acceptance.

## Selected implementation

Keep the native C# WinForms layered window and Blender-rendered RGBA frames. The observed local behavior is sufficient to choose this approach for the gift. No browser-specific hiding, desktop-shell embedding, alternative host or engine migration.

The user asked whether dragging could have a ragdoll effect and explicitly allows omitting it if too costly. Recommendation under discussion: authored carry/drag poses with restrained motion responding to pointer speed/direction and a short release/settle sequence. This is an optional proposal, not approved scope or implemented physics. Full articulated ragdoll would require runtime body/constraint simulation and a substantial change from the current flat-frame renderer; do not start it silently.

## Evidence and preserved outputs

- Phase 02 scope, user results, research and remaining limits: [review](evidence/phase-02-review.md).
- Source/model/rig/action preservation and stationary toe/return-pose checks: [wave verification](evidence/phase-02-wave-verification.json).
- All 73 RGBA frames have clear borders; first/last match exactly: [frame checks](evidence/phase-02-frames.json).
- Four component-check groups pass for alpha, hidden state/settings and diagnostic/disposal behavior: [host checks](evidence/phase-02-host-checks.json). These are not native-input automation.
- Local wave: `.local/phase-02/wave/stitch-rough-wave.blend`, `rough-wave-review.gif`, `rough-wave-contact-sheet.png`.
- Local executable/assets/settings/logs: `.local/phase-02/host/`.
- Verified public repository: `erdemozzer00/stitch-desktop-companion`; all character assets/renders remain ignored.

## Next phase priorities

1. Replace the robotic neutral stance with a relaxed pose and a subtle authored idle loop. Preserve silhouette and foot contact.
2. Rework the wave's timing, spacing, shoulder/elbow/wrist coordination and secondary head/ear motion. Increasing playback speed alone is not sufficient.
3. Review the new motion on light/dark backgrounds and at desktop size; get actual visual feedback before calling it polished.
4. Keep the optional drag-reaction discussion separate from core idle/wave work. Do not add physics or new motions before the core quality checkpoint.
5. Resolve the weak lower-body contrast and undecided legacy outline as part of Phase 03.

## Runtime and remaining limits

At this handoff no `StitchPet.exe` process was found. The local log ends with an orderly close; the PID file can be stale. Do not claim the pet is still open or restart it without a task need. Blender render processes and the optional MCP listener are closed.

Computer Use desktop capture previously failed twice with `0x80004002`; accessible-element input failed with unavailable geometry. User reports supply the visual interaction evidence; do not mislabel these as agent-run native tests. No global packages, startup registration or installer were added. Windows 11 recipient acceptance, mixed-DPI/multiple displays, packaging, duplicate-instance prevention and daily-use reliability remain later work.
