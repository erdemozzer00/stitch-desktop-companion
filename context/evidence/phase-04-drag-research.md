# Phase 04 drag research — 2026-09-19

Research only, requested by the user before implementation. Phase 03 is accepted. No new animation, dependency, skill installation, runtime change or desktop deployment occurred in this pass. External skills were assessed as reference material, not adopted as governing instructions. No external project was executed or its code copied.

## Findings and source boundaries

- **VPet: strongest inspected implementation reference.** [Input handling](https://github.com/LorisYounger/VPet/blob/main/VPet-Simulator.Core/Display/Main.xaml.cs) uses a raise anchor, mouse capture and release handling. [DisplayRaised / DisplayRaising](https://github.com/LorisYounger/VPet/blob/main/VPet-Simulator.Core/Display/MainDisplay.cs) separates dynamic carrying, stationary holding and ending animation. Reuse the conceptual state separation, not its framework or full interaction system. Our existing grip offset should remain stable rather than snapping to its fixed raise anchor. Source inspection is not a local test of VPet.
- **Kirby: useful scope contrast.** The [project README](https://github.com/90shree/desktop-pet-kirby) describes pointer-history velocity, throws, gravity and boundary bounce. That is whole-character motion, not proof of articulated ragdoll. Those release-flight behaviors conflict with our place-and-stay gift. README reviewed; implementation not verified or executed.
- **Other candidates:** [TonyNa desktop-pet](https://github.com/TonyNa-code/desktop-pet) advertises movement animation during drag but also substantial chat/UI scope. No reason to migrate our working host. A ShimejiEE API tree request at a presumed master ref returned 404; no implementation conclusion is drawn from it.

## Skill assessment

| Candidate | Inspected material / usefulness | Decision |
|---|---|---|
| [ifBars Blender animation workflow](https://github.com/ifBars/blender-agent-studio/blob/main/plugins/blender-agent-studio/skills/blender-animation-workflow/SKILL.md) | Semantic motion phases, pivots, contact and complete-motion review are useful. Much of the actual file concerns mechanical assemblies, connectors and GLB validation. | Reference only; not a turnkey character-carry solution. |
| [LevyBytes actions-fcurves](https://github.com/LevyBytes/AI-SKILL-blender/blob/main/actions-fcurves/SKILL.md) | A routed Blender documentation reference, not an authored motion generator. The entry file references a local DEVROOT validation tool. | Official docs and our existing scripts already cover the immediate need; do not install the wider package now. |
| [Windows desktop pet builder](https://github.com/Coolkidlab-Yin/windows-desktop-pet-builder/blob/main/skill/windows-desktop-pet-builder/SKILL.md) | [Architecture reference](https://github.com/Coolkidlab-Yin/windows-desktop-pet-builder/blob/main/skill/windows-desktop-pet-builder/references/architecture-and-physics.md) recommends states, timing and aligned anchors, but targets WPF and a much larger fetch/walk/physics feature set. Some smoothing examples use per-update constants despite broader delta-time guidance. | Select principles critically; no WPF rewrite or blanket adoption. |

No inspected skill proves animation quality or removes the need for our rig-specific moving review. This is a bounded assessment of selected files, not a full security, licensing or correctness audit of those repositories.

## Context7 use

Resolved Blender to `/websites/blender_api_current` and Windows Forms to `/websites/learn_microsoft_en-us_dotnet_desktop_winforms`; queried pose/rotation operations, quaternion interpolation and capture behavior. Context7 returned official [Blender mathutils](https://docs.blender.org/api/current/mathutils.html), [pose API](https://docs.blender.org/api/current/bpy.ops.pose.html) and [Microsoft mouse capture](https://learn.microsoft.com/en-us/dotnet/desktop/winforms/mouse-capture-in-windows-forms) sources.

`Quaternion.slerp` supports interpolating rotations, and capture-loss notifications support cancellation. These docs support implementation mechanisms, not artistic quality. The Blender `current` documentation is not a pinned 5.2.2 verification; check any newly used API in the installed executable during implementation. Direct web opens of two .NET API pages failed; do not claim those pages were read successfully. Context7's general capture documentation and existing host code were available.

## Repository-specific recommendation

The current `host/PetSpike.cs` already has a system drag threshold, screen-coordinate grip offset, mouse capture/cancellation and save-on-release. Its playback keeps idle/wave running during ordinary dragging. Extend this small implementation; retain the accepted assets and renderer.

Proposed behavior: `idle/wave -> pickup transition -> held response -> release/settle -> idle`. Dragging moves the window immediately. Only the character response is smoothed. Releasing keeps the user's chosen location; there is no throw or gravity world. This is an authored weight illusion, not a physical ragdoll.

Our runtime displays RGBA frames, not a live skeleton. Blender quaternion interpolation can author frames offline; it cannot blend arbitrary bone poses inside this runtime. A left/right/neutral hard switch would risk popping, and crossfading mismatched silhouettes risks ghosting. The first experiment must measure how many intermediate poses and entry/exit variants are needed before committing to a production asset set. Wave interruption is the highest-risk entry because its pose changes much more than idle.

## Next bounded experiment

1. Preserve Phase 03 and work privately under `.local/phase-04/`. Author one carry pose, restrained left/right responses and a short settle using existing bones, camera and accepted lighting. Keep ear/head follow-through subordinate to the body; no new gestures.
2. Render inexpensive previews for pickup from idle and a representative raised-hand wave pose, direction reversal, stationary holding and release. Assess grip drift, silhouette, deformation and clipping at 240/320/400. Include intermediate transition frames; three isolated poses are not sufficient.
3. If the motion works, trial a bounded continuous response parameter sampled from authored frames. Candidate input is screen-pointer velocity in displayed-character-widths per second, with a monotonic time base, capped time gaps, a quiet zone and smoothing. A possible smoothing rule is `alpha = 1 - exp(-dt/tau)`; constants remain experimental, not universal animation standards. Do not add a physics dependency for this.
4. Resolve arbitrary idle, entry and wave interruption without delaying window movement or popping to neutral. Estimate asset count, memory and render cost. If bridge complexity is disproportionate, retain ordinary dragging rather than silently degrading accepted wave motion.
5. Verify release during pickup, reversal, re-grab during settle, capture loss, hide/resize while held and repeated clicks. Settle must terminate; release must not trigger an accidental wave. Then run the existing focused host checks and remaining tray/covered-body checks.
6. Only after moving review succeeds, render production assets, validate, back up and update the same installed desktop app. Retain ordinary dragging as fallback. No new build is needed for this research-only turn.

Confidence: high that state-based authored carrying fits the existing architecture; medium that a small sprite set will look natural through all interruption cases. Visual quality and production cost remain unproven until the bounded experiment. Windows 11 target acceptance remains a later phase.
