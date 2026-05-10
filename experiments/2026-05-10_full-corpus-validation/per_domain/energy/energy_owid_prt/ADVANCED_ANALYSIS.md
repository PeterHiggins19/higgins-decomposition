# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_prt

**Domain:** energy
**Description:** OWID primary-energy consumption composition for PRT (PRT), annual TWh. T = 36 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: PRT

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `0905ad024f099ed8a0b1c60139e66c5afd5141f0b1ebca877771001f76361459`
**cnq_content_sha256:** `7ca9580338c7c4a7bc377c163463b47c0454d144080a7d82401a5273325bcebc`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 36 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 2.776e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 4.2107 | Cycle amplitude |
| Damping ζ | +0.0138 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 17 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.5000 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 0.7429 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 17 |
| Stability S_σ (global) | 0.5000 |

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
| Bearing angle range | 0.0002 to 0.5983 rad |
| Bearing angle mean | 0.0483 rad |
| Bearing pairs tested | 35 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1968 |
| Captured step fraction (global) | 0.4163 |
| CHSH S | 0.7429 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9994 | 41.5° | no |
| Nuclear | Hydro | +0.9839 | 47.2° | no |
| Oil | Hydro | +0.9805 | 21.0° | no |
| Nuclear | Wind | -0.8968 | 359.3° | no |
| Oil | Wind | -0.8960 | 50.9° | no |
| Coal | Solar | -0.8950 | 220.2° | no |
| Hydro | Wind | -0.8948 | 82.1° | no |
| Coal | Oil | +0.8364 | 86.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*