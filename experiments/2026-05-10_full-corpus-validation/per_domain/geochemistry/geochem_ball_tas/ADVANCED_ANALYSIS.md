# Advanced Analysis (Hˢ + CNQ v2) — geochem_ball_tas

**Domain:** geochemistry
**Description:** Ball (2022) intraplate-volcanic database — major-oxide composition binned by Total-Alkali-Silica (TAS, Le Bas 1986) rock-type classification. T = 15 rock types, D = 10 oxides.
**Citation / source:** Ball M.E. et al. (2022) — Geochem Earthchem 2022-3-RY3BRK; TAS classification per Le Bas 1986

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `e6d2f7d47d3c61d1c8ef52140039847444684b5726a8c88f37169a43927dee64`
**cnq_content_sha256:** `44c409f58621d0b1f1ddddce5f69528a947bbc5d55c9c6ebe735e499f3025898`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 15 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`OVERDAMPED_EXTREME`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.7246 | Cycle amplitude |
| Damping ζ | -0.0556 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 6 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.5385 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 6 |
| Stability S_σ (global) | 0.5385 |

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
| Bearing angle range | 0.0201 to 0.1227 rad |
| Bearing angle mean | 0.0614 rad |
| Bearing pairs tested | 14 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.0573 |
| Captured step fraction (global) | 0.0521 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| MgO | Na2O | -0.9836 | 171.2° | no |
| SiO2 | Al2O3 | +0.9682 | 11.9° | no |
| CaO | MgO | +0.9409 | 176.8° | no |
| TiO2 | Na2O | -0.9354 | 354.2° | no |
| Al2O3 | Na2O | +0.9351 | 63.5° | no |
| TiO2 | MgO | +0.9327 | 346.2° | no |
| CaO | K2O | -0.9281 | 189.1° | no |
| MgO | K2O | -0.9278 | 210.6° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*