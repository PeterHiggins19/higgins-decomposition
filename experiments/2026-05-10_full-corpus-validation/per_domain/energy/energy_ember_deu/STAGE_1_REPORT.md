# Stage 1 Report (pure CoDa) — energy_ember_deu

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for Germany, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:03Z
**cnt_content_sha256:** `9eb5bb7ccbf3b0d4829c86c2248d5e6eb9914967fb9833e5e912e44a06c4f27a`

## Input

- Source CSV: `ember_DEU_Germany_generation_TWh.csv`
- Source SHA-256: `8d52a1c20cd36340...`
- Records (T): **26**
- Carriers (D): **9**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind
- Closed-data SHA-256: `f060af8ebe3983a0...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2000 | 1.2508 | 47.5704 | — |
| 1 | 2001 | 1.2872 | 35.8312 | 30.3382 |
| 2 | 2002 | 1.3058 | 35.8630 | 0.7326 |
| 3 | 2003 | 1.3420 | 35.9423 | 0.6614 |
| 4 | 2004 | 1.3890 | 36.0079 | 0.5772 |
| ... | ... | ... | ... | ... |
| 23 | 2023 | 1.8076 | 5.7978 | 1.5336 |
| 24 | 2024 | 1.7783 | 36.1554 | 34.4578 |
| 25 | 2025 | 1.7670 | 48.1587 | 31.1242 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Other Fossil | +0.9987 | 301.8° | no |
| Gas | Other Fossil | +0.9978 | 59.8° | no |
| Gas | Hydro | +0.9975 | 72.3° | no |
| Coal | Other Fossil | +0.9939 | 53.3° | no |
| Bioenergy | Wind | +0.9923 | 23.2° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Bioenergy | Other Renewables | -0.7089 | 78.4° | no |
| Gas | Other Renewables | -0.8198 | 74.9° | no |
| Hydro | Other Renewables | -0.8249 | 86.8° | no |
| Other Fossil | Other Renewables | -0.8381 | 84.6° | no |
| Coal | Other Renewables | -0.8665 | 72.7° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 36 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | 0.442 | 8.454 | 1.474 | 10.657 |
| Bioenergy | Gas | 0.442 | 8.454 | 0.748 | 8.946 |
| Bioenergy | Hydro | 0.442 | 8.454 | -0.561 | 8.043 |
| Bioenergy | Nuclear | 0.442 | 8.454 | -33.689 | 10.098 |
| Bioenergy | Other Fossil | 0.442 | 8.454 | -0.371 | 7.858 |
| Bioenergy | Other Renewables | 0.442 | 8.454 | -33.965 | -0.665 |
| Bioenergy | Solar | 0.442 | 8.454 | -29.574 | 9.027 |
| Bioenergy | Wind | 0.442 | 8.454 | 0.599 | 9.444 |
| Coal | Gas | 1.474 | 10.657 | 0.748 | 8.946 |
| Coal | Hydro | 1.474 | 10.657 | -0.561 | 8.043 |
| ... (26 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*