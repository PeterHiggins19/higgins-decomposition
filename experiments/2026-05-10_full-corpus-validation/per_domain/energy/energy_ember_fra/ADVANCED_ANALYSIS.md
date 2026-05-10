# Advanced Analysis (Hˢ + CNQ v2) — energy_ember_fra

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for France, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `5dae940f20941c6f902b8195a8a32c753cef7bee32fe43c1f584b2e1e48c1e0f`
**cnq_content_sha256:** `7bf56321bb17087016e9665156e1102e770214c8307e402108887bf2cfb90b99`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 26 | Trajectory length |
| D (carriers) | 9 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.1772 | Cycle amplitude |
| Damping ζ | -0.0428 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 12 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.5000 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 12 |
| Stability S_σ (global) | 0.5000 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `reduced_or_projected` |
| D | 9 |
| Branch | `—` |
| Bearing angle range | 0.0042 to 0.3383 rad |
| Bearing angle mean | 0.1568 rad |
| Bearing pairs tested | 25 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.4267 |
| Captured step fraction (global) | 0.3162 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Other Fossil | +0.9890 | 23.6° | no |
| Other Fossil | Other Renewables | +0.9782 | 40.9° | no |
| Hydro | Nuclear | +0.9745 | 13.4° | no |
| Nuclear | Other Renewables | +0.9738 | 28.0° | no |
| Nuclear | Solar | -0.9691 | 67.4° | no |
| Hydro | Other Renewables | +0.9681 | 40.8° | no |
| Other Fossil | Solar | -0.9629 | 332.2° | no |
| Hydro | Other Fossil | +0.9566 | 47.9° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*