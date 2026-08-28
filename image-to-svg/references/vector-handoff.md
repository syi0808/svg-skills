# Bounded conversion within a vector workflow

Read this only when another workflow provides a selected raster target and a
conversion task. The same agent can follow these instructions; skills are not
an automatic program-call interface. Do not recursively invoke planning or the
parent production workflow. The caller owns design choices and candidate acceptance.

## Establish the conversion contract

Inspect the actual image. Establish whether it is a user-supplied fidelity target
or generated guidance, which parts need reconstruction, the output canvas and
background, and what must stay unchanged. Read any provided baseline SVG and scene.
Resolve a consequential conflict between target appearance and preservation rules
before modifying artwork; do not silently choose a new design.

Without a baseline, follow the normal source-faithful reconstruction workflow.
With a baseline, use it as the editable starting point and preserve unrelated
geometry, IDs, paint order, text, resources, and style. Reconstruct only selected
parts and add new semantic IDs deliberately. Do not replace the entire SVG just
because the generated raster contains attractive but unrequested details.

## Return a candidate, not a replacement

Write a separate complete candidate SVG so it can be validated and rendered.
If a scene is present, create its corresponding candidate map and bind any v2 plan
to the actual SVG. Do not overwrite the accepted baseline SVG, scene, or previews.
Validate and inspect the candidate as in the standalone conversion workflow.

Return the candidate paths, changed/added part IDs, meaningful approximations,
and checks performed. Flag unsupported effects or any preservation requirement
you could not satisfy. Do not claim to recover original vector layers from pixels.
The caller compares the candidate with the accepted result and decides whether
to integrate it. No further image generation or orchestration is part of this skill.
