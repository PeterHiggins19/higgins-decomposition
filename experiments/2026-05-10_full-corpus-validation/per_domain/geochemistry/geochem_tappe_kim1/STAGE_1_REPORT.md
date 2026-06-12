# Stage 1 Report (pure CoDa) — geochem_tappe_kim1

**Domain:** geochemistry
**Description:** Tappe et al. (2024) Kimberlite Group-1 bulk rock major-oxide composition, binned by country/region. T = 8 countries, D = 10 oxides. Kimberlites are intra-cratonic mantle-derived ultrapotassic rocks; K2O is typically very high (>3% on mass basis).
**Citation / source:** Tappe S. et al. (2024) — Geochem Earthchem 2022-2-FLV19S_Tappe_data_v2024

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `e0f8ea0b1ca06df3b92c3649d3a4d7f7f070461b38f83f4ac3661b151bdc0ca2`

## Input

- Source CSV: `tappe_kim1_by_country_barycenters.csv`
- Source SHA-256: `e4578e4c0e4b139e...`
- Records (T): **8**
- Carriers (D): **10**
- Carriers: SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5
- Closed-data SHA-256: `aca24df777276fb1...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | Central_Slave_Province_Lac_de_ | 1.3266 | 6.7909 | — |
| 1 | Maniitsoq_&_Sarfartoq | 1.4927 | 5.9868 | 2.1247 |
| 2 | N_Slave_Province | 1.3556 | 6.2062 | 1.1153 |
| 3 | Sarfartoq_Complex | 1.5433 | 6.2716 | 1.7723 |
| 4 | Somerset_Island | 1.3989 | 6.4650 | 1.9166 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | MgO | +0.9373 | 2.0° | YES |
| SiO2 | Al2O3 | +0.8387 | 13.4° | no |
| Al2O3 | MgO | +0.6466 | 13.2° | no |
| Al2O3 | P2O5 | +0.6230 | 30.4° | no |
| SiO2 | P2O5 | +0.5411 | 13.6° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| K2O | Na2O | -0.7830 | 41.8° | no |
| TiO2 | MgO | -0.7904 | 32.6° | no |
| SiO2 | TiO2 | -0.8172 | 33.1° | no |
| TiO2 | Al2O3 | -0.8270 | 224.5° | no |
| CaO | K2O | -0.8868 | 39.1° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| SiO2 | TiO2 | 2.549 | 3.041 | -0.959 | 0.743 |
| SiO2 | Al2O3 | 2.549 | 3.041 | -0.388 | 0.273 |
| SiO2 | FeO | 2.549 | 3.041 | 0.688 | 1.725 |
| SiO2 | CaO | 2.549 | 3.041 | 1.327 | 2.141 |
| SiO2 | MgO | 2.549 | 3.041 | 2.578 | 3.095 |
| SiO2 | MnO | 2.549 | 3.041 | -2.481 | -2.203 |
| SiO2 | K2O | 2.549 | 3.041 | -2.883 | -0.338 |
| SiO2 | Na2O | 2.549 | 3.041 | -3.935 | -2.600 |
| SiO2 | P2O5 | 2.549 | 3.041 | -1.556 | -0.868 |
| TiO2 | Al2O3 | -0.959 | 0.743 | -0.388 | 0.273 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*