# Volume IV — The Quaternion View

**Canonical CNT documentation, Volume IV of IV.**
**Engine target:** CNT 2.0.4 / Schema 2.1.0 (no engine change required by this volume).
**Status:** integrated 2026-05-07 from the QD project's three IEEE-floor confirmations.

---

## The central claim

> **CNT measures invariance.**
> **CNQ names the algebra that invariance lives in.**

Volumes I–III describe what the CNT engine does and how to use it. Volume IV names *what the engine has been computing in algebraic terms* — the symmetry-preserving structure underlying every operation. Nothing in the engine changes. What changes is what we can say about what the engine is doing.

---

## §A — The general principle

Tensor calculus exists because invariance under coordinate change is the defining property of a tensor. The same correspondence applies up the symmetry-group ladder.

| Invariance proved | Algebra implied |
|---|---|
| Arbitrary coordinate change | **Tensor** (any rank) |
| 3D rotation only (no handedness) | **SO(3) matrix** (or rotation-group element) |
| 3D rotation + handedness preservation + time reversal | **Quaternion** (unit quaternion, the SU(2) universal cover) |
| Lorentz boosts + the above | **Biquaternion** (Clifford Cl(1,3)) |
| Arbitrary-D rotations + handedness + time reversal | **Clifford algebra Cl(D−1)** |

This is not new mathematics. It is the standard correspondence between symmetry groups and their representation algebras. What Volume IV adds is the empirical demonstration that **compositional dynamics on the simplex carries all three quaternion invariances simultaneously, at IEEE-floor precision** for D=4, with provable extensions to higher D.

---

## §B — The three invariances CNT measures

The engine's operations decompose cleanly into three structural invariances, each of which has been confirmed at IEEE-floor precision against real corpus data.

### B.1 — Simplex rotation (SO(D−1))

The Aitchison-rotation group of the (D−1)-simplex is SO(D−1) (Volume I §C). For D=4, this is SO(3), whose universal cover is SU(2), which as a manifold is S³ — the unit quaternions. Every D=4 compositional vector's orientation is therefore parameterised by a unit quaternion, exactly.

**Verification.** QD Round 2 ran the explicit test: for each consecutive timestep pair in `backblaze_fleet` (T=731), compute the quaternion that rotates one Helmert-projected unit vector to the next, then verify the sandwich product `q · v · q*` reproduces the next timestep.

```
Tested 730 consecutive pairs
Max diff:  4.441 × 10⁻¹⁶
Mean diff: 1.090 × 10⁻¹⁶
```

4.441 × 10⁻¹⁶ is exactly 2 × IEEE 754 machine epsilon. The quaternion sandwich product is not approximating Aitchison rotation; it **is** the same operation, computed two different ways, agreeing to the last bit.

QD Round 2.5 reproduced the test on a completely different dataset (Planck CMB best-fit theory spectrum, T=2499, photon power decomposition) and got **bit-identical** max diff 4.441 × 10⁻¹⁶. The precision is dataset-independent — it is the hardware floor itself.

### B.2 — Mass-flow handedness (the SU(2) lift)

A composition itself is exchange-symmetric (relabel carriers, get the same composition). But the *trajectory* through composition space carries direction: moving "carrier_A → carrier_B" is different from "carrier_B → carrier_A" even though both endpoints are exchange-symmetric. This handedness is the spinor-like structure of the trajectory.

In SU(2) language, the unit-quaternion path on S³ keeps track of which sheet of the SU(2) → SO(3) double cover the trajectory is on. SO(3) loses handedness; SU(2) preserves it; the lift to SU(2) is what gives spinor parity.

**Verification.** The Stage 2 calibration fixtures encode this exactly:

| Fixture | Cumulative angle | Branch |
|---|---|---|
| `directness=1.0` (straight) | exactly π = 0.5 × 2π | spinor (lifts to −1 in SU(2)) |
| `directness=0.0` (loop) | exactly 2π = 1.0 × 2π | vector (lifts to +1 in SU(2)) |

