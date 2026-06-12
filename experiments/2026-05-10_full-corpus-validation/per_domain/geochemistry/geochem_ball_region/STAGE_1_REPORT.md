# Stage 1 Report (pure CoDa) — geochem_ball_region

**Domain:** geochemistry
**Description:** Ball (2022) intraplate-volcanic database — major-oxide composition binned by geographic Region (95 regions retained at min n=10 per region). T = 95, D = 10 oxides.
**Citation / source:** Ball M.E. et al. (2022) — Geochem Earthchem 2022-3-RY3BRK; region binning per source metadata

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `2d655b532e5e45ee96cbcbef075ddd853ae46722fc8b8b82413da4546f414af7`

## Input

- Source CSV: `ball_oxides_by_region_barycenters.csv`
- Source SHA-256: `1b184354432ad7fe...`
- Records (T): **95**
- Carriers (D): **10**
- Carriers: SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5
- Closed-data SHA-256: `a507c830b2a95cde...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | Afar | 1.5520 | 5.4383 | — |
| 1 | Air | 1.6873 | 4.6338 | 1.4516 |
| 2 | Amsterdam | 1.5240 | 5.3975 | 1.4638 |
| 3 | Antarctica | 1.6377 | 4.7369 | 1.1188 |
| 4 | As_Sirat | 1.5953 | 5.2664 | 0.8588 |
| ... | ... | ... | ... | ... |
| 92 | Western_USA | 1.6219 | 5.1280 | 0.9423 |
| 93 | Wudalianchi | 1.6114 | 4.8376 | 1.5597 |
| 94 | Yemen | 1.5778 | 5.1047 | 1.6700 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | Al2O3 | +0.8956 | 9.5° | YES |
| Al2O3 | Na2O | +0.6094 | 47.1° | no |
| K2O | P2O5 | +0.5636 | 54.9° | no |
| SiO2 | Na2O | +0.4852 | 27.4° | no |
| TiO2 | MgO | +0.4396 | 349.6° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| MgO | Na2O | -0.6155 | 221.1° | no |
| FeO | P2O5 | -0.6557 | 18.9° | no |
| SiO2 | P2O5 | -0.7138 | 17.8° | no |
| FeO | K2O | -0.7846 | 88.6° | no |
| CaO | MnO | -0.8679 | 250.9° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| SiO2 | TiO2 | 2.249 | 3.058 | -1.012 | 0.114 |
| SiO2 | Al2O3 | 2.249 | 3.058 | 0.913 | 1.877 |
| SiO2 | FeO | 2.249 | 3.058 | 0.636 | 1.533 |
| SiO2 | CaO | 2.249 | 3.058 | -3.202 | 1.676 |
| SiO2 | MgO | 2.249 | 3.058 | -0.360 | 1.446 |
| SiO2 | MnO | 2.249 | 3.058 | -3.463 | 0.781 |
| SiO2 | K2O | 2.249 | 3.058 | -3.015 | 0.304 |
| SiO2 | Na2O | 2.249 | 3.058 | -0.740 | 0.579 |
| SiO2 | P2O5 | 2.249 | 3.058 | -3.149 | -1.264 |
| TiO2 | Al2O3 | -1.012 | 0.114 | 0.913 | 1.877 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*