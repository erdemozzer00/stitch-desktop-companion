# Phase 02 execution notes

Status: IN PROGRESS. Started 2026-09-18. No Phase 02 acceptance claim yet.

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
