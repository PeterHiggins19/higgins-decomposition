# Hˢ Pipeline — A Definition in Symbolic Logic
## No Mathematics. Only Logic.

*For fun. — Peter Higgins, 2026*

---

## Primitives

Let the universe of discourse contain:

```
𝒳     — a compositional dataset (a finite collection of observations)
xᵢ    — the i-th observation (a vector of parts)
cⱼ    — the j-th carrier (a named part)
N     — the number of observations
D     — the number of carriers
𝒮     — the simplex (the space where compositions live)
ℝ     — the reals
𝒯     — the set of transcendental constants {2π, e^π, π^e, ...}
ℋ     — Shannon entropy function
σ²    — Aitchison variance function
```

---

## The Four Guards

The pipeline begins with four predicates. All must hold. If any fails, the pipeline halts.

```
G₁(𝒳)  ≡  D ≥ 2
           "The simplex requires at least two parts."

G₂(𝒳)  ≡  N ≥ 5
           "The trajectory requires at least five observations."

G₃(𝒳)  ≡  ∀i ∀j : xᵢⱼ ∈ ℝ ∧ ¬isNaN(xᵢⱼ) ∧ ¬isInf(xᵢⱼ)
           "Every value is a finite real number."

G₄(𝒳)  ≡  max(𝒳) / min(𝒳) < 10¹⁵
           "Scale disparity is bounded."

ADMIT(𝒳) ≡ G₁(𝒳) ∧ G₂(𝒳) ∧ G₃(𝒳) ∧ G₄(𝒳)
```

---

## Step 4: Simplex Closure

```
CLOSED(xᵢ)  ≡  ∀i : Σⱼ xᵢⱼ = 1
                "Every observation sums to unity."

CLOSE(𝒳) → 𝒳' such that CLOSED(𝒳')
            "If the input is not closed, project it onto 𝒮."
```

---

## Step 3 (applied within S4): Zero Replacement

```
ZERO(xᵢⱼ)     ≡  xᵢⱼ = 0
POSITIVE(xᵢⱼ) ≡  xᵢⱼ > 0

REPLACE(𝒳') → 𝒳'' such that ∀i ∀j : POSITIVE(x''ᵢⱼ)
              "Every zero is replaced by a small positive value.
               The result remains on the simplex."

VALID(𝒳'') ≡ CLOSED(𝒳'') ∧ ∀i ∀j : POSITIVE(x''ᵢⱼ)
```

---

## Step 5: CLR Transform

Define the geometric mean of an observation:

```
GM(xᵢ)  — the geometric mean of the D parts of xᵢ

CLR(xᵢⱼ)  ≡  the log-ratio of part j to the geometric mean of observation i

CENTRED(𝒴)  ≡  ∀i : Σⱼ yᵢⱼ = 0
               "In CLR space, every observation sums to zero."

TRANSFORM(𝒳'') → 𝒴 such that CENTRED(𝒴)
```

---

## Step 6: Cumulative Aitchison Variance

```
TRAJECTORY(𝒴) → σ²(t)   for t = 1, 2, ..., N

σ²(t) is a sequence. Define its properties:

INCREASING(σ²)   ≡  σ²(N) > σ²(1)
                    "Variance grows over the observation index."

DECREASING(σ²)   ≡  σ²(N) < σ²(1)
                    "Variance shrinks."

NONDEGENERATE(σ²) ≡  ∃t : σ²(t) ≠ σ²(1)
                     "The trajectory is not flat."
```

---

## Step 7: HVLD Vertex Lock Diagnostic

Fit a quadratic to the variance trajectory. The quadratic has a coefficient `a`, a fit quality `R²`, and a vertex location `v`.

```
BOWL(σ²)  ≡  a > 0
             "Variance is accelerating. The system is integrating."

HILL(σ²)  ≡  a < 0
             "Variance is decelerating. The system is segregating."

STRONG_FIT(σ²)  ≡  R² > 0.8
                   "The quadratic describes the trajectory well."

WEAK_FIT(σ²)    ≡  R² < 0.5
                   "The trajectory is not well-described by a quadratic."

SHAPE(σ²) ≡ BOWL(σ²) ∨ HILL(σ²)
```

