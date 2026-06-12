# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_hrv

**Domain:** energy
**Description:** OWID primary-energy consumption composition for HRV (HRV), annual TWh. T = 35 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: HRV

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `e54816db3185928f2f5b9f3d7a95397c8dc521154d3535e48f82da84ad8d7ed9`
**cnq_content_sha256:** `9aedad6a95d6595cdf3cc602bdf7f723234d79d871a584d57ec910e9361214cd`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 35 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 2.5942 | Cycle amplitude |
| Damping ζ | +0.0102 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 16 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.5152 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.3529 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 16 |
| Stability S_σ (global) | 0.5152 |

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
| Bearing angle range | 0.0036 to 0.0646 rad |
| Bearing angle mean | 0.0172 rad |
| Bearing pairs tested | 34 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.2436 |
| Captured step fraction (global) | 0.0115 |
| CHSH S | 0.3529 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9992 | 31.8° | no |
| Gas | Nuclear | +0.9984 | 30.4° | no |
| Gas | Oil | +0.9967 | 4.2° | YES |
| Nuclear | Hydro | +0.9920 | 32.5° | no |
| Oil | Hydro | +0.9882 | 7.2° | YES |
| Gas | Hydro | +0.9879 | 7.2° | YES |
| Coal | Gas | +0.9540 | 22.3° | no |
| Coal | Nuclear | +0.9532 | 34.9° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*