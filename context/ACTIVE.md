# Current handoff

**Last completed phase:** 02 - Motion and Windows feasibility, 2026-09-19.

**Status:** Phase 03 ACTIVE. User accepts the idle direction for now and explicitly likes the final 45-frame wave. The user also explicitly requests keeping the desktop app current. Minimal idle/wave/entry integration was brought forward for live Phase 03 review; appearance is still draft, and Phase 04 carry/drag work has not started.

**Current cursor:** The native app is updated and launched at `.local/phase-02/host/StitchPet.exe` (historical path retained for existing launch links). It now has 96-frame idle, 16 short entry variants of four frames each, and the accepted 45-frame wave at 24 fps. Await the user's observation of idle and click transitions at different idle phases. Next: contrast/outline/final 400px appearance work, then synchronize selected renders through `scripts/update_host_motion.ps1` again. Do not leave approved motion in previews only.

## Latest evidence

- `phase-03-runtime-frames.json`: 205 frames validated against manifests, clear alpha borders, exact entry starts at sampled idle poses and exact neutral entry endpoints/wave return.
- Entry sampling measured over all evaluated mesh vertices at all 96 idle phases: maximum projected difference 0.891 pixels at 400px. Eight buckets failed the chosen one-pixel bound (1.682px); sixteen passed. This numerical limit does not prove a perceptually invisible transition.
- `phase-03-host-checks.json`: six groups / 1943 assertions, including all 96 click phases, repeat suppression, idle return, settings, alpha and direct-method Windows layered-window smoke. It is not 1943 independent tests or physical input acceptance.
- `phase-03-host-install.json`: installed executable hash, backup location and frame count. Prior host and settings preserved in `.local/phase-03/host-backup-20260919-142436-346/`; prior 49-frame wave remains `.local/phase-03/wave-v2/`.
- Installed process launched with `motion=phase03-v3 idle=96 wave=45`; its saved 240px size and position were retained. PID file is only a hint; inspect the real process/log before making future claims.
- Current renders are 320px drafts; the 400px option is currently scaled. Do not claim final full-resolution output or professional animation quality from passing checks.

## User feedback and decisions

The user says idle now looks alive and likes the final faster wave. Previous Phase 02 slow/robotic complaints are superseded for this candidate. Previous physical observations confirmed corner pass-through, repeat-click suppression, dragging, sizes, hide/show and persisted geometry. Native interaction needs a short regression observation after this update; exact tray restoration and covered-body counter remain unconfirmed.

Keep the silent offline native C# layered-window host and Blender-rendered frames. Floating above normal apps is the settled scope: no browser hiding or desktop-shell embedding. Position/size/hide/show behavior is retained. Startup, packaging, duplicate-instance protection and recipient Windows 11 acceptance remain later work.

The approved later drag experiment uses authored carry poses, restrained direction/speed response and short settling, only if useful at bounded complexity. Ordinary drag is fallback. No full physics, engine migration or new rig.

## Tooling and continuation

The official Blender MCP trial worked via an isolated diagnostic stdio client, not native Codex registration. Hidden viewport captures could be stale; use direct renders as visual evidence and MCP when live inspection is useful. MCP was not forgotten and is not required for repeatable authoring.

Current scripts: `author_companion_motion.py`, `author_idle_entries.py`, `verify_companion_motion.py`, `preview_companion_motion.py`, `stage_host_motion.py`, `update_host_motion.ps1`. Update staging validates assets before compilation/deployment and preserves a backup. If the current tool-window process cannot close gracefully, close it through its own menu; do not kill unrelated same-name processes. Keep original downloads and all character assets/renders private under ignored `.local/`.

Computer Use capture previously failed with `0x80004002`; no fresh desktop screenshot proof is claimed. This turn's live smoke exercised native rendering through app methods; final visual/input observations still belong to the user. See `ANIMATION-PLAN.md` and `evidence/phase-03-review.md` for artistic work and remaining acceptance.
