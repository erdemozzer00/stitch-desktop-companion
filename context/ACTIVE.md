# Current handoff

**Last completed phase:** 02 - Motion and Windows feasibility, 2026-09-19.

**Status:** Phase 03 ACTIVE. User accepts the idle direction for now and explicitly likes the final 45-frame wave. The user also explicitly requests keeping the desktop app current. Minimal idle/wave/entry integration was brought forward for live Phase 03 review; appearance is still draft, and Phase 04 carry/drag work has not started.

**Latest user steering:** The prior updated app visibly played idle/wave and transitions at different idle phases had no conspicuous jump or stutter. The user approved limited idle polish, without new gestures, and asked to preserve the next-step plan. This polish is now rendered, checked and installed: chest motion +25%, head motion +20%, unchanged four-second timing and accepted wave. Backups: `idle-before-idle-polish/` and `entries-before-idle-polish/` under `.local/phase-03/`. User perception of this small amplitude revision remains open; prior transition feedback is not automatically approval of new output.

**Completed checkpoint:** limited idle polish, fresh source/feet/seam/entry checks, 240px comparison and desktop deployment/relaunch. The user closed the previous app through its menu. Next remaining Phase 03 work is contrast on dark backgrounds, outline choice and final native 400px renders. Do not start carry/drag effects or add gestures.

**Current cursor:** The native app is updated and launched at `.local/phase-02/host/StitchPet.exe` (historical path retained). Current revision `phase03-idle-polish`: 96-frame idle, 24 four-frame entry variants and the unchanged 45-frame wave at 24 fps. Comparison: `.local/phase-03/idle-polish-comparison.gif` (previous left, refined right, both at 240px). Next: Step 03.4 appearance comparison, then true 400px renders and matching entry assets; synchronize through `scripts/update_host_motion.ps1` again. Do not leave selected motion in previews only.

## Latest evidence

- `phase-03-runtime-frames.json`: 237 frames validated against manifests, clear alpha borders, exact entry starts at sampled idle poses and exact neutral entry endpoints/wave return.
- Refined idle entry sampling over all evaluated mesh vertices at all 96 idle phases: maximum projected difference 0.669px at 400px with 24 buckets. The previous 16-bucket approach measured 1.002px for this revised idle and missed the existing one-pixel bound. This is a numerical diagnostic, not perceptual acceptance.
- `phase-03-motion-checks.json`: all 24 saved entry scenes preserve source/action, endpoints match expected idle/neutral matrices exactly, maximum toe difference about 2.4e-7. Idle periodic endpoint matches, seam diagnostic passes; accepted wave hash is unchanged.
- `phase-03-host-checks.json`: six groups / 1943 assertions, including all 96 click phases, repeat suppression, idle return, settings, alpha and direct-method Windows layered-window smoke. It is not 1943 independent tests or physical input acceptance.
- `phase-03-host-install.json`: installed executable hash, backup location and frame count. Immediately prior host/settings preserved in `.local/phase-03/host-backup-20260919-145239-447/`; original Phase 02 host backup remains `host-backup-20260919-142436-346/`. Prior 49-frame wave remains `.local/phase-03/wave-v2/`.
- Installed revision `phase03-idle-polish`; settings hashes match before/after deployment. PID file is only a hint; inspect the real process/log before future claims. One smoke run failed because physical clicks changed the expected reaction count; only the test window now disables physical input. Rerun passed, and the ordinary pet remains interactive.
- Current renders are 320px drafts; the 400px option is currently scaled. Do not claim final full-resolution output or professional animation quality from passing checks.

## User feedback and decisions

The user says idle now looks alive and likes the final faster wave. Previous Phase 02 slow/robotic complaints are superseded for this candidate. Previous physical observations confirmed corner pass-through, repeat-click suppression, dragging, sizes, hide/show and persisted geometry. Native interaction needs a short regression observation after this update; exact tray restoration and covered-body counter remain unconfirmed.

Keep the silent offline native C# layered-window host and Blender-rendered frames. Floating above normal apps is the settled scope: no browser hiding or desktop-shell embedding. Position/size/hide/show behavior is retained. Startup, packaging, duplicate-instance protection and recipient Windows 11 acceptance remain later work.

The approved later drag experiment uses authored carry poses, restrained direction/speed response and short settling, only if useful at bounded complexity. Ordinary drag is fallback. No full physics, engine migration or new rig.

## Tooling and continuation

The official Blender MCP trial worked via an isolated diagnostic stdio client, not native Codex registration. Hidden viewport captures could be stale; use direct renders as visual evidence and MCP when live inspection is useful. MCP was not forgotten and is not required for repeatable authoring.

Current scripts: `author_companion_motion.py`, `author_idle_entries.py`, `verify_companion_motion.py`, `preview_companion_motion.py`, `stage_host_motion.py`, `update_host_motion.ps1`. Update staging validates assets before compilation/deployment and preserves a backup. If the current tool-window process cannot close gracefully, close it through its own menu; do not kill unrelated same-name processes. Keep original downloads and all character assets/renders private under ignored `.local/`.

Computer Use capture previously failed with `0x80004002`; no fresh desktop screenshot proof is claimed. This turn's live smoke exercised native rendering through app methods; final visual/input observations still belong to the user. See `ANIMATION-PLAN.md` and `evidence/phase-03-review.md` for artistic work and remaining acceptance.
