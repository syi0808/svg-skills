# Local helper tools

This skill bundles all six Python files in `scripts/`, including their shared
`svg_utils.py` module. They are regular files, not wrappers or links to another
skill. Installing or copying this skill folder alone is sufficient to provide the
helpers and their reference documentation. No automatic tracer is bundled.

Resolve `SKILL_DIR` to the directory containing this skill's `SKILL.md`, not the
current working directory. All commands below use only that directory. Scripts
never fetch source images, install dependencies, or locate another skill.

The bundled `validate_scene.py` checks v1 maps and v2 `plan`/`bound` scenes without
loading SVG. `validate_svg.py --scene` requires a bound map and also verifies the
actual SVG IDs, tags, parents, and order. See [scene-model.md](scene-model.md).

## Runtime dependencies

Python 3.10+ is required. Validation, measurement, and normalization use only the
standard library. Rendering requires an installed `rsvg-convert` or CairoSVG in
the selected Python environment; pixel comparison requires Pillow. These runtime
dependencies are separate from skill independence.

`render_svg.py --backend auto` prefers `rsvg-convert`, then checks for CairoSVG in
the current interpreter. It does not retry a failed render with another backend,
which could hide an SVG or renderer problem. CairoSVG also requires a working
native Cairo library. Prefer an already working local renderer; do not modify
global Python or shell configuration to satisfy this skill.

If a dependency is missing, report it and identify the checks not performed.
Dependency installation, when appropriate for the task, should use a local
environment. Do not substitute a remote converter or install another skill.

## Commands

```bash
python3 "$SKILL_DIR/scripts/validate_svg.py" converted.svg --scene scene.json
python3 "$SKILL_DIR/scripts/render_svg.py" converted.svg --output preview.png --width 768
python3 "$SKILL_DIR/scripts/render_svg.py" converted.svg --output small.png --width 96 --backend rsvg
python3 "$SKILL_DIR/scripts/measure_svg.py" converted.svg
python3 "$SKILL_DIR/scripts/normalize_svg.py" converted.svg --output normalized.svg
python3 "$SKILL_DIR/scripts/compare_render.py" source.png preview.png
```

All command entry points support `--help` and emit JSON on success. Omit `--scene`
when no scene file is needed; otherwise follow [scene-model.md](scene-model.md).
Choose preview widths for the actual source and intended display size, rather
than upscaling every small image. Height follows positive absolute root dimensions
when both exist, otherwise the viewBox ratio. Absolute units use 96 dpi;
percentage and font-relative root sizes use the viewBox fallback.

Validation failures or an exceeded comparison threshold exit `1`; input,
dependency, usage, and rendering failures exit `2`. Existing outputs are refused
unless `--force` is explicit; even then an input file cannot be replaced. Preserve
the best version before overwriting previews or normalized files.

The renderer limits each edge to 8192 pixels, total output to 16 million pixels,
and the rendering process to 30 seconds. `measure_svg.py` counts elements, groups,
and path segments; it does not calculate visible bounds or judge quality.
`normalize_svg.py` sorts attributes and serializes XML without simplifying paths
or changing text whitespace. Rerender and inspect after any cleanup.

## Static-vector preflight profile

The validator checks XML, SVG namespace, positive finite viewBox, finite geometry,
path command arity and arc flags, transforms, point lists, duplicate IDs, local
references and cycles, and optional scene mappings. Supported features include
basic shapes, paths, groups, local `use`, gradients, clips, masks, patterns, and
text. Warnings cover missing semantic IDs, accessible titles, unmapped parts,
and font-dependent text.

It rejects DTDs/entities, processing instructions, scripts, event handlers,
animation, raster images, external references, CSS `style` elements/attributes,
and other unsupported elements or attributes. UTF-8 input is limited to 5 MiB,
10,000 elements, and 128 nesting levels. This is a conservative static-vector
profile, not full SVG conformance validation or a sandbox for hostile uploads.
Unsupported features are reported, not stripped. Use an appropriate safe renderer
for artwork outside this profile rather than silently changing its appearance.

Parsing cannot prove visibility, correct occlusion, typography, accurate bounds,
or source fidelity. A successful render likewise does not perform visual review;
open the PNG with an image viewer and disclose any checks unavailable locally.

## Pixel comparison

`compare_render.py` requires Pillow and identical image dimensions, with a
16-million-pixel limit. It never silently resizes. It reports normalized RGB RMSE
after compositing on both black and white backgrounds, their maximum as `rmse`,
and separate alpha RMSE. Invisible RGB values do not count as visible differences.

Without `--max-rmse`, it reports measurements only; `passed: true` does not mean
the reconstruction met a fidelity target. `--max-rmse` accepts a finite value
in 0..1. Reserve a zero threshold for unchanged same-backend renders:

```bash
python3 "$SKILL_DIR/scripts/compare_render.py" before.png after.png --max-rmse 0
```

Match crop, scale, and background before source-to-render comparison. Different
renderers, fonts, or antialiasing can change pixels without changing semantics.
Scores are not similarity percentages and do not judge editability or lettering;
visual source-to-preview comparison remains the primary fidelity check.
