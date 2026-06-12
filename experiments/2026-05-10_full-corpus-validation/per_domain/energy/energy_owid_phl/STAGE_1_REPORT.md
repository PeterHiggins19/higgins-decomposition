# Stage 1 Report (pure CoDa) — energy_owid_phl

**Domain:** energy
**Description:** OWID primary-energy consumption composition for PHL (PHL), annual TWh. T = 31 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: PHL

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `5d29809a61016cec0bbc33d0dbf32d324d31318b4dba2165d63ba2d8f4574206`

## Input

- Source CSV: `owid_energy_PHL.csv`
- Source SHA-256: `cc662ed7209d293b...`
- Records (T): **31**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `a33fd5b6ededf4bf...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1994 | 0.5629 | 15.9467 | — |
| 1 | 1995 | 0.5330 | 15.8890 | 0.1831 |
| 2 | 1996 | 0.5887 | 15.9930 | 0.4495 |
| 3 | 1997 | 0.5753 | 15.9445 | 0.5967 |
| 4 | 1998 | 0.5773 | 15.9398 | 0.5617 |
| ... | ... | ... | ... | ... |
| 28 | 2022 | 1.1459 | 10.9174 | 0.3311 |
| 29 | 2023 | 1.1512 | 10.8931 | 0.2953 |
| 30 | 2024 | 1.1596 | 10.8973 | 0.3352 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9996 | 37.5° | no |
| Nuclear | Hydro | +0.9921 | 41.7° | no |
| Oil | Hydro | +0.9916 | 17.9° | no |
| Coal | Nuclear | +0.9887 | 31.8° | no |
| Coal | Oil | +0.9852 | 9.3° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Biofuel | -0.9317 | 57.4° | no |
| Hydro | Wind | -0.9529 | 31.3° | no |
| Oil | Wind | -0.9588 | 32.1° | no |
| Nuclear | Wind | -0.9632 | 41.3° | no |
| Coal | Wind | -0.9730 | 37.1° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 3.403 | 6.830 | 0.041 | 5.400 |
| Coal | Oil | 3.403 | 6.830 | 3.597 | 8.465 |
| Coal | Nuclear | 3.403 | 6.830 | -9.379 | -5.185 |
| Coal | Hydro | 3.403 | 6.830 | 1.215 | 6.046 |
| Coal | Solar | 3.403 | 6.830 | -6.217 | 0.232 |
| Coal | Wind | 3.403 | 6.830 | -6.217 | -0.600 |
| Coal | Biofuel | 3.403 | 6.830 | -6.016 | 0.994 |
| Gas | Oil | 0.041 | 5.400 | 3.597 | 8.465 |
| Gas | Nuclear | 0.041 | 5.400 | -9.379 | -5.185 |
| Gas | Hydro | 0.041 | 5.400 | 1.215 | 6.046 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*