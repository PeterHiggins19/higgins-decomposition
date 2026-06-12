# Stage 1 Report (pure CoDa) — energy_owid_tha

**Domain:** energy
**Description:** OWID primary-energy consumption composition for THA (THA), annual TWh. T = 44 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: THA

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `f20fb6e37ce174bacc19abbfd07aa4ba58ef24bd31e922714d9942b8b4cbece1`

## Input

- Source CSV: `owid_energy_THA.csv`
- Source SHA-256: `801e2ab8bbac7543...`
- Records (T): **44**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `a0a0febb300c8b87...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1981 | 0.4753 | 16.1988 | — |
| 1 | 1982 | 0.7539 | 16.7688 | 1.4935 |
| 2 | 1983 | 0.7275 | 16.7102 | 0.1960 |
| 3 | 1984 | 0.8110 | 16.8337 | 0.3028 |
| 4 | 1985 | 0.9503 | 17.0215 | 0.6764 |
| ... | ... | ... | ... | ... |
| 41 | 2022 | 1.1909 | 10.9463 | 0.4400 |
| 42 | 2023 | 1.1814 | 10.9178 | 0.2825 |
| 43 | 2024 | 1.1735 | 10.9220 | 0.1268 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9980 | 33.3° | no |
| Oil | Hydro | +0.9863 | 39.6° | no |
| Nuclear | Hydro | +0.9804 | 359.8° | no |
| Coal | Nuclear | +0.9733 | 30.5° | no |
| Coal | Gas | +0.9711 | 14.7° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Solar | -0.9428 | 51.3° | no |
| Hydro | Solar | -0.9587 | 102.0° | no |
| Coal | Solar | -0.9693 | 49.9° | no |
| Oil | Solar | -0.9790 | 43.9° | no |
| Nuclear | Solar | -0.9847 | 44.2° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.402 | 5.940 | 3.397 | 6.708 |
| Coal | Oil | 2.402 | 5.940 | 3.702 | 8.056 |
| Coal | Nuclear | 2.402 | 5.940 | -9.337 | -5.634 |
| Coal | Hydro | 2.402 | 5.940 | -0.279 | 5.309 |
| Coal | Solar | 2.402 | 5.940 | -6.671 | -0.123 |
| Coal | Wind | 2.402 | 5.940 | -7.445 | -0.511 |
| Coal | Biofuel | 2.402 | 5.940 | -6.015 | 1.100 |
| Gas | Oil | 3.397 | 6.708 | 3.702 | 8.056 |
| Gas | Nuclear | 3.397 | 6.708 | -9.337 | -5.634 |
| Gas | Hydro | 3.397 | 6.708 | -0.279 | 5.309 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*