# Hs-03: Nuclear SEMF Binding Energy

*Author: Peter Higgins*
*Date: 2026-04-30*
*Domain: NUCLEAR*
*Series: Core (Hs-01 through Hs-25)*

## 1. Purpose

This experiment validates the Hs decomposition against a well-established physics result: the semi-empirical mass formula (SEMF) decomposition of nuclear binding energy. The SEMF partitions binding energy into five terms (volume, surface, Coulomb, asymmetry, pairing), each with known physical origin and scaling behavior. By treating these five terms as compositional carriers, this experiment tests whether the Hs pipeline correctly identifies the compositional structure that nuclear physics already characterizes analytically.

## 2. Data Source

**Dataset:** Nuclear binding energy decomposed into 5 SEMF terms for elements Z=1 through Z=118.

**Origin:** AME2020 atomic mass evaluation combined with the semi-empirical mass formula.

**URL:** https://www-nds.iaea.org/amdc/

**License:** Public domain / academic use

**Description:** For each element (indexed by nuclear mass number A), the total binding energy is decomposed into five terms: volume (proportional to A), surface (proportional to A^(2/3)), Coulomb (proportional to Z^2/A^(1/3)), asymmetry (proportional to (A-2Z)^2/A), and pairing (dependent on odd/even nucleon count). These five terms are normalized to unit sum, forming a 5-part composition for each element.

**Repo copy:** `data/Nuclear/nuclear_semf_composition.csv`

## 3. System Parameters

| Parameter | Value |
|-----------|-------|
| N (observations) | 118 |
| D (carriers) | 5 |
| Carriers | B_volume, B_surface, B_coulomb, B_asymmetry, B_pairing |
| Time axis | Nuclear mass number A (indexed) |
| Zero replacement | Yes |
| Data hash (SHA-256/16) | `8f2f5fd2126ab09e` |

## 4. Method

The full Hs pipeline (v1.0 Extended) was applied via `hs_run.py`. The pipeline is deterministic -- repeated runs on identical input produce bit-identical output.

Zero replacement was applied because the pairing term can be exactly zero for certain nuclei. The epsilon value of 1e-10 was used to maintain compositional closure without distorting the structure.

## 5. Results

### 5.1 Variance Structure

- **Total variance:** 11.4273
- **Variance shape:** Bowl
- **Variance R-squared:** 0.8598
- **Entropy mean:** 0.5618
- **Entropy CV:** 6.31%

The bowl-shaped variance profile with R-squared = 0.8598 indicates strong parabolic structure across the nuclear chart. The low entropy CV (6.31%) reflects the relatively smooth evolution of binding energy composition as mass number increases -- the SEMF terms change gradually rather than abruptly. The moderate mean entropy (0.5618) indicates that no single term completely dominates; multiple carriers contribute meaningfully at most mass numbers.

### 5.2 Diagnostic Summary

| Category | Count |
|----------|-------|
| Total codes | 57 |
| Errors | 0 |
| Warnings | 1 |
| Discoveries | 20 |
| Calibration signals | 1 |
| Structural modes | 4 |
| Information | 31 |

**Zero errors.** One warning (MX-CMN-WRN) from the matrix diagnostic module.

**Key discoveries:**

