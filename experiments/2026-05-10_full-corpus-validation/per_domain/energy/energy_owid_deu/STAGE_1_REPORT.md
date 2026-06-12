# Stage 1 Report (pure CoDa) — energy_owid_deu

**Domain:** energy
**Description:** OWID primary-energy consumption composition for DEU (DEU), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: DEU

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `a7808658c4773b3dd5d4fdac4fbd15f51560c56368905d4f7f95c2730f642892`

## Input

- Source CSV: `owid_energy_DEU.csv`
- Source SHA-256: `1e9bea92de7afe6a...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `08ebf6d1abc43001...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.7703 | 15.2551 | — |
| 1 | 1966 | 0.8046 | 15.2595 | 0.7521 |
| 2 | 1967 | 0.8277 | 15.2854 | 1.4287 |
| 3 | 1968 | 0.8621 | 15.3775 | 0.4757 |
| 4 | 1969 | 0.8883 | 15.4564 | 0.9789 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.5910 | 3.5823 | 0.7224 |
| 58 | 2023 | 1.5617 | 4.0700 | 1.5054 |
| 59 | 2024 | 1.5329 | 11.0516 | 8.1270 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9957 | 70.8° | no |
| Coal | Oil | +0.9955 | 21.4° | no |
| Coal | Hydro | +0.9950 | 88.2° | no |
| Wind | Biofuel | +0.9452 | 115.2° | no |
| Gas | Oil | +0.9216 | 15.9° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Biofuel | -0.9480 | 50.9° | no |
| Oil | Wind | -0.9483 | 83.3° | no |
| Coal | Biofuel | -0.9491 | 46.9° | no |
| Oil | Biofuel | -0.9494 | 45.2° | no |
| Coal | Wind | -0.9560 | 93.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.836 | 7.144 | 1.228 | 4.679 |
| Coal | Oil | 0.836 | 7.144 | 1.678 | 6.539 |
| Coal | Nuclear | 0.836 | 7.144 | -9.863 | 4.126 |
| Coal | Hydro | 0.836 | 7.144 | -1.650 | 3.418 |
| Coal | Solar | 0.836 | 7.144 | -9.288 | 1.142 |
| Coal | Wind | 0.836 | 7.144 | -7.288 | 1.769 |
| Coal | Biofuel | 0.836 | 7.144 | -7.829 | -0.636 |
| Gas | Oil | 1.228 | 4.679 | 1.678 | 6.539 |
| Gas | Nuclear | 1.228 | 4.679 | -9.863 | 4.126 |
| Gas | Hydro | 1.228 | 4.679 | -1.650 | 3.418 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*