# Stage 1 Report (pure CoDa) — energy_owid_grc

**Domain:** energy
**Description:** OWID primary-energy consumption composition for GRC (GRC), annual TWh. T = 43 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: GRC

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `435add9c71eec931c33e2ebefeb80ece950bdd7e0d3b8f3339fc67cc6e313729`

## Input

- Source CSV: `owid_energy_GRC.csv`
- Source SHA-256: `0456160e2d7b9ffc...`
- Records (T): **43**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `11cc6215e95b90b9...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1982 | 0.7536 | 16.3665 | — |
| 1 | 1983 | 0.7538 | 16.2890 | 0.4603 |
| 2 | 1984 | 0.7769 | 16.3444 | 0.1506 |
| 3 | 1985 | 0.7883 | 16.3293 | 0.1632 |
| 4 | 1986 | 0.7993 | 16.4062 | 0.3119 |
| ... | ... | ... | ... | ... |
| 40 | 2022 | 1.3411 | 10.9330 | 0.5714 |
| 41 | 2023 | 1.3302 | 10.9285 | 0.3522 |
| 42 | 2024 | 1.3249 | 10.9362 | 0.4402 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9998 | 35.8° | no |
| Nuclear | Hydro | +0.9827 | 40.4° | no |
| Oil | Hydro | +0.9818 | 27.0° | no |
| Coal | Nuclear | +0.9800 | 47.6° | no |
| Coal | Oil | +0.9794 | 31.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Solar | -0.8970 | 356.3° | no |
| Oil | Biofuel | -0.9000 | 44.2° | no |
| Nuclear | Biofuel | -0.9010 | 41.3° | no |
| Oil | Solar | -0.9016 | 74.0° | no |
| Coal | Solar | -0.9139 | 121.8° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.692 | 7.080 | 1.206 | 4.021 |
| Coal | Oil | 0.692 | 7.080 | 3.326 | 7.850 |
| Coal | Nuclear | 0.692 | 7.080 | -9.816 | -5.584 |
| Coal | Hydro | 0.692 | 7.080 | 0.397 | 5.189 |
| Coal | Solar | 0.692 | 7.080 | -7.011 | 1.548 |
| Coal | Wind | 0.692 | 7.080 | -5.646 | 1.844 |
| Coal | Biofuel | 0.692 | 7.080 | -7.284 | -0.532 |
| Gas | Oil | 1.206 | 4.021 | 3.326 | 7.850 |
| Gas | Nuclear | 1.206 | 4.021 | -9.816 | -5.584 |
| Gas | Hydro | 1.206 | 4.021 | 0.397 | 5.189 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*