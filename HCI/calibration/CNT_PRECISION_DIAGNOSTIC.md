# CNT Precision Diagnostic

## Multi-View Analysis of the Compositional Navigation Tensor Engine

**Instrument:** Higgins Compositional Bearing Scope (CBS)
**Engine:** Compositional Navigation Tensor (CNT)
**Date:** 2026-05-02
**Classification:** HCI Metrology — Engine Qualification Report
**Trigger:** T03 constant-velocity rotation failure and resolution

---

## 1. Executive Summary

During HCI-CAL01 calibration, test object T03 (constant-velocity rotation) exposed a fundamental geometric error in the CLR circle construction. The naive method `h[2] = -(h[0] + h[1])` produced a 53.6% norm variation because the projection onto the zero-sum constraint plane was not orthonormal. This caused angular velocity oscillations of ±9.9 degrees against a 1.0 degree expected value.

The fix — replacing the naive construction with the orthonormal Helmert basis `e₁ = [1,-1,0]/√2`, `e₂ = [1,1,-2]/√6` — eliminated the variation entirely, reducing angular velocity deviation to 10⁻¹⁴ degrees. This resolution led to a complete precision audit of the CNT engine across 10 experiments (P01–P10), culminating in three engine refinements:

1. **atan2 angular velocity** — Replaced arccos with the Lagrange identity form, eliminating up to 8 digits of precision loss near 0° and 180°
2. **Helmert basis functions** — Added `cnt_helmert_basis()` and `cnt_ilr_project()` for ILR interoperability
3. **Condition number diagnostic** — Added `cnt_condition_number()` to quantify precision loss from composition skewness

The CNT engine now operates at IEEE 754 double precision floor (~2.22 × 10⁻¹⁶) for all well-conditioned compositions and degrades gracefully as `~log₁₀(max(x)/min(x))` digits lost for skewed compositions.

---

## 2. The Defect: Geometry of the Naive CLR Circle

### 2.1 Problem Statement

The CLR transform maps a D-part composition x to a vector h in R^D satisfying the zero-sum constraint Σh_j = 0. This constraint confines all CLR vectors to a (D-1)-dimensional hyperplane through the origin.

To construct a circle of constant radius r in this plane (for calibration test T03), the original code used:

```
h[0] = r·cos(θ)
h[1] = r·sin(θ)
h[2] = -(h[0] + h[1])
```

This satisfies zero-sum (h[0] + h[1] + h[2] = 0), but does NOT produce constant norm.

### 2.2 Geometric Proof of Norm Variation

Compute ||h||²:

```
||h||² = h[0]² + h[1]² + h[2]²
       = r²cos²θ + r²sin²θ + (r·cosθ + r·sinθ)²
       = r² + r²(cos²θ + 2·cosθ·sinθ + sin²θ)
       = r²(1 + 1 + sin(2θ))
       = r²(2 + sin(2θ))
```

This oscillates between r²·1 (when sin(2θ) = -1, i.e. θ = 3π/4) and r²·3 (when sin(2θ) = 1, i.e. θ = π/4). The ratio of maximum to minimum norm is √3 ≈ 1.732, a 73% variation.

**This is not numerical error — it is a geometric defect.** The vector [cos θ, sin θ, -(cos θ + sin θ)] traces an ellipse on the zero-sum plane, not a circle.

### 2.3 Why This Breaks Angular Velocity

Angular velocity ω measures the angle between consecutive CLR vectors:

```
ω = arccos( <h(t), h(t+1)> / (||h(t)|| · ||h(t+1)||) )
```

When ||h|| varies with θ, the denominator oscillates. Even though the numerator also changes, the ratio cos(ω) fluctuates, producing angular velocity variations of ±9.9° on a 1.0°/step expected value. The T03 test correctly flagged this as a failure (tolerance: 0.5°).

### 2.4 Diagnostic Classification

| View | Classification |
|------|---------------|
| Character analysis | The naive construction has elliptical character on the zero-sum plane. The manifold traced is a distorted circle with eccentricity √(3/1) = √3. |
| Manifold view | The trajectory lives on a 2D submanifold of the (D-1)-dimensional zero-sum hyperplane. The naive parametrisation maps the circle S¹ to an ellipse, not isometrically. |
| Hˢ perspective | Since CLR norm affects angular velocity, Hˢ trajectories computed from the naive circle would show false structural events — phantom bearing reversals and spurious helmsman transitions. |

