# Semantic scene model

Use this for compositions with multiple meaningful parts or likely follow-up edits.
The model is an editing map and design contract, not a second geometry engine.
For one simple shape, an internal plan and a stable SVG ID suffice.

## Version 1 contract

```json
{
  "version": 1,
  "intent": "A small rocket flying above a crescent moon",
  "canvas": {"viewBox": [0, 0, 512, 512]},
  "palette": {"ink": "#14213D", "accent": "#FCA311"},
  "elements": [
    {"id": "moon", "tag": "g", "parent": null, "role": "setting"},
    {"id": "moon.surface", "tag": "path", "parent": "moon", "role": "crescent silhouette"},
    {"id": "rocket", "tag": "g", "parent": null, "role": "subject"},
    {"id": "rocket.body", "tag": "path", "parent": "rocket", "role": "hull"},
    {"id": "rocket.window", "tag": "circle", "parent": "rocket", "role": "recognition detail"}
  ],
  "constraints": [
    "Keep rocket.window contained within rocket.body",
    "Leave clear space between the rocket and the moon"
  ]
}
```

- `version` is the integer `1`.
- `intent` is a short nonempty description of the requested result.
- `canvas.viewBox` is four finite numbers; its width and height are positive.
- `elements` lists meaningful SVG elements in document paint order. Each entry
  has a unique `id`, actual SVG `tag`, explicit `parent`, and descriptive `role`.
- `parent: null` means a direct child of the root SVG. Otherwise `parent` names
  another mapped SVG element that is the element's direct parent.
- Include all meaningful groups and visible parts. Resource IDs in `defs`, such as
  gradients and clipping paths, can remain SVG-only unless they need semantic edits.
- Optional `palette`, `constraints`, and per-element `geometry_hint` explain
  decisions. They do not execute, enforce constraints, or override SVG attributes.

The validator checks the core schema, the viewBox, mapped IDs, tags, parents, and
relative document order. It warns about unmapped drawing elements. It does not
prove that a window is contained or a silhouette is recognizable.

## Planning decisions that matter

1. Identify recognition-bearing parts before decoration: body, attachment points,
   distinctive cutouts, and expression often matter more than texture.
2. Choose a focal area, approximate bounding boxes, margins, and negative spaces.
3. Establish back-to-front order, including which attachments pass behind a body.
4. Choose one stroke system and a small coherent palette; fit them to the user's
   existing style rather than applying a universal flat style.
5. Map every requested edit to semantic IDs and nearby relationships.

For "make the leaf smaller," scale the leaf around its attachment to the stem,
not automatically around the canvas origin. Keep the stem and unrelated parts
unchanged. If a new highlight is justified, name and add that part deliberately
instead of introducing an anonymous path.

For an existing SVG without a scene file, derive the model from its actual
structure. Preserve existing IDs, including unfamiliar ones. Add semantic names
only when it will not break CSS, references, or callers. Do not rename all paths.
