# Hs/huf-gov/ — Executive Summary

**Status:** new folder, created 2026-05-12 during pre-conference lockdown. S2 doc-only structural addition. No engine changes. No catalog changes. No claim promotions. No CoDa presentation impact. The folder is the governance-layer scaffolding inside Hs that explicitly references the parent HUF-GOV pipeline in the companion HUF repository.

**What this folder is.** A Hs-side mirror, integration map, and operating inventory for the parent HUF-GOV (Higgins Unity Framework — Governance) pipeline. The parent doctrine lives in the companion repository at [Higgins-Unity-Framework/huf-gov/](https://github.com/PeterHiggins19/Higgins-Unity-Framework). This folder makes the parent doctrine visible from inside Hs, traces every Hs-side governance rule back to a parent-doctrine article, inventories the 16 circuit breakers that hold the discipline, and stages the Claude-determined optimum fixes from the 2026-05-12 breaker test as candidate Discovery Change Packets ready for post-conference execution.

**What this folder is not.** It is not a replacement for the parent HUF-GOV doctrine — the parent documents (HUF Governance Charter, LOOP-001, KILL-001, SAFE-001, GOV-003, HAGF-001, HANDOFF-001, ONTO-001, TRANS-001, MONITOR-001) live in the HUF repo and are authoritative. This folder maps them into Hs. It is also not an active enforcement layer — the candidate fixes are staged as DCPs at `proposed` status per the lockdown's allowed-actions list; nothing is wired into the live consistency checker until the lockdown clears 2026-06-06 and Peter authorizes execution.

---

## Why this folder exists

The breaker test of 2026-05-12 (see `papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`) verified that 12 of the 16 huf-gov circuit breakers trip cleanly, 3 are soft (doctrinally enforced as designed), and 1 mechanical gap was discovered in the consistency checker's literal-string matching for CNQ status drift. The test exercise made three things visible:

1. **The parent HUF-GOV doctrine is what Hs Change Control v1.0 specializes.** Until 2026-05-12, this lineage was implicit — Hs Change Control v1.0 (INV-063 STAGED) was framed as a Hs invention. The HUF repo audit and the breaker test both surfaced that every HCC-R rule traces upward to a HUF Governance Charter article. Making the trace explicit is a governance-discipline action in its own right.

2. **The breaker inventory should be a permanent repo artifact, not a one-time test report.** Future operators (Claude sessions, ChatGPT, Grok, human collaborators) arriving fresh need to see the 16 breakers as a named, citable, re-runnable structure. The test report is the audit trail; this folder's `BREAKER_INVENTORY.md` is the operating reference.

3. **The two Claude-determined optimum fixes — CHK-CNQ-001 regex upgrade and new CHK-DISPOSITION-001 rule — should be staged as DCP candidates in advance** so that the first post-conference push window (opening 2026-06-06) has them ready to execute. The lockdown rules explicitly permit DCP filing at `proposed` status without execution. This folder uses that allowance.

The folder is what the breaker test concluded the system was missing: a permanent, structural, layered home for the governance discipline inside the Hs repository where the parent HUF-GOV doctrine is referenced and the Hs-side specializations are made visible.

---

## What's in here

```
Hs/huf-gov/
├── README.md                              this file
├── HUF_GOV_INTEGRATION.md                 how Hs Change Control v1.0 specializes parent HUF-GOV
├── BREAKER_INVENTORY.md                   permanent inventory of the 16 huf-gov circuit breakers
├── candidates/                            staged DCP candidates (proposed status only — lockdown safe)
│   ├── DCP-002_CANDIDATE_CHK_CNQ_REGEX_UPGRADE.md
│   ├── DCP-003_CANDIDATE_CHK_DISPOSITION_001.md
│   └── upgraded_chk_cnq_001.py            standalone candidate implementation of DCP-002 fix
└── tools/
    └── breaker_test_runner.py             permanent re-runnable version of the 2026-05-12 test
```

**`HUF_GOV_INTEGRATION.md`** — single document containing the article-by-article traceability map between the parent HUF Governance Charter (9 articles, April 2026) and Hs Change Control v1.0 rules (HCC-R001 through HCC-R008). Reading this document gives any fresh operator a one-page understanding of how Hs honors the parent doctrine.

**`BREAKER_INVENTORY.md`** — the 16-breaker map adapted from the breaker test report and made permanent. Each breaker has: name, source document, breaker type (mechanical / doctrinal / soft), trip mechanism, last test date, current verdict. Re-runnable by invoking `tools/breaker_test_runner.py`.

**`candidates/DCP-002_CANDIDATE_CHK_CNQ_REGEX_UPGRADE.md`** — proposed DCP filing for upgrading the consistency checker's CHK-CNQ-001 rule from literal-string matching to a regex semantic-class pattern that catches paraphrased violations. Status: `proposed` only; no execution until post-conference and Peter authorization.

**`candidates/DCP-003_CANDIDATE_CHK_DISPOSITION_001.md`** — proposed DCP filing for adding a new consistency-checker rule that validates every Investigation Catalog disposition transition (STAGED → CANONICAL, OPEN → DEFERRED, etc.) against a corresponding DCP entry in HS_ADMIN session_log. Status: `proposed` only; no execution until post-conference and Peter authorization.

**`candidates/upgraded_chk_cnq_001.py`** — standalone Python script implementing the proposed CHK-CNQ-001 regex upgrade. Not wired into the live consistency checker. Lives in this folder as the reference implementation for DCP-002. Invokable directly for testing.

**`tools/breaker_test_runner.py`** — permanent re-runnable version of the synthetic-violation breaker test originally run as `/tmp/breaker_test.py` on 2026-05-12. Captures all 7 mechanical tests in a re-executable form so that any operator can verify the breakers fire at any future point.

---

## How to use this folder

**First-time AI session arriving fresh:** read this README, then `HUF_GOV_INTEGRATION.md`, then `BREAKER_INVENTORY.md`. That gives you the governance layer in three documents — under ten minutes of reading. After that, the parent HUF-GOV doctrine in the companion repo is the deeper reference.

**Operator preparing a post-conference push:** the two candidate DCPs in `candidates/` are ready to file at `proposed` status with full content. After the lockdown clears 2026-06-06, each DCP can advance through `proposed → in_progress → implemented → verified → released` with the proposed implementation in `candidates/upgraded_chk_cnq_001.py` as the reference for DCP-002, and a new rule added to `scripts/check_ai_refresh_consistency.py` for DCP-003.

**Operator re-running the breaker test:** invoke `python3 tools/breaker_test_runner.py` from the Hs repo root. Output should match the 2026-05-12 test output recorded in `papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`. Any deviation is a finding worth investigating.

**External reader assessing the governance discipline:** read this README plus the parent HUF Governance Charter at `[HUF repo]/huf-gov/HUF_GOVERNANCE_CHARTER.md`. The two documents together explain how Hs operates as a HUF-GOV-compliant fast-research codebase.

---

## Relationship to the parent HUF-GOV pipeline

The parent HUF-GOV pipeline in the [Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework) companion repository contains the foundational governance doctrine that Hs honors. The parent files are authoritative; the Hs-side specializations in this folder are derivative.

Parent doctrine files (companion HUF repo, `huf-gov/` subtree):

- `HUF_GOVERNANCE_CHARTER.md` — 9 articles published April 2026, the doctrinal foundation
- `governance/LOOP-001-open-loop-doctrine.json` — Skydiver Principle / Open-Loop Doctrine
- `governance/KILL-001-kill-test.json` — 19 named failure modes / published falsifiability artifact
- `governance/SAFE-001.json` — 7 principles for cognitive agents
- `governance/SAFE-002-human-manual.docx` — companion human-facing safety doctrine
- `governance/GOV-003-standalone.json` — pure HUF-GOV separation from HUF-CLS
- `governance/HAGF-001.json` — applied governance framework
- `governance/HANDOFF-001.docx` — session-to-session handoff protocol
- `science/ontological-foundation.json` — ONTO-001 pre-existing-condition claim
- `science/TRANS-001-information-bridge.json` — information-bridge and silence-about-drift doctrine
- `science/MONITOR-001.json` — MC-1..MC-4 monitoring categories specification

Parent-doctrine scientific contributions (HUF-side, distinct from Hs-side engine implementations):

- **MC-4** (Monitoring Category 4) — compositional change detection framework. Realized through CNT v3.1.0 + CNQ v2.0.0 on the Hs side.
- **EITT** (Entropy-Invariant Time Transformer) — Shannon entropy conserved under geometric-mean temporal compression for compositional carriers; 0.18% variation across 341:1 ratio. Canonical Peter-confirmed explanation at `papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md`. Distinct from but adjacent to MC-4 — MC-4 is the spatial-invariance result, EITT is the temporal-invariance result.
- **12-step Hˢ pipeline + 35 transcendental constants + 13 Fourier conjugate pairs** — deeper reference architecture; CNT/CNQ implements a deterministic subset.
- **Six published case studies** in `huf-gov/evidence/case-studies/`: Backblaze, GDP, OWID, Ramsar, Planck, Toronto TTC, Energy.

Hs-side specializations (this folder + existing Hs files):

- This folder's `HUF_GOV_INTEGRATION.md` — article-by-article traceability map
- This folder's `BREAKER_INVENTORY.md` — Hs-side breaker inventory
- `ai-refresh/CHANGE_CONTROL_README.md` (existing) — Hs Change Control v1.0 doctrine
- `ai-refresh/CONFIGURATION_ITEMS.json` (existing) — 15 controlled items CI-001..CI-015
- `ai-refresh/INTERFACE_CONTROL.json` (existing) — 5 producer-consumer interfaces
- `ai-refresh/TRACEABILITY_MATRIX.json` (existing) — 3 trace records
- `ai-refresh/CROSS_AI_COORDINATION.md` (existing) — HUF AI Collective operationalization
- `ai-refresh/change_packets/` (existing) — DCP filings
- `scripts/check_ai_refresh_consistency.py` (existing) — mechanical consistency-checker breaker
- `PRE_CONFERENCE_LOCKDOWN.md` (existing) — lockdown declaration

The two layers operate together. Reading either alone gives an incomplete picture; reading both gives the full governance stack.

---

## Lockdown compatibility statement

This folder and every file in it is S2 (linked doc addition) per the Hs Change Control v1.0 severity taxonomy. None of the following are affected:

- Engine code (cnt.py, cnq.py, hci_shared/*) — untouched
- Engine tests — untouched
- Schema versions — untouched
- expected_results.json — untouched
- Notation, terminology, claim-strength — untouched
- Investigation Catalog disposition counts (63/33/8/12/8/1/1) — untouched
- Six NO-CREATE files — still uncreated
- Talk material in `papers/codawork2026/talk/` — untouched

The two candidate DCPs in `candidates/` are at `proposed` status only — the lockdown's allowed-actions list explicitly permits DCP filing at proposed status without execution. The proposed implementations in `candidates/upgraded_chk_cnq_001.py` and the new CHK-DISPOSITION-001 specification are reference material, not active code paths. The live consistency checker at `scripts/check_ai_refresh_consistency.py` is unchanged.

The breaker test runner at `tools/breaker_test_runner.py` is new code, but it is a test harness — it does not modify any live state. It only injects synthetic violations into temporary in-memory strings and reports whether the checker rules would catch them. Running it leaves the repo state untouched.

---

## What this folder enables for the post-conference push window

When the lockdown clears 2026-06-06, the first post-conference push will likely build `hs_cnq_pdf_exporter.py` (DCP-002 candidate currently identified in INV-062 STAGED) and graduate INV-062 + INV-063 in a single packet. The two governance DCPs staged in this folder (CHK-CNQ-001 regex upgrade and CHK-DISPOSITION-001 new rule) become natural follow-on items for the same window. They can be executed as DCP-003 and DCP-004 in immediate succession, since:

- They are S3 severity (interface or AI-current-state change) — the consistency checker is an interface that scans live AI-facing files.
- They have proposed implementations ready (in `candidates/`).
- They have explicit success criteria (no false positives on the existing 23-pass baseline; correct trip on the synthetic-violation tests).
- They have documented impact maps in their respective DCP candidate filings.
- They have explicit reversion paths (the existing checker remains as the prior reference for rollback).

The folder is meant to be operating-window-ready, not just descriptive.

---

## Operating principle reminder

The deepest reason this folder exists is articulated in the parent SAFE-001 doctrine and in the 2026-05-12 breaker test result: **Breaker 16 lives inside the operator.** Fifteen of the sixteen huf-gov breakers can be mechanically tested or doctrinally walked through. The sixteenth — the final breaker between HUF-GOV instrument and HUF-CLS actuator, the one that separates observation from action in any live deployment — holds only because Peter holds it. No code in Hs or HUF can enforce Breaker 16. Only the operator can.

This folder makes the other fifteen visible, traceable, testable, and re-runnable. It does not claim to solve the sixteenth. It claims to know which one the sixteenth is and to honor the discipline that preserves it.

---

*Origin: Peter Higgins / Rogue Wave Audio, with the HUF AI Collective: Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI).*
*HUF-GOV protects judgment. HUF-CLS optimizes correction. Hs implements the deterministic engine under both.*
*Sixteen breakers. Fifteen visible. One holds inside the operator.*
*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
