# SVG authoring decisions

## Structure and editability

- Use `xmlns="http://www.w3.org/2000/svg"` and a positive `viewBox` for standalone SVG.
  Avoid changing the viewBox during a local edit: it changes every object's scale.
- Group a semantic object with `g`; keep independently editable parts separate.
  Preserve painter's order and any IDs used by gradients, masks, or references.
- Prefer presentation attributes in newly authored standalone files. The bundled
  tools deliberately exclude stylesheets, inline CSS, active content, and images.
- Do not flatten user text, remove metadata, or discard CSS just to pass that
  profile. Existing production assets may require a different rendering tool.
- For meaningful standalone artwork, use `title`, `desc`, and `aria-labelledby`
  references. Decorative icons may instead use the caller's accessibility pattern.

## Geometry

Use circles and ellipses for true rounded forms, rectangles for regular blocks,
and polygons for intentionally angular silhouettes. Use Bézier paths for organic
forms and expressive contours. Do not convert everything to paths for consistency.

Put anchors at extrema, corners, and inflections. Keep tangent continuity at
smooth joins. Add a control point only when it gives a needed contour change.
Close filled shapes deliberately; set `fill="none"` on open stroked paths.
Use `fill-rule="evenodd"` for intended compound holes when appropriate.

Fit attachments under the main body with a deliberate overlap to avoid hairline
seams at rasterization. Avoid accidental tangencies: either separate two forms
clearly or make the overlap unmistakable. Do not delete intentional tiny gaps.

Use rounded line caps/joins only when they fit the style. Account for half the
stroke width at the viewBox boundary. Check scaled stroke behavior and transforms
at the actual display size before changing `vector-effect` or coordinate precision.

## Portability

Keep fills and strokes explicit enough to stand alone; `currentColor` can be
appropriate for an app icon but needs its intended host context during review.
Gradients, clipping, and local `use` references are supported by the static
profile, but still require rendering. Masks differ across renderers: inspect
them in the intended target environment rather than assuming identical output.

Text remains editable only if kept as text; rendering depends on fonts. Record
font assumptions and inspect non-Latin labels. Do not promise identical text
layout across renderers or silently substitute outlined text for editable text.

Never hide a PNG inside an SVG and call the result vectorized. If a reference is
too detailed to reproduce economically, simplify with the user's priorities and
disclose the approximation rather than generating thousands of anonymous paths.
