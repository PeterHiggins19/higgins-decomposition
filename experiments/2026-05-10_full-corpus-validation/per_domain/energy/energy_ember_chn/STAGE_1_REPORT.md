# Stage 1 Report (pure CoDa) — energy_ember_chn

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for China, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:03Z
**cnt_content_sha256:** `de35a9b5d6193809d84e0614b3405112ec9b88a64fda60b1d0941d1e5c892bb6`

## Input

- Source CSV: `ember_CHN_China_generation_TWh.csv`
- Source SHA-256: `f47e4af61ed44a17...`
- Records (T): **26**
- Carriers (D): **8**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind
- Closed-data SHA-256: `b3dc013107556ed6...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2000 | 0.6986 | 9.0941 | — |
| 1 | 2001 | 0.7188 | 8.9001 | 0.4509 |
| 2 | 2002 | 0.7013 | 8.6660 | 0.5644 |
| 3 | 2003 | 0.6820 | 8.6443 | 0.4638 |
| 4 | 2004 | 0.7089 | 8.5566 | 0.2977 |
| ... | ... | ... | ... | ... |
| 23 | 2023 | 1.3317 | 3.4237 | 0.2798 |
| 24 | 2024 | 1.3926 | 3.3822 | 0.2907 |
| 25 | 2025 | 1.4521 | 3.4204 | 0.2995 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Hydro | +0.9941 | 16.1° | no |
| Coal | Other Fossil | +0.9145 | 61.9° | no |
| Hydro | Other Fossil | +0.9121 | 96.7° | no |
| Coal | Nuclear | +0.9029 | 21.9° | no |
| Nuclear | Other Fossil | +0.8983 | 168.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Wind | -0.9191 | 75.7° | no |
| Nuclear | Wind | -0.9375 | 347.8° | no |
| Hydro | Solar | -0.9840 | 100.7° | no |
| Other Fossil | Wind | -0.9866 | 359.1° | no |
| Coal | Solar | -0.9914 | 66.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | -1.832 | -0.745 | 2.175 | 4.805 |
| Bioenergy | Gas | -1.832 | -0.745 | -0.963 | 0.253 |
| Bioenergy | Hydro | -1.832 | -0.745 | 0.760 | 3.364 |
| Bioenergy | Nuclear | -1.832 | -0.745 | -0.293 | 1.206 |
| Bioenergy | Other Fossil | -1.832 | -0.745 | -2.063 | 1.695 |
| Bioenergy | Solar | -1.832 | -0.745 | -6.073 | 0.586 |
| Bioenergy | Wind | -1.832 | -0.745 | -2.689 | 0.552 |
| Coal | Gas | 2.175 | 4.805 | -0.963 | 0.253 |
| Coal | Hydro | 2.175 | 4.805 | 0.760 | 3.364 |
| Coal | Nuclear | 2.175 | 4.805 | -0.293 | 1.206 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*