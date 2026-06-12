# PUSH #38 — pre-push summary

**Date:** 2026-05-10
**Push type:** doc-only + admin + planning (preparing for community review pre-conference)
**Active priority:** CoDaWork 2026 conference talk (Coimbra, Portugal, 1–5 June 2026)
**Engine / tests / schema unchanged.**

---

## What this push delivers

| # | Artefact | Purpose |
|---|---|---|
| 1 | `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md` | Two empirical findings (INV-050, INV-051) with full statement, evidence, slide language, and how-to-defeat sections |
| 2 | `papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md` | Open invitation to AI assistants (Claude, ChatGPT, Grok, Gemini, Copilot) + human reviewers to engage methodologically before the conference |
| 3 | `ai-refresh/AI_REFRESH_2026-05-10_codawork2026_v3_1_0_findings_and_external_review.md` | AI-side companion to the invitation — fetch order, specific review asks, what's in / out of scope |
| 4 | `ai-refresh/PUSH38_PRE_PUSH_SUMMARY.md` (this file) | Pre-push hand-off card |
| 5 | `ai-refresh/HS_ADMIN.json` (modified) | Session_log push #38 entry; active_priority block extended with push #38 pointers; last_updated bumped |
| 6 | `HS_FAST_REFRESH.json` (modified) | last_push → #38; investigation_catalog_pointer recount; active_priority_pointer extended with push #38 docs |

---

## The two named findings

**INV-050 — Metric-invariance of the qualitative compositional verdict.** TV distance and Aitchison distance agree on every shock hit/miss verdict across the 9-country EMBER 2001–2025 corpus, while differing in raw magnitude. Catalogued CANONICAL. Preempts the packet's Metric-defeat falsifiability path.

**INV-051 — Deceptive-drift signature reproduced across 5 of 9 EMBER countries.** At annual grain: AUS=1, CHN=1, GBR=2, IND=2, JPN=2 deceptive transitions over 2001–2025. DEU/FRA/USA/WLD = 0 (correctly classified as non-deceptive — different regimes). Catalogued CANONICAL. Preempts the packet's Case-defeat falsifiability path. Monthly-grain reproduction of the packet's p = 0.0016 number for Germany specifically remains queued as `monthly_deceptive_drift.py`.

---

## The two defeat paths still open (the review's purpose)

- **Prior-art defeat** — MC-4 claim ("no prior monitoring framework tracks compositional market share at the carrier level with formal change detection") needs the community to either confirm or kill. Candidates we know about (Aitchison 1982/1986, Egozcue & Pawlowsky-Glahn 2018, market-share econometrics, Shannon/HHI diversity) are listed with our distinction reasoning in the invite. We welcome correction.
- **Category defeat** — is "composition monitoring as a primary observable" genuinely a distinct monitoring category, or at most a useful application note inside existing CoDa? No preconceived answer; the community is the right room.

---

## Pre-flight checks (all green)

| Check | Result |
|---|---|
| `ai-refresh/HS_ADMIN.json` parses | OK (34 top-level keys, 8 session_log entries, last entry push #38) |
| `HS_FAST_REFRESH.json` parses | OK (21 top-level keys, last_push #38) |
| `ai-refresh/INVESTIGATION_CATALOG.json` parses | OK |
| `ai-refresh/HS_MACHINE_MANIFEST.json` parses | OK |
| INV catalog math | 51 total / sum_by_disposition = 51 / sum_by_source = 51 ✓ |
| INV-049 / INV-050 / INV-051 present + CANONICAL | ✓ |
| Per-country regime_counts on disk vs INV-051 claim | AUS=1, CHN=1, GBR=2, IND=2, JPN=2; DEU=FRA=USA=WLD=0 ✓ |
| 14/15 referenced files present | ✓ (book of abstracts PDF is external reference — not required in repo) |

---

## Commit message suggestion

```
push #38 — Two named findings (INV-050 metric-invariance + INV-051 5-country deceptive drift)
           + external review invite + AI refresh addendum

Codified the two empirical findings most relevant to the CoDa community
discussion (INV-050 metric-invariance, INV-051 5-of-9-country deceptive
drift reproduction). Published EXTERNAL_REVIEW_INVITE.md asking AI
assistants and human reviewers to engage the methodology before the
conference. New AI-refresh addendum points any session resuming the work
to the two findings + the two unpreempted defeat paths (prior-art,
category) the community is the right room to engage.

No engine / test / schema changes. Catalog: 51 total / 29 CANONICAL.

Files added:
  papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md
  papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md
  ai-refresh/AI_REFRESH_2026-05-10_codawork2026_v3_1_0_findings_and_external_review.md
  ai-refresh/PUSH38_PRE_PUSH_SUMMARY.md

Files modified:
  ai-refresh/INVESTIGATION_CATALOG.json  (INV-050, INV-051 entries + recounts)
  ai-refresh/HS_ADMIN.json               (session_log push #38 + active_priority extensions)
  HS_FAST_REFRESH.json                   (last_push #38 + pointer extensions)
```

---

## After push lands

1. Verify CI green (no test changes expected — should be a clean doc-only pass).
2. Open the review window: AI assistants and human reviewers can engage between now (2026-05-10) and 2026-06-01 (conference start).
3. Any substantive feedback feeds into deliverables 5.3.N through 5.3.U on the master plan (slide content, Q&A bench, conference handout).
4. After 2026-06-05 (conference end) the external-review-invite retires alongside the push #36 priority redirect; planning shifts to the post-conference journal track.

---

## Still queued (not blockers for push #38)

- **5.3.M** — Monthly-grain deceptive-drift module (reproduces packet's p = 0.0016 for Germany)
- **EngPromo-2** — `cnt.R` port to schema v3.1.0 parity with `cnt.py`
- **5.3.N through 5.3.U** — Slide content, Q&A bench cards, conference handout for the 10-beat talk plan
