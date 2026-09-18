# Blender MCP and skill evaluation

Date: 2026-09-18. Research followed by a user-approved bounded local trial. Official MCP installed in an isolated Python environment; add-on enabled only in the trial Blender process. No third-party skill pack installed.

## Recommendation

Consider one bounded trial of the official Blender Lab MCP for live scene/pose inspection. Keep the existing background Python/render pipeline for reproducible preparation and rendering. MCP is a development aid, not a dependency of the recipient's desktop companion. Its benefit to iteration speed is plausible but not measured locally (medium confidence).

Do not install a broad third-party Blender skill pack as trusted instructions. Focused motion-review guidance can help, but inspected examples include invalid APIs. Prefer a short project-specific workflow covering the existing rig, blocking, shoulder/wrist deformation, motion arcs, head/ear follow-through, transitions, and visual review at desktop size. This can initially live in project notes; a separate skill is optional.

## MCP evidence and limitations

- [Official Blender Lab MCP](https://www.blender.org/lab/mcp-server/) requires Blender 5.1 or newer and separate add-on, MCP server, and client. Local Blender 5.2.2 LTS meets the declared version floor. This does not prove successful local integration.
- Its documented role is access to Blender's Python API, documentation, and complex scene setups. Its official warning says generated code is not sandboxed. Official origin does not remove that limitation.
- [Official source location](https://projects.blender.org/lab/blender_mcp) was unavailable through the research browser but subsequently accessible through Git. Reviewed the entry point, dependency declarations, add-on registration, socket connection, execution guard, and used tool implementations at release `v1.0.0`, commit `03004fd0216bfe5e0a3d9ac9b47d5efadc3d78c4`. This is a focused source review, not a complete security audit.
- [Third-party ahujasid MCP privacy terms](https://github.com/ahujasid/mcp-for-blender/blob/main/TERMS_AND_CONDITIONS.md) describe default-enabled telemetry, including prompts/code/scene information and possible training/dataset use. The text also contains inconsistent statements about collection after opt-out. Do not treat this as a verified privacy-preserving default or choose it solely for popularity.
- No MCP can establish natural animation quality or Windows desktop behavior by itself. Both require observed results.

## Skills inspected as untrusted reference material

| Candidate | Potential use | Assessment |
|---|---|---|
| [ra100 animation and rigging](https://github.com/ra100/blender-claude-plugin/blob/master/skills/blender-animation-rigging/SKILL.md) | Rig/action/API examples, live inspection workflow | Relevant topic, but invalid API examples verified locally. Do not install unchanged. |
| [arjun988 animation](https://github.com/arjun988/blender-skills/blob/main/.claude/skills/animation/SKILL.md) | Blocking, timing, arcs, overlap, loop review | Useful principles; game export/NLA requirements are not all applicable to pre-rendered sprites. Do not import the entire skill collection. |
| [LevyBytes Blender skill](https://github.com/LevyBytes/AI-SKILL-blender/blob/main/SKILL.md) | Routes to topic-specific Blender documentation | Potential reference aid, not a character-animation solution; detailed subskills not fully audited. |

### Local API spot check

Ran Blender with `--background --factory-startup --disable-autoexec --python-exit-code 1` and read API metadata only. No project/model file was opened or saved. Exit code 0, Blender 5.2.2 LTS.

- `apply_to_basis` is absent from `dir(bpy.ops.pose)`; `armature_apply` is present. The ra100 skill uses `bpy.ops.pose.apply_to_basis()`.
- Constraint type identifiers include `IK`, not `INVERSE_KINEMATICS`. The same skill uses `pose_bone.constraints.new('INVERSE_KINEMATICS')`.
- `FCurveModifiers.new` has one required input, `type`; the skill supplies two positional arguments. This is another API mismatch indicated by introspection; the call itself was not executed.

These are bounded findings about the inspected revision, not a complete audit of any repository. Web main/master branches may change.

## Installation scope if a trial is selected

- Blender add-on belongs in the local Blender environment; server/runtime belongs in isolated local development tooling. Do not vendor an entire MCP repository into the application source or bundle it with the gift.
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli): user `~/.codex/config.toml`, or trusted-project `.codex/config.toml` for project scope.
- [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills): repository `.agents/skills/<name>/SKILL.md` for a project-specific skill.
- This conversation still has the old `Documents/Codex/2026-09-18/se` working directory. The actual repository is on Desktop. Do not assume adding configuration or skills to the Desktop repository makes them discoverable in this conversation; verify the effective workspace and loaded tools explicitly.

## Bounded trial acceptance

1. Inspect the exact official release and local configuration before installation.
2. Establish a localhost connection and enumerate scene/rig data in a copied stage.
3. Inspect one pose and obtain a usable viewport observation; preserve the original assets.
4. Compare iteration effort with the existing script/render workflow. If setup or integration becomes a separate project, stop the trial and retain the working pipeline.
5. Record the observed result before relying on MCP for animation work. No claim that it guarantees professional motion.

## Implementation handoff retained

Audit-maintenance verification now passes for stage SHA-256 `674f2502a45a478a04285d6374904529ab327cd3dffd6aa37d3b88a685332413`. All four decoded RGBA channels are pixel-identical to the backed-up renders at frames 1, 20, and 40, although PNG file hashes differ. Frame 20 was also visually inspected. Rough wave and desktop-host behavior tests have not run.

The Rainmeter 4.5.26 installer was downloaded; SHA-256 is `a3a5579b1b54c03fb5301cad3d68731d3ab4620f6bcb0ba2585ae5823b4187c7` and Authenticode verification is Valid. An attempted portable-install command was rejected by automatic approval review with `blocked by policy`; no more specific reason was provided. Do not retry through another execution path to bypass that rejection. Rainmeter has not been installed or launched.

## Observed trial result

**Outcome: useful for live inspection; retain as an optional development aid.** No new wave or final-quality motion is claimed.

- A real MCP JSON-RPC initialize handshake and tools/list completed over stdio; 26 tools were listed. This was the diagnostic client in `scripts/blender_mcp_call.py`, NOT native tool discovery inside the Codex app. No global or project Codex config was changed, and no restart of this conversation was required.
- MCP called the running Blender add-on successfully: object hierarchy, armature detail, frame changes, and viewport screenshots. Scene inventory confirmed 127 bones and 14,886 vertices.
- Inspected the existing action at frames 1 and 20 using the material-preview viewport and project camera. Character, limbs, ears, and changing mouth/pose were visible. This viewport lighting is not the final Cycles render.
- Example total call times (each includes a fresh stdio server): scene inventory 2.007 s; rig detail 1.512 s; frame-20 change 1.963 s; warm viewport capture 2.081 s. First material-preview capture took 11.850 s including shader preparation. These are observations, not a controlled speed comparison with CLI rendering.
- Confirmed listener address `127.0.0.1:9877`; used stdio rather than the optional HTTP transport. Source HTTP mode disables DNS-rebinding protection and permits all CORS origins; it was not started.
- The inspected execution guard is explicitly weak, not a security boundary. No telemetry endpoint was found in the reviewed bridge/tool execution paths; dependencies and all possible executed Python are not covered by that statement.
- The source stage and trial copy were not saved by the probe. Normal Blender preferences were not changed. Only the isolated `.local/phase-02/mcp-trial/blender-profile` preference file was saved to dismiss first-run splash on restart.
- Cleanup verified: the trial Blender process is closed, port 9877 has no listener, and both stage/copy hashes still equal `674f2502a45a478a04285d6374904529ab327cd3dffd6aa37d3b88a685332413`. Evidence: private `cleanup.json`. The environment/source stay installed locally for reuse.
- Windows Computer Use capture failed with `SetIsBorderRequired failed ... (0x80004002)`; no coordinate input was issued. The MCP viewport capture succeeded independently.

### Problems resolved and exact environment

1. Upstream dependency `mcp[cli]>=1.2.0` selected MCP 2.2.0, which removed `mcp.server.fastmcp`; server import failed. Pinning `mcp[cli]==1.30.0` fixed startup. `pip check` passed.
2. Session-only add-on enabling with `default_set=False` did not create the preferences entry required during registration. `default_set=True, persistent=False` creates that in-memory entry; the normal profile remains isolated by `BLENDER_USER_RESOURCES`.
3. First-run splash obscured the first screenshot. Saved `show_splash=False` only in the isolated profile and restarted using that profile. Usable screenshots followed.

Local source: `.local/runtime/blender-mcp-official` (official v1.0.0). Local Python 3.12 environment: `.local/runtime/blender-mcp-venv`. Installed dependency snapshot and raw responses: `.local/phase-02/mcp-trial/installed-packages.txt` and neighboring JSON/log files. Keep them private, including viewport images and the copied model.

### Resume instructions

From the repository root, run `./scripts/start_blender_mcp_trial.ps1`. The existing isolated profile suppresses the splash. On a fresh machine, clone the exact official tag into the path above, create a venv, then install `mcp[cli]==1.30.0` and the source's `mcp/` subdirectory into that venv. Do not install an unrelated PyPI package based only on the shared name.

Use `.local/runtime/blender-mcp-venv/Scripts/python.exe scripts/blender_mcp_call.py <label> <tool> <arguments-json-file>`. Omit tool/arguments to enumerate tools. Arguments and generated media belong under `.local/`. The client checks protocol `isError` and nested operation status; inspect returned content too, since successful transport alone does not prove a meaningful visual result.

The bootstrap stops its listener after 30 minutes as a fallback. End a deliberate trial by closing only its Blender process after checking the recorded PID, executable, and `stitch-trial.blend` command line; verify port 9877 has closed. Do not close unrelated Blender work. Native Codex integration remains optional and unconfigured; use the verified diagnostic client in this conversation until there is a concrete reason to add it.
