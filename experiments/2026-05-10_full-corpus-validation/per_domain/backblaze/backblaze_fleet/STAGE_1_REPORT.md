# Stage 1 Report (pure CoDa) — backblaze_fleet

**Domain:** backblaze
**Description:** Backblaze drive failure telemetry, daily 2024-01-01 through 2025-12-31. D = 4 derived stress carriers (Mechanical, Thermal, Age, Errors) computed from the SMART-attribute aggregation.
**Citation / source:** Backblaze Drive Stats (https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data); pipeline-ready aggregation in HCI-CNT/adapters/backblaze_adapter.py

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:04Z
**cnt_content_sha256:** `2e5e111fe36dac11f3bf0f57ce66b9640401eeb9c406925a7d157f12aee54c15`

## Input

- Source CSV: `backblaze_fleet_input.csv`
- Source SHA-256: `1861af25ad461f4a...`
- Records (T): **731**
- Carriers (D): **4**
- Carriers: Mechanical, Thermal, Age, Errors
- Closed-data SHA-256: `72d8c2f5404bf60a...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2024-01-01 | 0.1883 | 3.8620 | — |
| 1 | 2024-01-02 | 0.1889 | 3.8592 | 0.0060 |
| 2 | 2024-01-03 | 0.1913 | 3.8499 | 0.0307 |
| 3 | 2024-01-04 | 0.1844 | 3.8769 | 0.0939 |
| 4 | 2024-01-05 | 0.1798 | 3.8975 | 0.0654 |
| ... | ... | ... | ... | ... |
| 728 | 2025-12-29 | 0.9281 | 2.1312 | 0.0263 |
| 729 | 2025-12-30 | 0.9320 | 2.1270 | 0.0125 |
| 730 | 2025-12-31 | 0.9281 | 2.1179 | 0.0306 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Thermal | Age | +0.9656 | 5.1° | YES |
| Mechanical | Age | +0.3994 | 62.6° | no |
| Mechanical | Thermal | +0.2771 | 67.7° | no |
| Thermal | Errors | -0.7378 | 13.6° | no |
| Age | Errors | -0.8181 | 14.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Mechanical | Age | +0.3994 | 62.6° | no |
| Mechanical | Thermal | +0.2771 | 67.7° | no |
| Thermal | Errors | -0.7378 | 13.6° | no |
| Age | Errors | -0.8181 | 14.3° | no |
| Mechanical | Errors | -0.8504 | 34.2° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 6 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Mechanical | Thermal | -0.963 | 0.496 | -1.223 | -0.658 |
| Mechanical | Age | -0.963 | 0.496 | -1.352 | -0.821 |
| Mechanical | Errors | -0.963 | 0.496 | 1.506 | 3.373 |
| Thermal | Age | -1.223 | -0.658 | -1.352 | -0.821 |
| Thermal | Errors | -1.223 | -0.658 | 1.506 | 3.373 |
| Age | Errors | -1.352 | -0.821 | 1.506 | 3.373 |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*