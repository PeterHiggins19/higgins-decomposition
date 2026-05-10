# Stage 1 Report (pure CoDa) — fao_credit_to_agriculture

**Domain:** world_bank_fao
**Description:** FAO indicator FAO_IC_23068 — Credit to Agriculture, Forestry and Fishing (USD millions). Pivoted compositional view: top-10 countries by total reporting volume, normalised so each year's row is the country-share of total recorded credit. Reveals year-by-year concentration shifts in agricultural lending.
**Citation / source:** FAO Aquastat / Credit to Agriculture indicator FAO_IC_23068; top-10 country selection by cumulative reporting volume

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `8afc845fe84ec4f3ff2b20e769143ff9779f5c478d20aa8c4bb1668cf7c89f9c`

## Input

- Source CSV: `fao_credit_to_agriculture.csv`
- Source SHA-256: `e3059d846efed2d5...`
- Records (T): **28**
- Carriers (D): **10**
- Carriers: IND, USA, DEU, CHN, AUS, ITA, NZL, FRA, KOR, GBR
- Closed-data SHA-256: `1eb62c7ac51789d0...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1996 | 1.3293 | 18.8899 | — |
| 1 | 1997 | 1.4925 | 18.2419 | 10.6468 |
| 2 | 1998 | 1.4954 | 18.2459 | 0.0442 |
| 3 | 1999 | 1.6221 | 18.4173 | 0.7537 |
| 4 | 2000 | 1.6233 | 18.4182 | 0.0609 |
| ... | ... | ... | ... | ... |
| 25 | 2021 | 2.0549 | 10.9926 | 0.0822 |
| 26 | 2022 | 2.0505 | 10.9942 | 0.2303 |
| 27 | 2023 | 2.0064 | 10.9851 | 0.2395 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| AUS | NZL | +0.9975 | 171.4° | no |
| USA | DEU | +0.9958 | 79.4° | no |
| USA | AUS | +0.9947 | 93.7° | no |
| IND | NZL | +0.9935 | 78.3° | no |
| DEU | AUS | +0.9879 | 171.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| IND | KOR | -0.7336 | 110.7° | no |
| NZL | KOR | -0.7605 | 181.2° | no |
| DEU | KOR | -0.7823 | 148.8° | no |
| AUS | KOR | -0.7863 | 158.0° | no |
| USA | KOR | -0.8038 | 116.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| IND | USA | 0.482 | 5.262 | 0.140 | 6.732 |
| IND | DEU | 0.482 | 5.262 | -0.090 | 7.038 |
| IND | CHN | 0.482 | 5.262 | -10.344 | 2.037 |
| IND | AUS | 0.482 | 5.262 | -0.207 | 5.671 |
| IND | ITA | 0.482 | 5.262 | -7.113 | 3.677 |
| IND | NZL | 0.482 | 5.262 | -0.419 | 5.030 |
| IND | FRA | 0.482 | 5.262 | -10.351 | 1.252 |
| IND | KOR | 0.482 | 5.262 | -8.264 | 2.481 |
| IND | GBR | 0.482 | 5.262 | -5.947 | 4.353 |
| USA | DEU | 0.140 | 6.732 | -0.090 | 7.038 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*