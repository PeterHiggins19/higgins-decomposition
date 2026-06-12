# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_bel

**Domain:** energy
**Description:** OWID primary-energy consumption composition for BEL (BEL), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: BEL

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `6c2d9abc29777d41b7e43e6e36dce93ddeb9d7c299d47fc0035983b3ee016fd6`
**cnq_content_sha256:** `5a90cdebba60eb1f60962a42382f0dade0d9c6bcbcf4e75a69ecf21904247759`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 60 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.8150 | Cycle amplitude |
| Damping ζ | +0.0194 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 30 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.4828 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.0339 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 30 |
| Stability S_σ (global) | 0.4828 |

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
| Bearing angle range | 0.0164 to 0.3223 rad |
| Bearing angle mean | 0.1009 rad |
| Bearing pairs tested | 59 |
| Bearing max residual | 4.44e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3465 |
| Captured step fraction (global) | 0.4475 |
| CHSH S | 0.0339 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9920 | 47.2° | no |
| Coal | Hydro | +0.9864 | 107.5° | no |
| Oil | Hydro | +0.9806 | 73.8° | no |
| Solar | Biofuel | +0.9461 | 42.8° | no |
| Gas | Solar | -0.8937 | 52.8° | no |
| Coal | Wind | -0.8890 | 187.7° | no |
| Oil | Wind | -0.8684 | 56.0° | no |
| Hydro | Wind | -0.8618 | 358.7° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*