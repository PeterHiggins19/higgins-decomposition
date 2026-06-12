# Stage 1 Report (pure CoDa) — energy_ember_combined_panel

**Domain:** energy
**Description:** EMBER 8-country combined panel — country and year columns flattened into a single trajectory; D = 9 generation carriers.
**Citation / source:** EMBER Climate (panel construction by HCI-CNT codawork2026 pipeline)

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:04Z
**cnt_content_sha256:** `7e84977e8d4ca5e69ac1d7d0883148849940be16efa3082340beb128e936e984`

## Input

- Source CSV: `ember_combined_panel_input.csv`
- Source SHA-256: `0287246a89863cc0...`
- Records (T): **207**
- Carriers (D): **9**
- Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind
- Closed-data SHA-256: `24121b69c80249fa...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | CHN-2000 | 0.6986 | 35.7762 | — |
| 1 | CHN-2001 | 0.7188 | 35.8192 | 0.4608 |
| 2 | CHN-2002 | 0.7013 | 35.8846 | 0.5784 |
| 3 | CHN-2003 | 0.6820 | 36.0325 | 0.4899 |
| 4 | CHN-2004 | 0.7089 | 36.1919 | 0.3508 |
| ... | ... | ... | ... | ... |
| 204 | WLD-2023 | 1.7687 | 4.0377 | 0.2140 |
| 205 | WLD-2024 | 1.7867 | 4.0713 | 0.2303 |
| 206 | WLD-2025 | 1.8081 | 4.0871 | 0.2455 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Bioenergy | Gas | +0.9217 | 345.9° | no |
| Gas | Other Fossil | +0.8993 | 163.7° | no |
| Coal | Hydro | +0.8974 | 276.0° | no |
| Bioenergy | Other Fossil | +0.8889 | 355.5° | no |
| Hydro | Other Fossil | +0.8522 | 343.0° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Other Renewables | -0.7917 | 110.9° | no |
| Other Fossil | Other Renewables | -0.7984 | 156.2° | no |
| Coal | Other Renewables | -0.8213 | 146.7° | no |
| Hydro | Other Renewables | -0.8242 | 120.4° | no |
| Bioenergy | Other Renewables | -0.8707 | 154.5° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 36 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Bioenergy | Coal | -1.561 | 8.454 | -2.671 | 10.657 |
| Bioenergy | Gas | -1.561 | 8.454 | -0.043 | 10.550 |
| Bioenergy | Hydro | -1.561 | 8.454 | -0.687 | 8.842 |
| Bioenergy | Nuclear | -1.561 | 8.454 | -33.689 | 10.098 |
| Bioenergy | Other Fossil | -1.561 | 8.454 | -1.933 | 9.246 |
| Bioenergy | Other Renewables | -1.561 | 8.454 | -36.463 | 2.168 |
| Bioenergy | Solar | -1.561 | 8.454 | -35.151 | 9.027 |
| Bioenergy | Wind | -1.561 | 8.454 | -4.215 | 9.444 |
| Coal | Gas | -2.671 | 10.657 | -0.043 | 10.550 |
| Coal | Hydro | -2.671 | 10.657 | -0.687 | 8.842 |
| ... (26 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*