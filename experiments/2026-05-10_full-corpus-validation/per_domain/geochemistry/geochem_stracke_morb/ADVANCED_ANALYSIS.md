# Advanced Analysis (Hˢ + CNQ v2) — geochem_stracke_morb

**Domain:** geochemistry
**Description:** Stracke MORB (mid-ocean ridge basalt) major-oxide composition, by ocean basin. T = 5 locations, D = 10 oxide carriers (SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5).
**Citation / source:** Stracke A. (2022) — Geochem Earthchem 2022_09-0SVW6S

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `017ed5dcd2afb80ff6b8eba210bf44c8c5b4327ec47c35d37bdc3ea4afedd8f8`
**cnq_content_sha256:** `c396acf234e086d96385e6ee919fdc96f7fdaaad568ab8fa6b185e4e052971c6`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 5 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`CRITICALLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.0000 | Cycle amplitude |
| Damping ζ | +0.0000 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 3 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.0000 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Critical damping — fastest possible non-oscillatory return to equilibrium. Theoretical knife-edge.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 3 |
| Stability S_σ (global) | 0.0000 |

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
| Bearing angle range | 0.0392 to 0.1240 rad |
| Bearing angle mean | 0.1010 rad |
| Bearing pairs tested | 4 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.2043 |
| Captured step fraction (global) | 0.1068 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| SiO2 | CaO | +0.9884 | 4.0° | YES |
| SiO2 | MgO | +0.9851 | 7.5° | YES |
| MgO | K2O | -0.9779 | 8.8° | YES |
| Na2O | P2O5 | -0.9679 | 4.8° | YES |
| CaO | MgO | +0.9590 | 8.4° | YES |
| SiO2 | Al2O3 | +0.9536 | 1.1° | YES |
| Al2O3 | CaO | +0.9523 | 4.1° | YES |
| SiO2 | K2O | -0.9495 | 20.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*