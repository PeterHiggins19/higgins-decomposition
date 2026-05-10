# Stage 1 Report (pure CoDa) — energy_owid_hrv

**Domain:** energy
**Description:** OWID primary-energy consumption composition for HRV (HRV), annual TWh. T = 35 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: HRV

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `e54816db3185928f2f5b9f3d7a95397c8dc521154d3535e48f82da84ad8d7ed9`

## Input

- Source CSV: `owid_energy_HRV.csv`
- Source SHA-256: `1711e0d27cbd371d...`
- Records (T): **35**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `eaae41c473d02923...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1990 | 1.1438 | 17.2769 | — |
| 1 | 1991 | 1.2022 | 17.3142 | 0.6845 |
| 2 | 1992 | 1.1658 | 17.2606 | 0.2278 |
| 3 | 1993 | 1.1442 | 17.2219 | 0.1936 |
| 4 | 1994 | 1.1181 | 17.1339 | 0.4971 |
| ... | ... | ... | ... | ... |
| 32 | 2022 | 1.3675 | 11.2127 | 1.3534 |
| 33 | 2023 | 1.3803 | 12.1584 | 3.6306 |
| 34 | 2024 | 1.3523 | 12.0192 | 0.8597 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9992 | 31.8° | no |
| Gas | Nuclear | +0.9984 | 30.4° | no |
| Gas | Oil | +0.9967 | 4.2° | YES |
| Nuclear | Hydro | +0.9920 | 32.5° | no |
| Oil | Hydro | +0.9882 | 7.2° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Wind | -0.8650 | 119.2° | no |
| Hydro | Wind | -0.9294 | 82.0° | no |
| Oil | Wind | -0.9336 | 68.0° | no |
| Nuclear | Wind | -0.9357 | 352.4° | no |
| Gas | Wind | -0.9372 | 74.8° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.039 | 5.364 | 2.995 | 6.593 |
| Coal | Oil | 1.039 | 5.364 | 3.238 | 7.211 |
| Coal | Nuclear | 1.039 | 5.364 | -9.629 | -5.967 |
| Coal | Hydro | 1.039 | 5.364 | 2.467 | 6.399 |
| Coal | Solar | 1.039 | 5.364 | -7.703 | 0.756 |
| Coal | Wind | 1.039 | 5.364 | -6.100 | 1.955 |
| Coal | Biofuel | 1.039 | 5.364 | -7.276 | -0.284 |
| Gas | Oil | 2.995 | 6.593 | 3.238 | 7.211 |
| Gas | Nuclear | 2.995 | 6.593 | -9.629 | -5.967 |
| Gas | Hydro | 2.995 | 6.593 | 2.467 | 6.399 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*