- **Euler-family constant** (S8-EUL-DIS): Structural resonance with the constant 1/(pi^e) at delta = 0.000041. This precision match (S8-TGT-DIS) at delta < 0.001 indicates the pipeline geometry encodes structure inherent to the physical system.
- **High chaos** (S9-CHH-DIS): 102 of 118 intervals classified as turbulent, reflecting the rapid compositional shifts caused by shell effects and pairing oscillations.
- **Stalls** (S9-STL-DIS): 9 entropy-rate stalls marking mass numbers where the binding energy composition is approximately stationary.
- **Reversals** (S9-REV-DIS): 93 compositional reversals, consistent with the odd-even staggering of the pairing term.
- **Drift decreasing** (XU-DRD-DIS): The system converges (variance ratio 2nd-to-1st = 0.3244). B_surface is the carrier with maximum shift.
- **Directed information flow** (XC-TEF-DIS): Dominant transfer entropy from B_surface to B_coulomb (TE = 0.6203), reflecting the physical relationship where both terms depend on nuclear radius.
- **Volatile ratios:** Five carrier pairs identified as independent (CV > 50%), including ln(B_surface/B_coulomb) at CV = 376.4, the most volatile pair.
- **Zero-crossing events** (XC-ZCR-DIS): 118 events across B_coulomb, B_asymmetry, and B_pairing, all of which approach zero at low mass numbers.
- **PID redundancy** (XC-PIR-DIS): Carriers share redundant information, consistent with the physical fact that all SEMF terms derive from the same underlying nuclear parameters (A and Z).

**Matrix diagnostics:**

- Condition number kappa = 1055.08, indicating moderate ill-conditioning consistent with the wide range of SEMF term magnitudes.
- Eigenvalue power law R-squared = 0.9876, alpha = -0.5407.
- One eigenvalue ratio match: lambda2/lambda1 = 0.1548, matching 1/(2pi) at delta = 0.0044.

**Structural modes detected (4):**

1. **SM-RTR-DIS** -- Regime transition detected. Stall points mark boundaries (e.g., magic numbers in nuclear physics).
2. **SM-DMR-DIS** -- Domain resonance. Euler-family geometry encodes structure inherent to the nuclear binding energy landscape.
3. **SM-MXR-DIS** -- Matrix resonance detected.
4. **SM-EDP-DIS** -- Eigenvalue power dynamics detected.

### 5.3 Projection Analysis

The five mandatory projections were generated. The helix exploded diagram shows the smooth evolution of binding energy composition from light to heavy nuclei, with B_volume increasing monotonically while B_coulomb grows and eventually competes. The polar stack reveals the interval-by-interval compositional balance, with the pairing term producing visible oscillation in the ghost composite. The manifold paper projection maps the 5-carrier trajectory through projected 3-space, showing a smooth curve consistent with the known regularity of SEMF scaling.

## 6. Conclusions

Hs-03 validates the pipeline against established nuclear physics. The results confirm:

1. **Correct reading of known compositional structure.** The SEMF decomposition is analytically understood. The pipeline detects the correct coupling relationships: directed information flow from B_surface to B_coulomb (both depend on nuclear radius), redundant information across carriers (all derive from A and Z), and volatile ratios where terms scale differently with mass number.

2. **Physical regime transitions.** The 9 stall points correspond to mass numbers where the binding energy composition is approximately stationary. These are consistent with nuclear shell closures (magic numbers) where binding energy per nucleon reaches local extrema.

3. **Pairing oscillation detection.** The 93 reversals in 118 intervals directly reflect the odd-even staggering of the pairing term, a fundamental feature of nuclear structure. The pipeline detects this oscillation without any prior knowledge of nuclear physics.

4. **Domain resonance.** The Euler-family constant match (1/(pi^e) at delta = 0.000041) is flagged as a structural mode. This indicates that the pipeline geometry resonates with the mathematical structure of the SEMF, which involves power-law and exponential scaling.

5. **Zero-crossing behavior.** All three small carriers (B_coulomb, B_asymmetry, B_pairing) approach the simplex boundary at low mass numbers, correctly reflecting the physical fact that these terms vanish for the lightest nuclei.

The Hs decomposition correctly characterizes the compositional structure of nuclear binding energy without requiring any domain-specific input. The pipeline reads from the data alone what nuclear physics derives from first principles.

## 7. Reproducibility

Run command:

```bash
cd tools/pipeline
python hs_run.py ../../data/Nuclear/nuclear_semf_composition.csv --exp-id "Hs-03" --name "Nuclear SEMF Binding Energy" --domain NUCLEAR
```

All outputs in `pipeline_output/`. Results JSON contains full numerical record. Pipeline is fully deterministic -- no stochastic elements.
