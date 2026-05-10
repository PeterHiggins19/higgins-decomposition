# Advanced Analysis (Hˢ + CNQ v2) — geochem_stracke_oib

**Domain:** geochemistry
**Description:** Stracke (2022) ocean island basalt (OIB) major-oxide composition, binned by location (top 15 locations by sample count, including Galapagos, Iceland, Hawaii, Tristan da Cunha, etc.). T = 15, D = 10 oxides.
**Citation / source:** Stracke A. (2022) — Geochem Earthchem 2022_09-0SVW6S_Stracke_data (OIB subset)

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `2cb0b919f9c33ea789717988573235c52c75e0597df653ce3512c46b83bbd2db`
**cnq_content_sha256:** `15d3d26c4be8c5356f7406fe0a8bf108f43653d1f8a418abe47a9ccfb88371d7`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 15 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.1268 | 0 = unstable, 1 = locked |
| Amplitude A | 0.3290 | Cycle amplitude |
| Damping ζ | -0.0083 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 8 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3846 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 8 |
| Stability S_σ (global) | 0.3846 |

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
| Bearing angle range | 0.0256 to 0.2493 rad |
| Bearing angle mean | 0.1174 rad |
| Bearing pairs tested | 14 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1188 |
| Captured step fraction (global) | 0.1154 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | Al2O3 | +0.9708 | 5.6° | YES |
| TiO2 | Al2O3 | -0.9521 | 20.2° | no |
| Al2O3 | P2O5 | -0.9440 | 7.3° | YES |
| SiO2 | TiO2 | -0.9318 | 13.3° | no |
| SiO2 | P2O5 | -0.9237 | 12.8° | no |
| TiO2 | P2O5 | +0.8975 | 14.5° | no |
| CaO | K2O | -0.8843 | 82.7° | no |
| MgO | K2O | -0.8797 | 245.2° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*