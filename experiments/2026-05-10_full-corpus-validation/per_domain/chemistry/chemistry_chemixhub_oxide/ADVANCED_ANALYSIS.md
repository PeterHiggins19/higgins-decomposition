# Advanced Analysis (Hˢ + CNQ v2) — chemistry_chemixhub_oxide

**Domain:** chemistry
**Description:** Chemixhub oxide compositional samples — synthetic-style mineral oxide compositions across 25 catalogued samples; D = 7 oxide carriers.
**Citation / source:** ChemixHub project, github.com/chemixhub (oxide composition subset)

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `e59d789783ebdf0d68ecd7826f396b24c37f52587a38956c752715387b5ce2e4`
**cnq_content_sha256:** `d3c4ca5cc4c697d24512c475990b18ec65d57f19739840c14653711bf6ed1b07`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 24 | Trajectory length |
| D (carriers) | 7 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 5.551e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.1751 | Cycle amplitude |
| Damping ζ | -0.0089 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 9 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.5909 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 9 |
| Stability S_σ (global) | 0.5909 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `reduced_or_projected` |
| D | 7 |
| Branch | `—` |
| Bearing angle range | 0.0158 to 0.0588 rad |
| Bearing angle mean | 0.0321 rad |
| Bearing pairs tested | 23 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.5754 |
| Captured step fraction (global) | 0.6027 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Al2O3 | CaO | +0.9520 | 35.2° | no |
| Fe2O3 | CaO | -0.8873 | 112.1° | no |
| SiO2 | TiO2 | -0.8015 | 10.5° | no |
| Al2O3 | Fe2O3 | -0.7533 | 46.7° | no |
| MgO | CaO | -0.6779 | 65.7° | no |
| Al2O3 | MgO | -0.6327 | 29.2° | no |
| Al2O3 | Na2O | -0.6054 | 15.3° | no |
| TiO2 | MgO | +0.5638 | 16.6° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*