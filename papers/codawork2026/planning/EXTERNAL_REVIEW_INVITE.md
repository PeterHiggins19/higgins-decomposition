# CodaWork 2026 — External review invite

**Status:** open invitation
**Date:** 2026-05-10 (after push #37 schema v3.1.0 promotion)
**Audience:** AI assistants (Claude, ChatGPT, Grok, Gemini, Copilot) and human reviewers willing to engage methodologically before the conference (1–5 June 2026, Coimbra, Portugal)
**Engine state for review:** CNT v3.1.0 + CNQ v2.0.0; nine EMBER countries on coherent 2001–2025 range; full-corpus reference suite at 101 datasets across 11 domains

---

## What we are asking for

We are preparing a fifteen-minute conference talk for CoDaWork 2026. The published abstract is *Compositional monitoring of energy-mix drift on the simplex* (book of abstracts page 25, accepted via correspondence with Prof. Egozcue). The talk honors that scope. Behind the talk sits a substantial framework (CNT v3.1.0 deterministic engine, CNQ v2.0.0 quaternion view, four binding doctrines, 101-dataset reference suite). We want help refining the talk's content before it lands in front of the CoDa community.

Specifically we want comments, criticism, and assistance on:

1. **The two named findings we are bringing into the discussion** — both empirical, both reproducible from the public engine output, both directly addressing the packet's four-paths falsifiability table.
2. **The methodological framing** — is the talk's claim-strength right, or are we over-reaching or under-stating?
3. **The slide structure** — does the ten-beat talk plan land cleanly in fifteen minutes for a CoDa audience?
4. **The three open questions for the community** — now explicitly named in `papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md`: **(Q1)** the Aitchison-norm-vs-concentration-measure relationship from the abstract; **(Q2)** the right family of "valid simplex distances" against which to test verdict-invariance, raised by INV-050; **(Q3)** the right null model for formal change-point detection on the simplex, raised by INV-051. Are these the right questions to ask the room, or should they be sharpened or replaced?
5. **The defeat paths we have NOT yet preempted** — Prior-art defeat and Category defeat remain genuinely open; we want any pointers the community has to existing CoDa work that might already cover what we are claiming as novel.

---

## The two named findings — focus the review here first

These are the freshest material. They emerged from the engine schema v3.1.0 promotion today and are now CANONICAL in the investigation catalog ([INV-050](../../../ai-refresh/INVESTIGATION_CATALOG.json) and [INV-051](../../../ai-refresh/INVESTIGATION_CATALOG.json)).

Full content: `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md`

### Finding 1 — Metric-invariance of the qualitative compositional verdict (INV-050)

**Statement:** *TV distance (half-L1) and Aitchison distance (log-ratio Euclidean) agree on every shock hit/miss verdict across the 9-country EMBER 2001–2025 corpus, while differing in raw magnitude. The qualitative compositional verdict is metric-invariant within this family.*

**Questions we want pressed:**

- Is the family of "valid simplex distances" we have implicitly defined (TV + Aitchison + their convex combinations) the right family to test verdict-invariance against, or should we broaden to include weighted log-ratio distances or Egozcue–Pawlowsky-Glahn evidence-information distance?
- Is the operationalisation of "shock verdict" robust? We threshold on whether the step-Δ is above the series median; alternatives include z-scoring, Mahalanobis-style thresholding on the CLR covariance, or quantile-relative thresholding.
- Does this constitute a methodological contribution worth a short note, or is it a known result that the CoDa community has documented under different terminology?

### Finding 2 — Deceptive-drift signature reproduced across 5 of 9 EMBER countries (INV-051)

**Statement:** *The deceptive-drift signature (K_eff tightening while TV stays at or below the series median) fires at annual grain in 5 of 9 EMBER countries: AUS, CHN, GBR, IND, JPN. Germany at annual grain shows K_eff tightening pre-2022 but TV above median — the drift was loud, not deceptive.*

**Questions we want pressed:**

- Is the protocol over-fitting to the corpus, or is the cross-country reproduction strong enough that we can speak of a generalisable signature?
- The Germany annual-grain result does not reproduce the packet's monthly p = 0.0016. We have queued a monthly module. Is the honest framing ("annual grain shows the K_eff side; monthly grain is needed for the TV-quietness side") the right framing, or are we over-conceding?
- Why these 5 and not the other 4? Per-country trajectories are in `papers/codawork2026/conference_2026_06/per_country/ember_*/cnt_v3.json`. We have a story for each (different structural transitions, different shock proximities) but it has not been pressure-tested.
- Are there other shock-anchored composition datasets (CoDa community benchmarks?) where the same protocol should be applied as independent validation?

---

## The defeat paths we have NOT preempted

The HUF MC-4 packet identifies four falsifiability conditions. INV-050 and INV-051 directly preempt Metric defeat and Case defeat. **Two remain open**, and the community is the right room to engage them.

### Prior-art defeat — open invitation

The MC-4 claim, sharpened in push #39 to the three-conjunct form: *"no monitoring framework in the energy / market-share literature operates **natively in Aitchison geometry** with **formal change detection** at the **carrier level** — the three conjuncts combined into one observable stack."* A defeater must overturn the conjunction, not just one disjunct. The pre-sharpening wording was *"no prior monitoring framework tracks compositional market share at the carrier level with formal change detection"* — the sharpened version retains the spirit but tightens the load-bearing language. If the community can name prior work that already combines all three conjuncts explicitly, the MC-4 claim should be narrowed or restated. We have not found such work; we welcome pointers.

Candidates we know about (and consider distinct, but happy to be corrected):

- Aitchison 1982/1986 — foundational simplex geometry, but compositionality as a *statistical condition to handle*, not as a *monitoring observable to read directly*
- Egozcue & Pawlowsky-Glahn 2018 — evidence information, important for scale-invariance discussion, but not framed as monitoring
- Standard market-share monitoring in econometrics — magnitude-based, not compositional
- Diversity indices (Shannon, Herfindahl-Hirschman) — yes for concentration measurement, but typically applied to single-point composition, not compositional drift on the simplex

A broader set of areas worth chasing (CoDa time series; industrial ecology / material flow analysis; diet-composition surveillance; sectoral allocation in macroeconomics) is enumerated in `papers/codawork2026/planning/PRIOR_ART_SEARCH_TARGETS.md`. Pointers to any of those areas — or to areas not on that list — are welcome.

We are open to any of these being more relevant than we think, or to other works we have missed.

### Category defeat — philosophical question

Is *"composition monitoring as a primary observable"* genuinely a distinct monitoring category, or is it at most a useful application note inside existing CoDa? We have no preconceived answer. We welcome the community's view, including the view that this is application-note status and the MC-4 label is too strong.

---

## What the engine actually outputs (so reviewers can verify)

Every CNT v3.1.0 run produces a deterministic JSON. The fields a reviewer might want to inspect first:

| Field | What it carries |
|---|---|
| `tensor.timesteps[t].coda_standard.aitchison_distance_step` | Period-to-period Aitchison distance (the abstract's headline metric) |
| `tensor.timesteps[t].coda_standard.shannon_entropy` | Per-step diversity |
| `tensor.timesteps[t].coda_standard.aitchison_norm` | Distance from simplex barycenter |
| `tensor.timesteps[t].navigation_concentration_family.tv_distance_step` | The packet's parallel half-L1 metric (schema v3.1.0) |
| `tensor.timesteps[t].navigation_concentration_family.k_eff` | exp(Shannon H) — effective categories |
| `tensor.timesteps[t].navigation_concentration_family.k_eff_yoy_change` | Year-over-year derivative of K_eff |
| `tensor.timesteps[t].navigation_concentration_family.concentration_regime` | qualitative tag: tightening / loosening / **deceptive** / stable |
| `tensor.navigation_concentration_summary.regime_counts` | Series-level counts of each regime |
| `helmsman_family.flips.total` | Dominant-axis transitions (the direction-and-persistence diagnostic) |
| `depth_tower.ir_class` | IR taxonomy classification |
| `diagnostics.cnt_content_sha256` | Deterministic content hash |

All nine EMBER countries on the conference's coherent 2001–2025 range are at `papers/codawork2026/conference_2026_06/per_country/ember_*/cnt_v3.json`. Per-country Stage 1 (pure CoDa) and Advanced (full Hˢ + CNQ v2) reports are in the same folders.

---

## How to engage

**For an AI assistant** reading this cold, the fetch order is in `ai-refresh/AI_REFRESH_2026-05-10_codawork2026_redirect.md` (or the most recent AI refresh — see `ai-refresh/HS_ADMIN.json` → `active_priority`). Read in this order:

1. `papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md` (master plan)
2. `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md` (the two empirical findings — INV-050, INV-051)
3. `papers/codawork2026/planning/ABSTRACT_TO_CNT_V3_MAP.md` (operator-by-operator mapping)
4. This document (EXTERNAL_REVIEW_INVITE.md)
5. The accepted abstract (book of abstracts page 25, also in `External_Published_Papers/book-of-abstracts-codawork-2026-draft.pdf`)
6. The HUF MC-4 packet (11 pages, the methods attachment that went with the original submission)

Then critique freely. We are explicitly inviting:

- Claim-strength critique — are we over-reaching anywhere?
- Methodological criticism — is the metric, the threshold, the null model, the regime tag the right one?
- Vocabulary critique — is anything we are naming already named differently in the literature?
- Slide-structure critique — does the 10-beat plan land in 15 minutes?
- Open-question critique — are the three open questions to the community the right ones?
- Prior-art pointers — does anything in the CoDa literature already cover what we claim as novel?

**For a human reviewer** the same documents, the same questions, plus you can directly verify any number in any cnt_v3.json against the public corpus.

---

## What we are not asking for

To save reviewer time, here is what is **out of scope** for this review pass:

- The broader instrument paper ("The Higgins Decomposition: a deterministic compositional diagnostic on the Aitchison simplex") is deferred to a journal track after the conference and does **not** need reviewer attention before June 1
- The CNQ v2.0.0 quaternion view, the depth tower, the IR taxonomy, the helmsman family beyond direct relevance to drift detection — these are appendix material for the talk and do not need to be reviewed for the conference
- The applied tiers (HCI-AUDIO, HCI-ULTRASOUND) are out of scope for this review
- The 101-dataset full-corpus validation is supporting evidence only — not the headline

We want the focus on **energy-mix drift on the simplex** because that is what the audience will hear about.

---

## Repository pointers

- HUF (submission origin): `github.com/PeterHiggins19/Higgins-Unity-Framework`
- Hs (production engine home): `github.com/PeterHiggins19/higgins-decomposition`
- This document: `papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md` on the Hs repo

---

*The conference is the right room to kill the MC-4 claim if it should be killed, or to sharpen it if it should survive. This invite is the pre-conference version of the same posture: surface the methodological and empirical work now, ask the community to press it before the room does, and incorporate good feedback into the slide content. Thanks in advance for any time spent on it.*