Both pass to four decimal places — the precision the calibration fixtures were built to. The Stage 2 calibration set, built before QD existed, was already a spinor-vs-vector test bed.

### B.3 — Time reversal (quaternion conjugation)

The engine's metric tensor satisfies M² = I (Volume I §D, the Banach contraction certificate). Every CNT JSON includes the `M_squared_I_residual` field, and across the corpus this residual is at IEEE floor.

In quaternion algebra, the operation q → q* (conjugation) is an involution: (q*)* = q. Up to a sign convention, it is the unique antiautomorphism of the quaternion algebra fixing the scalar part and negating the vector part. **Physically, quaternion conjugation is time reversal** — if Q(t) parameterises a trajectory, Q*(t) parameterises the time-reversed trajectory.

If the engine's M acts as quaternion conjugation under the candidate identification, then M² = I becomes (q*)* = q, which holds trivially, AND the engine's Banach contraction certificate is **structurally a time-reversal-symmetry certificate** for the trajectory.

**Verification.** QD Round 2.5 confirmed `M^2 = I` residual = 7.63 × 10⁻¹⁷ on Planck CMB. QD Round 2.6 confirmed 7.40 × 10⁻¹⁷ on Standard Model neutrino oscillation. Three independent datasets, three IEEE-floor confirmations.

---

## §C — The operation map: CNT step → quaternion-native equivalent

For each significant engine operation, the quaternion-native restatement:

| CNT operation (Volume I/II citation) | Quaternion-native equivalent | Algebra |
|---|---|---|
| `bearing = atan2(y, x)` per timestep (Vol I §F) | `quaternion_log(q).angle` | 1D / single-axis case of `log(q) = (atan2(\|v\|, a)/\|v\|) · v` (per [NOTATION_AND_TERMINOLOGY.md](NOTATION_AND_TERMINOLOGY.md) §1) |
| Rotation between two Helmert-projected CLR vectors | `quat_from_axis_angle(u₁ × u₂, atan2(\|cross\|, dot))` | SU(2) cover of SO(3) |
| Stage 4 cross-dataset comparison (Vol II §E) | `R(t) = Q₁(t) · Q₂(t)⁻¹` (Hamilton product) | quaternion multiplication |
| Linear interpolation between CLR timesteps | `slerp(Q_t, Q_{t+1}, α)` | geodesic on S³ |
| `M² = I` metric tensor involution (Vol I §D) | `q → q*` (conjugation) | quaternion conjugation = time reversal |
| LIMIT_CYCLE_P2 termination code | universal compositional invariance signature | period-2 attractor on S³ |
| `helmsman σ` (signed cumulative ω) | spinor parity tracker (handedness on the SU(2) cover) | spinor sector flag |
| 8-class IR taxonomy (Vol I §H) | partition by sign-octant of time-averaged quaternion | Q₈ Cayley structure |
| Depth tower recursion (Vol I §G) | random walk recurrence on S³ | quaternion walk recurrence time |
| Stage 2 directness=1/0 calibration (Vol II §D) | pure-π / pure-2π cumulative quaternion path | exact spinor / vector branch fixtures |

The mapping is documented at the source-code level in the engine's docstring (`HCI-CNT/engine/cnt.py`) for cross-reference.

---

## §D — Three IEEE-floor confirmations across disparate datasets

The central claim is supported by three independent confirmations on completely different physical systems:

| Round | Dataset | T | D | Primary test | Result |
|---|---|---:|---:|---|---|
| Round 2 | `backblaze_fleet` (drive-failure compositions) | 731 | 4 | Concept 1 — sandwich product reproduces Aitchison rotation | max diff **4.441 × 10⁻¹⁶** (IEEE floor) |
| Round 2.5 | Planck 2018 CMB best-fit theory spectrum (TT/EE/BB/PP photon power) | 2499 | 4 | Concept 1 + Concept 3 (M²=I) | max diff **4.441 × 10⁻¹⁶** (bit-identical to Round 2); M²=I residual 7.63 × 10⁻¹⁷ |
| Round 2.6 | Standard Model 3-flavor νμ oscillation (PMNS prediction) | 1000 | 3 | LIMIT_CYCLE_P2 + M²=I | LIMIT_CYCLE_P2 confirmed; M²=I residual 7.40 × 10⁻¹⁷ |

