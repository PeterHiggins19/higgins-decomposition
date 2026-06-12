# Stage 1 Report (pure CoDa) — geochem_qin_cpx

**Domain:** geochemistry
**Description:** Qin et al. (2024) clinopyroxene mineral spot analyses from intra-cratonic mantle xenoliths and ultramafic rocks. T = 30 top locations (>=10 spots each), D = 9 oxides (SiO2, TiO2, Al2O3, Cr2O3, FeO, CaO, MgO, MnO, Na2O — note Cr2O3 replaces K2O for clinopyroxene). Crucial test for whether the K2O-prefix in the helmsman lineage is specifically potassium or 'dominant alkali in general'.
**Citation / source:** Qin Y. et al. (2024) — Geochem Earthchem 2024-007_AVAW2Y_Qin_data

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:13Z
**cnt_content_sha256:** `0c09c3d953f8a60a781ede2d7df5c089f8d31c3c9604ff70896c80b057815c12`

## Input

- Source CSV: `qin_cpx_by_location_barycenters.csv`
- Source SHA-256: `b85e5060cb4c1a3d...`
- Records (T): **30**
- Carriers (D): **9**
- Carriers: SiO2, TiO2, Al2O3, Cr2O3, FeO, CaO, MgO, MnO, Na2O
- Closed-data SHA-256: `bfd0608a55eb1dec...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | FUERTEVENTURA | 1.3615 | 6.2331 | — |
| 1 | MEGATA_-_ICHINOMEGATA_MAAR | 1.2748 | 6.3843 | 2.4860 |
| 2 | UDACHNAYA_KIMBERLITE | 1.2441 | 6.1940 | 1.8302 |
| 3 | NOGRAD-G諱諶_VOLCANIC_FIELD | 1.3426 | 5.8875 | 1.4604 |
| 4 | BUSHVELD_UPPER_ZONE_-_UG2_LAYE | 1.2746 | 6.0413 | 1.7294 |
| ... | ... | ... | ... | ... |
| 27 | JAGERSFONTEIN_KIMBERLITE | 1.2569 | 6.1579 | 1.4682 |
| 28 | MOUNT_MELBOURNE | 1.3219 | 5.9212 | 1.6385 |
| 29 | MAIN_ETHIOPIAN_RIFT | 1.4292 | 6.1549 | 2.7171 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | MgO | +0.9619 | 4.9° | YES |
| SiO2 | CaO | +0.8670 | 3.5° | YES |
| FeO | MnO | +0.8395 | 28.3° | no |
| CaO | MgO | +0.7922 | 8.6° | YES |
| Cr2O3 | MgO | +0.5010 | 56.8° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Al2O3 | MgO | -0.6833 | 62.6° | no |
| FeO | Na2O | -0.7147 | 130.0° | no |
| TiO2 | Cr2O3 | -0.7607 | 79.9° | no |
| SiO2 | TiO2 | -0.7613 | 39.8° | no |
| TiO2 | MgO | -0.7644 | 47.9° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 36 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| SiO2 | TiO2 | 2.773 | 3.489 | -3.205 | -0.240 |
| SiO2 | Al2O3 | 2.773 | 3.489 | -1.110 | 1.011 |
| SiO2 | Cr2O3 | 2.773 | 3.489 | -3.378 | -0.261 |
| SiO2 | FeO | 2.773 | 3.489 | -0.540 | 0.924 |
| SiO2 | CaO | 2.773 | 3.489 | 1.882 | 2.579 |
| SiO2 | MgO | 2.773 | 3.489 | 1.496 | 2.244 |
| SiO2 | MnO | 2.773 | 3.489 | -3.887 | -2.291 |
| SiO2 | Na2O | 2.773 | 3.489 | -2.203 | -0.222 |
| TiO2 | Al2O3 | -3.205 | -0.240 | -1.110 | 1.011 |
| TiO2 | Cr2O3 | -3.205 | -0.240 | -3.378 | -0.261 |
| ... (26 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*