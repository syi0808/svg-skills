# Soft 3D Case Study: Mint Gear

The source was a 470 × 474 raster of a mint-green, eight-tooth gear with rounded
tips, a recessed lime ring and center button, and a soft ground shadow. The goal
was to preserve its softly lit, mostly matte finish in editable SVG, not to make
a 3D model. Later feedback changed which background and shadow layers were wanted.
The final SVG and PNG are under `examples/mint-gear/` in the repository checkout;
the methods below do not depend on those files.

## Separate the layers before tuning

- **Form:** Reconstruct the tooth tips and valleys as one Bézier silhouette. Keep
  the ring and button separate and get their proportions and alignment right
  before adjusting lighting.
- **Material and light:** Use a base fill for broad body tone, local gradients for
  the rolling shade on each tooth, and separate controls for the main highlight
  and the weaker light reflected into the shaded edge. Follow the source's light
  direction rather than putting an equally bright highlight on every tip.
- **Contact and environment:** Keep the dark recess at the ring distinct from the
  shadow on the ground. Make the ground shadow and any background independently
  removable. A request for a transparent canvas need not remove the ground shadow
  or the internal shading.

## What changed after the first render

| What we saw | What worked better |
| --- | --- |
| Directional shadows made from shifted copies of the full outline cut off abruptly where a tooth met a concave valley. | Use local gradient fields to position shade on the intended flanks. Reuse the actual contour in an opacity mask to let the deeper part of the shade wrap the tips. When the mask is sampled in steps, inspect for visible bands at zoom; a few large opacity jumps read as stripes. |
| The first pass's weak reflected light barely registered. Narrow, near-white highlights made the next pass look glossy and spotted instead of softly lit. | Keep the weak edge reflection, but give the main highlight a broader, mint-tinted footprint with lower peak opacity and gradual falloff. Compare the width and contrast of the bright region to the source, not just the brightest pixel. |
| The whole SVG looked blurry even though the Bézier silhouette was correct. | Diagnose opacity feathering separately from broad RGB shading. A hard clip confirmed that the mask was widening the edge, but the user wanted some softness. A much narrower contour mask restored it without making the shape look defocused. Check the ring and button boundaries independently; an oversized feather there also softens the whole icon. |
| The user wanted the ground shadow back without a background. | Restore only the shadow group: use overlapping radial ellipses, a broader ambient shadow and a denser core, that reach zero opacity before the canvas edge. Use a low-opacity dark tint rather than colors baked against the original cream background. Composite it over more than one background to catch a halo or a clipped tail. |

The gear's contour mask approximates a short opacity ramp with thin strokes
reusing the silhouette. White strokes extend the mask just outside the shape;
black strokes clipped to the inside lower opacity near the boundary. Keep the
transition monotonic along the edge normal: it should fade in one direction, not
produce a secondary rim. This approach stays editable and uses only the bundled
static-vector profile; no bitmap feather or blur filter is needed.

## Run a focused visual feedback loop

1. Establish a baseline render, then change one thing at a time: the silhouette
   feather, the width and strength of a highlight, or the ground shadow. Preserve
   the last useful render so the comparison shows what the change actually did.
2. Render at intended display size and rerender at a larger size for inspection
   (470px and 940px wide here). Compare the same crop and background. Look at the
   teeth at normal size to judge material and lighting; zoom into tips, valleys,
   and the center ring to catch bands, seams, and a fuzzy edge.
3. On a transparent render, sample alpha across an edge along its normal. Count
   consecutive pixels with `0 < alpha < 255` between the clear exterior and
   opaque interior. Isolate the body or avoid any shadow underneath it so the
   shadow's alpha does not inflate the count. If the source is opaque, judge its
   edge visually or sample the color transition; its alpha is not informative.
4. Check a transparent result over light and dark backgrounds. Check the drop
   shadow for a natural fade to transparent at the canvas borders and make sure
   it is not part of the body mask. Report the observations from actual renders;
   a validator pass or an aggregate pixel error does not assess material fidelity.

In this case, four samples at 470px wide crossed 6–7 partially transparent pixels
with the initial wide feather and 0–1 after switching to a hard clip. With the
final narrow mask they crossed 2px at the top and bottom and 3px at the left and
right, measured before the ground shadow was restored. Those are observations
for this render, not a default target: the feather scales with the SVG, and
pixel counts vary with output size, renderer, and where the contour crosses the
pixel grid.

## Follow-up: Recoloring and local refinements

The follow-up produced a sky-blue body with a lavender center
(`examples/mint-gear/sky-blue.svg` in the repository checkout). The reference
still governed shape, lighting direction, and depth; the palette was the
intentional departure.

### Recolor the whole material ramp

Changing only the base fill would leave mint-colored flanks and reflections on
the blue body. Recolor its midtones, rolled shadows, highlights, and recess as a
set, preserving their relative contrast. Keep gradient positions, stop offsets,
and opacities fixed for the first render so a color change does not also change
the lighting geometry. When the center then changed from lime to lavender,
only its color stops needed replacing. The blue recess belongs to the body;
the silhouette, transparency, and ground shadow stayed untouched.

### Feather the join without merging the forms

When the user asked for a more connected center, widening the button's mask
and lowering the surrounding contrast made the button and ring read as one
surface. That lost a depth cue the reference clearly had. Restore the
last faithful shape and shading, then soften just the button's outer edge with
a short radial opacity ramp. In this case the over-blended ramp was about
14 viewBox units wide; the correction used about 3.4 at the same scale, leaving
the visible button and the ring's highlight and shadow intact. Check the color
transition across an internal join, not the rendered alpha: the ring behind
the button keeps those pixels opaque.

### Review concave valleys separately from tooth tips

Reviewing the tips alone missed pale light between the top and upper-left
teeth and between the upper-left and left teeth. Shift and rotate existing local
gradient fields toward the lit flanks of those valleys, then taper their opacity
into the body. Avoid adding a hard light-colored stroke or repeating a bright
spot in every valley. When the palette differs from the source, compare where
the light sits and how it falls off relative to neighboring midtones, not exact
RGB values or background-mixed edge pixels.

For these local edits, compare the result to both the source and the last
accepted render. An SVG diff confirms which controls changed; a pixel diff
rendered at the same size with the same renderer can confirm that pixels
outside the intended region and the alpha channel did not change.
