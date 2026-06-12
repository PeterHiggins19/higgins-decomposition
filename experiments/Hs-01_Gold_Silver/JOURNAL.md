# Hs-01: Gold/Silver Price Ratio

*Author: Peter Higgins*
*Date: 2026-04-30*
*Domain: COMMODITIES*
*Series: Core (Hs-01 through Hs-25)*

## 1. Purpose

This experiment validates the Hs decomposition on the simplest possible compositional system: a 2-part simplex derived from monthly gold and silver price ratios. With D=2, the system has minimal compositional complexity (a single degree of freedom in the simplex). It serves as the baseline validation case, confirming that the pipeline correctly processes a time-varying binary composition and produces internally consistent diagnostics across all 12 steps.

## 2. Data Source

**Dataset:** Monthly gold and silver prices converted to a 2-part simplex (gold_frac, silver_frac).

**Origin:** MeasuringWorth.com (https://www.measuringworth.com/datasets/gold/)

**License:** Public domain / academic use

**Description:** The raw gold and silver price series spanning 1687 to 2024 were converted into compositional fractions where each observation sums to unity. The two carriers represent the relative share of gold and silver in the price pair at each monthly observation.

**Repo copy:** `data/Commodities/gold_silver_simplex.csv`

## 3. System Parameters

| Parameter | Value |
|-----------|-------|
| N (observations) | 624 |
| D (carriers) | 2 |
| Carriers | Gold, Silver |
| Time axis | Monthly (1687--2024) |
| Zero replacement | No |
| Data hash (SHA-256/16) | `5349a921c85695da` |

## 4. Method

The full Hs pipeline (v1.0 Extended) was applied via `hs_run.py`. The pipeline is deterministic -- repeated runs on identical input produce bit-identical output.

No zero replacement was required. The 2-part simplex is fully constrained: knowing one carrier determines the other. This makes the system a strict validation target -- the pipeline must produce results consistent with a single compositional degree of freedom.

## 5. Results

### 5.1 Variance Structure

- **Total variance:** 0.2958
- **Variance shape:** Bowl
- **Variance R-squared:** 0.9071
- **Entropy mean:** 0.1846
- **Entropy CV:** 58.19%

The bowl-shaped variance profile with R-squared = 0.9071 indicates a well-structured parabolic variance envelope. The high entropy CV (58.19%) reflects the large compositional swings in the gold/silver ratio over the 337-year observation window. The low mean entropy (0.1846) indicates the system spends most of its time far from the equal-share midpoint, with one metal dominating the ratio.

### 5.2 Diagnostic Summary

| Category | Count |
|----------|-------|
| Total codes | 48 |
| Errors | 0 |
| Warnings | 0 |
| Discoveries | 16 |
| Calibration signals | 1 |
| Structural modes | 3 |
| Information | 28 |

**Zero errors and zero warnings.** The pipeline processed this system cleanly.

**Key discoveries:**

- **Precision match** (S8-TGT-DIS): Structural resonance at delta = 0.000032 against the constant 1/pi.
- **High chaos** (S9-CHH-DIS): 533 of 624 intervals classified as turbulent.
- **Stalls** (S9-STL-DIS): 70 entropy-rate stalls detected, marking periods where the gold/silver ratio was approximately stationary.
- **Reversals** (S9-REV-DIS): 461 compositional reversals, consistent with the oscillatory nature of commodity ratios.
- **Drift decreasing** (XU-DRD-DIS): The system is converging (variance ratio 2nd-to-1st = 0.122). Gold is the carrier with maximum shift.
- **Zero-crossing events** (XC-ZCR-DIS): 36 events where Silver approached the simplex boundary (below 1% share), reflecting historical periods of extreme gold dominance.
- **Transfer entropy zero** (XC-TEZ-CAL): The system is compositionally memoryless -- the compositional state at time t does not predict the state at t+1 beyond what the marginal distribution provides.

**Matrix diagnostics:** The D=2 system yields degenerate matrix structure: rank-1 eigenbasis (lambda1 fraction = 1.0), perfect eigenbasis overlap (1.0), infinite condition number (kappa = inf), and zero anisotropy. These are the expected results for a system with a single compositional degree of freedom.

**Structural modes detected (3):**

1. **SM-RTR-DIS** -- Regime transition detected. Stall points mark boundaries between distinct compositional regimes.
2. **SM-FRZ-DIS** -- Frozen eigenbasis. The eigenvectors do not rotate across intervals (expected for D=2).
3. **SM-EDP-DIS** -- Eigenvalue power dynamics detected.

### 5.3 Projection Analysis

The five mandatory projections (helix exploded, manifold helix, six-view projections, polar stack, manifold paper) were generated. For a D=2 system, the helix collapses to a planar oscillation. The polar stack shows the gold/silver balance at each interval, with the ghost composite revealing the long-term drift toward gold dominance. The manifold paper projection maps the single-degree-of-freedom trajectory in 3D projected space.

## 6. Conclusions

Hs-01 validates the pipeline on the simplest possible compositional system. The results confirm:

1. **Correct degenerate handling.** The D=2 system produces rank-1 eigenbasis, infinite condition number, zero anisotropy, and frozen eigenvectors -- all mathematically expected for a single-degree-of-freedom simplex.

2. **Bowl detection at D=2.** The parabolic variance envelope (R-squared = 0.9071) is detected even in the minimal case, confirming that bowl structure is a property of the compositional geometry, not an artifact of high dimensionality.

3. **Regime transitions in commodity data.** The pipeline identifies 70 stall points and 461 reversals across 337 years of data, consistent with the known cyclical behavior of the gold/silver ratio driven by monetary policy changes, industrial demand shifts, and speculative episodes.

4. **Compositional memorylessness.** Transfer entropy is exactly zero, indicating that the gold/silver ratio follows a process where past compositional states provide no predictive information about future states beyond the marginal distribution.

5. **Boundary behavior.** The 36 zero-crossing events at the Silver boundary correspond to historical periods where gold dominated the pair almost entirely.

As the minimal validation case, Hs-01 establishes that the Hs pipeline produces correct and interpretable results at the lowest possible dimensionality before scaling to more complex systems.

## 7. Reproducibility

Run command:

```bash
cd tools/pipeline
python hs_run.py ../../data/Commodities/gold_silver_simplex.csv --exp-id "Hs-01" --name "Gold/Silver Price Ratio" --domain COMMODITIES
```

All outputs in `pipeline_output/`. Results JSON contains full numerical record. Pipeline is fully deterministic -- no stochastic elements.
