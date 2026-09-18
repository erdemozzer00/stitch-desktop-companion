# Roadmap

Work on one phase at a time. Complete its evidence handoff and stop before proceeding to the next phase. A completed handoff may have no active implementation phase.

## Phase 01 — Source verification and reproducible preparation

**Status: COMPLETE — 2026-09-18**

Evidence: [review](evidence/phase-01-review.md), [source and stage report](evidence/phase-01.json), [reopen and render checks](evidence/phase-01-verification.json).

Inventory and hash the supplied files; inspect the model, rig, action, texture paths, and local Blender version. Preserve originals and prepare a local working stage. Establish the public repository under the verified `erdemozzer00` account.

**Exit:** reproducible preparation and verification results, a baseline render, source/provenance notes, verified repository ownership and visibility, and a handoff listing remaining uncertainties. No new-animation or desktop-app claims.

## Phase 02 — Motion and Windows feasibility spikes

**Status: ACTIVE — 2026-09-18**

Produce a rough wave using the existing rig and a minimal floating Windows pet prototype. Following the user's 2026-09-18 direction change, test transparent presentation, click versus drag, position, size, hide/restore/exit, and access outside the visible character. The prior behind-applications/desktop-layer requirement is withdrawn.

Audit corrections and the bounded official Blender MCP trial are complete. The user authorized the simplified floating host; the current candidate is native C# WinForms with per-pixel alpha. Rainmeter On Desktop is superseded. Local Windows 10 testing is authorized; Windows 11 recipient acceptance remains deferred and unproven. Record local test gaps explicitly. See [Phase 02 execution notes](evidence/phase-02-review.md).

**Exit:** inspectable rough motion, observed floating-pet interaction, a selected implementation approach, and documented failures or tradeoffs. A transparent preview alone does not prove click/drag behavior. Rough motion is not final animation quality.

## Phase 03 — Appearance and animation polish

**Status: PLANNED**

Set the camera, lighting, materials, and intended desktop size. Polish one sequence: idle, notice the user, wave, and return to idle. Review it both enlarged and at intended display size.

Carry forward Phase 01's observed weak lower-body contrast on dark backgrounds. Resolve it through lighting/material and pose review without making the character look like a glowing sticker. The disabled legacy outline is not a settled final style.

**Exit:** a viewable motion preview and recorded visual review covering foot contact, weight, deformation, self-intersection, timing, head/ear follow-through, loop continuity, and small-size readability. Resolve the user's visual feedback before building additional motions. Static renders do not prove motion quality.

## Phase 04 — Integrated first version

**Status: PLANNED**

Integrate the approved animation with the verified desktop host. Implement click reactions, dragging, saved position, and basic size/hide/exit controls. Handle repeated clicks without abrupt pose jumps or overlapping reactions.

**Exit:** a working local companion with checked animation transitions, clean transparent edges, usable hit areas, and unobstructed desktop interaction outside the character. An animation preview inside a regular app window is not this phase's acceptance evidence.

## Phase 05 — Daily use and packaging

**Status: PLANNED**

Add startup at sign-in with an off switch and prevent duplicate running instances. Check sleep/resume, Explorer restart, settings persistence, and recovery from missing or invalid local settings. Produce a package that does not depend on Blender or development tools.

**Exit:** documented checks using the packaged application, verified startup enable/disable behavior, and short installation/removal instructions. Running a development script does not prove the package works independently.

## Phase 06 — Recipient-computer acceptance and delivery

**Status: PLANNED**

Validate the package on the recipient's Windows 11 computer and its actual display configuration. Check installation, startup, wallpaper/desktop behavior, interaction, sizing, silence, and removal. Finalize any personal message and the gift package.

**Exit:** target-computer acceptance results, delivered package and usage note, and explicit known limitations. Local developer-machine checks do not substitute for target-computer evidence.
