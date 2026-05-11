# AI Refresh — 2026-05-10 — CNT v3.1.0 + two named findings + external review invite

**Date:** 2026-05-10
**Push:** #38 (external review prep)
**Audience:** any AI session (Claude, ChatGPT, Grok, Gemini, Copilot) or human reviewer asked to comment on the CoDaWork 2026 conference work before the 1 June 2026 talk
**Status:** active priority addendum — supersedes the push #36 redirect's depth-only framing of the post-#36 work

---

## Summary in one paragraph

Between push #36 (the CoDaWork redirect) and this push, four substantive things happened that any AI session resuming the work needs to know about. (1) The HUF MC-4 packet's operators were promoted into the canonical CNT engine as schema v3.1.0 (`navigation_concentration_family` per timestep + `navigation_concentration_summary` series-level). (2) Australia (AUS) was added to the EMBER corpus, making nine countries on a clean coherent 2001–2025 range. (3) Two empirical findings were catalogued as CANONICAL: **INV-050 metric-invariance of the qualitative compositional verdict** (TV distance and Aitchison distance agree on every shock hit/miss verdict across the 9-country corpus) and **INV-051 deceptive-drift signature reproduced across 5 of 9 EMBER countries** (AUS, CHN, GBR, IND, JPN). (4) An external-review invitation document has been published at `papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md`. This refresh is the AI-side companion to that invitation: it tells any AI assistant what we want pressed, what's in scope, and what is explicitly out of scope. The active_priority block in `HS_ADMIN.json` still points to the CoDaWork talk; this document layers on top of it for any session that comes in during the next three weeks.

---

## What changed since push #36 (the CoDaWork redirect)

| Push | Title | What it added | Catalog |
|---|---|---|---|
| #37 | CNT v3.1.0 — navigation_concentration_family promoted into canonical engine | TV distance, K_eff, K_eff_yoy_change, tv_acceleration, concentration_regime in engine output; schema 3.0.0 → 3.1.0; retired runner-side packet_operators.py | INV-049 CANONICAL |
| #37 follow-on (named findings) | Metric-invariance of the qualitative verdict + 5-country deceptive-drift reproduction codified | Statement, evidence, slide language, defeat paths for each finding | INV-050 + INV-051 CANONICAL |
| #38 (this push) | External review invite + AI refresh narrative | EXTERNAL_REVIEW_INVITE.md + this file + admin updates | (no new INV — process push) |

Catalog after this push: **51 investigations total / 29 CANONICAL / 12 DEFERRED / 8 OPEN / 1 FALSIFIED / 1 CLOSED**.

---

## The two named findings — what we want pressed

These are the most important new material since push #36. Both are in `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md` with full statement, evidence, and slide language.

### Finding 1 — Metric-invariance (INV-050)

> *TV distance (half-L1) and Aitchison distance (log-ratio Euclidean) agree on every shock hit/miss verdict across the 9-country EMBER 2001–2025 corpus, while differing in raw magnitude. The qualitative compositional verdict is metric-invariant within this family.*

**Reviewer questions to press:**
- Is the family of "valid simplex distances" we tested (TV + Aitchison) too narrow? Should weighted log-ratio distances, Mahalanobis on CLR covariance, or Egozcue–Pawlowsky-Glahn evidence-information distance be added to the family?
- Is the operationalisation of "shock verdict" (threshold on whether step-Δ is above series median) robust? What threshold rules would break the verdict-agreement?
- Is this a methodological contribution worth a short note, or is it a known result that the CoDa community has documented under different terminology?

### Finding 2 — Deceptive-drift reproduction across 5 of 9 EMBER countries (INV-051)

> *The deceptive-drift signature (K_eff tightening while TV stays at or below the series median) fires at annual grain in 5 of 9 EMBER countries: AUS (1), CHN (1), GBR (2), IND (2), JPN (2). Germany at annual grain shows K_eff tightening pre-2022 but TV above median — drift was loud, not deceptive. Monthly-grain reproduction of the packet's p = 0.0016 number is queued (`monthly_deceptive_drift.py`).*

**Reviewer questions to press:**
- Is the protocol over-fitting to the corpus, or is the cross-country reproduction strong enough to call this a generalisable signature?
- Is the honest framing — annual grain shows the K_eff side; monthly grain is needed for the TV-quietness side — the right framing, or are we over-conceding?
- Why these 5 and not the other 4? Per-country trajectories are in `papers/codawork2026/conference_2026_06/per_country/ember_*/cnt_v3.json`. We have a story but it has not been pressure-tested.
- Are there other shock-anchored composition datasets (CoDa benchmarks?) where the same protocol should be applied as independent validation?

---

## The defeat paths the community is the right room to engage

The HUF MC-4 packet identifies four falsifiability conditions. INV-050 + INV-051 directly preempt Metric defeat and Case defeat. **Two remain open**:

