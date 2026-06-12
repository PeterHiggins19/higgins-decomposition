# CNQ — ROI and Use Cases (when does this system make sense?)

**Status:** experimental / candidate. See [`README.md`](README.md).
**Companion:** [`CNQ_VS_CODA_VS_CNT_COMPARE.md`](CNQ_VS_CODA_VS_CNT_COMPARE.md) for the dimension-by-dimension comparison.
**Approach:** the same supportive ROI framing as the existing CNT ROI paper (`HCI-CNT/coda_community/CNT_ROI_AND_USE_CASES.md`), extended to the three-tier system.

---

## The headline answer

CNQ makes sense when **at least two** of the following hold:

1. **D ≥ 8 carriers** (where CNT's channel-by-channel decomposition starts to obscure rather than reveal structure).
2. **Bundle of N ≥ 10 trajectories** to cross-compare (where Stage 4's bespoke pairwise logic becomes the bottleneck).
3. **T ≥ 1000 timesteps** (where smooth interpolation between timesteps matters, and SLERP's quality vs linear-CLR becomes visible).
4. **Audience includes adjacent communities** (robotics, graphics, physics, quantum information) where quaternion vocabulary opens doors that CoDa/CNT vocabulary doesn't.
5. **Cross-dataset structure is the primary observable** (you care more about how trajectories relate to each other than about any one trajectory's per-step values).

If none of these hold, CNT is the right tier. If exactly one holds, CNT can probably handle it with some engineering. If two or more hold, CNQ becomes the natural choice.

---

## The break-even composition (extended from the CNT ROI paper)

The original CNT ROI paper rendered the time-budget composition as a CoDa-style ternary diagram with three vertices: data ingestion, analysis, communication. CNQ adds a fourth vertex — **adjacent-community engagement** — which the channel-by-channel CNT vocabulary does not unlock.

A four-vertex composition is naturally rendered as a tetrahedron (the 3-simplex). CNQ time-budget composition for a typical large-system analysis:

| Vertex | CoDa-only baseline | CNT-on-CoDa | CNQ-on-CNT-on-CoDa |
|---|---:|---:|---:|
| Data ingestion / cleaning / closure | 60% | 30% | 25% |
| Analysis (per-trajectory + cross-dataset) | 30% | 40% | 25% |
| Communication / writeup | 10% | 25% | 25% |
| Adjacent-community engagement | 0% | 5% | 25% |

The interesting shift is the fourth row. CoDa-only and CNT analyses spend almost no time engaging adjacent communities because the communication cost is high (you must teach Aitchison geometry first). CNQ analyses spend a quarter of the time there because the vocabulary is already shared with robotics, graphics, physics, and quantum information.

In ROI terms: CNQ doesn't reduce per-analysis cost much (the algebra has similar complexity per step). It **reallocates** time from per-analysis cost to adjacent-community engagement, which is where the longer-term collaborative ROI lives.

---

## When CNQ makes sense, by use case

### Climate modeling (clear yes)

The CMIP archive (Coupled Model Intercomparison Project) contains compositional time series at scales CNT was not designed for: D=20-100 atmospheric mixing ratios, ocean tracer compositions, vegetation cover fractions, ice-mass distributions; T=1000+ months across multi-decade runs; N=10-50 model intercomparisons per scenario.

For a typical CMIP analysis:
- D=30 (atmospheric chemistry composition over time)
- T=1200 (100 years of monthly samples)
- N=30 (CMIP6 ensemble of GCMs running the same scenario)

CNT can analyze a single GCM's trajectory in this regime, but the cross-model intercomparison (the actual scientific goal) requires N²/2 = 435 pairwise Stage 4 comparisons, each with bespoke per-channel arithmetic. CNQ's Hamilton-product approach does the same 435 comparisons via 435 single-line algebraic operations, with the relative quaternion R(t) carrying all the cross-model structure as one object.

**Verdict.** Strong CNQ use case. The post-CodaWork outreach to climate modelers is the natural first adjacent-community engagement.

### Multi-decade economic flows (clear yes)

National accounts, sector composition over decades, cross-country comparison. UN System of National Accounts uses 17 sector classifications (D=17), 60+ countries (N=60+), monthly or quarterly data over 50+ years (T=600-2000).

CNT's EMBER 8-country corpus is the small-bundle prototype of this. CNQ-grade analysis would scale to the full SNA: 60-country bundle of D=17 trajectories with T=2000, computing pairwise relative-quaternion R(t) and bi-quaternion factoring for sector-level cross-comparisons.

**Verdict.** Strong CNQ use case. The IIASA / NGFS / SNA communities would recognize the value immediately.

### Industrial process composition (yes for certain processes)

Refinery streams, fermentation broths, chemical process monitoring — D in the tens to hundreds, T in the thousands of samples, sometimes large N (multi-batch comparisons).

Where the process composition is **multi-modal** (several distinct sub-systems coexisting in the same stream), the bi-quaternion or higher-Clifford factoring exposes the modal structure naturally. Where the process is **single-mode** (one dominant compositional signature with small variations), CNT is sufficient.

**Verdict.** CNQ for multi-modal processes; CNT for single-mode.

### Microbiome cohorts (yes with dominant-mode reduction)

Microbiome data is high-D (D=1000+ taxa), low-T (T=10-100 samples per subject), large-N (N=100+ subjects per cohort). Direct CNQ at D=1000 is computationally impractical; the natural approach is dominant-mode reduction (project to the most variable D=4 or D=8 subspace, carry the residual as CNT-compatible), then run CNQ on the reduced subspace.

This is a hybrid use case: CoDa cleans the OTU table; CNT analyzes per-subject trajectories at D=1000; CNQ analyzes the cohort-level structure at the reduced D=4 or D=8 subspace.

**Verdict.** Strong CNQ use case for cohort-level structure; CNT for per-subject; CoDa throughout for foundation.

### Gene-expression panels (yes with Clifford-algebra extension)

D = 10,000-30,000 genes, T = small (cell-cycle phases or treatment timepoints), N = thousands of cells (single-cell RNA-seq) or hundreds of subjects (bulk RNA-seq). At this scale, even CNQ's quaternion native operations need Clifford-algebra extensions; the practical approach is heavy dimensional reduction (gene modules, pathway-level aggregations) before applying CNQ.

**Verdict.** CNQ + dimensional reduction is the path; raw CNQ at D=30,000 is a CNQ v2.0+ problem.

### Single-domain ecology / geology / commodities (CNT is sufficient)

Most current corpus experiments fall here. D ≤ 10, T ≤ 1000, N=1 to 8. CNT's existing Stage 1-4 atlas does everything that's needed; CNQ would add complexity without proportional benefit.

**Verdict.** Stay with CNT. CNQ is over-engineering for this regime.

### Single static composition (CoDa is sufficient)

Cross-sectional study, snapshot analysis, distribution comparison. CoDa's variation matrix, biplot, balance dendrogram are exactly the right tools.

**Verdict.** Stay with CoDa. Even CNT is over-engineering.

---

## The break-even decision rule, formalised

A scoring rule for "should I use CNT or CNQ" given a problem:

```
score = 0
if D >= 8:                                   score += 2
if D == 4:                                   score += 1     # sweet-spot dimension
if N >= 10:                                  score += 2
if T >= 1000:                                score += 1
if cross_dataset_is_primary:                 score += 2
if audience_includes_adjacent_community:     score += 2
if continuous_time_interpolation_quality_matters: score += 1
if D == 8 and bi-quaternion_factoring_makes_sense: score += 1   # natural decomposition
if D > 30:                                   score += 1     # need Clifford generalisation
```

- **score < 3** → CNT is sufficient.
- **score 3-5** → CNT works; CNQ would help but the engineering cost is real. Choose based on outreach goals.
- **score ≥ 6** → CNQ is the right tier. The complexity is in the problem, not in the solution; CNQ's algebra is already mature.

For backblaze_fleet (D=4, T=731, N=1, single-domain): score = 1+0+0+0+0+0 = 1 → CNT is sufficient (which is correct; CNT already serves this dataset perfectly).

For a CMIP6 ensemble analysis (D=30, T=1200, N=30, cross-dataset primary, climate-modeler audience): score = 2+0+2+1+2+2+1+1 = 11 → CNQ is clearly the right tier.

For an EMBER-style 8-country annual energy mix (D=8, T=26, N=8): score = 2+0+0+0+0+0+0+1 = 3 → CNT works (current); CNQ would add the bi-quaternion factoring as upside.

---

## ROI scenarios (when CNQ pays back its engineering cost)

The CNQ engineering cost is estimated at ~14 days (per [`../doctrine/BENEFITS_POST_CODA.md`](../doctrine/BENEFITS_POST_CODA.md)). For that investment to make sense:

**Scenario A — single climate-model adoption.** One climate-modeling group adopts CNQ for their CMIP analysis. Their per-paper time savings: 3-5 days (Stage 4 cross-model comparisons reduce from per-channel arithmetic to single-line Hamilton products). Their per-paper communication benefit: significant — referees in adjacent fields recognize the algebra. **Break-even: ~3 papers, ~6-12 months.**

**Scenario B — economics consortium adoption.** IIASA or NGFS adopts CNQ for cross-country economic flow analysis. Their analyses are larger (60+ countries vs 8 EMBER) and their cross-dataset cost dominates. CNQ's O(N²) Hamilton products become the working paradigm. **Break-even: 1-2 reports, ~3-6 months.**

**Scenario C — robotics / SLAM cross-pollination.** Robotics community recognizes that compositional analysis on SU(2) is exactly what they're doing; they bring their noise-robust quaternion estimation techniques to CNT/CNQ; CNT/CNQ adopts them; both fields benefit. **Break-even: depends on the depth of cross-pollination, but the door has to be open first.**

**Scenario D — quantum information cross-pollination.** Quantum-information researchers recognize the spinor-parity structure in CNT's LIMIT_CYCLE_P2 corpus experiments and connect it to qubit dynamics. New domain opens. **Break-even: speculative, but high upside if the connection is real.**

In all four scenarios, the engineering cost is paid back through reduced per-analysis time and through unlocking adjacent-community engagement that CNT's vocabulary does not unlock.

---

## When NOT to invest in CNQ

- If the project is winding down (final paper, final corpus snapshot) and won't see new analyses. CNT is the right finishing tier.
- If the audience is exclusively the CoDa community. They have CoDa; CNT is the upgrade they care about; CNQ is not the right vocabulary for that audience.
- If budget for the ~14 days of engineering work isn't available. CNT works; defer CNQ.
- If the corpus is small (≤ 25 experiments) and the per-experiment cost is low. The CNT corpus today fits this; CNQ's value comes from scale that the corpus doesn't yet have.

---

## The post-CodaWork question

CNQ's ROI hinges on what happens after CodaWork 2026. Three scenarios:

**Scenario 1 — CodaWork goes well, project enters maintenance.** Existing CNT corpus is the deliverable; nothing new is built. CNQ's engineering cost isn't recouped. CNQ archives as "interesting validated direction; not pursued."

**Scenario 2 — CodaWork goes well, project picks up climate-science partner.** Climate partner needs scale CNT wasn't designed for. CNQ's ~14 days of engineering becomes the unlock for the partnership. ROI clear within 6 months.

**Scenario 3 — CodaWork goes well, project picks up multiple adjacent-community partners.** CNQ becomes the bridge into multiple fields; the spinor-parity diagnostic, bi-quaternion factoring, and SLERP interpolation each become the key insight for a different community. Engineering cost recouped within months; ongoing collaborative research replaces single-author research.

**My assessment:** Scenario 2 is most likely (climate-modeling outreach is the natural first adjacent-community engagement). Scenario 3 is possible if Peter chooses to pursue it. Scenario 1 is the floor — CNQ archives cleanly even if it's never built, with the validated foundation as a citable result.

---

## Decision framework, summarised

| If your typical analysis has | Then use |
|---|---|
| D ≤ 3, single composition | CoDa |
| D = 2-10, T = 10-1000, N = 1-8, single domain | CNT (current sweet spot) |
| D = 4 or D = 8 specifically, multi-bundle, cross-domain audience | CNQ (natural fit, bi-quaternion factoring works) |
| D = 10-100, T = 1000+, N = 10+, climate / economics / industrial process | CNQ (the design target) |
| D = 100+ (microbiome, gene expression) | CNQ + dominant-mode reduction (hybrid) |
| Audience needs to recognize the algebra immediately (robotics, physics, graphics) | CNQ (vocabulary unlock) |

---

*The instrument reads. The expert decides. The hashes carry the receipts. CNQ makes sense when the problem is bigger than CNT's working memory — and when the audience is bigger than the CoDa community.*