---

## Step 8: Transcendental Squeeze (Super Squeeze)

```
Let δ(σ², κ) denote the proximity of the variance trajectory
to transcendental constant κ ∈ 𝒯.

MATCH(σ², κ)     ≡  δ(σ², κ) < 0.01
                    "Proximity within 1%."

TIGHT(σ², κ)     ≡  δ(σ², κ) < 0.001
                    "Precision-level proximity."

NATURAL(𝒳)       ≡  ∃κ ∈ 𝒯 : MATCH(σ², κ)
                    "At least one transcendental constant is matched."

INVESTIGATE(𝒳)   ≡  ¬NATURAL(𝒳) ∧ ∃κ ∈ 𝒯 : δ(σ², κ) < 0.05
                    "No tight match, but proximity within 5%."

FLAG(𝒳)          ≡  ¬NATURAL(𝒳) ∧ ¬INVESTIGATE(𝒳)
                    "No match within 5%."

EULER(κ)         ≡  κ ∈ {2π, eᵖⁱ, πᵉ, 1/(eᵖⁱ), 1/(πᵉ), ...}
                    "The matched constant belongs to the Euler family."

CLASSIFICATION(𝒳) ≡ NATURAL(𝒳) ∨ INVESTIGATE(𝒳) ∨ FLAG(𝒳)
                    "Every dataset receives exactly one classification."

                    — this is an exhaustive partition:
                    NATURAL(𝒳) ⊕ INVESTIGATE(𝒳) ⊕ FLAG(𝒳)
                    (exclusive or — exactly one is true)
```

---

## Step 9: EITT Entropy Invariance

```
Let ℋ(𝒳) denote Shannon entropy of the compositional dataset.
Let 𝒟ₖ(𝒳) denote geometric-mean decimation at compression ratio k.

PRESERVED(𝒳, k)  ≡  |ℋ(𝒟ₖ(𝒳)) − ℋ(𝒳)| / ℋ(𝒳) < 0.05
                    "Entropy variation under k-fold decimation is less than 5%."

EITT_PASS(𝒳)     ≡  PRESERVED(𝒳, 2) ∧ PRESERVED(𝒳, 4) ∧ PRESERVED(𝒳, 8)
                    "Entropy is invariant at all tested compression ratios."

EITT_FAIL(𝒳)     ≡  ¬EITT_PASS(𝒳)
```

Define chaos indicators on the entropy trajectory:

```
Let ω(t) denote the angular velocity of the entropy trajectory.
Let μ_ω denote the running mean of ω.

STALL(t)     ≡  ω(t) < 0.15 · μ_ω
                "Entropy rate dropped below 15% of running mean."

SPIKE(t)     ≡  ω(t) > 3.5 · μ_ω
                "Entropy rate exceeded 3.5× running mean."

REVERSAL(t)  ≡  ∃ consecutive window of 5 samples with ≥ 2 sign changes in ω
                "Rapid compositional oscillation."

TURBULENT(𝒳) ≡  (#{t : STALL(t)} > 3) ∨ (#{t : SPIKE(t)} > 3) ∨ (#{t : REVERSAL(t)} > 0)
                "The system exhibits compositional turbulence."

SMOOTH(𝒳)    ≡  ¬TURBULENT(𝒳)
```

---

## Step 10: Ratio-Pair Lattice