- **Prior-art defeat** — *"no prior monitoring framework tracks compositional market share at the carrier level with formal change detection."* We have not found such work. We welcome pointers to anything in the CoDa, econometrics, market-share-monitoring, or diversity-index literature that already makes the same move. Candidates we know about (Aitchison 1982/1986, Egozcue & Pawlowsky-Glahn 2018, standard market-share econometrics, Shannon/HHI diversity indices) are listed in `EXTERNAL_REVIEW_INVITE.md` with our current reasoning for considering them distinct.
- **Category defeat** — is *"composition monitoring as a primary observable"* genuinely a distinct monitoring category, or is it at most a useful application note inside existing CoDa? We have no preconceived answer; we want the room's view.

If the community can defeat the MC-4 claim on either path, the claim should be narrowed or restated. That is the right outcome — the discipline of the packet is that the claim is falsifiable.

---

## What we are explicitly NOT asking for in this review

To save reviewer time:

- The broader instrument paper ("The Higgins Decomposition: a deterministic compositional diagnostic on the Aitchison simplex") is deferred to a journal track after the conference and does **not** need reviewer attention before June 1.
- The CNQ v2.0.0 quaternion view, the depth tower, the IR taxonomy, and the helmsman family beyond direct relevance to drift detection are appendix material for the talk and do not need to be reviewed for the conference.
- The applied tiers (HCI-AUDIO, HCI-ULTRASOUND) are out of scope for this review.
- The 101-dataset full-corpus validation is supporting evidence only — not the headline.

The talk's scope is **energy-mix drift on the simplex**. That is what the audience will hear about and what the review pass should focus on.

---

## Fetch order for an AI assistant coming in cold

1. `papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md` — the human-facing invitation, with the specific things we want reviewed
2. `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md` — full content of INV-050 and INV-051
3. `papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md` — master plan, beat structure, deliverable bundle
4. `papers/codawork2026/planning/ABSTRACT_TO_CNT_V3_MAP.md` — operator-by-operator mapping from abstract terms to engine output fields
5. `ai-refresh/AI_REFRESH_2026-05-10_codawork2026_redirect.md` — the push #36 redirect (still valid foundation)
6. This document — the push #38 update layered on top
7. `External_Published_Papers/book-of-abstracts-codawork-2026-draft.pdf` page 25 — the binding abstract
8. The HUF MC-4 packet (11-page methods attachment that went with the original submission)

Reviewers wanting to verify any number in the talk can pull the deterministic JSONs at `papers/codawork2026/conference_2026_06/per_country/ember_*/cnt_v3.json` and read the fields listed in EXTERNAL_REVIEW_INVITE.md's engine-output table.

---

## How to engage as an AI assistant

Once you have the fetch above:

- **Claim-strength critique** — name anywhere we are over-reaching. Be specific: file, line, the exact phrase that overshoots.
- **Methodological critique** — is the metric, the threshold, the null model, the regime tag the right one? Cite the alternative explicitly.
- **Vocabulary critique** — anything we are naming that already has a name in the literature? Give the citation.
- **Slide-structure critique** — does the 10-beat plan in master plan §5.1 land in 15 minutes for a CoDa audience? Mark beats that are too long, too short, or off-topic.
- **Open-question critique** — are the three open questions in §5.1 the right ones to ask the room?
- **Prior-art pointers** — anything in the CoDa literature that already covers compositional market-share monitoring with formal change detection? List with citation if so.

We do not require a particular response format. A short, sharp note pointing at the specific weakness is more useful than a long generic summary.

---

## What happens to feedback we receive

Anything substantive will be added to the talk's pressure-test bench and either incorporated into the slides (if it sharpens the claim) or archived as Q&A material (if it strengthens a defeat path the audience might press). Catalog entries will be opened for any pointer that materially affects the MC-4 claim. Per the project's discipline, every disposition is data — even "this is already a known result under a different name" is a finding worth recording.

If a reviewer's note kills the MC-4 claim, the claim is killed and restated. That is the right outcome.

---

## Cross-references

- Active priority block: `ai-refresh/HS_ADMIN.json` → `active_priority`
- Push #36 redirect: `ai-refresh/AI_REFRESH_2026-05-10_codawork2026_redirect.md`
- Master plan: `papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md`
- Named findings: `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md`
- External review invite: `papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md`
- Abstract-to-engine mapping: `papers/codawork2026/planning/ABSTRACT_TO_CNT_V3_MAP.md`
- INV-049 (engine-native concentration family): `ai-refresh/INVESTIGATION_CATALOG.json`
- INV-050 (metric-invariance): `ai-refresh/INVESTIGATION_CATALOG.json`
- INV-051 (5-country reproduction): `ai-refresh/INVESTIGATION_CATALOG.json`
- HUF MC-4 packet: included with the original conference submission; the operational vocabulary it codifies is now in CNT v3.1.0 as engine-native diagnostics
- Engine: `HCI-CNT/engine/cnt.py` (Python v3.1.0); `HCI-CNT/engine/cnt.R` (R, parity to v3.0.0, v3.1.0 update queued as EngPromo-2)

---

*Active until: 2026-06-05 (end of the conference). After the conference this addendum retires alongside the push #36 redirect.*
