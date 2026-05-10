# Stage 1 Report (pure CoDa) — energy_ember_usa

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for the United States, annual TWh, 2001-2025. 9 carriers (Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind).
**Citation / source:** EMBER Climate, Pipeline-ready dataset (https://ember-climate.org/data-tools/data-explorer/)

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:03Z
**cnt_content_sha256:** `43ce7a49a5edc4f6d0b5278e338029ecbddab9c755ec693fb2b942b440576b09`

## Input

- Source CSV: `ember_USA_United_States_generation_TWh.csv`
- Source SHA-256: `ecdb50b25cb5807b...`
- Records (T): **25**
- Carriers (D): **9**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind
- Closed-data SHA-256: `c18ec10635ffaec3...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2001 | 1.3439 | 37.5765 | — |
| 1 | 2002 | 1.3541 | 37.6197 | 0.5229 |
| 2 | 2003 | 1.3643 | 7.2854 | 31.9255 |
| 3 | 2004 | 1.3707 | 7.2028 | 0.2289 |
| 4 | 2005 | 1.3719 | 7.2022 | 0.2343 |
| ... | ... | ... | ... | ... |
| 22 | 2023 | 1.6297 | 4.4408 | 0.3132 |
| 23 | 2024 | 1.6342 | 4.5574 | 0.2720 |
| 24 | 2025 | 1.6699 | 4.5793 | 0.2448 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Other Renewables | +0.9995 | 82.9° | no |
| Bioenergy | Other Renewables | +0.9983 | 154.5° | no |
| Hydro | Nuclear | +0.9980 | 35.1° | no |
| Bioenergy | Nuclear | +0.9978 | 79.9° | no |
| Hydro | Other Renewables | +0.9977 | 112.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Solar | -0.9800 | 95.5° | no |
| Hydro | Solar | -0.9961 | 163.2° | no |
| Bioenergy | Solar | -0.9968 | 352.9° | no |
| Nuclear | Solar | -0.9981 | 104.3° | no |
| Other Renewables | Solar | -0.9991 | 355.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 36 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | -1.561 | 3.371 | 1.142 | 7.009 |
| Bioenergy | Gas | -1.561 | 3.371 | 1.909 | 5.926 |
| Bioenergy | Hydro | -1.561 | 3.371 | 0.091 | 4.931 |
| Bioenergy | Nuclear | -1.561 | 3.371 | 1.275 | 6.102 |
| Bioenergy | Other Fossil | -1.561 | 3.371 | -1.933 | 4.367 |
| Bioenergy | Other Renewables | -1.561 | 3.371 | -2.521 | 2.168 |
| Bioenergy | Solar | -1.561 | 3.371 | -35.151 | 0.570 |
| Bioenergy | Wind | -1.561 | 3.371 | -2.002 | 1.725 |
| Coal | Gas | 1.142 | 7.009 | 1.909 | 5.926 |
| Coal | Hydro | 1.142 | 7.009 | 0.091 | 4.931 |
| ... (26 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*