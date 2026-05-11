# PUSH #40 — pre-push summary

**Date:** 2026-05-10
**Push type:** doc-only + admin + cross-check archive (signal extraction from three ChatGPT review passes)
**Active priority:** CoDaWork 2026 conference talk (Coimbra, Portugal, 1–5 June 2026)
**Engine / tests / schema unchanged.**

---

## Peter's directive

> *"use only the most useful and store the rest"*

Three ChatGPT deep-research review passes (reports 4, 5, 6) were generated against the public repo. All three defaulted to repo-wide deep audit, missing the brief in EXTERNAL_REVIEW_INVITE.md. Push #40 extracts the useful signal and archives the rest.

---

## The three most-useful findings (actioned)

| # | Action | Effort | What it fixes |
|---|---|---|---|
| 1 | **Refresh HCI-CNQ/README.md** — strip pre-push-#32 "compiled engine still proposed" language at three locations | 15 min | The single highest-visibility doc inconsistency a reviewer hits — pre-push #32 language survived the v2.0.0 promotion |
| 2 | **Reconcile domain/version metadata** — README.md "18 physical domains, 101 experiments" → "11 domains and 101 reference datasets" per push #34; CITATION.cff license CC-BY-4.0 → Apache-2.0; version 1.0.0 → 3.1.0; abstract refreshed | 20 min | Two stale-metadata sources reviewers flag on first read |
| 3 | **New REPRODUCIBILITY_CHECKLIST.md at repo root** — five-step verification path (engines exist; four doctrines present; BIST self-test; 43-test suite; three IEEE-floor confirmations) | 30 min | Cold reviewer can verify reproducibility in 15–30 min without spelunking the docs |

---

## The rest (stored, not actioned)

Three ChatGPT reports archived verbatim at `ai-refresh/cross_check_archive/` with a single INDEX file enumerating signal vs noise:

- `chatgpt_deep_research_report4_2026-05-10.md` (HCI-CNQ engine + repo packaging audit)
- `chatgpt_deep_research_report5_2026-05-10.md` (whole-repo audit + governance)
- `chatgpt_deep_research_report6_2026-05-10.md` (HCI-CNQ engine again + hallucinated patches)
- `chatgpt_deep_research_2026-05-10_INDEX.md` (signal/noise breakdown + lesson + retry template)

**INV-052** (CANONICAL, push #40) captures the methodological observation:

> *Open-ended prompts naming only the repo URL trigger ChatGPT's repo-audit instinct, not the brief inside the repo. Successful re-prompts need explicit deep-audit suppression in the wording.*

The INDEX also documents the hallucinations (fabricated function names `QuaternionCalc`, `cnqEngine`; fake JSON diffs against code that doesn't exist) so they cannot be quietly applied downstream.

**Deferred to post-conference cleanup** (real but not blockers):

- `pyproject.toml packages = []` while script entry points are declared — `pip install -e .` does not wire `hs-cnt` / `hs-cnq` scripts
- `cnq.R` dimension dispatch is incomplete (D=3 + projected D≥5 advertised but not implemented in `cnq_run`); covered by EngPromo-2 when cnt.R goes to v3.1.0
- `cnq.py` vs `cnq.R` radial std parity bug (population vs sample)

---

## Pre-flight checks (all green)

| Check | Result |
|---|---|
| `ai-refresh/HS_ADMIN.json` parses | OK (10 session_log entries; last #40) |
| `HS_FAST_REFRESH.json` parses | OK (last_push #40; reproducibility_checklist pointer added) |
| `ai-refresh/INVESTIGATION_CATALOG.json` parses | OK |
| `ai-refresh/HS_MACHINE_MANIFEST.json` parses | OK |
| INV catalog math | 52 total / disp_sum 52 / src_sum 52 ✓ |
| INV-052 present + CANONICAL | ✓ (with narrative + related entries) |
| Linked files (3 reports + INDEX + 3 fixes) | 7/7 present |

---

## Commit message suggestion

```
push #40 — Use the useful, archive the rest (three ChatGPT review passes)

Three ChatGPT deep-research reviews were generated against the repo
this evening. None of the three engaged the brief in
EXTERNAL_REVIEW_INVITE.md; all three defaulted to repo-wide audit.

Actioned the three most useful findings:
1. HCI-CNQ/README.md - removed pre-push-#32 "compiled engine still
   proposed" language at three locations; v2.0.0 correctly named
   canonical since 2026-05-09.
2. README.md + CITATION.cff - reconciled stale metadata: "18 domains"
   -> "11 domains and 101 reference datasets" (push #34 ground truth);
   CITATION.cff license CC-BY-4.0 -> Apache-2.0; version 1.0.0 -> 3.1.0.
3. New REPRODUCIBILITY_CHECKLIST.md at repo root - five-step
   verification path for cold reviewers.

Archived three reports verbatim at ai-refresh/cross_check_archive/
plus an INDEX documenting signal vs noise (the hallucinated function
names + fake JSON diffs are explicitly named in the INDEX so they
cannot be quietly applied by downstream automation).

INV-052 CANONICAL captures the methodological observation: open-ended
prompts that name only the repo URL trigger ChatGPT's repo-audit
instinct rather than the brief inside the repo. Successful re-prompts
need explicit deep-audit suppression.

Catalog: 51 -> 52 total / 29 -> 30 CANONICAL / CHATGPT source 8 -> 9.

No engine / test / schema changes.
```

---

## Still queued (post-conference)

- **Post-conference CNQ engineering hygiene INV** — three deferred fixes (packaging, R port dimension branches, parity bug). To open after 2026-06-05.
- **Prior-art search execution** — targets enumerated in PRIOR_ART_SEARCH_TARGETS.md; targeted searches in the four areas due by 2026-05-25.
- **5.3.M** — Monthly-grain deceptive-drift module
- **EngPromo-2** — `cnt.R` port to schema v3.1.0 parity

---

*Push #40 ships the discipline of separating signal from noise without conceding either. The repo gets cleaner; the conference talk stays untouched; the three review reports are preserved for traceability; the methodological lesson is catalogued for the next AI session that walks in.*
