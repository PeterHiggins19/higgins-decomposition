# Mirror-deletion list — files that must be removed from the public mirror (Peter commits)

*Why this exists: this session moved full papers off-repo with `mv`. Files that were **untracked** simply
vanished (never on the mirror). But files that were **tracked at the last push (`148d0fb`)** still exist on
the public GitHub mirror — they are only removed when their **deletions are committed and pushed**. If the
commit stages new files but not the deletions, the full papers stay public. This list is the exact set to
delete. Author: Peter Higgins; assistant prepared, **Peter commits/pushes (sole gate).***

## ⚠️ First: a stale lock I must flag
The sandbox left a `.git/index.lock` it cannot remove (`Operation not permitted`). **Before any git command,
delete it:** Windows `del "D:\HUF_Research\Claude CoWorker\Current-Repo\Hs\.git\index.lock"`. Git will refuse
to commit while it exists.

## A — Full papers/drafts moved off-repo this session (tracked → delete from mirror)
- `papers/cnq_tiling_suite_2026/P1_CNQ_TILING_METHODS.md`
- `papers/cnq_tiling_suite_2026/P2_DECEPTIVE_DRIFT.md`
- `papers/cnq_tiling_suite_2026/P3_CNTT_TOOL_PAPER.md`
- `papers/codawork2026/manuscript/` — **all 24 files** (MANUSCRIPT.md, README, SUPPLEMENTARY, every
  `figures/*.pdf|png`, `output/Compositional_Monitoring_2026.docx|pdf`, `output/build_run.js`)
- `papers/in_progress/ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md`
- `papers/in_progress/PAPER_1_UNIVERSALITY_OUTLINE.md`
- `papers/in_progress/PAPER_1_UNIVERSAL_INVARIANCE_DRAFT.md`
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md`
- `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md`

Full copies now live off-repo in `arXiv/` (CoWorker root). Nothing lost.

## B — ⚠️ Sensitive deletions that were NEVER pushed (still public on the mirror — remove now)
These were removed from the working copy in earlier sessions but the deletions never reached the mirror, so
they are **still visible on the public GitHub repo**. All three have safe off-repo copies in
`FRONTIER_AUDIENCE_INTERNAL/` — content preserved; only the public exposure is the issue.
- `papers/in_progress/AUDIENCES_AT_THE_FRONTIER.md` — the **directed-audience strategy** you explicitly
  wanted **off** the public repo. (Confirmed present in HEAD `148d0fb`.)
- `papers/in_progress/GAUGE_THEORY_AND_Hs.md` — the **quarantined** differential-geometry tower.
- `papers/in_progress/MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md` — quarantined.

## NOT on the mirror (untracked; no action)
`papers/cnq_tiling_suite_2026/latex/` (whole folder), `P1_INTRODUCTION_DRAFT.md`,
`P5_COMPOSITIONAL_CHARACTER_SPACE.md`, `papers/financial/P6_COMPOSITIONAL_NAVIGATION_IN_FINANCE.md` — these
were created this session and never committed, so they were never on the mirror.

## The commit recipe (stages deletions AND new files)
```
cd D:\HUF_Research\Claude CoWorker\Current-Repo\Hs
del .git\index.lock                       REM if present (see above)
git add -A                                REM -A is essential: stages deletions too, not just new files
git status                                REM verify A+B show as "deleted"; the new abstracts/arXiv-policy show as "new file"
git commit -m "Papers off public repo: full copies to arXiv folder; abstracts only on Hs; remove tracked full drafts + stale sensitive docs from mirror"
git push
```
After push, confirm on the live GitHub that `papers/in_progress/AUDIENCES_AT_THE_FRONTIER.md`,
`GAUGE_THEORY_AND_Hs.md`, and `MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md` return 404, and that the full P1/P2/P3
drafts and the CoDaWork manuscript are gone.

*HUF and RWA: no `.tex` and no moved papers — nothing to delete there (verified). The `arXiv/` folder is in
the private CoWorker workspace, off all three public repos.*
