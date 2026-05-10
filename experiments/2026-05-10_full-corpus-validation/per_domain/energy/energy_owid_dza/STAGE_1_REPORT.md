# Stage 1 Report (pure CoDa) — energy_owid_dza

**Domain:** energy
**Description:** OWID primary-energy consumption composition for DZA (DZA), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: DZA

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `163c5b72935f3b80328b9712b6a84d9613d3da92030a55ad42f548754dbc4019`

## Input

- Source CSV: `owid_energy_DZA.csv`
- Source SHA-256: `2acab0aa582a3f7f...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `a38204950c988e38...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.9081 | 16.8110 | — |
| 1 | 1966 | 0.8209 | 16.6539 | 0.3536 |
| 2 | 1967 | 0.8313 | 16.6788 | 0.2936 |
| 3 | 1968 | 0.8554 | 16.7382 | 0.2379 |
| 4 | 1969 | 0.8460 | 16.6746 | 0.5812 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 0.6533 | 13.6395 | 0.7315 |
| 58 | 2023 | 0.6474 | 13.5572 | 0.5244 |
| 59 | 2024 | 0.6665 | 13.4892 | 0.5983 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Solar | Wind | +0.8521 | 78.3° | no |
| Oil | Hydro | +0.8500 | 56.0° | no |
| Oil | Nuclear | +0.8082 | 12.0° | no |
| Oil | Biofuel | +0.8082 | 12.0° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Solar | -0.8261 | 231.7° | no |
| Oil | Wind | -0.8354 | 24.4° | no |
| Nuclear | Solar | -0.8542 | 349.6° | no |
| Solar | Biofuel | -0.8542 | 59.4° | no |
| Oil | Solar | -0.8768 | 52.8° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.586 | 5.042 | 6.637 | 8.106 |
| Coal | Oil | 0.586 | 5.042 | 6.163 | 7.837 |
| Coal | Nuclear | 0.586 | 5.042 | -6.574 | -5.271 |
| Coal | Hydro | 0.586 | 5.042 | -2.684 | 5.021 |
| Coal | Solar | 0.586 | 5.042 | -5.878 | 1.584 |
| Coal | Wind | 0.586 | 5.042 | -5.937 | -1.891 |
| Coal | Biofuel | 0.586 | 5.042 | -6.574 | -5.271 |
| Gas | Oil | 6.637 | 8.106 | 6.163 | 7.837 |
| Gas | Nuclear | 6.637 | 8.106 | -6.574 | -5.271 |
| Gas | Hydro | 6.637 | 8.106 | -2.684 | 5.021 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*