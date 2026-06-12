# Stage 1 Report (pure CoDa) — iiasa_ngfs

**Domain:** iiasa
**Description:** IIASA NGFS Phase-4 scenario emissions allocation by sector. T = 31 years (2020-2050), D = 7 emission-sector carriers (Energy, Transport, Industry, Buildings, Agriculture, LULUCF, Other).
**Citation / source:** IIASA NGFS Phase-4 dataset (Network for Greening the Financial System scenarios)

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:05Z
**cnt_content_sha256:** `82dbeccfe91b487eb760a9ec9d4288747de6df47a1aebc27c9ea4ec7cfd5e438`

## Input

- Source CSV: `iiasa_ngfs_input.csv`
- Source SHA-256: `c22adce0bfa1aad3...`
- Records (T): **31**
- Carriers (D): **7**
- Carriers: Energy, Transport, Industry, Buildings, Agriculture, LULUCF, Other
- Closed-data SHA-256: `502770a19fcea337...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2020 | 1.5893 | 2.5114 | — |
| 1 | 2021 | 1.6141 | 2.4011 | 0.1880 |
| 2 | 2022 | 1.6369 | 2.3097 | 0.1604 |
| 3 | 2023 | 1.6578 | 2.2315 | 0.1411 |
| 4 | 2024 | 1.6772 | 2.1634 | 0.1269 |
| ... | ... | ... | ... | ... |
| 28 | 2048 | 1.7858 | 1.6733 | 0.0955 |
| 29 | 2049 | 1.7761 | 1.6932 | 0.1014 |
| 30 | 2050 | 1.7651 | 1.7194 | 0.1087 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Agriculture | Other | +0.9988 | 34.1° | no |
| Transport | Buildings | +0.9979 | 70.7° | no |
| Energy | Transport | +0.9733 | 154.4° | no |
| LULUCF | Other | +0.9710 | 76.9° | no |
| Agriculture | LULUCF | +0.9582 | 155.9° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Transport | Other | -0.9812 | 29.2° | no |
| Transport | LULUCF | -0.9980 | 158.0° | no |
| Energy | Other | -0.9981 | 54.3° | no |
| Energy | Agriculture | -0.9983 | 108.2° | no |
| Buildings | LULUCF | -0.9984 | 353.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 21 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Energy | Transport | -0.157 | 1.491 | -0.157 | 0.526 |
| Energy | Industry | -0.157 | 1.491 | 0.497 | 0.749 |
| Energy | Buildings | -0.157 | 1.491 | -0.850 | -0.301 |
| Energy | Agriculture | -0.157 | 1.491 | -0.050 | 0.536 |
| Energy | LULUCF | -0.157 | 1.491 | -0.861 | 0.942 |
| Energy | Other | -0.157 | 1.491 | -1.554 | -0.850 |
| Transport | Industry | -0.157 | 0.526 | 0.497 | 0.749 |
| Transport | Buildings | -0.157 | 0.526 | -0.850 | -0.301 |
| Transport | Agriculture | -0.157 | 0.526 | -0.050 | 0.536 |
| Transport | LULUCF | -0.157 | 0.526 | -0.861 | 0.942 |
| ... (11 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*