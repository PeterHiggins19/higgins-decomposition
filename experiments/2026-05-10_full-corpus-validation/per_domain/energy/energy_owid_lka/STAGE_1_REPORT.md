# Stage 1 Report (pure CoDa) — energy_owid_lka

**Domain:** energy
**Description:** OWID primary-energy consumption composition for LKA (LKA), annual TWh. T = 25 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: LKA

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `5f19fa113c8571855c3ada394974269a3366c7b65b9ead9577203780ddb7e9f2`

## Input

- Source CSV: `owid_energy_LKA.csv`
- Source SHA-256: `694a6c9754fe130b...`
- Records (T): **25**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `a28be6dfe8471f23...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2000 | 0.4555 | 14.2337 | — |
| 1 | 2001 | 0.4541 | 14.2788 | 1.5134 |
| 2 | 2002 | 0.4231 | 14.2856 | 4.4581 |
| 3 | 2003 | 0.5183 | 14.6833 | 1.5732 |
| 4 | 2004 | 0.4514 | 14.3484 | 1.3292 |
| ... | ... | ... | ... | ... |
| 22 | 2022 | 1.1363 | 16.0799 | 0.3931 |
| 23 | 2023 | 1.0829 | 16.0558 | 0.2885 |
| 24 | 2024 | 1.1411 | 16.1238 | 0.3294 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Nuclear | +1.0000 | 0.0° | YES |
| Gas | Biofuel | +1.0000 | 0.0° | YES |
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Gas | Oil | +0.9978 | 22.3° | no |
| Oil | Nuclear | +0.9978 | 22.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Biofuel | -0.8532 | 58.1° | no |
| Gas | Solar | -0.8625 | 358.3° | no |
| Nuclear | Solar | -0.8625 | 358.3° | no |
| Solar | Biofuel | -0.8625 | 46.2° | no |
| Oil | Solar | -0.8763 | 42.2° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -1.725 | 5.256 | -7.260 | -4.727 |
| Coal | Oil | -1.725 | 5.256 | 6.031 | 8.915 |
| Coal | Nuclear | -1.725 | 5.256 | -7.260 | -4.727 |
| Coal | Hydro | -1.725 | 5.256 | 4.646 | 7.310 |
| Coal | Solar | -1.725 | 5.256 | -1.665 | 3.705 |
| Coal | Wind | -1.725 | 5.256 | -1.045 | 2.651 |
| Coal | Biofuel | -1.725 | 5.256 | -7.260 | -4.727 |
| Gas | Oil | -7.260 | -4.727 | 6.031 | 8.915 |
| Gas | Nuclear | -7.260 | -4.727 | -7.260 | -4.727 |
| Gas | Hydro | -7.260 | -4.727 | 4.646 | 7.310 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*