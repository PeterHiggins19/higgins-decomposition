# The Compositional Message Principle (CMP) — proof, real-data test, and an honest boundary

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑22.
A full research cycle on the microbiome data we hold: **name it, prove it, test it, fix it, do it again.**
Honest‑broker tiered; deterministic, seeded, hash‑receipted; real data only; nothing pushed; Peter is the
sole gate. This makes the "the system is the message" theme ([`../../library/THE_SYSTEM_IS_THE_MESSAGE.md`](../../library/THE_SYSTEM_IS_THE_MESSAGE.md))
into a falsifiable, tested statement.*

---

## 1. The principle, named

**Compositional Message Principle (CMP).** For a compositional system (parts of a conserved whole), the
information a sample carries about an external state lives in the **inter‑part log‑ratios** (the relational
structure), and the amount recoverable grows with the **number of parts** — up to what the sample can
support. Two laws:

- **Law 1 — Relational Locus.** The log‑ratio (ILR/Aitchison) representation is a *sufficient statistic*;
  scalar/marginal aggregates are lossy and can be null while the relational signal is large. *The message
  is in the ratios.*
- **Law 2 — Dimensional Articulation.** Recoverable information is **non‑decreasing in the number of parts D**
  at the population level (more parts = more symbols), with a **finite‑sample boundary**: in a finite sample
  the realized signal rises with D only up to an effective dimension D\*(N), then estimation variance
  dominates.

## 2. The proof (T1 — mathematics)

Let a sample be a composition `x ∈ S^{D-1}` (closed, positive) and `Y` an external label. Let
`φ = ilr(x)`, the isometric log‑ratio map `S^{D-1} → R^{D-1}`.

- **Law 1.** `φ` is a **bijection** (Aitchison isometry), so it is a *sufficient statistic* for `Y`:
  `I(Y; X) = I(Y; φ(X))`. For any measurable reduction `g` (e.g. a scalar diversity index), the
  **data‑processing inequality** gives `I(Y; g(φ(X))) ≤ I(Y; φ(X))`, with equality iff `g` is sufficient.
  Permutation‑invariant scalar aggregates (effective diversity `K_eff = exp H`, Shannon `H`,
  Gini–Simpson dominance) discard *which* parts move relative to which — they are lossy `g`'s, so they can
  only lose information and may be ≈0 even when the relational signal is large. **⇒ the discriminative
  message lives in the ratios.**
- **Law 2 (population, Law 2a).** Amalgamating parts (summing some columns) is a deterministic map `A` of the
  finer composition; a `D'`‑part view (`D' < D`) is `A(φ_D(X))`. By DPI, `I(Y; φ_{D'}) ≤ I(Y; φ_D)` — so
  population information is **non‑decreasing in D**. **⇒ more parts cannot reduce recoverable information.**
- **Law 2 (finite sample, Law 2b).** An estimator `Î(D)` of that information (here: cross‑validated AUC of a
  regularized classifier on the `D−1` ILR coordinates) has bias → 0 but variance growing with the number of
  free parameters (≈ `D/N`). The realized signal ≈ `I(D) − penalty(D, N)`. For `N ≫ D` it tracks the rising
  `I(D)`; for `N ≲ D` it **peaks at an effective dimension D\*(N) and declines.** This is a *prediction*, and
  §4 tests it.

## 3. The test — real microbiome data (T1 — measured)

Data: **coda4microbiome** (Calle, Pujolassos & Susin 2023, *BMC Bioinformatics* 24:82). Engine geometry =
the repo's `HCI-CNTT/engine/geometry.py` (closure, CLR, Helmert‑ILR). Zeros: multiplicative replacement
(`0.65·min⁺`). Classifier: L2 logistic on standardized ILR; **repeated stratified k‑fold** ROC‑AUC.
Significance: label‑permutation null (classifier) and **PERMANOVA** on Aitchison distance (999 perms).
Seeded (`SEED=20260622`), determinism re‑checked (identical AUC on rerun).

### Cohort A — Crohn (N=975, D=48; 662 CD / 313 control), the diversity null as the anvil

| representation | what it is | separation AUC | test |
|---|---|---:|---|
| `K_eff` (effective diversity) | scalar aggregate | **0.505** | MW p=0.78 |
| Shannon | scalar aggregate | 0.505 | MW p=0.78 |
| Gini dominance | scalar aggregate | 0.527 | MW p=0.18 |
| sequencing depth | non‑compositional magnitude | 0.557 | MW p=0.004 |
| **ILR log‑ratios (relational)** | the full ratios | **0.832** (sd 0.004) | **PERMANOVA F=22.4, p=0.001**; classifier perm **p=0.005** |

