# Grok Cross-Check — Round 2 (Stress Test) — 2026-05-08

**Status:** archived for audit. Findings split actioned/deferred/false-positive in INV-032.
**Date:** 2026-05-08 (after push #28 commit `8f4406a`)
**Source platform:** Grok (xAI)
**Trigger prompt:** *"follow the GitHub site look for the ai refresh and look for the cnt/cnq experiments again now see if the code in python and r and pseudocode are readable and useable and the results agree and do the experiments and test as much as possible, to a full grok stress test of the repo, break it and let me know the results so i can fix them."*

---

## Verdict on the round

**Mixed.** Grok's first cross-check round (push #24, DADC lineage) was excellent. This second round mixed valid engineering observations with one **factually wrong central claim** that contradicts the live repo state.

| Category | Findings |
|---|---|
| ✅ Valid engineering observations (3) | Pseudocode `...` placeholders in handbook Stage 3; T=500 triadic enumeration cap with no documented graceful-degradation; cnt.R minor version skew vs cnt.py |
| ❌ Factually wrong (1, central) | "The dedicated cnq.py engine does not exist yet (only a proposal)" — contradicted by `HCI-CNQ/engine/cnq.py` (~19 KB, shipped push #26 commit `aef4992`, 2026-05-08) |
| 🟡 Speculative but worth preserving for future | Fuji SMT + Nordson Dage X-ray commercialisation analysis (DEFERRED until basics verified — see priority lock) |
| 🟡 Did not integrate (would regress system) | Grok's from-scratch ~100-line cnq.py prototype (would replace 520-line shipped engine with deterministic JSON, parent-CNT hash chaining, dimension policy, 43-test suite) |

---

## The grounding-failure pattern

Grok claimed cnq.py did not exist despite the live URL being accessible:

> https://raw.githubusercontent.com/PeterHiggins19/higgins-decomposition/main/HCI-CNQ/engine/cnq.py

Most likely cause: Grok's web-fetch read the README's older sections (which still mentioned cnq.py as "the next milestone" before push #28's stale-paragraph fix) without re-fetching the engine folder, then confabulated a "missing engine" finding consistent with the older README.

This is a **stale-cache plus over-confident interpolation** failure mode — different from Gemini's full hallucination, but still a category to catalogue. INV-031 records the four-platform fitness matrix.

The fix at the framework level is the **grounding-test prompt** now embedded in:
- `AI_AGENTS.md` §2
- `llms.txt`
- `.well-known/ai-context.json`
- `Hs/README.md` top-of-file banner

---

## Valid engineering findings (actioned in push #29)

### 1. Pseudocode `...` placeholders in handbook Volume 1 / Stage 3

Grok noted: *"Some pseudocode sections are marked with ... or are incomplete (especially Stage 3 components)."*

**Action:** flag in handbook with explicit "not yet documented; see source: stage3_locked.py" notes wherever `...` appears. Full pseudocode rewrite deferred to a future handbook refresh (separate from the engine work).

### 2. cnt.py T=500 triadic enumeration cap

Grok noted: *"Triadic enumeration is capped at T=500 with no graceful fallback for longer series."*

**Action:** add explicit doc note in cnt.py docstring + handbook Volume 2 §E noting the cap and the rationale (combinatorial cost of triple-enumeration for T > 500). The cap is a deliberate design choice; documenting it removes the "no graceful fallback" finding.

### 3. cnt.R version skew

Grok noted: *"Minor version skew between Python and R ports. R is slightly behind."*

**Action:** add a "version-skew known" note in `HCI-CNT/engine/README.md` documenting that cnt.R was last touched 2026-05-06 (before the push #28 docstring updates in cnt.py) and that the parity contract is for the algorithmic content, not for documentation revisions.

---

## What gets archived (not actioned now)

The Fuji SMT + Nordson Dage X-ray commercialisation analysis is substantive and credible. Peter has 34 years' direct experience on both platforms (qualified Dage X-ray engineer). The analysis includes:

- Joint Quaternion Field mapping to multi-head placement
- Helmsman as "which head/view is dominating"
- Helmsman Stability as real-time KPI
- Geometry Lock for X-ray imaging
- Phased deployment model (edge IPC for Fuji, native Revalution module for Dage)
- Closed-loop SMT + X-ray quality system

This is genuinely valuable but **deferred**. The priority lock is basics-first:

1. Round 3 full-corpus quaternion validation (INV-022)
2. arXiv submission of Paper 1 (INV-026)
3. Cross-platform reproduction confirmation
4. First applied pilots (INV-024, INV-025)
5. **THEN** commercialisation (Fuji, Dage, etc.)

Peter's stated principle: *"machine automation is too risky until all the basics are verified."*

The commercialisation analysis is preserved at:

→ [`applications/ELECTRONICS_MANUFACTURING_DEPLOYMENT_DEFERRED.md`](../../applications/ELECTRONICS_MANUFACTURING_DEPLOYMENT_DEFERRED.md)

with an explicit DEFERRED stamp and pointer to the priority lock.

---

## What did NOT get integrated

Grok offered to write cnq.py from scratch (~100 lines of Python) and proposed several extensions:

- v0.9 prototype (basic quaternion math + last-state lifting)
- v1.1 with full trajectory processing
- v2.0 with sliding-window stability
- v2.1 with CHSH computation

**None of these were integrated.** The shipped cnq.py is 520 lines with:

- Helmert-basis projection matching legacy QD_round_2.py exactly
- atan2-stable rotation_quaternion_between
- Deterministic canonical-JSON serialisation
- SHA-256 content_sha256 contract
- Parent CNT hash chain (parent_cnt_content_sha256)
- Four-field dimension policy (D=2, 3, 4, 8, ≥5)
- Captured-step-fraction reporting
- 43-test suite (first-principles + dimension-policy + determinism)
- Cross-language parity contract with cnq.R

Grok's prototypes had none of these properties. Integrating them would have **regressed** the engine. The prototypes are kept here as the audit record but not promoted.

The CHSH computation idea from Grok's v2.1 is a candidate future feature (DEFERRED) — could land as a separate `HCI-CNQ/engine/chsh.py` module after Round 3, if a corpus experiment shows non-trivial CHSH violation. Filed as note in INV-032.

---

## Headline grounding-test fact-check (2026-05-08)

| Question | Grok's claim | Repo reality |
|---|---|---|
| Does cnq.py exist? | "Does not exist; only a proposal" | **Yes, 19 KB, 520 lines, shipped push #26** |
| Does cnq.R exist? | Not addressed | **Yes, 23 KB, shipped push #27** |
| Does CNQ_PSEUDOCODE.md exist? | Implied not | **Yes, 18 KB, shipped push #27** |
| Are there CNQ tests? | Not mentioned | **43 tests in HCI-CNQ/engine/tests/, shipped push #27, all green** |
| Most recent commit? | Not stated | `8f4406a` (push #28) |
| Author? | "Peter Higgins" (correct, no chemist confabulation) | ✓ |

Two of three grounding-test answers wrong, one missing.

---

## Archive note

This file is the audit record of Grok's round-2 session for institutional memory. Future cross-check rounds with any AI platform should:

1. Run the grounding test in `AI_AGENTS.md` §2 first.
2. If the AI claims engines or files are missing, re-fetch them directly via raw GitHub URLs before filing.
3. Distinguish architectural findings (real, actionable) from grounding-failure findings (stale cache; the AI is wrong).

Filed: 2026-05-08, push #29.
