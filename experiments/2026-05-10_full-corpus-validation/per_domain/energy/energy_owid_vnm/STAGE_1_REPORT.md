# Stage 1 Report (pure CoDa) — energy_owid_vnm

**Domain:** energy
**Description:** OWID primary-energy consumption composition for VNM (VNM), annual TWh. T = 44 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: VNM

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `b0e3d21d799821d9bc3fdd9503626dd50af6b67ff06edef287321f5c0b81ea59`

## Input

- Source CSV: `owid_energy_VNM.csv`
- Source SHA-256: `aa339683c71d8f7a...`
- Records (T): **44**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `1fd3b8ef0b4f7012...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1981 | 0.9081 | 16.4705 | — |
| 1 | 1982 | 0.9033 | 16.5216 | 0.5462 |
| 2 | 1983 | 0.9086 | 16.6757 | 1.1882 |
| 3 | 1984 | 0.9344 | 16.7001 | 0.2984 |
| 4 | 1985 | 0.9127 | 16.6063 | 0.4490 |
| ... | ... | ... | ... | ... |
| 41 | 2022 | 1.4196 | 14.3715 | 0.9043 |
| 42 | 2023 | 1.3674 | 14.3301 | 0.3481 |
| 43 | 2024 | 1.3408 | 14.2992 | 0.2359 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Oil | Nuclear | +0.9962 | 28.3° | no |
| Oil | Biofuel | +0.9962 | 28.3° | no |
| Coal | Nuclear | +0.9498 | 27.2° | no |
| Coal | Biofuel | +0.9498 | 27.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Solar | -0.9056 | 85.8° | no |
| Oil | Solar | -0.9122 | 79.0° | no |
| Nuclear | Wind | -0.9590 | 354.3° | no |
| Wind | Biofuel | -0.9590 | 54.1° | no |
| Oil | Wind | -0.9704 | 61.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 4.304 | 7.610 | 1.889 | 6.041 |
| Coal | Oil | 4.304 | 7.610 | 3.840 | 7.295 |
| Coal | Nuclear | 4.304 | 7.610 | -8.647 | -5.599 |
| Coal | Hydro | 4.304 | 7.610 | 3.260 | 6.453 |
| Coal | Solar | 4.304 | 7.610 | -6.708 | 2.365 |
| Coal | Wind | 4.304 | 7.610 | -6.173 | 1.373 |
| Coal | Biofuel | 4.304 | 7.610 | -8.647 | -5.599 |
| Gas | Oil | 1.889 | 6.041 | 3.840 | 7.295 |
| Gas | Nuclear | 1.889 | 6.041 | -8.647 | -5.599 |
| Gas | Hydro | 1.889 | 6.041 | 3.260 | 6.453 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*