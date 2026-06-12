# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_sau

**Domain:** energy
**Description:** OWID primary-energy consumption composition for SAU (SAU), annual TWh. T = 17 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: SAU

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `f77f5d9d633c250f26b79a569aa115e3125427e8d6ede02cfac8c7748422eb6d`
**cnq_content_sha256:** `dd75fcf53d82aef653bc33efd0dd866e4d507534fda14b9dac0341558726b284`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 17 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.2305 | Cycle amplitude |
| Damping ζ | -0.0030 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 7 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.5333 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.0000 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 7 |
| Stability S_σ (global) | 0.5333 |

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
| Bearing angle range | 0.0054 to 0.0781 rad |
| Bearing angle mean | 0.0228 rad |
| Bearing pairs tested | 16 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3176 |
| Captured step fraction (global) | 0.0626 |
| CHSH S | 0.0000 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Hydro | +1.0000 | 0.0° | YES |
| Nuclear | Biofuel | +1.0000 | 0.0° | YES |
| Hydro | Biofuel | +1.0000 | 0.0° | YES |
| Oil | Nuclear | +0.9994 | 17.4° | no |
| Oil | Hydro | +0.9994 | 17.4° | no |
| Oil | Biofuel | +0.9994 | 17.4° | no |
| Gas | Nuclear | +0.9975 | 18.0° | no |
| Gas | Hydro | +0.9975 | 18.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*