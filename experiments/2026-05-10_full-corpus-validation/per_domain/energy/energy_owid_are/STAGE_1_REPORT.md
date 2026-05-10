# Stage 1 Report (pure CoDa) — energy_owid_are

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ARE (ARE), annual TWh. T = 16 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ARE

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `f0a2ca5d4e50fed586c98e9d73c0c08913733bdcda12fe7807ee28e908c77f1e`

## Input

- Source CSV: `owid_energy_ARE.csv`
- Source SHA-256: `cea2aed7af3abea6...`
- Records (T): **16**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `4a04b055f4e5e54f...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2009 | 0.6828 | 15.6290 | — |
| 1 | 2010 | 0.7080 | 15.7420 | 1.1315 |
| 2 | 2011 | 0.6992 | 15.6346 | 0.4263 |
| 3 | 2012 | 0.7396 | 15.9056 | 1.0066 |
| 4 | 2013 | 0.7601 | 15.5796 | 1.4478 |
| ... | ... | ... | ... | ... |
| 13 | 2022 | 0.9720 | 15.7339 | 0.5730 |
| 14 | 2023 | 1.0550 | 14.3482 | 4.2561 |
| 15 | 2024 | 1.0694 | 14.1601 | 1.0600 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Biofuel | +1.0000 | 0.0° | YES |
| Gas | Hydro | +0.9992 | 28.4° | no |
| Gas | Biofuel | +0.9992 | 28.4° | no |
| Oil | Hydro | +0.9987 | 27.5° | no |
| Oil | Biofuel | +0.9987 | 27.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Nuclear | -0.9001 | 111.1° | no |
| Gas | Nuclear | -0.9138 | 68.2° | no |
| Nuclear | Hydro | -0.9226 | 71.5° | no |
| Nuclear | Biofuel | -0.9226 | 71.5° | no |
| Oil | Nuclear | -0.9329 | 69.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.051 | 4.633 | 5.201 | 8.690 |
| Coal | Oil | 2.051 | 4.633 | 5.087 | 8.182 |
| Coal | Nuclear | 2.051 | 4.633 | -5.604 | 3.496 |
| Coal | Hydro | 2.051 | 4.633 | -7.860 | -4.651 |
| Coal | Solar | 2.051 | 4.633 | -1.760 | 3.311 |
| Coal | Wind | 2.051 | 4.633 | -7.011 | -2.089 |
| Coal | Biofuel | 2.051 | 4.633 | -7.860 | -4.651 |
| Gas | Oil | 5.201 | 8.690 | 5.087 | 8.182 |
| Gas | Nuclear | 5.201 | 8.690 | -5.604 | 3.496 |
| Gas | Hydro | 5.201 | 8.690 | -7.860 | -4.651 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*