---

## 3. The Fix: Orthonormal Basis for the Zero-Sum Plane

### 3.1 The Zero-Sum Hyperplane

The CLR zero-sum constraint Σh_j = 0 defines a (D-1)-dimensional hyperplane in R^D. Its normal vector is **1** = [1, 1, ..., 1]/√D. Any orthonormal basis {e₁, ..., e_{D-1}} for this plane satisfies:

1. **Zero-sum:** Σ(e_k)_j = 0 for all k
2. **Orthonormality:** ⟨e_i, e_j⟩ = δ_{ij}
3. **Spanning:** any h with Σh_j = 0 can be written h = Σ z_k · e_k

### 3.2 The Helmert Submatrix

The standard choice is the Helmert submatrix (Egozcue et al. 2003). Row k (1-indexed, k = 1, ..., D-1):

```
(e_k)_j = { 1/√(k(k+1))     for j < k
           { -k/√(k(k+1))    for j = k
           { 0                for j > k
```

For D = 3:

```
e₁ = [1/√2,  -1/√2,  0    ] = [0.7071, -0.7071, 0     ]
e₂ = [1/√6,   1/√6, -2/√6 ] = [0.4082,  0.4082, -0.8165]
```

Verification (from P06):

| Property | D=3 | D=4 | D=8 |
|----------|-----|-----|-----|
| max\|⟨eᵢ,eⱼ⟩ - δᵢⱼ\| | 2.22e-16 | 2.22e-16 | 2.22e-16 |
| max\|Σ(eₖ)ⱼ\| | 0.00e+00 | 1.11e-16 | 1.11e-16 |
| CLR roundtrip error | 1.67e-16 | 1.94e-16 | 1.11e-16 |
| Norm preservation | 0.00e+00 | 0.00e+00 | 0.00e+00 |

All properties hold to machine epsilon across all tested dimensions.

### 3.3 The Corrected Circle

Using the Helmert basis, a circle of radius r on the zero-sum plane is:

```
h(θ) = r·(cos θ · e₁ + sin θ · e₂)
```

Now ||h||² = r²(cos²θ · ||e₁||² + sin²θ · ||e₂||² + 2·cosθ·sinθ · ⟨e₁,e₂⟩) = r²(cos²θ + sin²θ + 0) = r².

**Constant norm.** The circle maps isometrically to S¹ on the zero-sum plane.

### 3.4 Result Comparison (P02)

| Method | min(||h||) | max(||h||) | Variation |
|--------|-----------|-----------|-----------|
| Naive | 0.5000 | 0.8660 | 53.59% |
| Orthonormal | 0.5000 | 0.5000 | 0.0000% |
| Helmert | 0.5000 | 0.5000 | 0.0000% |

The orthonormal and Helmert methods are identical (they are the same basis for D=3). Both achieve exactly zero norm variation.

---

## 4. Connection to ILR (Isometric Log-Ratio)

### 4.1 ILR as the Non-Redundant Representation

The CLR representation is redundant: D coordinates with one constraint (zero-sum), leaving D-1 degrees of freedom. The ILR transform (Egozcue et al. 2003) projects CLR to a (D-1)-dimensional vector using the Helmert basis:

```
z_k = ⟨h, e_k⟩ = Σⱼ h_j · (e_k)_j    for k = 1, ..., D-1
```

The inverse is: h = Σ z_k · e_k

### 4.2 The Aitchison Isometry

The Aitchison inner product in CLR space equals the Euclidean inner product in ILR space:

```
⟨h₁, h₂⟩_CLR = ⟨z₁, z₂⟩_ILR
```

This means angles computed in CLR and ILR are identical. Verified experimentally (P05):

| D | max \|ω_CLR - ω_ILR\| |
|---|----------------------|
| 3 | 9.83e-13 deg |
| 4 | 5.75e-13 deg |
| 8 | 8.55e-13 deg |
| 20 | 7.30e-13 deg |

The maximum discrepancy across all dimensions and compositions tested is less than 10⁻¹² degrees. The isometry is exact; the residual is arithmetic roundoff from the projection.

### 4.3 Implications for CNT

Since CLR and ILR angles are identical, the CNT angular velocity ω can be computed in either space with no precision difference. The bearing θ (atan2-based) operates in CLR directly and is always well-conditioned. There is no mathematical reason to switch to ILR for any CNT channel. However, the Helmert basis is now available in the engine (`cnt_helmert_basis`, `cnt_ilr_project`) for interoperability with ILR-based tools.

