# The Higgins Coordinate System

**Peter Higgins — Independent Researcher — Markham, Ontario, Canada**
**Rogue Wave Audio — RWA-001**
**Founded: 1 May 2026**

The instrument reads. The expert decides. The loop stays open.

---

> **Status note (2026-05-06).** This document is the **foundational
> specification** of the Higgins Coordinate System as it stood at the
> close of its first development cycle (April–May 2026). The same
> axiom, simplex foundations, CLR coordinates, and projection cube
> remain canonical. The operational implementation has since matured
> into the **Compositional Navigation Tensor (CNT)** engine 2.0.4 /
> schema 2.1.0, which now lives at [`HCI-CNT/`](../HCI-CNT/). CNT is
> the current canonical engine and report system; the 12-step
> pipeline described in §8 is preserved here as the original
> reference. For active use, the three CNT handbook volumes at
> [`HCI-CNT/handbook/`](../HCI-CNT/handbook/) are the current
> documentation, and the 25-experiment canonical corpus lives at
> [`experiments/Hs-CNT_2026-05/`](../experiments/Hs-CNT_2026-05/).


---

## 1. What This Document Is

This is the complete specification of the Higgins Coordinate System — a deterministic instrument for reading the geometric structure of compositional data. Everything in this document derives from a single axiom, builds through CoDa-approved mathematics, and terminates in a standardised diagnostic output.

The system was developed over 8 days (22-30 April 2026) and tested across 18 scientific domains spanning 44 orders of magnitude (10^-18 m to 10^26 m). It has produced 32 publication-worthy findings, 4 mathematical proofs, and a complete diagnostic code system of 106 codes and 14 structural modes.

This document replaces all prior specifications. It starts from the correct starting point: the barycentre.

---

## 2. The Generating Axiom

    For all X: Hs(X) = Hs(X)

The function is pure. Same input, same output, always. No hidden state, no randomness, no side effects. From this single axiom, three constraints follow:

**Closure.** The reading depends on nothing outside the input. The function is self-contained.

**Completeness.** For every valid input, the output exists. The domain must be bounded — there must be guards.

**Invariance.** The output does not change between calls. Every sub-function must also be deterministic. Therefore: the function decomposes into self-similar parts.

The entire pipeline, every diagnostic code, every structural mode, and every output format is a necessary consequence of this axiom.

---

## 3. The Barycentre

A composition is a vector of D positive parts carrying relative information only. The absolute size is lost at closure. What remains is structure.

The barycentre of the D-simplex is the uniform composition:

    e = (1/D, 1/D, ..., 1/D)

This is the point of maximum symmetry — every carrier contributes equally. It is fixed by the geometry of the simplex, not by the data. It does not move. It is the single fixed reference against which all structure is measured.

In the Poincare disc, the barycentre maps to the origin (r_P = 0). In the polar slice, it is the centre of the grid. In every cube face projection, it is the zero axis. Everything radiates from here.

---

## 4. The Higgins Coordinate

### 4.1 Definition

Given a composition x(t) at observation index t, the Higgins Coordinate is:

    h(t) = CLR(x(t))

where CLR is the Centred Log-Ratio transform:

    h_j(t) = ln(x_j(t)) - (1/D) * SUM_k ln(x_k(t))

This is the Aitchison isometry (1986). It maps compositions from the D-simplex to R^D, where the image lies in a (D-1)-dimensional hyperplane through the origin, satisfying:

    SUM_j h_j(t) = 0

Proof: SUM_j h_j = SUM_j [ln(x_j) - (1/D)*SUM_k ln(x_k)] = SUM_j ln(x_j) - D*(1/D)*SUM_k ln(x_k) = 0.

**h(t) is a position vector from the barycentre to the data point.** This is not an interpretation — it is the mathematical definition of the CLR transform. Each h(t) is computed from x(t) alone. No other observation is required. No inter-point connection exists.

### 4.2 Properties

**Magnitude.** The Aitchison norm:

    ||h(t)||_A = sqrt(SUM_j h_j(t)^2)

measures the distance from the barycentre. At uniform composition, ||h|| = 0. As composition concentrates on a single carrier, ||h|| approaches infinity.

Note: Standard CoDa defines ||x||_A = sqrt((1/D)*SUM CLR_j^2). The Hs pipeline uses the unnormalised form sqrt(SUM CLR_j^2) throughout. This is a uniform scaling by sqrt(D). All distances, norms, and comparisons within the system are self-consistent.

