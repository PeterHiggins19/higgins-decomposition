# Stage 1 Report (pure CoDa) — geochem_ball_age

**Domain:** geochemistry
**Description:** Ball (2022) intraplate-volcanic database — major-oxide composition binned by IUGS chronostratigraphic age epoch (Holocene through Eocene_or_older). T = 10 epochs, D = 10 oxides (SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5).
**Citation / source:** Ball M.E. et al. (2022) — Geochem Earthchem 2022-3-RY3BRK; chronostratigraphic binning per IUGS chart

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `23510774d1bdf07f7433a50d8dd5b52c075f871af44a665831766aa5c3f7a5b7`

## Input

- Source CSV: `ball_oxides_by_age_barycenters.csv`
- Source SHA-256: `1e68a5a75d6c2d0b...`
- Records (T): **10**
- Carriers (D): **10**
- Carriers: SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5
- Closed-data SHA-256: `b1a94c3b8d290187...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | Holocene | 1.5547 | 5.5019 | — |
| 1 | Late_Pleistocene | 1.5730 | 5.3755 | 0.1556 |
| 2 | Middle_Pleistocene | 1.5467 | 5.4701 | 0.2266 |
| 3 | Early_Pleistocene | 1.5919 | 5.0247 | 0.7958 |
| 4 | Pliocene | 1.5942 | 5.1430 | 0.2557 |
| ... | ... | ... | ... | ... |
| 7 | Early_Miocene | 1.5280 | 4.9352 | 0.1532 |
| 8 | Oligocene | 1.5447 | 5.0772 | 0.5421 |
| 9 | Eocene_or_older | 1.6046 | 4.9164 | 0.3480 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| K2O | Na2O | +0.8934 | 7.3° | YES |
| K2O | P2O5 | +0.8748 | 17.4° | no |
| SiO2 | Al2O3 | +0.8686 | 1.2° | YES |
| FeO | MgO | +0.8479 | 20.1° | no |
| FeO | CaO | +0.8057 | 18.9° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| FeO | Na2O | -0.8384 | 10.9° | no |
| MgO | Na2O | -0.8740 | 12.1° | no |
| FeO | P2O5 | -0.9316 | 3.5° | YES |
| MgO | K2O | -0.9522 | 10.0° | no |
| FeO | K2O | -0.9672 | 22.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| SiO2 | TiO2 | 2.528 | 2.734 | -0.593 | -0.332 |
| SiO2 | Al2O3 | 2.528 | 2.734 | 1.352 | 1.508 |
| SiO2 | FeO | 2.528 | 2.734 | 1.004 | 1.230 |
| SiO2 | CaO | 2.528 | 2.734 | 0.499 | 1.156 |
| SiO2 | MgO | 2.528 | 2.734 | 0.345 | 0.966 |
| SiO2 | MnO | 2.528 | 2.734 | -3.067 | -2.511 |
| SiO2 | K2O | 2.528 | 2.734 | -1.658 | -0.623 |
| SiO2 | Na2O | 2.528 | 2.734 | -0.263 | -0.022 |
| SiO2 | P2O5 | 2.528 | 2.734 | -2.365 | -1.800 |
| TiO2 | Al2O3 | -0.593 | -0.332 | 1.352 | 1.508 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*