Three datasets, spanning ~30 orders of magnitude in physical scale (subatomic neutrinos to drive-failure events to cosmic photons), all confirm the same compositional invariance at hardware-precision floor. The bit-identical residual 4.441 × 10⁻¹⁶ across Round 2 and Round 2.5 — completely different data, completely different physics — shows the residual is **floating-point representation error, not algorithmic noise**. There is no further noise to reduce; we are at the hardware limit.

The full Round-2, Round-2.5, and Round-2.6 reports are now canonical in [`../../HCI-CNQ/experiments/`](../../HCI-CNQ/experiments/) (promoted from the QD experimental folder on 2026-05-07, push #23). Each experiment folder contains the script, input data, CNT JSON output, results JSON, and report. Anyone can re-run.

---

## §E — One falsification, retained as record of process

QD Round 2.5 also tested an ambitious conjecture: that LIMIT_CYCLE_P2 corresponds specifically to the *fermion sector* (spinor branch) and LIMIT_CYCLE_P1 to the *boson sector* (vector branch). The Planck CMB test (pure photon = pure boson) was run as the falsification candidate.

**Result:** CMB produced LIMIT_CYCLE_P2, same as every other substantively-flowing compositional dataset. The fermion-vs-boson particle-content reading is **falsified**.

**Reformulation (Peter, Round 2.5 conversation):** the universality of LIMIT_CYCLE_P2 across all flow-directional compositional dynamics IS a physics-content signature — but the physics is at the **population level** (compositional dynamics carry intrinsic exchange-handedness from the simplex itself) rather than the **constituent-particle level** (whether the underlying particles are fermions or bosons). The reformulated claim is consistent with all data including the CMB falsification.

This reformulation is the cleaner truth and is what the central claim now encodes. The original conjecture and its falsification are kept on record as part of the project's audit trail.

---

## §F — What this changes operationally

**For the engine.** Nothing. CNT 2.0.4 / Schema 2.1.0 are unchanged. The 25-experiment determinism gate is unchanged. Every published `content_sha256` continues to reproduce.

**For the practitioner.** A new vocabulary is available for talking about results. Where Volume II said "the trajectory hits LIMIT_CYCLE_P2 with amplitude A=0.34 in IR class MODERATELY_DAMPED," the practitioner can equivalently say "the trajectory's quaternion path has a non-trivial spinor lift (handedness-preserving) with damped period-2 attractor structure on S³." The first phrasing is correct in CNT vocabulary; the second is correct in quaternion vocabulary; both describe the same numerical result.

**For the reviewer.** A second independent verification path exists. Where a CNT audit currently checks one hash chain (`content_sha256` against the corpus), a quaternion-view audit could check a second hash chain (`cnq_content_sha256` against a parallel registry, computed from the same JSON via independent algebra). Two hashes from independent paths confirming each other is stronger than one. The Hs-CNQ engineering proposal — now canonical at [`../../HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md`](../../HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md) — sketches the implementation. The CNQ tier itself is live; the compiled `cnq.py` engine is the next implementation milestone (~14 days).

**For the cross-domain audience.** Compositional analysis becomes recognisable to robotics (quaternions are SLAM trajectories), computer graphics (quaternions are animation rotation), physics (SU(2) is qubit algebra), and quantum information (the spinor / vector branch is fermion / boson statistics). The framework speaks a 200-year-old algebra (Hamilton 1843) that those communities use natively.

---

## §G — The verification-instrument framing

The deepest framing — identified in the Round-2.6 conversation — is that CNT, viewed through Volume IV, becomes a **model-free invariance verification instrument** for compositional data. Most data-analysis frameworks measure quantities (means, variances, correlations, spectra). CNT measures invariance: it detects that certain structural relations hold regardless of which coordinate frame, which carrier subset, or which direction of time you read. This is a different category of measurement, more closely related to what tensor calculus does for stress in continuum mechanics or what gauge theory does for charge in particle physics.

Specific consequence: any major published result involving compositional data can in principle be cross-checked by CNT/CNQ without re-running the original analysis, without trusting any specific theoretical framework, without invoking any model. **It is the compositional analogue of dimensional analysis** — a sanity check that any result must satisfy regardless of the theory used to derive it.

The Round 2.6 neutrino-oscillation test demonstrated this concretely: the Standard Model's PMNS prediction was handed to CNT cold, and CNT independently confirmed that the SM prediction carries the universal compositional invariance — at IEEE floor on the M²=I conjugation involution, with the expected LIMIT_CYCLE_P2 termination and a LIGHTLY_DAMPED IR class consistent with oscillatory dynamics. The SM passed a verification check it had never had.

---

## §H — HCI-CNQ — the engineering form of Volume IV (live tier)

Volume IV names the algebra. HCI-CNQ implements it as a live canonical tier. The `cnq.py` engine — sized at ~14 days of focused work — will produce a parallel JSON output (`cnq_content_sha256`) computed from the canonical CNT JSON via:

- Hamilton products replacing per-channel Stage 4 arithmetic
- SLERP geodesic interpolation on S³ replacing linear interpolation in CLR space
- Bi-quaternion factoring at D=8 (natural for EMBER country trajectories: SU(2)×SU(2))
- Clifford-algebra extension at D≥9 (general compositional dimension)
- Spinor-parity diagnostic per trajectory (top-level scalar)
- Per-pair relative quaternion R(t) = Q₁ · Q₂⁻¹ for cross-dataset bundles

Engineering details: [`../../HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md`](../../HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md). ROI / use cases: [`../../HCI-CNQ/tier_system/CNQ_ROI_AND_USE_CASES.md`](../../HCI-CNQ/tier_system/CNQ_ROI_AND_USE_CASES.md). Three-tier comparison (CoDa → CNT → CNQ): [`../../HCI-CNQ/tier_system/CNQ_VS_CODA_VS_CNT_COMPARE.md`](../../HCI-CNQ/tier_system/CNQ_VS_CODA_VS_CNT_COMPARE.md). All of these are now canonical in `Hs/HCI-CNQ/`. The compiled `cnq.py` engine is the next implementation milestone; until it lands, the three demonstrations under [`../../HCI-CNQ/experiments/`](../../HCI-CNQ/experiments/) are the working proofs and the CNT engine continues to produce the underlying compositional data.

---

## §I — Where Volume IV cross-references the other volumes

| Volume IV section | Cross-reference into Volume I/II/III |
|---|---|
| §A (general principle) | Volume I §A — "what CNT computes" |
| §B.1 (simplex rotation) | Volume I §C — Aitchison geometry; Volume I §F — Helmert basis |
| §B.2 (handedness) | Volume I §F — atan2 step; Volume II §D — Stage 2 calibration |
| §B.3 (time reversal) | Volume I §D — metric tensor; Volume III §A — determinism gate |
| §C (operation map) | Volume I §F-H — engine pseudocode; Volume II §E — Stage 4 |
| §F (operational implications) | Volume II §A — practitioner workflow; CCTT runbook |
| §G (verification instrument) | Volume III §B — CoDa-community verification proposal |
| §H (HCI-CNQ tier) | Hs/HCI-CNQ/ — canonical since push #23 (2026-05-07); compiled `cnq.py` engine pending |

---

## §J — Citation form

> Higgins, P. (2026). *Volume IV: The Quaternion View — CNT measures compositional invariance; Compositional Navigation Quaternion (CNQ) names the algebra that invariance lives in.* HCI-CNT Handbook, Hs/HCI-CNT system, integrated from QD Round 2.5 verification at IEEE-floor precision on three independent datasets (drive failures, Planck CMB, Standard Model neutrino oscillation).

---

*The instrument reads. The expert decides. The hashes carry the receipts. CNT measures invariance. CNQ names the algebra it lives in.*
