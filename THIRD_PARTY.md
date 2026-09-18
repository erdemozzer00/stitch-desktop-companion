# Asset provenance

The supplied GLB embeds these credits:

- Title: Stitch
- Author: [AlmondFeather](https://sketchfab.com/almondfeather)
- Source: https://sketchfab.com/3d-models/stitch-5a3f088e9e0e4bcf834f43e94f5329f4
- License label: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

These are embedded metadata, not an independent verification of the author's
rights to the underlying character. The source webpage could not be fetched
during the initial inspection. CC BY-NC allows adaptations and sharing subject
to its terms, including attribution, notice of changes and noncommercial use;
it does not automatically clear other rights.

This public repository contains project records and original preparation code.
It does not redistribute the downloaded model, textures, derived renders,
personal messages or executable gift package. Those files remain in ignored
`.local/`. A future decision to distribute character assets must preserve the
attribution and assess the intended distribution separately. Public source
availability is not a claim of a license to the character or the model.

## Local changes in Phase 01

- Relink the supplied textures and pack used images into a new Blender file.
- Add an orthographic inspection camera and studio lights.
- Disable the legacy Solidify outline modifier in viewport and render because
  its shell caused darkening in the Cycles inspection setup. Preserve the
  modifier and source file; a final outline style is not approved yet.
- Preserve the mesh geometry, bone rest data and existing animation action.
- Render three samples of the existing action; no new animation is claimed.

The input SHA-256 hashes and Blender version are recorded in
`context/evidence/phase-01.json`.
