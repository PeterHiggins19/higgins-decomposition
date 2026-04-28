# Character Analysis of the Higgins Decomposition

## Pipeline v3.0 — Hˢ = R ∘ M ∘ E ∘ C ∘ T ∘ V ∘ S

### A Full Functional Diagnostic, Exploded Atomic-Level Disassembly, State Machine Evaluation, and Systems Analysis

**Author:** Peter Higgins
**Affiliation:** Independent Researcher, Markham, Ontario, Canada
**Contact:** PeterHiggins@RogueWaveAudio.com
**Repository:** https://github.com/PeterHiggins19/higgins-decomposition
**Computational Support:** Claude (Anthropic), ChatGPT (OpenAI), Grok (xAI), Gemini (Google), Copilot (Microsoft)
**Date:** April 2026
**Framework Version:** 3.0
**Status:** OPEN TO FURTHER DEVELOPMENT

---

## 1. Scope and Intent

This document treats the Higgins Decomposition pipeline as a Device Under Test (DUT). Every mathematical operation is decomposed to its atomic level — if a decimal point moves, a sign flips, or an index increments, the operation is identified, attributed to its originator, and its effect on data propagation is described.

The analysis is structured as a working-state exploded functional diagnostic: each step is a state in a finite state machine, and every variable is tagged with its type, shape, units, creation point, and consumption points.

This document serves as the foundation for formal verification of pipeline correctness, sensitivity analysis of each atomic operation, identification of all mathematical dependencies and assumptions, and mapping the information-theoretic path from raw measurement to final diagnostic output.

---

## 2. The Decomposition (v3.0)

### 2.1 The Axiom

**Determinism:** Given identical input, the instrument produces identical output. No stochastic element exists at any level.

### 2.2 The Seven Operators

From the determinism axiom, via geometric-mean decimation structure on the Aitchison simplex, seven operators compose into the decomposition function:

**Hˢ = R ∘ M ∘ E ∘ C ∘ T ∘ V ∘ S**

| Operator | Name | Input → Output | Attribution |
|----------|------|----------------|-------------|
| **S** | Simplex closure | ℝ₊ᴺˣᴰ → Sᴰ | Aitchison (1982) |
| **V** | Variance trajectory | Sᴰ → σ²_A(t) | Aitchison (1986) + Higgins (2026) |
| **T** | Transcendental squeeze | σ²_A(t) → proximity vector | Higgins (2026) |
| **C** | Classification | proximity → diagnostic class | Higgins (2026) |
| **E** | Entropy test (EITT) | Sᴰ → invariance certificate | Shannon (1948) + Higgins (2026) |
| **M** | Mode synthesis | all diagnostics → structural mode | Higgins (2026) |
| **R** | Report | structural mode → human-readable output | Higgins (2026) |

Four operators (S, V, partial T, E) are standard CoDa operations built on Aitchison geometry. Three operators (C, M, R) are Higgins contributions. Two operators (T, E) contain open questions for the CoDa community.

### 2.3 The Twelve Steps (Implementation)

The seven operators are implemented as twelve computational steps in `higgins_decomposition_12step.py`:

| Step | State | Operation | Operator | Attribution |
|------|-------|-----------|----------|-------------|
| 1 | S1 | Define system | — | Configuration |
| 2 | S2 | Identify carriers | — | Configuration |
| 3 | S3 | Load data | — | Configuration |
| 4 | S4 | Close to simplex | **S** | Aitchison (1982), Martín-Fernández+ (2003) |
| 5 | S5 | CLR transform | **V** (part 1) | Aitchison (1986) |
| 6 | S6 | Aitchison variance | **V** (part 2) | Aitchison (1986), Higgins (2026) |
| 7 | S7 | HVLD vertex lock | **C** | Higgins (2026) |
| 8 | S8 | Transcendental squeeze | **T** | Higgins (2026) |
| 9 | S9 | EITT entropy test | **E** | Shannon (1948), Higgins (2026) |
| 10 | S10 | Ternary projection | **M** (part 1) | Geometry (standard) |
| 11 | S11 | Complex plane mapping | **M** (part 2) | Euler, Higgins (2026) |
| 12 | S12 | 3D helix/polar | **M** (part 3) | Higgins (2026) |

