# Stage 1 Report (pure CoDa) — energy_owid_bgr

**Domain:** energy
**Description:** OWID primary-energy consumption composition for BGR (BGR), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: BGR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `0179b1c4a58634a6dc71da46b199d48ca405e676d7030dbfaa134a30f24bf48c`

## Input

- Source CSV: `owid_energy_BGR.csv`
- Source SHA-256: `40047c9670275562...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `290290510f558cb2...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.8502 | 16.4558 | — |
| 1 | 1966 | 0.8611 | 16.5111 | 0.3313 |
| 2 | 1967 | 0.8962 | 16.6744 | 0.9335 |
| 3 | 1968 | 0.8753 | 16.6135 | 0.6325 |
| 4 | 1969 | 0.8891 | 16.6548 | 0.2771 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.6240 | 3.5798 | 0.5075 |
| 58 | 2023 | 1.6931 | 3.2857 | 0.7633 |
| 59 | 2024 | 1.7165 | 3.2129 | 0.5605 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Hydro | +0.9875 | 73.2° | no |
| Coal | Oil | +0.9861 | 25.0° | no |
| Oil | Hydro | +0.9754 | 60.0° | no |
| Solar | Biofuel | +0.9619 | 60.2° | no |
| Wind | Biofuel | +0.8732 | 31.7° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Wind | -0.7983 | 37.5° | no |
| Oil | Wind | -0.8155 | 32.2° | no |
| Gas | Wind | -0.9225 | 39.2° | no |
| Gas | Solar | -0.9308 | 68.0° | no |
| Gas | Biofuel | -0.9558 | 19.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.826 | 7.613 | 0.608 | 4.820 |
| Coal | Oil | 0.826 | 7.613 | 1.285 | 7.528 |
| Coal | Nuclear | 0.826 | 7.613 | -5.801 | 5.015 |
| Coal | Hydro | 0.826 | 7.613 | -0.680 | 5.084 |
| Coal | Solar | 0.826 | 7.613 | -8.356 | -0.046 |
| Coal | Wind | 0.826 | 7.613 | -7.483 | -1.105 |
| Coal | Biofuel | 0.826 | 7.613 | -8.245 | -1.827 |
| Gas | Oil | 0.608 | 4.820 | 1.285 | 7.528 |
| Gas | Nuclear | 0.608 | 4.820 | -5.801 | 5.015 |
| Gas | Hydro | 0.608 | 4.820 | -0.680 | 5.084 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*