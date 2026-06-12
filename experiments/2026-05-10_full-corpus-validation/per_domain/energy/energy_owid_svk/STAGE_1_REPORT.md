# Stage 1 Report (pure CoDa) — energy_owid_svk

**Domain:** energy
**Description:** OWID primary-energy consumption composition for SVK (SVK), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: SVK

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `f09156fce6114ec33c9bee5ce39643d5607c3043b267bebba5cacf4fe89c9505`

## Input

- Source CSV: `owid_energy_SVK.csv`
- Source SHA-256: `85a8a1f198842ef8...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `bb6a6f1bef537578...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.8879 | 16.8244 | — |
| 1 | 1966 | 0.8990 | 16.8318 | 0.1243 |
| 2 | 1967 | 0.9188 | 16.8487 | 0.2600 |
| 3 | 1968 | 0.9879 | 16.9881 | 0.7144 |
| 4 | 1969 | 0.9607 | 16.9086 | 0.2810 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.5839 | 7.6529 | 0.2805 |
| 58 | 2023 | 1.5964 | 7.7068 | 0.2816 |
| 59 | 2024 | 1.5929 | 7.6489 | 0.2627 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9924 | 16.4° | no |
| Coal | Hydro | +0.9497 | 22.4° | no |
| Oil | Hydro | +0.9333 | 26.0° | no |
| Coal | Gas | +0.9084 | 25.9° | no |
| Gas | Oil | +0.8980 | 16.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Biofuel | -0.7599 | 53.5° | no |
| Gas | Solar | -0.7929 | 41.2° | no |
| Oil | Biofuel | -0.8396 | 47.6° | no |
| Coal | Biofuel | -0.8398 | 46.5° | no |
| Gas | Biofuel | -0.8873 | 48.6° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.395 | 7.520 | 2.039 | 5.560 |
| Coal | Oil | 1.395 | 7.520 | 1.926 | 6.790 |
| Coal | Nuclear | 1.395 | 7.520 | -5.982 | 4.715 |
| Coal | Hydro | 1.395 | 7.520 | 0.451 | 5.089 |
| Coal | Solar | 1.395 | 7.520 | -9.176 | -1.176 |
| Coal | Wind | 1.395 | 7.520 | -8.464 | -4.229 |
| Coal | Biofuel | 1.395 | 7.520 | -7.550 | -0.623 |
| Gas | Oil | 2.039 | 5.560 | 1.926 | 6.790 |
| Gas | Nuclear | 2.039 | 5.560 | -5.982 | 4.715 |
| Gas | Hydro | 2.039 | 5.560 | 0.451 | 5.089 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*