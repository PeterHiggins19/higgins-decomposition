# Stage 1 Report (pure CoDa) — energy_owid_kor

**Domain:** energy
**Description:** OWID primary-energy consumption composition for KOR (KOR), annual TWh. T = 48 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: KOR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `08fd8fab5f4387018164ebc4f132e718f962b0666592879921cf1dfbe9303034`

## Input

- Source CSV: `owid_energy_KOR.csv`
- Source SHA-256: `7a7adfcea53ce99c...`
- Records (T): **48**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `2b52e7500fa0fd76...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1977 | 0.6985 | 15.8200 | — |
| 1 | 1978 | 0.7563 | 16.3669 | 3.1471 |
| 2 | 1979 | 0.7810 | 16.4333 | 0.1677 |
| 3 | 1980 | 0.7929 | 16.4221 | 0.2331 |
| 4 | 1981 | 0.8099 | 16.4380 | 0.3603 |
| ... | ... | ... | ... | ... |
| 45 | 2022 | 1.3948 | 6.0202 | 0.2401 |
| 46 | 2023 | 1.4030 | 5.9641 | 0.0997 |
| 47 | 2024 | 1.4031 | 5.8899 | 0.1747 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Hydro | +0.9915 | 79.2° | no |
| Coal | Oil | +0.9879 | 7.4° | YES |
| Oil | Hydro | +0.9870 | 71.0° | no |
| Solar | Biofuel | +0.8707 | 51.2° | no |
| Solar | Wind | +0.8654 | 53.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Solar | -0.8294 | 121.9° | no |
| Oil | Solar | -0.8384 | 47.2° | no |
| Nuclear | Biofuel | -0.8671 | 30.2° | no |
| Nuclear | Wind | -0.8702 | 37.4° | no |
| Nuclear | Solar | -0.9068 | 66.9° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.972 | 7.491 | -5.854 | 3.931 |
| Coal | Oil | 1.972 | 7.491 | 2.637 | 8.167 |
| Coal | Nuclear | 1.972 | 7.491 | 1.140 | 5.367 |
| Coal | Hydro | 1.972 | 7.491 | -2.584 | 4.110 |
| Coal | Solar | 1.972 | 7.491 | -7.188 | -0.272 |
| Coal | Wind | 1.972 | 7.491 | -7.275 | -2.528 |
| Coal | Biofuel | 1.972 | 7.491 | -8.115 | -2.384 |
| Gas | Oil | -5.854 | 3.931 | 2.637 | 8.167 |
| Gas | Nuclear | -5.854 | 3.931 | 1.140 | 5.367 |
| Gas | Hydro | -5.854 | 3.931 | -2.584 | 4.110 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*