# Stage 1 Report (pure CoDa) — energy_owid_cyp

**Domain:** energy
**Description:** OWID primary-energy consumption composition for CYP (CYP), annual TWh. T = 21 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: CYP

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `03118abb5c505e437be79f5e179804ebea919a8d2f4d7f4dc49ad6b1defa1d1e`

## Input

- Source CSV: `owid_energy_CYP.csv`
- Source SHA-256: `d6224a1a04fd9cba...`
- Records (T): **21**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `71285f7c2e926395...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2004 | 0.0844 | 13.8933 | — |
| 1 | 2005 | 0.0772 | 13.8398 | 0.2809 |
| 2 | 2006 | 0.0581 | 13.7203 | 0.6820 |
| 3 | 2007 | 0.0562 | 13.0982 | 5.2927 |
| 4 | 2008 | 0.0748 | 13.5069 | 2.5968 |
| ... | ... | ... | ... | ... |
| 18 | 2022 | 0.3831 | 14.9094 | 0.4109 |
| 19 | 2023 | 0.4198 | 14.9327 | 0.3402 |
| 20 | 2024 | 0.4371 | 14.9080 | 0.6389 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Nuclear | +1.0000 | 0.0° | YES |
| Gas | Hydro | +1.0000 | 0.0° | YES |
| Nuclear | Hydro | +1.0000 | 0.0° | YES |
| Gas | Oil | +0.9997 | 22.1° | no |
| Oil | Nuclear | +0.9997 | 22.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Wind | -0.7983 | 130.7° | no |
| Gas | Solar | -0.9015 | 355.9° | no |
| Nuclear | Solar | -0.9015 | 355.9° | no |
| Hydro | Solar | -0.9015 | 355.9° | no |
| Oil | Solar | -0.9062 | 35.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -1.079 | 5.898 | -6.611 | -3.809 |
| Coal | Oil | -1.079 | 5.898 | 7.101 | 9.993 |
| Coal | Nuclear | -1.079 | 5.898 | -6.611 | -3.809 |
| Coal | Hydro | -1.079 | 5.898 | -6.611 | -3.809 |
| Coal | Solar | -1.079 | 5.898 | -0.259 | 4.748 |
| Coal | Wind | -1.079 | 5.898 | -1.710 | 4.276 |
| Coal | Biofuel | -1.079 | 5.898 | -3.844 | 3.567 |
| Gas | Oil | -6.611 | -3.809 | 7.101 | 9.993 |
| Gas | Nuclear | -6.611 | -3.809 | -6.611 | -3.809 |
| Gas | Hydro | -6.611 | -3.809 | -6.611 | -3.809 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*