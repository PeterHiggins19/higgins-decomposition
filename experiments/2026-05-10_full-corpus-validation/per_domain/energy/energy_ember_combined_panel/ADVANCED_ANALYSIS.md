# Advanced Analysis (Hˢ + CNQ v2) — energy_ember_combined_panel

**Domain:** energy
**Description:** EMBER 8-country combined panel — country and year columns flattened into a single trajectory; D = 9 generation carriers.
**Citation / source:** EMBER Climate (panel construction by HCI-CNT codawork2026 pipeline)

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `7e84977e8d4ca5e69ac1d7d0883148849940be16efa3082340beb128e936e984`
**cnq_content_sha256:** `bdb37bc5b5d47abccdddbeced94ece34412858cd43b92c0cc3300ca48444d3c0`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 207 | Trajectory length |
| D (carriers) | 9 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.507e-13 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 8.3916 | Cycle amplitude |
| Damping ζ | +0.0012 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 107 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.4780 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 107 |
| Stability S_σ (global) | 0.4780 |

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
| Bearing angle range | 0.0018 to 2.3330 rad |
| Bearing angle mean | 0.1094 rad |
| Bearing pairs tested | 206 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.2069 |
| Captured step fraction (global) | 0.0065 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Bioenergy | Gas | +0.9217 | 345.9° | no |
| Gas | Other Fossil | +0.8993 | 163.7° | no |
| Coal | Hydro | +0.8974 | 276.0° | no |
| Bioenergy | Other Fossil | +0.8889 | 355.5° | no |
| Bioenergy | Other Renewables | -0.8707 | 154.5° | no |
| Hydro | Other Fossil | +0.8522 | 343.0° | no |
| Bioenergy | Wind | +0.8441 | 356.4° | no |
| Coal | Other Fossil | +0.8339 | 333.5° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*