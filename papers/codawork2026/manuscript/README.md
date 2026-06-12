# Manuscript — Compositional monitoring of energy-mix drift on the simplex

Author: **P. Higgins** · Rogue Wave Audio · Markham, Ontario
Prepared: 2026-05-17 (revision 2 — back-matter restructure + repo-citation consolidation)

This folder holds the publication-grade scientific paper that the CoDaWork 2026 presentation is a condensation of. Per the doctrine reset of 2026-05-17, the paper is the foundation and the talk is the summary, not the other way around.

## What's here

| Path | Purpose |
|---|---|
| [`output/Compositional_Monitoring_2026.docx`](output/Compositional_Monitoring_2026.docx) | **Authoritative submission file** — Word format with figures embedded, references inline, Nature-style structure with three back-matter appendices. |
| [`output/Compositional_Monitoring_2026.pdf`](output/Compositional_Monitoring_2026.pdf) | Read-only circulation copy rendered from the .docx via LibreOffice. |
| [`MANUSCRIPT.md`](MANUSCRIPT.md) | Markdown source of truth. Version-controlled in git. |
| [`SUPPLEMENTARY.md`](SUPPLEMENTARY.md) | Supplementary Information — 9-country corpus tables, sensitivity analyses, reproducibility instructions, cross-AI methodological notes. |
| [`figures/`](figures/) | Five publication figures as both PDF (vector) and PNG (raster). |
| [`build/`](build/) | Build scripts — `build_docx.js` (docx-js producer, alternative path) and figure-generation scripts. Pandoc is the primary build path. |

## Document standard

The manuscript follows the Hˢ Document Standard (internal v1, codified 2026-05-17) which adapts Nature submission conventions to Hˢ working practice:

- **Title** ≤ 90 characters
- **Abstract** 150 words
- **Introduction** blends into text (no separate header)
- **Results** with topical subheadings
- **Discussion** falsifiable defeat paths explicitly listed
- **Methods** placed at end, separate from main word count
- **Appendix A — Equations and Formulas** — formal numbered Eq. 1–10 with full variable definitions; body references each as Eq. N
- **Appendix B — Terms and Definitions** — alphabetical glossary; each entry tagged [std] (standard CoDa), [Hˢ] (specific to this work), or [convention]
- **Appendix C — Figure Conventions and Plate Digest** — universal carrier colour key (table form), plotting conventions, per-figure plate description with source-data path + reproducibility command
- **References — External** — peer-reviewed scholarly literature (numbered list, 28 entries)
- **References — Hˢ Repository** — single grouped reference with transparency note about peer-review status, indexed file paths

The split-references convention is Hˢ-specific. The repository is public and version-controlled, but the documents it contains have not undergone external peer review. Citing them with the same form as peer-reviewed literature would misrepresent their status. The single-table format in the Hˢ Repository references is honest about that.

## Citation conventions

Two citation forms appear in the body of the paper:

- **`[1]`, `[5]`, etc.** — numbered external references. Resolve to *References — External*.
- **`[Repo: name]`** — internal repository references. Resolve to *References — Hˢ Repository*.

Examples: `[1]` is Aitchison (1986); `[Repo: CNT engine]` is the open-source Hˢ CNT engine v3.1.0; `[Repo: INV-050]` is the TV/Aitchison pair-invariance investigation. The reader can verify every internal reference by visiting the repository path listed in the back-matter table.

## Build pipeline

The primary build path is markdown source → pandoc → .docx → LibreOffice → PDF.

```
cd papers/codawork2026/manuscript
pandoc MANUSCRIPT.md \
  -o output/Compositional_Monitoring_2026.docx \
  --resource-path=.:figures \
  --toc --toc-depth=2

python3 ${SKILLS}/docx/scripts/office/soffice.py \
  --headless --convert-to pdf \
  output/Compositional_Monitoring_2026.docx \
  --outdir output/
```

An alternative docx-js build path is preserved at `build/build_docx.js` for cases where finer-grained Word styling control is needed (custom heading styles, manual table widths, etc.). Pandoc remains primary because its output structure is closer to journal-submission expectations.

## What's new versus the abstract

The abstract committed three case countries (Germany, Japan, UK) and three structural findings (continuous arc / Fukushima shock / coal exit). The paper delivers all three case findings plus:

1. The full five-viewpoint protocol (composition timeline, helmsman, helmsman trajectory, Power Share, Activation Coefficient) is the central claim of the paper.
2. The Activation Coefficient is named as a formal diagnostic. The yeast factor metaphor is retained for prose.
3. The cross-country signature across nine countries (the three case countries plus AUS, CHN, FRA, IND, USA, World aggregate) is presented in Fig. 5 and detailed in the Supplementary.
4. The dominant cross-country finding: solar at sub-1% composition share doing 70–85% of structural directional work between 2010 and 2015, peaking at 760× its size.

The MC-4 four-defeat-path structure is preserved verbatim in the Discussion.
The L2→TV metric correction is documented as a methodological-discipline note in the Discussion.

## Relationship to the talk and the community study

Three artefacts now derive from the same data, the same engine outputs, and the same scientific finding:

1. **This manuscript** — the foundation document. Publication-grade. ~14 pages including figures + back-matter.
2. **The 20-slide community study** — `Studies/Energy_HiddenDirections_2026-05-17/Energy_HiddenDirections_2026-05-17.pdf`. Community-friendly tone, full five-viewpoint walkthrough.
3. **The 13-slide CoDaWork talk deck** — `Hs/CODA-Association/CODAwork2026/CodaWork2026_Talk_2026-05-13.pptx`. Conference-format condensation.

The manuscript is the canonical reference; the other two artefacts are condensations for different audiences.

## Status

- Draft 1.1 prepared 2026-05-17 (back-matter restructure + repo-citation consolidation)
- .docx and PDF render and validate cleanly (pandoc + LibreOffice both clean)
- Awaiting Peter's review pass before submission decision

## Citation (suggested)

> Higgins, P. (2026). Compositional monitoring of energy-mix drift on the simplex. Manuscript. github.com/PeterHiggins19/higgins-decomposition.
