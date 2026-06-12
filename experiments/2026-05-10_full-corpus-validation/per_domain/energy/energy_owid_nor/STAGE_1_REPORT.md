# Stage 1 Report (pure CoDa) — energy_owid_nor

**Domain:** energy
**Description:** OWID primary-energy consumption composition for NOR (NOR), annual TWh. T = 48 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: NOR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `810c4ce5a740b0ede3943dae639608dc95b3d4985c72457fff99627c01fb3450`

## Input

- Source CSV: `owid_energy_NOR.csv`
- Source SHA-256: `8c3aa6928f3dd384...`
- Records (T): **48**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `4524d0913fcea67c...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1977 | 0.8180 | 16.5172 | — |
| 1 | 1978 | 0.8316 | 16.5839 | 0.3973 |
| 2 | 1979 | 0.8337 | 16.6232 | 0.1724 |
| 3 | 1980 | 0.8432 | 16.6462 | 0.1202 |
| 4 | 1981 | 0.8211 | 16.6434 | 0.2112 |
| ... | ... | ... | ... | ... |
| 45 | 2022 | 1.1268 | 11.2098 | 0.5273 |
| 46 | 2023 | 1.0952 | 11.0468 | 0.6970 |
| 47 | 2024 | 1.0897 | 10.9657 | 0.4357 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Hydro | +0.9996 | 29.5° | no |
| Oil | Nuclear | +0.9973 | 33.2° | no |
| Coal | Oil | +0.9961 | 26.5° | no |
| Oil | Hydro | +0.9954 | 6.9° | YES |
| Coal | Nuclear | +0.9950 | 36.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Biofuel | -0.9277 | 70.6° | no |
| Hydro | Wind | -0.9402 | 63.2° | no |
| Nuclear | Wind | -0.9403 | 359.2° | no |
| Oil | Wind | -0.9432 | 75.0° | no |
| Coal | Wind | -0.9481 | 132.6° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.413 | 4.591 | 1.754 | 5.170 |
| Coal | Oil | 0.413 | 4.591 | 2.916 | 6.980 |
| Coal | Nuclear | 0.413 | 4.591 | -9.302 | -5.726 |
| Coal | Hydro | 0.413 | 4.591 | 4.068 | 7.674 |
| Coal | Solar | 0.413 | 4.591 | -6.492 | -1.462 |
| Coal | Wind | 0.413 | 4.591 | -5.836 | 1.986 |
| Coal | Biofuel | 0.413 | 4.591 | -7.265 | 0.440 |
| Gas | Oil | 1.754 | 5.170 | 2.916 | 6.980 |
| Gas | Nuclear | 1.754 | 5.170 | -9.302 | -5.726 |
| Gas | Hydro | 1.754 | 5.170 | 4.068 | 7.674 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*