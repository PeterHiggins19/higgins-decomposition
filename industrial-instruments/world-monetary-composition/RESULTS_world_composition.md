# The world economy as a composition in motion — turbulence, laminar flow, and concentration (INTERNAL · STUDY)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑25. A **proper,
real‑data** Hˢ study — no estimates — of how the composition of the world's economic weight (the backing of the
monetary systems) moves and churns over time. Deterministic, hash‑receipted (`d03048c3`). **Descriptive — what
the composition is doing — not a forecast and not financial advice.** Source: World Bank Open Data
(GDP, current US$). Peter is the sole gate; nothing posted.*

---

## The data

Real World Bank GDP (current US$, `NY.GDP.MKTP.CD`), the **10 largest economies, 2009–2023** — fetched live from
the World Bank API. Read as a composition: each year is a point on the simplex; the Hˢ engine reads its shares,
its motion (clr velocity), its concentration (effective dimension), and its **flow regime** (laminar vs
turbulent). Two levels — countries, and the blocs they compose ("the composition of compositions").

## Level 1 — the country composition (share 2009 → 2023)

| economy | 2009 | 2023 | move |
|---|---|---|---|
| United States | 36.1% | **38.4%** | steady‑dominant |
| **China** | 12.9% | **25.7%** | **doubled** — the great rise |
| **Japan** | 13.2% | **5.9%** | **more than halved** — the great fall |
| Germany | 8.7% | 6.4% | declining |
| India | 3.3% | **5.1%** | rising |
| United Kingdom | 6.0% | 4.8% | declining |
| France | 6.7% | 4.3% | declining |
| Italy | 5.5% | 3.3% | declining |
| Brazil | 4.2% | 3.1% | declining |
| Canada | 3.4% | 3.1% | ~steady |

## What the instrument reads in the motion

**The arrow (helmsman — the fastest log‑ratio mover).** Early (2010–12) it is **China**, climbing; in the late
window (2020–23) it is **Japan**, *falling* — the yen's collapse makes Japan the fastest mover in the ratios even
as the totals look ordinary. *(A clean ratio‑blind moment: a scalar "world GDP up" misses that the mix is being
yanked by Japan's decline.)*

**The momentum (mass × velocity).** Alternates between the two heavyweights — **United States** and **China** —
who carry most of the *weight* of the change even when a smaller economy moves faster. The arrow and the momentum
disagree (mass‑blindness, made visible): the fastest mover is rarely the heaviest.

**The concentration (effective dimension).** Falls steadily: **7.26 (2009) → 6.16 (2023)** out of 10. The world's
economic weight is **concentrating** — drifting toward a US–China duopoly with a thinning tail. The same at bloc
level: ~3.36 → ~3.17 of 4.

**The flow regime (tortuosity of the clr trajectory; 1 = laminar/straight, >1 = turbulent/churning).**

| window | tortuosity | regime |
|---|---|---|
| 2009–2012 | 1.24 | laminar (post‑crisis recovery, steady) |
| 2013–2016 | 1.36 | mild churn |
| **2015–2018** | **2.08** | **turbulent** — China slowdown / yuan, Brexit, trade tension |
| 2016–2019 | 1.90 | turbulent tail |
| 2017–2020 | 1.17 | briefly laminar |
| **2019–2022** | **1.81** | **turbulent** — COVID shock + inflation + yen |
| 2020–2023 | 1.29 | re‑laminarizing |

The composition flows *smoothly* in calm years and *churns* — doubling back on itself in clr‑space — exactly
across the known stress periods. The instrument finds the turbulence where macro history puts it, from the
geometry alone.

## Level 2 — the composition of compositions (blocs)

| bloc | 2009 | 2023 |
|---|---|---|
| North America | 39.5% | 41.4% |
| **Asia** (CN/JP/IN) | 29.4% | **36.7%** |
| **Europe** (DE/UK/FR/IT) | 26.9% | **18.8%** |
| Latin America | 4.2% | 3.1% |

The bloc read is the cleaner story under the country noise: **weight is moving West‑Pacific → Asia and out of
Europe**, North America holding. The same composition, read one level up — the recursion Peter asked for.

## Honest fences

- **Real data, deterministic reads** — every number reproduces to the receipt (`d03048c3`).
- **Current‑US$ caveat (important).** GDP in current US$ mixes *real growth + domestic prices + exchange rate.*
  Japan's fall is **partly yen depreciation**, not only lost output; Europe's decline partly euro/pound moves.
  The *composition read is honest about the data it is given* — it reads the US‑dollar‑denominated weight, which
  is exactly the monetary‑system‑relevant view, but it is not "real output" alone.
- **Descriptive, not predictive.** This is what the composition *did*, read exactly. No forecast, no advice.
- **One source, done properly — not the whole picture.** This is GDP weight. The natural next layers (further
  public sources): **IMF COFER** reserve‑currency shares (the money layer itself), broad‑money by country, equity
  market cap, and trade — each a composition, each stackable into the recursion.

## Honest scope

- **T1:** the engine + the deterministic reads on real World Bank data (`d03048c3`).
- **T2:** the regime/turbulence framing and the bloc recursion.
- **T3:** any interpretation of *why*, and anything forward‑looking. **Not financial advice.**

*Listed in the papers' [`SUPPORTING_CASE_STUDIES.md`](../../papers/SUPPORTING_CASE_STUDIES.md) — a documented
study of interest behind the P‑series.*

*Cross‑refs: `README.md`, `world_composition_study.py`, `../../library/THE_BLINDNESS_SUITE.md` (ratio‑ and
mass‑blind, both visible here), `../financial/` (the S&P‑sector composition study). Source:
https://data.worldbank.org (World Bank Open Data). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — real data + receipt · turbulence found in the geometry · current‑US$ caveat stated · descriptive not advice · the human decides.*
