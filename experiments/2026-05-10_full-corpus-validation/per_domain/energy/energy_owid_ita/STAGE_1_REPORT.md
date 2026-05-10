# Stage 1 Report (pure CoDa) — energy_owid_ita

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ITA (ITA), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ITA

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `2f454c21fa67145929d8d8520981d619fd5595c0f2010dcd11dfe7183e267640`

## Input

- Source CSV: `owid_energy_ITA.csv`
- Source SHA-256: `5e15060b74246aac...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `e24027ab7b47cacb...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.0283 | 15.9866 | — |
| 1 | 1966 | 1.0098 | 15.9694 | 0.0705 |
| 2 | 1967 | 0.9784 | 15.9139 | 0.2797 |
| 3 | 1968 | 0.9484 | 15.8614 | 0.2946 |
| 4 | 1969 | 0.9092 | 15.7864 | 0.4685 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.2964 | 10.8939 | 0.5774 |
| 58 | 2023 | 1.3211 | 10.9101 | 0.6230 |
| 59 | 2024 | 1.3183 | 10.9375 | 0.7424 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9861 | 20.3° | no |
| Coal | Oil | +0.9744 | 34.7° | no |
| Coal | Hydro | +0.9625 | 51.1° | no |
| Gas | Oil | +0.8844 | 12.7° | no |
| Solar | Wind | +0.8742 | 359.0° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Solar | -0.8857 | 145.7° | no |
| Coal | Biofuel | -0.9073 | 72.6° | no |
| Nuclear | Wind | -0.9304 | 359.7° | no |
| Oil | Biofuel | -0.9376 | 47.3° | no |
| Hydro | Biofuel | -0.9477 | 56.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.100 | 5.402 | 3.024 | 6.308 |
| Coal | Oil | 0.100 | 5.402 | 3.148 | 7.316 |
| Coal | Nuclear | 0.100 | 5.402 | -9.719 | 2.365 |
| Coal | Hydro | 0.100 | 5.402 | 0.956 | 5.052 |
| Coal | Solar | 0.100 | 5.402 | -7.225 | 1.251 |
| Coal | Wind | 0.100 | 5.402 | -7.225 | 0.782 |
| Coal | Biofuel | 0.100 | 5.402 | -7.366 | -0.307 |
| Gas | Oil | 3.024 | 6.308 | 3.148 | 7.316 |
| Gas | Nuclear | 3.024 | 6.308 | -9.719 | 2.365 |
| Gas | Hydro | 3.024 | 6.308 | 0.956 | 5.052 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*