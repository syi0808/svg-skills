# SVG Skills

An **agent-driven clean-room skill** for creating and refining editable SVG
illustrations through semantic planning, SVG authoring, and rendered visual
review. Here, "clean-room" describes a specification-first development approach,
not a claim of a strictly isolated or legally certified clean-room process.

## Skills

- [Vector Illustration](vector-illustration/SKILL.md): create new SVG artwork,
  refine existing vectors, or develop illustrations inspired by a visual reference.
- [Image to SVG](image-to-svg/SKILL.md): convert a supplied raster image into
  editable vector geometry while preserving its shapes, layout, colors, and
  negative space. Covers semantic reconstruction and optional local tracing, with
  source-to-render review rather than bitmap embedding.

Image to SVG follows the semantic-part and rendered-review approach of Vector
Illustration, with source fidelity rather than new composition as its default.
Each skill includes its own scripts and reference documents and works without the
other skill installed. Helpers are bundled as regular files, not shared symlinks
or cross-skill imports. Python 3.10+ is required; rendering needs `rsvg-convert` or
CairoSVG, and pixel comparison needs Pillow. Image to SVG does not bundle a tracer
or claim lossless conversion of photographs.

## Install with `npx skills`

Use the [Skills CLI](https://github.com/vercel-labs/skills#install-a-skill) to
download and install either skill. You need Node.js/npm (`npx`) and Git for remote
repository installs. The CLI version tested here, `skills@1.5.23`, requires
Node.js 22.20.0 or newer. Installing a skill does not install Python, an SVG
renderer, or Pillow; those remain runtime prerequisites described above.

### From GitHub

Install directly from the public repository
[`syi0808/svg-skills`](https://github.com/syi0808/svg-skills). Remote discovery
and individual installation of both skills were verified on 2026-08-28 with
`skills@1.5.23`.

List available skills without installing:

```bash
npx skills add syi0808/svg-skills --list
```

Install only the skill you need:

```bash
npx skills add syi0808/svg-skills --skill vector-illustration --agent codex --global --copy
npx skills add syi0808/svg-skills --skill image-to-svg --agent codex --global --copy
```

Or install both in one command:

```bash
npx skills add syi0808/svg-skills --skill vector-illustration image-to-svg --agent codex --global --copy
```

`--skill` selects the skill, `--agent codex` targets Codex, and `--global` makes
it available across projects. Omit `--global` for project-local installation.
`--copy` installs regular files rather than agent-directory symlinks. Each
selected skill includes its own `SKILL.md`, `agents/`, `references/`, and
`scripts/`; it does not depend on the other skill or this checkout after install.
Reinstalling can replace a same-name installation, so preserve local edits or
existing development links before doing so.

### From a Local Checkout

Run from this project's root to discover the two skills:

```bash
npx skills add . --list
```

Install either folder independently, or run both commands:

```bash
npx skills add ./vector-illustration --agent codex --global --copy
npx skills add ./image-to-svg --agent codex --global --copy
```

Local installs copy the current files; rerun the relevant command to pick up
development changes. Inspect installed skills with:

```bash
npx skills list --global --agent codex
```

For other coding agents and supported source URLs, see the
[CLI options](https://github.com/vercel-labs/skills#options).

### Usage

For a new illustration:
`$vector-illustration 달 위를 비행하는 로켓 일러스트를 SVG로 만들어줘.`

With a source image attached:
`$image-to-svg 이 이미지를 원본 비율과 색상을 유지한 편집 가능한 SVG로 변환해줘.`

### Repository Layout

Both skill folders and this README live in `syi0808/svg-skills`, with each skill
retaining its own scripts and references. The CLI discovers the existing
`vector-illustration/SKILL.md` and `image-to-svg/SKILL.md` layout; no npm package,
custom installer, or separate skill manifest is needed. Do not add a root
`SKILL.md` that would describe the whole collection as a single skill.

Before sharing future releases, verify remote discovery with
`npx skills add syi0808/svg-skills --list`. Installing from a private fork requires
the user's configured Git credentials.

Local discovery, individual and combined local installation, and individual
GitHub downloads were verified with `skills@1.5.23` in temporary home directories.
Installed scripts, references, and metadata matched the source files. Validation
passed, and each downloaded skill's 96px render matched the existing preview
exactly. The user's existing skill installations were not modified.

### Conversion Test

The [Moon Flight conversion test](examples/moon-flight/image-to-svg-test/test-report.md)
reconstructs the existing PNG without reading its SVG source, then validates the
new vector and compares 768px and 96px renders. The report includes artifacts,
visual corrections, measurements, and the limits of this single-case test.

The development and research notes below describe the original Vector
Illustration skill; Image to SVG adds a source-driven conversion workflow.

## Agent-Driven Development

An AI agent first developed a task-level specification, then turned that
specification into a reusable skill:

1. Identify the high-level workflow ideas relevant to editable vector artwork.
2. Define the skill's requirements, semantic scene model, authoring rules, and
   visual review criteria in a project-specific specification.
3. Implement that specification as skill instructions, reference documents, and
   local validation, rendering, measurement, and normalization helpers.

The intended boundary is to reuse research ideas rather than copy upstream code
or prompt wording. Public Chat2SVG materials were consulted; we do not claim that
the specification and implementation were produced by isolated teams or agents
with no exposure to upstream materials. Complete development provenance has not
been independently verified. The clean-room label is not a guarantee of
non-infringement, a legal opinion, or a substitute for permission where required.

## Research Attribution: Chat2SVG

This project acknowledges **Chat2SVG** as a methodological reference, particularly
for decomposing a scene into meaningful parts and correcting SVG output after
inspecting its rendered appearance. Credit for the original research belongs to
its authors:

**Ronghuan Wu, Wanchao Su, and Jing Liao.**
*Chat2SVG: Vector Graphics Generation with Large Language Models and Image
Diffusion Models.* CVPR 2025.

- [Official repository: kingnobro/Chat2SVG](https://github.com/kingnobro/Chat2SVG)
- [Paper: arXiv:2411.16602](https://arxiv.org/abs/2411.16602)
- [CVPR 2025 paper PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.pdf)
- [Official project page](https://chat2svg.github.io/)

This is not an official Chat2SVG release, and no affiliation with or endorsement
by its authors is claimed. It adapts selected workflow ideas, not the complete
research pipeline or its reported results. The skill does not bundle Chat2SVG
source code, prompt templates, pretrained weights, or sample images, and does not
implement its diffusion, segmentation, or learned SVG optimization backends.
See [the research mapping](vector-illustration/references/advanced-refinement.md)
for the intended scope and limitations.

## License and Reuse Notice

### Chat2SVG Repository

As of **2026-08-28**, the official repository at commit
[`9e609535f97d7aaee1057b93257780f4e98074b2`](https://github.com/kingnobro/Chat2SVG/tree/9e609535f97d7aaee1057b93257780f4e98074b2)
had no explicit repository-wide license identified in the reviewed files, and
GitHub reported its license as `null`.

**Public availability is not a general license to copy, modify, or redistribute
the repository's code, prompts, or assets.** Do not assume that the official
repository is MIT-, Apache-, or otherwise permissively licensed. Attribution in
this README does not grant rights to upstream material or replace any necessary
permission. See [GitHub's licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

### Paper and Other Research Materials

The linked arXiv paper lists the
[arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/).
That grant allows arXiv to distribute the article; it is not a general reuse
license for readers and does not license the GitHub repository. The paper,
figures, project-page assets, model weights, and third-party components must each
be considered under their applicable terms. No rights to those materials are
granted by this project.

### This Project

This project's original materials are licensed under the [MIT License](LICENSE).

Copyright (c) 2026 Yein Sung.

This license does not grant rights to Chat2SVG code, prompts, research materials,
or other third-party content, and is not inherited from Chat2SVG. Third-party
dependencies remain subject to their respective licenses.

Before incorporating upstream code, prompt text, figures, samples, or weights,
verify the terms for the exact material and version, obtain permission where
required, and preserve applicable notices. Recheck upstream licensing if its
status changes; the dated observation above is not a permanent license statement.
