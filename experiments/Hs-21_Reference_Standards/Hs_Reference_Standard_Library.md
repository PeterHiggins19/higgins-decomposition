# Hˢ Reference Standard Library
## Performance Metrology and Calibration Specification

**Pipeline:** Hˢ v1.0 Extended  
**Constants:** 35  
**Sample size:** 200 per reference  
**Total references:** 15  
**Generated:** 2026-04-25T09:37:28Z  
**Author:** Peter Higgins  
**Status:** Calibration standard for all Hˢ DUT comparisons

---

## Purpose

This library provides the reference values that every future Device Under Test (DUT)
is compared against. It establishes the performance ceiling (perfect mathematical
partitions), the physical standard (natural diffraction boundaries), transcendental
anchors, and the noise floor. Each metric includes its criteria for interpretation
and its precise definition.

---

## Master Comparison Table

| ID | Name | Category | Type | HTP | R² | Shape | Nearest | δ | Density | Conc | p(Bonf) | Sig |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF-01 | Gaussian | MATH | Self-conjugate | NATURAL | 0.763 | hill | 1/sqrt3 | 0.000579 | 0 | 0.141 | 0.0005 | ★★ |
| REF-02 | Sinc | MATH | FT pair of rect | NATURAL | 0.679 | hill | 1/(e^pi) | 0.000431 | 2 | 0.338 | 0.0009 | ★★ |
| REF-03 | Exp Decay | MATH | FT pair of Lorentzian | NATURAL | 0.725 | hill | 1/(pi^e) | 0.000005 | 5 | 0.382 | 0.0000 | ★★ |
| REF-04 | Sech | MATH | Self-conjugate | NATURAL | 0.761 | hill | 1/(e^pi) | 0.000130 | 0 | 0.080 | 0.0002 | ★★ |
| REF-05 | Linear Ramp | MATH | Trivial baseline | NATURAL | 0.574 | bowl | 1/ln10 | 0.000105 | 8 | 0.071 | 0.0008 | ★★ |
| REF-06 | Cosine | MATH | Periodic | NATURAL | 0.372 | hill | pi/4 | 0.000172 | 24 | 0.142 | 0.0081 | ★★ |
| REF-07 | Circular Piston | DIFFRACTION | Physical | NATURAL | 0.653 | hill | 1/pi | 0.000020 | 15 | 0.262 | 0.0005 | ★★ |
| REF-08 | Rect Aperture | DIFFRACTION | Physical | NATURAL | 0.351 | hill | 1/ln10 | 0.000008 | 12 | 0.155 | 0.0001 | ★★ |
| REF-09 | Babinet | DIFFRACTION | Closure principle | NATURAL | 0.360 | hill | omega_lambert | 0.000010 | 27 | 0.087 | 0.0002 | ★★ |
| REF-10 | Sin/Cos Circle | TRANSCENDENTAL | 2π | NATURAL | 0.596 | hill | catalan | 0.000077 | 36 | 0.130 | 0.0053 | ★★ |
| REF-11 | Fibonacci | TRANSCENDENTAL | φ | NATURAL | 0.586 | bowl | 1/(e^pi) | 0.002393 | 50 | 0.500 | 1.0000 | — |
| REF-12 | Exp e-family | TRANSCENDENTAL | e | NATURAL | 1.000 | bowl | pi/4 | 0.000001 | 49 | 0.055 | 0.0001 | ★★ |
| REF-13 | Uniform Random | NOISE | IID | NATURAL | 0.178 | bowl | ln_phi | 0.000060 | 40 | 0.224 | 0.0058 | ★★ |
| REF-14 | Gaussian Noise | NOISE | Gaussian | NATURAL | 0.927 | hill | apery | 0.000019 | 34 | 0.165 | 0.0018 | ★★ |
| REF-15 | Near-Constant | NOISE | Constant | INVESTIGATE | 0.876 | hill | none | 999.000000 | 0 | 0.000 | — | — |

---

## Category 1: Mathematical Reference Functions

Provable mathematical functions with known analytical properties. These establish what the pipeline does with functions whose Fourier, exponential, and periodic structure is exactly known.

### REF-01: Gaussian

