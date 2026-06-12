# Stage 1 Report (pure CoDa) — energy_owid_rou

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ROU (ROU), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ROU

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `7bf9321ae3ef22c19d89c5509f4f752a691f5c23eceb8aa256a91cf219440f7a`

## Input

- Source CSV: `owid_energy_ROU.csv`
- Source SHA-256: `2e6802ff80080c94...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `2d3022bcbc86d8cb...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.0634 | 16.9179 | — |
| 1 | 1966 | 1.0602 | 16.9127 | 0.0415 |
| 2 | 1967 | 1.0717 | 16.9622 | 0.2315 |
| 3 | 1968 | 1.0756 | 16.9630 | 0.0318 |
| 4 | 1969 | 1.0822 | 17.0045 | 0.2028 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.6642 | 3.2093 | 0.3389 |
| 58 | 2023 | 1.6633 | 3.1723 | 0.4323 |
| 59 | 2024 | 1.6432 | 2.8395 | 0.8219 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Oil | +0.9987 | 10.6° | no |
| Coal | Gas | +0.9945 | 45.6° | no |
| Coal | Oil | +0.9915 | 47.2° | no |
| Coal | Hydro | +0.9620 | 83.7° | no |
| Oil | Hydro | +0.9493 | 32.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Wind | -0.8676 | 43.2° | no |
| Oil | Wind | -0.8732 | 45.0° | no |
| Hydro | Biofuel | -0.8783 | 50.0° | no |
| Coal | Wind | -0.8882 | 81.4° | no |
| Hydro | Wind | -0.9241 | 39.6° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.057 | 6.394 | 1.257 | 7.262 |
| Coal | Oil | -0.057 | 6.394 | 1.429 | 6.738 |
| Coal | Nuclear | -0.057 | 6.394 | -6.233 | 3.048 |
| Coal | Hydro | -0.057 | 6.394 | 0.227 | 5.197 |
| Coal | Solar | -0.057 | 6.394 | -8.845 | -0.873 |
| Coal | Wind | -0.057 | 6.394 | -7.460 | -0.337 |
| Coal | Biofuel | -0.057 | 6.394 | -7.672 | -1.382 |
| Gas | Oil | 1.257 | 7.262 | 1.429 | 6.738 |
| Gas | Nuclear | 1.257 | 7.262 | -6.233 | 3.048 |
| Gas | Hydro | 1.257 | 7.262 | 0.227 | 5.197 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*