# Approved animation execution plan

Approved sequence: **relaxed stance and idle -> improved wave -> bounded drag/carry reaction experiment**.
Recorded 2026-09-19. The user accepts the refined idle and final 45-frame wave. The 400px appearance candidate is rendered, checked and installed. See [execution evidence](evidence/phase-03-review.md). The user explicitly approved the installed appearance on 2026-09-19; Phase 03 is complete.

## Goal and constraints

Make the existing Stitch feel alive, readable and naturally coordinated at desktop size. User feedback is the starting point: static idle looks robotic; the current wave is too slow and low quality, despite working input behavior.

Keep the supplied model/rig, Blender-authored RGBA frames and the selected native C# host. Full articulated ragdoll, engine migration, roaming, sound and new feature tracks are excluded. The drag experiment is approved to try, not promised as a finished feature regardless of quality or cost. Preserve the working Phase 02 fallback.

Only one phase is active. Complete and report Phase 03 before executing the Phase 04 experiment. Do not require user confirmation for routine posing/rendering choices; request visual feedback at the core-motion checkpoint or when a material design choice cannot be resolved from existing direction.

2026-09-19 user update: the 45-frame wave is now liked/accepted. The user explicitly requires keeping the desktop application current. Bring forward only the idle/wave playback and short-entry integration needed for live Phase 03 review; keep one active phase and leave the Phase 04 carry experiment unstarted. Subsequent accepted assets must go through `update_host_motion.ps1`, not remain preview-only. Preserve the prior installed host in a private backup. This describes the historical pre-appearance checkpoint, now superseded by final acceptance.

## Phase 03 — Core motion and appearance

Completed refinement: existing chest motion increased by 25% and head motion by 20%, with neutral anchoring, timing and the accepted wave preserved. Entries were rebuilt and the desktop app synchronized. Appearance selected soft lower fill, disabled legacy outline and genuine 400px frames. The user approved the installed result on 2026-09-19.

| Step | Work | Output and acceptance evidence | Status |
|---|---|---|---|
| 03.1 Relaxed stance | Inspect the actual pose controls, then soften the shoulders, elbows and hands and introduce restrained asymmetry. Preserve weight and foot contact. Check head/ear/hand clearance before committing to framing. | Low-cost pose comparison at desktop size; a selected relaxed base with recorded reasons and remaining deformation concerns. | COMPLETE: soft pose included in accepted baseline |
| 03.2 Subtle idle | Animate gentle breathing with restrained, offset head/ear motion. Avoid uniform whole-body scaling, constant bouncing or every body part moving together. Do not promise blinking before verifying suitable existing controls. | Repeated moving-loop preview: stable feet, no visible loop hitch, no distracting repetition and no robotic freeze. Inspect timing and seam velocity as well as matching endpoint poses. | ACCEPTED by user: limited chest/head polish; preserve motion |
| 03.3 Better wave | Re-block attention, lift, greeting and return. Adjust spacing and timing within the motion; simply increasing playback FPS is insufficient. Coordinate shoulder, elbow and wrist, then add limited head/ear follow-through. | Moving comparison against Phase 02 showing a more responsive greeting and a readable hand clear of the face/ears. Return must connect to the new relaxed pose. | ACCEPTED: final 45-frame wave; preserved during idle polish |
| 03.4 Appearance and transition review | Refine lower-body contrast on dark backgrounds and settle the outline choice. Keep one consistent camera, framing, scale and foot baseline across clips. Document neutral entry/exit poses and useful idle interruption points. | Idle + wave + return preview on light/dark backgrounds, at the supported 240/320/400 sizes and enlarged for deformation inspection. Frame/preservation checks plus explicit visual observations. | COMPLETE: soft fill, outline off, true 400px; checked and accepted by user |
| 03.5 Core-motion handoff | Present the combined moving preview and ask for targeted feedback on idle, greeting pace and character feel. Resolve reported core defects before an additional motion experiment. | User feedback and its disposition recorded; accepted core assets and known limitations identified. Stop at the Phase 03 handoff. | COMPLETE: explicit final appearance approval recorded |

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

## Phase 04 — Carried-toy response, revised plan approved

The user selected **A: carried toy**, not facing/travelling toward the pointer. They requested research and this plan, then an explicit start approval before implementation. This supersedes the old pickup-only 04A -> directional 04B sequence. Phase 04 remains the only active phase, and the user subsequently approved implementation after a verified full fallback copy. Godot, full articulated ragdoll, throwing and free flight remain excluded.

The old `.local/phase-04/04a/` outputs are a diagnostic pose-transition study. They are not accepted as the requested drag effect and are not a prerequisite for accepting the new direction. Preserve them as evidence, but do not re-present the six wave/idle pickup columns as the primary deliverable. Preserve accepted Phase 03 appearance, idle, wave and installed executable.

### Intended experience

