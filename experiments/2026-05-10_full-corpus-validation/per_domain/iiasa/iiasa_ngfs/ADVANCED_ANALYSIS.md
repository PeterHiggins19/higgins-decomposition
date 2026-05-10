# Advanced Analysis (Hˢ + CNQ v2) — iiasa_ngfs

**Domain:** iiasa
**Description:** IIASA NGFS Phase-4 scenario emissions allocation by sector. T = 31 years (2020-2050), D = 7 emission-sector carriers (Energy, Transport, Industry, Buildings, Agriculture, LULUCF, Other).
**Citation / source:** IIASA NGFS Phase-4 dataset (Network for Greening the Financial System scenarios)

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `82dbeccfe91b487eb760a9ec9d4288747de6df47a1aebc27c9ea4ec7cfd5e438`
**cnq_content_sha256:** `68c31ed1dc840449dc1b48441a577dd546b64a2a8f1c686f57ba2383f668b007`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 31 | Trajectory length |
| D (carriers) | 7 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.5799 | Cycle amplitude |
| Damping ζ | -0.0002 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 1 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.9655 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 1 |
| Stability S_σ (global) | 0.9655 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `reduced_or_projected` |
| D | 7 |
| Branch | `—` |
| Bearing angle range | 0.0123 to 0.0812 rad |
| Bearing angle mean | 0.0318 rad |
| Bearing pairs tested | 30 |
| Bearing max residual | 4.44e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1961 |
| Captured step fraction (global) | 0.1562 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Agriculture | Other | +0.9988 | 34.1° | no |
| Buildings | LULUCF | -0.9984 | 353.5° | no |
| Energy | Agriculture | -0.9983 | 108.2° | no |
| Energy | Other | -0.9981 | 54.3° | no |
| Transport | LULUCF | -0.9980 | 158.0° | no |
| Transport | Buildings | +0.9979 | 70.7° | no |
| Transport | Other | -0.9812 | 29.2° | no |
| Energy | Transport | +0.9733 | 154.4° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*