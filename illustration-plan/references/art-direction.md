# Art direction without a style taxonomy

Use a short description of the desired result, not a rigid catalog of named
styles. Only specify dimensions that affect the user's request:

- Mood: calm, playful, restrained, luxurious, energetic, or unsettling.
- Rendering language: flat silhouettes, line art, cut paper, soft dimensional
  shading, or a more realistic depiction.
- Material: matte, frosted glass, polished metal, paper, fabric, or no explicit
  material treatment.
- Palette and contrast: color relationships, brand colors, light/dark context,
  transparency, and which object carries the focal contrast.
- Detail and lighting: broad silhouettes versus fine contour detail, stroke
  rhythm, light direction, and how much shading survives at the display size.

These are combinable descriptions, not enumerated schema values. For example,
"quiet, spacious, softly dimensional, translucent blue glass with one warm accent"
is more actionable than an unexplained label such as "premium glassmorphism."

## Questions that change the drawing

Ask about use or display size if a tiny icon and a large editorial illustration
would require different silhouettes. Ask about direction when the user is choosing
between materially different treatments, not when a supplied reference already
answers the question. Establish whether a reference is inspiration or a fidelity
target before proposing a redesign. Preserve exact branding and requested wording.

Offer a few short, genuinely different options when asked to explore. Explain
their practical consequences, such as stronger small-size readability or more
material detail. Do not generate a moodboard unless visual generation was part
of the request and an appropriate capability can be used.

## Keep the direction achievable

Editable vector art and dense photographic detail are different priorities.
Prefer broad shading and intentional contours when the user values compact,
editable SVGs. Do not silently flatten the result to a bitmap or simplify away
recognition-bearing features when fidelity was requested.

Transparency and gradients can suggest glass; blur, refraction, and a changing
background may require effects the target renderer or helper profile cannot
support. State that distinction instead of promising a universal glass effect.
If the requirement cannot be met, ask about a meaningful tradeoff or flag the
required renderer work; do not change the user's chosen style to fit the tools.

## Planning economy

Plan recognition-bearing parts and their relationships, not every highlight.
Use stable IDs and short roles; capture attachment, overlap, negative space, and
preservation requirements in prose. Geometry hints are suggestions to the author,
not binding coordinates or a new authoring language. An unresolved assumption is
not user approval, and a later generated image is not authority to change the plan.
