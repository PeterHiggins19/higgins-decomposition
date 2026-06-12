# Stage 1 Report (pure CoDa) — energy_owid_uzb

**Domain:** energy
**Description:** OWID primary-energy consumption composition for UZB (UZB), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: UZB

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `dd6dfa7046ff9b61312bdbe6fbb13c7878b4e4c671eae725dbe87e7623ef8067`

## Input

- Source CSV: `owid_energy_UZB.csv`
- Source SHA-256: `95976d974447682c...`
- Records (T): **40**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `e23aff585ac38e7d...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 0.8529 | 16.7451 | — |
| 1 | 1986 | 0.8652 | 16.7531 | 0.2069 |
| 2 | 1987 | 0.8691 | 16.7792 | 0.4077 |
| 3 | 1988 | 0.8914 | 16.8180 | 0.0934 |
| 4 | 1989 | 0.8643 | 16.7602 | 0.3026 |
| ... | ... | ... | ... | ... |
| 37 | 2022 | 0.6563 | 15.3336 | 2.6975 |
| 38 | 2023 | 0.7464 | 14.2948 | 3.0672 |
| 39 | 2024 | 0.7786 | 13.7553 | 4.0212 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Gas | Nuclear | +0.9842 | 19.7° | no |
| Gas | Biofuel | +0.9842 | 19.7° | no |
| Nuclear | Hydro | +0.9567 | 24.6° | no |
| Hydro | Biofuel | +0.9567 | 24.6° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Solar | -0.8800 | 54.7° | no |
| Oil | Solar | -0.8818 | 70.9° | no |
| Nuclear | Solar | -0.9294 | 344.4° | no |
| Solar | Biofuel | -0.9294 | 56.9° | no |
| Hydro | Solar | -0.9418 | 89.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 3.218 | 4.814 | 5.623 | 8.030 |
| Coal | Oil | 3.218 | 4.814 | 3.519 | 6.659 |
| Coal | Nuclear | 3.218 | 4.814 | -7.953 | -5.638 |
| Coal | Hydro | 3.218 | 4.814 | 2.316 | 4.919 |
| Coal | Solar | 3.218 | 4.814 | -5.883 | 1.673 |
| Coal | Wind | 3.218 | 4.814 | -6.694 | -0.444 |
| Coal | Biofuel | 3.218 | 4.814 | -7.953 | -5.638 |
| Gas | Oil | 5.623 | 8.030 | 3.519 | 6.659 |
| Gas | Nuclear | 5.623 | 8.030 | -7.953 | -5.638 |
| Gas | Hydro | 5.623 | 8.030 | 2.316 | 4.919 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*