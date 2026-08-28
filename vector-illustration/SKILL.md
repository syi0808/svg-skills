---
name: vector-illustration
description: Create, edit, or refine editable SVG illustrations and icons. Coordinate visual planning, direct SVG authoring, optional image-guided enhancement, and rendered review. Use for finished vector artwork or SVG edits, not planning-only requests, faithful raster conversion alone, general UI, or data charts.
---

# Vector Illustration

Build editable vector artwork through semantic planning and rendered feedback.
Adapt the methodology of [Chat2SVG](https://github.com/kingnobro/Chat2SVG), not its
research runtime. The default workflow needs no model API, GPU, or model weights.

## Choose the smallest useful workflow

- **Planning only:** use `illustration-plan` when available and stop at directions
  or a scene plan. Do not produce artwork unless requested.
- **Create:** use `illustration-plan` to choose a visual direction and plan the
  semantic parts before writing SVG. Keep simple plans short.
- **Edit or repair:** inspect the existing source and render first. Preserve its
  IDs, visual style, dimensions, and unaffected parts; do not reconstruct the
  whole illustration to make a local change.
- **Reference-guided:** inspect the supplied image and compare meaningful objects,
  silhouettes, and overlaps. A raster reference is guidance, not the deliverable.
  For faithful raster-to-SVG conversion rather than reference-inspired artwork,
  use `image-to-svg` when available without a new style-planning or image-generation
  pass. Do not reinterpret a conversion brief as permission to redesign.
- **Optimize:** stabilize semantics and topology first. Read
  [advanced-refinement.md](references/advanced-refinement.md) for conservative
  cleanup and the limits of optional image-generation or differentiable backends.

Respect an established icon system or requested renderer. Do not replace a
code-native/vector deliverable with bitmap generation. Do not automatically add
image generation, SAM, DiffVG, or external API calls for a request to polish an SVG.

Read a selected sibling skill's `SKILL.md` from its available location before using
it; do not assume skills are callable programs or live at fixed relative paths.
Only load the skills needed by the current route. If a sibling is unavailable,
use the bundled scene contract and direct authoring/review workflow, preserve the
requested fidelity, and disclose material limitations. Do not install skills or
toolchains automatically. These helpers work without sibling skills installed.

## 1. Plan semantic parts

For new compositions, obtain a `scene.json` from `illustration-plan`. If the brief
already includes a sufficient plan, reuse it; a local SVG edit does not need a new
planning pass. When the planning skill is unavailable, record a concise visual
direction, subject, aspect ratio, background, semantic parts, and constraints using
the bundled [scene-model.md](references/scene-model.md). Ask only about consequential
ambiguities; do not require the user to know style terminology.

New scenes use version 2, `phase: "plan"`, and an `art_direction.description`.
Separate mood, rendering language, and material when useful. Assign stable IDs
such as `rocket.body` and `rocket.window`, but do not invent actual tags or parents
before authoring. Existing v1 bound maps remain valid and need no forced migration.
The scene is an intent and editing contract, not a geometry compiler.

## 2. Construct editable SVG

Read [svg-authoring.md](references/svg-authoring.md) when writing or repairing SVG.
Prefer editable primitives where they fit, and short purposeful paths where they
do not. Keep related parts grouped and paint back to front. Preserve negative
space and intentional asymmetry rather than enforcing
symmetry mechanically.

Produce a standalone SVG with a finite positive `viewBox`, semantic IDs, and
accessible `title`/`desc` where useful. Do not embed a raster to imitate vector work.
Keep an original copy or use separate iteration files before destructive edits.

After authoring, bind a v2 scene by adding actual tags and direct parents, ordering
entries by SVG paint order, and setting `phase: "bound"`. Add meaningful groups and
details as they materialize. Keep the scene and SVG synchronized without storing
coordinates or path data twice. Save candidate scene/SVG pairs separately during
revisions so a rejected change cannot overwrite the accepted plan or artwork.

## 3. Validate, render, and actually look

Resolve `SKILL_DIR` to the directory containing this file, not the current working
directory. All helpers support `--help`. Python 3.10+ is required. Read
[tooling.md](references/tooling.md) for dependencies, the supported static-SVG
profile, exit codes, and comparison details.

```bash
python3 "$SKILL_DIR/scripts/validate_svg.py" artwork.svg --scene scene.json
python3 "$SKILL_DIR/scripts/render_svg.py" artwork.svg --output preview.png --width 1024
```

Use `validate_scene.py scene.json` to check a plan before SVG authoring. An unbound
plan cannot pass `validate_svg.py --scene`; validate the draft SVG alone or finish
its mapping first. Omit `--scene` when no scene file is needed.
Fix validation errors before using the bundled renderer. Its conservative
static-vector profile is not the entire SVG
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

If richer contours or material treatment would benefit from image guidance, read
[image-guidance.md](references/image-guidance.md). Availability alone is not a
reason to generate an image. Inspect any generated candidate before accepting it
as a target; simple SVG corrections should remain direct edits. Use `image-to-svg`
only for an actual selected raster-to-vector reconstruction task. This workflow
owns design decisions, integration, and final candidate selection; sibling skills
do not decide to replace the accepted artwork. Every route ends in SVG validation
and actual rendered review, including when image generation is unavailable.

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