**Type:** Self-conjugate  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.7630 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 16.836634 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 62.822195 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | 1/sqrt3 | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00057918 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000013 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000461 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 16 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 0.1 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.141 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.1469 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 170.3% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | FAIL | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 48 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | res (66.2%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | stable | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 12 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-02: Sinc

**Type:** FT pair of rect  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.6791 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 7.425983 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 27.011944 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | 1/(e^pi) | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00043060 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000025 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000888 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 116 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 2.1 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.338 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.6092 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 28.2% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 21 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | res (62.4%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | stable | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 11 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-03: Exp Decay

**Type:** FT pair of Lorentzian  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.7254 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 6.609082 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 22.085783 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | 1/(pi^e) | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00000508 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000000 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000011 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 203 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 4.6 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.382 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.4933 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 60.6% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 13 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | res (66.7%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | stable | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 12 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-04: Sech

**Type:** Self-conjugate  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.7605 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 10.836784 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 42.649161 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | 1/(e^pi) | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00012953 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000004 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000150 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 39 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 0.5 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.080 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.2012 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 139.1% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 11 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | res (66.6%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | stable | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 11 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-05: Linear Ramp

**Type:** Trivial baseline  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | bowl | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.5741 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 1.018665 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 8.621468 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | 1/ln10 | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00010456 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000024 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000849 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 69 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 8.0 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.071 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.8208 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 24.0% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 1 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | res (63.6%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | increasing | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 10 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-06: Cosine

**Type:** Periodic  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.3720 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.193343 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 1.293680 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | pi/4 | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00017170 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000231 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.008092 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 97 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 23.9 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.142 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.4853 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 32.2% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 6 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | f (47.3%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | stable | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 8 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

---

## Category 2: Natural Diffraction Boundaries

Physical diffraction patterns representing natural compositional boundaries. Diffraction is nature's own simplex closure — energy partitions into transmitted, reflected, and diffracted components that must sum to the whole.

### REF-07: Circular Piston

**Type:** Physical  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.6533 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.382467 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 2.506541 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | 1/pi | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00002001 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000016 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000547 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 81 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 14.9 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.262 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.4673 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 43.4% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 7 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | Mid (45.0%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | decreasing | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 8 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-08: Rect Aperture

**Type:** Physical  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.3509 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.591699 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 2.099348 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | 1/ln10 | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00000780 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000004 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000140 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 78 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 11.7 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.155 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.3655 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 54.6% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 16 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | Scatter (55.5%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | decreasing | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 9 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-09: Babinet

**Type:** Closure principle  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.3600 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.401569 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 1.620138 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | omega_lambert | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00001019 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000007 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000245 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 149 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 27.1 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.087 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.4224 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 53.4% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 9 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | Complement (55.4%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | decreasing | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 8 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

---

## Category 3: Transcendental Constant Trajectories

Systems designed to generate specific transcendental constant behavior in the variance trajectory. These verify that the pipeline correctly detects known mathematical structure.

### REF-10: Sin/Cos Circle

**Type:** 2π  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.5960 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.142599 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 1.198626 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | catalan | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00007718 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000150 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.005253 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 89 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 35.6 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.130 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.5302 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 27.6% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 3 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | sin (48.2%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | stable | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 5 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-11: Fibonacci

**Type:** φ  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | bowl | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.5861 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.003214 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 0.000713 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | 1/(e^pi) | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00239336 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.119347 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 1.000000 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | No | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | No | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 2 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 49.9 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.500 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.9336 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 0.1% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 142 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | Fn (54.6%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | decreasing | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 10 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-12: Exp e-family

**Type:** e  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | bowl | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 1.0000 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.000000 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 1.515075 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | pi/4 | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00000133 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000002 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.000061 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 74 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 48.9 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.055 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.5885 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 46.0% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 0 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | exp(t) (50.0%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | stable | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 7 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

---

## Category 4: Noise and Instrument Floor

Random and degenerate data establishing what the instrument produces when there is no compositional structure to detect. Any DUT result must be distinguishable from this baseline.

### REF-13: Uniform Random

**Type:** IID  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | bowl | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.1784 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.056638 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 0.634323 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | ln_phi | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00005978 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000164 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.005751 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 103 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 39.7 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.224 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.9240 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 7.5% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | FAIL | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 195 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | R3 (36.2%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | decreasing | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 11 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-14: Gaussian Noise

**Type:** Gaussian  
**Classification:** NATURAL  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.9268 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.064924 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 0.806669 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | apery | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 0.00001870 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| p-value (single) | 0.000050 | <0.05 significant | Probability of landing within δ of any single constant under a uniform null hypothesis. P_single = 2δ / (σ²_A_max − σ²_A_min). Assumes the variance trajectory is equally likely to be anywhere in its range. |
| p-value (Bonferroni) | 0.001750 | <0.05 significant, <0.01 strongly significant | Bonferroni-corrected p-value: P_Bonf = P_single × |T| where |T|=35 is the number of constants tested. Corrects for multiple hypothesis testing. P_Bonf < 0.05 means the proximity is unlikely to arise by chance even after testing all 35 constants. |
| Significant (α=0.05) | Yes | Yes = statistically significant at 5% level | Whether the Bonferroni-corrected p-value is below 0.05. If Yes, the transcendental proximity would occur by chance less than 1 in 20 times. |
| Significant (α=0.01) | Yes | Yes = strongly significant at 1% level | Whether the Bonferroni-corrected p-value is below 0.01. If Yes, the transcendental proximity would occur by chance less than 1 in 100 times. |
| Squeeze count (35) | 59 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 34.5 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.165 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.9364 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 8.7% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | FAIL | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 214 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | G2 (39.0%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | increasing | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 12 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

### REF-15: Near-Constant

**Type:** Constant  
**Classification:** INVESTIGATE  
**N:** 200, **D:** 3  

| Metric | Value | Criteria | Definition |
|---|---|---|---|
| HVLD shape | hill | bowl = variance accelerating, hill = decelerating | Sign of quadratic coefficient 'a' in the parabolic fit σ²_A(t) ≈ at² + bt + c. Bowl (a>0) indicates the system's compositional dispersion is growing over time — carriers are diverging. Hill (a<0) indicates convergence — carriers are settling toward equilibrium. |
| HVLD R² | 0.8759 | >0.80 good, >0.95 excellent, <0.50 poor | Coefficient of determination for the quadratic fit to the variance trajectory. Measures how well a parabola describes σ²_A(t). R²=1.000 means the trajectory IS a perfect parabola. R²<0.50 means the trajectory is non-polynomial — may be oscillatory, step-like, or chaotic. |
| HVLD RMSE | 0.000000 | Lower is better. Compare to σ²_A range. | Root mean squared error of the HVLD quadratic fit residuals. RMSE = √(Σ(y_actual − y_predicted)² / N). Measures the absolute magnitude of the parabola's deviation from the actual trajectory. Should be interpreted relative to the σ²_A range — a small RMSE relative to range means the fit is tight. |
| σ²_A final | 0.000000 | System-dependent. Compare within category. | Cumulative Aitchison variance at the last observation. σ²_A = Σⱼ Var(CLRⱼ). Measures the total compositional dispersion accumulated across all carriers and all observations. Higher values indicate more compositional spread. Population variance (ddof=0). |
| Nearest constant | none | Name of the closest transcendental constant from the 35-constant library | The transcendental constant c ∈ T (|T|=35) that minimises |σ²_A(t*) − c| or |1/σ²_A(t*) − c| across all time indices t*. Tests both direct and reciprocal proximity. The constant's mathematical origin (Euler, Fibonacci, Feigenbaum, etc.) provides interpretive context. |
| δ (absolute) | 999.00000000 | <0.01 = NATURAL, <0.001 = precision, <0.0001 = exceptional | Absolute difference between the variance trajectory value (or its reciprocal) and the nearest transcendental constant. δ = |σ²_A(t*) − c|. Smaller δ means tighter transcendental proximity. δ < 0.01 passes the Higgins Transcendental Completeness Theorem threshold. |
| Squeeze count (35) | 0 | Higher = more constants in range. Context-dependent. | Total number of (time_index, constant, test_type) triplets where |test_value − constant| < 0.01. Counts all matches across all 35 constants, both direct and reciprocal, at all time points. A high count means the trajectory passes near many constants — expected for long trajectories spanning a wide range. |
| Match density | 0.0 | >100 = natural system, <50 = noise floor | Total squeeze matches divided by the trajectory arc length (Σ|Δσ²_A|). Measures matches per unit of trajectory traversed. Natural systems show high density (clustered matches); random systems show low density (scattered). This metric resolves the IVT false-positive issue. |
| Match concentration | 0.000 | >0.40 = clustered (natural), <0.25 = scattered (noise) | Herfindahl index of match distribution across constants: H = Σ(nᵢ/N)² where nᵢ is matches for constant i. Concentration = 1.0 means all matches hit one constant. Concentration ≈ 1/K means matches are uniformly spread across K constants. Natural systems cluster; random systems scatter. |
| Entropy mean (H̄) | 0.9372 | 0 = one carrier dominates, 1 = uniform distribution | Mean normalised Shannon entropy across all observations: H̄ = mean(−Σ pᵢ ln pᵢ / ln D). Measures average compositional evenness. H̄ near 1 means carriers are roughly equal. H̄ near 0 means one carrier dominates. Normalised by H_max = ln(D) so values are comparable across different D. |
| Entropy CV | 0.0% | <10% = stable entropy, >30% = variable | Coefficient of variation of normalised entropy: CV = σ_H / H̄ × 100%. Measures how much the compositional evenness varies across observations. Low CV means the entropy profile is stable; high CV means the system's compositional balance changes significantly over its trajectory. |
| EITT invariance | PASS | PASS = <5% variation at 2×, 4×, 8× decimation | Entropy-Invariant Time Transformer test. Applies geometric-mean block decimation at compression ratios M=2, 4, 8 and compares the decimated mean entropy to the native mean entropy. PASS means |H̄(M) − H̄(1)| / H̄(1) < 5% at all tested M. Geometric mean preserves compositional structure; arithmetic mean would not. |
| Chaos deviations | 196 | <10 = smooth, >50 = turbulent | Total count of compositional turbulence events detected by the EITT chaos detector: stalls (angular velocity < 15% of running mean), spikes (> 3.5× running mean), and reversals (≥ 2 sign changes in 5 consecutive samples). High chaos indicates rapid compositional oscillation or structural instability. |
| Dominant carrier | C3 (48.4%) | >60% = strong dominance, <40% = balanced | The carrier with the highest percentage contribution to total cumulative CLR variance. Shows which compositional part is driving the variance trajectory. Percentage = Var(CLRⱼ) / Σ Var(CLRⱼ) × 100%. |
| Drift direction | increasing | stable / increasing / decreasing | Comparison of σ²_A between first half and second half of the dataset. Variance ratio = Var(2nd half) / Var(1st half). Increasing (ratio > 1.05): system is evolving, second half more dispersed. Decreasing (ratio < 0.95): system is converging. Stable: second half similar to first half. |
| Discoveries | 9 | Count of DIS-level diagnostic codes | Number of diagnostic codes at the Discovery level (code suffix -DIS) emitted by the pipeline. Discoveries include: Euler-family matches, tight matches (δ<0.001), high chaos, carrier dominance (>60%), drift trends, PID patterns, transfer entropy flows, stable/volatile ratio pairs, and zero-crossing events. |

---

## Specification Thresholds

| Specification | Threshold | Criteria | Definition |
|---|---|---|---|
| NATURAL | δ < 0.01 | At least one match within 1% absolute | HTP pretest against 35 transcendental constants, testing both σ²_A and 1/σ²_A |
| INVESTIGATE | 0.01 ≤ δ < 0.05 | Nearest match between 1-5% | Requires alternate decomposition testing per HTCT protocol |
| FLAG | δ ≥ 0.05 | No match within 5% | Evaluate under HTCT Mode (a) synthetic, (b) adversarial, (c) improper decomposition, (d) extraordinary interest |
| Precision match | δ < 0.001 | Structural resonance confirmed | Pipeline geometry aligns with system geometry at 3+ decimal places |
| Noise floor (density) | density < 50 | IVT-dominated matches | Matches arise from Intermediate Value Theorem, not structural resonance |
| Natural (density) | density > 100 | Structural matches dominate | Match clustering indicates genuine compositional structure |
| Noise floor (concentration) | conc < 0.25 | Matches scattered uniformly | No preferred constant — random trajectory passes near whatever is in range |
| Natural (concentration) | conc > 0.40 | Matches clustered | System preferentially locks to specific constants — structural signal |
| Deterministic | Gauge R&R identical | Bit-identical on repeated runs | Zero stochastic elements in pipeline. SHA-256 hash verification. |

---

## How to Use This Library

1. **Run your DUT** through `run_full_extended()` in the Hˢ pipeline
2. **Compare** your DUT's metrics against the reference table — each metric has its criteria and definition
3. **Position** your result relative to the reference categories:
   - Near REF-12 (R²=1.000, δ=0.000001) → strong, clean structure
   - Near REF-07/08/09 (diffraction) → natural physical boundary
   - Near REF-13/14 (noise) → weak or absent structure
4. **Check significance:** p(Bonferroni) < 0.05
5. **Check density/concentration:** above noise floor thresholds
6. **Report** using `hs_codes.py` → `hs_reporter.py` (English, Portuguese, Italian)

---

## ISO Applicability

- **Repeatability:** Gauge R&R verified — bit-identical results
- **Traceability:** Each reference traces to a published mathematical function or physical principle
- **Uncertainty:** HVLD RMSE provides fit uncertainty; p-values provide statistical confidence
- **Calibration:** 15 references span the full operating range
- **Determinism:** Zero stochastic elements

---

*Hˢ — Higgins Decomposition on the Simplex*  
*The instrument reads. The expert decides. The loop stays open.*  
*Peter Higgins, 2026-04-25*