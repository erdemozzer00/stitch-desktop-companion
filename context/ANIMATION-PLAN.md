# Approved animation execution plan

Approved sequence: **relaxed stance and idle -> improved wave -> bounded drag/carry reaction experiment**.
Recorded 2026-09-19. Phase 03 implementation is underway. The user reviewed the moving drafts: idle looks alive enough for now, and the wave tempo is liked with a request for a slight speed increase. Preserve idle; retime wave from 49 to 45 frames at 24 fps. See [execution evidence](evidence/phase-03-review.md). Final appearance and transition approval remain open.

## Goal and constraints

Make the existing Stitch feel alive, readable and naturally coordinated at desktop size. User feedback is the starting point: static idle looks robotic; the current wave is too slow and low quality, despite working input behavior.

Keep the supplied model/rig, Blender-authored RGBA frames and the selected native C# host. Full articulated ragdoll, engine migration, roaming, sound and new feature tracks are excluded. The drag experiment is approved to try, not promised as a finished feature regardless of quality or cost. Preserve the working Phase 02 fallback.

Only one phase is active. Complete and report Phase 03 before executing the Phase 04 experiment. Do not require user confirmation for routine posing/rendering choices; request visual feedback at the core-motion checkpoint or when a material design choice cannot be resolved from existing direction.

## Phase 03 — Core motion and appearance

| Step | Work | Output and acceptance evidence | Status |
|---|---|---|---|
| 03.1 Relaxed stance | Inspect the actual pose controls, then soften the shoulders, elbows and hands and introduce restrained asymmetry. Preserve weight and foot contact. Check head/ear/hand clearance before committing to framing. | Low-cost pose comparison at desktop size; a selected relaxed base with recorded reasons and remaining deformation concerns. | COMPLETE: soft pose selected; not final user approval |
| 03.2 Subtle idle | Animate gentle breathing with restrained, offset head/ear motion. Avoid uniform whole-body scaling, constant bouncing or every body part moving together. Do not promise blinking before verifying suitable existing controls. | Repeated moving-loop preview: stable feet, no visible loop hitch, no distracting repetition and no robotic freeze. Inspect timing and seam velocity as well as matching endpoint poses. | DIRECTION ACCEPTED for now: user says idle looks alive; preserve motion |
| 03.3 Better wave | Re-block attention, lift, greeting and return. Adjust spacing and timing within the motion; simply increasing playback FPS is insufficient. Coordinate shoulder, elbow and wrist, then add limited head/ear follow-through. | Moving comparison against Phase 02 showing a more responsive greeting and a readable hand clear of the face/ears. Return must connect to the new relaxed pose. | TEMPO LIKED: small 49-to-45-frame adjustment requested; final review open |
| 03.4 Appearance and transition review | Refine lower-body contrast on dark backgrounds and settle the outline choice. Keep one consistent camera, framing, scale and foot baseline across clips. Document neutral entry/exit poses and useful idle interruption points. | Idle + wave + return preview on light/dark backgrounds, at the supported 240/320/400 sizes and enlarged for deformation inspection. Frame/preservation checks plus explicit visual observations. | NOT STARTED |
| 03.5 Core-motion handoff | Present the combined moving preview and ask for targeted feedback on idle, greeting pace and character feel. Resolve reported core defects before an additional motion experiment. | User feedback and its disposition recorded; accepted core assets and known limitations identified. Stop at the Phase 03 handoff. | NOT STARTED |

### Working method

1. Use copies of the verified Phase 01 stage; inspect the Phase 02 wave for comparison. Preserve source downloads, the verified stage and original action.
2. Work in new named actions and reproducible authoring scripts. Do not overwrite Phase 02 evidence or runtime assets while exploring poses.
3. Use inexpensive pose renders and short timing previews first. Increase render quality only after motion and framing stabilize. The production resolution must support the largest approved host size; do not silently upscale the current 320-pixel draft and call it final.
4. Keep durations and amplitudes as recorded artistic candidates until moving review. Do not invent universal timing/angle rules or guarantee professional quality from successful script execution.
5. Check pose silhouettes, shoulder/wrist deformation and interpenetration in the frames around motion extrema, not only selected keys. Review complete moving loops for acceleration, hesitation and return continuity.
6. Build an entry/exit plan for arbitrary idle timing. The later host integration must not wait an entire idle loop to react or use a conspicuous image crossfade to hide incompatible poses. Validate the chosen small transition strategy before expanding the state logic.

