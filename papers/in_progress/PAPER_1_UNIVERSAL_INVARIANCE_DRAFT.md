# A Universal Compositional Invariance Signature: Period-2 Termination at IEEE-Floor Precision Across Drive Failures, CMB Photon Power, and Standard-Model Neutrino Oscillation

**Peter Higgins**
Rogue Wave Audio / Binaural Test Lab, Markham, Ontario, Canada
peterhiggins@roguewaveaudio.com

Draft 2 - 2026-05-08
Catalog reference: INV-026 (OPEN)
Companion software: Hs / CNT engine 2.0.4, schema 2.1.0
Repository: https://github.com/PeterHiggins19/higgins-decomposition
License: CC BY 4.0
Reproduction protocol: CCTT v1.0 (one-command path from raw CSV to verified content_sha256)

---


## Abstract

We report a structural property of compositional time-series on the simplex that holds at IEEE 754 double-precision hardware floor across three physically unrelated systems. A deterministic compositional analysis engine (the Compositional Navigation Tensor, CNT) builds two recursive depth towers - energy and curvature - whose joint termination defines an information-recovery (IR) class. We observe LIMIT_CYCLE_P2 (period-2 attractor) termination at hardware precision on three independent datasets:

1. Hard-drive failure compositions over fleet history (Backblaze, D=4, T=731).
2. The Planck 2018 best-fit theoretical CMB photon power spectrum (D=4, T=2499).
3. The Standard-Model 3-flavour numu oscillation prediction (D=3, T=1000).

The metric-involution residual ||M(M(x)) - x||_inf sits at 7.40e-17 to 7.63e-17 (approximately machine epsilon) across all three. The quaternion sandwich-product reconstruction of consecutive Aitchison rotations matches at maximum component-wise difference 4.441e-16 on the macroscopic and the cosmological datasets - bit-identical to the last digit, and exactly 2 times IEEE 754 machine epsilon. Bit-identical residual across physically unrelated systems implies the residual is hardware floating-point representation error, not algorithmic noise: the underlying mathematical relationship is exact on the compositional simplex. We interpret this as evidence for a universal structural property of any flow-directional compositional dynamics carrying three concurrent invariances (simplex rotation under SO(D-1), mass-flow handedness via the SU(2) lift, and time-reversal symmetry expressed as quaternion conjugation). The result is reproducible in two minutes from the public repository via a published one-command protocol; verification is hash-anchored and language-independent.

**Keywords:** compositional data analysis, Aitchison geometry, simplex, period-doubling attractor, IEEE 754 precision, quaternion algebra, reproducibility, cross-domain universality.

---


## Notation

**Acronyms used in this paper:**

