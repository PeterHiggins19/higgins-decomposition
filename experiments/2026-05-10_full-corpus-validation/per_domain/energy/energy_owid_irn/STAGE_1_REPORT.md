# Stage 1 Report (pure CoDa) — energy_owid_irn

**Domain:** energy
**Description:** OWID primary-energy consumption composition for IRN (IRN), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: IRN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `8a33067ad6deccebb01fb8774cc8162ab59cf3224a892c3bbf18f828320a6bf1`

## Input

- Source CSV: `owid_energy_IRN.csv`
- Source SHA-256: `c41bd93ed7a60c55...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `6b25c3708f69e244...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.5867 | 16.4371 | — |
| 1 | 1966 | 0.5782 | 16.4203 | 0.0415 |
| 2 | 1967 | 0.5666 | 16.4083 | 0.0457 |
| 3 | 1968 | 0.5586 | 16.3891 | 0.0356 |
| 4 | 1969 | 0.5685 | 16.4094 | 0.0693 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 0.7285 | 11.0461 | 0.5599 |
| 58 | 2023 | 0.7414 | 11.0670 | 0.4899 |
| 59 | 2024 | 0.7389 | 10.9985 | 0.3410 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Biofuel | +0.9911 | 26.5° | no |
| Coal | Oil | +0.9685 | 28.0° | no |
| Coal | Hydro | +0.9586 | 35.3° | no |
| Oil | Hydro | +0.9568 | 20.5° | no |
| Coal | Biofuel | +0.9373 | 38.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Wind | -0.8349 | 62.2° | no |
| Hydro | Wind | -0.8567 | 45.5° | no |
| Coal | Nuclear | -0.8695 | 131.0° | no |
| Oil | Nuclear | -0.8949 | 56.7° | no |
| Nuclear | Biofuel | -0.9124 | 54.9° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.333 | 4.939 | 5.212 | 7.175 |
| Coal | Oil | 0.333 | 4.939 | 4.333 | 7.942 |
| Coal | Nuclear | 0.333 | 4.939 | -6.290 | 1.286 |
| Coal | Hydro | 0.333 | 4.939 | 1.002 | 5.069 |
| Coal | Solar | 0.333 | 4.939 | -7.185 | -1.795 |
| Coal | Wind | 0.333 | 4.939 | -5.808 | -0.592 |
| Coal | Biofuel | 0.333 | 4.939 | -8.213 | -5.616 |
| Gas | Oil | 5.212 | 7.175 | 4.333 | 7.942 |
| Gas | Nuclear | 5.212 | 7.175 | -6.290 | 1.286 |
| Gas | Hydro | 5.212 | 7.175 | 1.002 | 5.069 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*