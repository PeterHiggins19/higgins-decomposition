# Stage 1 Report (pure CoDa) — energy_owid_chn

**Domain:** energy
**Description:** OWID primary-energy consumption composition for CHN (CHN), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: CHN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `5bc147d0e048316c3e9eb7b687ad43e456b9085e1ea79270fe9693177ae9308d`

## Input

- Source CSV: `owid_energy_CHN.csv`
- Source SHA-256: `8fc0c0031a06b89e...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `89954b2ffc121e65...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.4955 | 16.1053 | — |
| 1 | 1966 | 0.5260 | 16.1614 | 0.2015 |
| 2 | 1967 | 0.5494 | 16.2180 | 0.2017 |
| 3 | 1968 | 0.5838 | 16.2748 | 0.1734 |
| 4 | 1969 | 0.5916 | 16.2840 | 0.2470 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.3609 | 5.2498 | 0.2604 |
| 58 | 2023 | 1.3851 | 5.2031 | 0.2835 |
| 59 | 2024 | 1.4295 | 5.0749 | 0.3121 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Hydro | +0.9970 | 23.7° | no |
| Coal | Oil | +0.9926 | 11.0° | no |
| Oil | Hydro | +0.9897 | 26.6° | no |
| Gas | Oil | +0.9777 | 14.6° | no |
| Gas | Hydro | +0.9632 | 29.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Nuclear | -0.8773 | 80.8° | no |
| Gas | Wind | -0.9501 | 74.4° | no |
| Hydro | Wind | -0.9614 | 68.3° | no |
| Coal | Wind | -0.9666 | 38.9° | no |
| Oil | Wind | -0.9676 | 47.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.429 | 8.112 | 0.655 | 4.533 |
| Coal | Oil | 2.429 | 8.112 | 1.380 | 6.580 |
| Coal | Nuclear | 2.429 | 8.112 | -6.222 | 0.905 |
| Coal | Hydro | 2.429 | 8.112 | 0.381 | 5.036 |
| Coal | Solar | 2.429 | 8.112 | -7.100 | -0.097 |
| Coal | Wind | 2.429 | 8.112 | -5.806 | 0.075 |
| Coal | Biofuel | 2.429 | 8.112 | -7.756 | -2.486 |
| Gas | Oil | 0.655 | 4.533 | 1.380 | 6.580 |
| Gas | Nuclear | 0.655 | 4.533 | -6.222 | 0.905 |
| Gas | Hydro | 0.655 | 4.533 | 0.381 | 5.036 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*