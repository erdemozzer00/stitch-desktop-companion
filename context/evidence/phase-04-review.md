# Phase 04 execution — 04A draft checkpoint

2026-09-19. The user approved 04A then 04B and explicitly cancelled Godot for the current scope. Phase 04 is active, not complete. No change to the installed accepted app.

## Authored output

`scripts/author_carry_preview.py` starts from the accepted appearance scenes. The study uses the existing leg IK controls, modest arm relaxation and restrained head/ear follow-through. It does not add physics, directions, throws or a new rig. Six pickups begin at actual idle frames 1/25/73 and wave frames 4/18/37. Each pickup has ten samples at 24 fps (0.375 seconds between endpoints); the twelve-sample settle returns to accepted neutral (0.458 seconds between endpoints). Held-neutral is intentionally a fixed pose in 04A; directional/secondary motion is deferred to 04B.

Private output: `.local/phase-04/04a/`. There are 72 motion-study PNGs at 240px / six samples, seven transition `.blend` files, separate neutral/held pose studies and two manifests. These are timing drafts using accepted camera/materials/lighting, not production-quality renders.

`scripts/preview_carry.py` generates light/dark six-case GIFs, an all-frame sheet and a self-contained `review.html` with frame stepping and case/background selection. The 320/400 HTML options magnify the 240px draft and are labelled accordingly. A blank, labelled test-reset interval separates repeats; jumping back to a wave source pose is not presented as part of the proposed animation. The orange dot stays at the source torso grip reference to expose drift rather than compensate for it. The review does not simulate a live desktop drag.

## Checks actually completed

- Blender render completed successfully; motion render log ended around 2 minutes 40 seconds on this machine. This low-resolution timing is not a production-render estimate.
- `verify_carry_preview.py` reopened all seven scenes. Every evaluated bone matrix at the start matches its source pose, and every end matches held or idle as appropriate: maximum endpoint matrix error zero. Original action, mesh/rig preservation fields and camera checks passed.
- Source idle/wave file hashes remained unchanged. See manifests for exact hashes.
- `phase-04-preview-checks.json`: all 72 draft alpha borders clear. Selected evaluated front-torso vertex drift is at most 0.080px projected at 400px. This is one anatomical point, not proof for arbitrary ear/hand grabs or every rendered pixel.
- The agent inspected the held render and the sheet containing every transition frame. The raised-hand sample visibly lowers through intermediate poses rather than resetting immediately; no obvious silhouette clipping appears in these sampled views. This is static sequential inspection, not a claim of watching real-time playback or complete self-intersection proof.
- Browser automation rejected opening the local HTML due to URL security policy. No alternate browser route/server was used to bypass it. Interactive HTML behavior and moving aesthetic acceptance remain unverified by the agent; GIFs and local HTML are provided for user review.
- Python/HTML-script syntax and installed-executable preservation are checked separately at this checkpoint. No host interaction suite was rerun because the host was not modified.

## Cost and open design question

The 72 draft PNGs occupy 2.88 MiB on disk. Their raw 32-bit pixels occupy 15.82 MiB at 240px; the same count at 400px would be 43.95 MiB, excluding other allocations. PNG byte hashes are all distinct, including equal-pose renders; production would reuse exact endpoint assets rather than retain noisy duplicate renders.

A naive expansion to 24 idle entry buckets and all 45 wave frames, with eight intermediate frames each, plus a shared held frame and ten settle intermediates, adds **563 unique frames / 343.63 MiB raw at 400px**, before current assets and runtime overhead. Do not adopt that expansion. The experiment demonstrates only six sampled transitions. Before any production work, choose and measure a bounded entry-selection/interruption policy and estimate disk/render costs from representative production-quality samples. This cost is a reason to control the transition design, not to resume Godot work.

One early observation of the existing process (PID 41000) reported Working Set 188,280,832 bytes, Private Bytes 185,057,280 and 261 handles. Later sampling found no StitchPet process, so no controlled multi-sample baseline or CPU comparison was obtained; the cause of process exit was not established. Do not invent a performance delta. The current draft is not loaded in the host. Actual idle/drag/repeated-cycle Working Set, Private Bytes, CPU and native-resource observations belong to a later controlled integration trial.

## Historical next cursor (superseded below)

Obtain moving feedback on this bounded 04A study, particularly raised-hand pickup and the held pose. Do not call it final or install it as the desktop app. If accepted, refine the bounded entry policy/cost and proceed to 04B directional response. Release during pickup, capture loss, re-grab during settle, all 45 wave entry states, arbitrary grip limitations and actual 240/320/400 production alpha checks remain open for integration. Startup, packaging and Windows 11 acceptance remain later phases.

## User correction and replanning — 2026-09-19

