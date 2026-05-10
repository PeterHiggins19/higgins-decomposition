# Stage 1 Report (pure CoDa) — energy_owid_hkg

**Domain:** energy
**Description:** OWID primary-energy consumption composition for HKG (HKG), annual TWh. T = 19 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: HKG

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `164b4fdb03c0566a93bb46509a66beb48ea8b0cfd5229c889c56e208e86876cb`

## Input

- Source CSV: `owid_energy_HKG.csv`
- Source SHA-256: `a7ca19e9d6524137...`
- Records (T): **19**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `dd5e2d1c713cd744...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2006 | 0.8759 | 16.6764 | — |
| 1 | 2007 | 0.8588 | 16.6148 | 0.2016 |
| 2 | 2008 | 0.8942 | 16.6803 | 0.2113 |
| 3 | 2009 | 0.8627 | 16.5967 | 0.2505 |
| 4 | 2010 | 0.8553 | 15.1540 | 4.7304 |
| ... | ... | ... | ... | ... |
| 16 | 2022 | 0.9946 | 14.7373 | 0.5247 |
| 17 | 2023 | 0.9476 | 14.7613 | 0.5027 |
| 18 | 2024 | 0.9019 | 14.7392 | 0.2530 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Hydro | +1.0000 | 0.0° | YES |
| Oil | Nuclear | +0.9977 | 18.0° | no |
| Oil | Hydro | +0.9977 | 18.0° | no |
| Coal | Nuclear | +0.9858 | 23.1° | no |
| Coal | Hydro | +0.9858 | 23.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Solar | -0.9484 | 353.7° | no |
| Oil | Solar | -0.9563 | 39.6° | no |
| Wind | Biofuel | -0.9606 | 338.4° | no |
| Gas | Biofuel | -0.9692 | 54.7° | no |
| Coal | Solar | -0.9697 | 44.8° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 4.763 | 7.653 | 5.042 | 6.632 |
| Coal | Oil | 4.763 | 7.653 | 6.277 | 8.441 |
| Coal | Nuclear | 4.763 | 7.653 | -7.032 | -4.904 |
| Coal | Hydro | 4.763 | 7.653 | -7.032 | -4.904 |
| Coal | Solar | 4.763 | 7.653 | -4.944 | 1.020 |
| Coal | Wind | 4.763 | 7.653 | -4.985 | -2.710 |
| Coal | Biofuel | 4.763 | 7.653 | -4.944 | 1.623 |
| Gas | Oil | 5.042 | 6.632 | 6.277 | 8.441 |
| Gas | Nuclear | 5.042 | 6.632 | -7.032 | -4.904 |
| Gas | Hydro | 5.042 | 6.632 | -7.032 | -4.904 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*