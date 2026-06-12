# Hs-LAB01: Titration Standards — Chemistry Calibration

*Author: Peter Higgins*
*Date: 2026-04-30*
*Domain: CHEMISTRY*
*Series: LAB-series (Laboratory Calibration Experiments)*

## 1. Purpose

This experiment calibrates the Hˢ instrument for chemical compositional analysis using three standard polyprotic acid titrations. Titration is the prototypical compositional process in chemistry: as the pH changes, species fractions (alpha values) redistribute on the simplex according to equilibrium constants. The system is fully determined by the acid dissociation constants (pKa), and the species fractions can be calculated exactly from closed-form expressions. This provides a rigorous calibration target with known ground truth at every point.

The three systems were chosen to span different pKa spacings and dimensionalities, providing a comprehensive chemistry calibration:

- **Phosphoric acid** (H₃PO₄): widely spaced pKa values (2.15, 7.20, 12.38) — well-resolved transitions, 4-part simplex
- **Citric acid** (H₃Cit): closely spaced pKa values (3.13, 4.76, 6.40) — overlapping equilibria, 4-part simplex
- **Carbonic acid** (H₂CO₃): two-step system (6.35, 10.33) — the ocean/blood pH buffer, 3-part simplex

This is the first Hˢ experiment in the LAB-series, designed to establish the instrument's capability for laboratory chemical research.

## 2. Data Source

### 2.1 Generation Method

Species fractions (alpha values) were computed from the exact closed-form expression for polyprotic acid equilibria:

For an n-protic acid with dissociation constants Ka₁, Ka₂, ..., Kaₙ, the fraction of the i-th species at a given [H⁺] is:

α₀ = [H⁺]ⁿ / D, α₁ = Ka₁·[H⁺]ⁿ⁻¹ / D, α₂ = Ka₁·Ka₂·[H⁺]ⁿ⁻² / D, ..., αₙ = Ka₁·Ka₂·...·Kaₙ / D

where D = [H⁺]ⁿ + Ka₁·[H⁺]ⁿ⁻¹ + Ka₁·Ka₂·[H⁺]ⁿ⁻² + ... + Ka₁·Ka₂·...·Kaₙ

This is not an approximation — it is the analytically exact solution of the equilibrium equations. The alpha values sum to exactly 1.0 at every pH (verified to machine precision: max deviation < 2.22 × 10⁻¹⁶).

### 2.2 pKa Values

| System | pKa₁ | pKa₂ | pKa₃ | Source |
|--------|-------|-------|-------|--------|
| H₃PO₄ | 2.148 | 7.198 | 12.375 | NIST Critical Stability Constants (25°C, I→0) |
| H₃Cit | 3.13 | 4.76 | 6.40 | CRC Handbook of Chemistry and Physics |
| H₂CO₃ | 6.35 | 10.33 | — | Apparent (includes CO₂(aq) equilibrium, 25°C) |

### 2.3 Carriers

**Phosphoric acid:** H₃PO₄ (fully protonated), H₂PO₄⁻ (dihydrogen phosphate), HPO₄²⁻ (hydrogen phosphate), PO₄³⁻ (phosphate)

**Citric acid:** H₃Cit (fully protonated), H₂Cit⁻ (dihydrogen citrate), HCit²⁻ (hydrogen citrate), Cit³⁻ (citrate)

**Carbonic acid:** H₂CO₃ (carbonic acid / dissolved CO₂), HCO₃⁻ (bicarbonate), CO₃²⁻ (carbonate)

## 3. System Parameters

| Parameter | H₃PO₄ | H₃Cit | H₂CO₃ |
|-----------|--------|--------|--------|
| N (pH points) | 200 | 200 | 200 |
| D (species) | 4 | 4 | 3 |
| pH range | 0.5–14.0 | 1.0–10.0 | 3.0–13.0 |
| Closure deviation | < 2.22e-16 | < 3.33e-16 | < 2.22e-16 |
| Zero replacement | Yes (structural zeros at pH extremes) | Yes | Yes |
| Data hash (SHA-256/16) | ba3349752b312208 | (see index) | (see index) |

## 4. Method

Each dataset was processed through the full Hˢ pipeline (v1.0 Extended) via `hs_run.py`, producing all 5 mandatory projection PDFs plus the results JSON and diagnostic report. The pipeline is deterministic — repeated runs produce bit-identical output.

