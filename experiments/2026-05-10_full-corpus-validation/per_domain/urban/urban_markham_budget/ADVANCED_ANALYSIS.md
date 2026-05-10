# Advanced Analysis (Hˢ + CNQ v2) — urban_markham_budget

**Domain:** urban
**Description:** City of Markham (Ontario) operating budget composition, fiscal years 2011-2025. T = 15 fiscal years, D = 8 budget category carriers (Operations & Asset Mgmt, Public Safety, Planning & Building, Recreation & Culture, Library & Heritage, Engineering & Capital, Corporate Services, Council & Administration).
**Citation / source:** City of Markham annual budget reports (compiled from public budget documents)

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `27f20ce2d5611f695825e61666f9569de52501cc3273abdb8b55679d2e409e1e`
**cnq_content_sha256:** `5ab71065e3b6800153391392b5ced8ae2c09e9fdf36a29c6280036716a916a35`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 15 | Trajectory length |
| D (carriers) | 8 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`MODERATELY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 2.776e-17 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.2852 | Cycle amplitude |
| Damping ζ | -0.0009 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 0 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 1.0000 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CHSH S | 2.0000 | Joint-coherence diagnostic; classical bound 2.0, Tsirelson 2√2 |
| CNQ dimension policy | `twin_quaternion_native` | How CNQ v2 routes this D-value |

**IR class meaning:** Damping is present but cycles can develop. Intermediate regime.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 0 |
| Stability S_σ (global) | 1.0000 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `twin_quaternion_native` |
| D | 8 |
| Branch | `—` |
| Bearing angle range | 0.0300 to 0.0357 rad |
| Bearing angle mean | 0.0333 rad |
| Bearing pairs tested | 14 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.1270 |
| Captured step fraction (global) | 0.1131 |
| CHSH S | 2.0000 |
| CHSH classical bound | 2.0 |
| CHSH Tsirelson bound | 2.8284 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Public Safety | Engineering & Capital | +1.0000 | 39.9° | no |
| Planning & Building | Corporate Services | -0.9995 | 340.0° | no |
| Public Safety | Council & Administration | -0.9995 | 16.6° | no |
| Engineering & Capital | Council & Administration | -0.9992 | 25.0° | no |
| Library & Heritage | Council & Administration | +0.9990 | 0.5° | YES |
| Planning & Building | Engineering & Capital | +0.9975 | 342.9° | no |
| Public Safety | Library & Heritage | -0.9971 | 19.1° | no |
| Public Safety | Planning & Building | +0.9968 | 32.4° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*