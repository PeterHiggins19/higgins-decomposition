# Stage 1 Report (pure CoDa) — energy_owid_ind

**Domain:** energy
**Description:** OWID primary-energy consumption composition for IND (IND), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: IND

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `bb1607806bce6a6ab4fdd53b24dc958014576fc0e333fefbbfbbf11bac907f6c`

## Input

- Source CSV: `owid_energy_IND.csv`
- Source SHA-256: `26580b2dc5076db1...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `f413d65cce0e467b...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.8427 | 16.5170 | — |
| 1 | 1966 | 0.8662 | 16.5522 | 0.1107 |
| 2 | 1967 | 0.8872 | 16.6187 | 0.2471 |
| 3 | 1968 | 0.9132 | 16.6563 | 0.0925 |
| 4 | 1969 | 0.9497 | 15.5477 | 7.3397 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.2119 | 4.5266 | 0.3939 |
| 58 | 2023 | 1.1926 | 4.4435 | 0.3034 |
| 59 | 2024 | 1.2152 | 4.2617 | 0.2822 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9969 | 7.1° | YES |
| Oil | Hydro | +0.9963 | 46.7° | no |
| Coal | Hydro | +0.9946 | 42.5° | no |
| Gas | Oil | +0.8090 | 22.2° | no |
| Coal | Gas | +0.7835 | 22.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Biofuel | -0.8449 | 21.9° | no |
| Coal | Wind | -0.8772 | 43.5° | no |
| Oil | Wind | -0.8807 | 45.3° | no |
| Gas | Solar | -0.8887 | 35.8° | no |
| Hydro | Wind | -0.8954 | 88.2° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.619 | 7.739 | 0.395 | 3.663 |
| Coal | Oil | 2.619 | 7.739 | 1.874 | 6.767 |
| Coal | Nuclear | 2.619 | 7.739 | -5.754 | 1.958 |
| Coal | Hydro | 2.619 | 7.739 | -0.197 | 5.786 |
| Coal | Solar | 2.619 | 7.739 | -7.886 | -0.332 |
| Coal | Wind | 2.619 | 7.739 | -7.107 | -0.395 |
| Coal | Biofuel | 2.619 | 7.739 | -8.240 | -2.279 |
| Gas | Oil | 0.395 | 3.663 | 1.874 | 6.767 |
| Gas | Nuclear | 0.395 | 3.663 | -5.754 | 1.958 |
| Gas | Hydro | 0.395 | 3.663 | -0.197 | 5.786 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*