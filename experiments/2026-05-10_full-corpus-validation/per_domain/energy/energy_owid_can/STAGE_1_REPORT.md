# Stage 1 Report (pure CoDa) — energy_owid_can

**Domain:** energy
**Description:** OWID primary-energy consumption composition for CAN (CAN), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: CAN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `b2b7e7c3dd64755b3c951543b749d5d47792ec4f1450ff3e1df0e2df173ff68a`

## Input

- Source CSV: `owid_energy_CAN.csv`
- Source SHA-256: `47657ec39a6940a1...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `5618a6ee59e4de4f...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.2582 | 16.1951 | — |
| 1 | 1966 | 1.2567 | 16.1734 | 0.2414 |
| 2 | 1967 | 1.2465 | 16.1735 | 0.1587 |
| 3 | 1968 | 1.2582 | 16.1284 | 1.6161 |
| 4 | 1969 | 1.2550 | 16.1248 | 0.5798 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.4851 | 4.5238 | 0.3255 |
| 58 | 2023 | 1.4953 | 4.2449 | 0.3818 |
| 59 | 2024 | 1.4842 | 4.2190 | 0.3102 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Hydro | +0.9979 | 10.0° | YES |
| Gas | Oil | +0.9941 | 6.4° | YES |
| Oil | Hydro | +0.9926 | 6.0° | YES |
| Coal | Hydro | +0.9907 | 72.2° | no |
| Coal | Gas | +0.9838 | 68.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Biofuel | -0.9461 | 24.1° | no |
| Coal | Wind | -0.9561 | 100.5° | no |
| Oil | Wind | -0.9652 | 39.7° | no |
| Gas | Wind | -0.9671 | 43.0° | no |
| Hydro | Wind | -0.9690 | 37.1° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.865 | 4.941 | 1.801 | 5.170 |
| Coal | Oil | -0.865 | 4.941 | 1.819 | 6.224 |
| Coal | Nuclear | -0.865 | 4.941 | -1.286 | 3.699 |
| Coal | Hydro | -0.865 | 4.941 | 1.469 | 5.559 |
| Coal | Solar | -0.865 | 4.941 | -7.617 | -2.127 |
| Coal | Wind | -0.865 | 4.941 | -7.540 | -0.523 |
| Coal | Biofuel | -0.865 | 4.941 | -8.230 | -1.748 |
| Gas | Oil | 1.801 | 5.170 | 1.819 | 6.224 |
| Gas | Nuclear | 1.801 | 5.170 | -1.286 | 3.699 |
| Gas | Hydro | 1.801 | 5.170 | 1.469 | 5.559 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*