The titration data represents a compositional trajectory on the D-part simplex, parameterised by pH. As pH increases (simulating NaOH addition), the composition smoothly traverses from the fully protonated vertex through intermediate forms to the fully deprotonated vertex. This is geometrically a path on the simplex, and the pipeline decomposes its variance structure, entropy trajectory, and compositional dynamics.

## 5. Results

### 5.1 Phosphoric Acid (H₃PO₄)

| Metric | Value |
|--------|-------|
| Total variance | 137.7610 |
| HVLD shape | bowl |
| HVLD R² | 0.9863 |
| Entropy mean | 0.2221 |
| Entropy CV | 73.30% |
| Squeeze count | 35 |
| Diagnostic codes | 59 (0 errors, 3 warnings, 16 discoveries) |
| Structural modes | 5 |
| Chaos (stalls/spikes/reversals) | 0/0/0 |
| EITT | PASS (all compressions) |

**Notable findings:**

The pipeline detects **SM-OVC-CAL** (overconstrained) — correctly identifying this as model-derived data rather than measured data. The near-perfect HVLD R² = 0.9863 and zero chaos signature are consistent with exact equilibrium chemistry.

All six pairwise log-ratios are classified as **volatile** (CV > 33 for all pairs). This is chemically correct: no two species maintain a constant ratio across the full pH range. Each pair is governed by a different combination of Ka values.

**Transfer entropy is zero across all 12 directed pairs.** This is the correct physical result: equilibrium chemistry is memoryless. The composition at any pH depends only on the pKa values and the current [H⁺], not on the pH history.

The condition number is extremely high (4.9 × 10¹⁵), reflecting the span of ~14 orders of magnitude in [H⁺] across the pH range.

### 5.2 Citric Acid (H₃Cit)

| Metric | Value |
|--------|-------|
| Total variance | 121.3381 |
| HVLD shape | bowl |
| HVLD R² | 0.9732 |
| Entropy mean | 0.3096 |
| Entropy CV | 71.88% |
| Squeeze count | 40 |
| Diagnostic codes | 55 (0 errors, 2 warnings, 14 discoveries) |
| Structural modes | 5 |
| Chaos (stalls/spikes/reversals) | 0/0/0 |
| EITT | PASS (all compressions) |

**Notable findings:**

Citric acid has the highest entropy mean (0.3096) of the three systems. This is chemically meaningful: with closely spaced pKa values (only 1.63 and 1.64 pH units apart), multiple species coexist across a wide pH range, producing higher compositional mixing.

The HVLD R² (0.9732) is lower than phosphoric acid's (0.9863). This reflects the overlapping equilibria: the variance trajectory has a smoother shape because the transitions between species are not as sharply resolved.

The pipeline correctly identifies drift as **decreasing** with Cit³⁻ (the fully deprotonated form) as the maximum shift carrier. This is consistent with the pH range ending at 10.0, where the citrate ion increasingly dominates.

### 5.3 Carbonic Acid (H₂CO₃)

| Metric | Value |
|--------|-------|
| Total variance | 85.8308 |
| HVLD shape | bowl |
| HVLD R² | 0.9951 |
| Entropy mean | 0.2576 |
| Entropy CV | 81.16% |
| Squeeze count | 59 |
| Diagnostic codes | 54 (0 errors, 2 warnings, 14 discoveries) |
| Structural modes | 5 |
| Chaos (stalls/spikes/reversals) | 0/0/0 |
| EITT | PASS (all compressions) |

**Notable findings:**

Carbonic acid produces the highest HVLD R² (0.9951) of the three systems. With only D=3, the compositional trajectory lives on a 2-simplex (triangle), and the variance trajectory is exceptionally well-fit by the parabolic model.

The EITT compression variation is the lowest of all three (0.0004% at 2× compression). This is consistent with the smooth, two-step equilibrium of the carbonate system.

The pipeline identifies drift as **increasing** with H₂CO₃ as the maximum shift carrier, reflecting the dominance reversal as pH increases from the carbonic acid vertex toward the carbonate vertex.

### 5.4 Cross-System Comparison

| System | D | Total Var | R² | Entropy Mean | Entropy CV | Squeeze | Condition No. |
|--------|---|-----------|-----|-------------|-----------|---------|---------------|
| H₃PO₄ | 4 | 137.76 | 0.9863 | 0.2221 | 73.30% | 35 | 4.9 × 10¹⁵ |
| H₃Cit | 4 | 121.34 | 0.9732 | 0.3096 | 71.88% | 40 | 158.8 |
| H₂CO₃ | 3 | 85.83 | 0.9951 | 0.2576 | 81.16% | 59 | 245.1 |

