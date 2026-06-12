# Stage 1 Report (pure CoDa) — energy_owid_fin

**Domain:** energy
**Description:** OWID primary-energy consumption composition for FIN (FIN), annual TWh. T = 51 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: FIN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `cbce60fb7524df2d1cd2823650887063d43dfb069356618534554ffd4e161bc1`

## Input

- Source CSV: `owid_energy_FIN.csv`
- Source SHA-256: `9310d4365983f2d4...`
- Records (T): **51**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `3dd0dd0e0c5df5ab...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1974 | 0.9368 | 16.9029 | — |
| 1 | 1975 | 0.9419 | 16.9764 | 0.4909 |
| 2 | 1976 | 0.9360 | 16.9817 | 0.4053 |
| 3 | 1977 | 1.0898 | 16.0876 | 9.6795 |
| 4 | 1978 | 1.1168 | 16.1250 | 0.3999 |
| ... | ... | ... | ... | ... |
| 48 | 2022 | 1.6866 | 3.9253 | 0.8297 |
| 49 | 2023 | 1.6971 | 3.5574 | 0.6994 |
| 50 | 2024 | 1.7248 | 3.1554 | 0.6499 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9954 | 21.4° | no |
| Coal | Oil | +0.9804 | 45.5° | no |
| Coal | Hydro | +0.9715 | 69.3° | no |
| Coal | Gas | +0.9642 | 139.8° | no |
| Gas | Oil | +0.9148 | 59.8° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Biofuel | -0.8280 | 71.9° | no |
| Gas | Biofuel | -0.8601 | 82.7° | no |
| Hydro | Wind | -0.9062 | 125.1° | no |
| Coal | Wind | -0.9062 | 155.4° | no |
| Oil | Wind | -0.9102 | 86.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.076 | 6.039 | -0.578 | 4.606 |
| Coal | Oil | -0.076 | 6.039 | 1.346 | 7.489 |
| Coal | Nuclear | -0.076 | 6.039 | -5.960 | 4.756 |
| Coal | Hydro | -0.076 | 6.039 | 0.436 | 6.138 |
| Coal | Solar | -0.076 | 6.039 | -7.515 | -1.977 |
| Coal | Wind | -0.076 | 6.039 | -7.724 | 0.803 |
| Coal | Biofuel | -0.076 | 6.039 | -8.857 | -0.665 |
| Gas | Oil | -0.578 | 4.606 | 1.346 | 7.489 |
| Gas | Nuclear | -0.578 | 4.606 | -5.960 | 4.756 |
| Gas | Hydro | -0.578 | 4.606 | 0.436 | 6.138 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*