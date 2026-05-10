# Stage 1 Report (pure CoDa) — energy_owid_isr

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ISR (ISR), annual TWh. T = 44 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ISR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `374490c20c48d448df6f4722d3a7367052b1f58761db81a91262c733a06561fd`

## Input

- Source CSV: `owid_energy_ISR.csv`
- Source SHA-256: `e1d866e249ece6ce...`
- Records (T): **44**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `89436eb6c53c24b5...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1981 | 0.0039 | 12.6826 | — |
| 1 | 1982 | 0.2641 | 14.9767 | 6.1389 |
| 2 | 1983 | 0.4022 | 15.3543 | 1.0006 |
| 3 | 1984 | 0.5114 | 15.4265 | 0.7559 |
| 4 | 1985 | 0.5566 | 15.4844 | 0.1706 |
| ... | ... | ... | ... | ... |
| 41 | 2022 | 1.1856 | 11.8403 | 1.3332 |
| 42 | 2023 | 1.2152 | 11.7746 | 0.8123 |
| 43 | 2024 | 1.2345 | 11.7687 | 0.3224 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9994 | 46.1° | no |
| Nuclear | Hydro | +0.9113 | 357.0° | no |
| Oil | Hydro | +0.9055 | 48.8° | no |
| Wind | Biofuel | +0.8171 | 350.4° | no |
| Coal | Hydro | +0.7796 | 74.6° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Solar | -0.7901 | 112.2° | no |
| Oil | Solar | -0.7983 | 78.6° | no |
| Nuclear | Solar | -0.8021 | 355.4° | no |
| Oil | Biofuel | -0.8327 | 33.8° | no |
| Nuclear | Biofuel | -0.8341 | 357.6° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.313 | 7.923 | -0.344 | 5.175 |
| Coal | Oil | 1.313 | 7.923 | 4.134 | 10.312 |
| Coal | Nuclear | 1.313 | 7.923 | -8.803 | -3.505 |
| Coal | Hydro | 1.313 | 7.923 | -3.475 | 1.332 |
| Coal | Solar | 1.313 | 7.923 | -6.782 | 2.601 |
| Coal | Wind | 1.313 | 7.923 | -4.959 | -0.426 |
| Coal | Biofuel | 1.313 | 7.923 | -5.227 | 0.139 |
| Gas | Oil | -0.344 | 5.175 | 4.134 | 10.312 |
| Gas | Nuclear | -0.344 | 5.175 | -8.803 | -3.505 |
| Gas | Hydro | -0.344 | 5.175 | -3.475 | 1.332 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*