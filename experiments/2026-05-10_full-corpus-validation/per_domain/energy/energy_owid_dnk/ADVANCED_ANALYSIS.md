# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_dnk

**Domain:** energy
**Description:** OWID primary-energy consumption composition for DNK (DNK), annual TWh. T = 47 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: DNK

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `05c343b7738640f0bd4982c652b9f0b14da4709dd10dcba734125a038889bcaa`
**cnq_content_sha256:** `a2393711fef00dbd9a89d540bb68468f6d166b9316a599f840757801b5f08305`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 47 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 1.9079 | Cycle amplitude |
| Damping ζ | +0.0529 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 29 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3556 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.6087 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 29 |
| Stability S_σ (global) | 0.3556 |

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
| Bearing angle range | 0.0029 to 0.4488 rad |
| Bearing angle mean | 0.0330 rad |
| Bearing pairs tested | 46 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.2794 |
| Captured step fraction (global) | 0.4659 |
| CHSH S | 0.6087 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9981 | 42.0° | no |
| Nuclear | Hydro | +0.9943 | 356.6° | no |
| Oil | Hydro | +0.9931 | 54.7° | no |
| Coal | Nuclear | +0.9747 | 53.4° | no |
| Coal | Hydro | +0.9683 | 83.4° | no |
| Coal | Oil | +0.9615 | 28.5° | no |
| Coal | Solar | -0.8765 | 104.4° | no |
| Solar | Biofuel | +0.8736 | 340.8° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*