# Stage 1 Report (pure CoDa) — energy_owid_tkm

**Domain:** energy
**Description:** OWID primary-energy consumption composition for TKM (TKM), annual TWh. T = 26 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: TKM

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `8ccee34829b5754c4fbc7ca817f67e847b7cd8346a21a5f8b3abebff26b84c13`

## Input

- Source CSV: `owid_energy_TKM.csv`
- Source SHA-256: `2481963bd9c2e094...`
- Records (T): **26**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `fee8734a936c8357...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 0.7821 | 16.0714 | — |
| 1 | 1986 | 0.6426 | 15.8985 | 0.6243 |
| 2 | 1987 | 0.6441 | 15.9014 | 0.0076 |
| 3 | 1988 | 0.6307 | 15.8534 | 0.1493 |
| 4 | 1989 | 0.6319 | 15.8838 | 0.1300 |
| ... | ... | ... | ... | ... |
| 23 | 2022 | 0.5069 | 15.0063 | 0.0929 |
| 24 | 2023 | 0.4940 | 14.9828 | 0.1000 |
| 25 | 2024 | 0.5418 | 15.0303 | 0.2486 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Wind | +1.0000 | 0.0° | YES |
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Wind | Biofuel | +1.0000 | 0.0° | YES |
| Gas | Nuclear | +0.9900 | 10.6° | no |
| Gas | Wind | +0.9900 | 10.6° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Solar | -0.9411 | 133.5° | no |
| Coal | Gas | -0.9692 | 55.9° | no |
| Coal | Nuclear | -0.9786 | 90.6° | no |
| Coal | Wind | -0.9786 | 90.6° | no |
| Coal | Biofuel | -0.9786 | 90.6° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -4.136 | 5.152 | 8.206 | 9.764 |
| Coal | Oil | -4.136 | 5.152 | 7.387 | 8.715 |
| Coal | Nuclear | -4.136 | 5.152 | -5.050 | -3.750 |
| Coal | Hydro | -4.136 | 5.152 | -1.228 | 0.045 |
| Coal | Solar | -4.136 | 5.152 | -5.050 | -0.152 |
| Coal | Wind | -4.136 | 5.152 | -5.050 | -3.750 |
| Coal | Biofuel | -4.136 | 5.152 | -5.050 | -3.750 |
| Gas | Oil | 8.206 | 9.764 | 7.387 | 8.715 |
| Gas | Nuclear | 8.206 | 9.764 | -5.050 | -3.750 |
| Gas | Hydro | 8.206 | 9.764 | -1.228 | 0.045 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*