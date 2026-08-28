# Helper tools

Resolve `SKILL_DIR` to this skill's actual directory before running commands.
Inputs are local UTF-8 files; scripts never download assets or install dependencies.
Python 3.10+ is needed. Validation, measurement, and normalization use only the
standard library. Rendering requires an installed `rsvg-convert` or CairoSVG;
comparison requires Pillow.

The bundled `validate_scene.py` checks legacy v1 maps and v2 `plan`/`bound` scenes
without loading SVG. Use it during planning; `validate_svg.py --scene` additionally
requires a bound map and verifies it against the actual SVG. See
[scene-model.md](scene-model.md) for the shared contract and the distinction between
structural checks and visual review.

## Runtime selection

`render_svg.py --backend auto` prefers `rsvg-convert`, then checks CairoSVG in the
current Python interpreter. It does not retry a failed render with a different
backend, because that could conceal an SVG or renderer problem.

If neither is available, report the missing dependency. If installation is
appropriate, use a project-local environment rather than modifying global Python:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install cairosvg pillow
```

CairoSVG also needs a working native Cairo library; consult its
[installation documentation](https://cairosvg.org/documentation/) if import fails.
An already-installed `rsvg-convert` avoids Python rendering dependencies. Compare
with the same backend throughout a regression check. Fonts and masks may vary.
On macOS, if Cairo is installed but cannot be found, locate its library directory
and set `DYLD_FALLBACK_LIBRARY_PATH` for that command only. Do not hardcode another
machine's library path or change the user's global shell configuration.

## Commands

```bash
python3 "$SKILL_DIR/scripts/validate_scene.py" scene.json
python3 "$SKILL_DIR/scripts/validate_svg.py" art.svg --scene scene.json
python3 "$SKILL_DIR/scripts/measure_svg.py" art.svg
python3 "$SKILL_DIR/scripts/render_svg.py" art.svg --output preview.png --width 1024
python3 "$SKILL_DIR/scripts/render_svg.py" art.svg --output small.png --width 32 --backend rsvg
python3 "$SKILL_DIR/scripts/normalize_svg.py" art.svg --output normalized.svg
python3 "$SKILL_DIR/scripts/compare_render.py" before.png after.png --max-rmse 0
```

All successful commands emit JSON. Validation errors or an exceeded comparison
threshold exit `1`; input, dependency, usage, and rendering failures exit `2`.
Output files cannot replace inputs, and existing outputs are refused unless
`--force` is explicit. Preserve a baseline before using that flag on a preview.

The renderer uses a fixed output width (default 1024). Height follows positive
absolute root dimensions when both exist, otherwise the viewBox ratio. Absolute
units use 96 dpi. Percentage or font-relative root sizes use the viewBox fallback.
The report includes the chosen dimensions. Raster output is limited to 8192 per
edge and 16 million pixels, and renderer execution times out after 30 seconds.

## Static-vector preflight profile

The validator checks XML, the SVG namespace, finite geometry, positive viewBox,
path command arity/arc flags, transforms, point lists, duplicate IDs, local
references, reference cycles, and optional scene mappings. It permits basic
shapes, paths, groups, local `use`, gradients, clips, masks, patterns, and text.
Warnings cover missing accessible titles, missing IDs, font dependence, and
unmapped semantic parts.

It rejects DTDs/entities, processing instructions, non-SVG elements, scripts,
event handlers, animation, embedded images, external references, CSS `style`
attributes/elements, and unsupported tags or attributes. Inputs are capped at
5 MiB, 10,000 elements, and 128 levels of nesting. This is a deliberately narrow
authoring profile, not full SVG conformance validation or a security sandbox for
arbitrary hostile uploads. Unsupported features are reported, never stripped.
Keep renderer libraries patched and use an isolated renderer for untrusted assets
outside this profile.

Parsing does not check rendered visibility, actual bounds, typography, masking
semantics, or artistic correctness. The measurement report counts elements,
groups, drawing elements, and path segments; it does not estimate geometric
bounding boxes or rate design quality.

## Pixel comparison

Pillow comparison requires identical image dimensions and never silently resizes.
It measures normalized RGB RMSE after alpha compositing on both black and white,
and reports the larger value as `rmse`, plus separate alpha RMSE. This catches
transparency changes without treating invisible RGB as a visible difference.

`--max-rmse` ranges from 0 to 1; `0` means no visible pixel difference on either
background. Without a threshold it reports measurements only. Different renderers,
fonts, viewport sizes, or antialiasing can produce differences without a semantic
change. No metric replaces opening the render.