The user clarified that the goal is directional carried-toy lag during actual mouse movement, not a new wave or a held-neutral transition study. The user selected direction A and requested a researched plan plus explicit approval before implementation. The old study remains technical evidence only; it did not satisfy the requested visual demonstration. The current cursor is the revised Phase 04 plan in ANIMATION-PLAN.md. No new render or runtime change was made during replanning.

## Verified fallback and directional preview — 2026-09-19

The user authorized implementation, conditional on taking a full desktop copy first. Copied to `C:/Users/Erdem/Desktop/stitch-desktop-companion-ragdoll-illuzyonsuz` before implementation edits. Robocopy copied 22,666 files (1,358,267,049 bytes) including Git history and ignored private assets/tools. All paths, sizes and SHA-256 contents matched. See `phase-04-fallback-backup.json`; the full manifest and restore guide are inside the backup. Additional backup metadata was written after verification. The copy is a frozen development snapshot with the accepted ordinary-drag app, not a packaged release. Earlier diagnostic motion previews remain in it but are not installed. Do not work in or push from the backup.

### Actual requested effect: directional-v1

The revised preview is `.local/phase-04/directional-v1/directional-light.gif` (plus dark version). It shows the same visible pointer trajectory side by side: plain dragging versus a carried-toy response. The 8.5-second route contains slow right movement, stop, faster left reversal, stop, return, upward/downward movement, diagonals and release. The character's anchor follows the recorded pointer immediately; its visual angle and authored ear/head/limb response evolve separately. This is scripted pointer replay, not a native interactive test.

`author_drag_bank.py` creates a bounded 9x5 bank: 45 poses at 240px / six samples using the accepted scene. Horizontal bank state changes head, ears, arms and leg controls; vertical state makes small articulated changes instead of scaling the image. A continuous rotation around the selected front-torso point supplements those poses. `preview_directional_drag.py` applies a critically damped visual controller, uses a slower ear response, selects a discrete bank frame and transforms it around that anchor. The preview has no unrestricted runtime bone blending, crossfaded silhouettes, physics engine, or Cartesian product of wave/idle/drag states.

The neutral bank pose returns to accepted neutral. This first experiment deliberately isolates directional response: wave/idle entry bridges and live hit-area handling are not implemented. Sustained rest uses a neutral pose; accepted animated idle will be reconnected during a later native trial. No deploy/update script was run.

### Evidence and limits

- Nine extreme-pose drafts were inspected before rendering the full 45-pose bank. Fifty-four render invocations in total, 45 retained bank images, within the 80-draft-image scope cap. Bank render finished around 91 seconds; not a 400px production timing estimate.
- `verify_drag_bank.py` reopened the saved blend. Neutral maximum evaluated matrix error was about 5.96e-7, and all 45 manifest anchor positions reproduced exactly. Accepted source hash, original action, mesh/rig preservation fields and camera passed.
- `phase-04-directional-checks.json`: all bank alpha borders clear; transformed characters stay inside the preview panels. Raw selected torso anchor drift across the bank is zero. The inverse affine map fixes that selected point to the pointer, not every possible anatomical grab.
- Max preview body angle about 10.31 degrees. The same analytic route sampled at 120 and 240 Hz differs by at most about 0.109 degrees in the displayed body angle. Constant-target one-step versus two-half-step spring evaluation matched within 1e-12 in a focused check. These measure the controller, not native display latency or visual quality.
- This route uses 15 bank images across 205 displayed samples; the complete bank supports more candidate input states. PNG storage is 1.81 MiB; raw pixels 9.89 MiB at 240px or 27.47 MiB for the same 45 poses at 400px. This excludes future bridges, transient surfaces and app overhead. Do not treat it as a finished production budget or measured process memory.
- Agent inspected extreme poses and a six-moment side-by-side sheet: intended lean and distinct ear/head changes are visible, with no obvious sampled clipping. Full motion acceptance remains user feedback. No new attempt was made to bypass the previously blocked browser-local-HTML policy.
- Python syntax passed; both main and backup executable hashes still match the accepted Phase 03 installation. No native host tests or process benchmark were claimed because the app was not changed or launched.

### Current handoff

Review directional-light.gif or directional-dark.gif: assess whether the right panel conveys the intended carried-toy effect and whether strength/settling feel natural. Preserve the verified backup. After motion-direction acceptance, proceed to the isolated actual-pointer host trial, accounting for redraw invalidation, frame-selection stepping, transformed bounds, off-center grip and interruption policy. Do not treat this preview as integrated or as Phase 04 completion.

## Accepted response and requested closed eyes — 2026-09-19

The user said the response is ideal and requested closing the eyes while carried. This accepts the directional strength; it does not accept a native implementation that has not yet been built. Keep controller values, bank articulation and pointer trajectory unchanged.

