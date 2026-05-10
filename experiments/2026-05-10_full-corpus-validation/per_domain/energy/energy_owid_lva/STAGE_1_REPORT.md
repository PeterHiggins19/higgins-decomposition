# Stage 1 Report (pure CoDa) — energy_owid_lva

**Domain:** energy
**Description:** OWID primary-energy consumption composition for LVA (LVA), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: LVA

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:10Z
**cnt_content_sha256:** `b10481f735240409c5681b32949ad7490b1723cd36b959928ac486ee05adb34e`

## Input

- Source CSV: `owid_energy_LVA.csv`
- Source SHA-256: `85e18dbbbe1a5718...`
- Records (T): **40**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `cf8cc521788f11ea...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 1.0072 | 17.1009 | — |
| 1 | 1986 | 1.1008 | 17.2299 | 0.3248 |
| 2 | 1987 | 1.1795 | 17.3320 | 0.3313 |
| 3 | 1988 | 1.1865 | 17.3151 | 0.2170 |
| 4 | 1989 | 1.1845 | 17.3261 | 0.2735 |
| ... | ... | ... | ... | ... |
| 37 | 2022 | 1.1210 | 10.9730 | 2.6273 |
| 38 | 2023 | 1.1925 | 11.0154 | 1.1424 |
| 39 | 2024 | 1.2272 | 11.0604 | 0.5990 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9963 | 28.4° | no |
| Coal | Nuclear | +0.9851 | 48.8° | no |
| Gas | Nuclear | +0.9834 | 29.2° | no |
| Coal | Oil | +0.9815 | 53.8° | no |
| Coal | Gas | +0.9709 | 62.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Wind | -0.8555 | 51.8° | no |
| Gas | Biofuel | -0.8907 | 60.8° | no |
| Oil | Biofuel | -0.9095 | 58.5° | no |
| Nuclear | Biofuel | -0.9151 | 357.3° | no |
| Hydro | Biofuel | -0.9282 | 67.1° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -1.056 | 5.560 | 2.969 | 6.552 |
| Coal | Oil | -1.056 | 5.560 | 3.830 | 7.355 |
| Coal | Nuclear | -1.056 | 5.560 | -9.321 | -6.015 |
| Coal | Hydro | -1.056 | 5.560 | 2.925 | 6.064 |
| Coal | Solar | -1.056 | 5.560 | -8.083 | 0.893 |
| Coal | Wind | -1.056 | 5.560 | -6.125 | 1.086 |
| Coal | Biofuel | -1.056 | 5.560 | -7.006 | 0.678 |
| Gas | Oil | 2.969 | 6.552 | 3.830 | 7.355 |
| Gas | Nuclear | 2.969 | 6.552 | -9.321 | -6.015 |
| Gas | Hydro | 2.969 | 6.552 | 2.925 | 6.064 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*