# Stage 1 Report (pure CoDa) — energy_owid_per

**Domain:** energy
**Description:** OWID primary-energy consumption composition for PER (PER), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: PER

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `0041be2753b42d6951ad685933c5fbd51b2e5d4c489195a9e271c89db0663a3d`

## Input

- Source CSV: `owid_energy_PER.csv`
- Source SHA-256: `7a9cbc3266d3a78e...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `e91a3daa7e87536d...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.6728 | 16.3952 | — |
| 1 | 1966 | 0.6196 | 16.3229 | 0.1892 |
| 2 | 1967 | 0.6334 | 16.3509 | 0.1609 |
| 3 | 1968 | 0.6582 | 16.3914 | 0.1036 |
| 4 | 1969 | 0.7037 | 16.5358 | 0.4835 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.3130 | 10.9770 | 0.1328 |
| 58 | 2023 | 1.3141 | 10.9648 | 0.2297 |
| 59 | 2024 | 1.3357 | 10.9613 | 0.4912 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9990 | 35.4° | no |
| Nuclear | Hydro | +0.9824 | 33.8° | no |
| Oil | Hydro | +0.9749 | 5.7° | YES |
| Coal | Hydro | +0.9594 | 29.8° | no |
| Coal | Nuclear | +0.9199 | 36.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | -0.8748 | 358.8° | no |
| Nuclear | Wind | -0.8749 | 359.7° | no |
| Gas | Wind | -0.8828 | 67.6° | no |
| Oil | Biofuel | -0.8838 | 58.8° | no |
| Coal | Solar | -0.8864 | 43.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.286 | 4.637 | 2.980 | 5.428 |
| Coal | Oil | 0.286 | 4.637 | 3.324 | 7.957 |
| Coal | Nuclear | 0.286 | 4.637 | -9.579 | -5.651 |
| Coal | Hydro | 0.286 | 4.637 | 2.690 | 6.773 |
| Coal | Solar | 0.286 | 4.637 | -7.555 | -0.435 |
| Coal | Wind | 0.286 | 4.637 | -6.036 | 0.588 |
| Coal | Biofuel | 0.286 | 4.637 | -6.258 | 1.690 |
| Gas | Oil | 2.980 | 5.428 | 3.324 | 7.957 |
| Gas | Nuclear | 2.980 | 5.428 | -9.579 | -5.651 |
| Gas | Hydro | 2.980 | 5.428 | 2.690 | 6.773 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*