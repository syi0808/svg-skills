# Render-driven visual review

Open the actual render. XML validity and a zero renderer exit code cannot establish
that artwork is visible, balanced, or semantically correct.

## Review in this order

| Category | Visible evidence | First intervention |
| --- | --- | --- |
| Semantic completeness | Missing limb, leaf, window, label, or requested object | Repair the semantic plan, then add the part |
| Silhouette and proportion | Subject is unrecognizable, head/body or object scales conflict | Change major geometry before details |
| Connectivity | Floating handle, detached wing, broken stem | Move the attachment or extend it behind the body |
| Occlusion and z-order | Window behind hull, front object hidden, holes filled | Reorder groups or repair clipping/fill rule |
| Composition | Cropping, weak focal point, crowded margin, competing mass | Reposition or resize whole objects |
| Negative space | Accidental tangent, narrow slit, inconsistent gap | Open a clear gap or commit to an overlap |
| Line and color system | Uneven stroke weight, invisible boundary, competing accents | Adjust the local style system |
| Small-scale readability | Features disappear, gaps merge, strokes blur | Simplify at the intended display size |

Judge intended asymmetry as a design choice, not automatically a defect.
For transparent artwork, inspect against light and dark backgrounds; alpha can
hide a white outline on one surface and expose a dark halo on another.

## Keep corrections accountable

Use a short working note when an iteration needs justification:

```text
ID: rocket.window
Evidence: lower edge is covered by the hull outline at 64 px.
Correction: move the window upward, retaining its radius and semantic ID.
Regression check: body outline, window contrast, moon separation.
```

Prefer a few material fixes to global regeneration. Save the prior best SVG,
render the new one at the same dimensions/backend, and inspect both. Reject
changes that improve detail while harming recognition, composition, or editability.

For target-guided work, separate **semantic differences** (missing/extra objects,
wrong overlap) from **geometric differences** (contour, scale) and **style
differences** (color, line weight). Address them in that order unless the user's
request specifically concerns style.

The comparison script reports pixel change, not an aesthetic or semantic score.
Do not use RMSE to rank differently composed candidates or compare unaligned
references. An empty or incorrect SVG can still match another empty render.

Before delivery, inspect the final post-cleanup render, not an earlier iteration.
Report unresolved limitations or absent rendering/viewing capabilities plainly.
