# Advanced Analysis (Hˢ + CNQ v2) — energy_ember_chn

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for China, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `de35a9b5d6193809d84e0614b3405112ec9b88a64fda60b1d0941d1e5c892bb6`
**cnq_content_sha256:** `4cba53a4717dd95f0d7f54330813e77c103d992318ecd3f2956072888601d73a`

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
| Amplitude A | 0.9415 | Cycle amplitude |
| Damping ζ | +0.0324 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 12 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.5000 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.8800 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

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
| Dimension policy | `twin_quaternion_native` |
| D | 8 |
| Branch | `—` |
| Bearing angle range | 0.0078 to 0.0727 rad |
| Bearing angle mean | 0.0356 rad |
| Bearing pairs tested | 25 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1928 |
| Captured step fraction (global) | 0.1425 |
| CHSH S | 0.8800 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Hydro | +0.9941 | 16.1° | no |
| Coal | Solar | -0.9914 | 66.7° | no |
| Other Fossil | Wind | -0.9866 | 359.1° | no |
| Hydro | Solar | -0.9840 | 100.7° | no |
| Nuclear | Wind | -0.9375 | 347.8° | no |
| Hydro | Wind | -0.9191 | 75.7° | no |
| Coal | Wind | -0.9190 | 43.5° | no |
| Coal | Other Fossil | +0.9145 | 61.9° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*