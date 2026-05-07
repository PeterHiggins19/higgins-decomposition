# QD — The Central Claim

**Status:** central — every other document in this project elaborates this one statement.
**Origin:** identified by Peter on 2026-05-07, in the Round 2.5 conversation, after the boson-falsification result. The statement crystallises what QD has been demonstrating from Round 2 forward.

---

## In two sentences

> **CNT measures invariance.**
> **CNQ names the algebra that invariance lives in.**

---

## In one paragraph

The Higgins Decomposition system, in its CNT form, is an instrument for measuring invariance in compositional dynamics. CNT detects that compositional time-series carry three specific structural invariances — invariance under simplex rotation (SO(D−1)), preservation of mass-flow handedness, and time-reversal symmetry — and these three invariances appear universally across all substantively-flowing compositional data, regardless of underlying physics. The CNQ tier names the algebra in which those three invariances are unified: for D=4, that algebra is the unit quaternions (the universal cover SU(2) of SO(3) carrying handedness and supporting conjugation as time reversal); for D=8, it is the biquaternions (SU(2)×SU(2)); for arbitrary D, it is the Clifford algebra Cl(D−1). CNT is the measurement; CNQ is the naming.

---

## The general principle

Tensor calculus exists because invariance under coordinate change is the defining property of a tensor. Proving a quantity is invariant under a specific symmetry group is equivalent to proving it has a specific algebraic type. The mapping is:

| Invariance proved | Algebra implied |
|---|---|
| Under arbitrary coordinate change | **Tensor** (any rank) |
| Under 3D rotation only (no handedness) | **SO(3) matrix** (or rotation-group element) |
| Under 3D rotation + handedness preservation + time reversal | **Quaternion** (unit quaternion, the SU(2) universal cover) |
| Under Lorentz boosts + the above | **Biquaternion** (Clifford Cl(1,3)) |
| Under arbitrary-D rotations + handedness + time reversal | **Clifford algebra Cl(D−1)** |

This is not new mathematics. It is the standard correspondence between symmetry groups and their representation algebras. What QD adds is the empirical demonstration that **compositional dynamics on the simplex is exactly the case where all three quaternion invariances apply at once**, for D=4, with provable extensions to higher D.

---

## What the data has shown so far

Three independent IEEE-floor confirmations on disparate datasets:

| Round | Test | Dataset | Precision | Status |
|---|---|---|---|---|
| 2 | Concept 1 — quaternion sandwich product reproduces D=4 Aitchison rotation | `backblaze_fleet` (drive failures, T=731) | max diff 4.441 × 10⁻¹⁶ | **PASS** at IEEE floor |
| 2.5 | Concept 1 — same test, different dataset | Planck CMB theory spectrum (T=2499) | max diff 4.441 × 10⁻¹⁶ | **PASS** bit-identical to Round 2 |
| 2.5 | Concept 3 — M² = I (quaternion conjugation = time reversal) | Planck CMB | residual 7.63 × 10⁻¹⁷ | **PASS** at IEEE floor |

The 4.441 × 10⁻¹⁶ figure is exactly 2 × IEEE 754 machine epsilon for double-precision floats — the smallest difference numerically representable on standard hardware. The bit-identity across two completely different datasets shows the quaternion identification is **mathematically exact**, not approximate; the residual is hardware floating-point representation error, dataset-independent.

A fourth confirmation came as a falsification-that-clarified: the Concept 4 hypothesis (LIMIT_CYCLE_P2 = fermion sector / LIMIT_CYCLE_P1 = boson sector) was tested against pure-boson CMB data and falsified — CMB produced LIMIT_CYCLE_P2, same as every other substantively-dynamic compositional dataset in the corpus. The reformulation under Peter's reframing is sharper: **LIMIT_CYCLE_P2 is the universal experimental signature of compositional dynamics carrying all three quaternion invariances**. The "physics content" being detected is not particle-level fermion/boson distinction but the population-level invariance structure that every flow-directional compositional trajectory inherits from the simplex itself.

