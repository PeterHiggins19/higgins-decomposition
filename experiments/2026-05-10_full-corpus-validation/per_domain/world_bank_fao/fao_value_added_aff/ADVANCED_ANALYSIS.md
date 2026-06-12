# Advanced Analysis (Hˢ + CNQ v2) — fao_value_added_aff

**Domain:** world_bank_fao
**Description:** FAO indicator FAO_MK_22016 — Value Added in Agriculture, Forestry and Fishing. Top-10 country compositional pivot, 1970-2024 (T = 55 years).
**Citation / source:** FAO Macro-Economic Indicators FAO_MK_22016; top-10 country selection

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `6f3d795a3c980326f28e214557b5899023e0455338ef9d0d7633652420e6f543`
**cnq_content_sha256:** `3f9dcf10da70ee2294d5e56032417f46ff529de07ab217345a445756c0131b45`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 55 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 2.220e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.6892 | Cycle amplitude |
| Damping ζ | -0.0231 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 33 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3774 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 33 |
| Stability S_σ (global) | 0.3774 |

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
| Bearing angle range | 0.0029 to 0.1509 rad |
| Bearing angle mean | 0.0446 rad |
| Bearing pairs tested | 54 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.4141 |
| Captured step fraction (global) | 0.6325 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| COL | KOR | +0.9905 | 238.3° | no |
| IDN | IND | +0.9774 | 67.8° | no |
| KOR | IND | +0.9611 | 176.2° | no |
| VNM | UGA | +0.9495 | 123.6° | no |
| COL | IND | +0.9417 | 184.1° | no |
| IDN | KOR | +0.9348 | 86.0° | no |
| UZB | COL | -0.9294 | 358.2° | no |
| IDN | VNM | -0.9229 | 69.3° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*