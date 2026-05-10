# Advanced Analysis (Hˢ + CNQ v2) — energy_owid_mkd

**Domain:** energy
**Description:** OWID primary-energy consumption composition for MKD (MKD), annual TWh. T = 27 years, D = 8 carriers (Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biofuel). Distinct from the EMBER electricity-generation dataset: this is total primary-energy consumption across all end uses.
**Citation / source:** Our World in Data — owid-energy-data.csv (compiled from BP Statistical Review, IEA, EIA); country: MKD

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `07d3f44f3ba3bd9c7c6b3a79da009c7cadd9ac0b07364f0bdede1242dfe81d90`
**cnq_content_sha256:** `4a3c2b3766e36ed3f240f199d8efcfda6e216650ac4ce81e093c356d729eb915`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 27 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.3157 | Cycle amplitude |
| Damping ζ | +0.0289 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 16 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3600 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 1.2308 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 16 |
| Stability S_σ (global) | 0.3600 |

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
| Bearing angle range | 0.0027 to 0.0564 rad |
| Bearing angle mean | 0.0213 rad |
| Bearing pairs tested | 26 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.2254 |
| Captured step fraction (global) | 0.0146 |
| CHSH S | 1.2308 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Oil | Nuclear | +0.9987 | 27.4° | no |
| Coal | Nuclear | +0.9973 | 32.6° | no |
| Coal | Oil | +0.9935 | 7.6° | YES |
| Nuclear | Hydro | +0.9795 | 29.3° | no |
| Oil | Hydro | +0.9764 | 9.7° | YES |
| Coal | Hydro | +0.9729 | 7.0° | YES |
| Coal | Solar | -0.9383 | 64.5° | no |
| Nuclear | Solar | -0.9375 | 356.8° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*