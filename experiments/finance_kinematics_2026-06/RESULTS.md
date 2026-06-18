# Finance — a financial system in motion (Hˢ kinematics)

*A large financial system **is** a composition in motion: the market's weight, distributed across sectors (or asset classes), shifting over time. Hˢ kinematics reads where that weight is flowing, how committed the move is, and when the regime changed. This run **demonstrates the capability** on a sector‑weight series; for a present‑conditions market call, drop in a real sector‑weight CSV (sources below). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker. Reproduce: `python run_finance_kinematics.py [your_sector_weights.csv]`.*

---

## The read (S&P 10 GICS sectors, 252 trading days)

| Reading (navigation / physics) | Value | What it means for a market |
|---|---|---|
| **Arrow of intent / momentum — coherence** | **0.048** (very low) | the market is **churning** — rotating without a single committed direction |
| weight flowing **to** | Comm Services, Information Tech, Materials, Industrials, Energy | sectors *receiving* mass‑weighted momentum |
| weight flowing **from** | Financials, Health Care, Cons Discretionary | sectors *shedding* momentum |
| **Course directness / path efficiency** | **0.066** (≈0) | a wandering, non‑directional path — not a clean trend, lots of back‑and‑forth |
| **Degrees of freedom / effective dimensionality** | **4.88** | the rotation runs in **~5 independent factors** at once (a genuinely multi‑factor market) |
| **Waypoints / phase transitions** | 5 (days 32, 72, 182, 209, 246) | five regime changes across the window |

**Diagnosis language (the system speaking, deterministically):**
> *"Financials is steering (shedding). Weight is moving toward Comm Services, Information Tech, Materials, Industrials, Energy. It is moving away from Financials, Health Care, Cons Discretionary. The mixture is steady (effective spread 7.65 → 7.66). The motion runs in about 5 independent directions. (8 of 10 parts have something to say; the rest are quiet.)"*

A portfolio manager reads that as: *money rotating out of Financials/Health Care into Tech/Comm Services/Materials — but choppily, with no committed direction (low coherence) and five regime breaks.* The honest, low‑coherence verdict is itself the finding: **this window is a churn, not a trend.**

## Why finance fits especially well

- **It is natively compositional.** Sector weights, asset‑class allocations, factor exposures, index constituents — all are "parts of a whole" summing to 1, tracked over time. No modelling assumption needed.
- **The new reads are exactly a market's questions.** *Where is the money flowing?* (arrow of intent / momentum). *Is this a trend or a churn?* (path efficiency + momentum coherence). *When did the regime break?* (waypoints). *One factor or many?* (effective dimensionality). And it **withholds** honestly when there's no directed move — the opposite of a system that always "predicts."
- **Deterministic + receipted.** Same data → same read → same hash — auditable, the property compliance and risk desks want, and the opposite of a black‑box signal.

## Honest provenance + the real‑data path (present conditions)

The file used here is the experiment's **synthetic baseline** (`financial_sector_input.csv`), so the *capability* is what's shown, **not a market call.** For Peter's "the months under present conditions," drop in a **real sector‑weight series** — public sources:

- **SPDR Select Sector ETF holdings/weights** (the 11 S&P sector ETFs — XLK, XLF, XLV, …) — daily holdings published by State Street/SSGA.
- **S&P 500 GICS sector breakdown** (S&P Dow Jones Indices / index fact sheets).
- Or build weights from **the real price files already in `DATA/financial data/`** (SP500.csv, all_stocks_5yr.csv) by mapping tickers → GICS sector → market‑cap weights per day.
- For **asset‑class** motion: a multi‑asset allocation series (stocks/bonds/cash/commodities/REITs) — the portfolio composition in motion.

Then `run_finance_kinematics.py your_weights.csv` and the read above becomes a present‑conditions statement of where the market's weight is moving, how committed, and when it turned.

*Tier 1 on the run (the engine is exact and reproducible); the *market interpretation* is the analyst's, never the engine's; the specific sectors here are baseline data, not a live signal.*
