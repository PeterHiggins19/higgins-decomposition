# Advanced Analysis (Hˢ + CNQ v2) — financial_sp500_sectors

**Domain:** financial
**Description:** S&P 500 sector-weight composition, daily for one trading year. T = 252 trading days, D = 10 GICS sectors (Information Tech, Health Care, Financials, Cons Discretionary, Comm Services, Industrials, Cons Staples, Energy, Utilities, Materials).
**Citation / source:** S&P Global GICS sector classifications applied to SP500.csv close-prices; sector weighting per S&P methodology

**CNT engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**CNQ engine:** HCI-CNQ v2.0.0 (schema cnq/2.0.0)
**Reading:** *full Hˢ extension stack — kappa^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification — plus the CNQ v2 quaternion view: bearing trajectory, radial trajectory, dimension policy, CHSH diagnostic.*
**cnt_content_sha256:** `45d6bf179dbc1511ad00c3edce6ea01fe43af3cc648ab58aab6470f1d8da9fe2`
**cnq_content_sha256:** `0b7abe322505344198cb9f64502196d2e02194386647f09a3c6c3b8975f96249`

**Engine independence:** these two SHA-256 fingerprints are computed from disjoint engines on the same input. They are independent by design (push #32 policy); their non-identity is a *feature*, not a discrepancy.

## Headline diagnostics

| Quantity | Value | Interpretation |
|---|---|---|
| T (records) | 252 | Trajectory length |
| D (carriers) | 10 | Compositional dimension |
| Termination | `EXHAUSTED` | How the depth tower closed |
| IR class | **`CRITICALLY_DAMPED`** | Imaginary-Radius class — the Hˢ damping signature |
| M²=I residual (max) | 1.110e-16 | Metric involution check; should be at IEEE floor |
| M²=I verified | YES | < 10⁻¹⁰ floor pass |
| Attractor fitted | no | Whether a P2 cycle could be identified |
| Period | — | If fitted, the cycle length |
| Period stability | 0.0000 | 0 = unstable, 1 = locked |
| Amplitude A | 0.0305 | Cycle amplitude |
| Damping ζ | +0.0030 | Sign and magnitude of the dominant-pair damping |
| Helmsman flips | 226 | Dominant-axis transitions across the trajectory |
| Helmsman stability S_σ | 0.0960 | Global trend persistence (1 = monotone, 0 = pure noise) |
| CNQ dimension policy | `reduced_or_projected` | How CNQ v2 routes this D-value |

**IR class meaning:** Critical damping — fastest possible non-oscillatory return to equilibrium. Theoretical knife-edge.

## Helmsman family

The helmsman family decomposes the trajectory into a per-step dominant-axis signature. It surfaces structural transitions (flips) and persistence (stability_S_sigma).

| Field | Value |
|---|---|
| Total flips | 226 |
| Stability S_σ (global) | 0.0960 |

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
| Bearing angle range | 0.0004 to 0.0181 rad |
| Bearing angle mean | 0.0063 rad |
| Bearing pairs tested | 251 |
| Bearing max residual | 3.33e-16 |
| Bearing gate pass | YES |
| Captured step fraction (mean) | 0.3297 |
| Captured step fraction (global) | 0.3336 |

## Carrier-pair coherence ranking

Pairs ranked by |Pearson r| on CLR.

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Utilities | Materials | -0.9292 | 7.9° | YES |
| Cons Discretionary | Comm Services | -0.8588 | 28.3° | no |
| Cons Discretionary | Utilities | +0.8291 | 6.9° | YES |
| Health Care | Cons Discretionary | +0.8159 | 9.1° | YES |
| Cons Discretionary | Materials | -0.7994 | 5.2° | YES |
| Financials | Energy | -0.7974 | 4.6° | YES |
| Health Care | Comm Services | -0.7746 | 16.7° | no |
| Health Care | Energy | -0.7263 | 6.5° | YES |

---

*Full CNQ = the more advanced option. For the pure-CoDa view see `STAGE_1_REPORT.md`.*