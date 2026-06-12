# Stage 1 Report (pure CoDa) — energy_owid_zaf

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ZAF (ZAF), annual TWh. T = 54 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ZAF

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `8e2e9a0bebd161f93dea754540ce5b0265f530add40ea3244925dd7f9df9962b`

## Input

- Source CSV: `owid_energy_ZAF.csv`
- Source SHA-256: `8348b9eb35e98280...`
- Records (T): **54**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `f739aee4a1e3c3d0...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1971 | 0.5763 | 15.3310 | — |
| 1 | 1972 | 0.6189 | 15.7031 | 1.8268 |
| 2 | 1973 | 0.6281 | 15.7315 | 0.0892 |
| 3 | 1974 | 0.6182 | 15.7583 | 0.1652 |
| 4 | 1975 | 0.6181 | 15.7755 | 0.2177 |
| ... | ... | ... | ... | ... |
| 51 | 2022 | 0.9217 | 5.4770 | 0.5024 |
| 52 | 2023 | 0.9135 | 5.7192 | 0.5323 |
| 53 | 2024 | 0.8833 | 5.9072 | 0.5555 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9975 | 8.8° | YES |
| Oil | Hydro | +0.9449 | 74.7° | no |
| Coal | Hydro | +0.9444 | 60.3° | no |
| Solar | Wind | +0.9321 | 356.1° | no |
| Gas | Oil | +0.7847 | 22.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Wind | -0.7488 | 55.0° | no |
| Gas | Solar | -0.7528 | 39.1° | no |
| Hydro | Solar | -0.7647 | 112.4° | no |
| Oil | Solar | -0.7941 | 38.8° | no |
| Coal | Solar | -0.8133 | 37.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 3.399 | 8.565 | 0.308 | 3.169 |
| Coal | Oil | 3.399 | 8.565 | 2.217 | 7.463 |
| Coal | Nuclear | 3.399 | 8.565 | -5.367 | 3.761 |
| Coal | Hydro | 3.399 | 8.565 | -2.645 | 3.763 |
| Coal | Solar | 3.399 | 8.565 | -6.790 | -0.518 |
| Coal | Wind | 3.399 | 8.565 | -7.930 | 0.002 |
| Coal | Biofuel | 3.399 | 8.565 | -7.597 | -1.881 |
| Gas | Oil | 0.308 | 3.169 | 2.217 | 7.463 |
| Gas | Nuclear | 0.308 | 3.169 | -5.367 | 3.761 |
| Gas | Hydro | 0.308 | 3.169 | -2.645 | 3.763 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*