# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_rus

**Domain:** energy
**Description:** OWID primary-energy consumption composition for RUS (RUS), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: RUS

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `1b79a04d41d549780eda410b3db09ad2cdb71ad7b6ef665f47c6b8d9f7f99787`
**cnq_content_sha256:** `5d364bb09373678c9a8ac2e93974ff7cf8b9b2dde5db5c0dc3cfd0d6614facf5`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 40 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`OVERDAMPED_EXTREME`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 1.5535 | Cycle amplitude |
| Damping ζ | -0.0353 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 24 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3684 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.3590 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 24 |
| Stability S_σ (global) | 0.3684 |

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
| Bearing angle range | 0.0038 to 0.0781 rad |
| Bearing angle mean | 0.0304 rad |
| Bearing pairs tested | 39 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3307 |
| Captured step fraction (global) | 0.0075 |
| CHSH S | 0.3590 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Coal | Oil | +0.9963 | 9.0° | YES |
| Gas | Hydro | +0.9962 | 15.3° | no |
| Gas | Nuclear | +0.9882 | 13.6° | no |
| Nuclear | Hydro | +0.9783 | 8.2° | YES |
| Coal | Hydro | +0.9696 | 9.3° | YES |
| Hydro | Solar | -0.9672 | 15.4° | no |
| Coal | Wind | -0.9660 | 9.8° | YES |
| Oil | Wind | -0.9659 | 10.8° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*