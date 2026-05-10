# Stage 1 Report (pure CoDa) — energy_owid_bgd

**Domain:** energy
**Description:** OWID primary-energy consumption composition for BGD (BGD), annual TWh. T = 54 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: BGD

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `de5fc6d8510cb3a16098797f012ebe05cda20e7dfc5bd65723a0b678c4715dd1`

## Input

- Source CSV: `owid_energy_BGD.csv`
- Source SHA-256: `32747e3e207e089c...`
- Records (T): **54**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `896063a2e3e8e54d...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1971 | 0.9817 | 17.0245 | — |
| 1 | 1972 | 0.9202 | 16.9107 | 0.2167 |
| 2 | 1973 | 1.0141 | 17.0694 | 0.4388 |
| 3 | 1974 | 0.9721 | 16.9015 | 0.4267 |
| 4 | 1975 | 0.9711 | 17.0355 | 0.6952 |
| ... | ... | ... | ... | ... |
| 51 | 2022 | 0.9694 | 14.3978 | 0.2779 |
| 52 | 2023 | 1.0199 | 14.1926 | 1.1829 |
| 53 | 2024 | 1.0615 | 13.9767 | 1.5671 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Oil | Hydro | +0.9639 | 27.5° | no |
| Oil | Nuclear | +0.9360 | 19.0° | no |
| Oil | Biofuel | +0.9360 | 19.0° | no |
| Nuclear | Hydro | +0.9333 | 35.9° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Wind | -0.9365 | 28.1° | no |
| Solar | Biofuel | -0.9629 | 53.3° | no |
| Nuclear | Solar | -0.9629 | 353.6° | no |
| Oil | Solar | -0.9667 | 53.0° | no |
| Hydro | Solar | -0.9756 | 113.1° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 2.684 | 5.364 | 5.527 | 7.886 |
| Coal | Oil | 2.684 | 5.364 | 4.995 | 7.479 |
| Coal | Nuclear | 2.684 | 5.364 | -7.628 | -5.528 |
| Coal | Hydro | 2.684 | 5.364 | 0.771 | 5.189 |
| Coal | Solar | 2.684 | 5.364 | -5.992 | 1.074 |
| Coal | Wind | 2.684 | 5.364 | -6.213 | -1.523 |
| Coal | Biofuel | 2.684 | 5.364 | -7.628 | -5.528 |
| Gas | Oil | 5.527 | 7.886 | 4.995 | 7.479 |
| Gas | Nuclear | 5.527 | 7.886 | -7.628 | -5.528 |
| Gas | Hydro | 5.527 | 7.886 | 0.771 | 5.189 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*