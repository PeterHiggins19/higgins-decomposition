# Stage 1 Report (pure CoDa) — energy_owid_est

**Domain:** energy
**Description:** OWID primary-energy consumption composition for EST (EST), annual TWh. T = 26 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: EST

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:08Z
**cnt_content_sha256:** `1e67ac339b683904e5d4b8daabaf19ca1b584740f928035501447ac220b2977d`

## Input

- Source CSV: `owid_energy_EST.csv`
- Source SHA-256: `53f2c5a65a23409f...`
- Records (T): **26**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `4eaeac05c6bd02da...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1999 | 0.9236 | 16.4249 | — |
| 1 | 2000 | 0.9161 | 16.4411 | 0.2577 |
| 2 | 2001 | 0.9449 | 16.4648 | 0.3241 |
| 3 | 2002 | 0.9354 | 15.4953 | 3.9843 |
| 4 | 2003 | 0.9162 | 15.3732 | 1.3935 |
| ... | ... | ... | ... | ... |
| 23 | 2022 | 1.0794 | 11.1437 | 0.7914 |
| 24 | 2023 | 1.1099 | 11.1424 | 0.3919 |
| 25 | 2024 | 1.2220 | 11.1868 | 0.5506 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Nuclear | +0.9986 | 33.4° | no |
| Oil | Nuclear | +0.9979 | 33.6° | no |
| Gas | Nuclear | +0.9938 | 39.2° | no |
| Gas | Oil | +0.9936 | 14.3° | no |
| Coal | Oil | +0.9934 | 4.0° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Solar | -0.8625 | 334.4° | no |
| Gas | Biofuel | -0.8792 | 46.2° | no |
| Coal | Biofuel | -0.8937 | 40.6° | no |
| Nuclear | Biofuel | -0.8998 | 44.5° | no |
| Oil | Biofuel | -0.9059 | 44.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 3.872 | 7.952 | 1.805 | 6.459 |
| Coal | Oil | 3.872 | 7.952 | 3.312 | 7.163 |
| Coal | Nuclear | 3.872 | 7.952 | -9.298 | -5.359 |
| Coal | Hydro | 3.872 | 7.952 | -2.269 | 0.574 |
| Coal | Solar | 3.872 | 7.952 | -7.455 | 1.596 |
| Coal | Wind | 3.872 | 7.952 | -5.438 | 2.009 |
| Coal | Biofuel | 3.872 | 7.952 | -6.281 | -0.087 |
| Gas | Oil | 1.805 | 6.459 | 3.312 | 7.163 |
| Gas | Nuclear | 1.805 | 6.459 | -9.298 | -5.359 |
| Gas | Hydro | 1.805 | 6.459 | -2.269 | 0.574 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*