Inspection found no shape keys or lid controls. The source mesh contains two disconnected 1,986-vertex eye components; Eye.L/R provide tracking, not closure. `author_carry_eyes.py` adds four spherical lid-cap surfaces weighted to the existing Head bone. They use UV samples from the source material's pale eye surround and dark-blue crease. The original mesh, eyeballs, materials, rig, camera and directional action remain unchanged. This is authored 3D geometry, not a flattened-eye scale effect. A slight curved seam avoids an entirely straight closed-eye line.

Private moving comparison: `.local/phase-04/directional-eyes-v1/carry-eyes-light.gif` and `carry-eyes-dark.gif`. Both columns have identical accepted carry motion; only the right column closes its eyes. The close lasts 0.25 seconds, stays closed while held, and reopens over 0.33 seconds beginning 0.25 seconds after release. These are preview timing choices. Source geometry study renders exposed that the eye socket hides the first half of a full spherical sweep, so the visible closure range was remapped before the final preview.

Checks and limits:

- Blender render completed successfully: seven initial 400px/24-sample geometry study renders, followed by 52 final 240px/six-sample renders (45 closed bank poses plus seven neutral closure states). Final render took about 97 seconds. Initial study images were superseded; the current manifest describes the final 240px files only. Future `author_carry_eyes.py` runs without `--bank` put studies in a separate `study/` subfolder.
- Accepted directional source file SHA-256, mesh/rig preservation fields, action keys and camera are unchanged. `preview_carry_eyes.py` confirms all 205 original pointer/response records exactly match; it imports the unchanged controller rather than duplicating it. All final PNG hashes, transparent borders and replay panel bounds pass.
- Agent inspected initial closure samples, final seven-state closure sheet, and sampled moving comparison. Closed eyes visibly cover the pupils; no conspicuous sampled face or body clipping was seen. This is not full temporal/user acceptance. No native GUI test or production-size movement claim is made.
- The final closed carry bank is intended to replace the open carry bank, not multiply every direction by seven lid states. Its 52 images represent 11.43 MiB of raw pixels at 240px, or a hypothetical 31.74 MiB at 400px before any entry/exit bridges. Historical open-eye comparison assets remain private. Process RAM has not been measured.
- The replay closes and opens near neutral. Its seven neutral samples do NOT solve arbitrary moving eye transitions, interrupted wave entry, capture loss or re-grab. Resolve those in the isolated native trial without delaying window movement or silently multiplying the bank. Keep the 96-frame proposed production cap unless a concrete cost review changes it.
- Python syntax and Git whitespace checks pass. Main and frozen-backup executable SHA-256 remain `d0ac9f4d32bc35a8399d0211fba770e4458e9aed7587cdc981ad4a7f03b27771`. No desktop install, launch or backup modification occurred.

At that checkpoint, facial review preceded Step 04.2. This was superseded by the cancellation below.

## Eye-closure cancellation — 2026-09-19

The user explicitly withdrew the closed-eye request after seeing the preview. The accepted direction is the original open-eye directional-v1 response, at its already approved strength. Do not integrate the eyelid geometry, closure samples or eye-state logic. The scripts, private previews and numeric evidence remain historical experiments, not accepted production inputs. No eye review is pending.

Only canonical scope/handoff records changed for this cancellation. The eye prototype was never installed, so no runtime rollback or new render is needed. Next remains Step 04.2: isolated actual-pointer integration using the original 45-pose open-eye bank, followed by grip/interruption/cost checks. Phase 04 is active; the installed Phase 03 app, frozen fallback and Godot exclusion remain intact.

## Isolated open-eye native trial — 2026-09-19

The user authorized continuing. Implemented `CarryMotion.cs` and an opt-in `--carry=<directory>` path in the existing host. Ordinary launches retain the baseline behavior. The private candidate is `.local/phase-04/native-trial/StitchPet.exe`; it contains 237 accepted 400px idle/wave/entry frames and the original 45 open-eye 240px carry drafts. `stage_carry_trial.py` checks source hashes before copying; no new renders and no eye assets are used. Main installed and frozen-backup executable hashes still equal `d0ac9f4d32bc35a8399d0211fba770e4458e9aed7587cdc981ad4a7f03b27771`.

### Behavior and deliberate limits