### 2.4 Extended Panel (Post-Pipeline)

Beyond the 12 core steps, the extended panel adds:

| Module | Function | File |
|--------|----------|------|
| Per-carrier contribution decomposition | Identifies which carrier drives compositional variance | `higgins_decomposition_12step.py` |
| Transfer entropy between carriers | Detects directed information flow (causal direction) | `higgins_decomposition_12step.py` |
| Ratio stability analysis | Identifies locked ratios (CV=0 = conservation law) | `higgins_decomposition_12step.py` |
| Amalgamation stability testing | Tests classification survival under carrier merging | `hs_amalgamation.py` |
| Component Power Mapping | Leverage, phase, power scores per carrier | `hs_sensitivity.py` |
| System fingerprinting | Seven-dimensional compositional signature | `hs_fingerprint.py` |
| Diagnostic code generation | 78 codes + 10 structural modes | `hs_codes.py` |

---

## 3. Pipeline State Machine

### 3.1 Global State Diagram

The pipeline is a linear finite state machine with 12 states (S1–S12) and no branches, loops, or conditional skips. The only conditional logic occurs WITHIN states (zero replacement in S4, D-based dispatch in S10).

```
S1(Define) → S2(Identify) → S3(Load) → S4(Close) → S5(CLR) →
S6(Variance) → S7(HVLD) → S8(Squeeze) → S9(Entropy) → S10(Ternary) →
S11(Complex) → S12(Helix)
```

States S1–S3 are configuration/loading (no math). States S4–S12 are computational.

The data flow has two branches after S4: the "variance branch" (S5→S6→S7→S8) operates on CLR-transformed data, while the "geometry branch" (S9→S10→S11→S12) operates on simplex data. Both branches read from the same simplex closure (S4 output).

### 3.2 State Transition Table

| State | Name | Precondition | Produces | Consumed By |
|-------|------|-------------|----------|-------------|
| S1 | Define System | experiment_id, name, domain, carriers | self.D, self.carriers | S2, S3, all downstream |
| S2 | Identify Carriers | carriers list length = D | D (integer), carrier labels | S4, S10 |
| S3 | Load Data | castable to float64 [N×D] | raw_data, data_hash | S4 |
| S4 | Close to Simplex | raw_data not None; shape[1] == D | simplex_data [N×D] | S5, S9, S10 |
| S5 | CLR Transform | simplex_data not None; all > 0 | clr_data [N×D] | S6, S10 (D>3) |
| S6 | Aitchison Variance | clr_data not None | sigma2_A [N] | S7, S8 |
| S7 | HVLD Vertex Lock | sigma2_A not None; N > 4 | hvld_result (dict) | Output |
| S8 | Super Squeeze | sigma2_A not None | squeeze_result (dict) | Output |
| S9 | EITT Entropy | simplex_data not None | entropy_result (dict) | Output |
| S10 | Ternary Projection | simplex_data not None | ternary_result (dict) | S11 |
| S11 | Complex Plane | ternary_result not None | complex_result (dict) | S12 |
| S12 | 3D Helix/Polar | complex_result not None | helix_result (dict) | Output |

### 3.3 Four Input Guards

Before S4 begins, the pipeline enforces four guards. Any failure produces an explicit rejection with diagnostic message — no silent failures.

| Guard | Condition | Rejection |
|-------|-----------|-----------|
| Dimensionality | D ≥ 2 | "Composition requires at least 2 carriers" |
| Sample size | N ≥ 5 | "Insufficient observations for statistical validity" |
| Data integrity | No NaN or Inf | "Data contains non-finite values" |
| Scale sanity | max/min < 10¹⁵ | "Scale range exceeds pipeline operating envelope" |

---

## 4. The 13 Pipeline Files

### 4.1 File Inventory

