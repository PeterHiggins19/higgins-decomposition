# Stage 1 Report (pure CoDa) — energy_ember_wld

**Domain:** energy
**Description:** EMBER electricity-generation-by-source aggregated for the World, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:03Z
**cnt_content_sha256:** `cedb9bde2ff40f43b13d5163d718889c7c6a7f37d0c0a16c738705cf8b4543c4`

## Input

- Source CSV: `ember_WLD_World_generation_TWh.csv`
- Source SHA-256: `eff4a4d3ffe97ec1...`
- Records (T): **26**
- Carriers (D): **9**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind
- Closed-data SHA-256: `8a5e5db5dc20f45a...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2000 | 1.5656 | 8.1695 | — |
| 1 | 2001 | 1.5632 | 7.9287 | 0.3185 |
| 2 | 2002 | 1.5623 | 7.7048 | 0.3117 |
| 3 | 2003 | 1.5530 | 7.5392 | 0.2274 |
| 4 | 2004 | 1.5577 | 7.3180 | 0.3178 |
| ... | ... | ... | ... | ... |
| 23 | 2023 | 1.7687 | 4.0377 | 0.2140 |
| 24 | 2024 | 1.7867 | 4.0713 | 0.2303 |
| 25 | 2025 | 1.8081 | 4.0871 | 0.2455 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Nuclear | +0.9957 | 20.9° | no |
| Nuclear | Other Renewables | +0.9955 | 39.6° | no |
| Coal | Gas | +0.9954 | 2.5° | YES |
| Coal | Hydro | +0.9948 | 9.8° | YES |
| Coal | Other Fossil | +0.9945 | 52.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Wind | -0.9941 | 69.8° | no |
| Nuclear | Solar | -0.9959 | 114.2° | no |
| Hydro | Solar | -0.9967 | 93.7° | no |
| Gas | Solar | -0.9980 | 85.3° | no |
| Coal | Solar | -0.9986 | 75.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 36 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | -0.997 | -0.713 | 1.693 | 2.916 |
| Bioenergy | Gas | -0.997 | -0.713 | 1.279 | 2.169 |
| Bioenergy | Hydro | -0.997 | -0.713 | 0.834 | 2.123 |
| Bioenergy | Nuclear | -0.997 | -0.713 | 0.379 | 2.089 |
| Bioenergy | Other Fossil | -0.997 | -0.713 | -0.828 | 1.437 |
| Bioenergy | Other Renewables | -0.997 | -0.713 | -3.071 | -1.975 |
| Bioenergy | Solar | -0.997 | -0.713 | -5.731 | 0.367 |
| Bioenergy | Wind | -0.997 | -0.713 | -2.312 | 0.343 |
| Coal | Gas | 1.693 | 2.916 | 1.279 | 2.169 |
| Coal | Hydro | 1.693 | 2.916 | 0.834 | 2.123 |
| ... (26 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*