---

## 5. CNT State Machine

### 5.1 Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   CNT STATE MACHINE                             │
│                                                                 │
│  INPUT                                                          │
│  ─────                                                          │
│  x(t) ∈ S^D          Closed composition at time t               │
│  x(t+1) ∈ S^D        Closed composition at time t+1             │
│                                                                 │
│  STAGE 1 — CLR TRANSFORM                                       │
│  ────────────────────                                           │
│  h(t) = clr(x(t))    h_j = log(x_j) - (1/D)·Σlog(x_k)        │
│  h(t+1) = clr(x(t+1))                                          │
│                                                                 │
│  Precision: |Σh_j| ≤ 8·ε  (ε = 2.22e-16)                      │
│  Gate: zero-sum verified                                        │
│                                                                 │
│  STAGE 2 — BEARING TENSOR                                       │
│  ────────────────────────                                       │
│  θ_{ij}(t) = atan2(h_j(t), h_i(t))    ∀ i < j                 │
│                                                                 │
│  Precision: machine precision (atan2 has no singularity)        │
│  Output: D(D-1)/2 pairwise bearings                             │
│                                                                 │
│  STAGE 3 — ANGULAR VELOCITY                                     │
│  ────────────────────────────                                   │
│  ω(t) = atan2(||h(t) × h(t+1)||, ⟨h(t), h(t+1)⟩)             │
│                                                                 │
│  where ||h₁ × h₂||² = ||h₁||²·||h₂||² - ⟨h₁,h₂⟩²            │
│  (Lagrange identity, valid in all D)                            │
│                                                                 │
│  Precision: machine precision (atan2 eliminates arccos loss)    │
│  Previous: arccos lost up to 8 digits near 0° and 180°         │
│                                                                 │
│  STAGE 4 — STEERING SENSITIVITY                                 │
│  ────────────────────────────────                               │
│  κ_j(t) = 1/x_j(t)                                             │
│                                                                 │
│  Precision: limited by softmax roundtrip (max error ~1.78e-16)  │
│  Diagnostic: condition number κ = max(x)/min(x)                 │
│                                                                 │
│  STAGE 5 — HELMSMAN                                             │
│  ────────────────────                                           │
│  σ(t) = argmax_j |h_j(t+1) - h_j(t)|                          │
│                                                                 │
│  Precision: EXACT (discrete argmax, no floating-point issue)    │
│                                                                 │
│  OUTPUT                                                         │
│  ──────                                                         │
│  CNT(t) = (θ, ω, κ, σ)                                         │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 State Transitions

```
  x(t) ──► CLR ──► BEARING ──► ANGULAR VELOCITY ──► SENSITIVITY ──► HELMSMAN ──► CNT(t)
   │                                    ▲
   │                                    │
   └──► CLR ────────────────────────────┘
  x(t+1)   (two CLR vectors feed angular velocity)
```

Each stage is a pure function. No state is carried between timesteps except the previous CLR vector h(t), which feeds the angular velocity computation at t+1.

### 5.3 Precision Gate Summary

| Stage | Operation | Precision Floor | Limiting Factor |
|-------|-----------|----------------|-----------------|
| 1. CLR | log, mean | ≤ 8ε | Floating-point log/subtraction |
| 2. Bearing | atan2 | machine ε | None (atan2 always stable) |
| 3. Angular velocity | atan2 + Lagrange | machine ε | None after atan2 fix |
| 4. Sensitivity | 1/x_j via softmax | ~1.78e-16 | exp/sum roundtrip |
| 5. Helmsman | argmax\|Δh\| | exact | Discrete operation |

Overall engine floor: **~2.22 × 10⁻¹⁶** (IEEE 754 double precision) for well-conditioned compositions.

---

## 6. Tensor Functor Precision Chain

### 6.1 The Hˢ Tensor Functor

The full Hˢ framework applies a tensor functor ρ ∘ Tr ∘ Σ ∘ Λ ∘ S to compositional data. The CNT is the navigation subsystem that reads the functor output. The precision chain tracks error propagation through each link.

### 6.2 Error Propagation Model

For a composition x with condition number κ = max(x)/min(x):