```
For all carrier pairs (cⱼ, cₖ) where j < k, define:

RATIO(cⱼ, cₖ)    — the log-ratio ln(xⱼ/xₖ) across all observations
CV(cⱼ, cₖ)       — the coefficient of variation of RATIO(cⱼ, cₖ)

LOCKED(cⱼ, cₖ)   ≡  CV(cⱼ, cₖ) < 0.01
                     "The ratio is essentially constant. These carriers are coupled."

STABLE(cⱼ, cₖ)   ≡  CV(cⱼ, cₖ) < 0.20 ∧ ¬LOCKED(cⱼ, cₖ)
                     "The ratio varies but within a tight band."

VOLATILE(cⱼ, cₖ) ≡  CV(cⱼ, cₖ) > 0.50
                     "The ratio is unconstrained. These carriers are independent."

                     — partition of all pairs into stability classes:
LATTICE(𝒳) ≡ ∀j<k : LOCKED(cⱼ,cₖ) ⊕ STABLE(cⱼ,cₖ) ⊕ VOLATILE(cⱼ,cₖ) ⊕ MODERATE(cⱼ,cₖ)
```

---

## Step 11: Transfer Entropy

```
TE(cⱼ → cₖ)   — directed information flow from carrier j to carrier k

FLOW(cⱼ, cₖ)    ≡  TE(cⱼ → cₖ) > threshold
                    "Carrier j informationally predicts carrier k."

MEMORYLESS(𝒳)   ≡  ∀j ∀k : TE(cⱼ → cₖ) = 0
                    "No carrier predicts any other. System is compositionally memoryless."

DIRECTED(𝒳)     ≡  ∃j ∃k : FLOW(cⱼ, cₖ) ∧ ¬FLOW(cₖ, cⱼ)
                    "There exists asymmetric information flow."
```

---

## Step 12: Fingerprint

```
FINGERPRINT(𝒳) ≡ ⟨ SHAPE(σ²),
                    R²_BAND(σ²),
                    CLASSIFICATION(𝒳),
                    CONSTANT_FAMILY(𝒳),
                    EITT_PASS(𝒳),
                    TURBULENT(𝒳),
                    DRIFT_DIRECTION(𝒳) ⟩

                "A 7-dimensional identity vector.
                 Two systems with similar fingerprints share
                 compositional geometry regardless of domain."

SIMILAR(𝒳₁, 𝒳₂)  ≡  FINGERPRINT(𝒳₁) = FINGERPRINT(𝒳₂)
                     "Same shape. Same family. Same behaviour."
```

---

## Extended Panel: Per-Carrier Contribution

```
CONTRIBUTION(cⱼ, 𝒳)  — fraction of total variance attributable to carrier j

DOMINANT(cⱼ, 𝒳)  ≡  CONTRIBUTION(cⱼ, 𝒳) > 0.60
                     "One carrier contributes more than 60% of variance."

∀𝒳 : ∃!cⱼ : DOMINANT(cⱼ, 𝒳) ∨ ¬∃cⱼ : DOMINANT(cⱼ, 𝒳)
     "At most one carrier is dominant."
```

---

## Extended Panel: Drift

```
DRIFT(𝒳)      — comparison of first half to second half composition

EVOLVING(𝒳)   ≡  second half is more dispersed than first half
CONVERGING(𝒳) ≡  second half is more concentrated than first half
STATIONARY(𝒳) ≡  ¬EVOLVING(𝒳) ∧ ¬CONVERGING(𝒳)
```

---

## Extended Panel: Component Power

```
POWER(cⱼ, 𝒳)     — influence of carrier j on system classification
FRACTION(cⱼ, 𝒳)  — mass fraction of carrier j

DISPROPORTIONATE(cⱼ, 𝒳)  ≡  POWER(cⱼ, 𝒳) / FRACTION(cⱼ, 𝒳) > 2.0
                             "Influence exceeds fraction by more than 2×."

RANK_MISMATCH(𝒳)  ≡  ∃j ∃k : FRACTION(cⱼ) > FRACTION(cₖ) ∧ POWER(cⱼ) < POWER(cₖ)
                     "Power ranking differs from mass ranking."
```

---

## T2: Subcompositional Recursion

