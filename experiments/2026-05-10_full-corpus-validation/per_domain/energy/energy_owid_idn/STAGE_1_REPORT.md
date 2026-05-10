# Stage 1 Report (pure CoDa) — energy_owid_idn

**Domain:** energy
**Description:** OWID primary-energy consumption composition for IDN (IDN), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: IDN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:09Z
**cnt_content_sha256:** `57a85ad4d3c73ec3b76f77cead29931d15a6efcc02ece770e71e4f6e2a4bb909`

## Input

- Source CSV: `owid_energy_IDN.csv`
- Source SHA-256: `7a7f0504fe489fb6...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `d3fa1fb63a0ba435...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 0.5386 | 16.3265 | — |
| 1 | 1966 | 0.6059 | 16.4700 | 0.3041 |
| 2 | 1967 | 0.6431 | 16.4871 | 0.4221 |
| 3 | 1968 | 0.6458 | 16.4287 | 0.3783 |
| 4 | 1969 | 0.7360 | 16.5733 | 0.5021 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.2272 | 11.9043 | 0.8468 |
| 58 | 2023 | 1.2467 | 11.7535 | 0.5007 |
| 59 | 2024 | 1.2464 | 11.7311 | 0.2044 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9952 | 33.2° | no |
| Oil | Hydro | +0.9236 | 20.1° | no |
| Gas | Nuclear | +0.9142 | 31.8° | no |
| Nuclear | Hydro | +0.9108 | 38.3° | no |
| Gas | Oil | +0.8774 | 9.3° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Solar | -0.7529 | 18.3° | no |
| Gas | Biofuel | -0.8684 | 77.0° | no |
| Hydro | Biofuel | -0.8910 | 114.3° | no |
| Oil | Biofuel | -0.9273 | 65.0° | no |
| Nuclear | Biofuel | -0.9387 | 357.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 3.011 | 6.226 | 3.134 | 6.934 |
| Coal | Oil | 3.011 | 6.226 | 3.755 | 8.192 |
| Coal | Nuclear | 3.011 | 6.226 | -8.884 | -5.505 |
| Coal | Hydro | 3.011 | 6.226 | 1.144 | 5.855 |
| Coal | Solar | 3.011 | 6.226 | -7.115 | -2.211 |
| Coal | Wind | 3.011 | 6.226 | -7.626 | -2.356 |
| Coal | Biofuel | 3.011 | 6.226 | -5.984 | 1.814 |
| Gas | Oil | 3.134 | 6.934 | 3.755 | 8.192 |
| Gas | Nuclear | 3.134 | 6.934 | -8.884 | -5.505 |
| Gas | Hydro | 3.134 | 6.934 | 1.144 | 5.855 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*