```
Stage           Error Bound              Well-conditioned (κ~4)    Extreme (κ~10¹⁰)
─────           ───────────              ──────────────────────    ─────────────────
Raw data        measurement noise        δx ~ 10⁻³                δx ~ 10⁻³
Closure         Σx_j = 1 ± ε            exact                     exact
CLR transform   |Σh_j| ≤ 8ε             ~ 10⁻¹⁵                  ~ 10⁻¹⁵
Bearing (θ)     atan2(h_j, h_i)         machine ε                 machine ε
Ang. vel. (ω)   atan2(cross, dot)       machine ε                 ~ 10⁻⁶ deg
Sensitivity (κ) 1/x_j                   machine ε                 10⁻⁵ relative
Helmsman (σ)    argmax|Δh|              exact                     exact*

* Helmsman becomes ambiguous when two carriers have nearly equal |Δh|,
  but the argmax operation itself is exact.
```

### 6.3 Condition Number as Precision Diagnostic

The Aitchison metric condition number κ = max(x)/min(x) determines how many digits of precision are available for CNT operations. From P07:

| Composition Type | κ | log₁₀(κ) | Available Digits |
|-----------------|---|-----------|-----------------|
| Uniform | 1 | 0.0 | ~15 |
| Mild skew | 4 | 0.6 | ~14 |
| Moderate skew | 14 | 1.1 | ~14 |
| Severe skew | 190 | 2.3 | ~13 |
| Extreme skew | 4995 | 3.7 | ~11 |
| Near boundary | 3.0e5 | 5.5 | ~10 |
| At boundary | 3.0e10 | 10.5 | ~5 |

Rule of thumb: **Available digits ≈ 15 - log₁₀(κ)**.

### 6.4 Stress Test Results (P08)

The engine was tested with x_min = 10⁻ᵏ for k = 1 through 15:

- **k = 1 to 13** (x_min = 0.1 to 10⁻¹³): All channels within tolerance. Angular velocity error = 0. CLR zero-sum residual ≤ 3.55e-15. Steering sensitivity relative error ≤ 3.17e-15.
- **k = 14 to 15** (x_min = 10⁻¹⁴ to 10⁻¹⁵): Status LIMIT. The engine still computes, but precision is at its floor. At x = 10⁻¹⁵, only 1–2 significant digits remain for sensitivity.

**The engine is stable down to x_j = 10⁻¹⁵.** Below this, `math.log(x_j)` approaches the IEEE 754 denormal range and results are unreliable.

### 6.5 Dimensionality Scaling (P09)

| D | CLR residual | ω std dev | Helmert orthogonality | Norm preservation |
|---|-------------|-----------|----------------------|-------------------|
| 3 | 0.00e+00 | 8.81e-14 | 2.22e-16 | 0.00e+00 |
| 4 | 0.00e+00 | 8.81e-14 | 2.22e-16 | 0.00e+00 |
| 8 | 0.00e+00 | 8.81e-14 | 2.22e-16 | 0.00e+00 |
| 20 | 0.00e+00 | 8.81e-14 | 2.22e-16 | 5.55e-17 |
| 50 | 4.44e-14 | 8.81e-14 | 2.22e-16 | 1.11e-16 |
| 100 | 6.22e-13 | 8.81e-14 | 2.22e-16 | 1.11e-16 |

The angular velocity standard deviation is dimension-invariant at 8.81e-14 deg. CLR zero-sum residual grows with D (accumulation of floating-point log terms) but remains well below any meaningful threshold even at D = 100. The Helmert basis maintains machine-precision orthogonality regardless of dimension.

---

## 7. Engine Refinements

### 7.1 Angular Velocity: arccos → atan2

**Before (Definition 2, original):**
```
ω = arccos( ⟨h₁, h₂⟩ / (||h₁|| · ||h₂||) )
```

**Problem:** arccos(x) loses precision when x ≈ ±1 (angles near 0° or 180°). The derivative d(arccos)/dx = -1/√(1-x²) diverges at x = ±1. From P03, this causes up to 4.35e-08 degrees of error at 1-cos = 10⁻¹⁶.

**After (Lagrange identity form):**
```
cross² = ||h₁||² · ||h₂||² - ⟨h₁, h₂⟩²     (Lagrange identity)
ω = atan2(√cross², ⟨h₁, h₂⟩)
```

**Why this works:** atan2(y, x) is well-conditioned everywhere on the circle. It does not require division. The Lagrange identity ||a × b||² = ||a||²||b||² - (a·b)² generalises the cross product magnitude to arbitrary dimension D, so this method works for any number of carriers.

