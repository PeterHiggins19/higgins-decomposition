# Stage 1 Report (pure CoDa) — energy_owid_nld

**Domain:** energy
**Description:** OWID primary-energy consumption composition for NLD (NLD), annual TWh. T = 57 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: NLD

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `37a33c1592820956f0a07b4190d6a40dba5030b4b5ffbf26182e3b716016e830`

## Input

- Source CSV: `owid_energy_NLD.csv`
- Source SHA-256: `2b9c80d755bc8137...`
- Records (T): **57**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `eb39f1818ee9e129...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1968 | 0.8577 | 16.3770 | — |
| 1 | 1969 | 0.8735 | 16.4722 | 2.1981 |
| 2 | 1970 | 0.8460 | 16.4049 | 0.4819 |
| 3 | 1971 | 0.8434 | 16.3572 | 0.4014 |
| 4 | 1972 | 0.8237 | 16.2515 | 0.4444 |
| ... | ... | ... | ... | ... |
| 54 | 2022 | 1.3046 | 6.7473 | 0.7916 |
| 55 | 2023 | 1.3078 | 6.5019 | 0.6074 |
| 56 | 2024 | 1.3479 | 6.3985 | 0.3413 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Oil | +0.9882 | 6.9° | YES |
| Coal | Oil | +0.9755 | 30.1° | no |
| Coal | Gas | +0.9682 | 33.3° | no |
| Gas | Nuclear | +0.9275 | 55.3° | no |
| Oil | Nuclear | +0.8706 | 50.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Solar | -0.8312 | 69.0° | no |
| Coal | Solar | -0.8473 | 116.0° | no |
| Coal | Wind | -0.8608 | 114.8° | no |
| Gas | Wind | -0.9055 | 67.2° | no |
| Oil | Wind | -0.9204 | 63.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.466 | 6.700 | 2.227 | 7.351 |
| Coal | Oil | 0.466 | 6.700 | 2.732 | 8.120 |
| Coal | Nuclear | 0.466 | 6.700 | -1.173 | 3.701 |
| Coal | Hydro | 0.466 | 6.700 | -5.866 | -1.514 |
| Coal | Solar | 0.466 | 6.700 | -7.400 | 0.627 |
| Coal | Wind | 0.466 | 6.700 | -6.155 | 1.060 |
| Coal | Biofuel | 0.466 | 6.700 | -8.120 | -0.813 |
| Gas | Oil | 2.227 | 7.351 | 2.732 | 8.120 |
| Gas | Nuclear | 2.227 | 7.351 | -1.173 | 3.701 |
| Gas | Hydro | 2.227 | 7.351 | -5.866 | -1.514 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*