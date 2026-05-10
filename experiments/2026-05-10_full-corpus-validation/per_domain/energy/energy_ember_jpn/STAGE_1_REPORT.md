# Stage 1 Report (pure CoDa) — energy_ember_jpn

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for Japan, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:03Z
**cnt_content_sha256:** `9f17aa83da0aa6db8cd99fec90ed4f2591c3a9f3a94b6f1878d0a5415731c57a`

## Input

- Source CSV: `ember_JPN_Japan_generation_TWh.csv`
- Source SHA-256: `e7643dca648ecadc...`
- Records (T): **26**
- Carriers (D): **8**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind
- Closed-data SHA-256: `9a4bf868b894abb2...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2000 | 1.5914 | 8.4004 | — |
| 1 | 2001 | 1.5813 | 7.6499 | 0.8478 |
| 2 | 2002 | 1.5911 | 7.1941 | 0.4967 |
| 3 | 2003 | 1.6160 | 6.5871 | 0.7576 |
| 4 | 2004 | 1.6110 | 6.1370 | 0.5825 |
| ... | ... | ... | ... | ... |
| 23 | 2023 | 1.6361 | 3.1122 | 0.5551 |
| 24 | 2024 | 1.6430 | 3.0909 | 0.3276 |
| 25 | 2025 | 1.6681 | 2.9946 | 0.2217 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Gas | +0.9901 | 8.4° | YES |
| Coal | Hydro | +0.9880 | 40.1° | no |
| Gas | Hydro | +0.9699 | 39.0° | no |
| Bioenergy | Coal | +0.9587 | 62.5° | no |
| Bioenergy | Gas | +0.9536 | 57.5° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Wind | -0.8159 | 312.9° | no |
| Hydro | Nuclear | -0.8892 | 191.8° | no |
| Coal | Nuclear | -0.9415 | 127.6° | no |
| Gas | Nuclear | -0.9604 | 126.6° | no |
| Bioenergy | Nuclear | -0.9665 | 354.1° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | -1.004 | 3.839 | 1.440 | 6.550 |
| Bioenergy | Gas | -1.004 | 3.839 | 1.462 | 6.788 |
| Bioenergy | Hydro | -1.004 | 3.839 | -0.057 | 5.080 |
| Bioenergy | Nuclear | -1.004 | 3.839 | -33.862 | 2.524 |
| Bioenergy | Other Fossil | -1.004 | 3.839 | -1.125 | 5.483 |
| Bioenergy | Solar | -1.004 | 3.839 | -4.320 | 3.835 |
| Bioenergy | Wind | -1.004 | 3.839 | -5.449 | 2.288 |
| Coal | Gas | 1.440 | 6.550 | 1.462 | 6.788 |
| Coal | Hydro | 1.440 | 6.550 | -0.057 | 5.080 |
| Coal | Nuclear | 1.440 | 6.550 | -33.862 | 2.524 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*