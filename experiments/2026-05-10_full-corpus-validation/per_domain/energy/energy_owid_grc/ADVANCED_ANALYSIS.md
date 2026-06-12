# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_grc

**Domain:** energy
**Description:** OWID primary-energy consumption composition for GRC (GRC), annual TWh. T = 43 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: GRC

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `435add9c71eec931c33e2ebefeb80ece950bdd7e0d3b8f3339fc67cc6e313729`
**cnq_content_sha256:** `ceb3765d0bb4e137994e9e714370b5871b0af870b6ae1eb3eb53a58ea5fc1ab2`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 43 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`OVERDAMPED_EXTREME`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 2.9088 | Cycle amplitude |
| Damping ζ | -0.0110 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 24 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.4146 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.2857 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 24 |
| Stability S_σ (global) | 0.4146 |

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
| Bearing angle range | 0.0008 to 0.1104 rad |
| Bearing angle mean | 0.0204 rad |
| Bearing pairs tested | 42 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.2200 |
| Captured step fraction (global) | 0.0569 |
| CHSH S | 0.2857 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9998 | 35.8° | no |
| Nuclear | Hydro | +0.9827 | 40.4° | no |
| Oil | Hydro | +0.9818 | 27.0° | no |
| Coal | Nuclear | +0.9800 | 47.6° | no |
| Coal | Oil | +0.9794 | 31.3° | no |
| Coal | Hydro | +0.9658 | 22.0° | no |
| Coal | Solar | -0.9139 | 121.8° | no |
| Oil | Solar | -0.9016 | 74.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*