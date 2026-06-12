# Stage 1 Report (pure CoDa) — energy_owid_mkd

**Domain:** energy
**Description:** OWID primary-energy consumption composition for MKD (MKD), annual TWh. T = 27 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: MKD

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `07d3f44f3ba3bd9c7c6b3a79da009c7cadd9ac0b07364f0bdede1242dfe81d90`

## Input

- Source CSV: `owid_energy_MKD.csv`
- Source SHA-256: `6212bcc07fc1d792...`
- Records (T): **27**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `4cca332b56f7724b...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1998 | 0.9281 | 16.6425 | — |
| 1 | 1999 | 1.0086 | 16.8675 | 0.6667 |
| 2 | 2000 | 1.0247 | 16.9282 | 0.5230 |
| 3 | 2001 | 0.9384 | 16.8533 | 0.6969 |
| 4 | 2002 | 0.9961 | 16.9529 | 0.2695 |
| ... | ... | ... | ... | ... |
| 24 | 2022 | 1.2651 | 12.0429 | 1.1010 |
| 25 | 2023 | 1.3761 | 12.1385 | 1.1280 |
| 26 | 2024 | 1.3501 | 12.0867 | 0.2758 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9987 | 27.4° | no |
| Coal | Nuclear | +0.9973 | 32.6° | no |
| Coal | Oil | +0.9935 | 7.6° | YES |
| Nuclear | Hydro | +0.9795 | 29.3° | no |
| Oil | Hydro | +0.9764 | 9.7° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Wind | -0.8859 | 63.4° | no |
| Hydro | Solar | -0.9247 | 79.4° | no |
| Oil | Solar | -0.9355 | 64.2° | no |
| Nuclear | Solar | -0.9375 | 356.8° | no |
| Coal | Solar | -0.9383 | 64.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 3.315 | 7.510 | 1.942 | 4.365 |
| Coal | Oil | 3.315 | 7.510 | 3.870 | 6.947 |
| Coal | Nuclear | 3.315 | 7.510 | -9.120 | -5.747 |
| Coal | Hydro | 3.315 | 7.510 | 2.532 | 5.837 |
| Coal | Solar | 3.315 | 7.510 | -6.771 | 1.104 |
| Coal | Wind | 3.315 | 7.510 | -7.619 | 0.617 |
| Coal | Biofuel | 3.315 | 7.510 | -5.966 | -0.208 |
| Gas | Oil | 1.942 | 4.365 | 3.870 | 6.947 |
| Gas | Nuclear | 1.942 | 4.365 | -9.120 | -5.747 |
| Gas | Hydro | 1.942 | 4.365 | 2.532 | 5.837 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*