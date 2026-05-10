# Advanced Analysis (Hˢ + CNQ v2) — backblaze_fleet

**Domain:** backblaze
**Description:** Backblaze drive failure telemetry, daily 2024-01-01 through 2025-12-31. D = 4 derived stress carriers (Mechanical, Thermal, Age, Errors) computed from the SMART-attribute aggregation.
**Citation / source:** Backblaze Drive Stats (https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data); pipeline-ready aggregation in HCI-CNT/adapters/backblaze_adapter.py

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `2e5e111fe36dac11f3bf0f57ce66b9640401eeb9c406925a7d157f12aee54c15`
**cnq_content_sha256:** `cf7a3bac80a388c68033683483f952e6f5c8c4280bcb17aeb107ecffa3fbfe96`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 731 | Trajectory length |
| D (carriers) | 4 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.2156 | Cycle amplitude |
| Damping ζ | -0.0002 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 220 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.6982 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `single_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 220 |
| Stability S_σ (global) | 0.6982 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `single_quaternion_native` |
| D | 4 |
| Branch | `—` |
| Bearing angle range | 0.0002 to 0.1881 rad |
| Bearing angle mean | 0.0130 rad |
| Bearing pairs tested | 730 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.0000 |
| Captured step fraction (global) | 0.0000 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Thermal | Age | +0.9656 | 5.1° | YES |
| Mechanical | Errors | -0.8504 | 34.2° | no |
| Age | Errors | -0.8181 | 14.3° | no |
| Thermal | Errors | -0.7378 | 13.6° | no |
| Mechanical | Age | +0.3994 | 62.6° | no |
| Mechanical | Thermal | +0.2771 | 67.7° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*