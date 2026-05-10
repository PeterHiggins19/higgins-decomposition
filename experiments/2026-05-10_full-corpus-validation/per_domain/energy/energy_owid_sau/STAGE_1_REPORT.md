# Stage 1 Report (pure CoDa) — energy_owid_sau

**Domain:** energy
**Description:** OWID primary-energy consumption composition for SAU (SAU), annual TWh. T = 17 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: SAU

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `f77f5d9d633c250f26b79a569aa115e3125427e8d6ede02cfac8c7748422eb6d`

## Input

- Source CSV: `owid_energy_SAU.csv`
- Source SHA-256: `2fd9b9ded6e196d2...`
- Records (T): **17**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `630037c4a0fb5ddc...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2008 | 0.6559 | 15.7656 | — |
| 1 | 2009 | 0.6409 | 15.6582 | 0.9711 |
| 2 | 2010 | 0.6438 | 15.4266 | 1.5256 |
| 3 | 2011 | 0.6456 | 15.3833 | 0.2322 |
| 4 | 2012 | 0.6492 | 15.2157 | 1.3868 |
| ... | ... | ... | ... | ... |
| 14 | 2022 | 0.6747 | 14.4450 | 4.5639 |
| 15 | 2023 | 0.6857 | 14.5870 | 0.9695 |
| 16 | 2024 | 0.7059 | 14.7311 | 0.8768 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Hydro | +1.0000 | 0.0° | YES |
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Hydro | Biofuel | +1.0000 | 0.0° | YES |
| Oil | Nuclear | +0.9994 | 17.4° | no |
| Oil | Hydro | +0.9994 | 17.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Solar | -0.9084 | 46.1° | no |
| Nuclear | Solar | -0.9164 | 350.1° | no |
| Hydro | Solar | -0.9164 | 350.1° | no |
| Solar | Biofuel | -0.9164 | 69.1° | no |
| Oil | Solar | -0.9188 | 43.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.233 | 1.857 | 6.793 | 8.862 |
| Coal | Oil | 0.233 | 1.857 | 7.316 | 9.534 |
| Coal | Nuclear | 0.233 | 1.857 | -6.027 | -3.869 |
| Coal | Hydro | 0.233 | 1.857 | -6.027 | -3.869 |
| Coal | Solar | 0.233 | 1.857 | -4.003 | 2.690 |
| Coal | Wind | 0.233 | 1.857 | -4.513 | 1.196 |
| Coal | Biofuel | 0.233 | 1.857 | -6.027 | -3.869 |
| Gas | Oil | 6.793 | 8.862 | 7.316 | 9.534 |
| Gas | Nuclear | 6.793 | 8.862 | -6.027 | -3.869 |
| Gas | Hydro | 6.793 | 8.862 | -6.027 | -3.869 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*