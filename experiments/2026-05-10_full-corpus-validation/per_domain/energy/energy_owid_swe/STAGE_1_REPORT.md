# Stage 1 Report (pure CoDa) — energy_owid_swe

**Domain:** energy
**Description:** OWID primary-energy consumption composition for SWE (SWE), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: SWE

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `4a48c91f30b3282e33ffa1c74b15ce114ed44e123896ca3490f559571623fd9e`

## Input

- Source CSV: `owid_energy_SWE.csv`
- Source SHA-256: `396b7956d1689868...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `0c19afc4101c2e0d...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.8573 | 16.2923 | — |
| 1 | 1966 | 0.8244 | 16.2417 | 0.8272 |
| 2 | 1967 | 0.8326 | 16.2478 | 0.1046 |
| 3 | 1968 | 0.7873 | 16.1630 | 0.7882 |
| 4 | 1969 | 0.7477 | 16.1283 | 0.9402 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.6407 | 3.6985 | 0.4914 |
| 58 | 2023 | 1.6659 | 3.3990 | 0.4703 |
| 59 | 2024 | 1.6340 | 3.8550 | 1.3303 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9971 | 9.2° | YES |
| Coal | Hydro | +0.9942 | 63.8° | no |
| Coal | Oil | +0.9920 | 65.5° | no |
| Wind | Biofuel | +0.6554 | 92.9° | no |
| Gas | Wind | +0.6492 | 332.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Oil | -0.7032 | 66.5° | no |
| Coal | Biofuel | -0.7115 | 90.9° | no |
| Coal | Wind | -0.9536 | 189.4° | no |
| Hydro | Wind | -0.9595 | 77.7° | no |
| Oil | Wind | -0.9627 | 78.9° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.701 | 5.867 | -6.473 | 1.510 |
| Coal | Oil | -0.701 | 5.867 | 1.240 | 8.177 |
| Coal | Nuclear | -0.701 | 5.867 | -0.384 | 6.106 |
| Coal | Hydro | -0.701 | 5.867 | 1.456 | 7.471 |
| Coal | Solar | -0.701 | 5.867 | -7.880 | -1.227 |
| Coal | Wind | -0.701 | 5.867 | -6.018 | 1.053 |
| Coal | Biofuel | -0.701 | 5.867 | -8.413 | -0.730 |
| Gas | Oil | -6.473 | 1.510 | 1.240 | 8.177 |
| Gas | Nuclear | -6.473 | 1.510 | -0.384 | 6.106 |
| Gas | Hydro | -6.473 | 1.510 | 1.456 | 7.471 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*