# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_tkm

**Domain:** energy
**Description:** OWID primary-energy consumption composition for TKM (TKM), annual TWh. T = 26 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: TKM

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `8ccee34829b5754c4fbc7ca817f67e847b7cd8346a21a5f8b3abebff26b84c13`
**cnq_content_sha256:** `5c48a411dcf852b1fee80c2ef25cd078e97afe7e87f59447103f565961ff50bc`

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
| Amplitude A | 0.7360 | Cycle amplitude |
| Damping ζ | +0.0274 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 9 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.6250 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.2400 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 9 |
| Stability S_σ (global) | 0.6250 |

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
| Bearing angle range | 0.0005 to 0.5723 rad |
| Bearing angle mean | 0.0541 rad |
| Bearing pairs tested | 25 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.5147 |
| Captured step fraction (global) | 0.8255 |
| CHSH S | 0.2400 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Wind | +1.0000 | 0.0° | YES |
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Wind | Biofuel | +1.0000 | 0.0° | YES |
| Gas | Nuclear | +0.9900 | 10.6° | no |
| Gas | Wind | +0.9900 | 10.6° | no |
| Gas | Biofuel | +0.9900 | 10.6° | no |
| Coal | Nuclear | -0.9786 | 90.6° | no |
| Coal | Wind | -0.9786 | 90.6° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*