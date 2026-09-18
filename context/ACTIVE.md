# Current handoff

**Last completed phase:** 01 - Source verification and reproducible preparation

**Status:** Phase 02 active; bounded audit corrections first, then independent host and motion experiments.

**Active phase:** 02 - Motion and Windows feasibility spikes. See [execution notes](evidence/phase-02-review.md).

**Latest result:** the approved [official Blender MCP trial](evidence/phase-02-tooling-research.md) succeeded in an isolated local environment via a stdio diagnostic client. Scene/rig inspection, frame changes, and viewport capture worked. Native Codex MCP registration remains unconfigured; no third-party skill pack was installed. Maintenance verification is PASS and decoded sample pixels match the prior renders. Rainmeter installation remains blocked by automatic approval review; desktop behavior tests have not started.

**Local runtime state:** trial Blender process and listener are closed; source/copy hashes unchanged. Installed MCP environment stays under ignored `.local/runtime/`. Resume commands and dependency pin are in the trial notes. Current task scope completed: tooling evaluation; Phase 02 itself remains active, with rough wave next.

## Completed evidence

- Public repository owner: `erdemozzer00`; visibility: `public`.
- Source hashes, inventory and stage settings: `evidence/phase-01.json`.
- Reopen, packed-texture, geometry/rest-rig and RGBA checks: `evidence/phase-01-verification.json`.
- Visual observations and limitations: `evidence/phase-01-review.md`.
- Local outputs: `.local/phase-01/stitch-stage.blend`, `frame_01.png`, `frame_20.png`, `frame_40.png`, `inspection-board.png`.
- Blender 5.2.2 LTS. No new animation, desktop host, installer or startup setting has been created.

## Next execution

1. Audit corrections are complete; originals and the prior stage remain preserved in `.local/phase-01-before-audit-fix/`.
2. Next: test a small wave with the existing rig using the focused workflow in the Phase 02 notes. The MCP trial can assist live inspection; reproducible rendering remains script-driven.
3. Independently test a portable Rainmeter host on the current Windows 10 PC with a placeholder: covered/uncovered desktop, Chrome, Show Desktop, click-through outside the shape, dragging and desktop icons. Do not register startup yet.
4. Select the host from observed results. Do not substitute a topmost overlay or focus-based hiding without explaining the behavior change.
5. Record failures and tradeoffs, then stop at the Phase 02 handoff. Reserve polish for Phase 03.

## Open items

- Weak lower-body contrast on dark backgrounds at small size: observed, to address in Phase 03.
- Legacy outline is disabled in the candidate stage; final appearance is not approved.
- No visual evidence yet for wave deformation or natural animation timing.
- Recipient display count, resolution and DPI are unknown; they do not block a local single-display spike.
- The user requested local Windows 10 tests first and deferred planning Windows 11 final acceptance. Keep that validation open; local results are not target-PC evidence.
- Third-party character assets and personal messages remain local, excluded from public Git.
