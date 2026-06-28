# Pre-push readiness — 2026-06-22 session (G-145 → G-163)

*Working-tree state on the CoWorker mirror. **Nothing pushed** — Peter is the sole gate. This manifest names
exactly what changed this session, which repo needs to push, and the safe staging recipe. Author: Peter
Higgins; AI-assisted per HUF-STD-001.*

---

## 1. Which repo needs to push — **Hs only**

| repo | files touched **this session** | push needed? |
|---|---:|---|
| **Current-Repo/Hs** | **39** | **YES** |
| Current-Repo/HUF | **0** | no |
| Current-Repo/RWA | **0** | no |

All of this session's work is in **Hs**. **HUF and RWA were not touched today** — no cross-repo parity change
this session (the shared Level-1 README block is unchanged; the positioning line went into Hs only). So this
is a **single-repo (Hs) push.**

## 1.5 ✅ VERIFIED AGAINST THE PUBLISHED REPOS (the truth out there)

Checked **directly against GitHub** (the mirror is offline + stale; copy‑paste changes a file's state without
changing content, so only the published repo is truth):

- **All three live repos are AHEAD of this mirror.** Hs **+6** commits (origin `7a85993` — incl. *"Summer
  Clean up"*, *"remove papers"*, *"Determinism Anchors"*, *"Hˢ kinematics"*); HUF **+3** (`37ba542`); RWA
  **+3** (`caeb161`). **The mirror is behind on all three — it is NOT a safe copy‑paste source.**
- **HUF / RWA:** no session work *and* only behind → **no push from this session**; just sync the live repos.
- **Hs session files vs published:** **22 genuinely NEW** (not on origin — safe to add) · **8 modified**, of
  which:
  - **2 CLEAN** (origin unchanged since the mirror's base; edits re‑apply directly): `ai-refresh/HS_ADMIN.json`,
    `huf-gov/HUF_GOV_INTEGRATION.md`.
  - **6 CONFLICT** (origin's +6 commits **already changed these** — the live version is newer; **do NOT copy
    the mirror's stale version over it**): `HS_FAST_REFRESH.json`, `ai-refresh/HS_TRACKING_LOG.json`,
    `ai-refresh/AI_ASSIST.json`, `IS_Hs_RIGHT_FOR_YOU.md`, `papers/ABSTRACT_LEDGER.md`,
    `papers/P7_FOUNDATIONS_SEED.md`.

**Reconciliation — the safe path (supersedes a naïve "copy the named files"):**
1. Work on a **fresh pull/clone of the live Hs repo** (it has origin's latest).
2. **Add** the 22 NEW files. *(Note: the live repo did a "remove papers" cleanup — confirm the new
   `papers/` files fit the current live layout before adding.)*
3. For the **6 CONFLICT files, RE‑APPLY the session's additions onto the LIVE current versions** — append the
   G‑145→G‑164 journal/refresh entries to the *live* admin JSONs (do not overwrite), and re‑add the new ledger
   rows / P7 paragraphs to the *live* files. **Never copy a mirror file over a newer published file.**
4. The **2 CLEAN files** can be applied directly.

## 2. ⚠ The mirror‑divergence warning (read before staging)

`git status` on the mirror shows **~210 changed files in Hs** (and 294 in HUF, 75 in RWA) — but **only 39 of
the Hs changes are from this session.** The rest is **pre-existing mirror drift** (`.gitattributes` / LFS /
binary churn, old deletions, prior-session leftovers) that is **not ours to push**. **Do NOT `git add -A`.**
Stage the **named session paths only**, from the **live repo** (not this diverged mirror), after a
`git status` review.

## 3. The session set (the 39 — what to stage), by area

- **The new arXiv series (papers/triangulation/ + spine):**
  `papers/triangulation/W1_MICROBIOME_WITNESS.md`, `W2_MUDSTONE_WITNESS.md`, `W3_FLEET_WITNESS.md`;
  `papers/TRIANGULATION_TRILOGY_PLAN.md`, `papers/COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md`,
  `papers/PUBLICATION_STAGING_AND_REVIEW_PLAN.md`, `papers/COLLECTIVE_REVIEW_PACKAGE_2026-06-22.md`,
  `papers/PROOF_AND_HONESTY_STANDARD.md`, `papers/THE_HUF_CONSTELLATION_SYSTEM_PROPOSAL.md`,
  `papers/ABSTRACT_LEDGER.md`, `papers/P7_FOUNDATIONS_SEED.md`,
  `papers/DISTRIBUTED_CONTROL_TETRAHEDRAL_3N_PAPER_SEED.md`, `papers/frontier/SO4_SPIN4_FUTURE_COMPONENT.md`.
- **The microbiome / CMP experiment (real data, receipted):**
  `experiments/compositional_message_2026-06/` (RESULTS + cmp_analysis/replicate/fix_hiv_law2/figures/verify.py + result JSONs + 2 figures).
- **The constellation study:** `industrial-instruments/constellation-spacex/` —
  `THE_DISTRIBUTED_CARNOT_DATACENTER.md`, `THE_FINANCIAL_CASE.md`, `THE_FINANCIAL_CASE_VERIFICATION.md`,
  `fin_case_verify.py`, `README.md`.
- **Doctrine + library:** `huf-gov/COMPONENT_REQUEST_ESCALATION_DOCTRINE.md`, `huf-gov/HUF_GOV_INTEGRATION.md`,
  `library/THE_SYSTEM_IS_THE_MESSAGE.md`, `library/FOR_THE_NEXT_EXPLORER.md`, `IS_Hs_RIGHT_FOR_YOU.md`.
- **Admin / state (rolled to G-163):** `HS_FAST_REFRESH.json`, `ai-refresh/HS_ADMIN.json`,
  `ai-refresh/HS_TRACKING_LOG.json`, `ai-refresh/AI_ASSIST.json`, `ai-refresh/COWORKER_SYSTEM_REVIEW_2026-06-22.md`,
  `ai-refresh/PRE_PUSH_READINESS_2026-06-22.md` (this file).

## 4. Off-repo — **NOT** part of this push (separate arXiv action)

The P1 late-fix and the P3 §3c addition live in **`arXiv/`**, which is **outside the three repos** by the
papers-location policy (the repo carries the P1/P3 *abstracts* only; full papers go to arXiv). So:
`arXiv/P1_cnq_tiling/latex/main.tex` (late-fix, recompiles 7 pp clean; `submission/` + `collective_review/`
copies **frozen**) and `arXiv/P3_cntt_tool/P3_CNTT_TOOL_PAPER.md` (§3c) are **staged for Peter's separate
arXiv post**, gated on the collective review — **not** this repo push.

## 5. Verification done this session (the state is clean)

- All four session admin JSONs parse (`HS_FAST_REFRESH`, `HS_ADMIN`, `HS_TRACKING_LOG`, `AI_ASSIST`).
- Independent coherence audit (G-156) returned clean: cross-refs resolve, receipted numbers agree, tiers held.
- The financial arithmetic is deterministic + receipted (`2d9fc354630bd5ee`); the proof corrected the ranges.
- Every new paper carries a Proof & Honesty Standard footer; the standard is a standing gate.
- Names off the public repo; instrument-not-data; no SpaceX contact; safety-primacy; tiers on every claim.

## 6. Push checklist — Peter executes (Hs only)

- [ ] On the **live Hs repo** (not the mirror), `git status`; **stage the §3 named paths only** (no `git add -A`).
- [ ] Confirm no DATA / derived / large binaries are staged (instrument-not-data; off-repo stays off).
- [ ] Commit (suggested message: *"Triangulation series + constellation study + proof/honesty standard (G-145→G-163)"*); push; confirm CI green.
- [ ] **HUF / RWA:** no session push needed; their mirror divergence is a *separate* reconcile-against-live task, not this commit.
- [ ] **arXiv (separate, later):** P1 + P3 post is gated on the collective (elder) review + Peter's decision; reconcile the frozen `submission/` copies then.

*Nothing here is committed or pushed. One repo (Hs) carries this session; the instrument reads, the human
gates. Peter is the sole gate.*
