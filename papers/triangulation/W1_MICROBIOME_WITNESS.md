# Witness I — The living system: a gut microbiome says the message is in the ratios

### (Triangulation series, Witness I of three; self-contained — assumes no prior reading)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-22. The first
of three independent witnesses to one compositional law. This paper is **self-contained**: it restates the
whole construction from the ground up, so it can be read alone. The shared foundation is repeated **by
design** — three unrelated systems that each independently require the same formula is the series' result, and
that argument only works if each paper earns it from scratch, with its own receipts. Honest-broker tiered;
real data, read and never copied; deterministic and hash-receipted. Full run + receipts:
`experiments/compositional_message_2026-06/`. Nothing posted; Peter is the sole gate.*

---

## Abstract

We read a real gut-microbiome cohort as a **composition** — parts of a conserved whole — and ask where the
information about an external state (Crohn's disease) lives. A scalar diversity summary (effective number of
taxa) does not separate cases from controls (AUC 0.505, p=0.78). The same data, read through its **inter-part
log-ratios** (the isometric-log-ratio / Aitchison geometry), separates them at AUC 0.832 (PERMANOVA p=0.001),
robustly across model families, and — because the log-ratio representation is scale-invariant — provably
independent of sequencing depth. We prove the underlying principle: the log-ratio map is a *sufficient
statistic*, so by the data-processing inequality every scalar/marginal aggregate is lossy and can be null
while the relational read is strong. We show, further, that the recoverable signal grows with the number of
parts included, up to a finite-sample capacity that we map. The result replicates on an independent HIV cohort
(PERMANOVA p=0.002). A living system, read deterministically and reproducibly, **independently requires the
relational reading** — the first of three witnesses that the message is in the ratios.

## 1. The claim, in this domain (the apex)

> A microbiome is a composition: relative abundances of taxa that always sum to one. If the disease signal it
> carries lives in the **relationships between taxa** rather than in any scalar summary of the community, then
> a relational reading will recover what a diversity index cannot — and the more taxa we include, the more of
> the signal we can read. We test exactly this, and prove why it must hold.

This is one instance of a general principle (the *Compositional Message Principle*). We do not assume it; we
build to it from closure and prove it, then measure it.

## 2. The bedrock: what a composition is (restated from the ground)

A composition is a vector `x = (x₁,…,x_D)` of nonnegative parts carrying only **relative** information; by
convention it is closed to a constant sum (`closure`: divide by the total). Such vectors live on the simplex
with the **Aitchison geometry** \[Aitchison 1986; Egozcue et al. 2003\]. The natural coordinates are
log-ratios:

- **Centered log-ratio** `clr(x) = log x − mean(log x)` — symmetric, but carries a sum-zero constraint.
- **Isometric log-ratio** `ilr(x) = clr(x)·Hᵀ`, where `H` is a Helmert orthonormal contrast basis: an exact
  isometry from the simplex `S^{D-1}` to `ℝ^{D-1}`. The ILR map is a **bijection** — it loses nothing.

These are the only tools the rest of the paper needs. (Canonical implementation:
`HCI-CNTT/engine/geometry.py`.)

## 3. The exact rung and tiling (restated; the trustworthy base)

At four parts the construction is *exact*: the three ILR coordinates are the imaginary part of a quaternion,
and a unit quaternion acts on them by the sandwich `q v q*` — an exact `SO(3)` rotation reproduced to the
IEEE floor (residual ≈ 1.1×10⁻¹⁶, one ULP). Higher-dimensional compositions are covered by overlapping
exact four-part charts and reconstructed through a connected atlas; a balanced tree keeps the conditioning at
`O(log D)`, carrying reconstruction to `D = 10⁶` at ≈ 4.1×10⁻¹² (numerical, not bit-exact identity). The
microbiome here (`D = 48`) sits well inside the exact-and-reproducible regime. (Full treatment: the exactness
paper, P1.)

## 4. Trust by construction (restated)

Every reading is computed by a fixed engine and stamped with a SHA-256 content receipt over a canonical
payload; identical inputs yield identical outputs and a matching hash, verified across independent platforms
(HS-EPS-1). Nothing below depends on a seed or a run; the numbers reproduce. This is what lets a *repeated*
result across witnesses count as evidence rather than echo.

## 5. The message is in the ratios (the theorem)

Let the sample be a composition `x ∈ S^{D-1}` and `Y` an external label. Let `φ = ilr(x)`.

- **Sufficiency.** `φ` is a bijection, so `I(Y; X) = I(Y; φ(X))` — the log-ratio representation is a
  *sufficient statistic* for `Y`.
- **Aggregates are lossy.** For any reduction `g` (a scalar diversity index, a dominance, a total), the
  **data-processing inequality** gives `I(Y; g(φ(X))) ≤ I(Y; φ(X))`, with equality only if `g` is sufficient.
  Permutation-invariant scalar summaries discard *which* taxa move relative to which; they can therefore be
  **near-zero even when the relational signal is large.**

So the prediction is sharp: a diversity index may be null while the full log-ratio read is strongly
informative. §6 measures exactly that.

## 6. The measured witness (Tier 1)

**Data.** `coda4microbiome` Crohn cohort \[Calle, Pujolassos & Susin 2023\]: `N = 975` samples, `D = 48`
genera, 662 Crohn / 313 control. Engine geometry = `HCI-CNTT/engine/geometry.py`. Classifier: L2-regularized
logistic regression on standardized ILR coordinates, repeated stratified 5-fold cross-validation. Significance
by label permutation and by PERMANOVA on Aitchison distance (999 permutations). Seeded; determinism
re-checked (identical AUC on rerun).

