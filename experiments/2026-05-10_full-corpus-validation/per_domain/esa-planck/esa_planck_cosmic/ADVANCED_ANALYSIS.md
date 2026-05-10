# Advanced Analysis (Hˢ + CNQ v2) — esa_planck_cosmic

**Domain:** esa-planck
**Description:** ESA Planck cosmological energy-density composition vs redshift. T = 18 redshift bins (z = 0.0 to z = 1100), D = 5 species carriers (Dark Energy, Cold Dark Matter, Baryons, Photons, Neutrinos).
**Citation / source:** Planck 2018 cosmological parameters (Planck Collaboration); composition computed at each redshift bin per standard LCDM evolution equations

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `d8aa00837caa13b0d5916c0f6f07d07c70e4691ec0e4b602f84d48fd2680328b`
**cnq_content_sha256:** `85343567b0a8c3a6239f10008b075e1a88c9e472c528ad9b93753f8dd1e8099b`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 17 | Trajectory length |
| D (carriers) | 5 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`LIGHTLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 6.4548 | Cycle amplitude |
| Damping ζ | +0.0021 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 0 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 1.0000 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Cycles develop but eventually decay. Underlying oscillatory dynamics with weak friction.

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
| Dimension policy | `reduced_or_projected` |
| D | 5 |
| Branch | `—` |
| Bearing angle range | 0.0010 to 0.3406 rad |
| Bearing angle mean | 0.1288 rad |
| Bearing pairs tested | 16 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.8333 |
| Captured step fraction (global) | 0.8333 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Dark Energy | Neutrinos | -1.0000 | 353.3° | no |
| Dark Energy | Photons | -1.0000 | 354.1° | no |
| Photons | Neutrinos | +1.0000 | 174.2° | no |
| Cold Dark Matter | Neutrinos | +1.0000 | 87.6° | no |
| Dark Energy | Cold Dark Matter | -1.0000 | 123.3° | no |
| Cold Dark Matter | Photons | +1.0000 | 88.6° | no |
| Dark Energy | Baryons | -1.0000 | 144.5° | no |
| Baryons | Neutrinos | +1.0000 | 113.0° | no |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*