| File | Lines | Role | Category |
|------|-------|------|----------|
| `higgins_decomposition_12step.py` | ~1200 | Core 12-step pipeline + extended panel | Core |
| `higgins_transcendental_pretest.py` | ~300 | 35-constant proximity test | Core |
| `hs_amalgamation.py` | ~400 | Subcompositional recursion engine | Core |
| `hs_codes.py` | ~500 | 78 diagnostic codes + 10 structural modes | Diagnostics |
| `hs_fingerprint.py` | ~350 | Seven-dimensional fingerprint + matcher | Diagnostics |
| `hs_sensitivity.py` | ~400 | Component Power Mapper | Diagnostics |
| `hs_metrology.py` | ~300 | Instrument self-evaluation | Diagnostics |
| `hs_ingest.py` | ~250 | Universal CSV/JSON loader | Ingestion |
| `hs_hepdata.py` | ~400 | HEPData fetch + pipeline integration | Ingestion |
| `hs_reporter.py` | ~300 | Multilingual output (5 languages) | Infrastructure |
| `hs_testgen.py` | ~350 | Adversarial + boundary + regression tests | Testing |
| `hs_audit.py` | ~300 | Audit trail + 16 breakpoints | Infrastructure |
| `hs_controller.py` | ~400 | Industrial state machine + Hˢ-GOV supervisor | Infrastructure |

### 4.2 Dependency Graph

```
hs_ingest.py / hs_hepdata.py
        ↓
higgins_decomposition_12step.py  ←  higgins_transcendental_pretest.py
        ↓
   ┌────┼────────────┐
   ↓    ↓            ↓
hs_codes.py  hs_fingerprint.py  hs_sensitivity.py
   ↓         hs_amalgamation.py
hs_reporter.py
   ↓
hs_audit.py → hs_controller.py → hs_metrology.py
```

External dependencies: numpy only. No scipy, no scikit-learn, no TensorFlow. The pipeline is self-contained.

---

## 5. Diagnostic Architecture

### 5.1 The 78 Diagnostic Codes

Codes are structured as three-letter identifiers with severity and domain classification:

| Range | Domain | Count | Examples |
|-------|--------|-------|---------|
| CLR-* | CLR transform diagnostics | 8 | CLR-001 through CLR-008 |
| VAR-* | Variance trajectory | 10 | VAR-001 through VAR-010 |
| HVL-* | HVLD classification | 6 | HVL-001 through HVL-006 |
| SQZ-* | Transcendental squeeze | 12 | SQZ-001 through SQZ-012 |
| ENT-* | Entropy (EITT) | 8 | ENT-001 through ENT-008 |
| TRN-* | Ternary/geometry | 6 | TRN-001 through TRN-006 |
| GEN-* | General/system-level | 10 | GEN-001 through GEN-010 |
| CAR-* | Per-carrier contribution | 8 | CAR-001 through CAR-008 |
| XFR-* | Transfer entropy | 6 | XFR-001 through XFR-006 |
| RAT-* | Ratio stability | 4 | RAT-001 through RAT-004 |
| **Total** | | **78** | |

### 5.2 The 10 Structural Modes

| Mode | Name | Meaning |
|------|------|---------|
| NATURAL | Natural system | All diagnostics consistent with natural composition |
| SYNTHETIC | Synthetic/artificial | Diagnostics indicate engineered or random data |
| TRANSITIONAL | Phase transition | System near boundary between modes |
| OSCILLATORY | Periodic structure | Variance trajectory shows periodic character |
| TURBULENT | Structural turbulence | Stalls, spikes, reversals in variance trajectory |
| LOCKED | Ratio-locked | One or more carrier ratios at CV ≈ 0 |
| HIERARCHICAL | Carrier hierarchy | Extreme separation between dominant and minor carriers |
| DEGENERATE | Near-degenerate | Multiple carriers collapse to similar proportions |
| DIVERGENT | Trajectory divergence | Variance trajectory diverges without bound |
| INDETERMINATE | Classification unclear | Insufficient data or conflicting diagnostics |

### 5.3 The Seven-Dimensional Fingerprint

Each DUT produces a fingerprint vector enabling cross-domain comparison:

| Dimension | What It Captures |
|-----------|-----------------|
| Shape | Variance trajectory curvature (bowl/hill/flat) |
| Fit quality | R² of HVLD parabola fit |
| Classification | HVLD class (NATURAL/SYNTHETIC/TRANSITIONAL/...) |
| Constant family | Which transcendental constant family dominates |
| Entropy stability | EITT variation coefficient |
| Turbulence level | Count and severity of trajectory anomalies |
| Drift direction | Compositional drift vector direction |

