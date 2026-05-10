# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_mex

**Domain:** energy
**Description:** OWID primary-energy consumption composition for MEX (MEX), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: MEX

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `5ca8fff7ec8384a20e5639d9403da741de84cfaa4ba3b990292ba0dc0f9f41d2`
**cnq_content_sha256:** `e9d21cc16cce8ecc66a0bc795e8358c3ee55259ac0034f5557cc2f2c52a82b3e`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 60 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`OVERDAMPED_EXTREME`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 1.9626 | Cycle amplitude |
| Damping ζ | -0.0167 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 34 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.4138 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.0339 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 34 |
| Stability S_σ (global) | 0.4138 |

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
| Bearing angle range | 0.0011 to 0.2355 rad |
| Bearing angle mean | 0.0421 rad |
| Bearing pairs tested | 59 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3350 |
| Captured step fraction (global) | 0.4092 |
| CHSH S | 0.0339 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9927 | 45.8° | no |
| Gas | Hydro | +0.9907 | 49.7° | no |
| Gas | Oil | +0.9887 | 9.1° | YES |
| Coal | Oil | +0.9851 | 38.2° | no |
| Coal | Hydro | +0.9786 | 283.4° | no |
| Coal | Gas | +0.9734 | 42.7° | no |
| Oil | Wind | -0.9055 | 41.2° | no |
| Coal | Wind | -0.8851 | 108.6° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*