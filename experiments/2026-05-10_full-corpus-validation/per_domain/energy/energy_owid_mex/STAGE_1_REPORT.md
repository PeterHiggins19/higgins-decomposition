# Stage 1 Report (pure CoDa) — energy_owid_mex

**Domain:** energy
**Description:** OWID primary-energy consumption composition for MEX (MEX), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: MEX

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `5ca8fff7ec8384a20e5639d9403da741de84cfaa4ba3b990292ba0dc0f9f41d2`

## Input

- Source CSV: `owid_energy_MEX.csv`
- Source SHA-256: `5814cbb44f184de4...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `6bbf09552c7a785f...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.9636 | 16.9283 | — |
| 1 | 1966 | 0.9765 | 16.9494 | 0.0727 |
| 2 | 1967 | 0.9670 | 16.9750 | 0.2606 |
| 3 | 1968 | 0.9697 | 16.9804 | 0.0664 |
| 4 | 1969 | 0.9838 | 16.9762 | 0.1543 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.1816 | 5.0728 | 0.2416 |
| 58 | 2023 | 1.1652 | 5.0410 | 0.6026 |
| 59 | 2024 | 1.1768 | 5.0328 | 0.1568 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9927 | 45.8° | no |
| Gas | Hydro | +0.9907 | 49.7° | no |
| Gas | Oil | +0.9887 | 9.1° | YES |
| Coal | Oil | +0.9851 | 38.2° | no |
| Coal | Hydro | +0.9786 | 283.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Nuclear | -0.7807 | 68.2° | no |
| Gas | Wind | -0.8467 | 47.6° | no |
| Hydro | Wind | -0.8790 | 96.5° | no |
| Coal | Wind | -0.8851 | 108.6° | no |
| Oil | Wind | -0.9055 | 41.2° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.282 | 4.659 | 2.514 | 6.602 |
| Coal | Oil | -0.282 | 4.659 | 2.491 | 7.583 |
| Coal | Nuclear | -0.282 | 4.659 | -5.968 | 2.053 |
| Coal | Hydro | -0.282 | 4.659 | -0.393 | 5.595 |
| Coal | Solar | -0.282 | 4.659 | -6.733 | -0.197 |
| Coal | Wind | -0.282 | 4.659 | -6.733 | -0.342 |
| Coal | Biofuel | -0.282 | 4.659 | -7.880 | -2.326 |
| Gas | Oil | 2.514 | 6.602 | 2.491 | 7.583 |
| Gas | Nuclear | 2.514 | 6.602 | -5.968 | 2.053 |
| Gas | Hydro | 2.514 | 6.602 | -0.393 | 5.595 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*