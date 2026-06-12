# Stage 1 Report (pure CoDa) — energy_owid_aus

**Domain:** energy
**Description:** OWID primary-energy consumption composition for AUS (AUS), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: AUS

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `f04c438854185e28cc1656044ed9707ba599f88293afac65dfc59515a54d6f38`

## Input

- Source CSV: `owid_energy_AUS.csv`
- Source SHA-256: `b03c0f0677ff5644...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `5dec6ea6f1629205...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.8587 | 16.2687 | — |
| 1 | 1966 | 0.8486 | 16.2276 | 0.2526 |
| 2 | 1967 | 0.8452 | 16.2222 | 0.0721 |
| 3 | 1968 | 0.8460 | 16.2342 | 1.8638 |
| 4 | 1969 | 0.8871 | 16.5718 | 2.3964 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.4693 | 11.4193 | 0.1787 |
| 58 | 2023 | 1.4752 | 11.4400 | 0.2522 |
| 59 | 2024 | 1.4727 | 11.4518 | 0.2040 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9980 | 38.3° | no |
| Nuclear | Hydro | +0.9977 | 45.7° | no |
| Oil | Hydro | +0.9975 | 29.8° | no |
| Coal | Nuclear | +0.9969 | 39.9° | no |
| Coal | Hydro | +0.9931 | 29.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Solar | -0.9289 | 71.7° | no |
| Coal | Wind | -0.9374 | 68.4° | no |
| Oil | Wind | -0.9512 | 66.7° | no |
| Nuclear | Wind | -0.9514 | 358.7° | no |
| Hydro | Wind | -0.9562 | 132.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.928 | 7.924 | -0.908 | 5.956 |
| Coal | Oil | 2.928 | 7.924 | 3.234 | 7.957 |
| Coal | Nuclear | 2.928 | 7.924 | -9.525 | -5.152 |
| Coal | Hydro | 2.928 | 7.924 | 0.342 | 5.678 |
| Coal | Solar | 2.928 | 7.924 | -6.056 | 1.705 |
| Coal | Wind | 2.928 | 7.924 | -6.484 | 1.277 |
| Coal | Biofuel | 2.928 | 7.924 | -7.554 | -1.546 |
| Gas | Oil | -0.908 | 5.956 | 3.234 | 7.957 |
| Gas | Nuclear | -0.908 | 5.956 | -9.525 | -5.152 |
| Gas | Hydro | -0.908 | 5.956 | 0.342 | 5.678 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*