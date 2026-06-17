# The world wine industry in motion — real OIV data, new Hˢ kinematics

*Hˢ kinematics + the diagnosis language on **real public OIV data** (`world wine data.xlsx`, provided 2026‑06‑15): world **wine production** as a composition of countries' shares, 1995–2025. This upgrades the wine showcase from the public‑chemistry demo to a real country‑level study. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; Tier 1 on the run; the *meaning* (New‑World rise) is the analyst's, not the engine's. Reproduce: `python run_wine_kinematics.py`. Source: OIV (International Organisation of Vine and Wine), public; aggregates (Global/EU) excluded.*

---

## The read (top 14 producing countries, 31 years)

| Reading (navigation / physics) | Value |
|---|---|
| **Arrow of intent / momentum — to** | **Spain, Australia, Chile** (+ Russia, South Africa) — gaining production share |
| **— from** | **France, Italy, Argentina** (+ China, Romania) — shedding share |
| **— coherence** | **0.10** (low) — a gradual, contested shift, not a single committed surge |
| **Course directness / path efficiency** | **0.13** — wandering; year‑to‑year noisy, no straight trend |
| **Degrees of freedom / effective dimensionality** | **7.3** — a genuinely multi‑country rearrangement (~7 independent directions) |
| **Spread trend (K_eff)** | **8.76 → 9.79 — diversifying** (production spreading across more countries) |

**Diagnosis language (the industry speaking, deterministically):**
> *"France is steering (shedding). Weight is moving toward Spain, Australia, Chile, Russia, South Africa. It is moving away from France, Italy, Argentina, People's Republic of China, Romania. The mixture is diversifying (effective spread 8.76 → 9.79). The motion runs in about 7 independent directions. (10 of 14 parts have something to say; the rest are quiet.)"*

## What it means (the analyst's read, not the engine's)

A wine economist recognises this instantly: the **globalisation of wine production** — the traditional Old‑World leaders (France, Italy) shedding *relative* share while Spain and the New World (Australia, Chile, South Africa) gain, the whole industry **diversifying** across more producers, gradually and on many fronts at once. The engine made no such claim; it stated, deterministically, *who gains and who sheds and that the mix is spreading* — and the meaning fell out for the expert. That is the instrument working as intended on a real industry.

## Provenance + the deeper data still available

- **Used (public, clean):** OIV `world wine data.xlsx` — production / consumption / exports / imports / surface area, by country and year. This run uses **Production**; the same engine reads **Exports**/**Imports** (trade composition) or a single country's product mix (wine / table grapes / dried grapes) with one parameter change.
- **Available, needs offline extraction (too large for the sandbox):** the **CEPII BACI** bilateral‑trade databases (`trade_i_baci_a_*.csv.zip`, ~4.5 GB unzipped each, per HS revision) and the **OEC SITC2** file. Wine is **HS 2204** inside them. To build a *bilateral wine‑trade composition* (each country's export‑destination mix over time — "where is the wine going"), stream‑filter the product code offline:
  ```
  unzip -p trade_i_baci_a_22.csv.zip trade_i_baci_a_22.csv \
    | awk -F, 'NR==1 || $4 ~ /^2204/' > wine_hs2204_bilateral.csv
  ```
  then pivot (exporter × destination‑share per year) and run `hs_kinematics_engine.run`. That is the next, richer wine study — the trade flows in motion — when run on a machine that can hold the file.

*Tier 1 on the production run (real OIV data, reproducible); the trade‑flow extension is scoped and one offline step away. The wine showcase now stands on real public data.*
