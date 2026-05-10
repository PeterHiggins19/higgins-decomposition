# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_che

**Domain:** energy
**Description:** OWID primary-energy consumption composition for CHE (CHE), annual TWh. T = 56 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: CHE

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `6f33b3b9f698fd0c21f28fc4823f7e5f14251c2ef6eac293725d2129b0c1bf9a`
**cnq_content_sha256:** `b8bd51d0458af5fc16b9419aa5e22bf0ded823aef90b14fc554dac4d7a2ea624`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 56 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.6454 | Cycle amplitude |
| Damping ζ | +0.0152 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 30 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.4444 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.4727 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 30 |
| Stability S_σ (global) | 0.4444 |

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
| Bearing angle range | 0.0056 to 0.2965 rad |
| Bearing angle mean | 0.0524 rad |
| Bearing pairs tested | 55 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3587 |
| Captured step fraction (global) | 0.3644 |
| CHSH S | 0.4727 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Hydro | +0.9959 | 5.2° | YES |
| Coal | Oil | +0.9809 | 81.3° | no |
| Coal | Hydro | +0.9796 | 83.7° | no |
| Coal | Solar | -0.9473 | 356.8° | no |
| Oil | Solar | -0.9383 | 57.6° | no |
| Hydro | Solar | -0.9314 | 60.1° | no |
| Nuclear | Biofuel | -0.9249 | 25.8° | no |
| Hydro | Wind | -0.9096 | 17.8° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*