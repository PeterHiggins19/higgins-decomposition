# Public data sources for the movers — across exchanges

*Named public sources for sector-weight / holdings compositions across the financial spectrum. Drop one
CSV per market into `data/` (rows = dates, columns = sector/holding shares summing to one) and
`run_exchanges.py` reads it automatically. Public, aggregate series only; no private or position-level
data on the repo. URLs web-checked 2026-06-16 — confirm and respect each provider's terms before bulk
download. Hˢ reads the composition; it does not redistribute the data.*

> Format: `date, Sector1, Sector2, …` with each row's sector weights summing to ~1 (or 100). Daily,
> weekly, or monthly all work. The demonstration series `data/US_SP500_sectors.csv` is a generic public
> S&P 500 ten-sector composition already in the repo.

## United States
- **S&P 500 / sector SPDRs** — State Street **Sector Tracker** + **daily holdings** files
  (ssga.com); 20-year historical sector weightings at financecharts.com (SPY). The cleanest sector-weight
  series.
- **Nasdaq-100** — Invesco QQQ holdings (invesco.com) / Nasdaq index pages; sector breakdown over time.

## Europe
- **STOXX Europe 600 / EURO STOXX 50** — STOXX / Deutsche Börse (stoxx.com) factsheets and index data;
  Yahoo Finance `^STOXX` history for the index level.
- **FTSE 100** — FTSE Russell (ftserussell.com) factsheets; iShares Core FTSE 100 (ISF) holdings for the
  sector breakdown.
- **DAX** — Deutsche Börse / iShares Core DAX holdings.

## Asia-Pacific
- **Nikkei 225 / TOPIX** — Japan Exchange Group (jpx.co.jp) and Nikkei Indexes (indexes.nikkei.co.jp);
  sector (33-industry TOPIX) weights.
- **Hang Seng** — HSI / Hang Seng Indexes (hsi.com.hk) industry weights.

## Canada
- **S&P/TSX Composite** — S&P Dow Jones Indices (spglobal.com) / TMX; iShares S&P/TSX 60 (XIU) holdings
  for sector weights.

## Cross-source helpers
- **Index constituents (current + historical):** the open `index-constituents` GitHub repo (yfiua) —
  constituents of popular indices, from which sector weights can be aggregated.
- **Index levels (any market):** Yahoo Finance / Investing.com historical download (for context, not the
  composition itself).
- **ETF holdings archives:** MasterDataReports / MasterDataCSV (third-party historical ETF holdings).

## The higher-order "study the studiers" series (per the project doctrine)
Beyond the market's own allocation, compose the **mix of the observers**: analyst sector-overweight
calls, institutional 13F sector positioning (SEC EDGAR, US), or investor-survey sentiment shares over
time. Read where the *consensus* is moving, not just the market. (Public, aggregate only.)

*Supply any of these as a shares-over-time CSV and the cross-exchange harness places it beside the others
in Compositional Character Space — same engine, same receipt.*
