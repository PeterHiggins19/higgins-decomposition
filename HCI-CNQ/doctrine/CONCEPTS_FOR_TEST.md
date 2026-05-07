# QD — Concepts For Test and Trial

**Status:** experimental. See [`README.json`](README.json).
**Companion:** [`QD_DEEPER_CONNECTIONS.md`](QD_DEEPER_CONNECTIONS.md) holds the math chain for each concept; this file is the operational catalogue with explicit per-concept test definitions.

---

## How to read this catalogue

Each concept gets:

- **What** — one-paragraph statement of the concept.
- **Claim strength** — ISOMORPHISM (provable), EQUIVALENCE (provable under explicit transform), ANALOGY (strong structural similarity, needs corpus evidence), or CONJECTURE (suspected, needs corpus evidence to validate or falsify).
- **Test** — what input data, what computation, what gate criterion.
- **Status** — NOT YET RUN until evidence exists.

---

## Concept 1 — Aitchison D=4 ↔ unit quaternions (foundation)

**What.** For datasets with D=4 carriers, the Aitchison-rotation group SO(D−1) = SO(3) is exactly the same group whose universal cover is the unit quaternions S³. Therefore, the orientation of any 4-carrier compositional vector is parameterised by a unit quaternion.

**Claim strength.** ISOMORPHISM.

**Test.** Run on `backblaze_fleet` (the only D=4 corpus experiment).
- Read the input CSV; CLR-project each row.
- Pick a fixed Helmert basis to map CLR to ℝ³.
- Map each ℝ³ point to a unit quaternion via the standard ℝ³ → S³ embedding (axis-angle with angle from the radial coordinate).
- Project back through the inverse Helmert basis to CLR.
- Diff reconstructed CLR vectors against original CLR vectors.

**Gate.** Maximum component-wise diff ≤ 1e-12.

**Status.** NOT YET RUN.

---

## Concept 2 — atan2 bearing ↔ quaternion log map (rank-1 case)

**What.** CNT's per-timestep bearing computation `θ = atan2(y, x)` is the rank-1 instance of the quaternion logarithm `log(q) = (atan2(|v|, a) / |v|) · v`.

**Claim strength.** EQUIVALENCE.

**Test.** For any D=4 corpus experiment:
- Reconstruct each timestep's quaternion from the CLR triple (per Concept 1).
- Compute the quaternion log of each unit quaternion.
- Extract the angle component.
- Compare to CNT's `bearing` channel value at that timestep.

**Gate.** Diff ≤ 1e-15.

**Status.** NOT YET RUN.

---

## Concept 3 — M² = I ↔ quaternion conjugation = time reversal

**What.** CNT's metric tensor M satisfies M² = I (Banach contraction certificate). Quaternion conjugation q → q* is also an involution. Under the candidate identification (CNT trajectory state ↔ unit quaternion), M acts as quaternion conjugation, which physically means **time-reversal symmetry**.

**Claim strength.** EQUIVALENCE.

**Test.** Pick three corpus experiments with different IR classes — `geochem_tappe_kim1` (CRITICALLY_DAMPED), `ember_deu` (OVERDAMPED_EXTREME), `ember_combined_panel` (MODERATELY_DAMPED).
- Reverse the CSV row order.
- Run the canonical CNT engine on the reversed CSV.
- Extract the new M tensor.
- Predict M_reversed from M_original via the candidate quaternion-conjugation transform.
- Diff predicted vs actual.

**Gate.** Diff ≤ 1e-12 component-wise. M_reversed should equal M_original* (the quaternion conjugate, applied component-wise under the identification).

**Status.** NOT YET RUN.

---

## Concept 4 — LIMIT_CYCLE_P2 ↔ spinor sector

**What.** The period-2 attractor termination code in CNT corresponds to trajectories that lift to the SU(2) double cover but not to SO(3) directly — i.e., the spinor sector. LIMIT_CYCLE_P1 (one-step return) corresponds to the vector sector.

**Claim strength.** CONJECTURE.

**Test.** Two-part test (the corpus alone is insufficient; we need synthetic data).

