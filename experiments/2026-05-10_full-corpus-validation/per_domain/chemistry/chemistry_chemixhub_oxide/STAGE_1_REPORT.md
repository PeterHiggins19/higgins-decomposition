# Stage 1 Report (pure CoDa) — chemistry_chemixhub_oxide

**Domain:** chemistry
**Description:** Chemixhub oxide compositional samples — synthetic-style mineral oxide compositions across 25 catalogued samples; D = 7 oxide carriers.
**Citation / source:** ChemixHub project, github.com/chemixhub (oxide composition subset)

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:04Z
**cnt_content_sha256:** `e59d789783ebdf0d68ecd7826f396b24c37f52587a38956c752715387b5ce2e4`

## Input

- Source CSV: `chemixhub_oxide_input.csv`
- Source SHA-256: `9968c4a135c8b7a5...`
- Records (T): **24**
- Carriers (D): **7**
- Carriers: SiO2, TiO2, Al2O3, Fe2O3, MgO, CaO, Na2O
- Closed-data SHA-256: `4c4cbb9d8e3b81c9...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | sample_00 | 1.6084 | 2.1480 | — |
| 1 | sample_01 | 1.6207 | 2.1227 | 0.1482 |
| 2 | sample_02 | 1.6268 | 2.1153 | 0.1180 |
| 3 | sample_03 | 1.6256 | 2.1240 | 0.0921 |
| 4 | sample_04 | 1.6174 | 2.1463 | 0.0926 |
| ... | ... | ... | ... | ... |
| 21 | sample_21 | 1.5489 | 2.2501 | 0.1009 |
| 22 | sample_22 | 1.5418 | 2.2722 | 0.1179 |
| 23 | sample_23 | 1.5448 | 2.2598 | 0.1545 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Al2O3 | CaO | +0.9520 | 35.2° | no |
| TiO2 | MgO | +0.5638 | 16.6° | no |
| Fe2O3 | Na2O | +0.4359 | 23.1° | no |
| Fe2O3 | MgO | +0.3938 | 88.7° | no |
| SiO2 | Al2O3 | +0.3680 | 11.0° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Al2O3 | MgO | -0.6327 | 29.2° | no |
| MgO | CaO | -0.6779 | 65.7° | no |
| Al2O3 | Fe2O3 | -0.7533 | 46.7° | no |
| SiO2 | TiO2 | -0.8015 | 10.5° | no |
| Fe2O3 | CaO | -0.8873 | 112.1° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 21 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| SiO2 | TiO2 | 1.366 | 1.627 | -1.174 | -0.721 |
| SiO2 | Al2O3 | 1.366 | 1.627 | 0.267 | 0.611 |
| SiO2 | Fe2O3 | 1.366 | 1.627 | -0.209 | 0.184 |
| SiO2 | MgO | 1.366 | 1.627 | -0.395 | -0.067 |
| SiO2 | CaO | 1.366 | 1.627 | 0.011 | 0.468 |
| SiO2 | Na2O | 1.366 | 1.627 | -1.231 | -0.786 |
| TiO2 | Al2O3 | -1.174 | -0.721 | 0.267 | 0.611 |
| TiO2 | Fe2O3 | -1.174 | -0.721 | -0.209 | 0.184 |
| TiO2 | MgO | -1.174 | -0.721 | -0.395 | -0.067 |
| TiO2 | CaO | -1.174 | -0.721 | 0.011 | 0.468 |
| ... (11 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*