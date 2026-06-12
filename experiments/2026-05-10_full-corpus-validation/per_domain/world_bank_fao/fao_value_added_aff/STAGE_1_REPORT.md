# Stage 1 Report (pure CoDa) — fao_value_added_aff

**Domain:** world_bank_fao
**Description:** FAO indicator FAO_MK_22016 — Value Added in Agriculture, Forestry and Fishing. Top-10 country compositional pivot, 1970-2024 (T = 55 years).
**Citation / source:** FAO Macro-Economic Indicators FAO_MK_22016; top-10 country selection

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `6f3d795a3c980326f28e214557b5899023e0455338ef9d0d7633652420e6f543`

## Input

- Source CSV: `fao_value_added_aff.csv`
- Source SHA-256: `9594d637fe9a5e9d...`
- Records (T): **55**
- Carriers (D): **10**
- Carriers: IRN, IDN, VNM, UZB, SOM, COL, KOR, IND, TZA, UGA
- Closed-data SHA-256: `d7ca914a8203a9ac...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1970 | 1.0620 | 12.8969 | — |
| 1 | 1971 | 1.0829 | 12.9519 | 0.2631 |
| 2 | 1972 | 1.0918 | 12.9625 | 0.2678 |
| 3 | 1973 | 1.0459 | 13.0972 | 0.4707 |
| 4 | 1974 | 1.0248 | 13.1443 | 0.2758 |
| ... | ... | ... | ... | ... |
| 52 | 2022 | 0.8436 | 6.0889 | 0.4805 |
| 53 | 2023 | 0.7276 | 6.2946 | 0.2869 |
| 54 | 2024 | 0.6274 | 6.4705 | 0.2521 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| COL | KOR | +0.9905 | 238.3° | no |
| IDN | IND | +0.9774 | 67.8° | no |
| KOR | IND | +0.9611 | 176.2° | no |
| VNM | UGA | +0.9495 | 123.6° | no |
| COL | IND | +0.9417 | 184.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SOM | IND | -0.8981 | 270.0° | no |
| IDN | SOM | -0.9151 | 27.5° | no |
| UZB | KOR | -0.9187 | 351.6° | no |
| IDN | VNM | -0.9229 | 69.3° | no |
| UZB | COL | -0.9294 | 358.2° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| IRN | IDN | 1.118 | 4.539 | 2.287 | 5.550 |
| IRN | VNM | 1.118 | 4.539 | -2.638 | 2.982 |
| IRN | UZB | 1.118 | 4.539 | -9.595 | -0.031 |
| IRN | SOM | 1.118 | 4.539 | -2.097 | 0.304 |
| IRN | COL | 1.118 | 4.539 | -0.830 | 1.917 |
| IRN | KOR | 1.118 | 4.539 | -2.086 | 5.130 |
| IRN | IND | 1.118 | 4.539 | -1.688 | 3.276 |
| IRN | TZA | 1.118 | 4.539 | -1.763 | -0.921 |
| IRN | UGA | 1.118 | 4.539 | -5.177 | -0.056 |
| IDN | VNM | 2.287 | 5.550 | -2.638 | 2.982 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*