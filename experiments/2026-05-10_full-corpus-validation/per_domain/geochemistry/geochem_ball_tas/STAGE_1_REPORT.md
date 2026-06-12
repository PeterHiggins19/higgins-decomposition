# Stage 1 Report (pure CoDa) — geochem_ball_tas

**Domain:** geochemistry
**Description:** Ball (2022) intraplate-volcanic database — major-oxide composition binned by Total-Alkali-Silica (TAS, Le Bas 1986) rock-type classification. T = 15 rock types, D = 10 oxides.
**Citation / source:** Ball M.E. et al. (2022) — Geochem Earthchem 2022-3-RY3BRK; TAS classification per Le Bas 1986

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `e6d2f7d47d3c61d1c8ef52140039847444684b5726a8c88f37169a43927dee64`

## Input

- Source CSV: `ball_oxides_by_tas_barycenters.csv`
- Source SHA-256: `3c5c8bbb84b41787...`
- Records (T): **15**
- Carriers (D): **10**
- Carriers: SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5
- Closed-data SHA-256: `4b86e1f2c2bf4059...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | Foidite | 1.7505 | 4.5564 | — |
| 1 | Picrobasalt | 1.6025 | 5.5670 | 1.4664 |
| 2 | Basanite | 1.6738 | 4.5899 | 1.5248 |
| 3 | Basalt | 1.5581 | 5.5447 | 1.3177 |
| 4 | Trachybasalt | 1.5998 | 4.8317 | 1.3684 |
| ... | ... | ... | ... | ... |
| 12 | Trachyte | 1.1695 | 6.2633 | 0.8885 |
| 13 | Dacite | 1.0998 | 5.8574 | 2.0404 |
| 14 | Rhyolite | 0.9195 | 7.5551 | 3.1269 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | Al2O3 | +0.9682 | 11.9° | no |
| CaO | MgO | +0.9409 | 176.8° | no |
| Al2O3 | Na2O | +0.9351 | 63.5° | no |
| TiO2 | MgO | +0.9327 | 346.2° | no |
| K2O | Na2O | +0.8896 | 348.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| TiO2 | Al2O3 | -0.9215 | 19.8° | no |
| MgO | K2O | -0.9278 | 210.6° | no |
| CaO | K2O | -0.9281 | 189.1° | no |
| TiO2 | Na2O | -0.9354 | 354.2° | no |
| MgO | Na2O | -0.9836 | 171.2° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| SiO2 | TiO2 | 2.193 | 4.294 | -1.633 | -0.246 |
| SiO2 | Al2O3 | 2.193 | 4.294 | 0.931 | 2.614 |
| SiO2 | FeO | 2.193 | 4.294 | 0.571 | 1.406 |
| SiO2 | CaO | 2.193 | 4.294 | -1.352 | 1.162 |
| SiO2 | MgO | 2.193 | 4.294 | -2.079 | 1.524 |
| SiO2 | MnO | 2.193 | 4.294 | -3.299 | -2.234 |
| SiO2 | K2O | 2.193 | 4.294 | -1.840 | 1.534 |
| SiO2 | Na2O | 2.193 | 4.294 | -0.727 | 1.550 |
| SiO2 | P2O5 | 2.193 | 4.294 | -3.205 | -1.453 |
| TiO2 | Al2O3 | -1.633 | -0.246 | 0.931 | 2.614 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*