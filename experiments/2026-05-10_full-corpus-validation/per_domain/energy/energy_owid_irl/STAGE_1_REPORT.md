# Stage 1 Report (pure CoDa) — energy_owid_irl

**Domain:** energy
**Description:** OWID primary-energy consumption composition for IRL (IRL), annual TWh. T = 46 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: IRL

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `450f68df55a98ffbce46d29f5bc84ac5de1ddd7a2e02cfe13b1dc0a5a427b047`

## Input

- Source CSV: `owid_energy_IRL.csv`
- Source SHA-256: `e40e30a84c0dc03e...`
- Records (T): **46**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `f23f7c296adb9254...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1979 | 0.7467 | 16.5243 | — |
| 1 | 1980 | 0.8860 | 16.8302 | 1.0460 |
| 2 | 1981 | 0.9874 | 16.9654 | 0.4182 |
| 3 | 1982 | 1.0752 | 17.0613 | 0.4105 |
| 4 | 1983 | 1.1094 | 17.0878 | 0.1528 |
| ... | ... | ... | ... | ... |
| 43 | 2022 | 1.2887 | 11.1467 | 0.6095 |
| 44 | 2023 | 1.3039 | 10.9471 | 1.5249 |
| 45 | 2024 | 1.3030 | 10.9278 | 0.7030 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9968 | 33.5° | no |
| Nuclear | Hydro | +0.9901 | 359.2° | no |
| Coal | Nuclear | +0.9885 | 45.8° | no |
| Oil | Hydro | +0.9839 | 35.6° | no |
| Coal | Oil | +0.9807 | 34.9° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Biofuel | -0.8835 | 95.5° | no |
| Hydro | Wind | -0.8901 | 155.8° | no |
| Gas | Biofuel | -0.9086 | 62.4° | no |
| Nuclear | Biofuel | -0.9119 | 359.1° | no |
| Oil | Biofuel | -0.9159 | 56.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.595 | 6.901 | 2.938 | 6.303 |
| Coal | Oil | 0.595 | 6.901 | 3.481 | 7.745 |
| Coal | Nuclear | 0.595 | 6.901 | -9.606 | -5.749 |
| Coal | Hydro | 0.595 | 6.901 | -0.338 | 4.252 |
| Coal | Solar | 0.595 | 6.901 | -8.183 | 0.040 |
| Coal | Wind | 0.595 | 6.901 | -5.999 | 2.762 |
| Coal | Biofuel | 0.595 | 6.901 | -6.995 | 0.514 |
| Gas | Oil | 2.938 | 6.303 | 3.481 | 7.745 |
| Gas | Nuclear | 2.938 | 6.303 | -9.606 | -5.749 |
| Gas | Hydro | 2.938 | 6.303 | -0.338 | 4.252 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*