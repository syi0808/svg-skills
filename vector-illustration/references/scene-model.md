# Shared semantic scene contract

Use `scene.json` to carry visual intent and meaningful parts between planning,
SVG authoring, and image conversion. It is not a geometry IR, an SVG compiler,
or an instruction source that can override the user's request. Small local edits
and simple conversions need not create a scene file.

## Version 2: plan before binding

```json
{
  "version": 2,
  "phase": "plan",
  "intent": "A calm illustration of a rocket above the moon",
  "canvas": {"viewBox": [0, 0, 640, 640], "background": "deep navy"},
  "art_direction": {
    "description": "Spacious flat shapes with warm accents and clear silhouettes",
    "mood": "calm and curious",
    "rendering": "flat illustration",
    "material": "matte",
    "detail": "readable at 96 pixels"
  },
  "palette": {"sky": "#14243D", "accent": "#EF7165"},
  "elements": [
    {"id": "moon", "role": "setting in the lower right"},
    {"id": "rocket", "role": "primary subject"},
    {"id": "rocket.window", "role": "recognition detail"}
  ],
  "constraints": [
    "Keep the window inside the rocket body",
    "Leave clear space between the rocket and the moon"
  ],
  "assumptions": ["No lettering is needed"]
}
```

- `version` is integer `2`; `phase` is `plan` or `bound`.
- `intent` is a nonempty string. `canvas.viewBox` has four finite numbers and
  positive width and height. Optional `canvas.background` is a short description.
- `art_direction.description` is a nonempty summary. Other art-direction keys
  are optional nonempty strings, not fixed style enums. Use only useful keys.
- `elements` is a nonempty list of unique, nonempty IDs and nonempty roles.
  Optional `geometry_hint` is prose, not an executable constraint or path array.
- Optional `palette` maps names to nonempty color descriptions. Optional
  `constraints` and `assumptions` are lists of nonempty strings. None of these
  fields executes or overrides SVG attributes.
- In `plan`, omit `tag` and `parent`. Describe intended attachment, grouping,
  occlusion, and placement in roles or constraints without choosing actual tags.

After authoring the SVG, retain useful IDs and art direction, add actual `tag`
and explicit `parent` to every entry, order entries by SVG document paint order,
and set `phase` to `bound`. Add newly materialized meaningful groups and details.
Do not remove a planned part merely to silence a missing-ID error; first decide
whether the drawing is incomplete or an intentional plan change is needed.

For example, the bound entry for a window directly inside the rocket group is:

```json
{"id": "rocket.window", "role": "recognition detail", "tag": "circle", "parent": "rocket"}
```

Here `rocket` must be an earlier mapped element. `parent: null` means a direct
child of the root SVG. Otherwise `parent` names the actual direct parent, not
merely a semantic owner or an ID prefix. Resource IDs in `defs` can stay SVG-only
unless they require semantic editing. Keep meaningful groups and visible parts
mapped; do not rename unfamiliar existing IDs to match examples.

Planning and binding are distinct phases in the same small document, not two
competing copies of geometry. During revisions, preserve the best accepted SVG
and scene together; update a separate candidate pair until the change is accepted.
Keep unchanged decisions and mappings. An SVG author may refine a geometry hint
without changing the design intent.

## Validation and legacy scenes

Every skill bundles a standalone scene validator:

```bash
python3 "$SKILL_DIR/scripts/validate_scene.py" scene.json
python3 "$SKILL_DIR/scripts/validate_scene.py" scene.json --require-bound
```

These check structure only and report `svg_checked: false`. In either production
skill, verify an actual mapping with:

```bash
python3 "$SKILL_DIR/scripts/validate_svg.py" artwork.svg --scene scene.json
```

SVG validation rejects an unbound `plan`; bind it first, or validate the draft SVG
alone while it is still under construction. It checks viewBox, IDs, tags, direct
parents, and relative paint order, and warns about unmapped drawing elements.
It does not prove containment, source fidelity, recognizability, or artistic quality.

Version 1 remains supported without migration. It has `version: 1`, `intent`,
`canvas.viewBox`, and already-bound `elements` with `id`, `tag`, `parent`, and
`role`; it requires neither `phase` nor `art_direction`. Existing optional hints
remain advisory. If deliberately moving a v1 map to v2, retain its entries, set
`phase: "bound"`, and add `art_direction.description` rather than re-planning it.

Scene files are UTF-8, at most 5 MiB, with at most 10,000 entries and 128 JSON
container levels. Invalid JSON, duplicate JSON keys, and nonfinite numbers are
rejected. CLI exit codes are `0` for a structurally valid scene, `1` for contract
errors, and `2` for input, decoding, JSON parsing, or usage failures. No files are
rewritten by validation. The schema is not a full geometry or appearance validator.