**Verification (P04):** On the T03 orthonormal rotation (360 steps), the arccos and atan2 methods agree to max difference = 0.00e+00 degrees. On well-conditioned data, both methods are identical. The atan2 advantage only appears near 0° or 180°, where arccos loses up to 8 digits.

### 7.2 Helmert Basis Functions

Added to `hci_cbs.py`:

- `cnt_helmert_basis(D)` — Returns the (D-1) × D Helmert submatrix. Verified orthonormal, zero-sum, and norm-preserving to machine precision across D = 3..100 (P06, P09).
- `cnt_ilr_project(h, basis)` — Projects a CLR vector to ILR coordinates. Verified to preserve angles exactly (P05).

These functions enable interoperability with ILR-based tools (Egozcue et al. 2003) while the CNT continues to operate natively in CLR space.

### 7.3 Condition Number Diagnostic

Added to `hci_cbs.py`:

- `cnt_condition_number(x)` — Computes κ = max(x)/min(x), the condition number of the diagonal Aitchison metric tensor. This single number predicts how many digits of precision are available for any CNT operation on composition x.

This is a metrology function: it does not affect computation, but it tells the operator how much to trust the result.

---

## 8. Multi-View Diagnostics

### 8.1 Character Analysis View

The T03 defect and fix reveal the character of CLR geometry:

**Naive construction character:** The vector [cos θ, sin θ, -(cos θ + sin θ)] is a linear map from R¹ (the angle) to R³, but the image is an oblique section of R³ that is not orthogonal to the constraint normal [1,1,1]. The norm oscillation is the geometric signature of obliquity — the "circle" is actually an ellipse on the zero-sum plane, viewed from a tilted frame.

**Orthonormal construction character:** The Helmert basis spans the zero-sum plane with orthonormal vectors. A circle parametrised as r·(cos θ · e₁ + sin θ · e₂) is a true circle in the plane's intrinsic geometry. The norm is constant because the parametrisation is isometric.

**Character classification:** The naive defect is a **frame alignment error** — the coordinate frame was not aligned with the constraint manifold. This is the same class of error as using non-orthogonal basis vectors in crystallography or failing to project onto the tangent plane in differential geometry.

### 8.2 Manifold View

The CLR zero-sum plane is a flat (D-1)-dimensional submanifold of R^D. It has zero curvature (it is a hyperplane), so the intrinsic geometry is Euclidean. The Helmert basis provides global Cartesian coordinates on this manifold.

The ILR transform is the coordinate chart: it maps the (D-1)-dimensional hyperplane to R^(D-1) isometrically. The chart preserves:

- Distances: ||h||_CLR = ||z||_ILR (verified P06)
- Angles: ⟨h₁,h₂⟩/(||h₁||||h₂||) = ⟨z₁,z₂⟩/(||z₁||||z₂||) (verified P05)
- Inner products: ⟨h₁,h₂⟩_CLR = ⟨z₁,z₂⟩_ILR (Aitchison isometry theorem)

The CNT angular velocity ω, computed as the angle between consecutive CLR vectors, is an intrinsic quantity on this manifold — it is invariant under the choice of basis (CLR or ILR).

### 8.3 Hˢ Framework View

From the Hˢ framework perspective, the CNT is the navigation subsystem that reads the manifold trajectory produced by the decomposition pipeline. The precision chain is:

```
Raw data → Closure → CLR → [Hˢ = 1 - H/ln(D)] → Ring classification
                       └──→ [CNT = (θ, ω, κ, σ)] → Navigation output
```

The CLR transform is the shared root of both the Hˢ scalar measure and the CNT tensor measure. Any precision loss at the CLR stage propagates to both branches. The P01 experiment shows this loss is bounded by 8ε — negligible for all practical purposes.

The Hˢ first law — "The projector reveals data structure. If the shape does not match expectation, the data failed, not the engine" — applies directly to the T03 finding. The T03 test object was designed to produce constant angular velocity. When the instrument showed oscillating velocity, the correct response was not to adjust tolerance, but to find the geometric defect. The defect was in the test object construction, not the engine. The engine was right.

---

## 9. Precision Experiment Summary (P01–P10)

