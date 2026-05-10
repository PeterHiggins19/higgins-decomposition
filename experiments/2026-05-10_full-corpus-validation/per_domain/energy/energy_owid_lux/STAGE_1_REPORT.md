# Stage 1 Report (pure CoDa) — energy_owid_lux

**Domain:** energy
**Description:** OWID primary-energy consumption composition for LUX (LUX), annual TWh. T = 56 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: LUX

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `a712c9fe64ce0e5c359896a261c0f141073c90d97b9f47066019e8d3406e35e3`

## Input

- Source CSV: `owid_energy_LUX.csv`
- Source SHA-256: `79fc36c85a87c8c0...`
- Records (T): **56**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `546d268d0d8967f6...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1969 | 0.6667 | 15.6182 | — |
| 1 | 1970 | 0.6789 | 15.7238 | 0.8096 |
| 2 | 1971 | 0.6946 | 15.7574 | 0.9092 |
| 3 | 1972 | 0.7847 | 16.2488 | 1.9125 |
| 4 | 1973 | 0.8511 | 16.3947 | 0.6469 |
| ... | ... | ... | ... | ... |
| 53 | 2022 | 0.8750 | 10.7002 | 0.6973 |
| 54 | 2023 | 0.9003 | 10.7362 | 0.8080 |
| 55 | 2024 | 0.9310 | 10.7525 | 0.5035 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9889 | 31.5° | no |
| Nuclear | Hydro | +0.9808 | 359.3° | no |
| Oil | Hydro | +0.9793 | 35.5° | no |
| Coal | Nuclear | +0.9787 | 61.8° | no |
| Coal | Hydro | +0.9522 | 177.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Biofuel | -0.9211 | 69.8° | no |
| Coal | Wind | -0.9227 | 162.2° | no |
| Nuclear | Solar | -0.9368 | 358.5° | no |
| Oil | Solar | -0.9435 | 57.2° | no |
| Hydro | Solar | -0.9499 | 329.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.582 | 8.279 | 1.327 | 6.468 |
| Coal | Oil | -0.582 | 8.279 | 4.213 | 7.610 |
| Coal | Nuclear | -0.582 | 8.279 | -9.284 | -5.128 |
| Coal | Hydro | -0.582 | 8.279 | -0.861 | 3.330 |
| Coal | Solar | -0.582 | 8.279 | -6.535 | 1.050 |
| Coal | Wind | -0.582 | 8.279 | -5.842 | 1.169 |
| Coal | Biofuel | -0.582 | 8.279 | -7.457 | 1.451 |
| Gas | Oil | 1.327 | 6.468 | 4.213 | 7.610 |
| Gas | Nuclear | 1.327 | 6.468 | -9.284 | -5.128 |
| Gas | Hydro | 1.327 | 6.468 | -0.861 | 3.330 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*