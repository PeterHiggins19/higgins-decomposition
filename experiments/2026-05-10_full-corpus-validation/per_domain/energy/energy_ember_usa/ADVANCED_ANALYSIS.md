# Advanced Analysis (Hˢ + CNQ v2) — energy_ember_usa

**Domain:** energy
**Description:** EMBER electricity-generation-by-source for the United States, annual TWh, 2001-2025. 9 carriers (Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind).
**Citation / source:** EMBER Climate, Pipeline-ready dataset (https://ember-climate.org/data-tools/data-explorer/)

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `43ce7a49a5edc4f6d0b5278e338029ecbddab9c755ec693fb2b942b440576b09`
**cnq_content_sha256:** `5fc1f07e4d710f7279b1dc8b9bf382720792096e241fb273ddcc75c4c7bef155`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 25 | Trajectory length |
| D (carriers) | 9 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`OVERDAMPED_EXTREME`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 3.300e-13 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 9.6883 | Cycle amplitude |
| Damping ζ | -0.0843 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 8 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.6522 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 8 |
| Stability S_σ (global) | 0.6522 |

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
| Bearing angle range | 0.0139 to 0.1034 rad |
| Bearing angle mean | 0.0487 rad |
| Bearing pairs tested | 24 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1669 |
| Captured step fraction (global) | 0.0005 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Nuclear | Other Renewables | +0.9995 | 82.9° | no |
| Other Renewables | Solar | -0.9991 | 355.7° | no |
| Bioenergy | Other Renewables | +0.9983 | 154.5° | no |
| Nuclear | Solar | -0.9981 | 104.3° | no |
| Hydro | Nuclear | +0.9980 | 35.1° | no |
| Bioenergy | Nuclear | +0.9978 | 79.9° | no |
| Hydro | Other Renewables | +0.9977 | 112.2° | no |
| Bioenergy | Hydro | +0.9975 | 121.7° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*