# Stage 1 Report (pure CoDa) — energy_ember_gbr

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for the United Kingdom, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:03Z
**cnt_content_sha256:** `337a6cda5bb3684284ef638c2448336749b91e5ebe0945cb9a75c2ef0d30d607`

## Input

- Source CSV: `ember_GBR_United_Kingdom_generation_TWh.csv`
- Source SHA-256: `b1df2a0ae6f21f77...`
- Records (T): **26**
- Carriers (D): **9**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind
- Closed-data SHA-256: `b80351f461235d90...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2000 | 1.3101 | 46.8517 | — |
| 1 | 2001 | 1.2966 | 46.8352 | 0.3465 |
| 2 | 2002 | 1.3038 | 46.9057 | 0.2975 |
| 3 | 2003 | 1.2941 | 46.8996 | 0.4536 |
| 4 | 2004 | 1.3107 | 47.0073 | 0.5488 |
| ... | ... | ... | ... | ... |
| 23 | 2023 | 1.6465 | 35.5749 | 0.4445 |
| 24 | 2024 | 1.6716 | 35.5466 | 0.7109 |
| 25 | 2025 | 1.6579 | 35.5367 | 1.7159 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Other Fossil | +0.9959 | 39.0° | no |
| Hydro | Other Fossil | +0.9947 | 343.0° | no |
| Gas | Nuclear | +0.9947 | 10.0° | no |
| Nuclear | Other Fossil | +0.9919 | 41.1° | no |
| Hydro | Nuclear | +0.9910 | 56.6° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Solar | -0.8073 | 220.8° | no |
| Hydro | Solar | -0.8537 | 244.3° | no |
| Other Fossil | Solar | -0.8675 | 184.3° | no |
| Gas | Solar | -0.8765 | 106.7° | no |
| Nuclear | Solar | -0.8839 | 112.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 36 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | 1.177 | 7.344 | -0.371 | 10.372 |
| Bioenergy | Gas | 1.177 | 7.344 | 2.498 | 10.474 |
| Bioenergy | Hydro | 1.177 | 7.344 | -0.687 | 7.103 |
| Bioenergy | Nuclear | 1.177 | 7.344 | 1.723 | 9.991 |
| Bioenergy | Other Fossil | 1.177 | 7.344 | -0.055 | 8.119 |
| Bioenergy | Other Renewables | 1.177 | 7.344 | -33.630 | -6.911 |
| Bioenergy | Solar | 1.177 | 7.344 | -29.191 | 4.311 |
| Bioenergy | Wind | 1.177 | 7.344 | 1.660 | 6.011 |
| Coal | Gas | -0.371 | 10.372 | 2.498 | 10.474 |
| Coal | Hydro | -0.371 | 10.372 | -0.687 | 7.103 |
| ... (26 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*