Systems sharing a fingerprint share compositional geometry — a structural homology detectable without domain knowledge.

---

## 6. Amalgamation Engine

### 6.1 Purpose

Amalgamation (carrier merging) is used not for data reduction but as a structural diagnostic. By systematically merging carriers and re-running the pipeline, amalgamation tests which features survive regrouping and which vanish inside merged carriers.

### 6.2 Key Results

| Metric | Value |
|--------|-------|
| Total schemes tested | 58 |
| Classification preserved | 58/58 (100%) |
| Datasets tested | 5 (SEMF, Planck, Geochemistry, Energy, Radionuclides) |
| Conservation laws detected | 2 (CDM/Baryon lock, Photon/Neutrino lock in Planck data) |

### 6.3 The Duality Observation

At extreme amalgamation (D→2), compositional systems exhibit black hole / white hole duality: information concentrates into a single dominant carrier (black hole — information absorbed) or disperses into near-equal carriers (white hole — information emitted). The cosmological data shows this transition at amalgamation level 3, where Dark Energy dominance creates a compositional event horizon.

---

## 7. Adversarial Robustness

### 7.1 The Fail-Safe Property

21 adversarial attacks tested. Zero plausible-but-wrong outputs. The pipeline either produces correct diagnostics or fails visibly with explicit error codes.

### 7.2 Attack Surface

| Attack | Pipeline Response |
|--------|------------------|
| All zeros | Guard rejection: "Data contains non-finite values" |
| NaN injection | Guard rejection: "Data contains non-finite values" |
| Extreme scale (10³⁰) | Guard rejection: "Scale range exceeds operating envelope" |
| Constant composition | Runs: correctly classifies as DEGENERATE |
| Binary alternating | Runs: correctly classifies as OSCILLATORY |
| Engineered avoidance (avoid all 35 constants) | Runs: correctly classifies as SYNTHETIC |
| Random walk | Runs: correctly classifies as SYNTHETIC |
| Exponential blowup | Guard rejection or DIVERGENT classification |
| Single carrier dominant (99.99%) | Runs: correctly classifies as HIERARCHICAL |
| Adversarial near-miss (δ < 10⁻⁸ to wrong constant) | Runs: reports correct constant, not nearest |

### 7.3 Diagnostic Consequence

The fail-safe property means: if Hˢ produces a NATURAL classification, the operator can trust it. The instrument does not produce plausible-but-wrong outputs under any tested adversarial condition.

---

## 8. Entropy Invariance (EITT)

### 8.1 The Claim

Shannon entropy computed on the simplex is near-invariant (variation < 5%) when observations are replaced by their pairwise geometric-mean blocks at compression ratios of 2×, 4×, 8×.

### 8.2 Evidence

Tested across all 15 natural systems. Invariance holds for all. Fails only under extreme carrier hierarchy (five or more orders of magnitude between largest and smallest carrier).

### 8.3 Open Question

No formal proof exists. The geometric mean is the natural centre of the Aitchison simplex. The invariance may be a consequence of simplex geometry. This is the most productive question CoDa could answer: if proved, it becomes a theorem of the simplex.

---

## 9. Instrument Metrology

### 9.1 Qualification Status: QUALIFIED

| Metric | Criterion | Result | Status |
|--------|-----------|--------|--------|
| Gauge R&R | Bit-identical on repeat | SHA-256 match | PASS |
| Linearity | Response proportional to input | Verified across 44 orders | PASS |
| Resolution | Minimum detectable δ | 5.87 × 10⁻⁶ demonstrated | PASS |
| Stability | No drift over time | Hash-verified across sessions | PASS |
| Bias | No systematic offset | Reference standards calibrated | PASS |
| Coverage | Domain span | 18 domains, 53 DUTs | PASS |

### 9.2 The Principle of Informational Transparency

An instrument operating within the natural geometry of its input domain (Aitchison geometry for the simplex) that chains sufficient deterministic transformations reads structure without creating or destroying it.

