# Stage 1 Report (pure CoDa) — energy_owid_jpn

**Domain:** energy
**Description:** OWID primary-energy consumption composition for JPN (JPN), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: JPN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `0431614f3f08f8ab320ad4350dd56672e8144d8f982fb71a4d102ab7a66df3a1`

## Input

- Source CSV: `owid_energy_JPN.csv`
- Source SHA-256: `5b8caf4dc56eeb1a...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `1d2635b3d6e67685...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.9839 | 15.8703 | — |
| 1 | 1966 | 0.9576 | 15.5671 | 2.8584 |
| 2 | 1967 | 0.9035 | 15.4868 | 0.2549 |
| 3 | 1968 | 0.8852 | 15.4701 | 0.4008 |
| 4 | 1969 | 0.8401 | 15.4095 | 0.1712 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.4428 | 5.4580 | 0.1886 |
| 58 | 2023 | 1.4780 | 5.3759 | 0.4075 |
| 59 | 2024 | 1.5041 | 5.2857 | 0.1711 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Hydro | +0.9960 | 42.4° | no |
| Oil | Hydro | +0.9897 | 39.5° | no |
| Coal | Oil | +0.9842 | 6.7° | YES |
| Solar | Wind | +0.9177 | 62.6° | no |
| Solar | Biofuel | +0.6583 | 52.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Wind | -0.8821 | 54.6° | no |
| Oil | Wind | -0.9049 | 39.5° | no |
| Coal | Solar | -0.9145 | 63.6° | no |
| Hydro | Solar | -0.9312 | 206.6° | no |
| Oil | Solar | -0.9479 | 56.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.832 | 6.348 | 1.507 | 4.114 |
| Coal | Oil | 1.832 | 6.348 | 2.180 | 6.938 |
| Coal | Nuclear | 1.832 | 6.348 | -8.987 | 4.254 |
| Coal | Hydro | 1.832 | 6.348 | -0.071 | 5.362 |
| Coal | Solar | 1.832 | 6.348 | -7.403 | 0.339 |
| Coal | Wind | 1.832 | 6.348 | -7.890 | -1.208 |
| Coal | Biofuel | 1.832 | 6.348 | -9.074 | -2.618 |
| Gas | Oil | 1.507 | 4.114 | 2.180 | 6.938 |
| Gas | Nuclear | 1.507 | 4.114 | -8.987 | 4.254 |
| Gas | Hydro | 1.507 | 4.114 | -0.071 | 5.362 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*