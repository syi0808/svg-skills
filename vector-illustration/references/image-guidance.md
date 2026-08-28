# Optional image-guided enhancement

Use this route when a named visual issue would benefit from a generated reference,
not merely because an image-generation skill exists. Simple icons, exact logos,
small local edits, and already satisfactory SVGs usually need direct editing only.
For faithful source conversion, use the supplied image instead of generating a new
target. Respect explicit requests to avoid image generation or external services.

## Choose a bounded enhancement

Keep the best SVG, scene, and preview unchanged. Identify the affected parts,
visible issue, intended improvement, and invariants such as composition, lettering,
palette, background, and untouched IDs. The latest user request and explicit
preservation requirements govern; an agreed plan outranks a generated suggestion.
If the requested direction changed, update the candidate plan deliberately.

Check that the image capability actually supports the needed reference input and
is usable, not just listed. Read its instructions. Pass an inspected PNG render
and the relevant art direction, along with what may change and what must remain.
Use reference-guided image editing when preserving a baseline; do not assume a
text-only generation call preserves its layout. If the available capability cannot
support the required control, use direct SVG edits or report the limitation.

Make additional time, cost, or external upload consequential to the user's choice
explicit before proceeding when not already covered by the request. Do not install
models or invoke a new paid service merely to complete this optional route. Treat
generation as a bounded candidate attempt, not an automatic loop until something
looks attractive. On failure or repeated drift, stop generation and retain the
baseline; continue with direct edits when feasible rather than hiding the failure.

## Inspect before vectorizing

Open the generated image and compare it with the baseline and plan. Reject changed
branding, lost parts, wrong proportions, unwanted cropping, or effects that cannot
be represented within the agreed SVG constraints. Select useful changes by named
part; do not treat the complete generated image as a new source of truth.

For small color, proportion, or curve corrections, edit the original SVG directly.
For genuine raster reconstruction, read the available `image-to-svg` skill and
provide a bounded handoff:

- The actual selected image and its role as generated guidance, not a user original.
- The baseline SVG and scene, when present, with an unchanged backup.
- The selected parts/changes and the IDs, text, layout, and style to preserve.
- Separate candidate output locations and the required canvas/background.

Keep unaffected geometry and IDs rather than rebuilding the whole illustration.
The converter returns a candidate, not a final design decision. If it cannot preserve
the required structure, reassess the change instead of silently losing editability.
If the conversion skill is unavailable, reconstruct selected parts directly under
the same constraints; disclose approximations that matter.

## Accept or revert

Validate the candidate SVG and bound scene, render it, and inspect it at composition
and intended display size. Compare with the best accepted result using the same
renderer and dimensions. Check unchanged parts and references as well as the desired
improvement. Pixel measurements are diagnostic, not an aesthetic acceptance test.

Accept the SVG and scene together only if the selected change is worthwhile and
preservation requirements still hold. Otherwise keep the baseline and explain any
remaining limitation. Count this work within the main workflow's correction budget;
do not restart an unlimited loop by handing control between skills.
