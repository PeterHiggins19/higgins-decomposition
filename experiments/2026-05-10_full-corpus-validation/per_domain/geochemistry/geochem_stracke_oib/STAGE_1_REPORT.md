# Stage 1 Report (pure CoDa) — geochem_stracke_oib

**Domain:** geochemistry
**Description:** Stracke (2022) ocean island basalt (OIB) major-oxide composition, binned by location (top 15 locations by sample count, including Galapagos, Iceland, Hawaii, Tristan da Cunha, etc.). T = 15, D = 10 oxides.
**Citation / source:** Stracke A. (2022) — Geochem Earthchem 2022_09-0SVW6S_Stracke_data (OIB subset)

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `2cb0b919f9c33ea789717988573235c52c75e0597df653ce3512c46b83bbd2db`

## Input

- Source CSV: `stracke_oib_by_location_barycenters.csv`
- Source SHA-256: `3bbe3a32aeda2106...`
- Records (T): **15**
- Carriers (D): **10**
- Carriers: SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5
- Closed-data SHA-256: `e1d7cfa28abe39a3...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | Azores | 1.5718 | 5.1672 | — |
| 1 | Azores-SaoMiguel | 1.3357 | 5.1141 | 2.0277 |
| 2 | Canary_Islands | 1.6222 | 4.7161 | 1.9793 |
| 3 | Cape_Verde_Islands | 1.6468 | 4.5884 | 0.2621 |
| 4 | Caroline_Islands | 1.6460 | 4.9105 | 0.8526 |
| ... | ... | ... | ... | ... |
| 12 | Mauritius | 1.5950 | 5.4799 | 1.1360 |
| 13 | St._Helena | 1.6094 | 5.0801 | 0.6849 |
| 14 | Tristan_da_Cunha | 1.6823 | 4.7967 | 0.8201 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | Al2O3 | +0.9708 | 5.6° | YES |
| TiO2 | P2O5 | +0.8975 | 14.5° | no |
| CaO | MgO | +0.8316 | 94.6° | no |
| FeO | MgO | +0.7020 | 102.5° | no |
| SiO2 | MnO | +0.6911 | 17.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| CaO | K2O | -0.8843 | 82.7° | no |
| SiO2 | P2O5 | -0.9237 | 12.8° | no |
| SiO2 | TiO2 | -0.9318 | 13.3° | no |
| Al2O3 | P2O5 | -0.9440 | 7.3° | YES |
| TiO2 | Al2O3 | -0.9521 | 20.2° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| SiO2 | TiO2 | 2.363 | 3.104 | -0.800 | -0.053 |
| SiO2 | Al2O3 | 2.363 | 3.104 | 1.213 | 1.928 |
| SiO2 | FeO | 2.363 | 3.104 | 0.404 | 1.200 |
| SiO2 | CaO | 2.363 | 3.104 | 0.349 | 1.749 |
| SiO2 | MgO | 2.363 | 3.104 | -0.512 | 1.436 |
| SiO2 | MnO | 2.363 | 3.104 | -3.333 | -2.042 |
| SiO2 | K2O | 2.363 | 3.104 | -2.945 | 0.093 |
| SiO2 | Na2O | 2.363 | 3.104 | -0.665 | 0.608 |
| SiO2 | P2O5 | 2.363 | 3.104 | -3.232 | -1.584 |
| TiO2 | Al2O3 | -0.800 | -0.053 | 1.213 | 1.928 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*