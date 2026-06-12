# Stage 1 Report (pure CoDa) — energy_ember_fra

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for France, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:03Z
**cnt_content_sha256:** `5dae940f20941c6f902b8195a8a32c753cef7bee32fe43c1f584b2e1e48c1e0f`

## Input

- Source CSV: `ember_FRA_France_generation_TWh.csv`
- Source SHA-256: `7d929d9c4c7d1b47...`
- Records (T): **26**
- Carriers (D): **9**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind
- Closed-data SHA-256: `e1216f5daefb7ee5...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2000 | 0.7976 | 9.7172 | — |
| 1 | 2001 | 0.7980 | 9.3571 | 0.9978 |
| 2 | 2002 | 0.7821 | 9.1189 | 0.7323 |
| 3 | 2003 | 0.7991 | 9.0479 | 0.3386 |
| 4 | 2004 | 0.7920 | 8.9575 | 0.4205 |
| ... | ... | ... | ... | ... |
| 23 | 2023 | 1.2212 | 5.4304 | 1.0948 |
| 24 | 2024 | 1.1407 | 5.7126 | 0.7272 |
| 25 | 2025 | 1.1342 | 5.4770 | 0.5862 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Other Fossil | +0.9890 | 23.6° | no |
| Other Fossil | Other Renewables | +0.9782 | 40.9° | no |
| Hydro | Nuclear | +0.9745 | 13.4° | no |
| Nuclear | Other Renewables | +0.9738 | 28.0° | no |
| Hydro | Other Renewables | +0.9681 | 40.8° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Other Renewables | Solar | -0.9288 | 355.7° | no |
| Other Fossil | Wind | -0.9389 | 298.9° | no |
| Other Renewables | Wind | -0.9477 | 358.5° | no |
| Other Fossil | Solar | -0.9629 | 332.2° | no |
| Nuclear | Solar | -0.9691 | 67.4° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 36 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | -1.008 | -0.288 | -2.671 | 2.076 |
| Bioenergy | Gas | -1.008 | -0.288 | -0.043 | 1.493 |
| Bioenergy | Hydro | -1.008 | -0.288 | 0.990 | 2.951 |
| Bioenergy | Nuclear | -1.008 | -0.288 | 2.857 | 4.809 |
| Bioenergy | Other Fossil | -1.008 | -0.288 | -0.531 | 1.184 |
| Bioenergy | Other Renewables | -1.008 | -0.288 | -3.395 | -1.893 |
| Bioenergy | Solar | -1.008 | -0.288 | -6.315 | 0.698 |
| Bioenergy | Wind | -1.008 | -0.288 | -4.215 | 1.170 |
| Coal | Gas | -2.671 | 2.076 | -0.043 | 1.493 |
| Coal | Hydro | -2.671 | 2.076 | 0.990 | 2.951 |
| ... (26 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*