*Part A (corpus-only):* tabulate `curvature_termination` across the 25 experiments. Identify the pattern between IR class and termination code. The conjecture predicts that LIMIT_CYCLE_P2 datasets cluster in IR classes that correspond to spinor-like dynamics (handedness-significant trajectories).

*Part B (synthetic):* generate two synthetic D=4 trajectories, one designed to have spinor parity (cumulative σ-integral = odd × 2π) and one with vector parity (even × 2π). Run CNT on both. The conjecture predicts P2 for the spinor case and P1 for the vector case.

**Gate.** Part A: descriptive only — look for a clean pattern. Part B: predicted termination code must match observed for both synthetics.

**Status.** NOT YET RUN.

---

## Concept 5 — CBS cube ↔ Cayley diagram of Q₈

**What.** The three orthogonal faces of CNT's CBS cube — span(ω, κ), span(κ, σ), span(ω, σ) — are exactly the three coordinate planes of the Cayley diagram of the quaternion group Q₈ = {±1, ±i, ±j, ±k}, with the Higgins time axis as the scalar axis.

**Claim strength.** ANALOGY (verifiable to EQUIVALENCE).

**Test.** Quaternion multiplication imposes specific algebraic relations: i·j = k, j·k = i, k·i = j (with sign reversal for swapped order). Under the candidate identification (ω ↔ i, κ ↔ j, σ ↔ k), CNT's channels should obey these products at every timestep.
- For three corpus experiments at varying D, compute the product table ω·κ, κ·σ, σ·ω at every timestep.
- Compare to the predicted channel values for the third channel.

**Gate.** Pearson correlation ≥ 0.9 between predicted and observed. Lower would mean the identification is wrong; near-1 would upgrade this from ANALOGY to EQUIVALENCE.

**Status.** NOT YET RUN.

---

## Concept 6 — 8-class IR taxonomy ↔ S³ sign octants

**What.** CNT's 8 IR classes correspond to the 8 sign-octants of S³ (the 8 elements of the quaternion group Q₈), with the IR boundary thresholds determined by the sign-flip boundaries of the trajectory's average quaternion.

**Claim strength.** CONJECTURE.

**Test.** For each of the 25 corpus experiments:
- Reconstruct the trajectory as a quaternion path (where dimensionally possible — D=4 cleanly, D=3 partially, D≥5 via dimensional reduction).
- Compute the time-averaged quaternion.
- Determine the sign-octant of the average (signs of the four components).
- Tabulate IR class vs sign-octant.

**Gate.** Either (a) every IR class corresponds to exactly one sign-octant (clean isomorphism), or (b) the assignment is many-to-one but well-defined (still a discovery), or (c) no clean pattern (claim falsified).

**Status.** NOT YET RUN.

---

## Concept 7 — Stage 4 cross-dataset ↔ Hamilton product Q₁ · Q₂⁻¹

**What.** CNT's Stage 4 cross-dataset comparison is the channel-decomposed form of the relative-rotation Hamilton product R(t) = Q₁(t) · Q₂(t)⁻¹.

**Claim strength.** EQUIVALENCE.

**Test.** The CodaWork demo's `spectrum_paper_codawork2026_ember.pdf` contains Stage 4 cross-dataset values for the 8 EMBER countries + World aggregate.
- Reconstruct each country's trajectory as a quaternion path.
- Compute the pairwise Hamilton products R_AB(t) = Q_A(t) · Q_B(t)⁻¹.
- Decompose R_AB(t) into its angle and axis components.
- Compare to the cross-dataset values in the spectrum paper.

**Gate.** Component-wise agreement ≤ 1e-12.

**Status.** NOT YET RUN.

---

## Concept 8 — Helmsman σ ↔ spinor parity tracker

**What.** CNT's σ channel (signed angular accumulation) is the spinor-parity tracker: the cumulative integral of σ over the full trajectory determines whether the trajectory lifts to the spinor branch (odd × 2π) or the vector branch (even × 2π) of the SU(2) → SO(3) cover.

**Claim strength.** ANALOGY.