```
AMALGAMATION(𝒜)  — a partition of {c₁, ..., c_D} into groups
                   where at least one group contains ≥ 2 carriers
                   and the result has < D carriers

Let 𝔸(𝒳) = the set of all non-trivial amalgamation schemes.
|𝔸| = 2^D − D − 1 for D carriers.

AMALGAMATE(𝒳, 𝒜) → 𝒳_𝒜  "Apply scheme 𝒜 to produce a reduced composition."

PRESERVES(𝒳, 𝒜)  ≡  CLASSIFICATION(𝒳_𝒜) = CLASSIFICATION(𝒳)
                     "The classification survives this regrouping."

ROBUST(𝒳)        ≡  ∀𝒜 ∈ 𝔸(𝒳) : PRESERVES(𝒳, 𝒜)
                     "Classification is invariant under all amalgamations."
```

---

## T2: Black Hole / White Hole Duality

```
BLACK_HOLE(cⱼ, cₖ)  ≡  LOCKED(cⱼ, cₖ)
                        "Zero-entropy channel. The ratio never changes.
                         No information transmitted. Structural attractor."

WHITE_HOLE(cⱼ, cₖ)  ≡  VOLATILE(cⱼ, cₖ)
                        "Maximum-entropy channel. The ratio is unconstrained.
                         Maximum uncertainty. Structural repeller."

INVISIBLE(cⱼ, cₖ, 𝒜)  ≡  BLACK_HOLE(cⱼ, cₖ) ∧ ∃G ∈ 𝒜 : cⱼ ∈ G ∧ cₖ ∈ G
                           "The lock exists but is hidden inside a merged group.
                            From outside the group, it cannot be observed."

DEEP(cⱼ, cₖ)  ≡  BLACK_HOLE(cⱼ, cₖ) ∧ ∀𝒜 ∈ 𝔸 :
                   (cⱼ ∈ G ∧ cₖ ∈ G for some G ∈ 𝒜)
                   → LOCKED_WITHIN(cⱼ, cₖ, 𝒜)
                  "The lock survives inside every amalgamation that contains both carriers.
                   This is deep structure — it never vanishes."

DUALITY(cⱼ, cₖ, cₘ)  ≡  BLACK_HOLE(cⱼ, cₖ) ∧ WHITE_HOLE(cⱼ, cₘ)
                          "Carrier j is locked with k but independent of m.
                           The attractor for one pair is the repeller context for another."
```

---

## Structural Modes

Structural modes are compound predicates — combinations of simpler predicates that identify investigation-worthy patterns:

```
SMOOTH_CONVERGENCE(𝒳)  ≡  BOWL(σ²) ∧ SMOOTH(𝒳) ∧ EITT_PASS(𝒳)
                          "Single population evolving continuously."

BIMODAL(𝒳)             ≡  HILL(σ²) ∧ TURBULENT(𝒳) ∧ EITT_FAIL(𝒳)
                          "Two distinct populations mixed on the simplex."

REGIME_TRANSITION(𝒳)   ≡  EVOLVING(𝒳) ∧ (#{t : STALL(t)} > 0)
                          "System transitions between compositional states.
                           Stalls mark boundaries."

CARRIER_COUPLING(𝒳)    ≡  ∃j ∃k : LOCKED(cⱼ, cₖ)
                          "At least one ratio pair is locked.
                           A conservation law or stoichiometric constraint."

CARRIER_INDEPENDENCE(𝒳) ≡ ∀j ∀k (j≠k) : VOLATILE(cⱼ, cₖ)
                          "Every ratio pair is volatile.
                           Each carrier is governed by a separate mechanism."

DOMAIN_RESONANCE(𝒳)    ≡  NATURAL(𝒳) ∧ EULER(κ*) ∧ STRONG_FIT(σ²)
                          where κ* is the matched constant
                          "Euler-family geometry encodes deep structure."

OVERCONSTRAINED(𝒳)     ≡  NATURAL(𝒳) ∧ R² > 0.99
                          "Near-perfect fit. Verify this is measured data, not model output."

MISSING_CARRIER(𝒳)     ≡  FLAG(𝒳) ∧ (∃j : ∃t : xⱼ(t) → 0)
                          "Energy or information is leaking to an untracked carrier."

TURBULENT_NATURAL(𝒳)   ≡  NATURAL(𝒳) ∧ TURBULENT(𝒳) ∧ EITT_FAIL(𝒳)
                          "The turbulence is structural, not noise."
```

