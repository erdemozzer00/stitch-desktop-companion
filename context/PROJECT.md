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

Prepare the model and animation in Blender, then evaluate pre-rendered transparent animation for the small desktop companion. Choose the application technology after the Windows desktop spike. Do not commit to a framework before the required window behavior has been demonstrated.

The initial Rainmeter On Desktop investigation is superseded by the user's requested Codex-pet-style floating behavior. No host was installed or implemented. Discuss the simplified host before choosing its framework; do not maintain parallel desktop-embedded and floating implementations. The recommendation is a standalone offline gift with familiar floating-pet interactions; direct installation as a custom Codex pet is a distinct alternative requiring the host app. The development PC is Windows 10 Pro (build 19045); the user requested local tests first and a later decision about Windows 11 final acceptance. Keep that target validation open.

The motion should fit Stitch's stylized design: readable weight, coordinated shoulder and wrist movement, restrained head and ear follow-through, and smooth transitions. Preserve the character's appearance. Re-rig only if a demonstrated defect requires it.

## Initial inspection baseline

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
