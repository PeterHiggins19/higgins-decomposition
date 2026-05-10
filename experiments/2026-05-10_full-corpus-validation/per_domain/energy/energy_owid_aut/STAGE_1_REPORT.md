# Stage 1 Report (pure CoDa) — energy_owid_aut

**Domain:** energy
**Description:** OWID primary-energy consumption composition for AUT (AUT), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: AUT

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `7a95775484e5ca7137b54c1deec9440ec3a526c396890f4f45ebc53b6ea00651`

## Input

- Source CSV: `owid_energy_AUT.csv`
- Source SHA-256: `29f864dbe4f17210...`
- Records (T): **60**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `6c2ad47133537781...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1965 | 1.2961 | 17.4467 | — |
| 1 | 1966 | 1.2975 | 17.4550 | 0.1110 |
| 2 | 1967 | 1.2863 | 17.4396 | 0.0986 |
| 3 | 1968 | 1.2717 | 17.4234 | 0.1176 |
| 4 | 1969 | 1.2693 | 17.4316 | 0.2121 |
| ... | ... | ... | ... | ... |
| 57 | 2022 | 1.5432 | 11.0239 | 0.3747 |
| 58 | 2023 | 1.5785 | 11.0209 | 0.5218 |
| 59 | 2024 | 1.6096 | 11.0384 | 0.3654 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9990 | 33.4° | no |
| Nuclear | Hydro | +0.9970 | 32.4° | no |
| Oil | Hydro | +0.9936 | 3.8° | YES |
| Coal | Nuclear | +0.9925 | 39.8° | no |
| Coal | Oil | +0.9912 | 21.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Solar | -0.9422 | 358.2° | no |
| Nuclear | Wind | -0.9432 | 356.9° | no |
| Coal | Wind | -0.9435 | 90.6° | no |
| Oil | Solar | -0.9451 | 66.5° | no |
| Coal | Solar | -0.9488 | 97.9° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 1.183 | 6.506 | 2.075 | 6.006 |
| Coal | Oil | 1.183 | 6.506 | 2.734 | 6.985 |
| Coal | Nuclear | 1.183 | 6.506 | -10.003 | -6.144 |
| Coal | Hydro | 1.183 | 6.506 | 2.470 | 6.468 |
| Coal | Solar | 1.183 | 6.506 | -6.185 | 0.987 |
| Coal | Wind | 1.183 | 6.506 | -6.422 | 0.964 |
| Coal | Biofuel | 1.183 | 6.506 | -7.849 | 0.217 |
| Gas | Oil | 2.075 | 6.006 | 2.734 | 6.985 |
| Gas | Nuclear | 2.075 | 6.006 | -10.003 | -6.144 |
| Gas | Hydro | 2.075 | 6.006 | 2.470 | 6.468 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*