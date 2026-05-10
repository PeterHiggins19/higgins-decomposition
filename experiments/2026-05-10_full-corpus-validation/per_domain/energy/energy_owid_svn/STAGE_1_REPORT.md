# Stage 1 Report (pure CoDa) — energy_owid_svn

**Domain:** energy
**Description:** OWID primary-energy consumption composition for SVN (SVN), annual TWh. T = 35 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: SVN

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:12Z
**cnt_content_sha256:** `5ad398b741423bec0f3d4820cc69631191a01cccf64f9327b869a764e8890423`

## Input

- Source CSV: `owid_energy_SVN.csv`
- Source SHA-256: `096af202a83aa043...`
- Records (T): **35**
- Carriers (D): **8**
- Carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel
- Closed-data SHA-256: `0992e7c879c6110f...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1990 | 1.5479 | 16.6528 | — |
| 1 | 1991 | 1.5650 | 16.6714 | 0.2304 |
| 2 | 1992 | 1.5463 | 16.6420 | 0.2160 |
| 3 | 1993 | 1.5171 | 16.6102 | 0.2326 |
| 4 | 1994 | 1.5256 | 16.6244 | 0.1709 |
| ... | ... | ... | ... | ... |
| 32 | 2022 | 1.5893 | 6.3933 | 0.6144 |
| 33 | 2023 | 1.6554 | 6.2941 | 0.5591 |
| 34 | 2024 | 1.7063 | 6.3470 | 0.6029 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Nuclear | +0.9984 | 13.8° | no |
| Gas | Oil | +0.9972 | 17.4° | no |
| Oil | Nuclear | +0.9966 | 9.0° | YES |
| Coal | Nuclear | +0.9963 | 14.4° | no |
| Coal | Gas | +0.9954 | 10.1° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Hydro | Solar | -0.9584 | 80.1° | no |
| Nuclear | Solar | -0.9667 | 76.2° | no |
| Coal | Solar | -0.9672 | 78.1° | no |
| Oil | Solar | -0.9682 | 69.5° | no |
| Gas | Solar | -0.9710 | 83.9° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Coal | Gas | 0.952 | 4.927 | 0.840 | 4.234 |
| Coal | Oil | 0.952 | 4.927 | 1.979 | 5.333 |
| Coal | Nuclear | 0.952 | 4.927 | 1.379 | 4.615 |
| Coal | Hydro | 0.952 | 4.927 | 1.002 | 4.322 |
| Coal | Solar | 0.952 | 4.927 | -8.510 | 0.221 |
| Coal | Wind | 0.952 | 4.927 | -9.738 | -5.069 |
| Coal | Biofuel | 0.952 | 4.927 | -7.603 | -0.691 |
| Gas | Oil | 0.840 | 4.234 | 1.979 | 5.333 |
| Gas | Nuclear | 0.840 | 4.234 | 1.379 | 4.615 |
| Gas | Hydro | 0.840 | 4.234 | 1.002 | 4.322 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*