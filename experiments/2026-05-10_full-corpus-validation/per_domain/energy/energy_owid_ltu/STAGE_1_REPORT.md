# Stage 1 Report (pure CoDa) — energy_owid_ltu

**Domain:** energy
**Description:** OWID primary-energy consumption composition for LTU (LTU), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: LTU

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `9b08a0af95d75960092d299d4de04e8635bf04298258fcfad79867aee4c0a9f4`

## Input

- Source CSV: `owid_energy_LTU.csv`
- Source SHA-256: `09315303bfddcaa4...`
- Records (T): **40**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `bbbf5bc7a9ee7365...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 1.1243 | 16.0064 | — |
| 1 | 1986 | 1.1964 | 16.0946 | 0.2627 |
| 2 | 1987 | 1.1616 | 16.0492 | 0.1556 |
| 3 | 1988 | 1.2096 | 16.0966 | 0.2961 |
| 4 | 1989 | 1.2185 | 16.0802 | 0.2519 |
| ... | ... | ... | ... | ... |
| 37 | 2022 | 1.1575 | 10.8164 | 0.6952 |
| 38 | 2023 | 1.2040 | 10.8300 | 0.9296 |
| 39 | 2024 | 1.2994 | 10.9055 | 0.7303 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Wind | Biofuel | +0.9819 | 201.7° | no |
| Gas | Oil | +0.9561 | 8.1° | YES |
| Coal | Oil | +0.9482 | 33.3° | no |
| Gas | Hydro | +0.9295 | 25.7° | no |
| Coal | Gas | +0.9176 | 36.8° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Wind | -0.8791 | 92.9° | no |
| Gas | Biofuel | -0.8872 | 66.5° | no |
| Oil | Wind | -0.8969 | 82.7° | no |
| Oil | Biofuel | -0.9338 | 62.8° | no |
| Nuclear | Wind | -0.9399 | 230.8° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.000 | 3.920 | 2.718 | 5.514 |
| Coal | Oil | -0.000 | 3.920 | 3.427 | 6.119 |
| Coal | Nuclear | -0.000 | 3.920 | -9.683 | 5.818 |
| Coal | Hydro | -0.000 | 3.920 | -0.058 | 2.323 |
| Coal | Solar | -0.000 | 3.920 | -9.336 | 1.100 |
| Coal | Wind | -0.000 | 3.920 | -7.243 | 2.030 |
| Coal | Biofuel | -0.000 | 3.920 | -7.243 | 0.896 |
| Gas | Oil | 2.718 | 5.514 | 3.427 | 6.119 |
| Gas | Nuclear | 2.718 | 5.514 | -9.683 | 5.818 |
| Gas | Hydro | 2.718 | 5.514 | -0.058 | 2.323 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*