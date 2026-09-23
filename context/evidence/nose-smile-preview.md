# Expressive nose-smile preview — 2026-09-23

## Scope

The user authorized starting the smile preview and added full, sweet eye closure during the smile. This approval applies to the isolated new reaction, not the previously cancelled closed-eye carry effect. The installed gift and all existing action banks remain untouched. Native nose clicks are not implemented at this checkpoint.

## Visual direction and iteration

The expression uses a lifted mouth-corner arc, open-to-closed curved eyelids, a brief full-smile hold and a soft return. A small head roll and ear-tip follow-through keep the face from reading as an isolated mechanical switch. Eye closure starts with the smile, reaches full closure just before the mouth peak and remains closed through that peak. Eyes reopen during the return. No squash of eyeballs, new human-like lips, sound or unrelated gesture.

Existing Chin controls were tried first, as the research recommended. The v1 local-axis lift and v2 pure mesh-space lift both exposed an unwanted lower gum strip in actual renders. These were rejected. The final candidate instead adds one bounded `WarmSmile` relative shape key to the private mesh copy: the mouth surface, teeth and gum components follow the same smooth spatial displacement field. Original basis vertices, topology, weights and UVs are retained. Separate eyes and nose are excluded. This is the previously planned localized fallback, not a whole facial rig.

Four geometric eyelid caps reuse the existing source material and Head weighting, adapting the historical carry-study construction with a raised-center happy seam. Their geometry is animated through per-frame shape samples in the saved preview scene. No closed-eye carry assets are used or installed. A v3 pitch of the head made a small lower-mouth surface visible; v4 removes pitch and keeps restrained roll. Prior v1/v2/v3 outputs are private rejected/intermediate experiments, not deliverables.

## Current artifacts

- Author: `scripts/preview_smile_motion.py`.
- Review/validation: `scripts/review_smile_motion.py`.
- Accepted source: `.local/phase-03/appearance-final/idle/idle.blend`, opened with auto-execution disabled.
- Current private candidate: `.local/phase-09/smile-preview-v4/`.
- `smile-pose.blend`, `neutral.png`, `smile-open.png`, `smile-closed.png`.
- `smile-motion.blend`, 28 transparent PNGs at 400px, 16 Cycles samples, 24fps.
- `smile-motion-review.gif`: 400px light and 240px dark views. The loop adds neutral viewing pauses; these are not reaction frames.
- `smile-contact-sheet.png`: selected transition/hold/return samples.
- `smile-size-review.png`: peak at 400/320/240px.
- Private `pose-checks.json`, `motion-checks.json`, `review-checks.json` record the actual run.

Actual authored duration is 28/24 = 1.167 seconds. If the existing four-frame entry is reused later, total runtime response would be 1.333 seconds. This small increase over the research's initial 24-frame trial budget gives the closure/hold/return room; it is not a global frame-rate or timing change. One 28-frame 400px RGBA bank is approximately 17.09MiB raw; actual packaged/process costs have not been measured because integration has not begun.

## Checks and limitations

The author saves and reopens the Blender scene before rendering animation, checks both endpoint bone matrices against accepted neutral, verifies hidden lids at endpoints, and verifies original geometry/rig/weights/UV/camera preservation and source bytes. The review script checks every frame hash, RGBA dimensions, alpha bounds, exact first/last pixel equality, equality with the standalone neutral render and full GIF decoding/duration. These checks do not establish subjective animation quality, all possible geometric intersections or native transition correctness.

Selected full-closure and in-between frames are visually inspected, including a three-size peak comparison. The user's moving review remains the next quality checkpoint. This preview contains neutral pauses rather than the actual idle-to-reaction entry, and has no native nose-region/drag/interrupt or recipient validation. Do not report it as integrated or accepted before user feedback.

Final v4 execution: all author assertions and review checks passed. All 28 render hashes verified; transparent bounds stay inside the canvas; first/last pixel error is zero and the first frame exactly matches the standalone neutral. The review GIF fully decoded with a 2,500ms loop including pauses. Inspected frames 1/4/6/8/12/17/22/28 and the 400/320/240px peak sheet: full lid closure and the mouth arc are visible; the prominent lower gum exposure from the rejected Chin-only trials is absent in these views. This sampled visual review does not claim every subframe or user-perceived temporal quality has been certified.

The accepted source SHA-256 remains `9c5e27504da499b8659285e8a7f56264caa9baae0ab3a935dc3f3d6cd1cbde90`. Installed executable SHA-256 remains `9560de22be8a5b61a634997fbd5a0b3cfc8318663a9cc1f05059a741643cb360`. Keep all model/render files private and preserve the existing backup directories.

## Next step

Show the v4 moving preview and collect feedback on the smile and closed-eye expression. If accepted, plan the minimal nose-click integration using the existing press-intent/non-drag release and no-overlap policy, with per-idle-phase nose mapping and focused hand/ear/carry regressions. Then deliberately update the gift package after backup. Do not silently integrate this preview or revisit withdrawn ear timing changes.