- The same native mouse handlers move the window immediately on the first move beyond the existing system threshold. Only visual angle/articulation use the response controller. The C# critically damped body/ear/vertical update keeps the accepted parameters; an independent CSV oracle from the Python preview checks it.
- Idle drag enters through the existing four-frame neutral bridge (about 0.167 seconds). A wave already in progress continues with pointer movement and global swing; its final neutral pose then yields to the carry bank. This intentionally avoids resetting the arm. It does not provide immediate full articulated carry motion from every wave pose; that compromise needs user review.
- A normalized grab pivot preserves the existing pointer/window offset. Re-grab inversely maps the displayed grip to preserve the current affine pose. Residual translation is committed to window location at rest, within integer pixel rounding. Per-bank torso-anchor compensation is supported. Arbitrary ear/hand/foot anatomical pinning remains unproven because those parts deform locally.
- A transparent margin of 35% of character size on every side accommodates rotation about sampled off-center grips. The character itself retains its selected size. Displayed alpha is supplied to the layered window, so the existing native alpha hit-routing mechanism follows the actual transformed bitmap. Physical click-through still needs user testing.
- Release and capture cancellation settle without a click-wave. Hide resets the response; resize cancels a held pointer safely. Transform changes invalidate the display even if the PNG reference stays the same. Held rest reaches an exact neutral response instead of redrawing an infinitesimal rotation indefinitely. Zero-angle rendering uses the simpler translation/resize path.
- Rendering remains draft-quality during carry: 240px/six samples, enlarged at 320/400. Keep production 400px rendering gated on actual-pointer review. No blanket claim of smooth arbitrary input, production quality or Win11 acceptance.

### Checks performed

- Baseline component checks: five groups, 1,941 assertions PASS (`phase-04-baseline-host-checks.json`). These are not independent end-to-end tests.
- Carry component/state/pixel checks: 179,452 assertions PASS (`phase-04-native-component.json`). Most assertions are repeated border-pixel checks, not separate scenarios. Covers all 96 idle starts, every wave frame, four entry frames across all 24 buckets, quick release, no automatic wave, bounded response, stall recovery, re-grab affine continuity and held rest. Nine extreme bank poses at three sizes, four grips and three angles have clear padded borders. Rendered marker checks validate GDI+ transform placement.
- C# response maximum angle error against the accepted 120Hz Python replay is about `3.72e-8` radians, within a `0.00011`-radian bound. This is numeric agreement, not native input latency or visual acceptance.
- `check_carry_trial.ps1 -Live` ran separate baseline and carry processes using real Windows layered-window presentation and direct method calls. Each runs idle, two scripted drag/release routes, cancellation, hide/show and resize, then exits. Both PASS. This is NOT physical mouse injection or menu/tray testing. Timer cadence stretched each nominal 8.5-second route to about 12.8 seconds in these smoke runs; do not call them real-time timing replicas of the GIF. A native rendered transformed PNG was inspected; no desktop screenshot proof is claimed.
- Final cumulative process samples after about 27.8 seconds: baseline CPU 3.016 seconds, carry CPU 4.281 seconds. These are processor-time totals, not whole-machine percentages. Idle samples include startup/JIT variability. A zero-angle drawing fast path reduced the observed extra idle cost in the final run; no universal performance guarantee follows.
- Final private bytes: baseline about 173.60 MiB, carry about 184.45 MiB (about 10.85 MiB difference). Working sets about 176.54 / 188.12 MiB. GDI object count remains 28 throughout both runs. Carry private bytes grew about 0.45 MiB between drag rounds; the harness and logs also allocate. Short runs do not establish leak-free or sustained performance. Raw additional 240px bank storage is 9.89 MiB; a hypothetical 45-frame 400px bank is 27.47 MiB before extra transition assets.
- Compilation treats warnings as errors. Python staging syntax and Git whitespace checks pass. Final component and live reports carry hashes for the tested runtime and check sources.

### Launch and next review

`start_carry_trial.ps1 -DesktopShortcut` launched the separate trial. At the check it was PID 15636, with the visible title `Stitch - taşıma denemesi`, launch log `carry=True`, and probe alignment recorded. Executable SHA-256: `89cfcf24496c1819fca7701edad51d2e0a12779cbaad07a0ed2159ee2c78f506`. PID may become stale. Desktop shortcut: `C:/Users/Erdem/Desktop/Stitch - Tasima Denemesi.lnk`. The existing accepted shortcut/app was not replaced.

The user has been asked to check actual dragging/reversals/stopping, wave-to-carry behavior, quick re-grab, different grips and small/large sizes. Physical feedback is pending. Follow with the remaining grip/interruption/cost gate; retain main installation and frozen fallback until the candidate earns production assets and installation. Do not start Phase 05 or reopen cancelled eye/Godot work.

Primary API references checked for this implementation: [Microsoft GDI+ transformation order](https://learn.microsoft.com/en-us/dotnet/desktop/winforms/advanced/why-transformation-order-is-significant) and [matrix representation](https://learn.microsoft.com/en-us/dotnet/desktop/winforms/advanced/matrix-representation-of-transformations), also queried through Context7; [layered-window alpha hit testing](https://learn.microsoft.com/en-us/windows/win32/winmsg/window-features). These support the API choice, not this app's physical-input acceptance.
