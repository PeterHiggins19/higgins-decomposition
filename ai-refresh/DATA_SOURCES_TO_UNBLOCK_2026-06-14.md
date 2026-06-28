# Data sources to unblock the built machinery (verified 2026‑06‑14)

*The exact public download locations for the three data‑blocked items. The pipelines are built and self‑tested; these files turn finished code into finished results. All sources public + freely licensed (most CC BY 4.0). Links verified by web search 2026‑06‑14. Author: Peter Higgins; AI‑assisted per HUF‑STD‑001. Honest‑broker; honest gaps flagged.*

---

## 1 · Canada provincial energy → unblocks S2‑2 (the multi‑archetype provincial showcase)

**Feeds:** the province‑level energy study (hydro‑heavy QC/BC/MB, gas AB, coal‑exit ON, wind PEI). EMBER is country‑level only, so this is the separate public provincial loader.

- **Statistics Canada — Table 25‑10‑0015‑01, "Electric power generation, monthly generation by type of electricity," by province/territory** (Survey 2151 MELE; last released 2026‑06‑01): https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2510001501 → use **"Download options" → CSV** (whole table). *This is the primary file — monthly generation by type, per province, the compositional series the engine wants.*
- StatCan — Table 25‑10‑0020‑01, "Electric power, annual generation by class of producer": https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2510002001
- StatCan — Table 25‑10‑0016‑01, monthly receipts/deliveries/availability: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2510001601
- **Canada Energy Regulator — Provincial & Territorial Energy Profiles** (per‑province generation, Figure Data CSV): https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/
- Canada energy information hub (electricity): https://energy-information.canada.ca/en/subjects/electricity

**What to grab:** the 25‑10‑0015 monthly CSV (all provinces, all generation types). A thin loader maps its fuel types to the engine's carrier template — then `run_cntt` per province.

## 2 · Monthly EMBER → unblocks the 9‑country deceptive‑drift P2 (P‑3) + the Fukushima bridge

**Feeds:** the monthly deceptive‑drift run (the annual grain wasn't quiet enough — monthly was the documented need) and the Gen‑1→2 Fukushima re‑run.

- **Ember — Monthly Electricity Data** (generation/emissions/demand, 88 geographies, monthly, CC BY 4.0; updated twice a month): https://ember-energy.org/data/monthly-electricity-data/ → download the **monthly full‑release CSV (long format)**.
- Ember — Data Explorer (interactive, same data): https://ember-energy.org/data/electricity-data-explorer/
- Ember — Yearly Electricity Data (the long 2000‑→ context for Fukushima at annual grain): https://ember-energy.org/data/yearly-electricity-data/
- Methodology: https://storage.googleapis.com/emb-prod-bkt-publicdata/public-downloads/ember_electricity_data_methodology.pdf

**Already in‑corpus (honest note):** `DATA/Energy/monthly_full_release_long_format.csv` is the Ember monthly file and already covers the P2 countries (used for the Canada/Portugal showcase). **So the 9‑country monthly P2 is essentially unblocked now** — re‑download only for freshness. The genuine gap is the **Fukushima 2011** signature: Ember *monthly* generally starts ~2015, so Japan monthly around 2010–2012 isn't in it. Options for the pre‑2015 Japanese monthly grain: Japan's own **METI / OCCTO** generation statistics, or run the Fukushima bridge at **annual** grain (the yearly file + the existing `dormant/` Japan series already capture the 2010 deceleration → 2011 shock).

## 3 · Public wine stats → unblocks the country‑level wine study (showcase depth)

**Feeds:** the Canada/Portugal wine study (variety/region production composition + trade‑destination composition). Public, sector‑level only — never producer/business data.

- **OIV — Statistics** (production, area under vine, consumption, trade by country; free database + reports): https://www.oiv.int/what-we-do/statistics
- OIV — *State of the World Vine & Wine Sector* (annual report, country tables): https://www.oiv.int/sites/default/files/2026-05/OIV-State_of_the_World_Wine_Sector_in_2025_0.pdf
- **UN Comtrade — wine trade, HS code 2204** ("Wine of fresh grapes"; export/import by country, annual or monthly): https://comtradeplus.un.org/ (bulk download needs a free account) — easy alternative with downloadable country trade: **OEC wine (HS 2204)** https://oec.world/en/profile/hs/wine
- **IVV (Instituto da Vinha e do Vinho) — Portugal wine statistics** (production/market by campaign): https://www.ivv.gov.pt/np4/estatistica/
- **Statistics Canada — grape & wine industry** (sales/production; e.g. "From the Vine to the Glass"): https://www150.statcan.gc.ca/n1/pub/11-621-m/11-621-m2006049-eng.htm (and current StatCan wine tables under 32‑10 / food‑and‑beverage series)

**What to grab:** OIV country production/variety tables (the composition over time) + Comtrade/OEC HS‑2204 export‑by‑destination (the trade composition). Then the wine showcase moves from the public‑chemistry demo to the country‑level study in `showcase/canada_portugal_2026-06/wine/`.

---

## Where each lands when downloaded

| File | Drop into | Pipeline ready to run |
|---|---|---|
| StatCan 25‑10‑0015 provincial CSV | `DATA/Energy/` | province loader → `run_cntt` per province (S2‑2) |
| Ember monthly CSV (fresh) | `DATA/Energy/` (replaces existing) | `experiments/deceptive_drift_null_2026-06/monthly_deceptive_drift.py` (P‑3, 9 countries) |
| Japan pre‑2015 monthly (METI/OCCTO) *or* annual | `DATA/Energy/` | the Fukushima Gen‑1→2 bridge re‑run |
| OIV + Comtrade/OEC + IVV wine tables | `showcase/canada_portugal_2026-06/wine/data/` | the country‑level wine study |

*Sources verified 2026‑06‑14. The 9‑country monthly P2 can likely run today on the in‑corpus Ember file; the others need a download. Public data in, engine performance out.*
