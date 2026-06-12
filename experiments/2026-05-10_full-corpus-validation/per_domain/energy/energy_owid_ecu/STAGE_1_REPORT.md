# Stage 1 Report (pure CoDa) — energy_owid_ecu

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ECU (ECU), annual TWh. T = 35 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ECU

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `bdb593a2dca71ca51bd5d57b96c6b75d0ddead49480d592d854bd53ee4128afa`

## Input

- Source CSV: `owid_energy_ECU.csv`
- Source SHA-256: `cdbb25ceb21e4847...`
- Records (T): **35**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `e921e43f0413fb91...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1990 | 0.5986 | 15.9504 | — |
| 1 | 1991 | 0.5887 | 15.9100 | 0.5685 |
| 2 | 1992 | 0.5855 | 15.9338 | 0.2972 |
| 3 | 1993 | 0.6290 | 16.2120 | 1.6960 |
| 4 | 1994 | 0.6185 | 15.9814 | 1.4344 |
| ... | ... | ... | ... | ... |
| 32 | 2022 | 0.7392 | 11.2005 | 0.4137 |
| 33 | 2023 | 0.7198 | 11.1159 | 1.5650 |
| 34 | 2024 | 0.7075 | 11.2726 | 1.1133 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9994 | 27.2° | no |
| Nuclear | Hydro | +0.9894 | 28.0° | no |
| Oil | Hydro | +0.9842 | 5.5° | YES |
| Gas | Oil | +0.9766 | 13.8° | no |
| Gas | Nuclear | +0.9750 | 36.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Biofuel | -0.9187 | 35.4° | no |
| Nuclear | Biofuel | -0.9204 | 40.0° | no |
| Oil | Wind | -0.9324 | 34.0° | no |
| Nuclear | Wind | -0.9360 | 44.3° | no |
| Hydro | Wind | -0.9394 | 39.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -2.618 | 3.442 | 1.979 | 5.808 |
| Coal | Oil | -2.618 | 3.442 | 5.377 | 8.764 |
| Coal | Nuclear | -2.618 | 3.442 | -7.998 | -4.808 |
| Coal | Hydro | -2.618 | 3.442 | 4.261 | 7.278 |
| Coal | Solar | -2.618 | 3.442 | -6.511 | -1.556 |
| Coal | Wind | -2.618 | 3.442 | -5.593 | -0.097 |
| Coal | Biofuel | -2.618 | 3.442 | -5.976 | -0.682 |
| Gas | Oil | 1.979 | 5.808 | 5.377 | 8.764 |
| Gas | Nuclear | 1.979 | 5.808 | -7.998 | -4.808 |
| Gas | Hydro | 1.979 | 5.808 | 4.261 | 7.278 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*