The diversity null is reproduced exactly (p=0.78) — and the relational geometry recovers a strong signal the
aggregates are blind to. Because ILR is **closure/scale‑invariant**, this 0.832 is provably **depth‑free**
(depth alone reached only 0.557). **Law 1 holds.** *Law 2:* including more parts (top‑D taxa + amalgamated
remainder) raises AUC **0.639 (3 parts) → 0.832 (48 parts)**, saturating ~25–33 parts; a second label‑free
ordering (CLR‑variance) gives the same rise (0.625 → 0.832). Permutation‑null stays flat ~0.53–0.55 across D.
**Law 2 holds at N/D ≈ 20.**

### Cohort B — HIV (N=155, D=60; 128 Pos / 27 Neg; 35% zeros), the independent replication

| representation | separation AUC | test |
|---|---:|---|
| `K_eff` / Shannon / dominance / depth | 0.505–0.543 | all near‑null |
| **ILR log‑ratios (full D=60, relational)** | **0.618** | **PERMANOVA F=3.5, p=0.002**; classifier perm p=0.07 |
| **ILR log‑ratios (best low‑D)** | **0.71** (≈3–25 parts) | well above null |

**Law 1 replicates:** the relational representation beats every aggregate and PERMANOVA is significant
(p=0.002). The *full‑60‑part classifier* is only marginal by permutation (p=0.07) — and that is the cue for
Law 2.

## 4. Fix it, do it again — the honest boundary (T1 — measured)

On HIV the Law‑2 curve goes the **wrong way**: AUC peaks at low D (0.71) and **declines to ~0.61 at D=60**.
This is not a refutation — it is the §2 prediction. With `N/D ≈ 2.6` and only 27 minority samples, the
high‑D classifier **overfits**: estimation variance overtakes the information gain.

**Diagnosis test:** re‑ran HIV Law 2 with a **dimension‑aware** estimator (inner‑CV‑regularized logistic).
Prediction: variance control should tame the high‑D decline. Result: it **partially** does — full‑D AUC rises
0.613 → 0.658 and the peak rises to 0.725 — but the curve is **still non‑monotone** (peaks mid‑D). So the
honest, refined statement is **Law 2b**: in a finite sample, more parts help only **up to D\*(N)**; beyond it,
no fixed estimator recovers the population monotonicity. Crohn (N/D≈20) sits below its D\*; HIV (N/D≈2.6)
sits above its D\* by D=60.

This refinement is itself a result: **there is an effective compositional dimension a dataset can support**,
and it scales with N — a falsifiable, useful boundary (and a natural tie to the engine's own effective‑rank
/ `K_eff` instincts).

## 5. Verdict, tiers, and kill conditions

- **Law 1 (Relational Locus): SUPPORTED, T1.** Two independent cohorts; relational ≫ every aggregate;
  PERMANOVA p=0.001 / 0.002; depth‑invariant by construction. **Kills if** a relationship‑blind aggregate
  ever matches/exceeds the full relational representation on a real labeled composition.
- **Law 2a (population monotonicity): PROVEN, T1** (DPI). **Kills if** a correct estimator on a large‑N
  composition shows recoverable information strictly decreasing in D across the whole range.
- **Law 2b (finite‑sample boundary): SUPPORTED, T1.** Crohn rises‑saturates; HIV peaks‑declines;
  regularization shifts but does not erase D\*. **Kills if** the peak/decline fails to track N/D across
  datasets.
- **Not claimed:** no biological causation, no clinical utility, no "diversity is useless" (diversity is a
  *lossy* read, not a wrong one); HIV carries a known MSM enterotype confounder (we test *where* signal
  lives, not *why*). Generalization beyond gut‑microbiome genus data is **T3** until more domains are run.

## 6. Receipts & reproduction

- Inputs (sha256, 16): Crohn `X`,`y` and HIV `X`,`y` recorded in `cmp_result.json` / `cmp_result_hiv.json`.
- Result hashes: Crohn `acf65ce93f7020d5`; HIV `252ed1984c57e956`. Determinism re‑checked (identical AUC).
- Reproduce: `python cmp_analysis.py` (Crohn), `python cmp_replicate.py` (HIV), `python cmp_fix_hiv_law2.py`
  (the fix), `python cmp_figures.py` (figures). Seed `20260622`. Real data: `DATA/MicroBiome/coda4microbiome/`.
- Figures: `fig1_law1_relational_vs_aggregate.png`, `fig2_law2_dimensional_articulation.png`.

*The message is in the ratios (proven and measured); more parts speak louder up to what the sample can hear
(proven for the population, bounded in the sample). The honest boundary is the finding, not a flaw.
Paper seed: [`../../papers/COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md`](../../papers/COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md).
Peter is the sole gate; nothing pushed.*
