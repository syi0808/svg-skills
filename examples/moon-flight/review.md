# Moon flight — validation record

Validated on 2026-08-28 using the default agent-native workflow, without image
generation, pretrained weights, or GPU optimization.

## Artifacts

- `artwork.svg`: original editable source; 29 drawing elements, 3 semantic groups,
  and 79 path segments.
- `scene.json`: all 32 meaningful drawing/group IDs mapped in document order.
- `preview.png`: 768 × 768 render; `preview-small.png`: 96 × 96 render.
- `normalized.svg` and `normalized.png`: serialization-only regression candidate.

## Observed checks

- SVG and scene validation complete with no errors or warnings.
- Opened and visually inspected the 768 px and 96 px previews: the rocket remains
  recognizable; fins and flame attach to the hull; the window is contained; moon
  and rocket are separated; crater details stay within the lunar silhouette.
- The orbit passes behind the moon intentionally. Small accent dots are secondary
  details, not required recognition features.
- Rendered with librsvg 2.59.2 and, separately, CairoSVG in an isolated `uv`
  environment. Also opened and inspected the CairoSVG preview.
- Normalization produces RMSE `0` against its baseline on both black and white
  backgrounds, separately for each renderer. Alpha RMSE is also `0`.
- Exercised valid path commands and compact arc flags; local gradients, clips,
  and `use`; malformed paths, transforms, references, and scene mappings;
  external/active SVG rejection; resource limits; input/output protection;
  mixed-text whitespace; alpha-aware comparison; and missing-renderer errors.
- An oversized JSON integer exposed an overflow during validation. Corrected it
  and verified rejection of oversized numbers, nonfinite values, invalid types,
  deeply nested JSON, unsupported encodings, and overflowing absolute units.

This example verifies local tooling and one concrete visual workflow. It does not
establish general design quality, full SVG conformance, hostile-upload isolation,
or equivalence to the Chat2SVG research results. No independent-agent evaluation
was performed.
