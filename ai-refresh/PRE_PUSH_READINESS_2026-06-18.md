# Pre-push readiness — 2026-06-18 (CoWorker copy; live Hˢ repo is canonical)

*Prepared for Peter's push. **No commit/push by the assistant.** Context (Peter, 2026-06-18): in-progress was
removed from the **live Hˢ repo** and pushed; the **CoWorker copy's in-progress is intentionally untouched**.
This mounted copy is therefore behind the live remote and must not be force-pushed as-is.*

## ⚠️ Two operational gotchas (read first)
1. **`.git/index.lock`** — **RESOLVED by Peter (2026-06-18): all locks in the CoWorker `.git` deleted.**
   (The sandbox may still show a stale cached copy of the lock; the Windows filesystem + git are
   authoritative. If git operations run, the lock is gone.)
2. **This copy has diverged** from the remote (`main ... origin/main [ahead 76, behind 1]`) and still has
   `papers/in_progress/` tracked at HEAD `148d0fb`. **Do not `git add -A` + push from this copy** — it would
   re-introduce the in-progress folder (incl. the sensitive trio) you just removed from the live repo. Apply
   this session's new work to the **live** clone (already clean), or `git pull` the in-progress removal into
   this copy first, then add the new files.

## Live-repo check (please confirm on GitHub)
The three sensitive docs lived inside `papers/in_progress/`; removing that folder from the live repo should
404 them. Confirm gone on live: `papers/in_progress/AUDIENCES_AT_THE_FRONTIER.md`,
`GAUGE_THEORY_AND_Hs.md`, `MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md`.

## This session's work to land on the live repo

### A — New files to ADD (23)
abstracts + policy: `papers/cnq_tiling_suite_2026/{P1_ON_HS_ABSTRACT,P1_REVIEW_BRIEF,P1_REVISION_SHEET,P2_ABSTRACT,P3_ABSTRACT,P5_ABSTRACT}.md(.json)`,
`papers/financial/P6_ABSTRACT.md`, `papers/PAPERS_LOCATION_POLICY.md`.
conformance + collaborator: `ai-refresh/HS_MACHINE_EPSILON_CONFORMANCE.json`, `collaborations/COLLABORATORS_STUDIES_GUIDE.json`,
`papers/GROK_WORK_ORDER_COLLABORATORS_2026-06.json`, `collaborations/geology-wehner/DIAGNOSIS_OF_THREE_VIEWS.md`.
publication + standards: `papers/PUBLICATION_FIT_P1_P3.md`, `papers/LATEX_ARXIV_STANDARDS.md`.
doctrine + seeds: `papers/CONTRADICTION_TEST_PROTOCOL.md`, `papers/P7_FOUNDATIONS_SEED.md`, `papers/EITT_PAPER_SEED.md`,
`papers/frontier/{LIE_THEORY_THREAD_ASSESSMENT,SPECTRAL_COMPOSITION_AND_THE_ROTATION_GROUP,LIGHT_AS_COMPOSITION_RIEMANN_SILBERSTEIN,SPATIAL_HEARING_INVERSE_COMPOSITION_FRONT_END}.md`.
admin: `ai-refresh/{MIRROR_DELETION_LIST_2026-06-18,SESSION_MANIFEST_2026-06-18,PRE_PUSH_READINESS_2026-06-18}.md`.

### B — Modified files to UPDATE
`ai-refresh/HS_TRACKING_LOG.json` (G-97..G-114), `papers/TRIANGULATION_LEDGER.md`/`TRIANGULATION_PROTOCOL.md`,
`papers/ABSTRACT_LEDGER.md`, `papers/THE_HIGGINS_DECOMPOSITION_SERIES.md`, `papers/cnq_tiling_suite_2026/00_SUITE_README.md`,
and the other `M` entries from `git status`.

### C — Deletions to carry (the arXiv restructure; full copies now off-repo in CoWorker `arXiv/`)
`papers/cnq_tiling_suite_2026/{P1_CNQ_TILING_METHODS,P2_DECEPTIVE_DRIFT,P3_CNTT_TOOL_PAPER}.md`,
`papers/cnq_tiling_suite_2026/latex/**` (was untracked — no deletion needed), `papers/codawork2026/manuscript/**`.
These leave the repo holding **abstracts only**; full copies live in `arXiv/` (off-repo). *(in-progress
deletions are your separate, already-pushed action on the live repo — not part of this set.)*

## Verified this session (all green)
P1 LaTeX compiles (6 pp, 0 errors) — now in `arXiv/`; HS-EPS-1 5/5 core receipt `06ccdb25`; geology 3/3
`3d568d24`; all new JSON valid; C-2 swept on the public narrative. Nothing pushed — your gate.
