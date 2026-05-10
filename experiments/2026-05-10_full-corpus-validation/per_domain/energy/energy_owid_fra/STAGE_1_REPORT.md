# Stage 1 Report (pure CoDa) — energy_owid_fra

**Domain:** energy
**Description:** OWID primary-energy consumption composition for FRA (FRA), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: FRA

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `2bc7d3816e81a6f66e64db07c01f7f2e2f8ec579b8d01875cc3ce894f1eb2d94`

## Input

- Source CSV: `owid_energy_FRA.csv`
- Source SHA-256: `c33d84c7fe6137da...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `188daa009ef61b2f...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.0820 | 15.8467 | — |
| 1 | 1966 | 1.0946 | 15.8841 | 0.4088 |
| 2 | 1967 | 1.0644 | 15.8707 | 0.4062 |
| 3 | 1968 | 1.0793 | 15.9257 | 0.3486 |
| 4 | 1969 | 1.0609 | 15.9176 | 0.1421 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.5579 | 3.3139 | 0.4770 |
| 58 | 2023 | 1.5622 | 3.3184 | 0.4745 |
| 59 | 2024 | 1.5531 | 3.3223 | 0.2795 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9938 | 46.9° | no |
| Coal | Oil | +0.9922 | 80.8° | no |
| Coal | Hydro | +0.9904 | 353.2° | no |
| Gas | Oil | +0.9697 | 14.1° | no |
| Gas | Hydro | +0.9665 | 69.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Biofuel | -0.9113 | 33.9° | no |
| Coal | Wind | -0.9360 | 120.4° | no |
| Oil | Wind | -0.9556 | 51.2° | no |
| Hydro | Wind | -0.9624 | 68.1° | no |
| Gas | Wind | -0.9740 | 51.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -1.177 | 5.932 | 0.691 | 4.229 |
| Coal | Oil | -1.177 | 5.932 | 1.577 | 6.265 |
| Coal | Nuclear | -1.177 | 5.932 | 0.593 | 5.264 |
| Coal | Hydro | -1.177 | 5.932 | -0.300 | 4.575 |
| Coal | Solar | -1.177 | 5.932 | -7.840 | -1.042 |
| Coal | Wind | -1.177 | 5.932 | -7.913 | -0.203 |
| Coal | Biofuel | -1.177 | 5.932 | -7.508 | -0.995 |
| Gas | Oil | 0.691 | 4.229 | 1.577 | 6.265 |
| Gas | Nuclear | 0.691 | 4.229 | 0.593 | 5.264 |
| Gas | Hydro | 0.691 | 4.229 | -0.300 | 4.575 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*