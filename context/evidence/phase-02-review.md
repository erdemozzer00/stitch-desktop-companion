# Phase 02 execution notes

Status: IN PROGRESS. Started 2026-09-18. No Phase 02 acceptance claim yet.

## Current direction change - 2026-09-18

The user requested discussion before further implementation: follow familiar Codex-pet behavior with Stitch and drop special browser/desktop visibility requirements. This supersedes the earlier desktop-only/Rainmeter On Desktop scope below. No Windows host exists, so this does not discard host implementation. Retain Blender, the supplied rig, transparent rendered frames, and the tested optional MCP development aid.

[Official pet documentation](https://learn.chatgpt.com/docs/pets) confirms floating above other apps, dragging, sizing, hiding, and saved position; it also describes sprite animation. It does not establish that an independent pet can reproduce every Codex behavior or that the host implementation is reusable. Recommend a standalone offline companion with idle, click-wave, drag/save-position, size, hide/restore/exit, and optional startup. A custom pet inside Codex is a separate dependency choice, not the assumed gift delivery. Do not add Codex chat/task features or implement two Windows hosts.

The pasted AI conversation is reference material, not instructions to install its named projects. Its exact asset-contract examples, third-party host claims, and percentage-of-work estimates were not independently verified and must not become requirements. No framework selected or product code changed during the discussion.

### Motion work interrupted at the discussion

Researched [anticipation](https://www.animationmentor.com/blog/anticipation-the-12-basic-principles-of-animation/), [arcs](https://www.animationmentor.com/blog/arc-the-12-basic-principles-of-animation/), [overlap](https://www.animationmentor.com/blog/follow-through-and-overlapping-action-the-12-basic-principles-of-animation/), and [readable poses](https://www.animationmentor.com/blog/tutorial-building-appealing-character-poses-for-animation/). Apply clear key poses before interpolation, controlled changes of speed, and restrained follow-through after the main action. The large head/ears require checking hand silhouette and clearance at small size. Numerical timing and angles must be tuned visually, not presented as universal rules.

Live inspection found no constraints on the shoulder/upper-arm/forearm/wrist/palm chain, no rig drivers or NLA tracks, and quaternion rotation controls. A temporary FK arm raise was explored in memory. No new action, rendered motion, or saved wave exists. The first capture was stale while the window was hidden; do not treat it as visual pose proof. Local inspection and attempted-pose arguments: `.local/phase-02/mcp-trial/wave-rig-inspection.json` and `wave-block-args.json`. The trial was closed; stage and copy hashes remain `674f2502a45a478a04285d6374904529ab327cd3dffd6aa37d3b88a685332413`.

The sections below retain prior-phase history; desktop-only host choices and covered-window checks are superseded by this direction change.

The user-approved [Blender MCP trial](phase-02-tooling-research.md) is complete: isolated official server, scene/rig queries, frame changes, and inspected viewport captures worked. No third-party skill pack was installed. Fresh stage verification passed; decoded RGBA pixels at all three sample frames match the backed-up renders. The Rainmeter portable-install command was rejected by automatic approval review (`blocked by policy`); only the downloaded installer hash and signature have been verified. Host tests remain NOT RUN.

## Approved scope and decisions

- Build the silent desktop-only Stitch gift with the supplied model/rig.
- Preserve the Blender pre-rendered RGBA direction. Sprite sheets package those same frames.
- Evaluate Rainmeter before implementing custom shell/window management. Its documented On Desktop mode, dragging and saved position are relevant existing capabilities.
- Keep the Windows-host placeholder separate from the rough wave until both are understood.
- The user approved testing on the current Windows 10 PC first and deferred planning the Windows 11 final check. Target compatibility remains open.
- Record work in canonical Markdown so another session can resume from this repository.

## Step 1 - Audit maintenance

Complete. Prior local stage/renders are preserved in `.local/phase-01-before-audit-fix/`. Removed unjustified backface-culling override, added focused preservation checks, and tied fresh verification to stage SHA-256. The original export manifest/.git criticism concerned a different ZIP and does not require rebuilding the project. Fresh verification PASS and pixel comparison are recorded in the tooling trial notes; named-field checks do not cover every shader, constraint, or keyframe.

## Step 2 - Windows host experiment

Candidate: Rainmeter portable, isolated under `.local/`. No startup registration or wallpaper replacement. A placeholder will make hit areas and interaction observable.

| Check | Status | Evidence / limitation |
|---|---|---|
| Launch and transparent shape | NOT RUN | |
| Placeholder click response | NOT RUN | |
| Drag and saved position | NOT RUN | |
| Transparent area reaches desktop icons | NOT RUN | |
| Fully covered by normal application | NOT RUN | |
| Partially covered by normal application | NOT RUN | |
| Minimize and restore | NOT RUN | |
| Show Desktop / Win+D | NOT RUN | |
| Current display scale | NOT RUN | |
| Alternate DPI / monitor configuration | NOT RUN | |
| Windows 11 target | DEFERRED | User requested Windows 10 tests first. |

## Step 3 - Rough motion

NOT STARTED. One short wave using the existing rig, separate from final lighting and polish. Rendered motion must be inspected; static samples or successful Python execution alone are insufficient.

### Focused animation workflow

1. Inspect control names, local rotation axes, constraints, and the active action before posing; do not infer them from a generic rig tutorial.
2. Work in a new copied action/stage. Preserve source mesh, weights, UVs, rest pose, and existing action.
3. Block neutral, attention, raised arm, wave extrema, and return poses. Check shoulders/wrists and self-intersection before adding in-between motion.
4. Refine spacing and arcs, then add restrained head/ear follow-through. Keep planted feet stable and avoid large idle motion.
5. Render a short loop; review both enlarged and at desktop size against light and dark backgrounds. Check reaction entry/exit and loop continuity in moving footage.
6. Save reproducible animation code/parameters and observations. Treat viewport inspection as iteration feedback; use final render playback for appearance and motion acceptance. Do not import unrelated game-export/NLA rules or unverified API snippets.

## Research supporting the experiment

- [Rainmeter On Desktop, dragging and position](https://github.com/rainmeter/rainmeter-docs/blob/master/source/manual/settings/skin-sections.html).
- [Bitmap animation](https://github.com/rainmeter/rainmeter-docs/blob/master/source/manual/meters/bitmap.html).
- [Mouse actions and drag interaction](https://github.com/rainmeter/rainmeter-docs/blob/master/source/manual/mouse-actions.html).
- [Portable installation](https://github.com/rainmeter/rainmeter-docs/blob/master/source/manual/installing-rainmeter/index.html).
- [Windows 11 Show Desktop fix](https://github.com/rainmeter/rainmeter/pull/413): reason to keep target validation open, not evidence of a current failure.

## Handoff

Pending experiment results. Do not advance to Phase 03 until Phase 02 results and remaining limitations have been reported.
