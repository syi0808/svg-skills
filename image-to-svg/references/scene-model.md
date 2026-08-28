# Semantic scene model

For multipart or iterative conversions, keep an optional `scene.json` beside the
SVG. It records the intended parts and editing relationships, not a second
geometry engine or an automatic compiler. Simple conversions need only useful
IDs in the SVG itself.

## Version 1 contract

```json
{
  "version": 1,
  "intent": "Reconstruct a raster bird icon while preserving its silhouette",
  "canvas": {"viewBox": [0, 0, 256, 256]},
  "palette": {"body": "#E9B44C", "eye": "#14243D"},
  "elements": [
    {"id": "bird", "tag": "g", "parent": null, "role": "subject"},
    {"id": "bird.body", "tag": "path", "parent": "bird", "role": "main silhouette"},
    {"id": "bird.wing", "tag": "path", "parent": "bird", "role": "overlapping wing"},
    {"id": "bird.eye", "tag": "circle", "parent": "bird", "role": "recognition detail"}
  ],
  "constraints": ["Keep the eye inside the head and preserve the source margins"]
}
```

- `version` is the integer `1`; `intent` is a nonempty string.
- `canvas.viewBox` contains four finite numbers with positive width and height,
  matching the SVG's viewBox.
- `elements` is a nonempty list in SVG document paint order. Each entry has a
  unique nonempty `id`, actual SVG `tag`, explicit `parent`, and nonempty `role`.
- `parent: null` denotes a direct child of the SVG root. Otherwise `parent` names
  an already listed element that is the actual direct parent in the SVG.
- Include meaningful groups and visible parts. Resource IDs in `defs`, gradients,
  clips, and masks can stay SVG-only unless they need semantic editing.
- Optional `palette`, `constraints`, and per-element `geometry_hint` record
  source observations or intent; they do not execute or override SVG attributes.

The local `scripts/validate_svg.py --scene scene.json` checks the schema, viewBox,
mapped IDs, tags, parents, and relative order. It warns about unmapped drawing
elements. It does not prove containment, recognizability, or faithful geometry.

Keep IDs stable between iterations. When editing a part, preserve its attachment
points and occlusion relationships rather than scaling around the canvas origin.
If the input already has useful IDs, preserve them; do not rename all paths just
to fit the example. Record uncertainty about hidden geometry rather than claiming
to recover the original vector layers from pixels.
