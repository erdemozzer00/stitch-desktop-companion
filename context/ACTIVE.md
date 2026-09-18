# Current handoff

**Last completed phase:** 01 - Source verification and reproducible preparation

**Status:** Phase 02 active. The user authorized the simplified floating-pet implementation on 2026-09-18. The old desktop-only requirement is superseded.

**Latest user steering (2026-09-18):** proceed with a standalone floating Stitch and keep Markdown handoffs current. Do not resume Rainmeter On Desktop or introduce two host tracks. Preserve prior model/animation work.

**Active phase:** 02 - Motion and Windows feasibility spikes. See [execution notes](evidence/phase-02-review.md).

**Latest result:** `host/PetSpike.cs` compiles with warnings as errors and runs a native layered window with a 73-frame rough wave. Saved position/size survived relaunch; a startup-preview reaction completed in about 3.05 seconds without a logged failure. Native pointer events separately recorded dragging, clicking and suppression of a repeated click. Candidate: WinForms plus `UpdateLayeredWindow`; native transparency/menu acceptance remains open. No SDK, web runtime, installer or startup registration added. Computer Use screenshots failed twice with `SetIsBorderRequired ... 0x80004002`; accessibility reads work but clicking fails with `coordinate input geometry is unavailable`.

**Local runtime state:** the animated pet is running, without the probe panel; PID is recorded in `.local/phase-02/host/process.pid` (always verify executable before acting on it). Right-click the pet or tray icon to exit; double-click the tray icon to restore. Render and verification processes finished; the MCP listener is closed. Private motion scene, frames, review GIF and contact sheet exist under `.local/phase-02/wave/`. No final motion-quality approval. The asynchronous user visibility/dragging question remains unanswered.

## Completed evidence

- Public repository owner: `erdemozzer00`; visibility: `public`.
- Source hashes, inventory and stage settings: `evidence/phase-01.json`.
- Reopen, packed-texture, geometry/rest-rig and RGBA checks: `evidence/phase-01-verification.json`.
- Visual observations and limitations: `evidence/phase-01-review.md`.
- Local outputs: `.local/phase-01/stitch-stage.blend`, `frame_01.png`, `frame_20.png`, `frame_40.png`, `inspection-board.png`.
- Blender 5.2.2 LTS. The host and new wave are Phase 02 spikes; no installer/startup setting yet.
- Rough-wave saved-scene checks: `evidence/phase-02-wave-verification.json`.
- All 73 RGBA frames have clear borders; first and last are pixel-identical; idle equals frame 1: `evidence/phase-02-frames.json`.
- Runtime copies: `.local/phase-02/host/assets/`; executable `.local/phase-02/host/StitchPet.exe`.

## Next execution

1. Audit corrections are complete; originals and the prior stage remain preserved in `.local/phase-01-before-audit-fix/`.
2. Obtain the user's observation of the open pet and the rough GIF. Key poses/contact sheet were reviewed; moving playback and naturalness are not accepted. No polish yet.
3. Resolve the short native checklist in Phase 02 review: alpha-zero click-through, size, hide/restore/tray/exit, and post-integration pointer-triggered wave. No startup registration yet. Do not retry failed screenshot capture indefinitely or substitute guessed input.
4. Select the host from observed results; avoid browser-specific hiding, Windows desktop embedding, or a generic multi-pet engine.
5. Record failures and tradeoffs, then stop at the Phase 02 handoff. Reserve polish for Phase 03.

## Open items

- Weak lower-body contrast on dark backgrounds at small size: observed, to address in Phase 03.
- Legacy outline is disabled in the candidate stage; final appearance is not approved.
- Blocking and selected rendered frames were inspected; natural timing and final deformation quality are not accepted.
- Recipient display count, resolution and DPI are unknown; they do not block a local single-display spike.
- The user requested local Windows 10 tests first and deferred planning Windows 11 final acceptance. Keep that validation open; local results are not target-PC evidence.
- Third-party character assets and personal messages remain local, excluded from public Git.