- Once the existing system drag threshold is crossed, the window follows the screen pointer directly. No pickup clip, smoothing controller or frame-selection work may delay location updates.
- The held body gives slightly behind the movement, with restrained head/ear follow-through. On reversal it catches up smoothly; after a stop it briefly settles. This is a stylized weight illusion, not a physics-accuracy claim or an automatic turn toward the travel direction.
- Vertical movement gets a small authored response, not uniform whole-image stretching. Diagonal movement must not trigger abrupt horizontal/vertical mode switches.
- Faster movement produces a stronger but capped response. Small pointer jitter should not shake the character. When held still it returns to a quiet held pose. Release keeps the chosen window position and returns to accepted idle.
- Preserve original click-versus-drag, repeat-click and position-saving behavior. No sound, unrelated gestures, camera orbit or renderer migration. Keep eyes open: the user cancelled the closed-eye experiment after preview.

### Step 04.1 — Causal motion preview (first authorized implementation deliverable)

Create a short private low-cost preview with a **visible pointer/grip marker and moving Stitch together**, using the accepted model, rig, camera, materials and lighting. Show right -> stop -> reverse left -> stop -> up/down -> diagonal -> release, including both slow and faster movement. A roughly 6–10-second review is a planning target, not a final animation duration or a fixed loop to play while dragging.

First demonstrate torso response and subordinate ear follow-through; modest foot response is secondary and must improve the result rather than expand the task. Use a reproducible pointer trajectory and response parameters. Compare against ordinary dragging on the same trajectory so the added weight is visible. The previous static held pose is only an available starting point.

The preview must use a bounded response representation that can plausibly run in the current sprite host. If Blender can produce a convincing curve but the finite frame representation cannot reproduce it, report the difference before native work. Do not silently demonstrate unrestricted live skeletal blending and promise it in the bitmap player.

Prefer a small authored pose/frame bank with bounded transforms as a supplement. Whole-image rotation alone is not the completed effect. Do not crossfade incompatible silhouettes or pre-render every combination of idle phase, wave phase, direction, speed and settle. The exact bank topology is an implementation experiment, not a proven plan assumption.

**Review checkpoint:** ask whether the observed motion conveys a carried toy, whether the strength feels right and whether stopping/reversing feels natural. A second pickup-only preview does not meet this checkpoint. No production render or desktop deployment yet.

The user has accepted directional-v1 strength ("tepkisi ideal"). Preserve its controller and route exactly. The later requested closed-eye refinement was previewed and then explicitly cancelled. Use the original open-eye 45-pose bank from directional-v1; do not carry eyelid geometry, blink frames or eye-state logic into Step 04.2. Eye artifacts are historical evidence only. No additional facial review gate remains. The installed baseline and frozen backup remain unchanged.

### Step 04.2 — Small pointer-controlled native trial

After the motion direction is accepted, use an isolated build of the existing C# host to drive the response with the actual pointer. Keep the accepted installed app intact until the candidate is reviewed. Use a monotonic time base, normalized pointer velocity (displayed-character widths per second), bounded input and time gaps. Start with a small stable response controller; retain motion state through reversals rather than restarting a canned clip at every mouse event. A damped spring or exact exponential response is a candidate mechanism, not a quality guarantee. Tune against the pointer route and actual hand control.

Window displacement remains immediate. Smooth only the visual pose/response. Current `Advance` only presents when the Bitmap reference changes: any continuous visual transform requires redraw invalidation when its parameters change too. Transformed alpha bounds and hit areas must follow the displayed result. Do not increase CPU continuously when the response is at rest.

### Step 04.3 — Grip, interruptions and cost gate

**Grip contract:** retain the current initial pointer/window offset for all ordinary opaque-point grabs. Separately track a reference torso point to evaluate the carried illusion. A fixed torso anchor is not equivalent to fixing any anatomical ear/hand/foot under the cursor. Do not snap the character to a canonical grip point. Test grabs from torso, head, ear and foot regions; if satisfactory anatomical anchoring cannot be achieved with the bounded representation, explicitly describe the limit before changing interaction scope. Arbitrary-ear suspension is not promised.

**Interruption policy:** handle drag beginning in idle, sampled entry, or wave; release during pickup, quick re-grab, reversal and stop while held. No automatic neutral reset or accidental click-wave on release. Choose a bounded policy before expanding the frame bank; the old 563-frame naive expansion is rejected. Preserve the accepted gesture, but do not promise that every wave pose will acquire a full new carry bridge. Document and visually assess the actual compromise if one is needed.

**Proposed acceptance checks (project targets, not universal animation rules):**