**Observations:**

The total variance decreases with D (and with the range of [H⁺] covered), as expected: fewer species means fewer log-ratio degrees of freedom.

The entropy CV is consistently high (71–81%) across all three systems. This reflects the titration trajectory: entropy is low at the extremes (single species dominates) and peaks in the buffer regions where multiple species coexist. The high CV is the compositional signature of sequential proton transfer.

All three systems share the same structural mode signature: SM-OVC-CAL, SM-DMR-DIS, SM-SCG-INF, SM-MXR-DIS, SM-EDP-DIS. The overconstrained signal (SM-OVC-CAL) correctly identifies all three as model-derived rather than measured data. The smooth convergence signal (SM-SCG-INF) correctly identifies the equilibrium trajectory as a single population evolving continuously.

## 6. Conclusions

### 6.1 Instrument Performance

The Hˢ pipeline correctly processes titration compositional data and produces chemically interpretable results:

1. **SM-OVC-CAL detection** correctly distinguishes exact equilibrium calculations from noisy measured data. When real titration data is measured in the lab (with electrode noise, temperature fluctuations, dilution effects), this flag should disappear — providing a direct quality metric for experimental technique.

2. **Zero chaos** (no stalls, spikes, or reversals) confirms the pipeline correctly reads smooth, monotonic compositional trajectories.

3. **Zero transfer entropy** confirms the pipeline correctly identifies equilibrium systems as memoryless.

4. **Volatile pairwise ratios** for all carrier pairs confirm the pipeline correctly identifies that no two species maintain a constant ratio across the full titration — consistent with the mathematics of polyprotic equilibria.

5. **EITT PASS** at all compression levels confirms the compositional information is scale-invariant — the equilibrium curve sampled at 200 points contains the same information as 25 points.

### 6.2 Chemistry Calibration Targets

These three titrations establish chemistry-specific calibration benchmarks:

- **Noise-free reference:** Any lab titration run through Hˢ can be compared against these exact equilibrium benchmarks. The difference reveals measurement quality.
- **pKa spacing effects:** Phosphoric acid (widely spaced) versus citric acid (closely spaced) shows how pKa separation affects the HVLD R², entropy mean, and condition number.
- **Dimensionality baseline:** Carbonic acid (D=3) versus the triprotic acids (D=4) provides a cross-dimensional reference within the same chemical framework.

### 6.3 Implications for Laboratory Use

When a researcher titrates a real acid sample and runs the data through Hˢ:

- If SM-OVC-CAL disappears, the data contains real measurement noise — the instrument is reading experimental variation.
- If chaos counts increase from zero, the titration has non-equilibrium features (electrode lag, CO₂ absorption, precipitation).
- If transfer entropy becomes nonzero, there are hysteresis or kinetic effects — the system has memory.
- If EITT fails, the compositional information is scale-dependent — the measurement interval matters.

Each of these is a direct, quantitative quality signal for the experimental chemist.

## 7. Reproducibility

### Run commands

```bash
cd tools/pipeline

# Phosphoric acid
python hs_run.py ../../experiments/Hs-LAB01_Titration_Standards/data/phosphoric_acid_titration.csv \
  --exp-id "Hs-LAB01-H3PO4" --name "Phosphoric Acid Titration" --domain CHEMISTRY

# Citric acid
python hs_run.py ../../experiments/Hs-LAB01_Titration_Standards/data/citric_acid_titration.csv \
  --exp-id "Hs-LAB01-CITRIC" --name "Citric Acid Titration" --domain CHEMISTRY

# Carbonic acid
python hs_run.py ../../experiments/Hs-LAB01_Titration_Standards/data/carbonic_acid_titration.csv \
  --exp-id "Hs-LAB01-H2CO3" --name "Carbonic Acid Titration" --domain CHEMISTRY
```

### Data generation

The titration datasets are generated by `titration_generator.py` in the experiment `data/` folder. The script computes exact alpha values from the closed-form polyprotic acid equilibrium expression. No external data dependencies.

### Output inventory

3 runs × 8 files = 24 pipeline output files in `pipeline_output/`.

---

Peter Higgins / Rogue Wave Audio — CC BY 4.0
