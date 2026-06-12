# Stage 1 Report (pure CoDa) — financial_sp500_sectors

**Domain:** financial
**Description:** S&P 500 sector-weight composition, daily for one trading year. T = 252 trading days, D = 10 GICS sectors (Information Tech, Health Care, Financials, Cons Discretionary, Comm Services, Industrials, Cons Staples, Energy, Utilities, Materials).
**Citation / source:** S&P Global GICS sector classifications applied to SP500.csv close-prices; sector weighting per S&P methodology

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:05Z
**cnt_content_sha256:** `45d6bf179dbc1511ad00c3edce6ea01fe43af3cc648ab58aab6470f1d8da9fe2`

## Input

- Source CSV: `financial_sector_input.csv`
- Source SHA-256: `b9fb10cd3fd29095...`
- Records (T): **252**
- Carriers (D): **10**
- Carriers: Information Tech, Health Care, Financials, Cons Discretionary, Comm Services, Industrials, Cons Staples, Energy, Utilities, Materials
- Closed-data SHA-256: `535bbd84a1580862...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | day_000 | 2.0349 | 2.3660 | — |
| 1 | day_001 | 2.0345 | 2.3669 | 0.0110 |
| 2 | day_002 | 2.0340 | 2.3674 | 0.0119 |
| 3 | day_003 | 2.0329 | 2.3656 | 0.0179 |
| 4 | day_004 | 2.0333 | 2.3682 | 0.0082 |
| ... | ... | ... | ... | ... |
| 249 | day_249 | 2.0359 | 2.2920 | 0.0208 |
| 250 | day_250 | 2.0355 | 2.2898 | 0.0129 |
| 251 | day_251 | 2.0367 | 2.2915 | 0.0141 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Cons Discretionary | Utilities | +0.8291 | 6.9° | YES |
| Health Care | Cons Discretionary | +0.8159 | 9.1° | YES |
| Comm Services | Materials | +0.7030 | 9.5° | YES |
| Health Care | Utilities | +0.6142 | 7.3° | YES |
| Information Tech | Energy | +0.5767 | 4.8° | YES |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Health Care | Comm Services | -0.7746 | 16.7° | no |
| Financials | Energy | -0.7974 | 4.6° | YES |
| Cons Discretionary | Materials | -0.7994 | 5.2° | YES |
| Cons Discretionary | Comm Services | -0.8588 | 28.3° | no |
| Utilities | Materials | -0.9292 | 7.9° | YES |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 45 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Information Tech | Health Care | 1.417 | 1.541 | 0.415 | 0.554 |
| Information Tech | Financials | 1.417 | 1.541 | 0.426 | 0.552 |
| Information Tech | Cons Discretionary | 1.417 | 1.541 | 0.177 | 0.306 |
| Information Tech | Comm Services | 1.417 | 1.541 | 0.171 | 0.306 |
| Information Tech | Industrials | 1.417 | 1.541 | -0.009 | 0.104 |
| Information Tech | Cons Staples | 1.417 | 1.541 | -0.244 | -0.131 |
| Information Tech | Energy | 1.417 | 1.541 | -0.630 | -0.524 |
| Information Tech | Utilities | 1.417 | 1.541 | -1.192 | -1.077 |
| Information Tech | Materials | 1.417 | 1.541 | -1.117 | -0.920 |
| Health Care | Financials | 0.415 | 0.554 | 0.426 | 0.552 |
| ... (35 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*