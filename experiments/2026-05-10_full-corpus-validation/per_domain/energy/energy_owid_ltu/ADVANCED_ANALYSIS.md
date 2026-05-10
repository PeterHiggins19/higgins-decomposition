# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_ltu

**Domain:** energy
**Description:** OWID primary-energy consumption composition for LTU (LTU), annual TWh. T = 40 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: LTU

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `9b08a0af95d75960092d299d4de04e8635bf04298258fcfad79867aee4c0a9f4`
**cnq_content_sha256:** `421162e2ecc89a1569fa2f65ef7c7d7e6f1eb686bd79f8ad67c6ae0489ea5fe5`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 40 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 2.220e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.3794 | Cycle amplitude |
| Damping ζ | +0.0207 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 20 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.4737 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.3590 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 20 |
| Stability S_σ (global) | 0.4737 |

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
| Bearing angle range | 0.0027 to 1.7217 rad |
| Bearing angle mean | 0.1141 rad |
| Bearing pairs tested | 39 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.4023 |
| Captured step fraction (global) | 0.6266 |
| CHSH S | 0.3590 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Wind | Biofuel | +0.9819 | 201.7° | no |
| Gas | Oil | +0.9561 | 8.1° | YES |
| Coal | Oil | +0.9482 | 33.3° | no |
| Nuclear | Wind | -0.9399 | 230.8° | no |
| Oil | Biofuel | -0.9338 | 62.8° | no |
| Gas | Hydro | +0.9295 | 25.7° | no |
| Coal | Gas | +0.9176 | 36.8° | no |
| Oil | Hydro | +0.9076 | 22.9° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*