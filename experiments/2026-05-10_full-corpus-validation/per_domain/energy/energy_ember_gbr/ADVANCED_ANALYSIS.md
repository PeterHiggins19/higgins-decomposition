# Advanced Analysis (Hˢ + CNQ v2) — energy_ember_gbr

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for the United Kingdom, annual TWh, 2000-2025. 9 carriers.
**Citation / source:** EMBER Climate

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `337a6cda5bb3684284ef638c2448336749b91e5ebe0945cb9a75c2ef0d30d607`
**cnq_content_sha256:** `ecf0eddcc52c46443d516a61dac071620eb797d595867cdb092801c69338eff1`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 26 | Trajectory length |
| D (carriers) | 9 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`OVERDAMPED_EXTREME`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 2.509e-14 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 7.5047 | Cycle amplitude |
| Damping ζ | -0.0078 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 15 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3750 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 15 |
| Stability S_σ (global) | 0.3750 |

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
| Bearing angle range | 0.0294 to 0.4107 rad |
| Bearing angle mean | 0.1201 rad |
| Bearing pairs tested | 25 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3801 |
| Captured step fraction (global) | 0.0026 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gas | Other Fossil | +0.9959 | 39.0° | no |
| Hydro | Other Fossil | +0.9947 | 343.0° | no |
| Gas | Nuclear | +0.9947 | 10.0° | no |
| Nuclear | Other Fossil | +0.9919 | 41.1° | no |
| Hydro | Nuclear | +0.9910 | 56.6° | no |
| Gas | Hydro | +0.9910 | 49.5° | no |
| Bioenergy | Hydro | +0.9592 | 76.4° | no |
| Bioenergy | Other Fossil | +0.9434 | 52.6° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*