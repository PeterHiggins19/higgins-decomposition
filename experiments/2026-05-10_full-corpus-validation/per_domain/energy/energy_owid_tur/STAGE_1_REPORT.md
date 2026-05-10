# Stage 1 Report (pure CoDa) — energy_owid_tur

**Domain:** energy
**Description:** OWID primary-energy consumption composition for TUR (TUR), annual TWh. T = 43 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: TUR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `705d8bbe3ad4231ae3fa89b21f81750b324793fe9b07fa06c0239018f5860050`

## Input

- Source CSV: `owid_energy_TUR.csv`
- Source SHA-256: `439a5211f931f61b...`
- Records (T): **43**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `e0b4e2906317d23e...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1982 | 0.9317 | 16.4979 | — |
| 1 | 1983 | 0.8976 | 16.4405 | 0.2681 |
| 2 | 1984 | 0.9306 | 16.4811 | 0.1642 |
| 3 | 1985 | 0.9175 | 16.4588 | 0.2771 |
| 4 | 1986 | 0.9428 | 16.7317 | 1.9406 |
| ... | ... | ... | ... | ... |
| 40 | 2022 | 1.5082 | 11.4471 | 0.2920 |
| 41 | 2023 | 1.5121 | 11.4397 | 0.2811 |
| 42 | 2024 | 1.5419 | 11.4668 | 0.2584 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Nuclear | +0.9987 | 36.2° | no |
| Oil | Nuclear | +0.9979 | 36.6° | no |
| Coal | Oil | +0.9964 | 3.8° | YES |
| Nuclear | Hydro | +0.9928 | 37.6° | no |
| Oil | Hydro | +0.9905 | 11.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Biofuel | -0.8383 | 47.6° | no |
| Nuclear | Wind | -0.9208 | 355.7° | no |
| Coal | Wind | -0.9220 | 65.5° | no |
| Hydro | Wind | -0.9292 | 81.6° | no |
| Oil | Wind | -0.9344 | 62.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.810 | 7.235 | 1.377 | 5.665 |
| Coal | Oil | 2.810 | 7.235 | 3.086 | 7.756 |
| Coal | Nuclear | 2.810 | 7.235 | -9.611 | -5.548 |
| Coal | Hydro | 2.810 | 7.235 | 1.715 | 6.137 |
| Coal | Solar | 2.810 | 7.235 | -7.713 | 0.901 |
| Coal | Wind | 2.810 | 7.235 | -6.140 | 1.166 |
| Coal | Biofuel | 2.810 | 7.235 | -6.814 | -0.635 |
| Gas | Oil | 1.377 | 5.665 | 3.086 | 7.756 |
| Gas | Nuclear | 1.377 | 5.665 | -9.611 | -5.548 |
| Gas | Hydro | 1.377 | 5.665 | 1.715 | 6.137 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*