# Advanced Analysis (Hˢ + CNQ v2) — fao_credit_to_agriculture

**Domain:** world_bank_fao
**Description:** FAO indicator FAO_IC_23068 — Credit to Agriculture, Forestry and Fishing (USD millions). Pivoted compositional view: top-10 countries by total reporting volume, normalised so each year's row is the country-share of total recorded credit. Reveals year-by-year concentration shifts in agricultural lending.
**Citation / source:** FAO Aquastat / Credit to Agriculture indicator FAO_IC_23068; top-10 country selection by cumulative reporting volume

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `8afc845fe84ec4f3ff2b20e769143ff9779f5c478d20aa8c4bb1668cf7c89f9c`
**cnq_content_sha256:** `51480c929441308597111accad8d0e8bd3e6a1ac7929883ba3483dacf990e90d`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 28 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 4.5584 | Cycle amplitude |
| Damping ζ | +0.0610 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 20 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.2308 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 20 |
| Stability S_σ (global) | 0.2308 |

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
| Bearing angle range | 0.0018 to 2.5426 rad |
| Bearing angle mean | 0.2146 rad |
| Bearing pairs tested | 27 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.4161 |
| Captured step fraction (global) | 0.3085 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| AUS | NZL | +0.9975 | 171.4° | no |
| USA | DEU | +0.9958 | 79.4° | no |
| USA | AUS | +0.9947 | 93.7° | no |
| IND | NZL | +0.9935 | 78.3° | no |
| DEU | AUS | +0.9879 | 171.4° | no |
| USA | NZL | +0.9863 | 104.0° | no |
| IND | AUS | +0.9857 | 63.1° | no |
| DEU | NZL | +0.9811 | 164.6° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*