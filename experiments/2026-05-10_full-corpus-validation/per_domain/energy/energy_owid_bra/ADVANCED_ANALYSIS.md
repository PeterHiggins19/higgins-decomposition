# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_bra

**Domain:** energy
**Description:** OWID primary-energy consumption composition for BRA (BRA), annual TWh. T = 60 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: BRA

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `c437249c7fb82ba2791c338a4fdfdea6c3109d899246e9e2156010fe7dd10613`
**cnq_content_sha256:** `8d6953a8bc9a0971ae78a823e5c31cf376269a63c4f689dc9aa4bc45163bddfe`

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
| Amplitude A | 3.5534 | Cycle amplitude |
| Damping ζ | -0.0091 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 20 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.6552 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.2373 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 20 |
| Stability S_σ (global) | 0.6552 |

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
| Bearing angle range | 0.0030 to 0.4699 rad |
| Bearing angle mean | 0.0613 rad |
| Bearing pairs tested | 59 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3818 |
| Captured step fraction (global) | 0.4127 |
| CHSH S | 0.2373 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Hydro | +0.9963 | 64.7° | no |
| Oil | Hydro | +0.9907 | 6.3° | YES |
| Coal | Oil | +0.9896 | 56.3° | no |
| Gas | Solar | -0.7965 | 13.7° | no |
| Hydro | Wind | -0.7889 | 60.1° | no |
| Coal | Wind | -0.7803 | 157.2° | no |
| Oil | Wind | -0.7258 | 59.2° | no |
| Oil | Nuclear | -0.7137 | 61.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*