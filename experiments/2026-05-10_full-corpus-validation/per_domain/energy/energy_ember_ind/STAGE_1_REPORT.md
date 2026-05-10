# Stage 1 Report (pure CoDa) — energy_ember_ind

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for India, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:03Z
**cnt_content_sha256:** `a299b9bfb449c89a37f812f1326cc5fc4430aed90e6998507790970ee252373a`

## Input

- Source CSV: `ember_IND_India_generation_TWh.csv`
- Source SHA-256: `05cde94fa8f37b98...`
- Records (T): **26**
- Carriers (D): **8**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind
- Closed-data SHA-256: `b8cb88ec7cd1c9bf...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2000 | 1.0427 | 8.7110 | — |
| 1 | 2001 | 1.0256 | 8.6322 | 0.3563 |
| 2 | 2002 | 1.0200 | 8.6676 | 0.1264 |
| 3 | 2003 | 1.0380 | 8.1102 | 0.6194 |
| 4 | 2004 | 1.0925 | 8.0990 | 0.6706 |
| ... | ... | ... | ... | ... |
| 23 | 2023 | 0.9703 | 4.4611 | 0.2859 |
| 24 | 2024 | 0.9900 | 4.4858 | 0.2077 |
| 25 | 2025 | 1.0711 | 4.5582 | 0.4061 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Hydro | +0.9477 | 76.0° | no |
| Coal | Hydro | +0.9457 | 16.4° | no |
| Gas | Other Fossil | +0.9449 | 132.5° | no |
| Coal | Other Fossil | +0.9448 | 63.1° | no |
| Hydro | Other Fossil | +0.9440 | 104.8° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Solar | -0.9239 | 80.3° | no |
| Nuclear | Wind | -0.9480 | 351.5° | no |
| Other Fossil | Solar | -0.9703 | 356.6° | no |
| Hydro | Solar | -0.9735 | 121.6° | no |
| Gas | Solar | -0.9848 | 208.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | -1.581 | -0.516 | 2.944 | 3.861 |
| Bioenergy | Gas | -1.581 | -0.516 | -0.470 | 1.940 |
| Bioenergy | Hydro | -1.581 | -0.516 | 0.767 | 2.238 |
| Bioenergy | Nuclear | -1.581 | -0.516 | -0.392 | 0.764 |
| Bioenergy | Other Fossil | -1.581 | -0.516 | -2.941 | 1.267 |
| Bioenergy | Solar | -1.581 | -0.516 | -7.159 | 0.926 |
| Bioenergy | Wind | -1.581 | -0.516 | -1.648 | 0.292 |
| Coal | Gas | 2.944 | 3.861 | -0.470 | 1.940 |
| Coal | Hydro | 2.944 | 3.861 | 0.767 | 2.238 |
| Coal | Nuclear | 2.944 | 3.861 | -0.392 | 0.764 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*