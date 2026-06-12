# Stage 1 Report (pure CoDa) — energy_owid_prt

**Domain:** energy
**Description:** OWID primary-energy consumption composition for PRT (PRT), annual TWh. T = 36 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: PRT

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `0905ad024f099ed8a0b1c60139e66c5afd5141f0b1ebca877771001f76361459`

## Input

- Source CSV: `owid_energy_PRT.csv`
- Source SHA-256: `3a9eeef70132d9a6...`
- Records (T): **36**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `1e3b1e74f9ecbdeb...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1989 | 0.6922 | 15.6907 | — |
| 1 | 1990 | 0.8080 | 16.5056 | 2.5945 |
| 2 | 1991 | 0.7997 | 16.5010 | 0.0563 |
| 3 | 1992 | 0.6696 | 16.1222 | 1.5064 |
| 4 | 1993 | 0.7923 | 16.2830 | 1.0138 |
| ... | ... | ... | ... | ... |
| 33 | 2022 | 1.3061 | 11.5684 | 3.1834 |
| 34 | 2023 | 1.3888 | 11.7480 | 0.8028 |
| 35 | 2024 | 1.4406 | 11.7334 | 0.4196 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9994 | 41.5° | no |
| Nuclear | Hydro | +0.9839 | 47.2° | no |
| Oil | Hydro | +0.9805 | 21.0° | no |
| Coal | Oil | +0.8364 | 86.0° | no |
| Coal | Nuclear | +0.8333 | 77.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Wind | -0.8233 | 169.2° | no |
| Hydro | Wind | -0.8948 | 82.1° | no |
| Coal | Solar | -0.8950 | 220.2° | no |
| Oil | Wind | -0.8960 | 50.9° | no |
| Nuclear | Wind | -0.8968 | 359.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -3.876 | 7.062 | -5.676 | 4.268 |
| Coal | Oil | -3.876 | 7.062 | 3.227 | 8.502 |
| Coal | Nuclear | -3.876 | 7.062 | -9.802 | -4.973 |
| Coal | Hydro | -3.876 | 7.062 | 1.110 | 6.778 |
| Coal | Solar | -3.876 | 7.062 | -5.333 | 1.732 |
| Coal | Wind | -3.876 | 7.062 | -2.597 | 2.509 |
| Coal | Biofuel | -3.876 | 7.062 | -7.629 | 0.363 |
| Gas | Oil | -5.676 | 4.268 | 3.227 | 8.502 |
| Gas | Nuclear | -5.676 | 4.268 | -9.802 | -4.973 |
| Gas | Hydro | -5.676 | 4.268 | 1.110 | 6.778 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*