# Stage 1 Report (pure CoDa) — energy_owid_kaz

**Domain:** energy
**Description:** OWID primary-energy consumption composition for KAZ (KAZ), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: KAZ

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `f4127c0c517849e6a94dbed462992105eec1476680a6f992255de4cb30032a0b`

## Input

- Source CSV: `owid_energy_KAZ.csv`
- Source SHA-256: `6657d2aa7d1e5831...`
- Records (T): **40**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `0d85e8c95270da69...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 1.0087 | 16.9331 | — |
| 1 | 1986 | 1.0115 | 16.9326 | 0.2330 |
| 2 | 1987 | 1.0140 | 16.9602 | 0.1631 |
| 3 | 1988 | 1.0199 | 16.9918 | 0.1583 |
| 4 | 1989 | 1.0441 | 15.8137 | 5.4183 |
| ... | ... | ... | ... | ... |
| 37 | 2022 | 1.1979 | 14.0729 | 0.2676 |
| 38 | 2023 | 1.1910 | 14.0754 | 0.4576 |
| 39 | 2024 | 1.2269 | 14.1263 | 0.2969 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Biofuel | +0.9986 | 21.1° | no |
| Oil | Biofuel | +0.9902 | 22.7° | no |
| Coal | Oil | +0.9833 | 3.5° | YES |
| Solar | Wind | +0.9754 | 244.0° | no |
| Gas | Biofuel | +0.9728 | 19.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Wind | Biofuel | -0.8228 | 53.6° | no |
| Coal | Solar | -0.8298 | 52.9° | no |
| Solar | Biofuel | -0.8352 | 47.7° | no |
| Oil | Wind | -0.8467 | 69.5° | no |
| Oil | Solar | -0.8559 | 57.6° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 4.802 | 7.389 | 4.107 | 6.192 |
| Coal | Oil | 4.802 | 7.389 | 4.032 | 6.730 |
| Coal | Nuclear | 4.802 | 7.389 | -8.287 | 0.557 |
| Coal | Hydro | 4.802 | 7.389 | 1.914 | 4.950 |
| Coal | Solar | 4.802 | 7.389 | -6.970 | 0.392 |
| Coal | Wind | 4.802 | 7.389 | -6.970 | 1.256 |
| Coal | Biofuel | 4.802 | 7.389 | -8.287 | -5.912 |
| Gas | Oil | 4.107 | 6.192 | 4.032 | 6.730 |
| Gas | Nuclear | 4.107 | 6.192 | -8.287 | 0.557 |
| Gas | Hydro | 4.107 | 6.192 | 1.914 | 4.950 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*