# Stage 1 Report (pure CoDa) — geochem_stracke_morb

**Domain:** geochemistry
**Description:** Stracke MORB (mid-ocean ridge basalt) major-oxide composition, by ocean basin. T = 5 locations, D = 10 oxide carriers (SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5).
**Citation / source:** Stracke A. (2022) — Geochem Earthchem 2022_09-0SVW6S

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:04Z
**cnt_content_sha256:** `017ed5dcd2afb80ff6b8eba210bf44c8c5b4327ec47c35d37bdc3ea4afedd8f8`

## Input

- Source CSV: `geochem_stracke_morb_input.csv`
- Source SHA-256: `72945b32a6dfa09e...`
- Records (T): **5**
- Carriers (D): **10**
- Carriers: SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5
- Closed-data SHA-256: `912144a6b99e3f35...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | MORB-Arctic | 1.5237 | 5.3715 | — |
| 1 | MORB-Atlantic | 1.4986 | 6.1051 | 1.5745 |
| 2 | MORB-Gakkel | 1.4935 | 5.9421 | 0.5391 |
| 3 | MORB-Indian | 1.4904 | 6.4971 | 0.7071 |
| 4 | MORB-Pacific | 1.5107 | 6.0939 | 0.4740 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | CaO | +0.9884 | 4.0° | YES |
| SiO2 | MgO | +0.9851 | 7.5° | YES |
| CaO | MgO | +0.9590 | 8.4° | YES |
| SiO2 | Al2O3 | +0.9536 | 1.1° | YES |
| Al2O3 | CaO | +0.9523 | 4.1° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Al2O3 | P2O5 | -0.9066 | 2.4° | YES |
| CaO | K2O | -0.9416 | 17.7° | no |
| SiO2 | K2O | -0.9495 | 20.0° | no |
| Na2O | P2O5 | -0.9679 | 4.8° | YES |
| MgO | K2O | -0.9779 | 8.8° | YES |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| SiO2 | TiO2 | 2.737 | 3.030 | -0.598 | -0.464 |
| SiO2 | Al2O3 | 2.737 | 3.030 | 1.627 | 1.868 |
| SiO2 | FeO | 2.737 | 3.030 | 0.869 | 1.312 |
| SiO2 | CaO | 2.737 | 3.030 | 1.159 | 1.541 |
| SiO2 | MgO | 2.737 | 3.030 | 0.634 | 1.136 |
| SiO2 | MnO | 2.737 | 3.030 | -2.989 | -2.510 |
| SiO2 | K2O | 2.737 | 3.030 | -2.732 | -1.110 |
| SiO2 | Na2O | 2.737 | 3.030 | -0.047 | 0.182 |
| SiO2 | P2O5 | 2.737 | 3.030 | -2.893 | -2.414 |
| TiO2 | Al2O3 | -0.598 | -0.464 | 1.627 | 1.868 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*