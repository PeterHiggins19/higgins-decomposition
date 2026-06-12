# Stage 1 Report (pure CoDa) — energy_owid_twn

**Domain:** energy
**Description:** OWID primary-energy consumption composition for TWN (TWN), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: TWN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `6c129612eef9b1f5113e437a32a613b26c12c1d8fcb4b82e7a8ce095f662f4e7`

## Input

- Source CSV: `owid_energy_TWN.csv`
- Source SHA-256: `a9c258155916b572...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `cf7a33863838db0b...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.0619 | 17.0614 | — |
| 1 | 1966 | 1.0679 | 17.0694 | 0.1379 |
| 2 | 1967 | 1.0709 | 17.0851 | 0.2223 |
| 3 | 1968 | 1.1236 | 17.1856 | 0.3242 |
| 4 | 1969 | 1.0850 | 17.1573 | 0.3827 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.3653 | 11.0199 | 0.6935 |
| 58 | 2023 | 1.3708 | 11.0000 | 0.7646 |
| 59 | 2024 | 1.3855 | 10.9857 | 0.6435 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9720 | 52.7° | no |
| Coal | Hydro | +0.9220 | 57.0° | no |
| Coal | Oil | +0.9217 | 11.5° | no |
| Gas | Oil | +0.8913 | 15.5° | no |
| Gas | Hydro | +0.8765 | 71.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Solar | -0.6650 | 73.9° | no |
| Gas | Nuclear | -0.6674 | 113.5° | no |
| Coal | Wind | -0.7317 | 63.5° | no |
| Hydro | Wind | -0.8074 | 320.0° | no |
| Oil | Wind | -0.8541 | 56.4° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.897 | 7.131 | 1.939 | 5.491 |
| Coal | Oil | 2.897 | 7.131 | 3.007 | 7.588 |
| Coal | Nuclear | 2.897 | 7.131 | -6.042 | 4.920 |
| Coal | Hydro | 2.897 | 7.131 | -0.759 | 5.603 |
| Coal | Solar | 2.897 | 7.131 | -7.674 | 0.640 |
| Coal | Wind | 2.897 | 7.131 | -7.326 | 0.273 |
| Coal | Biofuel | 2.897 | 7.131 | -9.644 | -2.485 |
| Gas | Oil | 1.939 | 5.491 | 3.007 | 7.588 |
| Gas | Nuclear | 1.939 | 5.491 | -6.042 | 4.920 |
| Gas | Hydro | 1.939 | 5.491 | -0.759 | 5.603 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*