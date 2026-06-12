# Advanced Analysis (Hˢ + CNQ v2) — geochem_tappe_kim1

**Domain:** geochemistry
**Description:** Tappe et al. (2024) Kimberlite Group-1 bulk rock major-oxide composition, binned by country/region. T = 8 countries, D = 10 oxides. Kimberlites are intra-cratonic mantle-derived ultrapotassic rocks; K2O is typically very high (>3% on mass basis).
**Citation / source:** Tappe S. et al. (2024) — Geochem Earthchem 2022-2-FLV19S_Tappe_data_v2024

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `e0f8ea0b1ca06df3b92c3649d3a4d7f7f070461b38f83f4ac3661b151bdc0ca2`
**cnq_content_sha256:** `d27a993f25cf48a2e8e01cccd75e2633d050e4661e8ada69ce1686c8e9f266a6`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 8 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.4697 | 0 = unstable, 1 = locked |
| Amplitude A | 0.5492 | Cycle amplitude |
| Damping ζ | +0.2340 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 4 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3333 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 4 |
| Stability S_σ (global) | 0.3333 |

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
| Bearing angle range | 0.0724 to 0.5344 rad |
| Bearing angle mean | 0.3968 rad |
| Bearing pairs tested | 7 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3785 |
| Captured step fraction (global) | 0.2951 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | MgO | +0.9373 | 2.0° | YES |
| CaO | K2O | -0.8868 | 39.1° | no |
| SiO2 | Al2O3 | +0.8387 | 13.4° | no |
| TiO2 | Al2O3 | -0.8270 | 224.5° | no |
| SiO2 | TiO2 | -0.8172 | 33.1° | no |
| TiO2 | MgO | -0.7904 | 32.6° | no |
| K2O | Na2O | -0.7830 | 41.8° | no |
| Al2O3 | FeO | -0.7126 | 30.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*