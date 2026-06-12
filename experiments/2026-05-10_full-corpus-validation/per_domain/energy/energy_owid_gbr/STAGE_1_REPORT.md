# Stage 1 Report (pure CoDa) — energy_owid_gbr

**Domain:** energy
**Description:** OWID primary-energy consumption composition for GBR (GBR), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: GBR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `1a7ec8b7a7c3520f9f2e80eab2c87d51addf3ccba0e4f189e8236862545f100c`

## Input

- Source CSV: `owid_energy_GBR.csv`
- Source SHA-256: `7360a9a3c80c2ca2...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `5bf31c323f2d3cad...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.8013 | 15.2159 | — |
| 1 | 1966 | 0.8295 | 15.2751 | 0.2864 |
| 2 | 1967 | 0.8615 | 15.3769 | 0.4871 |
| 3 | 1968 | 0.8913 | 15.4738 | 0.8206 |
| 4 | 1969 | 0.9333 | 15.5854 | 0.6366 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.4145 | 3.9764 | 0.3609 |
| 58 | 2023 | 1.4114 | 3.9072 | 0.2765 |
| 59 | 2024 | 1.4168 | 3.8656 | 0.1216 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9913 | 61.6° | no |
| Coal | Oil | +0.9841 | 65.5° | no |
| Coal | Hydro | +0.9752 | 126.9° | no |
| Oil | Nuclear | +0.9480 | 34.9° | no |
| Nuclear | Hydro | +0.9477 | 120.7° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Wind | -0.8997 | 186.1° | no |
| Nuclear | Solar | -0.9115 | 26.4° | no |
| Hydro | Wind | -0.9145 | 359.1° | no |
| Oil | Wind | -0.9177 | 72.6° | no |
| Nuclear | Biofuel | -0.9619 | 38.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.695 | 6.689 | 1.561 | 5.177 |
| Coal | Oil | -0.695 | 6.689 | 1.940 | 6.290 |
| Coal | Nuclear | -0.695 | 6.689 | 0.050 | 3.971 |
| Coal | Hydro | -0.695 | 6.689 | -1.998 | 2.020 |
| Coal | Solar | -0.695 | 6.689 | -8.076 | -0.959 |
| Coal | Wind | -0.695 | 6.689 | -7.216 | 0.778 |
| Coal | Biofuel | -0.695 | 6.689 | -8.135 | -1.223 |
| Gas | Oil | 1.561 | 5.177 | 1.940 | 6.290 |
| Gas | Nuclear | 1.561 | 5.177 | 0.050 | 3.971 |
| Gas | Hydro | 1.561 | 5.177 | -1.998 | 2.020 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*