# Stage 1 Report (pure CoDa) — energy_owid_usa

**Domain:** energy
**Description:** OWID primary-energy consumption composition for USA (USA), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: USA

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `f3f09906ca82085074bae7b1a9526f9e60bf218f25de7c10751511eed2cb960d`

## Input

- Source CSV: `owid_energy_USA.csv`
- Source SHA-256: `7b5246202c4f7a0d...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `b9ccede0f479e430...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.1850 | 15.9760 | — |
| 1 | 1966 | 1.1838 | 15.9646 | 0.3439 |
| 2 | 1967 | 1.1889 | 15.9796 | 0.2862 |
| 3 | 1968 | 1.1855 | 15.9794 | 0.4184 |
| 4 | 1969 | 1.1877 | 15.9890 | 0.0940 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.5331 | 3.2569 | 0.2380 |
| 58 | 2023 | 1.5233 | 3.1602 | 0.2767 |
| 59 | 2024 | 1.5393 | 3.0613 | 0.2286 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9970 | 64.4° | no |
| Gas | Oil | +0.9960 | 5.6° | YES |
| Gas | Hydro | +0.9934 | 68.9° | no |
| Coal | Oil | +0.9885 | 35.0° | no |
| Coal | Hydro | +0.9885 | 114.6° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Biofuel | -0.9644 | 37.9° | no |
| Coal | Wind | -0.9763 | 32.8° | no |
| Gas | Wind | -0.9779 | 41.8° | no |
| Oil | Wind | -0.9856 | 39.1° | no |
| Hydro | Wind | -0.9866 | 100.1° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.210 | 5.437 | 1.608 | 5.692 |
| Coal | Oil | 0.210 | 5.437 | 1.721 | 6.125 |
| Coal | Nuclear | 0.210 | 5.437 | -0.272 | 3.754 |
| Coal | Hydro | 0.210 | 5.437 | -1.117 | 3.673 |
| Coal | Solar | 0.210 | 5.437 | -7.405 | -0.868 |
| Coal | Wind | 0.210 | 5.437 | -7.495 | -0.458 |
| Coal | Biofuel | 0.210 | 5.437 | -8.539 | -1.072 |
| Gas | Oil | 1.608 | 5.692 | 1.721 | 6.125 |
| Gas | Nuclear | 1.608 | 5.692 | -0.272 | 3.754 |
| Gas | Hydro | 1.608 | 5.692 | -1.117 | 3.673 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*