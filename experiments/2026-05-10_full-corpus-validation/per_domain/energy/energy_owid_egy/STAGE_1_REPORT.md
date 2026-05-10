# Stage 1 Report (pure CoDa) — energy_owid_egy

**Domain:** energy
**Description:** OWID primary-energy consumption composition for EGY (EGY), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: EGY

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `0759be1d8f6fc93be6448a7dd2bff5115fed512a2e6743a0d024f7799389ceb7`

## Input

- Source CSV: `owid_energy_EGY.csv`
- Source SHA-256: `7fdec2eeb194e740...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `c718ee0ac412ca3e...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.4376 | 15.9732 | — |
| 1 | 1966 | 0.3844 | 15.8549 | 0.4300 |
| 2 | 1967 | 0.5048 | 16.1343 | 0.5650 |
| 3 | 1968 | 0.5626 | 16.2056 | 0.3491 |
| 4 | 1969 | 0.7334 | 16.5135 | 0.5993 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 0.9657 | 13.7889 | 0.2354 |
| 58 | 2023 | 0.9727 | 13.8029 | 0.1141 |
| 59 | 2024 | 0.9949 | 13.8405 | 0.3390 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Oil | Nuclear | +0.9982 | 26.8° | no |
| Oil | Biofuel | +0.9982 | 26.8° | no |
| Oil | Hydro | +0.9768 | 13.7° | no |
| Hydro | Biofuel | +0.9762 | 33.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Wind | -0.9284 | 79.9° | no |
| Coal | Wind | -0.9337 | 109.9° | no |
| Nuclear | Wind | -0.9413 | 358.1° | no |
| Wind | Biofuel | -0.9413 | 55.1° | no |
| Oil | Wind | -0.9430 | 55.6° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.895 | 5.501 | 2.685 | 6.674 |
| Coal | Oil | 0.895 | 5.501 | 4.639 | 8.266 |
| Coal | Nuclear | 0.895 | 5.501 | -8.143 | -5.455 |
| Coal | Hydro | 0.895 | 5.501 | 2.207 | 6.354 |
| Coal | Solar | 0.895 | 5.501 | -6.614 | 1.344 |
| Coal | Wind | 0.895 | 5.501 | -5.920 | 1.434 |
| Coal | Biofuel | 0.895 | 5.501 | -8.143 | -5.455 |
| Gas | Oil | 2.685 | 6.674 | 4.639 | 8.266 |
| Gas | Nuclear | 2.685 | 6.674 | -8.143 | -5.455 |
| Gas | Hydro | 2.685 | 6.674 | 2.207 | 6.354 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*