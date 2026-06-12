# Stage 1 Report (pure CoDa) — energy_owid_bra

**Domain:** energy
**Description:** OWID primary-energy consumption composition for BRA (BRA), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: BRA

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `c437249c7fb82ba2791c338a4fdfdea6c3109d899246e9e2156010fe7dd10613`

## Input

- Source CSV: `owid_energy_BRA.csv`
- Source SHA-256: `46a5596ef1fe4f51...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `2f147494107eec71...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.8317 | 16.4048 | — |
| 1 | 1966 | 0.8320 | 16.4092 | 0.0651 |
| 2 | 1967 | 0.8350 | 16.4242 | 0.0829 |
| 3 | 1968 | 0.7886 | 16.3482 | 0.1741 |
| 4 | 1969 | 0.7864 | 16.3450 | 0.0454 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.5704 | 3.2454 | 0.6699 |
| 58 | 2023 | 1.6035 | 3.1011 | 0.4935 |
| 59 | 2024 | 1.6402 | 2.9802 | 0.3397 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Hydro | +0.9963 | 64.7° | no |
| Oil | Hydro | +0.9907 | 6.3° | YES |
| Coal | Oil | +0.9896 | 56.3° | no |
| Gas | Hydro | +0.6280 | 27.7° | no |
| Coal | Gas | +0.6046 | 157.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | -0.7137 | 61.0° | no |
| Oil | Wind | -0.7258 | 59.2° | no |
| Coal | Wind | -0.7803 | 157.2° | no |
| Hydro | Wind | -0.7889 | 60.1° | no |
| Gas | Solar | -0.7965 | 13.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -0.618 | 5.643 | 0.135 | 2.496 |
| Coal | Oil | -0.618 | 5.643 | 1.650 | 7.885 |
| Coal | Nuclear | -0.618 | 5.643 | -7.134 | 0.811 |
| Coal | Hydro | -0.618 | 5.643 | 1.302 | 6.899 |
| Coal | Solar | -0.618 | 5.643 | -9.510 | -0.455 |
| Coal | Wind | -0.618 | 5.643 | -8.329 | -0.035 |
| Coal | Biofuel | -0.618 | 5.643 | -5.602 | 3.200 |
| Gas | Oil | 0.135 | 2.496 | 1.650 | 7.885 |
| Gas | Nuclear | 0.135 | 2.496 | -7.134 | 0.811 |
| Gas | Hydro | 0.135 | 2.496 | 1.302 | 6.899 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*