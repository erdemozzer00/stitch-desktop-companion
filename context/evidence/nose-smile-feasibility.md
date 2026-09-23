# Nose-click smile — research handoff, 2026-09-23

## Scope and decision

The user requested internet and visual research into Stitch smiling, and feasibility on the accepted model, followed by a report. This is not authorization to author a new animation, change hit regions or deploy a new app. The later full-access permission allowed blocked local inspection to resume; it did not expand product scope.

Recommendation: a brief, warm, slightly mischievous smile on a non-drag nose click. First review a small facial pose made with existing Chin controls. No whole facial rig, character replacement, Godot migration or new tool installation is justified by current evidence. Confidence is high in the available controls and click-routing architecture, medium in the resulting aesthetic quality until a pose is rendered and reviewed.

## References actually inspected

1. [Disney's original Lilo & Stitch movie page](https://movies.disney.com/lilo-stitch) and its [official hero still](https://lumiere-a.akamaihd.net/v1/images/h_liloandstitch_19755_0999631f.jpeg?region=0%2C0%2C2048%2C878): viewed directly in the browser. Stitch dances with a broad open grin, prominent teeth and round open eyes. The page describes his mischievous character and developing affection/family bonds.
2. [Disney Books: Stitch's Valentine](https://books.disney.com/book/stitchs-valentine-disney-stitch-2/): inspected the actual cover in the browser. Its raised-arm joyful pose again uses a broad toothed grin and open eyes. This is expression reference, not a pose to copy into the pet.
3. [Official Blender shape-key introduction](https://docs.blender.org/manual/en/latest/animation/shape_keys/introduction.html) and [relative shape-key controls](https://docs.blender.org/manual/en/latest/animation/shape_keys/shape_keys_panel.html), retrieved through Context7 `/websites/blender_manual_en`: relative keys can blend facial shape offsets and restrict deformation with a vertex group. This supports a conditional correction fallback, not a requirement to add keys.

Artistic interpretation: preserve Stitch's broad, nonhuman muzzle and visible teeth; lift the corners without pursing human-like lips or stretching the full face. The official references also demonstrate that open eyes can read as happy, so closed eyes are not needed. Their large open mouths are not evidence that this particular desktop model must open its jaw as widely. A restrained version is more proportionate to the user's nose-touch request and the accepted model. Any proposed timing/amplitude below is a trial choice, not an official character standard.

The Disney drawing tutorial was located but not watched; do not cite it as observed animation instruction. No reference images were downloaded into or published with the repository.

## Actual model evidence

Opened `.local/phase-03/appearance-final/idle/idle.blend` in installed Blender 5.2 with file scripts disabled. The accepted 400px `idle_0001.png` was also viewed directly: the existing mouth already shows a narrow line of teeth.

- One character mesh, 14,886 vertices, 14,643 polygons; no shape keys in this saved accepted scene.
- `Chin`, `Chin.L`, and `Chin.R` are unconstrained deform bones with lower-face weights. `Nose`, `Nostril.L/R`, and `Tongue_A` through `Tongue_D` also exist.
- The earlier targeted eyelid/lip/jaw name scan did not include `Chin`; absence of names from that scan was not absence of facial controls. Use this direct inspection for the current decision.
- 26 connected mesh components: main head/body, two eyeballs, nose, twenty repeated 97-vertex mouth components, and two 459-vertex strips. Their arrangement/weights strongly support actual tooth rows and gum strips rather than a solely painted white mouth line. These semantic labels are inferred from geometry, positions and weights.
- Small in-memory translations of each side Chin control moved about 378 vertices, including 81 in the sampled mouth-corner region. No movement was measured in either eyeball, the separate nose or the defined eye-rim sample for these probes. This does not prove all deformations will remain clean at larger amplitudes.
- Side Chin also influences outer lower teeth. Main Chin controls lower mouth/lower teeth. Check tooth alignment, gum visibility and intersections in a rendered pose.
- `Head.R` affects a broad head/ear region; do not assume it is a cheek-only control.

Private reproducible inspection files, intentionally excluded from Git:

- `.local/phase-09/research/inspect_face.py`
- `.local/phase-09/research/face-inventory.json`
- `.local/phase-09/research/probe_face_controls.py`
- `.local/phase-09/research/face-control-probes.json`

Source hash remained `9c5e27504da499b8659285e8a7f56264caa9baae0ab3a935dc3f3d6cd1cbde90`. Numerical probes were transient; no modified scene, smile pose or animation was saved or rendered. Numerical movement is feasibility evidence, not visual approval.

## Proposed bounded implementation, not started

1. On a private copy, try modest bilateral `Chin.L/R` corner lift and minimal main-Chin adjustment. Preserve eyes, nose, materials, camera and lighting. Compare neutral with the smile at 240/320/400px. A smile must be distinguishable from the current toothy resting face without becoming a grimace. Use a localized shape-key correction only if the existing controls visibly prove insufficient.
2. After pose feedback, preview a short reaction: tiny head response, corner lift, brief readable smile and relaxed return. Initial budget is 24 authored frames at 24fps plus the reused four-frame idle entry: about 1.17 seconds total. Timing can change after moving review. Preserve exact neutral endpoints; do not replace the accepted idle or unrelated action banks.
3. Only after visual approval, add the nose to existing press-intent routing. The host currently records intent on press, triggers on non-drag release, maps residual carry transforms back to the sprite and rejects overlapping/queued reactions. Reuse these rules. Nose dragging must remain ordinary immediate dragging, not a smile trigger. A region projected from the actual nose component per idle frame is preferable to a large static face rectangle. Retain hand/ear priority and actual alpha gating.
4. Check all 96 idle phases and three sizes for nose hit alignment, neighboring eye/face misses, press-to-drag cancellation, capture loss, busy clicks, carry interruption and neutral return. Verify wave, peace, ears and tray behavior. Review moving output for teeth/gum clipping, facial pinching, unintended nose/eye motion and entry/exit pops.
5. Only then update the installed personal gift after a verified backup. Keep the previous accepted package recoverable and record user feedback separately from automated checks.

One 24-frame 400x400 RGBA bank is approximately 14.65MiB of raw pixel storage. This is not a prediction of process memory or compressed disk size. Reuse the existing entry bank, scale the same source images to 240/320px and measure actual disk size, Working Set and Private Bytes if integrated; do not multiply banks by display size or add expression combinations speculatively.

## Preserved state and next action

The installed `C:/Users/Erdem/Desktop/Hediye/StitchPet.exe` was read-only hash-checked and remains `9560de22be8a5b61a634997fbd5a0b3cfc8318663a9cc1f05059a741643cb360`. No app code, installed asset, shortcut, startup setting or accepted source was changed. Only research output and project notes were added. App regression tests are not applicable to these documentation-only tracked changes.

Report the result and proposed facial-pose preview to the user. Do not silently begin preview authoring or deployment. The accepted ear timing/no-overlap policy stays in place; the user's superseded speed/overlap request is not pending work.

## Subsequent authorization — 2026-09-23

The user authorized starting the preview and specifically requested sweet, expressive eye closure at the full smile. This supersedes this research's open-eye recommendation for the new smile reaction. It does not restore the cancelled closed-eye carry feature. Author the isolated facial preview using existing Chin controls and adapted geometric eyelids, with visible pose/motion review before integration. The installed gift remains unchanged.
