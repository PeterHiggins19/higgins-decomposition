# Stage 1 Report (pure CoDa) — energy_owid_blr

**Domain:** energy
**Description:** OWID primary-energy consumption composition for BLR (BLR), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: BLR

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `d63f9e5dc65380bdbd75e4ff07644602da22f6c7bae1350d51dad6681053fbda`

## Input

- Source CSV: `owid_energy_BLR.csv`
- Source SHA-256: `64403c917668ab64...`
- Records (T): **40**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `ce61074b034bb10a...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 0.7340 | 16.1534 | — |
| 1 | 1986 | 0.6978 | 16.1087 | 0.1595 |
| 2 | 1987 | 0.7194 | 16.1265 | 0.1181 |
| 3 | 1988 | 0.7619 | 16.1834 | 0.1450 |
| 4 | 1989 | 0.7856 | 16.2073 | 0.0906 |
| ... | ... | ... | ... | ... |
| 37 | 2022 | 0.9452 | 11.1048 | 0.3023 |
| 38 | 2023 | 1.0667 | 11.3163 | 0.9886 |
| 39 | 2024 | 1.1005 | 11.3779 | 0.3067 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9923 | 13.3° | no |
| Gas | Oil | +0.9041 | 9.8° | YES |
| Coal | Gas | +0.8996 | 19.8° | no |
| Solar | Wind | +0.7662 | 26.0° | no |
| Gas | Hydro | +0.6730 | 17.4° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Solar | -0.7797 | 35.9° | no |
| Gas | Solar | -0.8503 | 35.2° | no |
| Gas | Wind | -0.8686 | 25.7° | no |
| Oil | Wind | -0.9440 | 22.9° | no |
| Coal | Wind | -0.9445 | 28.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.685 | 5.815 | 4.456 | 8.043 |
| Coal | Oil | 1.685 | 5.815 | 3.861 | 8.349 |
| Coal | Nuclear | 1.685 | 5.815 | -8.193 | 2.979 |
| Coal | Hydro | 1.685 | 5.815 | -1.088 | 0.520 |
| Coal | Solar | 1.685 | 5.815 | -6.692 | -0.921 |
| Coal | Wind | 1.685 | 5.815 | -5.331 | -0.997 |
| Coal | Biofuel | 1.685 | 5.815 | -8.751 | 0.730 |
| Gas | Oil | 4.456 | 8.043 | 3.861 | 8.349 |
| Gas | Nuclear | 4.456 | 8.043 | -8.193 | 2.979 |
| Gas | Hydro | 4.456 | 8.043 | -1.088 | 0.520 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*