- Window follows the pointer on the first handled move past threshold, with no intentional animation wait. Verify in the real trial; do not claim OS event-to-photon latency from a code assertion.
- Preview includes right/left/up/down/diagonal, stop, reverse and release. A slow and faster drag visibly differ without excessive flailing or a flying-character posture.
- Selected torso grip drift target <= 1 displayed pixel at 400px under the intended grip condition. Measure rendered pose plus runtime transform; do not reuse the old 0.080px static-study result as proof. Assess off-center grabs separately.
- Stop/release aims to settle in roughly 0.3–0.6 seconds; movement must terminate rather than oscillate forever. Tune during review; no single-frame reset to force the timing target.
- No conspicuous pose pop, double silhouette or clipped ear/foot at 240/320/400. Numeric endpoints complement actual moving inspection.
- Check wave beginning/peak/return visually. Exercise all 45 wave start states and the current entry states for state-machine correctness during integration; this does not mean rendering 45 new transition clips.
- Capture loss, Alt+Tab, hide/show, resize and re-grab do not leave held/settle state stuck or create a release click. Include tray restoration and the covered-body counter from the existing integration checklist.

**Cost limits:** first preview budget is at most 80 newly rendered unique draft images at 240px/six samples; reuse frames across the longer displayed route. This is a scope control for the experiment, not a quality claim. For a production candidate, target at most 96 added 400px source frames including necessary bridges and release (58.6 MiB of raw 32-bit pixels). This is provisional: if quality needs more, stop expansion and report alternatives rather than quietly relaxing the budget. One 400px bank serves all display sizes. These budgets count total retained additions, not per direction.

Before production calculate exact deduplicated frame count, representative PNG disk size, decoded pixel storage and estimated render time. Measure actual process Working Set, Private Bytes, CPU and GDI-resource trend before/after comparable idle, dragging and repeated interaction runs. Investigate allocation growth if observed; raw pixel arithmetic is not total process RAM. No new profiler framework unless evidence calls for one.

### Step 04.4 — Production, install and handoff

Only after the visual direction, actual pointer control and bounded cost are acceptable, produce native 400px assets, run focused motion/alpha/host checks, back up and update the same installed app. Keep the proven ordinary drag fallback if the effect does not add quality. Record checks, user observations and limits; stop at the Phase 04 handoff. Phase 05 owns startup, duplicate instances and packaging; Phase 06 owns recipient Windows 11 acceptance.

### Research basis and uncertainty

Research refreshed 2026-09-19:

- [Animation Mentor: overlap and pendulum motion](https://www.animationmentor.com/blog/tutorial-overlap-pendulum-motion-animation/) distinguishes lag during base movement from follow-through at a stop and recommends refining offsets against the base trajectory. Application here: visibly connect pointer motion, body response and later ear response. Do not copy tutorial timing values as universal constants.
- [Daniel Holden: Spring-It-On](https://theorangeduck.com/page/spring-roll-call) derives time-dependent damping/spring responses and explains why fixed per-frame blending changes with update rate. Application here: bounded visual state with elapsed time, not a delayed window. No source code copied and no physical-ragdoll claim.
- [Microsoft: MouseCaptureChanged](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.control.mousecapturechanged?view=netframework-4.8.1) documents that Alt+Tab can lose capture without MouseUp. Keep cancellation explicit; the existing host already has a handler to extend.
- Context7 resolved `/websites/blender_api_current`; queried Quaternion.slerp/make_compatible and received [official mathutils documentation](https://docs.blender.org/api/current/mathutils.html). This supports offline pose interpolation, not runtime skeletal blending. Any newly used API still needs verification in installed Blender 5.2.2.
- Prior [GitHub and skill research](evidence/phase-04-drag-research.md) remains relevant for conceptual state separation. No new skill, framework or MCP installation is justified by this correction.

Confidence is high in the intended behavior and the need to preserve immediate pointer control. Confidence is medium in achieving natural, direction-dependent overlap with a small sprite bank and acceptable arbitrary-grab transitions. Step 04.1 and the native trial are intended to resolve those uncertainties, not hide them with extra assets.

## Durable outputs and resumption

This file owns the execution plan; [ACTIVE.md](ACTIVE.md) owns the cursor and [ROADMAP.md](ROADMAP.md) owns phase status. Preserve old 04A evidence as historical diagnostic work. Future direction-based trials belong under ignored `.local/phase-04/`, separately named from `04a`. Code, notes and appropriate evidence belong in Git; models/textures/renders remain private.

**Resume:** native open-eye carry was accepted; the installed native-trial has 400px carry and earlier idle handoff with response parameters preserved. The user now requests controls detached from the character, opened only by tray-icon click. A static tray remote prototype is ready; wait for visual approval BEFORE integration. See ACTIVE.md and [visual checkpoint](evidence/phase-04-tray-visual-prototype.md). Existing host, motion and installed application were not changed in that prototype step. Release-polish user feedback remains open. Do not re-ask for accepted directional motion or cancelled eyes. The original Phase 03 installation and frozen desktop fallback remain intact.
