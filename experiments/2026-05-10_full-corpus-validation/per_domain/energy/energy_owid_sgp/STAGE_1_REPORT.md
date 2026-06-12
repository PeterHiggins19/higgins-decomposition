# Stage 1 Report (pure CoDa) — energy_owid_sgp

**Domain:** energy
**Description:** OWID primary-energy consumption composition for SGP (SGP), annual TWh. T = 17 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: SGP

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `d5f539d6e189fd386e1278f17f40b00500ea004d9445bee805d60e0e27a3b965`

## Input

- Source CSV: `owid_energy_SGP.csv`
- Source SHA-256: `f9e76c3276c4e537...`
- Records (T): **17**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `458f7523a8b4f5ae...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2008 | 0.3806 | 15.2438 | — |
| 1 | 2009 | 0.3756 | 14.9195 | 1.5601 |
| 2 | 2010 | 0.3383 | 14.7914 | 0.7720 |
| 3 | 2011 | 0.3280 | 14.7195 | 0.4791 |
| 4 | 2012 | 0.3451 | 14.7987 | 1.2739 |
| ... | ... | ... | ... | ... |
| 14 | 2022 | 0.4622 | 15.5324 | 0.5221 |
| 15 | 2023 | 0.4176 | 15.4472 | 0.4096 |
| 16 | 2024 | 0.4156 | 15.4549 | 0.3037 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Hydro | +1.0000 | 0.0° | YES |
| Nuclear | Wind | +1.0000 | 0.0° | YES |
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Hydro | Wind | +1.0000 | 0.0° | YES |
| Hydro | Biofuel | +1.0000 | 0.0° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Solar | -0.9429 | 38.3° | no |
| Nuclear | Solar | -0.9443 | 354.6° | no |
| Hydro | Solar | -0.9443 | 354.6° | no |
| Solar | Wind | -0.9443 | 72.4° | no |
| Solar | Biofuel | -0.9443 | 72.4° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.230 | 4.218 | 6.536 | 8.001 |
| Coal | Oil | 0.230 | 4.218 | 8.442 | 9.934 |
| Coal | Nuclear | 0.230 | 4.218 | -5.207 | -3.747 |
| Coal | Hydro | 0.230 | 4.218 | -5.207 | -3.747 |
| Coal | Solar | 0.230 | 4.218 | -3.617 | 2.804 |
| Coal | Wind | 0.230 | 4.218 | -5.207 | -3.747 |
| Coal | Biofuel | 0.230 | 4.218 | -5.207 | -3.747 |
| Gas | Oil | 6.536 | 8.001 | 8.442 | 9.934 |
| Gas | Nuclear | 6.536 | 8.001 | -5.207 | -3.747 |
| Gas | Hydro | 6.536 | 8.001 | -5.207 | -3.747 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*