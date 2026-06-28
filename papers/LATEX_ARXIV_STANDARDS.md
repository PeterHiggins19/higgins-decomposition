# LaTeX-for-arXiv standard — the locked recipe

*Why this file exists: the publication cycle once stalled for months because the LaTeX never came out
right — charts ran off the page, text rendered microscopic, the output missed the venue's format spec.
P1 compiled and displayed correctly on the first attempt in TeXworks (2026-06-18). This file freezes the
choices that made that work so we never go in circles again. Author: Peter Higgins; AI-assisted per
HUF-STD-001. The reference build is `arXiv/P1_cnq_tiling/latex/` (off-repo; the repo holds the P1 abstract only) — copy it, don't reinvent it.*

---

## The one-line rule

**Start from the working reference build, change only the content, and recompile after every change.**
Do not assemble a new preamble from memory. the off-repo `arXiv/P1_cnq_tiling/latex/main.tex` is the known-good
skeleton; clone it for the next paper.

## The compile recipe (exactly this, in this order)

```
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Four passes: first builds the `.aux`, `bibtex` builds the `.bbl`, the last two resolve all citations and
cross-references. A clean run ends with **no errors and no "undefined references/citations"** in the
`.log`. If either appears, fix it before declaring the build good — a paper that "mostly compiles" is not
done.

## Engine and bibliography — the safe combination

- **Compiler: pdfLaTeX.** This is what arXiv runs. Author and test in pdfLaTeX so the local build and the
  arXiv build are the same engine.
- **Bibliography: `natbib` + `bibtex`** with `\bibliographystyle{plainnat}`. This produces a classic
  `.bbl` with no version coupling. **Avoid `biblatex`/`biber` for arXiv unless you have a reason** — arXiv
  pins specific biber/bbl-format versions (TeX Live 2025 = biber 2.20, bbl format 3.3 *only*), and a
  mismatched `.bbl` is a hard submission error. The reference build uses natbib precisely to dodge this.
- **Always upload the `.bbl`.** arXiv does not reliably re-run bibtex from your `.bib`; it reads your
  committed `.bbl`. Ship `main.bbl` in the submission. (It is already present in the reference build.)

## Figures — the rules that stop "off the page" and "microscopic text"

These three failures (charts off the margin, unreadable text, spec violations) all come from the same
root: a figure sized in absolute units or pasted at native resolution. Fix it at the source.

1. **Size figures relative to the text width, never in absolute cm/pt.** Use
   `\includegraphics[width=0.8\linewidth]{fig.pdf}` (or `\textwidth`). A figure scaled to the line width
   cannot run off the page. **Never** hard-code `width=18cm` on a one-inch-margin page.
2. **Wrap every figure in a `figure` environment with `\centering` and a `\caption`** — not a bare
   `\includegraphics` in the text flow. This is what gives float placement, centering, and a numbered
   caption the venue expects.
3. **Make the text inside the figure large enough at final size.** A plot shrunk to `0.8\linewidth` shrinks
   its fonts too. Author figure label/tick fonts at ~9–11pt *as rendered in the paper*, which usually means
   ~16–20pt in the source plot before scaling. Preview at 100% and read every label. If you cannot read a
   tick label on paper, the reader cannot either.
4. **Vector for plots, raster only for photos.** Save charts as **PDF** (vector — stays crisp at any zoom);
   use **PNG/JPG** only for photographs or bitmaps. With pdfLaTeX the allowed formats are **`.pdf`, `.png`,
   `.jpg` only**.
5. **No `.eps`, no `.ps`.** pdfLaTeX cannot embed them; arXiv will error on `\includegraphics{plot.eps}`.
   Convert to PDF first. (EPS is only for the legacy `latex`→`dvi`→`ps` path, which we do not use.)
6. **Wide tables/figures:** if something is genuinely wide, use a `table*`/`figure*` (two-column spanning)
   or rotate with `\begin{sidewaystable}` (rotating package) — do not let it overflow the margin.

## arXiv-specific gotchas (the automated processor is strict)

- **Upload sources, not a PDF** (arXiv recompiles): `main.tex`, `refs.bib` *and* `main.bbl`, and every
  figure file, in one archive. Do not include `.aux/.log/.out/.blg` — they regenerate.
- **Include the `.bbl`** (restated because it is the single most common bibliography failure).
- **One top-level `.tex`.** If multiple `.tex` files exist, the main file must be obvious (or named so it
  sorts first / declared in `00README.XXX`). The reference build is a single `main.tex` — keep it that way
  unless there is a reason not to.
- **Standard packages only.** The reference preamble — `inputenc, amsmath, amssymb, amsthm, graphicx,
  booktabs, geometry, hyperref, natbib` — is all on arXiv's TeX Live. Exotic packages may not be; if you
  add one, confirm it is in current TeX Live before relying on it.
- **`\usepackage[hidelinks]{hyperref}` loads near-last** (only `natbib` can matter for order); a wrong
  package order is a frequent silent breakage.
- **No absolute paths** in `\includegraphics` or `\input`. Reference files relatively, in the same upload.
- **Bounding box** (only relevant if you ever include PostScript, which we do not): the `%%BoundingBox`
  must be near the file start. The clean fix is: don't use PostScript — use PDF figures.

## Pre-submission checklist (run before handing to Peter)

- [ ] `pdflatex → bibtex → pdflatex → pdflatex` completes with **zero errors**.
- [ ] `.log` shows **no undefined references and no undefined citations**.
- [ ] Every figure is `width=…\linewidth`, inside a `figure` float, with a caption.
- [ ] Every figure's text is readable at 100% zoom on the rendered page.
- [ ] All figures are `.pdf/.png/.jpg`; **no `.eps/.ps`** anywhere.
- [ ] `main.bbl` exists and is current; it is in the upload set.
- [ ] Opened the final PDF in a real viewer (TeXworks/Acrobat) and **eyeballed every page** for overflow,
      cut-off margins, and tiny text — the failure modes that bit us before are visual, so look.
- [ ] Title/section structure matches the target venue's expectations (see
      [`PUBLICATION_FIT_P1_P3.md`](PUBLICATION_FIT_P1_P3.md)).
- [ ] Claim discipline intact: no "lossless"/"identity" at high D, no "first" as fact.

## Minimal known-good skeleton (copy this for a new paper)

```latex
\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage[margin=1in]{geometry}
\usepackage[hidelinks]{hyperref}
\usepackage{natbib}

\title{...}
\author{Peter Higgins\thanks{Human authorship for all claims; AI-assisted per HUF-STD-001.}}
\date{2026}

\begin{document}
\maketitle
\begin{abstract} ... \end{abstract}

\section{Introduction} ...

\begin{figure}[h]\centering
  \includegraphics[width=0.8\linewidth]{fig1.pdf}
  \caption{...}\label{fig:one}
\end{figure}

\bibliographystyle{plainnat}
\bibliography{refs}
\end{document}
```

Compile with the four-pass recipe above. This is the configuration that produced a correct first-attempt
render; treat any deviation as something to justify, test, and — if it works — fold back into this file.

*Status: standing standard. The reference build is `arXiv/P1_cnq_tiling/latex/` (off-repo; the repo holds the P1 abstract only). Update this file only
when a new, tested improvement earns its place.*
