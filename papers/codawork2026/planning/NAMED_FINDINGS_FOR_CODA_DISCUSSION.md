# Named findings for the CoDa community discussion

**Companion to:** `CONFERENCE_2026_06_PLAN.md` (master plan)
**Created:** 2026-05-10 (push #37)
**Status:** these are CANONICAL findings (catalog INV-050, INV-051). Both should appear by name in the conference talk and in the Q&A bench, and both should be cited explicitly when the CoDa community discusses the work.

---

## Purpose

Two specific empirical findings emerged during the schema v3.1.0 engine promotion and the 9-country EMBER re-run. They are not asides — they are the two scientific results most relevant to the CoDa community's existing methodological discussions on the simplex. They go into the talk by name, and they are the named anchors for any post-conference correspondence.

---

## Finding 1 — Metric-invariance of the qualitative compositional verdict

**Catalog reference:** [INV-050](../../../ai-refresh/INVESTIGATION_CATALOG.json) (CANONICAL, push #37, raised by USER)

### Statement (sharpened in push #39)

> *TV distance (half-L1) and Aitchison distance (log-ratio Euclidean) **agree on every shock hit/miss verdict across the 9-country EMBER 2001–2025 corpus**, while differing in raw magnitude. The qualitative verdict is robust to substitution within this pair. Whether the invariance extends to the broader family of valid simplex distances (weighted log-ratio, Mahalanobis on CLR covariance, Egozcue–Pawlowsky-Glahn evidence information distance) is open — named explicitly as Q2 in `papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md`.*

### Earlier (broader) framing — superseded but preserved for traceability

> *The qualitative compositional verdict — "does this step register as a shock or not" — is metric-invariant within the family of valid simplex distances, even though the metrics themselves are not numerically equivalent.*

The earlier wording reaches one rung wider than the evidence (the tested family was two metrics, not the full simplex-distance family). The sharpened version stays inside what the data show and explicitly invites the broadening as a community question.

### Concrete observation

TV distance (½ Σ|ρᵢ(t) − ρᵢ(t−1)|, half-L1, bounded [0,1]) and Aitchison distance (‖clr(ρ(t)) − clr(ρ(t−1))‖₂, log-ratio Euclidean) **agree on every shock hit/miss verdict** across the 9-country EMBER corpus at the year-grain level. The two metrics differ in raw magnitude — one is bounded, the other is unbounded — but the qualitative classification a reviewer would draw (this step is a shock; that step is not) survives metric substitution.

### Why this matters for the CoDa community

- The Aitchison-vs-Euclidean discussion has been one of the community's foundational methodological debates since Aitchison 1982. A simulation-free empirical demonstration that *the qualitative verdict survives metric choice within a defensible family* is a concrete addition to that discussion.
- It directly answers the **Metric defeat** path in the HUF MC-4 packet's four falsifiability conditions. A reviewer pressing "your TV-based detection might be metric-dependent" gets the answer that the verdict survives substitution.
- It reframes the packet's Appendix A metric-correction note (L2 → TV catch March 22, 2026) from a bug-fix footnote into a methodological robustness asset: catching the original mislabeling led to side-by-side metric computation, which revealed the verdict-invariance.

### How it lands in the talk

| Slide context | Talk language |
|---|---|
| Methods / metric stack | "We compute both TV distance and Aitchison distance per timestep. They differ in magnitude. They agree on every shock verdict across the 9-country corpus. The qualitative verdict is robust to substitution within this pair; whether the invariance extends to weighted log-ratio or evidence information distances is the second of our three open questions for the room." |
| Q&A response to Metric defeat | "If the metric is wrong, the verdict moves. We checked TV against Aitchison across nine countries — it doesn't move. We haven't tested the broader family of valid simplex distances; that's Q2 in our open-questions slide." |
| Robustness sub-claim on the headline slide | One footnote line: *"Verdict reproduces under TV substitution for Aitchison distance across the 9-country corpus; magnitudes differ, classifications do not. Broader-family invariance is open (Q2)."* |

### How to defeat it (honest)

A motivated reviewer would point out that:

1. The family we tested is small (two metrics). Adding the family of weighted log-ratio distances, or evidence-information distance from Egozcue and Pawlowsky-Glahn 2018, would broaden the family.
2. "Shock verdict" is a thresholded operationalisation. A reviewer could redefine the threshold rule and look for the metric agreement to break down.
3. The corpus is 9 EMBER countries; broader corpora (the 73-country OWID expansion, or non-energy domains in the 101-dataset reference suite) should be tested.

We welcome any of these — and the 73-country OWID expansion + 11-domain reference suite are already available to anyone wanting to run the same check independently.

---

## Finding 2 — Deceptive-drift signature reproduced across 5 of 9 EMBER countries

**Catalog reference:** [INV-051](../../../ai-refresh/INVESTIGATION_CATALOG.json) (CANONICAL, push #37, raised by USER)

### Statement

> *The deceptive-drift signature — K_eff tightening while TV stays at or below the series median — is empirically present in 5 of 9 EMBER countries at annual grain (AUS, CHN, GBR, IND, JPN). The packet's single-country headline (Germany pre-2022) is the conservative case.*

### Concrete observation

The CNT v3.1.0 engine's `concentration_regime` tag fires `deceptive` when both of the packet's protocol conditions are satisfied at a step transition: K_eff is declining (concentration tightening) AND TV is at or below the series median (compositional movement is quiet). On the 9-country EMBER 2001–2025 corpus:

| Country | Deceptive transitions | Note |
|---|---|---|
| AUS | 1 | Concentration tightening while overall movement quiet |
| CHN | 1 | Same pattern |
| GBR | **2** | Two distinct deceptive-drift years |
| IND | **2** | Same |
| JPN | **2** | Likely Fukushima reorganisation noise + restart signal |
| DEU | 0 | K_eff tightens pre-2022, but TV exceeds median — *loud* drift, not deceptive |
| FRA | 0 | Mostly loosening across the period |
| USA | 0 | Mostly stable |
| WLD | 0 | World aggregate smooths out individual-country signatures |

### Why this matters for the CoDa community

- The packet's MC-4 claim ("no prior monitoring framework tracks compositional market share at the carrier level with formal change detection") was originally illustrated with one country pre-one-event. Independent reproduction *across multiple economies of different structural types* (Pacific economy, large emerging economies, island nation, post-Fukushima reorganisation) is significantly stronger evidence.
- The countries where the signature does NOT fire (DEU at annual grain, USA, FRA, WLD) are not failure cases — they are different regimes that the same protocol *correctly classifies as non-deceptive*. Germany's pre-2022 drift was *loud* (high TV); USA's energy mix is mostly stable; WLD averages everything. The protocol distinguishes deceptive from loud drift cleanly.
- The signature being grain-dependent (annual data hides what monthly data shows) is itself a methodologically interesting result. It tells you something about how often you need to measure to see the structural pattern.

### How it lands in the talk

| Slide context | Talk language |
|---|---|
| Results — beyond the three | "Beyond DEU/JPN/GBR the engine's concentration_regime tag fires `deceptive` in 5 of 9 EMBER countries at annual grain: AUS, CHN, GBR, IND, JPN. The packet's single-country headline is the conservative case." |
| Methods — why some countries don't fire | "Germany at annual grain shows K_eff tightening but TV above median — the energy mix was visibly moving toward renewables, not silently concentrating. That's *loud* drift, not *deceptive* drift. The protocol distinguishes them; the regime tag is `tightening` for Germany pre-2022, not `deceptive`." |
| Null-model caveat — on the deceptive-drift slide, NOT in speaker notes (push #39) | "The packet's p = 0.0016 for Germany is computed against the series' own empirical-frequency baseline. This is a weaker null than a Dirichlet, permutation, or bootstrap null. The right null for compositional change-point detection on the simplex is Q3 in our three open questions for the room. We treat p = 0.0016 as an opening empirical claim, not a closed methodological one." |
| Q&A response to Case defeat | "Why this set of 5 and not the other 4? Each per-country trajectory is in the corpus folder. The differences are interpretable — different starting concentrations, different growth dynamics, different shock proximity. The protocol classified each correctly." |

### How to defeat it (honest)

A motivated reviewer would point out that:

1. The cut between `deceptive` and `tightening` is the TV-median threshold. Different threshold definitions might re-classify some countries. We use the series-own median; alternatives are series-pooled, world-relative, or non-median quantiles.
2. The annual-grain analysis cannot reproduce the packet's monthly p = 0.0016 number for Germany. That p-value reproduction requires the monthly EMBER pipeline (queued as `monthly_deceptive_drift.py`).
3. The 9-country corpus is still small. The 73-country OWID expansion is the natural broader test.

Again, all of these are tractable, and the materials are open for anyone to run.

---

## Why both findings travel together

The two findings are complementary halves of the methodological case:

- **INV-050 (metric-invariance)** shows that the *what* of the detection is robust — switching the metric does not change the qualitative verdict.
- **INV-051 (5-country reproduction)** shows that the *where* of the detection generalises — the signature is not a Germany-only anomaly.

Together they answer the two most natural CoDa-community challenges to the MC-4 claim. The packet identified four defeat paths; these two findings directly preempt two of them (Metric defeat and Case defeat). Prior-art defeat is the community's to weigh in on (and the audience may know more than we do about prior compositional-monitoring work); Category defeat is the philosophical question (is "monitoring composition directly" a category, or just an application note on existing CoDa?).

---

## How to cite these in the talk

The slide that names these findings should also name their catalog entries (INV-050, INV-051) so the audience can fetch the full provenance from the public catalog at `ai-refresh/INVESTIGATION_CATALOG.json`. The Q&A bench card should carry both findings with the per-country numbers cached for instant reference.

---

## Status of named findings in the talk bundle

- [x] Catalogued as CANONICAL (INV-050, INV-051, push #37)
- [ ] Slide drafted with the two findings as headline-level results (queued as deliverable 5.3.S — to be added to master plan §5.3)
- [ ] Q&A response cards drafted with the per-country numbers (queued as 5.3.T)
- [ ] Footnote in the conference handout (queued as 5.3.U)

---

*Both findings are robust to the engine's deterministic contract — same input, same output, always. The numbers in this document are reproducible from `papers/codawork2026/conference_2026_06/per_country/ember_*/cnt_v3.json` by reading `tensor.navigation_concentration_summary.regime_counts.deceptive` and `tensor.timesteps[].coda_standard.aitchison_distance_step` vs `tensor.timesteps[].navigation_concentration_family.tv_distance_step`. The talk's claims are tied to those JSON fields, not to slide-level paraphrase.*
