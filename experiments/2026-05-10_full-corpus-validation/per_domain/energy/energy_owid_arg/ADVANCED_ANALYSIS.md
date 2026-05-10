# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_arg

**Domain:** energy
**Description:** OWID primary-energy consumption composition for ARG (ARG), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: ARG

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `abd7d4587962b8e5147708bec38de0a212c6f7d460a8e54949180d4db7dd74d5`
**cnq_content_sha256:** `a7d5919a1e5f58f9b2250d153c7d0ddaceffa8a047358c4017749c16d4ff6ebb`

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
| Amplitude A | 3.1490 | Cycle amplitude |
| Damping ζ | +0.0208 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 40 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3103 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.1695 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 40 |
| Stability S_σ (global) | 0.3103 |

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
| Bearing angle range | 0.0047 to 0.4674 rad |
| Bearing angle mean | 0.0664 rad |
| Bearing pairs tested | 59 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.4991 |
| Captured step fraction (global) | 0.3570 |
| CHSH S | 0.1695 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9902 | 67.5° | no |
| Gas | Oil | +0.9431 | 12.9° | no |
| Coal | Gas | +0.9345 | 69.6° | no |
| Gas | Hydro | +0.9203 | 34.0° | no |
| Hydro | Biofuel | -0.8864 | 86.3° | no |
| Gas | Biofuel | -0.8063 | 59.3° | no |
| Coal | Wind | -0.8026 | 125.1° | no |
| Hydro | Solar | -0.8002 | 29.8° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*