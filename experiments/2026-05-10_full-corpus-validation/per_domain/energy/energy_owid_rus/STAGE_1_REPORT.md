# Stage 1 Report (pure CoDa) — energy_owid_rus

**Domain:** energy
**Description:** OWID primary-energy consumption composition for RUS (RUS), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: RUS

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `1b79a04d41d549780eda410b3db09ad2cdb71ad7b6ef665f47c6b8d9f7f99787`

## Input

- Source CSV: `owid_energy_RUS.csv`
- Source SHA-256: `67e2e70e3ee571e9...`
- Records (T): **40**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `08bbb7c8a704386e...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 1.3195 | 16.2994 | — |
| 1 | 1986 | 1.3242 | 16.3079 | 0.0399 |
| 2 | 1987 | 1.3276 | 16.3194 | 0.1467 |
| 3 | 1988 | 1.3243 | 16.3197 | 0.0861 |
| 4 | 1989 | 1.3205 | 16.3160 | 0.0434 |
| ... | ... | ... | ... | ... |
| 37 | 2022 | 1.2913 | 7.4898 | 0.4991 |
| 38 | 2023 | 1.2885 | 7.3066 | 0.2296 |
| 39 | 2024 | 1.2751 | 7.2031 | 0.2149 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9963 | 9.0° | YES |
| Gas | Hydro | +0.9962 | 15.3° | no |
| Gas | Nuclear | +0.9882 | 13.6° | no |
| Nuclear | Hydro | +0.9783 | 8.2° | YES |
| Coal | Hydro | +0.9696 | 9.3° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Solar | -0.9610 | 13.4° | no |
| Gas | Solar | -0.9638 | 14.4° | no |
| Oil | Wind | -0.9659 | 10.8° | no |
| Coal | Wind | -0.9660 | 9.8° | YES |
| Hydro | Solar | -0.9672 | 15.4° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.729 | 5.038 | 3.247 | 5.774 |
| Coal | Oil | 1.729 | 5.038 | 2.444 | 5.278 |
| Coal | Nuclear | 1.729 | 5.038 | 1.046 | 3.517 |
| Coal | Hydro | 1.729 | 5.038 | 1.022 | 3.675 |
| Coal | Solar | 1.729 | 5.038 | -7.552 | -3.255 |
| Coal | Wind | 1.729 | 5.038 | -7.414 | -2.723 |
| Coal | Biofuel | 1.729 | 5.038 | -8.475 | -3.426 |
| Gas | Oil | 3.247 | 5.774 | 2.444 | 5.278 |
| Gas | Nuclear | 3.247 | 5.774 | 1.046 | 3.517 |
| Gas | Hydro | 3.247 | 5.774 | 1.022 | 3.675 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*