**Direction.** The unit vector h(t)/||h(t)|| encodes which carriers dominate and which are suppressed. Positive components are above the geometric mean; negative components are below it.

**Independence.** Each h(t) is computed from x(t) alone. The Higgins Coordinate at index t carries no information from any other index.

### 4.3 What the CLR Is and Is Not

The CLR is the canonical embedding of the simplex into Euclidean space. It is:

- An isometry (preserves Aitchison distances)
- Invertible (CLR to composition and back, losslessly)
- The unique transform satisfying scale invariance, ratio preservation, and centering
- Standard CoDa mathematics (Aitchison 1986)

It is NOT:

- An approximation
- A projection that loses information
- Dependent on basis choice for its scalar diagnostics (Tr(V) is invariant under CLR/ILR — proven, see Section 9.3)

### 4.4 Basis Invariance Theorem

Let PSI be the Helmert basis (D x (D-1), orthonormal columns). Then ILR = PSI^T * CLR, and:

    Tr(PSI^T * Cov(CLR) * PSI) = Tr(Cov(CLR))

The trace of the variation matrix is invariant under CLR/ILR basis change. This means the scalar diagnostics produced by the instrument do not depend on which orthonormal basis is chosen. ALR (additive log-ratio) breaks this invariance because its transformation matrix is not orthogonal — ALR inflates the trace by up to 3x and can reverse the HVLD shape classification.

---

## 5. The Projection Cube

### 5.1 Axis Assignment

For a dataset with D carriers and N observations indexed by t:

    Axis X: CLR dimension 1 — h_1(t)
    Axis Y: CLR dimension 2 — h_2(t)
    Axis Z: Observation index t

These three axes define a rectangular coordinate system. Each observation is a point (h_1(t), h_2(t), t) with a position vector from the barycentre axis.

### 5.2 Three Face Projections

Looking at the cube from three orthogonal directions yields three mutually exclusive projections. Each shows the barycentre and position vectors radiating to data points.

**Face XY — The Compositional Plane (Plan View)**

    Project onto: (h_1, h_2)
    Suppress: t
    Barycentre: the origin (0, 0)
    Each vector: line from (0,0) to (h_1(t), h_2(t))

Shows directional structure with time removed. Points near the origin are near-uniform. Points far from origin are concentrated. The angle encodes which carriers dominate. A change of dominant carrier appears as angular rotation.

**Face XZ — Front Elevation**

    Project onto: (t, h_1)
    Suppress: h_2
    Barycentre axis: the horizontal line h_1 = 0
    Each vector: vertical line from (t, 0) to (t, h_1(t))

Shows how CLR dimension 1 evolves relative to the barycentre across the observation window. Vectors above the axis: carrier above geometric mean. Below: carrier below geometric mean.

**Face YZ — Side Elevation**

    Project onto: (t, h_2)
    Suppress: h_1
    Barycentre axis: the horizontal line h_2 = 0
    Each vector: vertical line from (t, 0) to (t, h_2(t))

Same structure for CLR dimension 2.

### 5.3 Completeness

Three faces, three projections, each showing the barycentre and vectors from it. No connecting lines between consecutive points. The time ordering is visible because axis Z is the observation index — the points are spaced along it. Colour encoding (green to red) reinforces the index ordering without implying interpolation.

For D > 3 carriers, additional cube projections are formed by selecting different pairs (h_i, h_j) for the XY plane. The number of distinct compositional planes is C(D-1, 2) = (D-1)(D-2)/2. Each can be paired with t to form its own projection cube.

### 5.4 What Is Not Drawn

No lines connect h(t) to h(t+1). The instrument does not know what happened between measurements. No splines are fitted. No interpolation is performed. The positions are discrete. The word "trajectory" is retired — a trajectory implies continuous motion along a path. The Higgins Coordinate is a discrete sequence of independent position vectors.

---

## 6. The Polar Slice

### 6.1 Definition

At each observation index t, the full D-dimensional Higgins Coordinate h(t) is rendered as a polar diagram:

    For each carrier j = 1, ..., D:
        Radial axis at angle theta_j = 2*pi*(j-1)/D
        Radial distance: |h_j(t)| / max(|h|)
        Sign: encoded by colour (green = above geometric mean, red = below)

The resulting D-vertex polygon is the **Higgins Polar Slice** at index t. The barycentre is the centre of the polar grid. Each vertex is the tip of a radial vector from centre along carrier j's axis.

This is the full-dimensional Higgins Coordinate rendered in carrier space, with no dimensional reduction.

