# Stage 1 Report (pure CoDa) — energy_owid_pol

**Domain:** energy
**Description:** OWID primary-energy consumption composition for POL (POL), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: POL

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `445a0438d4abe6d9d9b5f9910b62821dffef7d5418a0b9b11e8fbbb9673a397c`

## Input

- Source CSV: `owid_energy_POL.csv`
- Source SHA-256: `fe1963ca1428eb53...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `d791585e91cdbe8f...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.4116 | 15.7795 | — |
| 1 | 1966 | 0.4285 | 15.8264 | 0.1472 |
| 2 | 1967 | 0.4564 | 15.8992 | 0.1611 |
| 3 | 1968 | 0.5150 | 16.0147 | 0.2624 |
| 4 | 1969 | 0.5512 | 16.0590 | 0.3853 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.3011 | 11.0282 | 0.7913 |
| 58 | 2023 | 1.3758 | 11.0358 | 0.4080 |
| 59 | 2024 | 1.4173 | 11.0658 | 0.3347 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Nuclear | +0.9994 | 39.3° | no |
| Gas | Oil | +0.9905 | 4.7° | YES |
| Oil | Hydro | +0.9896 | 46.2° | no |
| Nuclear | Hydro | +0.9878 | 357.4° | no |
| Coal | Hydro | +0.9854 | 40.8° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | -0.9267 | 359.4° | no |
| Hydro | Wind | -0.9353 | 201.2° | no |
| Oil | Wind | -0.9356 | 65.7° | no |
| Coal | Wind | -0.9658 | 59.2° | no |
| Nuclear | Wind | -0.9679 | 358.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 3.084 | 8.313 | 2.484 | 5.770 |
| Coal | Oil | 3.084 | 8.313 | 3.149 | 6.422 |
| Coal | Nuclear | 3.084 | 8.313 | -9.645 | -5.388 |
| Coal | Hydro | 3.084 | 8.313 | -1.157 | 2.931 |
| Coal | Solar | 3.084 | 8.313 | -7.995 | 0.762 |
| Coal | Wind | 3.084 | 8.313 | -5.686 | 1.454 |
| Coal | Biofuel | 3.084 | 8.313 | -6.411 | 0.850 |
| Gas | Oil | 2.484 | 5.770 | 3.149 | 6.422 |
| Gas | Nuclear | 2.484 | 5.770 | -9.645 | -5.388 |
| Gas | Hydro | 2.484 | 5.770 | -1.157 | 2.931 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*