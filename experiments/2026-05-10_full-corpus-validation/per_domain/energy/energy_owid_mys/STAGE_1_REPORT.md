# Stage 1 Report (pure CoDa) — energy_owid_mys

**Domain:** energy
**Description:** OWID primary-energy consumption composition for MYS (MYS), annual TWh. T = 55 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: MYS

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `7cc05b05abb8019351b5388a1304c71838148f5cde3bf83fd4dfd87d4ee67294`

## Input

- Source CSV: `owid_energy_MYS.csv`
- Source SHA-256: `c58626f0c81a052b...`
- Records (T): **55**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `b90e6847116114f1...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1970 | 0.3088 | 15.2523 | — |
| 1 | 1971 | 0.3624 | 15.8237 | 2.1615 |
| 2 | 1972 | 0.4279 | 16.0730 | 0.7689 |
| 3 | 1973 | 0.4013 | 16.0037 | 0.1223 |
| 4 | 1974 | 0.4562 | 16.1607 | 0.6988 |
| ... | ... | ... | ... | ... |
| 52 | 2022 | 1.3007 | 14.2056 | 0.3360 |
| 53 | 2023 | 1.3178 | 14.2218 | 0.2639 |
| 54 | 2024 | 1.3239 | 14.2288 | 0.0579 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Wind | +1.0000 | 0.0° | YES |
| Oil | Nuclear | +0.9890 | 31.7° | no |
| Oil | Wind | +0.9890 | 31.7° | no |
| Oil | Hydro | +0.9273 | 10.2° | no |
| Hydro | Wind | +0.9057 | 32.7° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Solar | Wind | -0.8930 | 47.5° | no |
| Nuclear | Solar | -0.8930 | 358.1° | no |
| Oil | Biofuel | -0.9113 | 54.2° | no |
| Nuclear | Biofuel | -0.9386 | 357.6° | no |
| Wind | Biofuel | -0.9386 | 357.6° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.123 | 6.122 | 2.418 | 7.163 |
| Coal | Oil | 2.123 | 6.122 | 4.338 | 8.626 |
| Coal | Nuclear | 2.123 | 6.122 | -8.376 | -5.105 |
| Coal | Hydro | 2.123 | 6.122 | 2.495 | 6.132 |
| Coal | Solar | 2.123 | 6.122 | -6.739 | 0.365 |
| Coal | Wind | 2.123 | 6.122 | -8.376 | -5.105 |
| Coal | Biofuel | 2.123 | 6.122 | -6.004 | 1.043 |
| Gas | Oil | 2.418 | 7.163 | 4.338 | 8.626 |
| Gas | Nuclear | 2.418 | 7.163 | -8.376 | -5.105 |
| Gas | Hydro | 2.418 | 7.163 | 2.495 | 6.132 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*