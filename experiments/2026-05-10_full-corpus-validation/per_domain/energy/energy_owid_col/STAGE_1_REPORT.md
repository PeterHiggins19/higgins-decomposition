# Stage 1 Report (pure CoDa) — energy_owid_col

**Domain:** energy
**Description:** OWID primary-energy consumption composition for COL (COL), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: COL

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `52d263f872c782307adb264aea3d7744f1ff6bfca1ca2d40f0ba82322f33df4f`

## Input

- Source CSV: `owid_energy_COL.csv`
- Source SHA-256: `5f47fb6eba809e8a...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `d84fc1099f8fb928...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.1177 | 17.2453 | — |
| 1 | 1966 | 1.0774 | 17.2020 | 0.1436 |
| 2 | 1967 | 1.1237 | 17.2616 | 0.1660 |
| 3 | 1968 | 1.1058 | 17.2513 | 0.1531 |
| 4 | 1969 | 1.1484 | 17.2964 | 0.1256 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.3210 | 11.7420 | 0.3827 |
| 58 | 2023 | 1.3620 | 11.4225 | 1.1320 |
| 59 | 2024 | 1.4030 | 11.4740 | 1.0367 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9955 | 29.2° | no |
| Coal | Oil | +0.9817 | 12.8° | no |
| Gas | Hydro | +0.9815 | 4.4° | YES |
| Coal | Nuclear | +0.9798 | 33.1° | no |
| Gas | Nuclear | +0.9766 | 26.8° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Biofuel | -0.8750 | 87.4° | no |
| Hydro | Biofuel | -0.9015 | 75.2° | no |
| Gas | Biofuel | -0.9073 | 78.7° | no |
| Oil | Biofuel | -0.9235 | 71.5° | no |
| Nuclear | Biofuel | -0.9255 | 344.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.152 | 6.320 | 2.962 | 6.026 |
| Coal | Oil | 2.152 | 6.320 | 3.592 | 7.277 |
| Coal | Nuclear | 2.152 | 6.320 | -9.357 | -6.057 |
| Coal | Hydro | 2.152 | 6.320 | 2.950 | 6.536 |
| Coal | Solar | 2.152 | 6.320 | -8.109 | 0.147 |
| Coal | Wind | 2.152 | 6.320 | -6.640 | -1.346 |
| Coal | Biofuel | 2.152 | 6.320 | -7.400 | 1.613 |
| Gas | Oil | 2.962 | 6.026 | 3.592 | 7.277 |
| Gas | Nuclear | 2.962 | 6.026 | -9.357 | -6.057 |
| Gas | Hydro | 2.962 | 6.026 | 2.950 | 6.536 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*