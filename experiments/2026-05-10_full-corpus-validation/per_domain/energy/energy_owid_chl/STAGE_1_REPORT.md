# Stage 1 Report (pure CoDa) — energy_owid_chl

**Domain:** energy
**Description:** OWID primary-energy consumption composition for CHL (CHL), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: CHL

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:07Z
**cnt_content_sha256:** `997c58d683424af69b1bad2408b6b6779edb9433bcb364f92d864ecf75171838`

## Input

- Source CSV: `owid_energy_CHL.csv`
- Source SHA-256: `7e6f8f71af8fcc94...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `398bdb333b731789...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.1330 | 17.2702 | — |
| 1 | 1966 | 1.1166 | 17.2550 | 0.0494 |
| 2 | 1967 | 1.0906 | 17.2257 | 0.1323 |
| 3 | 1968 | 1.0322 | 17.1420 | 0.2210 |
| 4 | 1969 | 1.0557 | 17.1868 | 0.2114 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.4942 | 14.4844 | 0.4185 |
| 58 | 2023 | 1.4860 | 14.4794 | 0.5630 |
| 59 | 2024 | 1.4825 | 14.4790 | 0.2075 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Oil | Nuclear | +0.9960 | 25.0° | no |
| Oil | Biofuel | +0.9960 | 25.0° | no |
| Hydro | Biofuel | +0.9852 | 30.1° | no |
| Nuclear | Hydro | +0.9852 | 30.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Solar | -0.9183 | 353.9° | no |
| Hydro | Wind | -0.9282 | 82.3° | no |
| Nuclear | Wind | -0.9420 | 352.0° | no |
| Wind | Biofuel | -0.9420 | 58.2° | no |
| Oil | Wind | -0.9426 | 67.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.416 | 6.085 | 3.087 | 6.209 |
| Coal | Oil | 2.416 | 6.085 | 4.272 | 7.378 |
| Coal | Nuclear | 2.416 | 6.085 | -8.805 | -6.001 |
| Coal | Hydro | 2.416 | 6.085 | 2.725 | 6.572 |
| Coal | Solar | 2.416 | 6.085 | -7.111 | 2.745 |
| Coal | Wind | 2.416 | 6.085 | -6.153 | 2.069 |
| Coal | Biofuel | 2.416 | 6.085 | -8.805 | -6.001 |
| Gas | Oil | 3.087 | 6.209 | 4.272 | 7.378 |
| Gas | Nuclear | 3.087 | 6.209 | -8.805 | -6.001 |
| Gas | Hydro | 3.087 | 6.209 | 2.725 | 6.572 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*