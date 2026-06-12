# Advanced Analysis (Hˢ + CNQ v2) — energy_ember_ind

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for India, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `a299b9bfb449c89a37f812f1326cc5fc4430aed90e6998507790970ee252373a`
**cnq_content_sha256:** `d808bb3610c3bd5205c10813315d87bef6dd6d9495896ef872bbf8d66f6e39c7`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 26 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.6158 | Cycle amplitude |
| Damping ζ | +0.0187 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 15 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3750 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.0800 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 15 |
| Stability S_σ (global) | 0.3750 |

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
| Bearing angle range | 0.0064 to 0.1442 rad |
| Bearing angle mean | 0.0523 rad |
| Bearing pairs tested | 25 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.2295 |
| Captured step fraction (global) | 0.0839 |
| CHSH S | 0.0800 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Solar | -0.9848 | 208.0° | no |
| Hydro | Solar | -0.9735 | 121.6° | no |
| Other Fossil | Solar | -0.9703 | 356.6° | no |
| Nuclear | Wind | -0.9480 | 351.5° | no |
| Gas | Hydro | +0.9477 | 76.0° | no |
| Coal | Hydro | +0.9457 | 16.4° | no |
| Gas | Other Fossil | +0.9449 | 132.5° | no |
| Coal | Other Fossil | +0.9448 | 63.1° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*