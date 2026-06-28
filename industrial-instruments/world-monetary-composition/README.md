# World monetary composition — the world economy read as a moving composition (INTERNAL · STUDY)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑25. A **proper,
real‑data, no‑estimate** Hˢ study of how the composition of the world's economic weight — the backing of the
monetary systems — moves, churns, and concentrates over time. Deterministic, hash‑receipted (`d03048c3`).
**Descriptive, not a forecast, not financial advice.** Source: World Bank Open Data. Peter is the sole gate;
nothing posted.*

---

> **Prior art (the past is the future).** This is **not new** — a deeper version (GDP sector + expenditure drift,
> 1960–2024, drift‑before‑shock) was run in **March 2026** (`GDP‑DRIFT‑002`), archived in the HUF legacy evidence.
> This session is **continuity, not novelty**; see [`PRIOR_ART_the_past_is_the_future.md`](PRIOR_ART_the_past_is_the_future.md).

## The idea

The world's monetary systems rest on a **composition** — the share of global economic weight each economy
carries — and that composition *moves* over time, sometimes smoothly (laminar), sometimes churning (turbulent).
Hˢ reads that motion exactly: the shares, the arrow (who is moving fastest in the ratios), the momentum (who
carries the weight of the change), the concentration (effective dimension), and the **flow regime** — and it does
so at two levels: countries, and the blocs they compose (the composition of compositions).

## The result in one line

Reading the **10 largest economies, 2009–2023** (real World Bank GDP, `d03048c3`): **China's share doubled
(12.9 → 25.7%)** while **Japan's more than halved (13.2 → 5.9%)**; the world's economic weight is **concentrating**
(effective dimension 7.3 → 6.2 of 10, toward a US–China duopoly); and the composition **flows laminar in calm
years and turns turbulent exactly across the known stress periods** (a tortuosity peak of **2.08 in 2015–2018**,
another at **1.81 in 2019–2022**). At bloc level, weight moves **Europe → Asia**, North America holding. Full read
in [`RESULTS_world_composition.md`](RESULTS_world_composition.md).

## What's here

| file | what it holds |
|---|---|
| [`RESULTS_world_composition.md`](RESULTS_world_composition.md) | **GDP layer** — shares, arrow, momentum, concentration, flow regime, bloc recursion (`d03048c3`) |
| [`RESULTS_cofer_money_layer.md`](RESULTS_cofer_money_layer.md) | **money layer** — IMF COFER reserve‑currency composition; USD 72→58%; reserves *diversifying* while GDP concentrates (`e339945f`) |
| `world_composition_study.py` · `cofer_money_layer.py` | the runners (real World Bank GDP / real IMF COFER → the Hˢ read; need numpy) |
| `AI_ASSIST.json` | the standard onramp node |

## Honest scope (read this)

- **Real data, deterministic reads** — reproduces to the receipt.
- **Current‑US$ caveat.** GDP in current US$ mixes real growth + prices + **exchange rate** — Japan's fall is
  partly the yen, Europe's partly the euro/pound. The read is honest about the dollar‑denominated weight (the
  monetary‑system view), not "real output" alone.
- **One source, done properly.** GDP weight is one layer. The natural next public sources — each a composition,
  each stackable — are **IMF COFER** (reserve‑currency shares, the money layer itself), broad money, equity market
  cap, and trade. This study is the first proper layer, not the whole picture.
- **Descriptive, not advice.** What the composition did, read exactly; no forecast.

*Cross‑refs: `../financial/` (S&P‑sector composition), `../../library/THE_BLINDNESS_SUITE.md`,
`../README.md`. Source: https://data.worldbank.org (World Bank Open Data, `NY.GDP.MKTP.CD`). Peter is the sole
gate; nothing posted.*

*Proof & Honesty Standard — real data + receipt · turbulence found in the geometry · current‑US$ caveat stated · descriptive not advice · the human decides.*
