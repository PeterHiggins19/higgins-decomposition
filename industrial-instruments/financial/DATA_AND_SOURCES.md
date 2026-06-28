# Financial — compositional data that plugs straight in

*Hˢ reads compositions: parts of a whole, tracked in order. Below are public financial series that are
already compositional (or close to it), and the higher-order "study the studiers" series that carry the
deeper reading. The repository ships one demonstration series; everything else is the user's to supply,
from public sources, in the same `rows = dates, columns = parts summing to a whole` shape.*

> Format for every series: a CSV with a date/order column, then columns that are **non-negative shares
> of one whole** (they sum to a constant — 1, 100%, or a real budget). Run with `python3 run_financial.py <file.csv>`.

## Tier A — the market's own allocation (a composition by construction)

- **Index sector weights** — e.g. S&P 500 / STOXX / TOPIX sector weightings over time (the demo here).
  Sector shares sum to 1. Public from index providers and many ETF fact sheets.
- **Asset-class allocation** — equities / bonds / cash / alternatives / real assets shares of a fund,
  endowment, or national pension over time. Public from annual reports and regulators.
- **Fund flows by category** — net assets by fund category (equity / fixed-income / money-market /
  multi-asset) as shares of the total, over time. Public from fund-industry aggregators.
- **Central-bank balance-sheet composition** — securities / loans / FX / gold as shares of total assets
  over time. Public from central-bank statistical releases.
- **Government revenue or expenditure mix** — receipts or outlays by category as shares of the total,
  over fiscal periods. Public from treasury/finance-ministry data.
- **Banking-system aggregates** — assets or liabilities by class as shares of the whole, over time.
  Public from financial-stability and regulator releases.

## Tier B — study the studiers (the higher-order composition)

The deeper reading Hˢ enables: don't read the market, read the **composition of those who study and
move it**, and see where that mix is heading.

- **Analyst/forecaster allocation** — the mix of buy/hold/sell or sector-overweight calls across the
  analysts covering a market, as shares, over time. The composition of opinion in motion.
- **Institutional positioning** — the mix of where large institutions place weight (by sector, region,
  factor) as shares, over time — the composition of the movers, not the moved.
- **Survey / sentiment composition** — the share breakdown of investor-survey responses (bullish /
  neutral / bearish, or expected-regime categories) over time.
- **Index-membership / rebalancing mix** — the composition of which constituents enter/exit and their
  weight, over rebalancing periods — how the system that *defines* the market reallocates itself.

Form any of these as a shares-over-time table and Hˢ reads whether the *system of observers* has a
direction — the structured way to see a chaotic field's heading.

## Honest notes

- Use **public, aggregate** series only; no private, client, or position-level data on the repo (the
  carrier-filter / data-is-the-star discipline). The demo series is a generic public-structure example.
- Hˢ reads motion deterministically; it is **not investment advice** and makes no forecast. The
  statistics others publish characterise the data — this complements them, never restates them.
- Not sure a series qualifies? Run [`../../COMPOSITION_GAUGE.html`](../../COMPOSITION_GAUGE.html).
