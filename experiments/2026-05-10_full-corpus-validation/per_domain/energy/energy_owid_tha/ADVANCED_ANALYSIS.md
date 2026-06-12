# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_tha

**Domain:** energy
**Description:** OWID primary-energy consumption composition for THA (THA), annual TWh. T = 44 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: THA

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `f20fb6e37ce174bacc19abbfd07aa4ba58ef24bd31e922714d9942b8b4cbece1`
**cnq_content_sha256:** `72a6ac2f2840177a5e181d7526c5683bd68c590cac6f3f8ab3345f443b7d119a`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 44 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.2962 | Cycle amplitude |
| Damping ζ | +0.0069 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 25 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.4048 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.3256 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 25 |
| Stability S_σ (global) | 0.4048 |

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
| Bearing angle range | 0.0007 to 0.1300 rad |
| Bearing angle mean | 0.0118 rad |
| Bearing pairs tested | 43 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1920 |
| Captured step fraction (global) | 0.0504 |
| CHSH S | 0.3256 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9980 | 33.3° | no |
| Oil | Hydro | +0.9863 | 39.6° | no |
| Nuclear | Solar | -0.9847 | 44.2° | no |
| Nuclear | Hydro | +0.9804 | 359.8° | no |
| Oil | Solar | -0.9790 | 43.9° | no |
| Coal | Nuclear | +0.9733 | 30.5° | no |
| Coal | Gas | +0.9711 | 14.7° | no |
| Coal | Solar | -0.9693 | 49.9° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*