# Stage 1 Report (pure CoDa) — energy_owid_ven

**Domain:** energy
**Description:** OWID primary-energy consumption composition for VEN (VEN), annual TWh. T = 58 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: VEN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `0733188bfa9e8449d03c4cc7ce2a4330e35b03cd4832fc93a2fb565bb0037a14`

## Input

- Source CSV: `owid_energy_VEN.csv`
- Source SHA-256: `6818dbbba80792dd...`
- Records (T): **58**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `e48982decd0766ee...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.7664 | 16.0596 | — |
| 1 | 1966 | 0.7729 | 16.0697 | 0.0573 |
| 2 | 1967 | 0.7851 | 16.0979 | 0.1108 |
| 3 | 1968 | 0.8167 | 16.2168 | 0.4280 |
| 4 | 1969 | 0.8330 | 16.2566 | 0.1309 |
| ... | ... | ... | ... | ... |
| 55 | 2022 | 1.0826 | 15.2404 | 1.1489 |
| 56 | 2023 | 1.0944 | 15.2763 | 0.1820 |
| 57 | 2024 | 1.0832 | 15.1608 | 0.3545 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Gas | Nuclear | +0.9725 | 13.8° | no |
| Gas | Biofuel | +0.9725 | 13.8° | no |
| Oil | Nuclear | +0.9176 | 13.7° | no |
| Oil | Biofuel | +0.9176 | 13.7° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Solar | -0.7009 | 12.7° | no |
| Gas | Wind | -0.7936 | 32.3° | no |
| Oil | Wind | -0.8666 | 30.8° | no |
| Nuclear | Wind | -0.8733 | 35.8° | no |
| Wind | Biofuel | -0.8733 | 35.8° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -1.093 | 3.546 | 5.946 | 7.658 |
| Coal | Oil | -1.093 | 3.546 | 6.010 | 7.886 |
| Coal | Nuclear | -1.093 | 3.546 | -6.752 | -5.273 |
| Coal | Hydro | -1.093 | 3.546 | 4.503 | 6.944 |
| Coal | Solar | -1.093 | 3.546 | -5.897 | -3.479 |
| Coal | Wind | -1.093 | 3.546 | -6.038 | -1.091 |
| Coal | Biofuel | -1.093 | 3.546 | -6.752 | -5.273 |
| Gas | Oil | 5.946 | 7.658 | 6.010 | 7.886 |
| Gas | Nuclear | 5.946 | 7.658 | -6.752 | -5.273 |
| Gas | Hydro | 5.946 | 7.658 | 4.503 | 6.944 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*