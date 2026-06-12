# Stage 1 Report (pure CoDa) — energy_owid_nzl

**Domain:** energy
**Description:** OWID primary-energy consumption composition for NZL (NZL), annual TWh. T = 55 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: NZL

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `cc37a5bdf4113f92bdffbbda8ea42e3f0a5566b12166e9bc789929533aeb16b1`

## Input

- Source CSV: `owid_energy_NZL.csv`
- Source SHA-256: `f03538974ee80734...`
- Records (T): **55**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `97a5f2a0a0935acf...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1970 | 1.0527 | 16.8524 | — |
| 1 | 1971 | 1.0383 | 16.8533 | 0.2633 |
| 2 | 1972 | 1.0526 | 16.9487 | 0.5021 |
| 3 | 1973 | 1.0675 | 16.9832 | 0.1360 |
| 4 | 1974 | 1.1101 | 17.1071 | 0.4994 |
| ... | ... | ... | ... | ... |
| 52 | 2022 | 1.3485 | 11.7377 | 0.5246 |
| 53 | 2023 | 1.3419 | 11.6762 | 0.2942 |
| 54 | 2024 | 1.3751 | 11.6640 | 0.6089 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Hydro | +0.9985 | 30.5° | no |
| Coal | Oil | +0.9923 | 15.8° | no |
| Oil | Nuclear | +0.9913 | 29.1° | no |
| Oil | Hydro | +0.9887 | 5.6° | YES |
| Coal | Nuclear | +0.9848 | 35.8° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | -0.8222 | 27.0° | no |
| Coal | Wind | -0.8875 | 88.7° | no |
| Oil | Wind | -0.8885 | 66.5° | no |
| Nuclear | Wind | -0.8962 | 352.1° | no |
| Hydro | Wind | -0.9092 | 67.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.744 | 6.168 | 2.654 | 6.378 |
| Coal | Oil | 1.744 | 6.168 | 3.737 | 7.233 |
| Coal | Nuclear | 1.744 | 6.168 | -9.257 | -5.840 |
| Coal | Hydro | 1.744 | 6.168 | 3.302 | 6.999 |
| Coal | Solar | 1.744 | 6.168 | -7.280 | -0.367 |
| Coal | Wind | 1.744 | 6.168 | -6.155 | 1.675 |
| Coal | Biofuel | 1.744 | 6.168 | -7.280 | -2.814 |
| Gas | Oil | 2.654 | 6.378 | 3.737 | 7.233 |
| Gas | Nuclear | 2.654 | 6.378 | -9.257 | -5.840 |
| Gas | Hydro | 2.654 | 6.378 | 3.302 | 6.999 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*