---

## Why this matters

Most data-analysis frameworks measure quantities — means, variances, correlations, spectra. CNT measures *invariance*: it detects that certain structural relations hold regardless of which coordinate frame you use, which subset of carriers you label as primary, or which direction of time you read the trajectory in. This is a different category of measurement, more closely related to what tensor calculus does for stress in continuum mechanics or what gauge theory does for charge in particle physics.

CNQ names what category of algebra the measured invariance lives in. The naming matters because:

- It connects compositional analysis to two centuries of established mathematical machinery (Hamilton 1843 → modern Clifford-algebra geometric algebra).
- It makes the framework immediately recognisable to adjacent fields (robotics, computer graphics, physics, quantum information) where quaternion algebra is daily working language.
- It enables operations that are awkward in CNT's channel-by-channel form to become single algebraic expressions (Hamilton products, SLERP, parity extraction).
- It positions the system to scale to dimensionally larger problems (climate, multi-decade economics, microbiome cohorts) where channel-by-channel arithmetic exhausts the practitioner's working memory but quaternion / Clifford arithmetic does not.

---

## Where QD sits relative to the canonical CNT system

Nothing about CNT changes. CNT 2.0.4 stays canon; the 25-experiment corpus stays the determinism gate; every existing CNT result remains valid. QD adds a *naming layer* on top. CNT continues to measure; CNQ adds the algebraic interpretation of what is measured.

This is the same relationship classical mechanics has to Hamiltonian mechanics — both compute the same trajectories; one expresses them in coordinate-by-coordinate forces, the other in coordinate-free phase-space flow. Hamilton's reformulation didn't change a single measurement; it changed what could be said about measurements, and what mathematics could be brought to bear.

QD does the same for CNT.

---

## Status

This statement is the central claim of the Quaternion Decomposition project as of Round 2.5 (2026-05-07). The supporting documents elaborate it:

- [`QD_DEEPER_CONNECTIONS.md`](QD_DEEPER_CONNECTIONS.md) — the 10 specific correspondences between CNT operations and quaternion algebra, with claim-strength labels.
- [`QD_CONCEPTS_FOR_TEST.md`](QD_CONCEPTS_FOR_TEST.md) — the operational test catalogue.
- [`QD_CORPUS_COMPARISON_PLAN.md`](QD_CORPUS_COMPARISON_PLAN.md) — how the existing CNT corpus is used as the standard to surpass and include.
- [`QD_BENEFITS_POST_CODA.md`](QD_BENEFITS_POST_CODA.md) — what becomes possible after CodaWork if this central claim is integrated into the canonical handbook.
- [`QD_ROUND_2_REPORT.md`](QD_ROUND_2_REPORT.md) — the first IEEE-floor confirmation.
- [`../experiments/planck_cmb_quaternion/QD_ROUND_2_5_REPORT.md`](../experiments/planck_cmb_quaternion/QD_ROUND_2_5_REPORT.md) — the second IEEE-floor confirmation plus the falsification-that-clarified.
- [`../tier_system/`](../tier_system/) — the proposed engineering tier, the operational form of the central claim.

Until Peter promotes QD beyond `0.1.0-candidate`, this statement lives only in this folder. After promotion, it becomes the opening sentence of Volume IV of the canonical CNT handbook.

---

## Citation form

If this becomes a published claim:

> Higgins, P. (2026). *The Higgins Decomposition measures compositional invariance; the Compositional Navigation Quaternion names the algebra it lives in.* Quaternion Decomposition project, Hs / HCI-CNT system, Round 2.5 verification at IEEE-floor precision on drive-failure (`backblaze_fleet`) and cosmic microwave background (Planck 2018 best-fit theory spectrum) data.

---

*The instrument reads. The expert decides. The hashes carry the receipts. Today they carry the central claim too.*
