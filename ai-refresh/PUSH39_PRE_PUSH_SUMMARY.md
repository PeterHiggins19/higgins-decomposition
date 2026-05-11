# PUSH #39 — pre-push summary

**Date:** 2026-05-10
**Push type:** doc-only + admin (claim-sharpening pass for the CoDaWork 2026 talk)
**Active priority:** CoDaWork 2026 conference talk (Coimbra, Portugal, 1–5 June 2026)
**Engine / tests / schema unchanged.**

---

## What this push delivers

Acted on all six recommendations from the Claude self-review against `EXTERNAL_REVIEW_INVITE.md` (the review pass earlier this session). Push #39 is the implementation pass.

| # | Action | Where it lands |
|---|---|---|
| 1 | **MC-4 claim sharpened to three-conjunct form** | Beat 2 of master plan §5.1 + EXTERNAL_REVIEW_INVITE.md + HS_ADMIN.json active_priority |
| 2 | **INV-050 framing tightened** from broader-family to pair-invariance | NAMED_FINDINGS_FOR_CODA_DISCUSSION.md (earlier wording preserved for traceability) + INVESTIGATION_CATALOG.json INV-050 entry |
| 3 | **Three open questions explicitly named** | New doc `papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md` + master plan §5.1 Beat 8 + EXTERNAL_REVIEW_INVITE.md item 4 |
| 4 | **Cut list for the 10-beat plan added** | Master plan §5.1.1: drop order is (1) Beat 5 animation, (2) Beat 10 live demo, (3) Beat 7 OWID slide |
| 5 | **Null-model caveat moved onto Beat 5 slide** | Master plan §5.1 Beat 5 + NAMED_FINDINGS_FOR_CODA_DISCUSSION.md slide-language row |
| 6 | **Prior-art search targets enumerated** | New doc `papers/codawork2026/planning/PRIOR_ART_SEARCH_TARGETS.md`: four specific areas with authors, journals, and queries |

---

## The sharpened MC-4 claim

> *No monitoring framework in the energy / market-share literature operates **natively in Aitchison geometry** with **formal change detection** at the **carrier level** — the three conjuncts combined into one observable stack. A defeater must overturn the conjunction, not just one disjunct.*

The pre-sharpening wording (*"no prior monitoring framework tracks compositional market share at the carrier level with formal change detection"*) is preserved in the planning docs for traceability. The talk's Beat 2 slide carries the new wording.

## The three open questions (now named explicitly)

1. **Q1 — Concentration measure vs Aitchison norm** (the abstract's named question)
2. **Q2 — The right family of "valid simplex distances"** against which to test verdict-invariance (raised by INV-050)
3. **Q3 — The right null model for compositional change-point detection** on the simplex (raised by INV-051 and the packet's p = 0.0016 caveat)

All three are CANONICAL for the conference talk per `papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md`.

---

## Pre-flight checks (all green)

| Check | Result |
|---|---|
| `ai-refresh/HS_ADMIN.json` parses | OK (9 session_log entries, last entry push #39) |
| `HS_FAST_REFRESH.json` parses | OK (last_push #39) |
| `ai-refresh/INVESTIGATION_CATALOG.json` parses | OK |
| `ai-refresh/HS_MACHINE_MANIFEST.json` parses | OK |
| INV catalog math | 51 total / sum_by_disposition = 51 / sum_by_source = 51 ✓ |
| INV-050 entry contains "SHARPENED IN PUSH #39" | ✓ |
| 11/11 linked planning files present | ✓ |
| active_priority block has push #39 doc pointers | ✓ (three_open_questions_doc, prior_art_search_targets_doc, mc4_claim_sharpened_push39) |

---

## Commit message suggestion

```
push #39 — Claim-sharpening pass for CoDaWork 2026 talk

Acted on a six-point Claude self-review against EXTERNAL_REVIEW_INVITE.md:

1. MC-4 claim sharpened to three-conjunct form (natively Aitchison +
   formal change detection + carrier-level — combined into one
   observable stack). A defeater must overturn the conjunction.
2. INV-050 framing tightened from broader-family-invariance to the
   demonstrated TV+Aitchison pair-invariance across the 9-country EMBER
   2001-2025 corpus. Earlier wording preserved for traceability.
3. Three open questions for the community explicitly named (Q1 from
   the abstract; Q2 from INV-050; Q3 from INV-051) — new doc
   papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md.
4. Cut list for the 10-beat plan written into master plan §5.1.1.
5. Null-model caveat moved from speaker notes onto the Beat 5 slide.
6. Prior-art search targets enumerated in new doc
   papers/codawork2026/planning/PRIOR_ART_SEARCH_TARGETS.md.

No engine / test / schema changes. Catalog: 51 total / 29 CANONICAL
(unchanged from push #38 — INV-050 was sharpened, not added).

Files added:
  papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md
  papers/codawork2026/planning/PRIOR_ART_SEARCH_TARGETS.md
  ai-refresh/PUSH39_PRE_PUSH_SUMMARY.md

Files modified:
  papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md
  papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md
  papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md
  ai-refresh/INVESTIGATION_CATALOG.json
  ai-refresh/HS_ADMIN.json
  HS_FAST_REFRESH.json
```

---

## Still queued (not blockers for push #39)

- **Prior-art search execution** — the targets are listed; someone needs to run the searches between 2026-05-11 and 2026-05-25 per the timeline in PRIOR_ART_SEARCH_TARGETS.md
- **5.3.M** — Monthly-grain deceptive-drift module (queued)
- **EngPromo-2** — `cnt.R` port to schema v3.1.0 parity
- **5.3.N through 5.3.U** — Slide content for the talk
- **Post-conference CNQ engineering hygiene INV** — packaging + CITATION.cff + R port dimension branches + parity bug (from the ChatGPT deep audit; queued for after June 5)

---

*Push #39 ships the talk's claim-strength tightening without touching the engine. The work behind the talk is unchanged; the talk's wording is now one notch harder to defeat without becoming any less interesting.*
