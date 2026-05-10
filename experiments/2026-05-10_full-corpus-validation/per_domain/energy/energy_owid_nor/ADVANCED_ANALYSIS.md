# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_nor

**Domain:** energy
**Description:** OWID primary-energy consumption composition for NOR (NOR), annual TWh. T = 48 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: NOR

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `810c4ce5a740b0ede3943dae639608dc95b3d4985c72457fff99627c01fb3450`
**cnq_content_sha256:** `83db95cf207a0a564c807dfb59f7597c6fa90033f737575979c051c7e2cfaa46`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 48 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.1168 | Cycle amplitude |
| Damping ζ | +0.0240 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 27 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.4130 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.0426 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 27 |
| Stability S_σ (global) | 0.4130 |

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
| Bearing angle range | 0.0029 to 0.0392 rad |
| Bearing angle mean | 0.0109 rad |
| Bearing pairs tested | 47 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3866 |
| Captured step fraction (global) | 0.0182 |
| CHSH S | 0.0426 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Hydro | +0.9996 | 29.5° | no |
| Oil | Nuclear | +0.9973 | 33.2° | no |
| Coal | Oil | +0.9961 | 26.5° | no |
| Oil | Hydro | +0.9954 | 6.9° | YES |
| Coal | Nuclear | +0.9950 | 36.1° | no |
| Coal | Hydro | +0.9932 | 25.4° | no |
| Coal | Wind | -0.9481 | 132.6° | no |
| Oil | Wind | -0.9432 | 75.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*