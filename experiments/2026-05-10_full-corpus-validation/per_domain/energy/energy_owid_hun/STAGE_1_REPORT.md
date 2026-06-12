# Stage 1 Report (pure CoDa) — energy_owid_hun

**Domain:** energy
**Description:** OWID primary-energy consumption composition for HUN (HUN), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: HUN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `9b33364dca684c65a86b576492ebd5c43aaa9a9d280740368f26331a106d8c38`

## Input

- Source CSV: `owid_energy_HUN.csv`
- Source SHA-256: `2bb69df5d058e1da...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `76d9141debd84179...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.8004 | 16.3189 | — |
| 1 | 1966 | 0.8568 | 16.4279 | 0.3087 |
| 2 | 1967 | 0.9337 | 16.5148 | 0.3567 |
| 3 | 1968 | 0.9737 | 16.5705 | 0.1916 |
| 4 | 1969 | 1.0022 | 16.6056 | 0.1225 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.4202 | 5.1512 | 0.3434 |
| 58 | 2023 | 1.4476 | 4.9501 | 0.5478 |
| 59 | 2024 | 1.4527 | 4.9800 | 0.3265 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9906 | 69.0° | no |
| Coal | Hydro | +0.9891 | 107.8° | no |
| Coal | Oil | +0.9889 | 54.3° | no |
| Gas | Hydro | +0.9800 | 72.1° | no |
| Gas | Oil | +0.9772 | 8.9° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Biofuel | -0.8127 | 90.3° | no |
| Oil | Wind | -0.8128 | 36.5° | no |
| Hydro | Wind | -0.8171 | 84.8° | no |
| Gas | Wind | -0.8478 | 37.5° | no |
| Gas | Biofuel | -0.8574 | 44.4° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.201 | 7.931 | 2.036 | 6.973 |
| Coal | Oil | -0.201 | 7.931 | 2.153 | 7.386 |
| Coal | Nuclear | -0.201 | 7.931 | -5.679 | 4.752 |
| Coal | Hydro | -0.201 | 7.931 | -3.166 | 1.745 |
| Coal | Solar | -0.201 | 7.931 | -8.832 | 0.711 |
| Coal | Wind | -0.201 | 7.931 | -7.126 | -0.864 |
| Coal | Biofuel | -0.201 | 7.931 | -7.584 | -0.610 |
| Gas | Oil | 2.036 | 6.973 | 2.153 | 7.386 |
| Gas | Nuclear | 2.036 | 6.973 | -5.679 | 4.752 |
| Gas | Hydro | 2.036 | 6.973 | -3.166 | 1.745 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*