# Licensing — quick answer

This repository is **dual-licensed**. The split is intentional: code and prose answer to different conventions, and forcing one licence onto both creates worse outcomes than splitting them.

## TL;DR

| You want to… | Use this licence | File |
|---|---|---|
| Run, modify, redistribute, or embed any source file (`.py`, `.R`, `.js`, `.sh`, `pyproject.toml`, `requirements.txt`, etc.) | **Apache License 2.0** | [`LICENSE`](LICENSE) |
| Quote, translate, remix, or republish any prose, slide, diagram, or document (`.md`, `.docx`, `.pptx`, `.html`, `.pdf`, narrative `.json`) | **CC BY 4.0** | [`docs/LICENSE-DOCS.md`](docs/LICENSE-DOCS.md) |
| Cite this work in a paper or talk | See attribution block in [`NOTICE`](NOTICE) and [`CITATION.cff`](CITATION.cff) | — |

Both licences are permissive. Both require attribution. Neither restricts commercial use. Both are forever — once granted, they cannot be revoked.

## Why two licences

**Apache-2.0 governs the code** because it is the standard licence for permissive open-source software with patent protection. It includes an explicit patent grant from contributors, a notice-preservation requirement, and is compatible with the mainstream open-source ecosystem (used by NumPy, TensorFlow, Apache Arrow, Kubernetes, and most scientific computing infrastructure). This matters here because the engine produces claim-strength assertions that may eventually map to patentable applied uses (electronics-manufacturing diagnostics, audio diagnostics, ultrasound). The Apache-2.0 patent grant protects everyone downstream from being sued by an upstream contributor.

**CC BY 4.0 governs the documentation** because it is the standard licence for prose and learning materials. CC licences were purpose-built for written content — books, articles, slide decks, diagrams, datasets — and have clean attribution mechanics designed for that medium. Apache-2.0's machinery (notice preservation, source vs object form, patent clauses) fits awkwardly on a paragraph of prose. CC BY 4.0 lets a researcher quote a handbook volume in their own paper or textbook with a simple citation, no NOTICE-file gymnastics required.

**Creative Commons themselves recommend against putting CC licences on software.** Their FAQ ([creativecommons.org/faq](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software)) is explicit: use a software licence for software. The dual structure here follows that guidance directly.

## What's covered by what

### Apache-2.0 ([`LICENSE`](LICENSE))

- All source files: `.py`, `.R`, `.js`, `.sh`
- Build and packaging: `pyproject.toml`, `requirements.txt`, `setup.py`
- Engine schemas embedded in source code
- Everything under `HCI-CNT/engine/`, `HCI-CNQ/engine/`, `HCI-CNQ/scripts/`, `tools/`
- Generated CNT and CNQ output JSONs (they inherit the engine's licence)

### CC BY 4.0 ([`docs/LICENSE-DOCS.md`](docs/LICENSE-DOCS.md))

- All Markdown files (`.md`): READMEs, handbook volumes, AI-refresh narratives, claim-strength tables, notation references, status reports, this file, `NOTICE`
- All slides (`.pptx`)
- All Word documents (`.docx`)
- All PDFs
- All HTML demonstrations
- Prose-form JSON files used as documentation: admin JSONs, the Investigation Catalog, schema documentation

### Other

- **Input CSVs** (Backblaze, Planck, EMBER, etc.) are public datasets under their original upstream licences. See per-experiment `JOURNAL.md` files for upstream attribution.
- **No third-party code is bundled** beyond the dependencies declared in `requirements.txt` and `pyproject.toml`, each retaining its own licence.

## How to attribute

For prose or slides (CC BY 4.0):

> Higgins, P. (2026). *Higgins Decomposition (Hs)*, [section title]. github.com/PeterHiggins19/higgins-decomposition, release v0.29.0. Licensed CC BY 4.0.

For code (Apache-2.0): preserve the `LICENSE` and `NOTICE` files in any redistribution. The Apache-2.0 text spells out the exact mechanics in §4.

For citing the project as a whole in a paper: see [`CITATION.cff`](CITATION.cff). After Paper 1 (INV-026) is on arXiv, please cite the paper as the primary reference and this repository as the reproduction artefact.

## Companion repository

The companion governance / theory repository is the Higgins Unity Framework (HUF):

- [github.com/PeterHiggins19/Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework)

HUF carries its own licence statements; consult that repository directly for its terms.

## Questions

Email [PeterHiggins@RogueWaveAudio.com](mailto:PeterHiggins@RogueWaveAudio.com) (business) or [peterhiggins2016@gmail.com](mailto:peterhiggins2016@gmail.com) (personal). For an attribution edge case where you genuinely cannot tell which licence applies to a specific file (rare — almost everything sorts cleanly by file extension), default to the more restrictive interpretation and ask.