### 6.2 The Composite Overlay (Ghost Stack)

Overlaying all N polar slices on a single plot with alpha-blended transparency reveals which carriers are stable (overlapping vertices) versus which shift across the observation window (spread vertices). This is a visual summary of the barycentric vector sequence without any connecting lines.

### 6.3 The Circularity Ratio

From the polar slice at index t:

    rho(t) = r_min / r_max

where r_min and r_max are the minimum and maximum radii of the polar projection. This is the Cayley transform:

    rho = (1 - alpha*a) / (1 + alpha*a)

where a = (r_max - r_min)/(r_max + r_min) is the normalised asymmetry and alpha = (1-f)/(1+f) is the projector parameter derived from the floor f.

The circularity ratio measures how circular (uniform) versus elongated (concentrated) the composition is. At rho = 1, the polar slice is a perfect circle (uniform composition). As rho approaches 0, the slice collapses to a line (single-carrier dominance).

---

## 7. The Tensor Functor

### 7.1 The Complete Function Chain

    Hs(X) = rho . Tr . SIGMA . LAMBDA . S(X)

Five named layers, each with explicit tensor rank:

| Layer | Name | Operation | Rank Change | Attribution |
|-------|------|-----------|-------------|-------------|
| S | Closure | x_ij / SUM_k x_ik | (1,1) to (1,1) | Aitchison (1982) |
| LAMBDA | CLR Transform | ln(p_ij) - (1/D)*SUM_k ln(p_ik) | (1,1) to (1,1) | Aitchison (1986) |
| SIGMA | Covariance Tensor | (1/(N-1))*SUM_t (h(t)-h_bar)(h(t)-h_bar)^T | (1,1) to (0,2) sym | Aitchison (1986) |
| Tr | Trace Contraction | SUM_i V_ii = SUM_i lambda_i | (0,2) to (0,0) | Linear algebra |
| rho | Classification | Pattern match against transcendental constants | (0,0) to label | Higgins (2026) |

The trace contraction Tr is the balun gate — the dimensional collapse from a D x D matrix to a scalar. This is where the full eigenstructure of the variation matrix is contracted to a single number. CLR and ILR produce the same trace (basis invariance). ALR does not.

### 7.2 The Variation Matrix V

    V = (1/(N-1)) * SUM_t (h(t) - h_bar) * (h(t) - h_bar)^T

where h_bar = (1/N)*SUM_t h(t) is the sample mean of the Higgins Coordinates.

This is a (D x D) symmetric positive-definite matrix with:

- Eigenvalues lambda_1 >= lambda_2 >= ... >= lambda_D (the variance along each principal axis)
- Eigenvectors v_1, v_2, ..., v_D (the principal directions of compositional variation)
- Trace: sigma^2_A = Tr(V) = SUM_i lambda_i (total Aitchison variance)

The variation matrix is computed from the collection of position vectors — it measures how the Higgins Coordinates spread around their mean, not how they connect to each other in time.

### 7.3 Eigenstructure Diagnostics

The eigenstructure of V carries information beyond the trace:

- **Eigenvalue dominance:** lambda_1/Tr(V) — if close to 1, the variation is essentially 1-dimensional
- **Eigenvector stability:** |<v_1(first window), v_1(last window)>| — measures whether the principal direction rotates
- **Condition number:** kappa = lambda_max/lambda_min — measures anisotropy
- **Von Neumann entropy:** S_vN = -SUM(rho_eig * ln(rho_eig)) where rho_eig = lambda/Tr — measures eigenvalue uniformity
- **Reflection coefficient:** GAMMA = sqrt(1 - lambda_1/Tr(V)) — impedance match measure
- **VSWR:** (1+GAMMA)/(1-GAMMA) — standing wave ratio analogue
- **Power law:** lambda_1(t) ~ c*t^alpha, R^2 of fit — deterministic eigenvalue evolution

### 7.4 The Impedance Match Observation

Empirically, tested systems exhibit low reflection coefficient (GAMMA near 0), consistent with rank-1 dominant covariance. This is an observed property of natural compositional data, not a theorem. It means that a single principal direction typically captures most of the compositional variance — the variation matrix is effectively rank-1.

---

## 8. The Pipeline

### 8.1 The 12-Step Decomposition (foundational reference)

The 12-step pipeline below was the operational implementation of the
tensor functor at the close of the first development cycle (May 2026).
It is preserved here as the **foundational reference** — the original
end-to-end recipe the system was built on.

