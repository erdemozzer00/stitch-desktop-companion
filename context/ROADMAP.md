# Roadmap

Exactly one phase is active. Complete its evidence handoff and stop before proceeding to the next phase.

## Phase 01 — Source verification and reproducible preparation

**Status: ACTIVE**

Inventory and hash the supplied files; inspect the model, rig, action, texture paths, and local Blender version. Preserve originals and prepare a local working stage. Establish the public repository under the verified `erdemozzer00` account.

**Exit:** reproducible preparation and verification results, a baseline render, source/provenance notes, verified repository ownership and visibility, and a handoff listing remaining uncertainties. No new-animation or desktop-app claims.

## Phase 02 — Motion and Windows feasibility spikes

**Status: PLANNED**

Produce a rough wave using the existing rig and a separate minimal Windows desktop prototype using a simple visual. Test visibility behind full and partial application windows, minimize/restore, Win+D, click handling, dragging, and access to underlying desktop icons.

**Exit:** inspectable rough motion, observed desktop behavior, a selected implementation approach, and documented failures or tradeoffs. Turning off always-on-top is not sufficient proof of desktop integration. Rough motion is not final animation quality.

## Phase 03 — Appearance and animation polish

**Status: PLANNED**

Set the camera, lighting, materials, and intended desktop size. Polish one sequence: idle, notice the user, wave, and return to idle. Review it both enlarged and at intended display size.

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
