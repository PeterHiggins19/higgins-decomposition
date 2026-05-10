# Stage 1 Report (pure CoDa) — energy_owid_pak

**Domain:** energy
**Description:** OWID primary-energy consumption composition for PAK (PAK), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: PAK

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:11Z
**cnt_content_sha256:** `5bb6563fec6d311ac001a0e29dee4b176726fb7bc66fa3afd0f2ae6f619fba79`

## Input

- Source CSV: `owid_energy_PAK.csv`
- Source SHA-256: `e345ce339a100a69...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `61154553a06cb030...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.1513 | 17.2818 | — |
| 1 | 1966 | 1.1377 | 17.2766 | 0.2105 |
| 2 | 1967 | 1.1308 | 17.2681 | 0.1663 |
| 3 | 1968 | 1.1316 | 17.2630 | 0.0654 |
| 4 | 1969 | 1.1594 | 17.2939 | 0.2460 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.4589 | 11.2330 | 0.5379 |
| 58 | 2023 | 1.4708 | 11.1606 | 0.5165 |
| 59 | 2024 | 1.4658 | 11.1354 | 0.3627 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Biofuel | +0.9945 | 33.8° | no |
| Gas | Biofuel | +0.9792 | 28.2° | no |
| Hydro | Biofuel | +0.9679 | 30.4° | no |
| Gas | Oil | +0.9587 | 9.8° | YES |
| Gas | Hydro | +0.9583 | 16.7° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Solar | Biofuel | -0.8722 | 37.6° | no |
| Gas | Solar | -0.8939 | 32.0° | no |
| Hydro | Wind | -0.9070 | 57.3° | no |
| Gas | Wind | -0.9239 | 52.3° | no |
| Hydro | Solar | -0.9333 | 25.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.097 | 6.094 | 3.269 | 6.487 |
| Coal | Oil | 2.097 | 6.094 | 2.755 | 7.163 |
| Coal | Nuclear | 2.097 | 6.094 | -6.095 | 2.396 |
| Coal | Hydro | 2.097 | 6.094 | 1.796 | 5.292 |
| Coal | Solar | 2.097 | 6.094 | -7.265 | -1.250 |
| Coal | Wind | 2.097 | 6.094 | -7.834 | -0.227 |
| Coal | Biofuel | 2.097 | 6.094 | -9.683 | -6.075 |
| Gas | Oil | 3.269 | 6.487 | 2.755 | 7.163 |
| Gas | Nuclear | 3.269 | 6.487 | -6.095 | 2.396 |
| Gas | Hydro | 3.269 | 6.487 | 1.796 | 5.292 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*