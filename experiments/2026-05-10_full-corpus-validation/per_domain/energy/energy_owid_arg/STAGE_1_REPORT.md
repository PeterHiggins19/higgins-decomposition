# Stage 1 Report (pure CoDa) — energy_owid_arg

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ARG (ARG), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ARG

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `abd7d4587962b8e5147708bec38de0a212c6f7d460a8e54949180d4db7dd74d5`

## Input

- Source CSV: `owid_energy_ARG.csv`
- Source SHA-256: `7df2f8bda759e86b...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `7545fa22a9ce8f6b...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.5501 | 16.1825 | — |
| 1 | 1966 | 0.5422 | 16.1325 | 0.2203 |
| 2 | 1967 | 0.5528 | 16.1588 | 0.0837 |
| 3 | 1968 | 0.5725 | 16.1936 | 0.1565 |
| 4 | 1969 | 0.5688 | 16.1898 | 0.2074 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.2378 | 4.0975 | 0.5046 |
| 58 | 2023 | 1.2812 | 4.0815 | 0.3861 |
| 59 | 2024 | 1.2988 | 3.9890 | 0.4277 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9902 | 67.5° | no |
| Gas | Oil | +0.9431 | 12.9° | no |
| Coal | Gas | +0.9345 | 69.6° | no |
| Gas | Hydro | +0.9203 | 34.0° | no |
| Oil | Hydro | +0.7892 | 33.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Wind | -0.7629 | 48.0° | no |
| Hydro | Solar | -0.8002 | 29.8° | no |
| Coal | Wind | -0.8026 | 125.1° | no |
| Gas | Biofuel | -0.8063 | 59.3° | no |
| Hydro | Biofuel | -0.8864 | 86.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -1.501 | 4.733 | 2.324 | 6.509 |
| Coal | Oil | -1.501 | 4.733 | 2.027 | 8.065 |
| Coal | Nuclear | -1.501 | 4.733 | -5.724 | 3.403 |
| Coal | Hydro | -1.501 | 4.733 | 0.229 | 4.550 |
| Coal | Solar | -1.501 | 4.733 | -8.775 | -1.530 |
| Coal | Wind | -1.501 | 4.733 | -7.255 | -0.125 |
| Coal | Biofuel | -1.501 | 4.733 | -7.850 | 0.186 |
| Gas | Oil | 2.324 | 6.509 | 2.027 | 8.065 |
| Gas | Nuclear | 2.324 | 6.509 | -5.724 | 3.403 |
| Gas | Hydro | 2.324 | 6.509 | 0.229 | 4.550 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*