**Test.** For each of the 25 corpus experiments:
- Compute ∫σ dt over the full trajectory.
- Check whether (∫σ / 2π) is closer to an even integer or an odd integer.
- Tabulate against `curvature_termination` (LIMIT_CYCLE_P1 vs LIMIT_CYCLE_P2).

**Gate.** All LIMIT_CYCLE_P2 experiments should have ∫σ ≈ odd × 2π; all LIMIT_CYCLE_P1 should have ∫σ ≈ even × 2π. Agreement on at least 80% of the relevant experiments would support the claim.

**Status.** NOT YET RUN.

---

## Concept 9 — Depth tower ↔ S³ random walk recurrence time

**What.** CNT's depth tower depth (number of recursion steps before terminator hits) is correlated with — possibly equal to up to a constant — the canonical recurrence time of the trajectory's quaternion dynamics on S³.

**Claim strength.** ANALOGY.

**Test.** For each corpus experiment:
- Compute the quaternion-coordinate dynamics' recurrence time analytically (the smallest k such that Qᵏ ≈ 1 to a fixed tolerance).
- Compare to `summary.curvature_depth` from the JSON.

**Gate.** Pearson correlation ≥ 0.7 across the 25 experiments. Higher than 0.9 would suggest direct equality up to a constant.

**Status.** NOT YET RUN.

---

## Concept 10 — directness=1 / directness=0 ↔ pure scalar / pure vector velocity

**What.** The Stage 2 calibration directness parameter is the relative weight of scalar-part vs vector-part of the trajectory's instantaneous quaternion velocity. directness=1 → pure scalar; directness=0 → pure vector.

**Claim strength.** ISOMORPHISM (after explicit construction).

**Test.** The calibration fixtures `STANDARD_CALIBRATION_stage2_*` contain reference trajectories at directness=1 and directness=0.
- Read each fixture; reconstruct as quaternion path.
- Compute instantaneous quaternion velocity q̇(t) = dq/dt at each timestep.
- Decompose q̇(t) into scalar and vector parts.
- For directness=1: vector part should be identically zero.
- For directness=0: scalar part should be identically zero.

**Gate.** Both conditions must hold to ≤ 1e-15 (IEEE floor, since the fixtures are documented to that precision).

**Status.** NOT YET RUN.

---

## Test priority order (Round-2 sequencing)

When QD reaches Round 2 (first corpus test), run in this order to maximize information yield per unit work:

1. **Concept 1** (foundation) — if this fails, everything else is moot.
2. **Concept 10** (calibration check) — fastest to run, gives a second independent confirmation of Concept 1.
3. **Concept 2** (atan2 ↔ quaternion log) — same data as Concept 1, same scaffolding.
4. **Concept 7** (Stage 4 ↔ Hamilton product) — uses the EMBER 8-country corpus already in the demo folder.
5. **Concept 3** (time reversal) — three CSV-flips and three engine reruns, no math.
6. **Concept 5** (CBS cube ↔ Q₈) — channel-product tables, post-hoc on existing JSONs.
7. **Concept 6, 8, 9** (IR taxonomy, helmsman, depth tower) — these need the average-quaternion / σ-integral / recurrence-time computations that build on Concept 1.
8. **Concept 4** (spinor sector) — needs synthetic data, last.

---

## What "promotes" QD to candidate status

Per [`HCI-CNQ_ADMIN.json`](../HCI-CNQ_ADMIN.json) `status_promotion_path`:

- **Concept 1 PASS** = QD becomes a real coordinate system, not a metaphor.
- **Concept 1 + 10 PASS** = the identification has two independent confirmations and warrants Round 3.
- **Concepts 1, 2, 3, 7, 10 all PASS** = the algebraic equivalence is established. QD becomes a candidate Volume IV of the handbook.
- **Plus Concept 4 or 6 PASS** = QD has discovered something CNT cannot say in its current vocabulary. QD is then proposed for integration.

Until Concept 1 runs, QD remains experimental. Round 2 work is gated on Peter's go-ahead.

---

*Exploration. Documents only. Not for repo use until status promotion.*
