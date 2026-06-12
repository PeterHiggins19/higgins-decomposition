# Stage 1 Report (pure CoDa) — energy_owid_mar

**Domain:** energy
**Description:** OWID primary-energy consumption composition for MAR (MAR), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: MAR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `df658eeb0f9d976efd8ee164aa8257bdc7362ac05104ef98404bf7fc630d174e`

## Input

- Source CSV: `owid_energy_MAR.csv`
- Source SHA-256: `ad37f0c908c58bdc...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `d0c94e9b4817ad1e...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.9507 | 16.9216 | — |
| 1 | 1966 | 0.8627 | 16.8357 | 0.4905 |
| 2 | 1967 | 0.8079 | 16.7750 | 0.1700 |
| 3 | 1968 | 0.7755 | 16.7120 | 0.1957 |
| 4 | 1969 | 0.7870 | 16.6863 | 0.2132 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 0.9368 | 13.7590 | 1.3162 |
| 58 | 2023 | 1.0388 | 13.9920 | 1.5907 |
| 59 | 2024 | 1.0290 | 14.0043 | 0.2285 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Oil | Nuclear | +0.9983 | 25.9° | no |
| Oil | Biofuel | +0.9983 | 25.9° | no |
| Coal | Nuclear | +0.9024 | 25.2° | no |
| Coal | Biofuel | +0.9024 | 25.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Solar | -0.7602 | 184.7° | no |
| Hydro | Wind | -0.8670 | 159.5° | no |
| Oil | Wind | -0.9080 | 68.7° | no |
| Nuclear | Wind | -0.9105 | 306.9° | no |
| Wind | Biofuel | -0.9105 | 67.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 4.168 | 6.842 | 1.105 | 4.330 |
| Coal | Oil | 4.168 | 6.842 | 5.014 | 8.297 |
| Coal | Nuclear | 4.168 | 6.842 | -8.267 | -5.323 |
| Coal | Hydro | 4.168 | 6.842 | -0.903 | 6.209 |
| Coal | Solar | 4.168 | 6.842 | -6.914 | 1.802 |
| Coal | Wind | 4.168 | 6.842 | -5.931 | 3.069 |
| Coal | Biofuel | 4.168 | 6.842 | -8.267 | -5.323 |
| Gas | Oil | 1.105 | 4.330 | 5.014 | 8.297 |
| Gas | Nuclear | 1.105 | 4.330 | -8.267 | -5.323 |
| Gas | Hydro | 1.105 | 4.330 | -0.903 | 6.209 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*