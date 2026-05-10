# Stage 1 Report (pure CoDa) — energy_owid_bel

**Domain:** energy
**Description:** OWID primary-energy consumption composition for BEL (BEL), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: BEL

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `6c2d9abc29777d41b7e43e6e36dce93ddeb9d7c299d47fc0035983b3ee016fd6`

## Input

- Source CSV: `owid_energy_BEL.csv`
- Source SHA-256: `f72a8f9a85bcde7b...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `bda2e23e825e7115...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.7136 | 15.6209 | — |
| 1 | 1966 | 0.7268 | 14.8633 | 3.4408 |
| 2 | 1967 | 0.7653 | 14.9123 | 2.7095 |
| 3 | 1968 | 0.8060 | 15.0807 | 0.9564 |
| 4 | 1969 | 0.8519 | 15.2778 | 1.2702 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.4127 | 5.1268 | 0.5014 |
| 58 | 2023 | 1.4180 | 4.7241 | 0.5706 |
| 59 | 2024 | 1.4082 | 4.5087 | 0.3335 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9920 | 47.2° | no |
| Coal | Hydro | +0.9864 | 107.5° | no |
| Oil | Hydro | +0.9806 | 73.8° | no |
| Solar | Biofuel | +0.9461 | 42.8° | no |
| Gas | Oil | +0.8234 | 23.9° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Biofuel | -0.8613 | 37.2° | no |
| Hydro | Wind | -0.8618 | 358.7° | no |
| Oil | Wind | -0.8684 | 56.0° | no |
| Coal | Wind | -0.8890 | 187.7° | no |
| Gas | Solar | -0.8937 | 52.8° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.068 | 8.046 | 1.466 | 6.047 |
| Coal | Oil | -0.068 | 8.046 | 2.369 | 7.878 |
| Coal | Nuclear | -0.068 | 8.046 | -5.501 | 5.099 |
| Coal | Hydro | -0.068 | 8.046 | -3.772 | 2.359 |
| Coal | Solar | -0.068 | 8.046 | -7.700 | -0.379 |
| Coal | Wind | -0.068 | 8.046 | -7.106 | 0.236 |
| Coal | Biofuel | -0.068 | 8.046 | -8.575 | -1.211 |
| Gas | Oil | 1.466 | 6.047 | 2.369 | 7.878 |
| Gas | Nuclear | 1.466 | 6.047 | -5.501 | 5.099 |
| Gas | Hydro | 1.466 | 6.047 | -3.772 | 2.359 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*