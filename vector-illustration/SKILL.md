---
name: vector-illustration
description: Create, refine, or repair editable SVG illustrations and icons from text, an existing SVG, or a visual reference. Use for vector artwork that benefits from semantic parts and rendered visual review, not raster-only image generation, general UI implementation, or data-chart generation.
---

# Vector Illustration

Build editable vector artwork through semantic planning and rendered feedback.
Adapt the methodology of [Chat2SVG](https://github.com/kingnobro/Chat2SVG), not its
research runtime. The default workflow needs no model API, GPU, or model weights.

## Choose the smallest useful workflow

- **Create:** identify the subject, parts, layout, and visual language before
  writing SVG. For a small icon, a brief internal plan is enough.
- **Edit or repair:** inspect the existing source and render first. Preserve its
  IDs, visual style, dimensions, and unaffected parts; do not reconstruct the
  whole illustration to make a local change.
- **Reference-guided:** inspect the supplied image and compare meaningful objects,
  silhouettes, and overlaps. A raster reference is guidance, not the deliverable.
  For faithful raster-to-SVG conversion rather than reference-inspired artwork,
  prefer `image-to-svg` when available.
- **Optimize:** stabilize semantics and topology first. Read
  [advanced-refinement.md](references/advanced-refinement.md) for conservative
  cleanup and the limits of optional image-generation or differentiable backends.

Respect an established icon system or requested renderer. Do not replace a
code-native/vector deliverable with bitmap generation. Do not automatically add
image generation, SAM, DiffVG, or external API calls for a request to polish an SVG.

## 1. Plan semantic parts

Record the subject, required components, aspect ratio, palette, stroke language,
background/transparency, and important attachment/occlusion relationships.
Use reasonable defaults when the brief leaves low-impact details open.

For multi-part or iterative work, keep a `scene.json` beside the SVG using
[scene-model.md](references/scene-model.md). Assign stable IDs such as
`rocket.body`, `rocket.window`, and `moon.surface`, and map them to SVG elements.
The scene records intent and relationships; it is not an automatic SVG compiler.

## 2. Construct editable SVG

Read [svg-authoring.md](references/svg-authoring.md) when writing or repairing SVG.
Prefer editable primitives where they fit, and short
purposeful paths where they do not. Keep related parts grouped and paint back to
front. Preserve negative space and intentional asymmetry rather than enforcing
symmetry mechanically.

Produce a standalone SVG with a finite positive `viewBox`, semantic IDs, and
accessible `title`/`desc` where useful. Do not embed a raster to imitate vector work.
Keep an original copy or use separate iteration files before destructive edits.

## 3. Validate, render, and actually look

Resolve `SKILL_DIR` to the directory containing this file, not the current working
directory. All helpers support `--help`. Python 3.10+ is required. Read
[tooling.md](references/tooling.md) for dependencies, the supported static-SVG
profile, exit codes, and comparison details.

```bash
python3 "$SKILL_DIR/scripts/validate_svg.py" artwork.svg --scene scene.json
python3 "$SKILL_DIR/scripts/render_svg.py" artwork.svg --output preview.png --width 1024
```

Omit `--scene` when no scene file is needed. Fix validation errors before using the
bundled renderer. Its conservative static-vector profile is not the entire SVG
standard: do not silently strip unsupported features from user artwork. Explain
the limitation and use an appropriate existing renderer only when that input can
be handled safely.

Open the PNG with an available image-viewing tool. Rendering successfully is not
visual inspection. If the renderer or image viewer is unavailable, state which
check was not performed; do not claim a visually verified result.

## 4. Critique and correct

Use [visual-review.md](references/visual-review.md) to inspect at composition scale
and intended display size. Prioritize missing semantic parts, wrong topology,
occlusion, or proportions before tiny curve adjustments.

For each material defect, record the affected IDs, visible evidence, and intended
correction. Apply a focused edit, revalidate, rerender, and inspect again. Compare
against the best previous version; a revision is not automatically an improvement.
Stop when the brief is met and material defects are resolved, or after three
unproductive correction rounds; retain the best version and report limitations.
Continue beyond that only when the user asks for further iteration.

For small icons, also render at the intended size. For transparent artwork, check
both light and dark surroundings. Fix clipping and invisible strokes in the final
size, not merely in a zoomed preview.

## 5. Clean up only after review

```bash
python3 "$SKILL_DIR/scripts/measure_svg.py" artwork.svg
python3 "$SKILL_DIR/scripts/normalize_svg.py" artwork.svg --output normalized.svg
```

Normalization only serializes XML consistently; it does not simplify geometry or
claim perceptual optimization. Rerender after any cleanup. When comparing two
renders from the same backend at identical dimensions, optionally use:

```bash
python3 "$SKILL_DIR/scripts/compare_render.py" before.png after.png --max-rmse 0
```

Pixel differences can catch unintended changes, not judge design quality or
semantic similarity. Do not optimize toward a metric at the expense of editability.

## Deliver

Return the final SVG path and a rendered preview when available. Include
the scene file for multi-part work and a brief account of what was checked or
remains unverified. Do not flood the user with internal iterations or numerical scores.
Keep the source editable and preserve existing IDs unless the requested edit
actually removes their objects.
