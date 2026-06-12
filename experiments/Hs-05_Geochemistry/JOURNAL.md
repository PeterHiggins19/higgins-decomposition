# Hs-05: Ball Intraplate Volcanics

*Author: Peter Higgins*
*Date: 2026-04-30*
*Domain: GEOCHEMISTRY*
*Series: Core (Hs-01 through Hs-25)*

## 1. Purpose

This experiment validates the Hs decomposition on a large-scale geochemical dataset: 10-part major-element oxide compositions from 26,266 intraplate volcanic rock samples. This is the largest dataset in the Hs validation suite and tests the pipeline at scale. Geochemical oxide compositions are a canonical application domain for compositional data analysis, making this experiment a direct test of the pipeline against established CoDa practice.

## 2. Data Source

**Dataset:** Major-element oxide compositions of intraplate volcanic rocks from the Ball (2022) compilation.

**Origin:** EarthChem / Ball 2022

**URL:** https://doi.org/10.26022/IEDA/112433

**License:** CC BY 4.0

**Description:** Each sample is characterized by 10 major-element oxide weight percentages (SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5) normalized to unit sum. The samples are cross-sectional (no time axis) and represent a wide range of intraplate volcanic lithologies from oceanic and continental settings worldwide.

**Repo copy:** `data/Geochemistry/ball_oxides_composition.csv`

## 3. System Parameters

| Parameter | Value |
|-----------|-------|
| N (observations) | 26,266 |
| D (carriers) | 10 |
| Carriers | SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5 |
| Time axis | Sample index (cross-sectional, no time axis) |
| Zero replacement | Yes |
| Data hash (SHA-256/16) | `feed7349a1920080` |

## 4. Method

The full Hs pipeline (v1.0 Extended) was applied via `hs_run.py`. The pipeline is deterministic -- repeated runs on identical input produce bit-identical output.

Zero replacement was applied because trace oxides (particularly MnO and P2O5) can have values at or near the detection limit. The epsilon value of 1e-10 was used for replacement. With N=26,266 observations, this is the largest single run in the validation suite and tests pipeline computational scaling.

## 5. Results

### 5.1 Variance Structure

- **Total variance:** 5.9881
- **Variance shape:** Bowl
- **Variance R-squared:** 0.5282
- **Entropy mean:** 0.6840
- **Entropy CV:** 7.76%

The bowl-shaped variance profile is detected with R-squared = 0.5282. This is the lowest R-squared in the validation suite, reflecting the high compositional complexity of a 10-part natural system with multiple independent geological processes generating variance. The moderate mean entropy (0.6840) and low CV (7.76%) indicate that the oxide compositions are distributed broadly across the simplex without extreme concentration on any single carrier. SiO2 is the dominant carrier but does not overwhelm the system.

### 5.2 Diagnostic Summary

| Category | Count |
|----------|-------|
| Total codes | 80 |
| Errors | 0 |
| Warnings | 3 |
| Discoveries | 40 |
| Calibration signals | 1 |
| Structural modes | 5 |
| Information | 31 |

**Zero errors.** Three warnings (MX-SCR-WRN, MX-CMN-WRN, MX-REF-WRN) from the matrix diagnostic module, consistent with the high dimensionality and natural variance of the system.

**Key discoveries:**

- **Euler-family constant** (S8-EUL-DIS): Structural resonance with 1/(2pi) at delta = 0.000001, the highest-precision match in the validation suite. This is flagged as a precision match (S8-TGT-DIS).
- **High chaos** (S9-CHH-DIS): 26,254 of 26,266 intervals classified as turbulent. This is expected for a cross-sectional dataset where sequential samples have no physical relationship.
- **Stalls** (S9-STL-DIS): 3,491 stall events where adjacent samples had similar compositions.
- **Spikes** (S9-SPK-DIS): 403 spike events where entropy rate exceeded the threshold, marking sharp compositional transitions between adjacent samples.
- **Reversals** (S9-REV-DIS): 22,360 compositional reversals, expected for unordered cross-sectional data.
- **Drift increasing** (XU-DRU-DIS): The system is evolving (variance ratio 2nd-to-1st = 1.7388). MgO is the carrier with maximum shift, consistent with its role as the primary indicator of magma differentiation.
- **Stable ratio** (XC-RPS-DIS): ln(SiO2/MnO) is compositionally locked (CV = 17.96), indicating that SiO2 and MnO maintain a consistent proportional relationship across all samples.
- **Volatile ratios:** 24 carrier pairs identified as independent (CV > 50%), with ln(CaO/MgO) the most volatile at CV = 1,428.6. This extreme volatility reflects the independent geological controls on CaO (plagioclase fractionation) and MgO (olivine fractionation).
- **PID redundancy** (XC-PIR-DIS): Carriers share redundant information, consistent with the common petrogenetic origin of the oxide suite.
- **Zero-crossing events** (XC-ZCR-DIS): 26,265 events across all 10 carriers. Multiple trace oxides (MnO, P2O5, TiO2, K2O) approach the simplex boundary in many samples.
- **Transfer entropy zero** (XC-TEZ-CAL): The system is compositionally memoryless, expected for cross-sectional data with no inherent ordering.

