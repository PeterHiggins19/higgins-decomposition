# Advanced Analysis (Hˢ + CNQ v2) — commodities_gold_silver

**Domain:** commodities
**Description:** Annual gold-silver mass-fraction composition normalized over both metals, 1688-2025 (T = 1338 years). D = 2 carriers — minimum compositional dimension; the engine handles D = 2 via the degenerate-pair branch.
**Citation / source:** Compiled from BoE+Bullion historical price/production records; normalized to a 2-element composition by total-mass weighting

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `bcf18e517375e80cab742fa6aa9426497846b37ea42abbd38e51df201502a15d`
**cnq_content_sha256:** `a7ec3aac561ab518e126b9e37422d70dd35f1b7fb4dd90ad403a9dfd44d671da`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 1338 | Trajectory length |
| D (carriers) | 2 | Compositional dimension |
| Termination | `FIXED_POINT` | How the depth tower closed |
| IR class | **`D2_DEGENERATE`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 0.000e+00 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.3971 | Cycle amplitude |
| Damping ζ | +0.0004 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 161 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.8795 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `degenerate_2part_bearing_only` | How CNQ v2 routes this D-value |

**IR class meaning:** (class meaning not in standard taxonomy)

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 161 |
| Stability S_σ (global) | 0.8795 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `FIXED_POINT`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `degenerate_2part_bearing_only` |
| D | 2 |
| Branch | `—` |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Gold | Silver | -1.0000 | 0.0° | YES |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*