**The current canonical engine is CNT 2.0.4** in
[`HCI-CNT/engine/cnt.py`](../HCI-CNT/engine/cnt.py) (Python) and
[`HCI-CNT/engine/cnt.R`](../HCI-CNT/engine/cnt.R) (R, parity). CNT
preserves every axiom and every operator named here — closure, CLR,
variance trajectory, matrix analysis, transcendental squeeze, EITT,
report — and additionally provides:

* a single canonical JSON output conforming to schema 2.1.0
  (recorded in [`HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](../HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) Part E);
* a four-stage paged atlas (Order 1 through Order 4+) replacing the
  scattered standalone outputs;
* trajectory-native operators — bearings θ, angular velocity ω,
  helmsman σ, period-2 attractor, IR class — built on the same
  tensor structure;
* end-to-end hash-chained provenance (`source_file_sha256` →
  `engine_signature` → `content_sha256` → PDF page footer);
* a determinism gate over a 25-experiment canonical corpus,
  passing 25 of 25 byte-identically.

The 12 steps below remain mathematically valid; users running new
analyses should reach for CNT (`HCI-CNT/`) rather than re-implementing
the steps directly. The 12-step recipe is documented here for
historical lineage and to make the inheritance from this foundational
spec to the current engine explicit.

For the operational mapping from each step below into its CNT
counterpart, see Volume I §C ("The CNT Engine: tensor decomposition
over the simplex") and Volume I §D (engine pseudocode).

---

The pipeline as originally specified:

| Step | Operation | What It Computes |
|------|-----------|-----------------|
| 1-3 | Configuration | System name, carriers, raw data load |
| 4 | Closure (S) | Zero replacement (delta = 1e-6), closure to simplex |
| 5 | CLR Transform (LAMBDA) | Higgins Coordinates h(t) for all t |
| 6 | Variance (SIGMA, Tr) | Cumulative sigma^2_A(t), HVLD shape fit |
| 6.5 | Matrix Analysis | V(t) eigenstructure, impedance metrics |
| 7 | HVLD | Quadratic fit: shape (bowl/hill), R^2, vertex |
| 8 | Super Squeeze | Test sigma^2_A against 35 transcendental constants |
| 9 | EITT | Entropy invariance under geometric-mean decimation |
| 10 | Ternary | Projection to 2D (barycentric for D=3) |
| 11 | Complex Plane | Centroid-relative polar coordinates |
| 12 | Report | Diagnostic codes, fingerprint, structured output |

### 8.2 Input Guards

Four mandatory guards enforce the domain boundary:

| Guard | Condition | Code |
|-------|-----------|------|
| Dimensionality | D >= 2 | GD-D2M-ERR |
| Sample size | N >= 5 | GD-N5M-ERR |
| Data integrity | No NaN, no Inf | GD-NAN-ERR, GD-INF-ERR |
| Scale sanity | max/min < 10^15 | GD-SCL-ERR |

### 8.3 The HVLD (Higgins Vertex Lock Diagnostic)

Quadratic fit to the cumulative variance sequence sigma^2_A(t):

    y = a*t^2 + b*t + c

- a > 0: **bowl** (information accelerating, variance convex)
- a < 0: **hill** (information decelerating, variance concave)
- Vertex: (t_v, y_v) = (-b/(2a), c - b^2/(4a))
- R^2 = 1 - (SS_res / SS_tot)

### 8.4 The Super Squeeze

Test the variance value and its reciprocal against 35 transcendental constants:

    delta = |test_value - constant|

- delta < 0.01: **NATURAL** (variance locks to universal constant)
- 0.01 <= delta < 0.05: **INVESTIGATE**
- delta >= 0.05 or no match: **FLAG**

The 35 constants include: pi, e, phi, sqrt(2), sqrt(3), sqrt(5), ln(2), ln(10), Euler gamma, Catalan, Apery, Khinchin, Feigenbaum delta, Feigenbaum alpha, Glaisher-Kinkelin, Lambert W(1), Dottie, and their reciprocals, products, and powers. The Euler family (2*pi, e^pi, pi^e, 1/(2*pi), 1/(e^pi), 1/(pi^e)) receives special detection.

### 8.5 The EITT (Entropy Invariance Temporal Test)

Shannon entropy per observation:

    H[i] = -SUM(p[p>0] * ln(p[p>0]))

Normalised: H_norm = H / H_max where H_max = ln(D).

Decimation test: reshape data into blocks, compute geometric mean per block, re-close, recompute entropy. Compression factors: 2x, 4x, 8x.

    Variation = |H_decimated - H_original| / H_original

- Variation < 5%: **PASS** (information invariant under resolution change)
- Variation >= 5%: **FAIL** (resolution is a hidden parameter)

Analytic bound (O-1, proved April 28, 2026):

    |delta_H(M)| <= 0.5 * lambda_max(|HESSIAN_H(mu)|) * Tr(SIGMA_1) * [1 - R(M, rho)]

where R(M, rho) approaches 1 as M increases.

---

## 9. The Diagnostic Code System

### 9.1 Code Format

    SS-CCC-LLL

- SS: Stage (2 characters) — where in the pipeline
- CCC: Condition (3 characters) — what was detected
- LLL: Level (3 characters) — INF (information), WRN (warning), ERR (error), DIS (discovery), CAL (calibration)

### 9.2 Code Groups

| Group | Stage | Count | Function |
|-------|-------|-------|----------|
| GD | Input Guards | 6 | Reject invalid input |
| S4 | Closure | 3 | Zero replacement, closure |
| S5 | CLR | 1 | Transform confirmation |
| S6 | Variance | 3 | Variance range, zero check |
| S7 | HVLD | 5 | Shape, R^2, vertex |
| S8 | Squeeze | 8 | Classification, Euler family |
| S9 | EITT | 9 | Entropy invariance, chaos |
| SA-SC | Geometry | 3 | Ternary, complex, polar |
| XU | Extended Universal | 18 | Per-carrier, drift, CoDa, fingerprint |
| XC | Extended Conditional | 12 | PID, transfer entropy, order, ratios |
| MX | Matrix | 24 | Eigenstructure, impedance, commutators |
| PD | Poincare | 9 | Circularity, hyperbolic, geodesic |
| RP | Report | 3 | Completion, determinism, verification |
| **Total** | | **106** | |

### 9.3 Structural Modes (14)

Structural modes fire when specific combinations of diagnostic codes are present:

| Mode | Code | Condition |
|------|------|-----------|
| Smooth Convergence | SM-SCG-INF | Bowl + EITT pass, no chaos, no flag |
| Bimodal Population | SM-BPO-DIS | Hill + EITT fail + chaos |
| Missing Carrier | SM-MCA-WRN | Flag + zero crossing |
| Domain Resonance | SM-DMR-DIS | Euler family + natural, no flag |
| Carrier Coupling | SM-CPL-DIS | PID redundancy + ratio stability |
| Carrier Independence | SM-IND-DIS | Multiple volatile ratios, no coupling |
| Degenerate Simplex | SM-DGN-WRN | Zero crossing + flag or low R^2 |
| Regime Transition | SM-RTR-DIS | Stalls + reversals + drift |
| Turbulent Natural | SM-TNT-DIS | Natural + EITT fail + chaos |
| Overconstrained | SM-OVC-CAL | High R^2 + natural + EITT pass |
| Frozen Eigenbasis | SM-FRZ-DIS | Eigenvector locked + low entropy + commutator zero |
| Thermal State | SM-THR-WRN | High entropy + low condition + scrambled |
| Matrix Resonance | SM-MXR-DIS | Multiple transcendental matches in eigenvalues |
| Eigenvalue Power | SM-EDP-DIS | Power law R^2 > 0.8 in eigenvalue evolution |

---

## 10. The Poincare Connection

### 10.1 The Cayley Transform

The circularity ratio rho = r_min/r_max from the polar slice IS the Cayley transform:

    C(z) = (1 - z) / (1 + z)

Applied to z = alpha*a where a is the normalised asymmetry and alpha = (1-f)/(1+f).

Properties:
- Involution: C(C(z)) = z (perfectly reversible)
- Fixed point: C(0) = 1 (zero asymmetry = circle)
- Boundary: C(1) = 0 (maximum asymmetry = line)
- Exponential form: C(z) = exp(-2*arctanh(z))

### 10.2 Hyperbolic Distance

    d_H = -ln(rho) = 2*arctanh(alpha*a)

This is the Busemann function in the Poincare disc model. It measures compositional concentration in a geometry where concentrated compositions are exponentially harder to distinguish than diffuse ones.

The Poincare radius:

    r_P = (1 - rho) / (1 + rho)

maps each Higgins Coordinate to the open unit disc.

### 10.3 The Poincare Metric Factor

At Poincare radius r_P:

    Factor = 2 / (1 - r_P^2) = (1 + rho)^2 / (2*rho)

At rho = 0.1 (high asymmetry): factor = 6.05 — the instrument is 6x more sensitive to changes in concentrated compositions. At rho = 0.8 (near-uniform): factor = 2.02 — nearly Euclidean.

### 10.4 Cross-Ratio Invariance

For four compositions with circularity ratios rho_1, rho_2, rho_3, rho_4:

    (rho_1, rho_2; rho_3, rho_4) = [(rho_1-rho_3)(rho_2-rho_4)] / [(rho_1-rho_4)(rho_2-rho_3)]

This cross-ratio is exactly preserved under any change of the projector floor parameter f. The relative asymmetry structure of any dataset is independent of the floor.

### 10.5 What Is and Is Not Hyperbolic

- The Aitchison simplex: **Euclidean** (isometric to R^(D-1) via ILR)
- The full projector: **Euclidean**
- The 1D diagnostic rho: **Hyperbolic** (through the Cayley transform)

The Poincare connection applies to the circularity diagnostic, not to the full D-dimensional coordinate. This is a bounded claim.

### 10.6 Poincare Diagnostic Codes

| Code | Quantity | Range |
|------|----------|-------|
| PD-RHO | Circularity ratio rho | [f, 1] |
| PD-RAD | Poincare radius r_P | [0, alpha] |
| PD-DHY | Hyperbolic distance d_H | [0, infinity) |
| PD-MET | Metric factor | [2, infinity) |
| PD-ZON | Hyperbolic zone | E (<0.3), T (0.3-1.0), H (1.0-2.0), D (>2.0) |
| PD-EFF | Geodesic efficiency | [0, 1] |
| PD-KAP | Geodesic curvature kappa_g | R |
| PD-CRO | Cross-ratio | R (Mobius invariant) |
| PD-BUS | Busemann function ln(rho) | (-infinity, 0] |

---

## 11. The Component Power Mapper

### 11.1 Purpose

Standard CoDa tells you the variance per carrier. The power mapper tells you what happens to the entire instrument reading when you perturb each carrier. These are different questions.

### 11.2 Three Analyses

**Compositional Leverage Index (CLI):** Perturb each carrier by epsilon in both directions, re-close, re-run the full pipeline, measure fingerprint distance vs perturbation size. Leverage = mean(fingerprint_distance / perturbation). Detects asymmetry between removal and addition.

**Phase Boundary Map (PBM):** Sweep each carrier from current value toward zero (scales 1.0 to 0.01) and toward dominance (scales 1.0 to 5.0). Record where the classification flips (NATURAL to FLAG, bowl to hill). Criticality margin = distance to nearest boundary. Phase-sensitive if margin < 0.3.

**Component Power Score (CPS):** Weighted combination — leverage (0.35), criticality (0.30), transfer entropy (0.20), synergy (0.15). Power-to-mass ratio reveals disproportionate influence: a carrier at 1% of the composition driving 30% of the variance.

### 11.3 The Yeast Result

In bread composition, yeast (0.9% by mass) has a power-to-fraction ratio of 33.64x. Removing yeast flips the classification — the composition of bread becomes the composition of brick. The power mapper distinguishes component POWER from component FRACTION.

---

## 12. The Amalgamation Engine

### 12.1 Subcompositional Recursion

For D carriers, generate all possible merges: combine carriers into groups, sum the original values, re-close, re-run the full pipeline. This produces amalgamated systems of dimension D-1, D-2, ..., down to 2.

### 12.2 Classification Persistence

Track which classifications survive amalgamation:

    CLASS(X) = CLASS(AMALG_1(X)) = CLASS(AMALG_2(X)) = ...

In all tested experiments, classification persists through all amalgamation levels — 100% invariance. This means the geometric structure is deep, not an artifact of carrier count.

### 12.3 The Black Hole / White Hole Duality

For each pairwise log-ratio ln(x_i / x_j):

- CV < 0.01 or range < 0.01: **Black hole** (attractor — locked ratio, zero-entropy channel)
- CV >= 0.50 or range > 2.0: **White hole** (repeller — volatile ratio, maximum-entropy channel)
- Between: **Grey zone**

Black holes that persist through all amalgamation levels are deep-structure invariants. In the cosmic energy budget, CDM/Baryon and Photon/Neutrino are deep-structure black holes — their ratios were fixed at the Big Bang and are detected as geometric invariants by the pipeline without physics input.

---

## 13. The EITT Self-Consistency Test

### 13.1 Temporal Decimation

Reshape data into blocks of size M, compute geometric mean per block, re-close, recompute entropy:

    Level 0: X           (N observations)
    Level 1: D_2(X)      (N/2, geometric-mean blocks)
    Level 2: D_4(X)      (N/4)
    Level 3: D_8(X)      (N/8)

    H(X) approx H(D_2(X)) approx H(D_4(X)) approx H(D_8(X))

If information is invariant under observation resolution, the function is self-consistent. If not, resolution is a hidden parameter violating the axiom.

### 13.2 Carrier Decimation

The amalgamation engine performs the same test on carriers:

    Level 0: X           (D carriers)
    Level 1: A_1(X)      (D-1)
    ...
    Level D-2: A_{D-2}(X) (2 carriers)

Both temporal and carrier decimation test the same property: invariance under resolution change.

### 13.3 The Fixed-Point Property

    For all X: Hs(X) = Hs(X)                     (determinism)
    For all X: H(X) approx H(D_k(X))             (temporal invariance)
    For all X: CLASS(X) = CLASS(A(X))             (carrier invariance)

The function is a fixed point of its own decimation. The function, the information, and the classification are all invariant under the operations the function performs.

---

## 14. The Data Integrity Law

### 14.1 Three Laws

**First Law:** The instrument does not fabricate. If the shape does not match expectation, the data contains that structure.

**Second Law:** Every nibble is preserved. No data point is discarded, smoothed, or suppressed. Degenerate and missing markers tag all boundary conditions.

**Third Law:** Confidence is stated. The methodology chain is certifiable to CoDaWork standards. No known misstep exists.

### 14.2 Carrier Lock Points

    LOCK-ACQ = first valid timestep after DEGEN (signal acquisition boundary)
    LOCK-LOSS = last valid timestep before DEGEN (signal loss boundary)
    Offset value: exact CLR spread at boundary (instrument's resolving band)

### 14.3 Reporting Principle

The instrument reports numbers and diagnostic codes. It does not interpret what those numbers mean for the domain. Hs reports descriptive mathematics and process results. Others use governance wording, policy language, or domain-specific interpretation. The instrument is non-toxic by design.

---

## 15. Standard Output

### 15.1 Mandatory Outputs (7)

| Output | Format | Content |
|--------|--------|---------|
| Exploded helix | PDF, 1 page | Bill of materials — 10 pipeline layers |
| Manifold helix | PDF, 1 page | Isometric 3D view of CLR position vectors |
| Projections | PDF, 4 pages | Three cube face projections + polar view |
| Polar stack | PDF, N+2 pages | Per-observation polar slices + composite |
| Manifold paper | PDF, 3 pages | 3D stacked polar slices in projected space |
| Projector | HTML | Interactive 3D radar-polygon viewer |
| Cinema | PPTX | Polar slice slideshow for playback |

### 15.2 Pipeline Runner

    hs_run.py: data in, complete output out

One command produces all mandatory outputs plus JSON data, diagnostic codes, fingerprint, and report in up to 5 languages (en, zh, hi, pt, it).

---

## 16. Tested Domains

The system has been tested across 18 scientific domains:

Commodities (gold/silver), Nuclear physics (SEMF binding energy, AME2020 masses, decay chains), Particle physics (HEP branching ratios), Cosmology (Planck 2018 cosmic energy budget), Materials science (hBN dielectric function), Geochemistry (basalt-rhyolite differentiation), Signal processing (Fourier conjugate pairs), Energy systems (EMBER electricity generation), Engineering (disk drive reliability), Gravitational waves (GW150914), Spring-mass dynamics, Thermodynamic oscillators, Titration chemistry, and calibration standards (cylinder, sphere, cube).

Scale range: 10^-18 m (QCD quarks) to 10^26 m (Hubble radius) — 44 orders of magnitude. All 18 domains produce structurally consistent results.

---

## 17. Notation Summary

| Symbol | Name | Definition |
|--------|------|------------|
| e | Barycentre | (1/D, ..., 1/D) — uniform composition |
| h(t) | Higgins Coordinate | CLR(x(t)) — position vector from barycentre |
| h_j(t) | Component j | ln(x_j) - (1/D)*SUM ln(x_k) |
| ||h(t)||_A | Aitchison norm | sqrt(SUM h_j^2) — distance from barycentre |
| V | Variation matrix | Cov(h) — (D x D) symmetric |
| sigma^2_A | Total variance | Tr(V) = SUM lambda_i |
| lambda_i | Eigenvalues of V | Variance along principal axis i |
| GAMMA | Reflection coefficient | sqrt(1 - lambda_1/Tr(V)) |
| rho(t) | Circularity ratio | r_min/r_max of polar slice |
| alpha | Projector parameter | (1-f)/(1+f), f = floor |
| a(t) | Normalised asymmetry | (r_max-r_min)/(r_max+r_min) |
| r_P(t) | Poincare radius | (1-rho)/(1+rho) |
| d_H(t) | Hyperbolic distance | -ln(rho) = 2*arctanh(alpha*a) |
| H | Shannon entropy | -SUM(p*ln(p)) |
| H_norm | Normalised entropy | H / ln(D) |
| D_k | Temporal decimation | Geometric-mean blocks, factor k |
| A_m | Carrier amalgamation | Merge m carriers, re-close |

---

## 18. The Decomposition as a Whole

    Hs = R . M . E . C . T . V . S

    S = Closure (project onto simplex)
    V = Variance (cumulative sigma^2_A(t) from Higgins Coordinates)
    T = Transform (CLR — produces Higgins Coordinates)
    C = Classification (squeeze against 35 transcendental constants)
    E = Entropy test (EITT geometric-mean decimation)
    M = Mode synthesis (conjunction of diagnostic predicates)
    R = Report (codes + fingerprint + structured output)

Every layer operates on position vectors from the barycentre or on statistics derived from them. No layer requires inter-point connections. The function is pure, deterministic, and self-similar at every level of decomposition.

The formal equation:

    Hs(X) = FIX(lambda f. REPORT(MODES(LATTICE(CLASSIFY(SHAPE(VARIANCE(CLR(CLOSE(GUARD(X))))))))))

where FIX is the fixed-point combinator.

---

## 19. What This System Does

The Higgins Coordinate System answers one question:

    What is invariant about this composition?

It answers by testing invariance at every level:

- **Temporal invariance:** Does entropy survive decimation? (EITT)
- **Carrier invariance:** Does classification survive amalgamation?
- **Ratio invariance:** Which pairwise ratios are constant? (Black holes)
- **Shape invariance:** Does curvature sign survive fitting? (HVLD)
- **Constant invariance:** Does the variance lock to universal reference? (Super Squeeze)
- **Basis invariance:** Does the trace survive coordinate change? (CLR = ILR)

The decomposition is the decimation turned inside out. What it decimates: observations and carriers. What it measures: what survives. What it reports: the invariants.

---

Peter Higgins — Independent Researcher — Markham, Ontario, Canada
Rogue Wave Audio — RWA-001
Hs — The instrument reads. The expert decides. The loop stays open.


---

## Cross-reference — current canonical implementation

The Higgins Coordinate System as specified in this document has matured
into the Compositional Navigation Tensor (CNT) engine. The mapping from
this foundational spec to the current canon:

| Section in this document | Current home |
|---|---|
| §2 The Generating Axiom | [Volume I Part A — Foundations](../HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) |
| §3 The Barycentre | Volume I Part B — Compositional-data foundations |
| §4 The Higgins Coordinate (CLR) | Volume I Part B + Part C |
| §5 The Projection Cube | [`HCI-CNT/atlas/stage1_v4.py`](../HCI-CNT/atlas/stage1_v4.py) (Stage 1 plate) + Volume II Part A |
| §6 The Polar Slice | [`HCI-CNT/atlas/stage2_locked.py`](../HCI-CNT/atlas/stage2_locked.py) (Stage 2 plate book — polar bearing rose) |
| §7 The Tensor Functor | Volume I Part C — The CNT Engine |
| §8 The Pipeline (12 steps) | [`HCI-CNT/engine/cnt.py`](../HCI-CNT/engine/cnt.py) (single deterministic engine) + Volume I Part D pseudocode |
| §8.5 EITT | Cross-dataset EITT lives in Stage 4 ([`HCI-CNT/atlas/stage4_locked.py`](../HCI-CNT/atlas/stage4_locked.py)) |
| §9 Diagnostic Code System | Schema 2.1.0 ([Volume I Part E](../HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md)) + IR taxonomy in `j["depth"]["higgins_extensions"]` |

For the current 25-experiment canonical corpus, see
[`experiments/Hs-CNT_2026-05/`](../experiments/Hs-CNT_2026-05/) (release
snapshot at engine 2.0.4) or [`HCI-CNT/experiments/`](../HCI-CNT/experiments/)
(live working folder).

The instrument reads. The expert decides. The hashes carry the receipts.
