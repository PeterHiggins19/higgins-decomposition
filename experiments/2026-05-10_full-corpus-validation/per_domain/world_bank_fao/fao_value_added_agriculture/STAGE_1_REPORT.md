# Stage 1 Report (pure CoDa) — fao_value_added_agriculture

**Domain:** world_bank_fao
**Description:** FAO indicator FAO_MK_22010 — Value Added (Agriculture), USD millions. Top-10 country compositional pivot. T years × D = 10 countries; each year's row sums to 1.0 (country-share of agricultural value added among the top-10 reporting nations).
**Citation / source:** FAO Macro-Economic Indicators FAO_MK_22010; top-10 country selection by cumulative value added

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:14Z
**cnt_content_sha256:** `2d34a10633925caeb305e5e0d919f18c910d4816ef308e0e4edb6882e41acf93`

## Input

- Source CSV: `fao_value_added_agriculture.csv`
- Source SHA-256: `f65f12fbcebce3db...`
- Records (T): **15**
- Carriers (D): **10**
- Carriers: IRN, UZB, COL, TZA, NGA, UGA, PRY, IND, PAK, CHL
- Closed-data SHA-256: `6be657906a453acc...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2009 | 1.3731 | 18.9580 | — |
| 1 | 2010 | 1.8016 | 17.0366 | 15.3199 |
| 2 | 2011 | 1.2457 | 10.7294 | 16.5689 |
| 3 | 2012 | 0.9760 | 10.5913 | 0.6724 |
| 4 | 2013 | 0.7636 | 4.4788 | 7.9570 |
| ... | ... | ... | ... | ... |
| 12 | 2021 | 1.6578 | 14.5280 | 17.9276 |
| 13 | 2022 | 1.6357 | 14.5063 | 0.2889 |
| 14 | 2023 | 1.1689 | 18.7321 | 16.4611 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| TZA | PAK | +0.9991 | 147.1° | no |
| TZA | UGA | +0.9959 | 186.3° | no |
| COL | PRY | +0.9956 | 175.0° | no |
| UGA | PAK | +0.9949 | 153.6° | no |
| IRN | IND | +0.9917 | 144.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| TZA | IND | -0.7569 | 190.9° | no |
| IND | PAK | -0.7579 | 276.4° | no |
| IRN | UGA | -0.8061 | 175.0° | no |
| IRN | TZA | -0.8187 | 172.0° | no |
| IRN | PAK | -0.8206 | 193.4° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| IRN | UZB | -9.024 | 4.588 | -5.971 | 7.445 |
| IRN | COL | -9.024 | 4.588 | -5.894 | 7.074 |
| IRN | TZA | -9.024 | 4.588 | -0.456 | 5.773 |
| IRN | NGA | -9.024 | 4.588 | -5.971 | 5.898 |
| IRN | UGA | -9.024 | 4.588 | -0.629 | 6.314 |
| IRN | PRY | -9.024 | 4.588 | -5.894 | 5.940 |
| IRN | IND | -9.024 | 4.588 | -9.024 | 0.600 |
| IRN | PAK | -9.024 | 4.588 | -1.566 | 4.924 |
| IRN | CHL | -9.024 | 4.588 | -9.695 | 0.631 |
| UZB | COL | -5.971 | 7.445 | -5.894 | 7.074 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*