# Advanced Analysis (Hˢ + CNQ v2) — geochem_qin_cpx

**Domain:** geochemistry
**Description:** Qin et al. (2024) clinopyroxene mineral spot analyses from intra-cratonic mantle xenoliths and ultramafic rocks. T = 30 top locations (>=10 spots each), D = 9 oxides (SiO2, TiO2, Al2O3, Cr2O3, FeO, CaO, MgO, MnO, Na2O — note Cr2O3 replaces K2O for clinopyroxene). Crucial test for whether the K2O-prefix in the helmsman lineage is specifically potassium or 'dominant alkali in general'.
**Citation / source:** Qin Y. et al. (2024) — Geochem Earthchem 2024-007_AVAW2Y_Qin_data

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `0c09c3d953f8a60a781ede2d7df5c089f8d31c3c9604ff70896c80b057815c12`
**cnq_content_sha256:** `71f474b33e1259447190f2a7671d099106808b0f6c348219363bbc6ffc95d8b4`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 30 | Trajectory length |
| D (carriers) | 9 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.1552 | 0 = unstable, 1 = locked |
| Amplitude A | 0.3703 | Cycle amplitude |
| Damping ζ | -0.0159 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 21 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.2500 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 21 |
| Stability S_σ (global) | 0.2500 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `reduced_or_projected` |
| D | 9 |
| Branch | `—` |
| Bearing angle range | 0.1131 to 0.8389 rad |
| Bearing angle mean | 0.3029 rad |
| Bearing pairs tested | 29 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.5892 |
| Captured step fraction (global) | 0.6185 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | MgO | +0.9619 | 4.9° | YES |
| SiO2 | CaO | +0.8670 | 3.5° | YES |
| FeO | MnO | +0.8395 | 28.3° | no |
| CaO | MgO | +0.7922 | 8.6° | YES |
| TiO2 | MgO | -0.7644 | 47.9° | no |
| SiO2 | TiO2 | -0.7613 | 39.8° | no |
| TiO2 | Cr2O3 | -0.7607 | 79.9° | no |
| FeO | Na2O | -0.7147 | 130.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*