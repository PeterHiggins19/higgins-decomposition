# Advanced Analysis (Hˢ + CNQ v2) — fao_value_added_agriculture

**Domain:** world_bank_fao
**Description:** FAO indicator FAO_MK_22010 — Value Added (Agriculture), USD millions. Top-10 country compositional pivot. T years × D = 10 countries; each year's row sums to 1.0 (country-share of agricultural value added among the top-10 reporting nations).
**Citation / source:** FAO Macro-Economic Indicators FAO_MK_22010; top-10 country selection by cumulative value added

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `2d34a10633925caeb305e5e0d919f18c910d4816ef308e0e4edb6882e41acf93`
**cnq_content_sha256:** `a3bdb7013d2a8d4e110460f7f40319eee672f781c128284e1f89e0d598d2b410`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 15 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`OVERDAMPED_EXTREME`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.665e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 3.4630 | Cycle amplitude |
| Damping ζ | -0.0534 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 9 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.3077 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Strong damping, the system snaps to its attractor without overshooting. Common in well-regulated, near-equilibrium dynamics.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 9 |
| Stability S_σ (global) | 0.3077 |

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
| Bearing angle range | 0.0069 to 2.7380 rad |
| Bearing angle mean | 0.5525 rad |
| Bearing pairs tested | 14 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.4377 |
| Captured step fraction (global) | 0.5143 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| TZA | PAK | +0.9991 | 147.1° | no |
| TZA | UGA | +0.9959 | 186.3° | no |
| COL | PRY | +0.9956 | 175.0° | no |
| UGA | PAK | +0.9949 | 153.6° | no |
| IRN | IND | +0.9917 | 144.1° | no |
| UZB | NGA | +0.9909 | 176.3° | no |
| IRN | PAK | -0.8206 | 193.4° | no |
| IRN | TZA | -0.8187 | 172.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*