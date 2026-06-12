# Stage 1 Report (pure CoDa) — energy_owid_esp

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ESP (ESP), annual TWh. T = 57 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ESP

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `24e06d3f427b3a1c34e2ec8d99eb200c6fff0b41a7a4fd37639af0ed2ac9774b`

## Input

- Source CSV: `owid_energy_ESP.csv`
- Source SHA-256: `562aeb8f4a0ea6f4...`
- Records (T): **57**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `d8ed5e10c1b6a70f...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1968 | 0.9533 | 16.4976 | — |
| 1 | 1969 | 0.9864 | 15.5705 | 7.0847 |
| 2 | 1970 | 0.9416 | 15.5153 | 0.3263 |
| 3 | 1971 | 0.9888 | 15.7475 | 1.6073 |
| 4 | 1972 | 1.0628 | 15.9648 | 1.0155 |
| ... | ... | ... | ... | ... |
| 54 | 2022 | 1.5571 | 3.0600 | 0.6218 |
| 55 | 2023 | 1.6073 | 2.8901 | 0.6415 |
| 56 | 2024 | 1.5931 | 3.0901 | 0.5093 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9894 | 65.5° | no |
| Coal | Oil | +0.9817 | 78.8° | no |
| Coal | Hydro | +0.9661 | 345.9° | no |
| Solar | Biofuel | +0.8293 | 62.6° | no |
| Coal | Nuclear | +0.8227 | 167.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Solar | -0.8929 | 133.4° | no |
| Hydro | Wind | -0.8976 | 352.3° | no |
| Hydro | Solar | -0.9258 | 343.4° | no |
| Oil | Solar | -0.9498 | 62.1° | no |
| Coal | Solar | -0.9639 | 345.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -1.422 | 6.933 | -5.497 | 3.162 |
| Coal | Oil | -1.422 | 6.933 | 1.758 | 7.792 |
| Coal | Nuclear | -1.422 | 6.933 | 0.159 | 4.442 |
| Coal | Hydro | -1.422 | 6.933 | -0.920 | 6.473 |
| Coal | Solar | -1.422 | 6.933 | -7.400 | 0.193 |
| Coal | Wind | -1.422 | 6.933 | -7.400 | 1.225 |
| Coal | Biofuel | -1.422 | 6.933 | -9.341 | -1.307 |
| Gas | Oil | -5.497 | 3.162 | 1.758 | 7.792 |
| Gas | Nuclear | -5.497 | 3.162 | 0.159 | 4.442 |
| Gas | Hydro | -5.497 | 3.162 | -0.920 | 6.473 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*