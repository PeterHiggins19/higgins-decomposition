# Stage 1 Report (pure CoDa) — energy_owid_che

**Domain:** energy
**Description:** OWID primary-energy consumption composition for CHE (CHE), annual TWh. T = 56 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: CHE

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `6f33b3b9f698fd0c21f28fc4823f7e5f14251c2ef6eac293725d2129b0c1bf9a`

## Input

- Source CSV: `owid_energy_CHE.csv`
- Source SHA-256: `4b94dbe63690962a...`
- Records (T): **56**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `d79f979e396618d9...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1969 | 0.8355 | 15.7831 | — |
| 1 | 1970 | 0.8621 | 15.4525 | 4.6441 |
| 2 | 1971 | 0.8175 | 15.3715 | 0.9881 |
| 3 | 1972 | 0.8606 | 15.5475 | 1.0260 |
| 4 | 1973 | 0.9074 | 15.6244 | 0.4469 |
| ... | ... | ... | ... | ... |
| 53 | 2022 | 1.4780 | 5.7437 | 0.4571 |
| 54 | 2023 | 1.4696 | 5.8078 | 0.3949 |
| 55 | 2024 | 1.4718 | 5.8311 | 0.2818 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9959 | 5.2° | YES |
| Coal | Oil | +0.9809 | 81.3° | no |
| Coal | Hydro | +0.9796 | 83.7° | no |
| Solar | Wind | +0.8861 | 49.0° | no |
| Nuclear | Hydro | +0.8337 | 21.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Wind | -0.9096 | 17.8° | no |
| Nuclear | Biofuel | -0.9249 | 25.8° | no |
| Hydro | Solar | -0.9314 | 60.1° | no |
| Oil | Solar | -0.9383 | 57.6° | no |
| Coal | Solar | -0.9473 | 356.8° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -2.593 | 4.604 | -3.567 | 3.585 |
| Coal | Oil | -2.593 | 4.604 | 2.243 | 7.320 |
| Coal | Nuclear | -2.593 | 4.604 | 1.590 | 4.958 |
| Coal | Hydro | -2.593 | 4.604 | 1.970 | 6.787 |
| Coal | Solar | -2.593 | 4.604 | -7.283 | 0.234 |
| Coal | Wind | -2.593 | 4.604 | -7.704 | -3.219 |
| Coal | Biofuel | -2.593 | 4.604 | -8.270 | -1.538 |
| Gas | Oil | -3.567 | 3.585 | 2.243 | 7.320 |
| Gas | Nuclear | -3.567 | 3.585 | 1.590 | 4.958 |
| Gas | Hydro | -3.567 | 3.585 | 1.970 | 6.787 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*