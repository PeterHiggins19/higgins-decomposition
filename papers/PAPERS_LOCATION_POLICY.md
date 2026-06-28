# Papers-location policy — abstracts in the repo, full copies off-repo, mutual citation

*Standing policy for the Hˢ (and HUF/RWA) repositories. Author: Peter Higgins; AI-assisted per HUF-STD-001.*

## The rule

1. **No public repo holds a full copy of any paper or its LaTeX.** The public repos carry **abstracts only**.
2. **The only full copies live off-repo**, in the CoWorker `arXiv/` folder (the single source of truth for
   full text, LaTeX, figures, and the typeset PDFs that go to arXiv).
3. **Bidirectional citation.** The repo abstract cites the published arXiv paper (once live); each paper cites
   the exact Hˢ location where the work was done (engine, experiments, data, conformance). Abstract points
   out to the paper; paper points back to the open work — a closed loop, no duplicated full text on the repos.

## Where each lives

| Paper | Abstract (in this repo) | Full copy (off-repo `arXiv/`) |
|---|---|---|
| P1 exact tiling | `cnq_tiling_suite_2026/P1_ON_HS_ABSTRACT.md`, `P1_ABSTRACT_LOCKED.md` | `arXiv/P1_cnq_tiling/` (+ `latex/`) |
| P2 deceptive drift | `cnq_tiling_suite_2026/P2_ABSTRACT.md` | `arXiv/P2_deceptive_drift/` |
| P3 engine (JOSS) | `cnq_tiling_suite_2026/P3_ABSTRACT.md` | `arXiv/P3_cntt_tool/` |
| P5 character space | `cnq_tiling_suite_2026/P5_ABSTRACT.md` | `arXiv/P5_character_space/` |
| P6 finance | `financial/P6_ABSTRACT.md` | `arXiv/P6_financial/` |
| CoDaWork manuscript | `codawork2026/` (letter+abstract) | `arXiv/codawork2026_manuscript/` |
| P7 foundations (Coda) | `P7_FOUNDATIONS_SEED.md` (seed; not yet a full paper) | — (becomes a full copy when written) |

The **abstract ledger** (`ABSTRACT_LEDGER.md`) is the single in-repo register of all abstracts.

## Exceptions / notes

- **JOSS (P3):** JOSS requires `paper.md` in the software repo at submission. When P3 is submitted, its full
  draft returns from `arXiv/P3_cntt_tool/` to the repo as the JOSS `paper.md`; until then the working copy is
  off-repo, abstract only here.
- **P7** is a living seed that accumulates in-repo as the spine develops; it converts to an off-repo full copy
  only once it is written as a paper.
- When a new paper is drafted: put the full draft in `arXiv/`, leave an abstract here, wire the two pointers.
