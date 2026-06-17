# Financial — the system's own vector map (worked reading)

*A deterministic Hˢ reading of a financial system's composition in motion. Not statistics, not a
forecast, not advice — the vector map the composition itself generates, complementing the analysis
others have already done. Author: Peter Higgins (human authorship for claims); AI-assisted per
HUF-STD-001. Honest-broker.*

Run: `python3 run_financial.py` (numpy + stdlib; deterministic).
Input: `sp500_sectors.csv` — 252 trading days × 10 S&P 500 sector weights (parts of one whole, summing
to 1, tracked in order). Receipt: `content_hash = 5b2a32d60a32a78a32240058c58a6eed46eb8e7ffacf32ddec70406ae7227d7e`.

## What the system is doing (the reading)

- **Who is steering:** **Financials** is the loudest mover — and it is *shedding* weight. The reading
  is of the composition's own motion, not a judgement about the sector.
- **Where the weight is flowing (arrow of intent / momentum):** toward **Comm Services, Information
  Tech, Materials**; away from **Financials, Health Care, Cons Discretionary**.
- **How directed the motion is (path efficiency 0.066; coherence 0.048):** very low — this composition
  **mixes and wanders far more than it marches.** It is a diffusive system over this window, not a
  ballistic one; the mix is rebalancing, not running in a single direction.
- **How many independent things are moving (effective dimensionality 4.88):** about **five** — the ten
  sectors move in roughly five independent directions, not ten and not one.
- **Where the system reorganised (regime changes):** trading days **32, 72, 182, 209, 246** — the
  points where the composition genuinely restructured (not every wiggle; the noise-survived breaks).
- **Diagnosis, in the system's own words:** *"Financials is steering (shedding). Weight is moving
  toward Comm Services, Information Tech, Materials, Industrials, Energy. It is moving away from
  Financials, Health Care, Cons Discretionary. The mixture is steady (effective spread 7.65 → 7.66).
  The motion runs in about 5 independent directions. (8 of 10 parts have something to say.)"*

Every value is reproducible to the hash on any machine; a second reader gets the same vector map.

## What this is — and is not

This reads **how the composition moved over the supplied window**. It is **descriptive and
deterministic**: it computes no probabilities, fits no model, and predicts no price. It is **not
investment advice** and not a recommendation to buy, sell, or hold anything. What the motion *means*,
and any decision taken, remain entirely the reader's. Hˢ is not a financial advisor.

The demonstration series is a generic S&P 500 sector composition carried in the repository; swap in any
allocation/holdings/flows series (rows = dates, cols = parts summing to a whole) and the same reading
runs — see [`DATA_AND_SOURCES.md`](DATA_AND_SOURCES.md).
