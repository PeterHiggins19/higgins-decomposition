# Stage 1 Report (pure CoDa) — energy_owid_aze

**Domain:** energy
**Description:** OWID primary-energy consumption composition for AZE (AZE), annual TWh. T = 37 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: AZE

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `651b3af68712e4c3ad201e4e5f83deed94e66d76fc4868e3b8dd481c57c6cbb7`

## Input

- Source CSV: `owid_energy_AZE.csv`
- Source SHA-256: `d2e0390de48e6197...`
- Records (T): **37**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `482cf28bbd1e6c6a...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1985 | 0.7766 | 16.1859 | — |
| 1 | 1986 | 0.7454 | 16.0397 | 0.5241 |
| 2 | 1987 | 0.7426 | 16.0493 | 0.0537 |
| 3 | 1988 | 0.7411 | 16.0225 | 0.1364 |
| 4 | 1989 | 0.7327 | 16.0076 | 0.0577 |
| ... | ... | ... | ... | ... |
| 34 | 2022 | 0.7327 | 14.4353 | 0.7456 |
| 35 | 2023 | 0.7372 | 14.4581 | 0.5097 |
| 36 | 2024 | 0.8182 | 14.7501 | 1.8393 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Gas | Nuclear | +0.9794 | 13.0° | no |
| Gas | Biofuel | +0.9794 | 13.0° | no |
| Oil | Nuclear | +0.9758 | 14.2° | no |
| Oil | Biofuel | +0.9758 | 14.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Solar | Biofuel | -0.9354 | 63.0° | no |
| Gas | Wind | -0.9355 | 40.7° | no |
| Oil | Wind | -0.9456 | 42.6° | no |
| Nuclear | Wind | -0.9570 | 356.9° | no |
| Wind | Biofuel | -0.9570 | 50.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | -5.301 | 2.939 | 6.642 | 8.159 |
| Coal | Oil | -5.301 | 2.939 | 6.064 | 7.917 |
| Coal | Nuclear | -5.301 | 2.939 | -6.687 | -5.141 |
| Coal | Hydro | -5.301 | 2.939 | 3.012 | 5.654 |
| Coal | Solar | -5.301 | 2.939 | -5.802 | 2.148 |
| Coal | Wind | -5.301 | 2.939 | -5.531 | 0.614 |
| Coal | Biofuel | -5.301 | 2.939 | -6.687 | -5.141 |
| Gas | Oil | 6.642 | 8.159 | 6.064 | 7.917 |
| Gas | Nuclear | 6.642 | 8.159 | -6.687 | -5.141 |
| Gas | Hydro | 6.642 | 8.159 | 3.012 | 5.654 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*