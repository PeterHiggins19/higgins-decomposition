# Q&A bench card — INV-051 deceptive drift 5-of-9

**When to use:** if asked about the deceptive-drift signature, why these 5 countries and not the other 4, grain-dependence, or the Germany p-value.

---

## The 30-second answer

> *"The packet's deceptive-drift signature — K-eff tightening while TV stays at or below the series median — fires at annual grain in 5 of 9 EMBER countries: **AUS, CHN, GBR, IND, JPN.** Catalogued as INV-051. Germany at annual grain shows K-eff tightening but TV above median — the protocol classifies this as LOUD drift, not deceptive. USA and WLD are mostly stable; FRA is mostly loosening. The protocol distinguishes regimes cleanly; it does not just fire everywhere."*

## If pressed on "Why these 5 and not the other 4?"

> *"Each per-country trajectory is in the conference_2026_06/ folder, individually inspectable. The differences are interpretable. Germany pre-2022 was visibly moving toward renewables — loud drift, not silent. USA's energy mix is mostly stable. France is mostly loosening (denuclearisation). WLD averages out individual-country signatures. Australia, China, the UK, India, Japan — Pacific economy, emerging economies, island nation, post-Fukushima — all reproduce the deceptive pattern. The diversity of country types is exactly what made the cross-country reproduction strong evidence."*

## If pressed on the Germany p = 0.0016

> *"That number is from the packet's monthly-grain protocol on the German monthly EMBER deseasonalised data. At annual grain, the K-eff side reproduces but the TV-quietness side does not — annual data averages over the months where TV is below median. The monthly module is queued (`monthly_deceptive_drift.py`). And the p-value itself is computed against the series' own empirical-frequency baseline — that's exactly Q3, the right-null-model question."*

## If pressed on grain-dependence

> *"Grain-dependence is methodologically interesting on its own. The K-eff side is grain-robust; the TV-quietness side is grain-dependent. That tells you something about how often you need to measure to see the structural pattern — and that's a feature, not a bug. Different domains will have different right-grains."*

## What to NOT claim

- Do not say *"universal signature"* — 5/9 is moderate, not universal.
- Do not say *"the protocol works everywhere"* — the protocol correctly classifies 4 countries as non-deceptive. That's evidence of discrimination, not failure.
- Do not over-defend Germany at annual grain. Honest framing: K-eff side fires; TV side requires monthly grain; queued.

## Receipts

- Per-country regime_counts in `papers/codawork2026/conference_2026_06/per_country/ember_*/cnt_v3.json` field `tensor.navigation_concentration_summary.regime_counts.deceptive`
- Cross-corpus table in `papers/codawork2026/conference_2026_06/DECEPTIVE_DRIFT_REPORT.md`
- INV-051 in `ai-refresh/INVESTIGATION_CATALOG.json`
