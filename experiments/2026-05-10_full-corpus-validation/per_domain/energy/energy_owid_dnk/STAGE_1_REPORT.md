# Stage 1 Report (pure CoDa) — energy_owid_dnk

**Domain:** energy
**Description:** OWID primary-energy consumption composition for DNK (DNK), annual TWh. T = 47 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: DNK

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `05c343b7738640f0bd4982c652b9f0b14da4709dd10dcba734125a038889bcaa`

## Input

- Source CSV: `owid_energy_DNK.csv`
- Source SHA-256: `871efe3a5a6936a5...`
- Records (T): **47**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `0907ab86c30fc02c...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1978 | 0.4674 | 14.9620 | — |
| 1 | 1979 | 0.5170 | 15.0124 | 0.6496 |
| 2 | 1980 | 0.6213 | 15.1494 | 0.6402 |
| 3 | 1981 | 0.5916 | 15.1336 | 0.2125 |
| 4 | 1982 | 0.6499 | 15.2064 | 0.6339 |
| ... | ... | ... | ... | ... |
| 44 | 2022 | 1.3071 | 11.6919 | 0.6523 |
| 45 | 2023 | 1.2705 | 11.5854 | 0.6756 |
| 46 | 2024 | 1.2476 | 11.5728 | 0.4110 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9981 | 42.0° | no |
| Nuclear | Hydro | +0.9943 | 356.6° | no |
| Oil | Hydro | +0.9931 | 54.7° | no |
| Coal | Nuclear | +0.9747 | 53.4° | no |
| Coal | Hydro | +0.9683 | 83.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Biofuel | -0.7611 | 335.1° | no |
| Nuclear | Solar | -0.7775 | 359.0° | no |
| Hydro | Solar | -0.7788 | 357.5° | no |
| Coal | Biofuel | -0.8106 | 80.8° | no |
| Coal | Solar | -0.8765 | 104.4° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.131 | 8.034 | -4.717 | 5.327 |
| Coal | Oil | 1.131 | 8.034 | 3.859 | 9.248 |
| Coal | Nuclear | 1.131 | 8.034 | -9.247 | -4.373 |
| Coal | Hydro | 1.131 | 8.034 | -3.920 | 1.518 |
| Coal | Solar | 1.131 | 8.034 | -6.642 | 1.713 |
| Coal | Wind | 1.131 | 8.034 | -0.826 | 4.065 |
| Coal | Biofuel | 1.131 | 8.034 | -7.226 | 0.808 |
| Gas | Oil | -4.717 | 5.327 | 3.859 | 9.248 |
| Gas | Nuclear | -4.717 | 5.327 | -9.247 | -4.373 |
| Gas | Hydro | -4.717 | 5.327 | -3.920 | 1.518 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*