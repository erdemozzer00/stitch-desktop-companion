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

## Next cursor

Obtain moving feedback on this bounded 04A study, particularly raised-hand pickup and the held pose. Do not call it final or install it as the desktop app. If accepted, refine the bounded entry policy/cost and proceed to 04B directional response. Release during pickup, capture loss, re-grab during settle, all 45 wave entry states, arbitrary grip limitations and actual 240/320/400 production alpha checks remain open for integration. Startup, packaging and Windows 11 acceptance remain later phases.
