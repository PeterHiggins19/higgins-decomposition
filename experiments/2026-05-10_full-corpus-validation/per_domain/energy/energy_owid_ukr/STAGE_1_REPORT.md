# Stage 1 Report (pure CoDa) — energy_owid_ukr

**Domain:** energy
**Description:** OWID primary-energy consumption composition for UKR (UKR), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: UKR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `c073955b1bc0ee7dc6c26c58d2ee5934caebd36c4cc5c0f8aa607aa5ab165fa7`

## Input

- Source CSV: `owid_energy_UKR.csv`
- Source SHA-256: `2692716fd9dc125f...`
- Records (T): **40**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `8967c1f1a8867c01...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 1.2898 | 16.1975 | — |
| 1 | 1986 | 1.2695 | 16.1594 | 0.2209 |
| 2 | 1987 | 1.2797 | 16.1708 | 0.1952 |
| 3 | 1988 | 1.3187 | 16.2509 | 0.3981 |
| 4 | 1989 | 1.3085 | 16.2301 | 0.1346 |
| ... | ... | ... | ... | ... |
| 37 | 2022 | 1.5907 | 5.5501 | 0.9217 |
| 38 | 2023 | 1.6004 | 5.6115 | 0.4846 |
| 39 | 2024 | 1.5809 | 6.2845 | 1.2504 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Gas | +0.9859 | 11.2° | no |
| Gas | Nuclear | +0.9731 | 10.1° | no |
| Coal | Oil | +0.9649 | 14.8° | no |
| Gas | Hydro | +0.9630 | 44.0° | no |
| Nuclear | Hydro | +0.9605 | 53.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Wind | -0.9196 | 22.4° | no |
| Hydro | Solar | -0.9363 | 75.8° | no |
| Coal | Solar | -0.9484 | 46.1° | no |
| Gas | Solar | -0.9618 | 48.8° | no |
| Nuclear | Solar | -0.9654 | 52.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.456 | 5.533 | 1.931 | 5.785 |
| Coal | Oil | 1.456 | 5.533 | 1.170 | 5.298 |
| Coal | Nuclear | 1.456 | 5.533 | 1.623 | 4.454 |
| Coal | Hydro | 1.456 | 5.533 | -0.709 | 2.602 |
| Coal | Solar | 1.456 | 5.533 | -7.972 | -0.385 |
| Coal | Wind | 1.456 | 5.533 | -7.357 | -1.401 |
| Coal | Biofuel | 1.456 | 5.533 | -8.956 | -3.498 |
| Gas | Oil | 1.931 | 5.785 | 1.170 | 5.298 |
| Gas | Nuclear | 1.931 | 5.785 | 1.623 | 4.454 |
| Gas | Hydro | 1.931 | 5.785 | -0.709 | 2.602 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*