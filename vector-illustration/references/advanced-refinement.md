# Optional refinement and research mapping

Read this for reference-driven enhancement, topology changes, or optimization.
The bundled skill implements the agent-native workflow only. There is no hidden
SDXL, SAM, SVG-VAE, or DiffVG backend, and no equivalent research-quality guarantee.

## Semantic topology refinement

Compare the current render and reference by named parts. First list missing,
extra, disconnected, or incorrectly occluded components. Make a small semantic
diff, for example: add `apple.stem`, reduce `apple.leaf`, move `apple.highlight`
in front of `apple.body`. Update the scene map and SVG together.

Preserve intended connections and object identity. Do not trace every texture
region into a path. A region is worth adding when it improves recognition or a
requested stylistic feature at the delivery size.

## Optional raster guidance

Prefer the user's existing reference. Read [image-guidance.md](image-guidance.md)
only when a generated target could resolve a concrete visual issue within the
request. It covers capability checks, baseline preservation, selected-part
conversion, and candidate acceptance. Generated guidance remains optional; it
does not replace SVG validation or the agent's visual review.

## Conservative optimization

1. Preserve the best reviewed source and render.
2. Remove only proven redundant geometry; preserve meaningful parts and IDs.
3. Do not merge objects, flatten transforms, round coordinates, or remove `defs`
   indiscriminately. Each can break editability, strokes, or references.
4. Render the candidate using the same backend and viewport as the baseline.
5. For serialization-only normalization, require zero pixel difference. For
   geometric simplification, inspect contours and small-scale readability and
   choose a tolerance appropriate to that edit, not a universal quality score.

`normalize_svg.py` does only XML serialization and attribute ordering. It does not
replace a geometric optimizer. If an existing project already uses SVGO, keep
its configuration and test the result; avoid presets that remove semantic IDs.

A separately requested differentiable backend needs a target, verified environment,
cost/time budget, ID-to-path mapping, topology constraints, rollback artifact,
and visual regression check. Stop on failed setup or semantic drift instead of
promising a nonexistent GPU optimization command.

## What is adapted, not reproduced

[Chat2SVG's official repository](https://github.com/kingnobro/Chat2SVG) separates
template generation, diffusion-based detail enhancement, and shape optimization.
This skill retains semantic decomposition and rendered correction. The agent
performs semantic additions instead of requiring SAM segmentation. No upstream
code, prompt templates, pretrained weights, or sample images are bundled.

The [project overview](https://chat2svg.github.io/) describes latent-space and
point-level refinement. Those are optional future integrations here, not features
implemented by these helper scripts. Pixel differences remain regression evidence,
not a substitute for semantic or visual review.
