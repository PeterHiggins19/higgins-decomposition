# Advanced Analysis (Hˢ + CNQ v2) — nuclear_semf

**Domain:** nuclear
**Description:** Semi-empirical mass formula (SEMF) component decomposition across the valley of stability. T = 76 nuclides (light to heavy), D = 5 SEMF term carriers (Volume, Surface, Coulomb, Asymmetry, Pairing). The 'time' axis is nuclide ordering by Z+A; each row is one (Z, A) pair.
**Citation / source:** AME2020 nuclear masses (Wang et al. 2021); SEMF terms per Weizsäcker formula

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `61cd5824a643a0df92c590ff65d0e36ba52beb92ed3f35cb9a83921f5d169a8c`
**cnq_content_sha256:** `3cb728ba65dee46eec5f70d606912024d6a3d24d60e91db0448bb3a988a5d11f`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 76 | Trajectory length |
| D (carriers) | 5 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.8577 | Cycle amplitude |
| Damping ζ | +0.0006 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 5 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.9324 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 5 |
| Stability S_σ (global) | 0.9324 |

## Depth tower (Hˢ involution ladder)

The depth tower iterates the M operator until convergence, with each level recording its M²=I residual. Termination signals the structure of the dynamics.

**Termination:** `EXHAUSTED`

## CNQ v2 quaternion view

CNQ v2 names the algebra the trajectory lives in. For each step it computes a bearing angle (direction in CLR space, mod 2π) and a radial amplitude. The dimension policy tells you which factoring branch CNQ took for this D.

| Field | Value |
|---|---|
| Dimension policy | `reduced_or_projected` |
| D | 5 |
| Branch | `—` |
| Bearing angle range | 0.0073 to 0.2130 rad |
| Bearing angle mean | 0.0626 rad |
| Bearing pairs tested | 75 |
| Bearing max residual | 2.22e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.8369 |
| Captured step fraction (global) | 0.8966 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Surface | Asymmetry | -0.9885 | 61.0° | no |
| Surface | Pairing | +0.9389 | 46.8° | no |
| Coulomb | Pairing | -0.9270 | 75.1° | no |
| Asymmetry | Pairing | -0.8802 | 54.8° | no |
| Volume | Coulomb | +0.7885 | 64.0° | no |
| Surface | Coulomb | -0.7444 | 95.0° | no |
| Coulomb | Asymmetry | +0.6387 | 144.8° | no |
| Volume | Pairing | -0.5113 | 38.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*