---

## The Complete Pipeline as a Single Logical Sentence

```
Hˢ(𝒳) ≡

  ADMIT(𝒳)                                          — gates open

  → VALID(REPLACE(CLOSE(𝒳)))                        — on the simplex, all positive

  → CENTRED(TRANSFORM(𝒳''))                         — in CLR space

  → NONDEGENERATE(TRAJECTORY(𝒴))                    — variance trajectory exists

  → SHAPE(σ²) ∧ (STRONG_FIT(σ²) ∨ WEAK_FIT(σ²))   — shape classified

  → CLASSIFICATION(𝒳)                               — NATURAL ∨ INVESTIGATE ∨ FLAG

  → EITT_PASS(𝒳) ∨ EITT_FAIL(𝒳)                   — entropy invariance tested

  → LATTICE(𝒳)                                      — all ratio pairs ranked

  → FINGERPRINT(𝒳)                                  — geometric identity assigned

  → (ROBUST(𝒳) ∨ ¬ROBUST(𝒳))                       — amalgamation stability tested

  → ⋃ { MODE(𝒳) : MODE ∈ STRUCTURAL_MODES }        — investigation prompts emitted

  → DETERMINISTIC                                    — same input, same output, always
```

---

## Properties of the Logical System

**Decidability.** Every predicate in the system is decidable for any finite compositional dataset. There are no undecidable propositions. Given 𝒳, the pipeline terminates and every predicate resolves to TRUE or FALSE.

**Exhaustiveness.** The classification is an exhaustive partition: every dataset is NATURAL ⊕ INVESTIGATE ⊕ FLAG. No dataset is unclassified (unless the guards reject it, in which case it is outside the domain).

**Monotonicity of information.** Each step adds information; no step destroys the output of a previous step. The fingerprint at step 12 contains the outputs of all prior steps. This is a monotonically increasing information chain.

**Determinism.** ∀𝒳 : Hˢ(𝒳) = Hˢ(𝒳). Same input, same output. The pipeline is a pure function from compositional datasets to diagnostic readings. No randomness. No state. No side effects.

**Compositionality of the logic itself.** The structural modes are composed from simpler predicates. The pipeline is composed from sequential steps. The amalgamation recursion composes smaller analyses into a persistence map. The logic of Hˢ is itself compositional — parts combining to form wholes, each readable independently, together forming a complete diagnosis.

---

## What the Logic Reveals

By stripping away the arithmetic and leaving only the logical structure, several things become visible:

**The pipeline is a chain of implications.** Each step implies the next. The guards imply validity. Validity implies the transform is possible. The transform implies the trajectory exists. The trajectory implies a shape. The shape implies a classification. The classification implies a fingerprint. The fingerprint implies comparability.

**The structural modes are emergent.** They are not separate computations — they are logical consequences of the simpler predicates. SMOOTH_CONVERGENCE is not measured; it is deduced from BOWL ∧ SMOOTH ∧ EITT_PASS. The ten modes are ten patterns that emerge from the interaction of approximately thirty atomic predicates.

**The duality is a logical complementarity.** BLACK_HOLE and WHITE_HOLE are not opposites in a numerical sense — they are complementary logical states of the same relation (the ratio pair). One is the zero of the information channel. The other is the maximum. Between them lies the full spectrum of coupling. The duality is not in the numbers. It is in the logic.

**Determinism is a logical property, not a numerical one.** The pipeline is deterministic not because the arithmetic is precise, but because every predicate is a pure function. ∀𝒳 : Hˢ(𝒳) = Hˢ(𝒳) is a statement about the logical structure, not about floating-point precision. The SHA-256 hash is a numerical *verification* of a logical *truth*.

---

*The entire Hˢ pipeline is thirty-one predicates, ten structural modes, four guards, and one chain of implications. The rest is arithmetic.*

*Peter Higgins, 2026*