Verified by: conjugate preservation (12/12 bit-identical) and EITT entropy invariance (< 5% at all tested scales).

---

## 10. Experimental Validation Summary

### 10.1 Canonical Counts

| Measure | Count |
|---------|-------|
| Physical domains | 18 |
| Experiments | 25 (Hs-01 through Hs-25) |
| Distinct systems | 36 |
| Devices under test | 53 |
| Pipeline files | 13 |
| Interactive tools | 8 |
| Diagnostic codes | 78 |
| Structural modes | 10 |
| Transcendental constants tested | 35 |
| Conjugate pairs validated | 13 |
| Reference standards | 15 |
| Languages | 5 |

### 10.2 Domain Coverage

| # | Domain | Experiment(s) | Scale |
|---|--------|--------------|-------|
| 1 | Precious metals | Hs-01 | Financial |
| 2 | Energy systems | Hs-02 | National infrastructure |
| 3 | Nuclear physics (binding) | Hs-03, Hs-11 | Femtometre |
| 4 | Acoustics | Hs-04 | Audio band |
| 5 | Geochemistry | Hs-05 | Geological |
| 6 | Nuclear fusion | Hs-06 | Plasma |
| 7 | QCD | Hs-07 | Sub-femtometre |
| 8 | Particle physics | Hs-08, Hs-24 | Electroweak |
| 9 | Stellar physics | Hs-09 | Stellar |
| 10 | Gravitational waves | Hs-10 | Cosmological |
| 11 | Classical mechanics | Hs-12 | Macroscopic |
| 12 | Metallurgy | Hs-13 | Engineering |
| 13 | Mathematics | Hs-14 | Abstract |
| 14 | Materials science | Hs-15 | Nanometre |
| 15 | Cosmology | Hs-16, Hs-25 | Universe |
| 16 | Data engineering | Hs-17 | IT infrastructure |
| 17 | Urban planning | Hs-18, Hs-19 | Municipal |
| 18 | Nuclear decay | Hs-23 | Radioactive chains |

Plus: conversation drift (Hs-20, exploratory), reference standards (Hs-21, calibration), natural pairs (Hs-22, cross-domain).

---

## 11. CoDaWork 2026 Submission

### 11.1 Conference

11th International Workshop on Compositional Data Analysis, Coimbra, Portugal, June 1–5, 2026.

### 11.2 Abstract

Submitted to codawork2026@coda-association.org. 279 words. Preference: oral presentation.

### 11.3 Three Open Questions for CoDa

1. Can the EITT entropy invariance be proved from Aitchison geometry?
2. Does the variance-trajectory classification survive ILR substitution for CLR?
3. Independent validation on CoDa community benchmark datasets.

### 11.4 Deliverables in Repository

Abstract PDF, submission letter, executive summary (tiered claims), strategic agenda, collaboration path, speech (gift ramp format), slide deck (.pptx), action plan, 3 interactive cosmic demos, symbolic logic definition.

---

## 12. Identity Authority

All identity questions resolve to RWA-001 (RWA_Corporate_Reference_v1.0.json):

| Field | Canonical Value |
|-------|----------------|
| Owner | Peter Higgins |
| Company | Rogue Wave Audio |
| Abbreviation | RWA |
| Email | PeterHiggins@RogueWaveAudio.com |
| Location | Markham, Ontario, Canada |
| Repository | github.com/PeterHiggins19/higgins-decomposition |
| Parent repository | github.com/PeterHiggins19/Higgins-Unity-Framework |
| Affiliation (publications) | Independent Researcher |

---

## 13. What This Document Does Not Cover

This Character Analysis is the DUT diagnostic for the pipeline itself. It does not cover: the physics of any particular domain (that belongs to the experiment journals), the governance framework (that belongs to HUF), the commercial applications (that belongs to the Applications Guide), or the formal mathematical proofs (those belong to the theory documents and, ultimately, to the CoDa community).

---

*Hˢ — The instrument reads. The expert decides. The loop stays open.*

*Character Analysis v3.0 — Peter Higgins, April 2026*
*STATUS: OPEN TO FURTHER DEVELOPMENT*