### Phase 03 quality gate

- Idle looks relaxed and alive while remaining quiet enough for continuous desktop use.
- Wave timing addresses the user's slow-motion complaint; the hand is readable at the smallest supported size.
- Feet stay planted where intended; no visible foot sliding, shoulder collapse, wrist kink or hand/ear intersection in reviewed motion.
- Loop and reaction-return transitions have no visible snap or unintended pause. Matching first/last images alone is insufficient.
- Character lighting and transparent edges work on light/dark backgrounds; clipping checks cover all frames and supported sizes.
- Source preservation checks pass for the named mesh/rig/action fields. New checks should follow new risks, not duplicate existing checks without cause.
- The user has reviewed actual moving output. Numeric checks, contact sheets and agent-written pose code do not constitute visual acceptance.

## Phase 04 — Bounded drag experiment, then integration

Start only after the Phase 03 handoff. This section records the approved next dependency, not a second active phase.

1. **Small visual experiment:** author a carry pose, restrained directional responses and a short release/settle action using the existing rig. Whole-image rotation may supplement the authored motion but must not be the entire effect. No limb physics, throws, free flight or collision world.
2. **Minimal live trial:** drive a small set of authored responses from pointer direction/speed. Keep the pointer's grip predictable, limit visual offsets/rotation, and avoid lagging the entire window behind the pointer. Preserve the tested click-versus-drag threshold, mouse capture and saved position behavior.
3. **Interruptions:** verify pickup during idle and during a wave, quick direction reversal, stopping while held, release, capture loss and hiding while held. No pose jumps, accidental click-wave on release, endlessly settling motion or character movement after the drag ends beyond the bounded authored settle.
4. **Go/no-go:** keep the effect only if moving review shows added weight/character without obvious pose popping, rotating-sticker appearance, clipped bounds, difficult grabbing or disproportionate runtime complexity. If the experiment fails, report the reason and retain ordinary dragging; the core gift must remain usable. Do not upgrade to full ragdoll as an automatic fallback.
5. **Integration:** reuse the existing host. Add only the idle/transition/drag behavior that has earned acceptance. Test reactions from several idle positions in the loop and repeated inputs. Recheck transparent hit areas, both size presets, tray-based restoration, covered-body counter behavior and close/relaunch persistence. Tray restoration and the covered-body counter were not separately confirmed in Phase 02.

Later Phase 05 handles startup, duplicate instances, packaging and daily-use reliability. Phase 06 remains actual recipient Windows 11 acceptance. Do not fold these into animation work.

## Durable outputs and resumption

- This file is the execution plan; [ACTIVE.md](ACTIVE.md) is the current cursor and [ROADMAP.md](ROADMAP.md) owns phase status. Update these rather than introducing a second planning system.
- New private assets/previews belong under `.local/phase-03/`; a later drag trial belongs under `.local/phase-04/`. These are planned locations, not existing deliverables.
- Reproducible source scripts belong under `scripts/`. Create `context/evidence/phase-03-review.md` when execution begins, recording compared variants, selected parameters, actual checks and unresolved feedback. Do not pre-fill passing results.
- Keep public Git free of third-party models, textures and rendered character assets. Commit scripts and records at meaningful checkpoints.
- Existing desktop screenshot automation is unreliable on this PC. Use render artifacts for motion review and clearly attributed user observations for native visual/input checks; do not invent automated evidence.
- **Resume using ACTIVE.md:** private timing candidates are in progress. Keep Phase 02 runtime untouched until the motion/transition review is ready.
