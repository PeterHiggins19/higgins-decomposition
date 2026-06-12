# Hs-17: Backblaze Fleet Composition

*Author: Peter Higgins*
*Date: 2026-04-30*
*Domain: STORAGE*
*Series: Core (Hs-01 through Hs-25)*

## 1. Purpose

This experiment applies the Hs decomposition to hard drive fleet failure mode compositions derived from Backblaze operational data. The objective is to determine whether the Hs pipeline can characterize the compositional structure of failure mode distributions across a large-scale storage fleet over time, and whether the resulting diagnostics correspond to known patterns of drive degradation and failure.

## 2. Data Source

**Dataset:** Backblaze Hard Drive Stats
**Origin URL:** https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data
**License:** CC BY 4.0
**Repo copy:** `experiments/Hs-17_Backblaze/Hs-17_fleet_composition.csv`

The dataset represents quarterly failure mode compositions for the Backblaze hard drive fleet from 2013 to 2023. Each observation is a quarterly snapshot. The five carriers represent the proportional contribution of each failure category to the total failure budget: index (sequential position), Mechanical, Thermal, Age, and Errors. The compositions are closed (sum to 1) at each time step, forming a 5-part simplex.

## 3. System Parameters

| Parameter | Value |
|-----------|-------|
| N (observations) | 108 |
| D (carriers) | 5 |
| Carriers | index, Mechanical, Thermal, Age, Errors |
| Time axis | Quarterly (2013--2023) |
| Zero replacement | Yes |
| Epsilon | 1e-10 |
| Data hash (SHA-256/16) | `051cca62652b01a6` |

## 4. Method

The full Hs pipeline (v1.0 Extended) was applied via `hs_run.py`. The pipeline is deterministic -- repeated runs on identical input produce bit-identical output.

Zero replacement was applied to handle structural zeros in the failure mode data. The index carrier captures positional structure across the quarterly time series. The remaining four carriers partition failure modes into Mechanical, Thermal, Age-related, and Error-based categories.

## 5. Results

### 5.1 Variance Structure

- **Total variance:** 1.7544
- **Shape classification:** Bowl
- **Variance R-squared:** 0.8835
- **Entropy mean:** 0.5561
- **Entropy CV:** 29.00%

The bowl-shaped variance curve with R-squared = 0.8835 indicates a system with concentrated variance at the boundaries of the observation window and lower variance in the interior. This is consistent with a fleet that underwent compositional transitions at the beginning and end of the observation period while maintaining relative stability in between.

### 5.2 Diagnostic Summary

- **Total diagnostic codes:** 60
- **Errors:** 0
- **Warnings:** 1
- **Discoveries:** 23
- **Calibration signals:** 0
- **Structural modes:** 4
- **Information codes:** 32

**Carrier dominance:** The index carrier contributes 66.3% of total variance, indicating that the sequential position (time) is the primary driver of compositional change in the fleet.

**Entropy dynamics:** High chaos (66 chaotic intervals), 14 stalls, 3 spikes, and 49 reversals were detected. This pattern indicates a compositionally turbulent system with frequent oscillations between failure mode regimes.

**Carrier coupling:** Thermal/Errors (CV = 18.30) and Age/Errors (CV = 18.07) form stable pairwise ratios, indicating these carriers are compositionally locked. This suggests a physical coupling between thermal stress, aging, and error accumulation in drive failure mechanisms.

**Directed information flow:** Transfer entropy analysis identified a dominant flow from Thermal to Age (TE = 0.066), consistent with the physical expectation that thermal stress accelerates age-related degradation.

**Drift direction:** Decreasing (variance ratio 2nd/1st half = 0.028), with maximum shift in the Errors carrier. The fleet is converging toward a more stable failure mode distribution.

**Zero-crossing events:** 12 near-zero events detected in the index and Age carriers, indicating compositions approaching the simplex boundary.

**Matrix diagnostics:** Condition number kappa = 2738.4. Eigenvalue power law R-squared = 0.9954 with alpha = -0.444. Q-metric = 218.96.

**Precision match:** A structural resonance was detected at the 1/e constant with delta = 0.000258 (below the 0.001 precision threshold).

### 5.3 Structural Modes

Four structural modes were detected:

1. **SM-RTR-DIS (Regime transition):** Stall points mark boundaries between distinct compositional regimes in the fleet history. The 14 detected stalls suggest multiple regime transitions across the 2013--2023 observation window.

2. **SM-CPL-DIS (Carrier coupling):** The stable Thermal/Errors and Age/Errors ratios encode a physical constraint. These failure modes share a common physical driver -- cumulative operational stress on the drives.

3. **SM-MXR-DIS (Matrix resonance):** The eigenvalue spectrum and condition number indicate structured matrix geometry in the CLR-transformed data.

4. **SM-EDP-DIS (Eigenvalue power dynamics):** The near-perfect power law fit (R-squared = 0.9954) in the eigenvalue spectrum indicates a scale-free variance structure across the compositional modes.

### 5.4 Projection Analysis

The five mandatory projections (helix exploded, manifold helix, six-view projections, polar stack, manifold paper) capture the fleet's compositional trajectory through the 5-part simplex. The helix projections show the temporal evolution of failure mode proportions. The polar stack reveals per-interval compositional fingerprints. The manifold paper projection maps the CLR-space trajectory into 3D projected space, exposing the geometric structure of regime transitions.

## 6. Conclusions

The Hs decomposition successfully characterizes the compositional structure of hard drive fleet failure modes. The key findings are:

1. The fleet's failure mode composition is time-dominated (index carrier = 66.3% of variance), confirming that the fleet's failure profile evolved systematically over the 2013--2023 period.

2. The coupling between Thermal, Age, and Errors carriers (stable pairwise ratios with CV < 19) reflects the known physical relationship between thermal stress, aging, and error accumulation in hard drives.

3. The directed information flow from Thermal to Age (TE = 0.066) is consistent with the engineering understanding that thermal cycling accelerates mechanical wear and age-related failure.

4. The bowl-shaped variance curve with R-squared = 0.8835 and 14 detected stalls indicate a fleet that passed through multiple compositional regimes, likely corresponding to fleet-wide hardware generation transitions.

5. The convergent drift (decreasing variance ratio = 0.028) suggests the fleet was stabilizing toward a more uniform failure mode distribution by 2023.

The decomposition produces diagnostics that align with domain knowledge from storage engineering without requiring any domain-specific tuning.

## 7. Reproducibility

Run command:
```bash
cd tools/pipeline
python hs_run.py ../../experiments/Hs-17_Backblaze/Hs-17_fleet_composition.csv --exp-id "Hs-17" --name "Backblaze Fleet Composition" --domain STORAGE
```

All outputs in `pipeline_output/`. Results JSON contains full numerical record.