**Matrix diagnostics:**

- Eigenvalue power law R-squared = 0.9399, alpha = 0.3111.
- 19 eigenvalue ratio matches to mathematical constants, with the best being lambda6/lambda5 = 0.5744, matching Euler's gamma at delta = 0.0028.
- Q = 102.71, the highest matrix quality factor in the validation suite.

**Structural modes detected (5):**

1. **SM-RTR-DIS** -- Regime transition. Stall points mark compositional boundaries between rock types.
2. **SM-DMR-DIS** -- Domain resonance. Euler-family geometry encodes geochemical structure.
3. **SM-CPL-DIS** -- Carrier coupling. The stable SiO2/MnO ratio encodes a petrogenetic constraint.
4. **SM-MXR-DIS** -- Matrix resonance detected.
5. **SM-EDP-DIS** -- Eigenvalue power dynamics detected.

### 5.3 Projection Analysis

The five mandatory projections were generated. The helix exploded diagram shows the 10-carrier system with SiO2 and MgO as the dominant variance carriers. The polar stack reveals the sample-by-sample compositional balance, with the ghost composite showing the average oxide proportions characteristic of intraplate basalts. The manifold paper projection maps the high-dimensional trajectory through projected 3-space, showing a distributed cloud consistent with multiple overlapping rock types rather than a single evolutionary trend.

## 6. Conclusions

Hs-05 validates the pipeline at scale on a canonical geochemical dataset. The results confirm:

1. **Scalability.** The pipeline processes 26,266 observations with 10 carriers and produces complete diagnostics with zero errors. Computational scaling is adequate for datasets of this size.

2. **Geochemically meaningful diagnostics.** The pipeline identifies MgO as the carrier with maximum shift, which geochemistry identifies as the primary fractionation index. The stable SiO2/MnO ratio reflects a known petrogenetic constraint. The extreme volatility of the CaO/MgO ratio correctly captures the independent fractionation of plagioclase and olivine.

3. **Bowl structure at high D.** The lower R-squared (0.5282) compared to simpler systems is expected: a 10-part composition with multiple independent geological processes produces variance that does not follow a single parabolic envelope as tightly. The bowl is still detected, indicating that the fundamental variance structure persists even in complex natural systems.

4. **Cross-sectional behavior.** The pipeline correctly identifies the cross-sectional nature of the data: transfer entropy is zero (no memory), nearly all intervals are turbulent (adjacent samples are unrelated), and drift is increasing (the dataset spans a compositional range rather than converging).

5. **Carrier coupling.** The detection of a single stable ratio (SiO2/MnO) among 45 possible pairs is geochemically significant. It indicates a constraint that holds across the entire intraplate volcanic population regardless of tectonic setting or degree of differentiation.

The Hs decomposition correctly characterizes the compositional structure of a large, complex geochemical dataset and produces diagnostics that align with established petrological understanding.

## 7. Reproducibility

Run command:

```bash
cd tools/pipeline
python hs_run.py ../../data/Geochemistry/ball_oxides_composition.csv --exp-id "Hs-05" --name "Ball Intraplate Volcanics" --domain GEOCHEMISTRY
```

All outputs in `pipeline_output/`. Results JSON contains full numerical record. Pipeline is fully deterministic -- no stochastic elements.
