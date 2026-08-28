# Source-specific conversion decisions

## Flat artwork and low-resolution edges

Read the design behind the pixels. A slightly ragged raster circle is usually a
circle, not a many-node polygon; an intentionally irregular hand-drawn contour is
not. Preserve distinguishing proportions and asymmetry instead of substituting a
generic icon of the same subject.

Sample colors from solid interiors when a pixel-reading tool is available.
Antialiased boundary pixels mix foreground with background and should not become
extra palette entries or permanent halos. Treat JPEG ringing and isolated specks
as possible artifacts, not automatically as source detail. Do not erase small
features that carry identity, such as an eye, letter counter, or deliberate gap.

Transparent pixels can contain invisible RGB values. Inspect the composited
appearance and alpha rather than using those values as visible colors. A baked-in
checkerboard is ordinary image content, not actual transparency; establish whether
the user wants it removed before excluding it.

## Sketches and line art

Use centerline-style strokes for approximately uniform-width lines when they
preserve the source. Use filled outlines for expressive variable-width strokes
when a single SVG stroke cannot reproduce them. Keep line endings and junctions
deliberate, and preserve open contours rather than closing every path.

Avoid tracing both sides of a narrow line as unrelated strokes. For filled
outlines, preserve inner holes and inspect small sizes for blocked gaps. Stroke
caps, joins, and widths matter as much as the centerline position.

## Lettering and logos

Transcribe only legible text. Do not guess tiny labels, invent a brand name, or
replace custom lettering with a vaguely similar font while claiming fidelity.
If exact text is material but unreadable, request a higher-resolution source or
the wording. Preserve letter spacing, alignment, counters, and distinctive marks.

Editable text and portable appearance are different goals. Use SVG `text` when
text editing matters, and disclose required fonts. For fixed logo lettering,
outlined glyphs may preserve appearance better, but they are geometry-editable,
not text-editable. Explain that tradeoff and honor any requested text treatment.
Do not fetch or redistribute font files without checking their availability and
applicable terms. If a renderer substitutes a font, treat it as a fidelity issue.

## Photographs, textures, and soft shading

A photo can be approximated with vector shapes, but a small editable illustration
cannot generally preserve all photographic detail. Establish whether the user
values recognizable structure, a limited palette, or dense visual approximation.
Do not promise lossless recovery of vector geometry from a raster source.

For an agreed simplified reconstruction, keep major silhouettes, relative tone,
lighting direction, and recognition-bearing details. Use a few intentional
gradients for broad shading rather than encoding every pixel. If no useful
approximation meets the brief, explain the limitation rather than embedding the
photo or producing an unrelated stylized substitute.

## Optional local tracing

Check installed tools and their local help before choosing commands; do not assume
a particular tracer or version exists. Match monochrome versus color tracing to
the source and requested result. Work on a copy for any thresholding, denoising,
palette reduction, or alpha preparation; disclose changes that affect appearance.

Automatic contours often do not correspond to semantic objects. Inspect holes,
disconnected islands, transparency, edge halos, and layered color seams. Preserve
the baseline before simplifying nodes and verify that cleanup does not erase
small identity-bearing features. Group or label meaningful contours when useful,
but do not claim automatic semantic decomposition or original-layer recovery.

Treat tracer output as unverified SVG. Validate its structure and references
before rendering. If the bundled validator rejects unsupported features such
as CSS, inspect the generated source and use an appropriate safe renderer or a
verified equivalent rewrite; never strip features blindly to make validation pass.
