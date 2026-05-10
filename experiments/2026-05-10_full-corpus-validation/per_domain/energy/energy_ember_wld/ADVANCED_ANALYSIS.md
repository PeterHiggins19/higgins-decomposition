# Advanced Analysis (Hˢ + CNQ v2) — energy_ember_wld

**Domain:** energy
**Description:** EMBER electricity-generation-by-source aggregated for the World, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `cedb9bde2ff40f43b13d5163d718889c7c6a7f37d0c0a16c738705cf8b4543c4`
**cnq_content_sha256:** `79b7e72361df9711090eb31c11bcc4b7b7085344206638aac9a109e9cde01e9b`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 26 | Trajectory length |
| D (carriers) | 9 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.1351 | Cycle amplitude |
| Damping ζ | +0.0042 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 4 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.8333 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 4 |
| Stability S_σ (global) | 0.8333 |

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
| Bearing angle range | 0.0018 to 0.0346 rad |
| Bearing angle mean | 0.0134 rad |
| Bearing pairs tested | 25 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.0339 |
| Captured step fraction (global) | 0.0246 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Solar | -0.9986 | 75.3° | no |
| Gas | Solar | -0.9980 | 85.3° | no |
| Hydro | Solar | -0.9967 | 93.7° | no |
| Nuclear | Solar | -0.9959 | 114.2° | no |
| Hydro | Nuclear | +0.9957 | 20.9° | no |
| Nuclear | Other Renewables | +0.9955 | 39.6° | no |
| Coal | Gas | +0.9954 | 2.5° | YES |
| Coal | Hydro | +0.9948 | 9.8° | YES |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*