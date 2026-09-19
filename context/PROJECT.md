# Project

## Purpose

Create a personal gift: a recognizable, naturally animated Stitch companion for the recipient's Windows 11 desktop, using the supplied Blender model.

## Agreed first version

- Silent idle movement and a click-triggered wave or happy reaction.
- Codex-pet-style floating character; the user withdrew the requirement to stay behind normal application windows on 2026-09-18. Do not implement browser-detection hiding or desktop-shell embedding.
- Drag to position, remember the position, and provide size, hide, and exit controls.
- Start at sign-in, with a setting to disable startup.
- A short personal message may be added after the core interaction works; its wording is not yet chosen.
- Offline operation; no AI service or subscription is needed for the agreed behaviors.

The recipient uses a static downloaded wallpaper. Her display count, resolution, and DPI are not yet confirmed. Do not claim support for untested display configurations.

## Working approach

Prepare the model and animation in Blender, then use pre-rendered transparent frames in the small desktop companion. The Windows feasibility spike and user observations now support the application technology selection below.

Phase 02 decision (2026-09-19): retain the small native C# WinForms layered-window host and Blender-rendered RGBA frames based on local checks and the user's manual observations. This selects the implementation approach; it does not approve the existing motion quality or certify the recipient's Windows 11 setup.

The initial Rainmeter On Desktop investigation is superseded by the user's requested Codex-pet-style floating behavior. The selected host is C# WinForms using the Windows layered-window API, with the observed behavior and remaining limitations recorded in Phase 02. Do not maintain parallel desktop-embedded and floating implementations. The gift is standalone and offline; direct installation as a custom Codex pet is not the delivery choice. The development PC is Windows 10 Pro (build 19045); the user requested local tests first and a later decision about Windows 11 final acceptance. Keep that target validation open.

The motion should fit Stitch's stylized design: readable weight, coordinated shoulder and wrist movement, restrained head and ear follow-through, and smooth transitions. Preserve the character's appearance. Re-rig only if a demonstrated defect requires it.

## Initial inspection baseline

Tray remote refinement (2026-09-19): the user removed the El salla command from the panel; the recipient will wave by clicking Stitch. The remote contains size, hide/show and exit only at this stage. Preserve click-to-wave unchanged. The user subsequently approved this visual prototype and explicitly requested integration; the updated trial is installed, pending physical user review.

These observations were reconciled with the generated Phase 01 evidence:

- Source Blender file version: 2.78.
- Working Blender version: 5.2.2 LTS.
- One character mesh, 14,886 vertices, and a 127-bone rig.
- No unweighted vertices reported in the inspected source mesh.
- Existing action: `Stitch_Anim`, frames 0–40 at 24 fps.

These facts do not establish deformation quality, a finished wave, or application compatibility. Exact source hashes, provenance, and reproducible inspection details belong in the source and evidence records.

## Boundaries

Keep the original downloads unchanged. Keep model files, textures, renders, and local output outside Git while redistribution remains unverified. The verified public repository is `erdemozzer00/stitch-desktop-companion`.

No roaming behavior, speech, sound, real-time AI, complex settings system, or new rig is part of the first version. The user explicitly requested replacing the old desktop-only requirement with familiar floating-pet behavior. Codex is an interaction reference; do not infer a request for its chat, task-monitoring, or account features.

On 2026-09-19 the user approved the order: relaxed stance/idle, improved wave, then a bounded authored carry/drag experiment. The experiment is authorized; shipping the effect depends on visual quality and proportionate complexity. The user allows omitting it if costly or unsuitable. Full articulated physics is excluded; keep the current renderer and ordinary dragging as fallback. See the [animation execution plan](ANIMATION-PLAN.md).

2026-09-19: The user approved splitting the carry trial into 04A (pickup, held-neutral, release/settle) and 04B (direction/speed response after moving review). Godot is cancelled for the current scope. Keep the accepted installed app unchanged during the inexpensive 04A preview experiment.

Latest correction (2026-09-19): The user selected carried-toy A: the pointer directly moves Stitch while body/ears lag and settle. Facing toward travel direction is not the selected effect. The old pickup-only-first review order is superseded; the next preview must show the actual pointer trajectory and synchronized directional response. The user requested a revised plan and explicit approval before starting it. See ANIMATION-PLAN.md; preserve existing accepted app.

The user subsequently approved the revised directional experiment, conditional on a full desktop fallback copy first. The copy was completed and verified before implementation; see context/evidence/phase-04-fallback-backup.json. Godot remains outside the current scope.

Latest decision: the directional-v1 reaction is ideal; preserve its strength and timing with eyes OPEN. The user cancelled the subsequently previewed closed-eye addition. Its private geometry and scripts remain historical experiments only and must not enter the runtime or production asset bank. No facial refinement approval is pending. Continue the original open-eye carry integration plan; the accepted source and installed app were never changed by the eye experiment.

Phase 04 native trial policy: existing idle-entry frames provide the short neutral bridge; an active wave finishes under immediate pointer movement and global visual swing before switching to the articulated carry bank. This avoids resetting the raised arm but delays the full carried pose until the greeting ends. The user must assess that compromise in the isolated trial. Global rotation follows the selected grab coordinate; local ear/limb articulation does not guarantee exact anatomical pinning for arbitrary grabs.

Latest feedback: the user accepted the native carry trial overall ("10/10"), reporting only brief release pixelation and near-static pause. Authorized a fix preserving response strength, followed by a simple modern interface for a nontechnical recipient. Final chosen palette is a restrained near-black PURPLE gradient with white text, superseding the initial black/white idea. The initially implemented character-attached command bar is now superseded by the decision below. This does not authorize unrelated gestures, voice, Godot or early startup/packaging work.

Latest UI decision (2026-09-19): keep the independent floating character and all behaviors unchanged. Move controls entirely to a compact remote opened by clicking the notification-area Stitch icon. No controls above/below the character and no extra screen-corner launcher. Normal desktop shortcut launch creates the pet and tray icon; the panel stays closed until clicked. Use standard Windows shortcut behavior. Research Raycast and WinUI patterns, then present ONLY a static visual prototype; integrate only after explicit visual approval. Use the existing model face as the proposed icon. See [tray visual checkpoint](evidence/phase-04-tray-visual-prototype.md). Startup opt-in/out, single-instance activation and final packaging remain Phase 05.

That visual approval and implementation authorization have now been received. The detached remote is integrated and installed; see [integration result](evidence/phase-04-tray-integration.md). The earlier prototype-only restriction is satisfied. Continue with actual trial feedback; do not re-request design approval.
