# Current handoff

**Last completed phase:** 02 - Motion and Windows feasibility spikes, 2026-09-19.

**Status:** Phase 03 in progress. Step 03.1 pose comparison selected the soft stance; idle/wave timing drafts and their data/image checks are complete for review. See the [execution plan](ANIMATION-PLAN.md) and [live review](evidence/phase-03-review.md). Animation quality is explicitly not approved; no Phase 04 work has started.

**Current cursor:** Collect targeted moving-preview feedback: is the idle too subtle/still robotic, and is the wave pace suitable? Artifact: `.local/phase-03/idle-wave-review.gif` (4-second idle followed by 49-frame wave, 24 fps). React to feedback before spending on final render quality. Next: revise core motion as needed, then Step 03.4 contrast/outline/400-pixel output and interruption-transition review. These 320-pixel low-sample drafts are not final assets. The Phase 02 host/assets remain unchanged; do not tell the user the desktop app already has the new idle.

**Latest checks:** `phase-03-motion-checks.json` verifies preserved source fields/action, near-stationary toes, idle periodic endpoint and wave return. `phase-03-frame-checks.json` verifies all 145 frame hashes/clear alpha boundaries, exact neutral/return image equality, and unchanged Phase 02 host assets. Contact sheets/selected poses inspected; moving naturalness remains for user feedback. Original failed combined run completed idle but failed on a negative quaternion interpolation factor; corrected wave authored/rendered separately with success. Do not restart the entire phase or rerender valid idle just because the older log contains that known error.

## Latest user feedback

The user reports alignment and six corner-counter clicks work; rapid/repeated clicks and dragging across the desktop do not interrupt or glitch the wave; both sizes work without clipping and preserve animation; hide/show works; closing/reopening restores the same position and size.

The user also says the wave is much too slow and low quality, and the static idle looks robotic. Treat these as concrete Phase 03 defects to address, not as approval of the current motion. Existing logs support repeated-click suppression, dragging, hide/show, resizing and close/relaunch. Exact tray restoration and the covered-body counter were not separately confirmed; retain them as explicit integration checklist items rather than inventing full acceptance.

## Selected implementation

Keep the native C# WinForms layered window and Blender-rendered RGBA frames. The observed local behavior is sufficient to choose this approach for the gift. No browser-specific hiding, desktop-shell embedding, alternative host or engine migration.

The user approved trying the recommended authored carry/drag response after idle and wave quality work. The bounded experiment may use pointer direction/speed, restrained secondary motion and a short release/settle sequence. Inclusion remains conditional on its quality and complexity; ordinary dragging is the fallback. Full articulated ragdoll and an engine migration remain excluded. Nothing has been implemented for this effect yet.

## Evidence and preserved outputs

- Phase 02 scope, user results, research and remaining limits: [review](evidence/phase-02-review.md).
- Source/model/rig/action preservation and stationary toe/return-pose checks: [wave verification](evidence/phase-02-wave-verification.json).
- All 73 RGBA frames have clear borders; first/last match exactly: [frame checks](evidence/phase-02-frames.json).
- Four component-check groups pass for alpha, hidden state/settings and diagnostic/disposal behavior: [host checks](evidence/phase-02-host-checks.json). These are not native-input automation.
- Local wave: `.local/phase-02/wave/stitch-rough-wave.blend`, `rough-wave-review.gif`, `rough-wave-contact-sheet.png`.
- Local executable/assets/settings/logs: `.local/phase-02/host/`.
- Verified public repository: `erdemozzer00/stitch-desktop-companion`; all character assets/renders remain ignored.

## Current phase priorities

1. Replace the robotic neutral stance with a relaxed pose and a subtle authored idle loop. Preserve silhouette and foot contact.
2. Rework the wave's timing, spacing, shoulder/elbow/wrist coordination and secondary head/ear motion. Increasing playback speed alone is not sufficient.
3. Review the new motion on light/dark backgrounds and at desktop size; get actual visual feedback before calling it polished.
4. Run the approved bounded drag experiment in Phase 04 after the core-motion checkpoint and Phase 03 handoff. Do not introduce full physics or expand scope if the small experiment disappoints.
5. Resolve the weak lower-body contrast and undecided legacy outline as part of Phase 03.

## Runtime and remaining limits

No pet process was launched or changed in this animation turn. The previous handoff found it closed; its old PID file can be stale. Rendering/check processes have finished and the optional MCP listener was not started. Current scripts: `author_companion_motion.py`, `verify_companion_motion.py`, `preview_companion_motion.py`. All outputs stay under `.local/phase-03/`; no runtime asset installation yet.

Computer Use desktop capture previously failed twice with `0x80004002`; accessible-element input failed with unavailable geometry. User reports supply the visual interaction evidence; do not mislabel these as agent-run native tests. No global packages, startup registration or installer were added. Windows 11 recipient acceptance, mixed-DPI/multiple displays, packaging, duplicate-instance prevention and daily-use reliability remain later work.
