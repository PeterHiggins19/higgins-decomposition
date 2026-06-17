# Cross-exchange diagnostic — the system as it stands

*Hˢ read across the movers of several exchanges, each allocation composition placed in Compositional
Character Space. One row is real and reproducible now; the rest are **staged** — the harness runs them
the moment the named public series (see [`DATA_SOURCES_EXCHANGES.md`](DATA_SOURCES_EXCHANGES.md)) are
dropped into `data/`. Honest by design: we show the framework fully and the real reading we have, and we
do not fill empty exchanges with invented numbers. Run: `python3 run_exchanges.py`. Descriptive, not
advice. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.*

## What runs today (real, reproducible)

| Exchange / index | T | D | coherence | path eff. | eff. dim | regimes | character | receipt |
|---|---:|---:|---:|---:|---:|---:|---|---|
| **US — S&P 500 sectors** | 252 | 10 | 0.048 | 0.066 | 4.88 | 5 | **Turbulent** | `5b2a32d6…` |

Reading: the US sector composition is **Turbulent** — low directedness (coherence 0.048, path efficiency
0.066) and high complexity (~5 independent directions of 10) with five dated regime changes; the weight
flows toward Communication Services and Information Technology, away from Financials and Health Care. A
rebalancing, churning system, not one marching one way. (Same classification the cross-domain character
space gives it — finance churn sits structurally beside a microbiome's, not beside a driven energy
transition.)

## Staged — ready the moment the public series are supplied

| Exchange / index | source (see DATA_SOURCES) | status |
|---|---|---|
| US — Nasdaq-100 | Invesco QQQ holdings | ⏳ supply series → auto-runs |
| Europe — STOXX 600 / EURO STOXX 50 | STOXX / Deutsche Börse | ⏳ |
| UK — FTSE 100 | FTSE Russell / iShares ISF | ⏳ |
| Germany — DAX | Deutsche Börse / iShares | ⏳ |
| Japan — Nikkei 225 / TOPIX | JPX / Nikkei Indexes | ⏳ |
| Hong Kong — Hang Seng | Hang Seng Indexes | ⏳ |
| Canada — S&P/TSX | S&P DJI / iShares XIU | ⏳ |
| Higher-order — analyst / 13F positioning | SEC EDGAR / survey shares | ⏳ |

## How to read the cross-exchange map (for an expert)

Each exchange lands somewhere on two axes the engine computes deterministically: **directedness**
(coherence + path efficiency — is the whole going somewhere, or rebalancing?) against **complexity**
(effective dimensionality — how many independent stories?). The four characters that fall out
(Ballistic, Contested, Turbulent, Diffusive) let you compare markets *structurally* — not by return, but
by how their allocation moves. Two exchanges with the same character are moving in the same *kind* of
way, whatever their prices did. That cross-exchange character map is the splash: a single, reproducible
picture of how the world's allocation systems are behaving, side by side.

## Honest envelope

The reading is Tier 1 (verified, reproducible to the hash); the meaning is Tier 3 (the expert's). This
is descriptive — no forecast, no probability, **not investment advice**. Only public, aggregate series;
private/position-level data never on the repo. The staged rows are explicitly empty until real data is
supplied — we do not estimate them.