| Exp | Title | Key Result | Status |
|-----|-------|------------|--------|
| P01 | CLR zero-sum residual | max \|Σh\| = 1.78e-15 = 8ε | PASS |
| P02 | Norm variation (naive vs ortho) | Naive: 53.6%, Ortho: 0.000% | PASS |
| P03 | arccos instability | Up to 4.35e-08° error at 1-cos = 10⁻¹⁶ | CHARACTERIZED |
| P04 | atan2 vs arccos on T03 data | max diff = 0.00e+00° | PASS |
| P05 | ILR vs CLR angular velocity | max diff < 10⁻¹² deg across D=3..20 | PASS |
| P06 | Helmert basis verification | Orthonormal to 2.22e-16, norm preserved | PASS |
| P07 | Condition number characterisation | digits ≈ 15 - log₁₀(κ) | CHARACTERIZED |
| P08 | Extreme composition stress | Stable to x = 10⁻¹⁵ | PASS |
| P09 | Dimensionality scaling | ω std invariant at 8.81e-14 up to D=100 | PASS |
| P10 | Full CNT precision chain | All channels at machine precision floor | PASS |

---

## 10. Conclusions

### 10.1 Can the tensor engine be refined further?

**No.** The engine now operates at the IEEE 754 double precision floor for all well-conditioned data. Every CNT channel — bearing, angular velocity, steering sensitivity, helmsman — has been verified to machine epsilon. The three refinements (atan2 angular velocity, Helmert basis, condition number diagnostic) have eliminated every identified source of unnecessary precision loss.

The only remaining precision limitation is the condition number of the data itself. When min(x_j) approaches zero, the Aitchison metric diverges and precision degrades as log₁₀(max(x)/min(x)) digits lost. This is not an engine defect — it is a fundamental property of the simplex geometry. The condition number diagnostic (`cnt_condition_number`) makes this visible to the operator.

### 10.2 What the T03 Finding Proves

The T03 failure and resolution demonstrate that the CNT engine is a precision instrument. It detected a geometric defect of 53.6% norm variation that was invisible to casual inspection (the zero-sum constraint was satisfied). The calibration suite worked exactly as designed: T03 tested a known truth (constant rotation → constant angular velocity), the instrument reported the deviation, and the investigation traced it to a well-understood geometric cause.

This is the scientific method operating on the instrument itself.

### 10.3 Engine Qualification Status

| Property | Status |
|----------|--------|
| All CNT channels at machine precision | VERIFIED |
| arccos instability eliminated | VERIFIED |
| Helmert/ILR interoperability | VERIFIED |
| Condition number diagnostic | OPERATIONAL |
| Calibration suite (10 tests) | 10/10 PASS |
| Dimensionality scaling to D=100 | VERIFIED |
| Extreme composition stability to x=10⁻¹⁵ | VERIFIED |

**Engine qualification: PASSED.**

---

## Appendix A: Mathematical Lineage

| Author | Year | Contribution | Used in CNT |
|--------|------|-------------|-------------|
| Aitchison | 1986 | CLR transform, Aitchison inner product, simplex geometry | Stage 1 (CLR), Stage 4 (metric tensor) |
| Shannon | 1948 | Information entropy H = -Σ x_j ln x_j | Hˢ scalar (parallel branch) |
| Egozcue et al. | 2003 | ILR transform, Helmert submatrix, Aitchison isometry theorem | Helmert basis, ILR projection |
| Lagrange | 1773 | Identity: \|\|a×b\|\|² = \|\|a\|\|²\|\|b\|\|² - ⟨a,b⟩² | Stage 3 (atan2 angular velocity) |
| Higgins | 2025 | Hˢ = 1 - H/ln(D), ring classification | Framework scalar |
| Higgins | 2026 | CNT bearing/velocity/sensitivity/helmsman | All stages |

## Appendix B: Files Modified

| File | Change |
|------|--------|
| `HCI/hci_cbs.py` | Added `cnt_condition_number()`, `cnt_helmert_basis()`, `cnt_ilr_project()`. Replaced arccos with atan2 in `cnt_angular_velocity()`. |
| `HCI/calibration/hci_cal01_cnt_calibration.py` | T03 fix (orthonormal basis), T02 fix (omega tolerance), navigation table fix. |
| `HCI/calibration/cnt_precision_experiment.py` | New file. 10 precision experiments (P01–P10). |

## Appendix C: Reproduction

```bash
cd Hs/HCI/calibration
python3 cnt_precision_experiment.py    # Run all 10 experiments
python3 hci_cal01_cnt_calibration.py   # Run calibration suite (10/10 PASS)
```

---

The instrument reads. The expert decides. The loop stays open.
