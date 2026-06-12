# Advanced Analysis (Hˢ + CNQ v2) — energy_ember_jpn

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for Japan, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `9f17aa83da0aa6db8cd99fec90ed4f2591c3a9f3a94b6f1878d0a5415731c57a`
**cnq_content_sha256:** `10cde6fd1c4debb25043f8beaef05e528089f44e0177fcc0b692e9ed0cdfb7fe`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 26 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.665e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 7.0123 | Cycle amplitude |
| Damping ζ | +0.0189 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 17 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.2917 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.4000 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 17 |
| Stability S_σ (global) | 0.2917 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `twin_quaternion_native` |
| D | 8 |
| Branch | `—` |
| Bearing angle range | 0.0034 to 0.1100 rad |
| Bearing angle mean | 0.0402 rad |
| Bearing pairs tested | 25 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1170 |
| Captured step fraction (global) | 0.0002 |
| CHSH S | 0.4000 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Gas | +0.9901 | 8.4° | YES |
| Coal | Hydro | +0.9880 | 40.1° | no |
| Gas | Hydro | +0.9699 | 39.0° | no |
| Bioenergy | Nuclear | -0.9665 | 354.1° | no |
| Gas | Nuclear | -0.9604 | 126.6° | no |
| Bioenergy | Coal | +0.9587 | 62.5° | no |
| Bioenergy | Gas | +0.9536 | 57.5° | no |
| Coal | Nuclear | -0.9415 | 127.6° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*