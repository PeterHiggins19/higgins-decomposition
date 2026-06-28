# P8 (seed) — The Compositional Message Principle: the discriminative signal lives in the log‑ratios, and scales with the number of parts up to a sample‑set capacity

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑22. A living
**paper seed** — a small, sharp, falsifiable result with a proof and a two‑cohort real‑data test, written to
be honest about its boundary. Honest‑broker tiered. Nothing posted; Peter is the sole gate. This formalises
and tests the "the system is the message" thesis ([`../library/THE_SYSTEM_IS_THE_MESSAGE.md`](../library/THE_SYSTEM_IS_THE_MESSAGE.md));
the full run + receipts live at [`../experiments/compositional_message_2026-06/`](../experiments/compositional_message_2026-06/).*

---

## Abstract (draft)

In a compositional system — parts of a conserved whole — we ask *where* the information about an external
state is carried, and *how it scales with the number of parts*. We state the **Compositional Message
Principle**: (1) the isometric log‑ratio (ILR) representation is a sufficient statistic, so the discriminative
signal lives in the inter‑part **ratios**, and scalar/marginal aggregates (diversity, dominance, depth) are
lossy and can be null while the relational signal is strong; (2) recoverable information is **non‑decreasing
in the number of parts** at the population level, with a finite‑sample boundary — in a sample of size N the
realized signal rises with the number of parts only up to an **effective dimension D\*(N)**. We prove (1) and
the population half of (2) by sufficiency and the data‑processing inequality, and test both on two independent
gut‑microbiome cohorts. On Crohn's disease (N=975, D=48) — where effective diversity is null (AUC 0.50,
p=0.78) — the relational geometry separates cases at AUC 0.83 (PERMANOVA p=0.001), depth‑free by construction,
and the signal rises monotonically with the number of parts to saturation. On an HIV cohort (N=155, D=60) the
relational locus replicates (PERMANOVA p=0.002) but the dimensional curve **peaks mid‑dimension and declines**
— exactly the predicted finite‑sample boundary (N/D≈2.6), only partly mitigated by regularisation. The honest
boundary is part of the contribution: a compositional dataset has an effective dimension it can support, and
it scales with sample size.

## 1. Contribution

A single, provable, falsifiable statement about compositional data with a clean two‑cohort test and an
explicitly mapped failure mode — the kind of small result that is *earned* rather than asserted. It gives a
principled reason to read compositions in log‑ratio coordinates (not via scalar summaries) and a principled
caution about how many parts a given sample can actually exploit.

## 2. The theorems (T1)

Sample `x ∈ S^{D-1}` (closed, positive); label `Y`; `φ = ilr(x): S^{D-1} → R^{D-1}` (Aitchison isometry,
a bijection).

- **T‑1 (Relational Locus / sufficiency).** `I(Y;X) = I(Y;φ(X))`; for any reduction `g`,
  `I(Y;g(φ(X))) ≤ I(Y;φ(X))` (data‑processing inequality), equality iff `g` is sufficient. Permutation‑
  invariant scalar aggregates are lossy `g`'s. **⇒ the message is in the ratios.**
- **T‑2a (Articulation, population).** Amalgamation is a deterministic coarsening `A`; a coarser `D'`‑part
  view is `A(φ_D(X))`, so `I(Y;φ_{D'}) ≤ I(Y;φ_D)` (DPI). **⇒ recoverable information is non‑decreasing in D.**
- **T‑2b (Articulation, finite sample).** A consistent estimator `Î_N(D)` has variance increasing with `D/N`;
  realized signal ≈ `I(D) − penalty(D,N)`, which rises then (for `N ≲ D`) falls — defining an effective
  dimension `D\*(N)`.

## 3. The evidence (T1 — measured; coda4microbiome, Calle et al. 2023)

| cohort | aggregates (best) | relational ILR | PERMANOVA | articulation |
|---|---:|---:|---|---|
| **Crohn** N=975, D=48 | K_eff/Shannon **0.505** (p=0.78) | **0.832** (sd .004) | F=22.4, **p=0.001** | **rises 0.64→0.83**, saturates ~25–33 parts (two label‑free orderings) |
| **HIV** N=155, D=60 | ≤ **0.543** | full‑D 0.618 / best low‑D **0.71** | F=3.5, **p=0.002** | **peaks mid‑D, declines** (N/D≈2.6); CV‑tuning lifts full‑D 0.61→0.66, still non‑monotone |

Relational ≫ aggregate on both cohorts (T‑1 supported); population monotonicity proven (T‑2a) and realised on
Crohn; the finite‑sample boundary (T‑2b) demonstrated on HIV exactly as predicted. ILR scale‑invariance makes
the relational signal provably independent of sequencing depth (depth alone ≤0.557).

## 4. Honest envelope (kills + non‑claims)

- **Kills.** T‑1 dies if a relationship‑blind aggregate ever matches the full relational read on a real
  labeled composition. T‑2a dies if a correct estimator shows information strictly decreasing in D at large
  N. T‑2b dies if the peak/decline fails to track N/D across datasets.
- **Not claimed.** No biological causation; no clinical use; diversity is *lossy*, not *wrong*; HIV carries a
  known MSM enterotype confounder (we test *where* the signal lives, not *why*); generality beyond gut‑genus
  data is **T3** until more domains (energy, finance, geology, gas) are run through the identical pipeline.
- **Determinism.** Seeded, hash‑receipted (Crohn `acf65ce93f7020d5`, HIV `252ed1984c57e956`), identical on
  rerun; engine geometry is the repo's own `HCI-CNTT/engine/geometry.py`.

## 5. Related work & venue (to firm up)

Compositional data analysis (Aitchison; Egozcue–Pawlowsky‑Glahn ILR), log‑ratio microbiome methods
(`coda4microbiome`: Calle, Pujolassos & Susin 2023), PERMANOVA (Anderson 2001), and sample‑complexity /
bias–variance for high‑dimensional classification. The novelty here is the *framing as a message‑locus +
articulation principle with an explicit effective‑dimension boundary*, tied to the Hˢ exact‑reading program
(P1) and MC‑4 / ratio‑blindness ([`../../HUF/huf-gov/RATIO_BLINDNESS_DOCTRINE.md`]). Likely venue: a
CoDa / applied‑statistics methods note. (Prior‑art sweep is required before any "first/novel" wording.)

## 6. Status

**SEED — proof + two‑cohort test complete; honest boundary characterised.** Next, only if Peter directs:
(a) replicate T‑1 across non‑microbiome compositions already in the repo (energy/finance/geology/gas) for the
generality claim; (b) estimate `D\*(N)` directly via a learning‑curve sweep (vary N at fixed D) to make T‑2b
quantitative; (c) prior‑art sweep + venue fit. Registered in the abstract ledger as P8 (seed). Names off the
public repo; Peter is the sole gate; nothing posted.
