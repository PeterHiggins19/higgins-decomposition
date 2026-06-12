# Stage 1 Report (pure CoDa) — commodities_gold_silver

**Domain:** commodities
**Description:** Annual gold-silver mass-fraction composition normalized over both metals, 1688-2025 (T = 1338 years). D = 2 carriers — minimum compositional dimension; the engine handles D = 2 via the degenerate-pair branch.
**Citation / source:** Compiled from BoE+Bullion historical price/production records; normalized to a 2-element composition by total-mass weighting

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:05Z
**cnt_content_sha256:** `bcf18e517375e80cab742fa6aa9426497846b37ea42abbd38e51df201502a15d`

## Input

- Source CSV: `commodities_gold_silver_input.csv`
- Source SHA-256: `c22e45ebac0b37b7...`
- Records (T): **1338**
- Carriers (D): **2**
- Carriers: Gold, Silver
- Closed-data SHA-256: `2d77c9e71505e71e...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 1688 | 0.2344 | 1.9120 | — |
| 1 | 1689 | 0.2336 | 1.9158 | 0.0038 |
| 2 | 1690 | 0.2336 | 1.9158 | 0.0000 |
| 3 | 1691 | 0.2340 | 1.9139 | 0.0019 |
| 4 | 1692 | 0.2346 | 1.9111 | 0.0028 |
| ... | ... | ... | ... | ... |
| 1335 | 2026 | 0.0820 | 2.9124 | 0.0000 |
| 1336 | 2026 | 0.0820 | 2.9124 | 0.0000 |
| 1337 | 2026 | 0.0820 | 2.9124 | 0.0000 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gold | Silver | -1.0000 | 0.0° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gold | Silver | -1.0000 | 0.0° | YES |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 1 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Gold | Silver | 1.325 | 2.301 | -2.301 | -1.325 |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*