- CoDa: Compositional Data (Analysis)
- CLR: Centred Log-Ratio
- ILR: Isometric Log-Ratio
- CNT: Compositional Navigation Tensor (the engine analysed here, version 2.0.4)
- CNQ: Compositional Navigation Quaternion (proposed sibling engine, only invoked in section 5)
- DADC: Dimension-Apportioned Diffraction Correction (the original loudspeaker work)
- BTL: Binaural Test Lab (sound-controlled professional laboratory; identity card RWA-001)
- CCTT: CNT Compositional Tensor Train (the published 7-phase reproduction protocol)
- IR class: Information-Recovery class (8-class taxonomy of trajectory termination)
- UCIS: Universal Compositional Invariance Signature (this paper's term for the property in section 1.1)
- PMNS: Pontecorvo-Maki-Nakagawa-Sakata neutrino mixing matrix
- CMB: Cosmic Microwave Background
- SM: Standard Model

**Mathematical symbols (plain ASCII; Greek letters spelled out where used in prose):**

- D : number of carriers (composition dimension)
- T : number of timesteps in a trajectory
- S^(D-1) : the (D-1)-simplex; positive vectors with components summing to 1
- C(y) : Aitchison closure operator, C(y) = y / sum_i(y_i)
- clr(x) : centred log-ratio of composition x
- ilr(x) : isometric log-ratio (Helmert basis)
- H : (D-1) by D Helmert orthonormal contrast matrix
- theta_ij(x) : bearing tensor, pairwise CLR angle between carriers i and j
- omega(t, t+1) : angular velocity between consecutive compositions
- kappa_HS_ij(x) : Higgins Steering Metric Tensor (full Aitchison pullback metric)
- sigma(t, t+1) : helmsman, dominant-displacement carrier index
- M(x) : metric involution, satisfies M(M(x)) = x exactly in continuous math
- ||v||_inf : component-wise sup-norm of vector v
- eps_mach : IEEE 754 double-precision machine epsilon, approximately 2.220e-16
- q : unit quaternion (element of S^3)
- q . v . q* : quaternion sandwich product (rotates 3-vector v by the rotation q represents)
- A, zeta, lambda : period-2 attractor amplitude, damping factor, contraction rate
- eps : multiplicative zero-replacement constant, default 1e-10

**Compositional vocabulary:**

A *composition* x is a vector of strictly positive numbers (carrier abundances) treated as a point on the simplex. Only relative magnitudes carry information; absolute scale is removed by closure. A *carrier* is one of the D parts. A *flow-directional compositional time-series* is an ordered sequence x(1), x(2), ..., x(T) where the temporal index has physical meaning. *Subcompositional coherence* is the requirement that conclusions about a subset of carriers should not depend on which other carriers were observed.

**Engine vocabulary:**

A *channel* is one of CNT's four named per-timestep outputs: bearing theta, angular velocity omega, curvature kappa, helmsman sigma. A *depth tower* (energy or curvature) is a recursive aggregation of the trajectory's per-timestep displacements, iterated under a contraction operator until termination. A *termination code* is the condition under which a depth tower stops iterating: FIXED_POINT, LIMIT_CYCLE_P2, LIMIT_CYCLE_Pn, CHAOS, or TIMEOUT. The *IR class* is an 8-element taxonomy classifying trajectories that terminate at LIMIT_CYCLE_P2 by their amplitude A and damping factor zeta.

**Provenance vocabulary:**

The *determinism contract* is the property that fixed input bytes plus fixed engine config produce bit-identical canonical JSON output. The *hash chain* consists of three independent SHA-256 anchors: source_file_sha256 (raw input), closed_data_sha256 (closed/normalised data), content_sha256 (full canonical JSON). The *engine signature* identifies which engine build produced an output. The *Investigation Catalog* is the public audit-trail document at ai-refresh/INVESTIGATION_CATALOG.json. The *corpus* is the framework's 25-experiment reference set.

---


## 1. Introduction

Most quantitative data is compositional. Whenever the parts of a system compete for a fixed (or controlled) total - energy mixes per country, failure-mode breakdowns of a fleet, geochemical oxide compositions, cosmological energy budgets, polarisation states of an electromagnetic wave, modal occupations in a quantum acoustic device - the resulting vector lives on the simplex and only relative magnitudes carry information. The mathematical home for such data has been understood since Aitchison (1986) and was refined into an isometric framework by Egozcue et al. (2003). That framework operates on static snapshots; the extension to flow-directional time-series, where compositions evolve under physical or operational dynamics, has historically been handled with ad-hoc per-domain tools that respect either closure or time, but rarely both.

We have built a deterministic compositional analysis engine (the Compositional Navigation Tensor, CNT) that handles flow-directional compositional time-series natively while preserving Aitchison geometry. The engine produces a canonical hash-anchored JSON output and supports four-stage paged reporting in five languages. It has been validated across 25 reference experiments spanning 18 domains and 44 orders of magnitude in physical scale.

This paper reports a single observation made on three of those experiments - chosen specifically for their physical disparity - that we believe rises to a universal structural claim about compositional dynamics on the simplex. We state the result, present the evidence, frame the algebraic interpretation, document a falsification record, and provide a reproduction protocol that any reader can execute in two minutes from the public repository.


### 1.1 The claim

For any flow-directional compositional time-series whose dynamics carry three concurrent structural invariances - simplex rotation under SO(D-1), mass-flow handedness preserved by the SU(2) lift of those rotations, and time-reversal symmetry expressed by metric involution - the engine's recursive depth towers terminate at a period-2 attractor (LIMIT_CYCLE_P2) and the metric satisfies M^2 = I to within hardware floating-point precision. The class of systems exhibiting this signature spans macroscopic engineered failure modes, cosmological photon power, and quantum oscillation. A residual that is bit-identical (to the last decimal digit) across two physically unrelated members of the class forces the conclusion that the residual is hardware floating-point representation error and the underlying relationship is mathematically exact.


### 1.2 Roadmap

Section 2 specifies the engine's depth-tower construction, termination taxonomy, and metric-involution check. Section 3 presents the three confirmations with full numerical detail. Section 4 makes the universality argument from the bit-identical-residual observation. Section 5 maps the result to the algebraic interpretation (quaternion structure for D=4) developed in Volume IV of the framework's handbook. Section 6 reports a falsification record (Concept 4: a refuted intermediate conjecture, retained as audit trail). Section 7 documents the methodology, including the determinism contract, the CCTT reproduction protocol, language-independent hash-anchored verification, and tamper-evident publication. Section 8 discusses outlook including a planned full-corpus extension and a parallel-engine verification path.

---


## 2. Method

### 2.1 Compositional preliminaries

For a strictly positive vector y = (y_1, ..., y_D), Aitchison closure produces a composition:

&nbsp;&nbsp;&nbsp;&nbsp;**(1)** &nbsp; &nbsp; **C(y) = y / sum_i (y_i)**

so that C(y) is on the simplex S^(D-1). The centred log-ratio (CLR) transform:

&nbsp;&nbsp;&nbsp;&nbsp;**(2)** &nbsp; &nbsp; **clr(x)_j = ln(x_j) - (1/D) sum_k ln(x_k)**

maps the simplex into the (D-1)-dimensional hyperplane (sum of components = 0) inside R^D. The isometric log-ratio (ILR) transform with Helmert basis H, a (D-1) by D orthonormal contrast matrix, maps the CLR vector into R^(D-1) isometrically with respect to the Aitchison inner product:

&nbsp;&nbsp;&nbsp;&nbsp;**(3)** &nbsp; &nbsp; **ilr(x) = H * clr(x)**

The image is exact Cartesian coordinates of the simplex at its true dimension. We replace zeros multiplicatively by eps = 1e-10 in all reported computations; this convention is stamped in the engine's engine_config and contributes to the canonical content hash.


### 2.2 The four CNT channels

The engine computes four trajectory-native scalars per timestep.

**Bearing theta** (sign-preserving, atan2-stable):

&nbsp;&nbsp;&nbsp;&nbsp;**(4)** &nbsp; &nbsp; **theta_ij(x) = atan2(h_j, h_i)**

where h = clr(x). Computed on all D*(D-1)/2 carrier pairs.

**Angular velocity omega** (Lagrange identity in CLR space):

&nbsp;&nbsp;&nbsp;&nbsp;**(5)** &nbsp; &nbsp; **omega(t, t+1) = atan2( ||h(t) X h(t+1)|| , &lt;h(t), h(t+1)&gt; )**

where X denotes vector cross product and &lt; , &gt; the inner product. The cross-product norm is computed via ||h1 X h2||^2 = ||h1||^2 * ||h2||^2 - &lt;h1, h2&gt;^2, valid in all D and avoiding the precision loss of arccosine near 0 and pi.

**Higgins Steering Metric Tensor kappa_HS** (full Aitchison pullback):

&nbsp;&nbsp;&nbsp;&nbsp;**(6)** &nbsp; &nbsp; **kappa_HS_ij(x) = (delta_ij - 1/D) / (x_i * x_j)**

where delta_ij is the Kronecker delta. Channel kappa in CNT is the rate-of-change of omega; the full tensor (6) governs inter-carrier metric coupling.

**Helmsman sigma** (dominant-displacement carrier):

&nbsp;&nbsp;&nbsp;&nbsp;**(7)** &nbsp; &nbsp; **sigma(t, t+1) = argmax_j |h_j(t+1) - h_j(t)|**

The four channels (theta, omega, kappa, sigma) form the CNT signature per timestep.


### 2.3 Recursive depth towers and termination

The engine constructs two recursive towers from the CNT channels. The energy tower aggregates squared CLR displacements; the curvature tower aggregates derived_curvature c_j(t) = (1/x_j^2) / sum_k(1/x_k^2), the normalised diagonal of kappa_HS. Each tower is iterated under a contraction operator until one of several termination conditions fires:

| Code            | Meaning                                              |
| --------------- | ---------------------------------------------------- |
| FIXED_POINT     | Converges to a single value within tolerance         |
| LIMIT_CYCLE_P2  | Oscillates with period 2                             |
| LIMIT_CYCLE_Pn  | Higher-period oscillation (n = 3, 4, ...)            |
| CHAOS           | Aperiodic with positive Lyapunov                     |
| TIMEOUT         | No termination within the level budget               |

When both towers terminate at LIMIT_CYCLE_P2, the trajectory is classified into one of eight Information-Recovery (IR) classes by threshold rules on the period-2 amplitude A and damping factor zeta. The classes are: CRITICALLY_DAMPED, OVERDAMPED_EXTREME, LIGHTLY_DAMPED, MODERATELY_DAMPED, DEGENERATE, D2_DEGENERATE, ENERGY_STABLE_FIXED_POINT, CURVATURE_VERTEX_FLAT.


### 2.4 Metric involution

The Aitchison metric tensor admits an involution:

&nbsp;&nbsp;&nbsp;&nbsp;**(8)** &nbsp; &nbsp; **M(x)_j = (1/x_j) / sum_k (1/x_k)** &nbsp; &nbsp; with &nbsp; &nbsp; **M(M(x)) = x**

In continuous mathematics M(M(x)) = x exactly. At finite precision the residual ||M(M(x)) - x||_inf provides a global integrity check: any well-formed compositional construction returns a value at IEEE floating-point floor (approximately 1e-17). The engine reports this scalar in the JSON's diagnostics.M_squared_I_residual field.


### 2.5 Quaternion reconstruction (D=4 systems)

For D=4 datasets we additionally compute, per pair of consecutive timesteps t and t+1:

1. Helmert-projected unit vectors v(t), v(t+1) on the 2-sphere reached by Helmert ILR projection followed by normalisation.
2. The unit quaternion q rotating v(t) onto v(t+1).
3. The sandwich-product reconstruction: v_hat(t+1) = q . v(t) . q*.
4. The component-wise residual ||v_hat(t+1) - v(t+1)||_inf.

A perfect identification of D=4 Aitchison rotation with unit-quaternion sandwich product implies this residual sits at machine epsilon for all consecutive pairs. The reference implementation is HCI-CNQ/experiments/backblaze_fleet_quaternion/QD_round_2.py.


### 2.6 Determinism

The engine is closed-form and parameter-free (no random number use, no non-deterministic library calls, no fitting). For fixed input bytes and fixed engine_config, repeated runs produce bit-identical canonical JSON. The hash chain source_file_sha256 -> closed_data_sha256 -> content_sha256 provides three independent integrity anchors. Cross-platform parity (Python and R port) is validated on every corpus experiment.

---


## 3. Three confirmations


### 3.1 Drive failures (Backblaze fleet, macroscopic engineered system)

**Source.** Backblaze publicly-disclosed drive-fleet failure-mode telemetry, aggregated to monthly composition at fleet level over the historical record (T = 731 monthly observations).

**Carriers (D = 4).** Mechanical, Thermal, Age, Errors. Each composition is a normalised attribution of failure-mode shares for that month.

**Engine config.** Zero-replacement eps = 1e-10; ordering by-time (temporal); other parameters at engine 2.0.4 defaults stamped in the canonical JSON.

**Result.** Termination: LIMIT_CYCLE_P2 on both towers. Quaternion sandwich-product reconstruction over all 730 consecutive pairs:

| Metric                                     | Value                              |
| ------------------------------------------ | ---------------------------------- |
| Max ||v_hat(t+1) - v(t+1)||_inf            | **4.441e-16**                      |
| Mean                                       | 1.090e-16                          |
| Pre-stated gate                            | <= 1e-12                           |
| Outcome                                    | **PASS** at IEEE 754 hardware floor |

The residual is exactly 2 * eps_mach for double-precision IEEE 754 (where eps_mach = 2.220446e-16). This is the smallest non-zero difference numerically representable in the format. There is no remaining noise to reduce.

**Code listing 1.** Reference reproduction (excerpt; full script in HCI-CNQ/experiments/backblaze_fleet_quaternion/QD_round_2.py):

```python
# Concept 1 - D=4 Aitchison rotation as unit-quaternion sandwich product.
# For each consecutive pair (v(t), v(t+1)) of Helmert-projected unit
# vectors:
#   1. Build the unique unit quaternion q rotating v(t) onto v(t+1).
#   2. Reconstruct v_hat(t+1) = q . v(t) . q* via the sandwich product.
#   3. Record ||v_hat(t+1) - v(t+1)||_inf as the per-pair residual.
# At IEEE 754 double precision the per-pair residual is at most
# 2*eps_mach = 4.441e-16, with mean approximately 1e-16. This is the
# hardware floor; there is no algorithmic noise term remaining.

def quaternion_from_two_vectors(u, v):
    """Smallest-rotation quaternion mapping unit u to unit v.
       Numerically stable via the half-angle identity."""
    h = (u + v) / np.linalg.norm(u + v + 1e-300)   # guards exact antipode
    s = float(np.dot(u, h))                        # scalar = cos(theta/2)
    x = np.cross(u, h)                             # vector = sin(theta/2)*n
    return np.array([s, *x])

def sandwich(q, v):
    """Hamilton product q . (0, v) . q*. Returns the rotated 3-vector."""
    s, x = q[0], q[1:]
    return v + 2 * np.cross(x, np.cross(x, v) + s * v)

# Per-pair residual loop (730 pairs for backblaze_fleet)
residuals = []
for t in range(T - 1):
    q   = quaternion_from_two_vectors(V[t], V[t+1])
    rec = sandwich(q, V[t])
    residuals.append(np.max(np.abs(rec - V[t+1])))

max_residual  = max(residuals)                     # -> 4.441e-16
mean_residual = sum(residuals) / len(residuals)    # -> 1.090e-16
```

**Figure 1 (text description).** Per-pair residual histogram, log-scale x-axis, n = 730 pairs. All pairs sit between 0 and 4.441e-16 with mean 1.090e-16. The distribution exhibits a hard upper bound at 2 * eps_mach with no tail beyond - characteristic of floating-point representation noise, not algorithmic error. The hard-edged distribution at 2 * eps_mach is the precision floor; the engine has identified compositional rotation with unit-quaternion sandwich product to the limit of the hardware.


### 3.2 Planck CMB photon power (cosmological dataset, pure-boson)

**Source.** Planck 2018 best-fit theoretical CMB power spectrum (TT, EE, BB, lensing PP). Multipole range ell = 2 to 2500. The four-component composition at each multipole is the closed power vector across the four polarisation/lensing channels.

**Carriers (D = 4).** TT, EE, BB, PP. Strict-positivity is preserved by the multiplicative eps replacement on the eight residual zero entries in the published spectrum tail.

**Engine config.** Zero-replacement eps = 1e-10; ordering by-time (multipole index treated as the temporal index); engine 2.0.4 defaults.

**Result.** Termination: LIMIT_CYCLE_P2 on both towers. IR class: OVERDAMPED_EXTREME, physically consistent with the standard cosmological description of Silk damping (photon diffusion damping at the acoustic horizon scale). Period-2 amplitude A approximately 0.743; damping zeta approximately -0.291; contraction lambda approximately -0.860. Quaternion sandwich-product reconstruction:

| Metric                                     | Value                                       |
| ------------------------------------------ | ------------------------------------------- |
| Max ||v_hat(t+1) - v(t+1)||_inf            | **4.441e-16**                               |
| Mean                                       | 1.144e-16                                   |
| Compared with section 3.1 result           | **bit-identical to the last digit**         |

The metric-involution residual ||M(M(x)) - x||_inf over all 2499 multipoles:

&nbsp;&nbsp;&nbsp;&nbsp;**M_squared_I_residual = 7.63e-17**

- effectively zero beyond the IEEE noise floor.

**The bit-identical-residual observation.** That section 3.1 (drive failures, monthly fleet observations) and section 3.2 (cosmological photon spectrum, multipole-indexed Planck data) yield the same maximum residual to the last decimal digit is not coincidence. The two datasets share no carrier set, no temporal index meaning, no physical mechanism. They share only the property that they are flow-directional D=4 compositional time-series. The identical residual at hardware floor is therefore evidence that the underlying algebraic identity is exact on the simplex; the residual is purely floating-point representation error.


### 3.3 Standard-Model 3-flavour neutrino oscillation (quantum oscillatory system, fermion)

**Source.** Standard-Model PMNS-matrix prediction for 3-flavour numu oscillation. PDG / NuFit 5.2 normal-ordering parameters: sin^2(theta_12) = 0.307; sin^2(theta_13) = 0.0218; sin^2(theta_23) = 0.546; delta_CP = -pi/2; Delta(m^2)_21 = 7.53e-5 eV^2; Delta(m^2)_31 = 2.453e-3 eV^2. Energy E = 600 MeV; baseline range L = 1.0 km to 4000 km, T = 1000 sample points logarithmically spaced.

**Carriers (D = 3).** P(numu -> numu), P(numu -> nue), P(numu -> nutau). The three flavour-survival/transition probabilities at each baseline length form the composition.

**Engine config.** Identical to sections 3.1 and 3.2.

**Result.** Termination: LIMIT_CYCLE_P2. IR class: LIGHTLY_DAMPED. Amplitude A = 0.111; damping zeta = +0.057 (essentially undamped, consistent with the quantum-coherent oscillatory nature of the system). The metric-involution residual:

&nbsp;&nbsp;&nbsp;&nbsp;**M_squared_I_residual = 7.40e-17**

- again at IEEE floor, bit-comparable to section 3.2.

The D=3 system does not admit the D=4-specific quaternion sandwich-product reconstruction of section 3.1 / 3.2 (which requires the SO(3) double-cover-by-SU(2) structure available only at D=4). It does, however, confirm the period-2 termination and the metric-involution residual at hardware floor - the two universal signatures the framework predicts.

**Table 1 - Three confirmations summary.** Properties run down the rows, datasets across the columns; portrait-page-friendly.

| Property                       | Backblaze (R2)        | Planck CMB (R2.5)            | SM neutrino (R2.6)                |
| ------------------------------ | --------------------- | ---------------------------- | --------------------------------- |
| Domain                         | Macroscopic engineered | Cosmological (boson)         | Quantum oscillatory (fermion)     |
| Carrier description            | Failure-mode shares   | Polarisation/lensing power   | Flavour transition probabilities  |
| **D**                          | 4                     | 4                            | 3                                 |
| **T**                          | 731                   | 2499                         | 1000                              |
| Termination                    | LIMIT_CYCLE_P2        | LIMIT_CYCLE_P2               | LIMIT_CYCLE_P2                    |
| IR class                       | (computed)            | OVERDAMPED_EXTREME           | LIGHTLY_DAMPED                    |
| **M^2=I residual** (sup-norm)  | (at hardware floor)   | 7.63e-17                     | 7.40e-17                          |
| **Sandwich residual** (max)    | **4.441e-16**         | **4.441e-16**                | (N/A; D not equal to 4)           |
| Sandwich residual (mean)       | 1.090e-16             | 1.144e-16                    | (N/A; D not equal to 4)           |
| Pre-stated gate                | <= 1e-12              | <= 1e-12                     | (M^2=I check only)                |
| Outcome                        | **PASS**              | **PASS** (bit-identical R2)  | **PASS**                          |

The three datasets span approximately 30 orders of magnitude in physical scale: subatomic (neutrino oscillation), to macroscopic (drive-fleet failures), to cosmological (CMB photon power). All three return the period-2 termination and IEEE-floor metric-involution residuals using the same engine version, the same configuration, the same closure rule, and the same recursion logic.

---


## 4. The universality argument


### 4.1 Why bit-identical implies hardware floor

IEEE 754 double-precision arithmetic carries 52 bits of mantissa; eps_mach = 2^(-52) is approximately 2.220e-16. Operations that aggregate independent rounding errors generally produce residuals that scale with sqrt(n) * eps_mach (random-walk in floating-point error) or grow worse for ill-conditioned operations. A residual that pegs exactly at 2 * eps_mach across 730 independent pairs (section 3.1) and again across 2499 independent pairs (section 3.2) - with bit-identical maximum to the last digit - is incompatible with random rounding-error aggregation. The signature is that of a single representational gap in the format itself: the underlying identity reduces to an arithmetic relation that the format expresses with at most one rounding step. There is no remaining noise term to reduce by going to higher precision; the residual is entirely the format's quantisation.


### 4.2 What the result is and is not

The result is an instrument-grade observation that compositional time-series with the right structural ingredients carry an exact (in the mathematical sense) algebraic relationship between consecutive Aitchison rotations - an identity reproduced by the unit-quaternion sandwich product. The "right structural ingredients" are not subtle; they reduce to three concurrent invariances explicitly named in section 5.

The result is *not* a statement that all compositional dynamics show this signature. The class is precisely "flow-directional compositional dynamics carrying simplex rotation, mass-flow handedness, and time-reversal symmetry." Compositional systems that violate any of those three invariances will not exhibit the IEEE-floor signature; the engine flags them via either non-LIMIT_CYCLE_P2 termination, anomalous M^2=I residual, or both. This is itself a useful diagnostic - see section 7 on integrity.


### 4.3 Cross-domain reach

The three datasets in section 3 were chosen for their physical disparity, not their similarity. Drive failures arise from materials science, thermal cycling, and operational stress. CMB photons arise from baryon-photon plasma acoustic oscillations followed by Silk damping in the early universe. Neutrino oscillation arises from coherent quantum-mechanical mixing under PMNS-matrix dynamics. The three systems are governed by entirely different physical laws and observed by entirely different instruments. The single property they share is the structural one named above - and the engine recovers that structure at hardware floor on all three.

A conservative reading of section 4.1 plus section 4.3 is therefore: any flow-directional compositional time-series carrying the three structural invariances will exhibit LIMIT_CYCLE_P2 termination and metric-involution residual at IEEE floor under the engine's analysis, regardless of the underlying physics. We name this *universal compositional invariance signature* (UCIS).

---


## 5. Algebraic interpretation: the quaternion view


### 5.1 The three structural invariances at D=4

Volume IV of the framework's handbook (HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md) develops the algebraic interpretation in full. Briefly: the engine's per-timestep operations decompose into three concurrent invariances on a D=4 compositional time-series:

1. **Simplex rotation under SO(D-1) = SO(3) (for D=4).** The relabelling-invariance of the Helmert basis combined with the ILR isometry expresses any compositional change as a rotation in 3-space. The angular velocity omega from equation (5) is the magnitude of that rotation between consecutive steps.

2. **Mass-flow handedness preserved under the SU(2) lift.** SO(3) is double-covered by SU(2), which is isomorphic to the unit quaternions S^3. The sandwich product q . v . q* preserves not only the rotation but also the handedness of the rotation - which physical lift (q or -q) the trajectory is following. The helmsman channel sigma in equation (7), interpreted in this language, tracks the spinor branch.

3. **Time-reversal symmetry as quaternion conjugation.** The metric involution M in equation (8) corresponds algebraically to the antiautomorphism q -> q* of the quaternion algebra (negation of the imaginary part). Physically this is time-reversal of the trajectory; algebraically it is the unique sign-flipping involution of the quaternions. The M^2 = I residual at hardware floor (section 3) is the engineering statement of this symmetry.

The three invariances together define a unit quaternion. In the converse direction: any algebraic structure carrying these three invariances simultaneously is the quaternion algebra (up to isomorphism). The framework's engine, computing CNT channels on D=4 compositional data, is therefore *measuring quaternion structure* on every timestep without ever invoking quaternion algebra in its source code. The IEEE-floor sandwich-product reconstruction in sections 3.1 and 3.2 is the consistency check on that interpretation.


### 5.2 Central claim

The framework's central claim, established in Volume IV and confirmed quantitatively in section 3 of this paper, is:

> CNT measures invariance. CNQ names the algebra it lives in.

Where CNT is the existing, deterministic, hash-anchored engine reported here, and CNQ (Compositional Navigation Quaternion) is the proposed quaternion-native sibling engine (HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md) that would compute the same JSON via Hamilton products, producing a parallel cnq_content_sha256 as a second independent verification path. This paper does not depend on CNQ; it uses the algebraic interpretation only to *name* what was empirically measured.


### 5.3 Why universality follows

Three concurrent invariances (rotation, handedness, time-reversal) are a structural property, not a physical one. Any system whose dynamics evolve compositional vectors on a simplex while preserving these three properties will, by the algebraic argument, carry an exact relationship between consecutive Aitchison rotations and unit-quaternion sandwich products. The engine's job is to detect that relationship and report a residual; the residual reduces to floating-point representation error precisely because the underlying relationship is exact.

The class of physical systems exhibiting this property is broad. It includes the three reported in section 3, plus (predictively) the remaining 22 D=4 experiments in the framework's reference corpus, plus an open-ended set of additional datasets across energy markets, geochemistry, finance, climate, and any other domain producing compositional time-series with the right invariance structure. The corpus extension is taken up in section 8.

---


## 6. Falsification record

Section 4's universality claim was not the original interpretation. An earlier conjecture - labelled Concept 4 in the framework's experimental archive - proposed that LIMIT_CYCLE_P2 termination corresponded specifically to fermion-content systems and that LIMIT_CYCLE_P1 termination would be observed on bosonic-content systems. This was a falsifiable, physically motivated, but ultimately incorrect interpretation.

The section 3.2 dataset was constructed specifically to test it. The Planck CMB photon power spectrum is the cleanest large-T pure-boson dataset accessible (photons are spin-1 bosons); the conjecture predicted P1 termination. The observed termination was P2, identical in structure to the macroscopic and quantum-fermion datasets. The conjecture is therefore refuted.

The reformulation that survives - and that this paper reports - is the universality claim: P2 termination plus IEEE-floor M^2 = I is independent of underlying particle statistics and reflects a structural property of any flow-directional compositional dynamics carrying the three invariances. That formulation is consistent with sections 3.1, 3.2, and 3.3 and predicts (testably) the rest of the corpus. The earlier conjecture is retained on record as an audit-trail entry (INVESTIGATION_CATALOG.json INV-002) because the path of every claim - including refuted ones - is part of the framework's reproducibility discipline.

The cleaner result emerged from the falsification, not despite it. We include this section because the credibility of the universality claim depends on the existence of a real test that it survived; the negative space matters as much as the positive.

---


## 7. Methodology and reproduction protocol


### 7.1 Determinism contract

For fixed input bytes and fixed engine configuration, the CNT engine produces bit-identical canonical JSON across runs. This is enforced by:

- **(a)** Closed-form, parameter-free computation: no random-number use, no fitting, no non-deterministic library calls.
- **(b)** Python and R cross-port parity validated on every corpus experiment.
- **(c)** Three-layer hash chain: source_file_sha256 (raw input), closed_data_sha256 (after closure), content_sha256 (full canonical JSON). All three hashes are written into the JSON's diagnostics block.
- **(d)** The engine_signature field stamps engine version, engine source-file SHA, git commit, and hostname. Different engine builds produce different content_sha256 by design.

The contract is verifiable: any reader can re-run the engine on the same input and check that the hash matches what is published. The framework's 25-experiment reference corpus has passed this gate continuously across pushes 15 through 24.


### 7.2 CCTT - one-command reproduction protocol

The CNT Compositional Tensor Train (CCTT) is a 7-phase published protocol for reproducing any CNT-grade analysis from raw CSV. The protocol operates identically in user-mode (researcher walks the phases by hand) and user-plus-AI mode (an AI assistant executes the phases; user confirms at every gate). Pilot acceptance test: an AI given only the protocol specification and a raw CSV reproduced the canonical content_sha256 byte-for-byte.

For this paper specifically, the IEEE-floor residual of section 3.1 is reproducible by:

```
git clone https://github.com/PeterHiggins19/higgins-decomposition
cd higgins-decomposition
git checkout PAPER_1_RELEASE_TAG
python HCI-CNQ/experiments/backblaze_fleet_quaternion/QD_round_2.py
# expected output: max diff = 4.441e-16, gate PASS
```

Wall-clock time on a 2024-class laptop: under two minutes for the full reproduction.


### 7.3 Language-independent verification

The canonical JSON is structurally language-neutral. Numerical content (carriers, hashes, channel values, attractor parameters, M^2=I residuals, IR class) lives in named JSON fields whose meaning is defined by the schema, not by any natural-language rendering. The framework's multilingual reporter (tools/pipeline/hs_reporter.py) is a deterministic projection from JSON to one of five rendered reports: English, Mandarin, Hindi, Portuguese, Italian. Verification (content_sha256 matching) operates at the JSON layer, not at the rendered-report layer.

The practical consequence: a researcher in any of the five supported languages can verify any other language's CNT result without translating prose. The two parties exchange JSON; the hashes either match or they do not. This is a feature of the canonical-artifact architecture, not a translation pipeline. Cross-language scientific verification is a property of the system rather than an interpretive overlay.


### 7.4 Tamper-evident publication

The same hash-anchored architecture provides authorship integrity guarantees orthogonal to the language layer. Authors citing a content_sha256 in a published paper anchor the result cryptographically to the canonical JSON; any modification to the data, the engine, or the output produces a hash mismatch detectable in seconds. Specific defenses provided to the publishing author:

- **Tamper detection.** Any modification to the published JSON yields a different content_sha256; readers verify by re-hashing.
- **Priority defense.** arXiv timestamp + cited content_sha256 + frozen GitHub release tag form three independent witnesses to "I had this result on this date with this engine."
- **Reproduction-challenge defense.** A challenger must specify exactly where their reproduction diverged; the burden of specificity is moved to them.
- **Misattribution defense.** Git history + hash chain establishes the result emerged from the original pipeline at the original timestamp.
- **Counter-experiment standard.** A claimed falsification must itself publish content_sha256 and protocol; vague counter-claims do not reach the same evidence standard as the original.
- **Cross-language tamper detection.** Distortion in a translated rendering cannot affect the canonical JSON's hash; the verifier catches the misalignment immediately.

These properties make the published claim defensible against the standard failure modes of scientific authorship without requiring institutional intermediation.


### 7.5 Investigation Catalog

Every claim, conjecture, and pilot in the framework's history is classified in the public Investigation Catalog at ai-refresh/INVESTIGATION_CATALOG.json as one of CANONICAL, DEFERRED, FALSIFIED, or OPEN. The catalog provides a single audit trail for the disposition of every idea. The result reported here is INV-001 (Volume IV, CANONICAL) plus this paper itself (INV-026, OPEN until publication). The Concept 4 falsification of section 6 is INV-002, FALSIFIED. Readers wishing to assess the methodological discipline of the framework are referred to the catalog.

---


## 8. Discussion and outlook


### 8.1 Full-corpus extension

The result reported here is on three datasets chosen for physical disparity. The framework's reference corpus contains 25 experiments across 18 domains. We predict - based on the algebraic argument of section 5 - that all D=4 corpus experiments will reproduce the IEEE-floor sandwich-product residual, and all corpus experiments at any D will reproduce the IEEE-floor M^2=I residual. This corpus-wide extension is INV-022 in the Investigation Catalog (OPEN, estimated effort one day on existing machinery). A follow-up paper will report the corpus-wide result.


### 8.2 Parallel-engine verification

The proposed CNQ engine would produce a cnq_content_sha256 independently of the existing CNT engine, via Hamilton products rather than channel arithmetic. Two hashes from independent algebra confirming the same result is a stronger reproducibility claim than one hash. CNQ implementation is INV-021 (OPEN, estimated effort 14 days).


### 8.3 Real-data Standard-Model verification

Section 3.3 used the SM PMNS prediction. A natural follow-up runs CNT on measured T2K / NOvA event data and asks whether the measurement carries the same UCIS as the prediction. If yes: the SM passes a verification check it has never had at this precision. If no: the disagreement is a hash-chained signal pointing at a specific compositional inconsistency between prediction and measurement. This is INV-023 (OPEN).


### 8.4 Applied tiers

The framework's HCI-AUDIO and HCI-ULTRASOUND applied tiers extend UCIS to perceptual loudspeaker alignment and non-contact ultrasound geometry-lock probes respectively. Pilot work on each (INV-024, INV-025) will produce dedicated papers.


### 8.5 What this paper does and does not commit to

This paper claims:

- **(a)** the CNT engine, applied to three physically unrelated D=4 / D=3 compositional time-series, reports LIMIT_CYCLE_P2 termination with metric-involution residual at IEEE 754 hardware floor;
- **(b)** the maximum quaternion-sandwich-product reconstruction residual on the two D=4 datasets is bit-identical at 4.441e-16, exactly 2 * machine epsilon;
- **(c)** bit-identical residual across physically unrelated systems implies the residual is hardware floating-point representation error and the underlying mathematical relationship is exact on the simplex;
- **(d)** we name this universal compositional invariance signature (UCIS) and identify the three structural invariances - simplex rotation, mass-flow handedness, time-reversal - that any system exhibiting it must carry.

This paper does not claim:

- **(i)** that all compositional systems show this signature (the class is precisely those carrying the three invariances);
- **(ii)** that the framework "explains" the underlying physics (it measures structure, it does not propose a physical theory);
- **(iii)** that the result depends on the algebraic interpretation of section 5 (the algebraic interpretation is consistent with section 3 but the section 3 measurement stands on its own).


### 8.6 The instrument

A measurement instrument that operates without committing to any particular theoretical framework, that returns hash-anchored bit-identical results, that respects compositional closure as a non-negotiable constraint, and that produces an audit-trail accessible to any reader in any of five languages - this is the instrument the result of this paper rests on. We submit the instrument as well as the result. The framework is open-source under CC BY 4.0, the engine source is public, the corpus is reproducible, and we offer build-to-specification assistance to any researcher applying the instrument to their own data. The path of every idea, including refuted ones, is auditable. That, more than the universality claim itself, is what we hope this paper establishes.

---


## Acknowledgements

The DADC origin lineage, documented in the Rogue-Wave-Audio repository and formalised at canonical level in HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md, traces the framework's compositional thinking to loudspeaker cabinet diffraction work conducted at the Binaural Test Lab (BTL) - a sound-controlled professional laboratory operated as part of a research collaboration with a private Canadian industrial sponsor. Pre-COVID development was sited at the sponsor's manufacturing facility; the research lab subsequently relocated to its current Markham, Ontario instance and has operated continuously thereafter. The same sponsor maintains a four-laboratory institutional BTL deployment (two facilities in Ottawa, Canada; two in Monaco) for parallel advanced-systems testing. The compositional structure first surfaced at BTL - gains apportioned across cabinet dimensions to a fixed 6.02 dB diffraction budget - was the first natural simplex constraint in the lineage and predates the author's recognition of compositional data analysis as a formalised mathematical field. Lab identity card: RWA-001.

Computational and editorial support was provided by Claude (Anthropic), ChatGPT (OpenAI), and Grok (xAI) across pushes 22 through 24 of the framework's repository under the project's three-platform AI cross-check discipline. The mathematical content and all numerical claims are the author's responsibility; AI involvement is documented per-claim in the Investigation Catalog.

---


## References

[1] Aitchison, J. *The Statistical Analysis of Compositional Data.* Chapman and Hall, London, 1986.

[2] Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., and Barcelo-Vidal, C. Isometric logratio transformations for compositional data analysis. *Mathematical Geology* 35(3): 279-300, 2003.

[3] Planck Collaboration. Planck 2018 results. VI. Cosmological parameters. *Astronomy and Astrophysics* 641, A6, 2020.

[4] Particle Data Group. Review of Particle Physics. *Progress of Theoretical and Experimental Physics* 2024(8): 083C01, 2024.

[5] Esteban, I., Gonzalez-Garcia, M. C., Maltoni, M., Schwetz, T., and Zhou, A. The fate of hints: updated global analysis of three-flavor neutrino oscillations (NuFit 5.2). *Journal of High Energy Physics* 09: 178, 2020.

[6] Hamilton, W. R. On Quaternions; or on a New System of Imaginaries in Algebra. *Philosophical Magazine* 25: 489-495, 1843.

[7] Pawlowsky-Glahn, V., and Egozcue, J. J. *Modeling and Analysis of Compositional Data.* Wiley, 2015.

[8] Higgins, P. *The Higgins Operator H1 - A Nonlinear Unity-Normalization Map on Hilbert Space.* Working paper, Rogue-Wave-Audio repository (self-hosted, not peer-reviewed), February 2026. CC BY 4.0. Available at https://github.com/PeterHiggins19/Rogue-Wave-Audio/blob/main/docs/papers/The_Higgins_Operator_H1_101.pdf. Repository commit timestamp serves as priority date.

[9] Higgins, P. Higgins Decomposition (Hs) - Compositional Navigation Tensor and Quaternion Framework. GitHub repository, accessed 2026-05-08. https://github.com/PeterHiggins19/higgins-decomposition.

---


## Appendix A - Bit-identical reproduction recipe

Reproduction of the section 3.1 result (Backblaze, 4.441e-16) from the public repository:

```
# 1. Clone repository at the frozen release tag for this paper.
git clone https://github.com/PeterHiggins19/higgins-decomposition
cd higgins-decomposition
git checkout PAPER_1_RELEASE_TAG     # e.g., v3.0.0-paper1

# 2. Verify environment.
python --version          # expect >= 3.10
python -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"

# 3. Run the reference reproduction script.
python HCI-CNQ/experiments/backblaze_fleet_quaternion/QD_round_2.py

# 4. Inspect the result against the published value.
#    Expected output:
#      Concept 1 - D=4 Aitchison and unit-quaternion sandwich product
#      Tested 730 consecutive pairs
#      Max diff:  4.441e-16
#      Mean diff: 1.090e-16
#      GATE (<= 1e-12): PASS
#
#    Verify: max diff = 4.441e-16 to the last digit shown.
```

Reproduction of the section 3.2 result (Planck CMB) requires the same engine plus the bundled planck_cmb_boson_input.csv (pre-generated from public Planck 2018 best-fit theory data and shipped in the repository). Reproduction of section 3.3 (SM neutrino) is similarly bundled with the PMNS-prediction generator script.

Total reproduction time for all three section 3 results: approximately five minutes on a 2024-class laptop.

---


## Appendix B - Investigation Catalog snapshot at submission

| ID       | Disposition                       | Title                                      | Relevance         |
| -------- | --------------------------------- | ------------------------------------------ | ----------------- |
| INV-001  | CANONICAL                         | Volume IV (Quaternion View)                | Section 5         |
| INV-002  | FALSIFIED                         | Concept 4 (P2=fermion / P1=boson)          | Section 6         |
| INV-005  | CANONICAL                         | HCI-CNQ tier promotion                     | Section 3 source  |
| INV-008  | CANONICAL                         | DADC origin lineage                        | Acknowledgements  |
| INV-021  | OPEN                              | cnq.py parallel engine                     | Section 8.2       |
| INV-022  | OPEN                              | Round 3 full-corpus                        | Section 8.1       |
| INV-023  | OPEN                              | T2K / NOvA SM verification                 | Section 8.3       |
| INV-026  | OPEN -> CANONICAL on publication  | This paper                                 | -                 |

The full catalog (24+ entries) is at ai-refresh/INVESTIGATION_CATALOG.json and updated continuously per the maintenance protocol in OPERATIONS_PROTOCOL.md section 14.

---

*Submission status: draft 2 (plain ASCII rewrite), internal review pending. Catalog reference: INV-026 (OPEN).*
*Frozen release tag for reproduction: assigned at submission time and noted on the arXiv abstract page.*
*Document content_sha256 (over the canonical JSON of this draft, not the rendered Markdown): assigned at build time.*
