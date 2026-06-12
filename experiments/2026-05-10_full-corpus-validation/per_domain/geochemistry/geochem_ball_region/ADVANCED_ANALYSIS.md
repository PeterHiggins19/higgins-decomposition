# Advanced Analysis (Hˢ + CNQ v2) — geochem_ball_region

**Domain:** geochemistry
**Description:** Ball (2022) intraplate-volcanic database — major-oxide composition binned by geographic Region (95 regions retained at min n=10 per region). T = 95, D = 10 oxides.
**Citation / source:** Ball M.E. et al. (2022) — Geochem Earthchem 2022-3-RY3BRK; region binning per source metadata

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `2d655b532e5e45ee96cbcbef075ddd853ae46722fc8b8b82413da4546f414af7`
**cnq_content_sha256:** `e9e446146804987335f6352a733e0636d763aaeece77171da9644ee351dd4003`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 95 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.2068 | 0 = unstable, 1 = locked |
| Amplitude A | 0.5647 | Cycle amplitude |
| Damping ζ | -0.0002 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 58 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3763 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 58 |
| Stability S_σ (global) | 0.3763 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `reduced_or_projected` |
| D | 10 |
| Branch | `—` |
| Bearing angle range | 0.0121 to 0.3511 rad |
| Bearing angle mean | 0.0979 rad |
| Bearing pairs tested | 94 |
| Bearing max residual | 4.44e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1587 |
| Captured step fraction (global) | 0.0611 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | Al2O3 | +0.8956 | 9.5° | YES |
| CaO | MnO | -0.8679 | 250.9° | no |
| FeO | K2O | -0.7846 | 88.6° | no |
| SiO2 | P2O5 | -0.7138 | 17.8° | no |
| FeO | P2O5 | -0.6557 | 18.9° | no |
| MgO | Na2O | -0.6155 | 221.1° | no |
| Al2O3 | Na2O | +0.6094 | 47.1° | no |
| Al2O3 | P2O5 | -0.6027 | 17.1° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*