| representation | what it is | separation AUC | test |
|---|---|---:|---|
| effective diversity `K_eff` | scalar aggregate | **0.505** | Mann-Whitney p = 0.78 |
| Shannon entropy | scalar aggregate | 0.505 | p = 0.78 |
| Gini dominance | scalar aggregate | 0.527 | p = 0.18 |
| sequencing depth | non-compositional magnitude | 0.557 | p = 0.004 |
| **ILR log-ratios** | the full relational read | **0.832** (sd 0.004) | **PERMANOVA F = 22.4, p = 0.001**; classifier permutation p = 0.005 |

The diversity null is reproduced exactly; the relational geometry recovers a strong signal the aggregates are
blind to. Because ILR is scale-invariant, this 0.832 is **provably depth-free** (depth alone reached only
0.557), and it is not an artifact of the classifier: random forest gives 0.864 and an Aitchison-distance kNN
gives 0.838. *(Figure: `fig1_law1_relational_vs_aggregate.png`.)*

**More parts, more message — up to capacity.** Including the top-`n` genera plus an amalgamated remainder and
sweeping `n`, the cross-validated AUC rises from 0.64 (3 parts) to 0.83 (48 parts) and saturates around
25-33 parts; a second, label-free ordering (by CLR variance) gives the same rise. The increase is the
predicted **dimensional articulation**; its saturation is the honest finite-sample boundary `D*(N)` (here `N`
is large relative to `D`, so the curve rises cleanly). *(Figure: `fig2_law2_dimensional_articulation.png`.)*

**Independent replication.** On an independent HIV cohort (`N = 155`, `D = 60`) the relational locus
replicates — aggregates ≤ 0.543, relational PERMANOVA p = 0.002 — and the articulation curve there *peaks and
declines* at full dimension, exactly as the finite-sample boundary predicts when `N/D ≈ 2.6`. The boundary is
reported, not hidden.

**Receipts.** Result hash `acf65ce93f7020d5` (Crohn), `252ed1984c57e956` (HIV); inputs hashed; reproduce with
`cmp_analysis.py` / `cmp_replicate.py` / `cmp_verify.py` (seed 20260622). Independent re-computation confirms
the ILR round-trip to 1.8×10⁻¹⁵ (the sufficiency premise), the AUC across model families, and the PERMANOVA.

## 7. Back to the apex

A living community of bacteria — which cannot have been arranged to agree with anything — independently
requires the relational reading: its disease signal is invisible to the scalar summary and visible in the
ratios, exactly as the sufficiency theorem says, and it scales with dimension up to the sample's capacity.
This is **one located coordinate** of the compositional law. Two more witnesses, in unrelated domains
(a deep-time mudstone; an engineered fleet), are needed to locate it; they are the companion papers.

## 8. Honest envelope

- **Tier 1 (measured/proven):** the sufficiency theorem and the DPI corollary; the Crohn separation
  (relational ≫ aggregates), depth-invariance, cross-model robustness, PERMANOVA; the HIV replication; the
  articulation curve and its `D*(N)` boundary; determinism + receipts.
- **Tier 2/3 (not claimed):** no biological causation and no clinical use — this locates *where the signal
  lives*, not *why*; diversity is a **lossy** read, not a wrong one; the HIV cohort carries a known
  enterotype (MSM) confounder, irrelevant to the locus question; universality across all compositional
  domains is the *series'* claim (T2/T3), established only by the three witnesses together, not by this paper
  alone.
- **Kills.** The claim dies if a relationship-blind scalar aggregate ever matches the full relational read on
  a real labeled composition. It did not here.

## 9. Reproducibility

Open scripts, seeded, deterministic, hash-receipted; real data read from `coda4microbiome` and never copied
into the repository (instrument-not-data). The relational reading, the permutation and PERMANOVA tests, the
dimensional sweep, and the independent-model checks all reproduce from the replication kit at
`experiments/compositional_message_2026-06/`.

## Acknowledgments

Developed from a body of acoustic-engineering practice; AI-assisted per HUF-STD-001. The AI collective
contributed independent cross-checks (proof re-derivation, code re-runs, claim audits); all claims are the
author's. Data: Calle, Pujolassos & Susin (2023), *BMC Bioinformatics* 24:82.

## 10. Supporting studies — the three-study trust (HUF support standard)

This witness does not rest on a single run; two supporting studies reinforce it into a three-study trust:

- **Support A — HIV replicate.** The same *relational ≫ aggregate* pattern replicates on an independent HIV
  cohort (permutation p = 0.002) — the result is not Crohn-specific (`cmp_result_hiv.json`).
- **Support B — dimension is the message.** On the Crohn data, as parts grow 5 → 48 the relational AUC rises
  **0.64 → 0.83** and the compositional **symbol-capacity 7 → 79 bits**, while the scalar Shannon read stays at
  chance — the message grows with the number of parts (`bf24c615…`,
  `../../experiments/dimension_is_the_message_2026-06/`).

Main + A + B = a three-study trust. Full chain: `../NINE_STUDY_TRUST_LEDGER.md`; literature placement:
`../COMMUNICATIONS_GEOMETRY_LITERATURE_SCAN.md`.

*Witness I of three. The message is in the ratios — measured here, proven generally, and located only when
the mudstone (Witness II) and the fleet (Witness III) say the same thing with their own receipts.
Cross-refs: `../COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md`, `../TRIANGULATION_TRILOGY_PLAN.md`,
`../P7_FOUNDATIONS_SEED.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide. See [`../PROOF_AND_HONESTY_STANDARD.md`](../PROOF_AND_HONESTY_STANDARD.md).*
