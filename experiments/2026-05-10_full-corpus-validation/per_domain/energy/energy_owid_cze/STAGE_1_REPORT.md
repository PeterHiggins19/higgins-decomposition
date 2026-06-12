# Stage 1 Report (pure CoDa) — energy_owid_cze

**Domain:** energy
**Description:** OWID primary-energy consumption composition for CZE (CZE), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: CZE

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `52a45f287d41c348b218414504548718e6a73728f4e03da4d4bfc6cf3de00808`

## Input

- Source CSV: `owid_energy_CZE.csv`
- Source SHA-256: `eba35473ac59dd40...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `121b78052482d0ef...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.4461 | 15.9146 | — |
| 1 | 1966 | 0.4645 | 15.9349 | 0.1182 |
| 2 | 1967 | 0.4978 | 15.9975 | 0.2383 |
| 3 | 1968 | 0.5075 | 15.9886 | 0.3459 |
| 4 | 1969 | 0.5088 | 15.9605 | 0.2439 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.5002 | 4.8006 | 0.3077 |
| 58 | 2023 | 1.5364 | 4.5907 | 0.3101 |
| 59 | 2024 | 1.5719 | 4.3992 | 0.3433 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9939 | 11.4° | no |
| Coal | Hydro | +0.9912 | 60.1° | no |
| Oil | Hydro | +0.9878 | 74.0° | no |
| Gas | Oil | +0.9211 | 13.6° | no |
| Coal | Gas | +0.9069 | 15.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Biofuel | -0.7773 | 93.9° | no |
| Oil | Biofuel | -0.8028 | 43.2° | no |
| Gas | Solar | -0.8034 | 36.7° | no |
| Coal | Biofuel | -0.8091 | 38.8° | no |
| Gas | Wind | -0.8270 | 20.9° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.635 | 8.208 | 1.234 | 5.177 |
| Coal | Oil | 1.635 | 8.208 | 1.662 | 6.686 |
| Coal | Nuclear | 1.635 | 8.208 | -5.733 | 4.009 |
| Coal | Hydro | 1.635 | 8.208 | -1.542 | 4.014 |
| Coal | Solar | 1.635 | 8.208 | -8.772 | -0.799 |
| Coal | Wind | 1.635 | 8.208 | -8.166 | -2.402 |
| Coal | Biofuel | 1.635 | 8.208 | -7.116 | -0.871 |
| Gas | Oil | 1.234 | 5.177 | 1.662 | 6.686 |
| Gas | Nuclear | 1.234 | 5.177 | -5.733 | 4.009 |
| Gas | Hydro | 1.234 | 5.177 | -1.542 | 4.014 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*