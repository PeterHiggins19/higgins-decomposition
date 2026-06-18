# Wine showcase — the compositional read, on public data only

*Hˢ on wine as a compositional problem, using a **public** wine‑chemistry dataset. No winery, brand, person, or private engagement appears here — by design. This demonstrates the *capability* the wine sector can use; a country‑level Canada/Portugal study would be built only from the public sources listed in `../DATA_NEEDS.md`. Tier 1 on the run (public data, reproducible). Reproduce: `python ../run_showcase.py`.*

---

## Why wine is a compositional problem

A wine is *parts of a whole*: a chemical profile (acids, phenols, sugars, colour), and at sector scale a region's output is *parts of a whole* too (varieties, styles, export destinations). Those are exactly what Hˢ reads — relative structure, not absolute magnitude — so the same instrument that reads an energy mix reads a wine profile.

## The demonstration — public wine chemistry (3 cultivars, 13 attributes, 178 wines)

Using the standard public UCI wine dataset (chemical analysis of wines from three cultivars), treated as a 13‑part chemical composition:

| Read | Result |
|---|---|
| Apparatus | **static / cross‑sectional** — no time axis, so Hˢ serves the **standard CoDa apparatus** (ternary, CLR biplot, variation matrix), the dynamic layer *not* forced |
| What separates the cultivars (the discriminating chemistry) | **flavanoids**, then **colour intensity**, **malic acid**, **non‑flavanoid phenols** — the carriers whose relative profile most distinguishes the three groups |
| Effective rank | **7.36 of 12** — the chemical profile is genuinely high‑dimensional (no single ratio carries it) |

This is the **static‑user path** in action: a wine chemist with a table of analyses gets the standard compositional read — which chemical balances separate their samples — with no need to learn the dynamic machinery. (And if they had a *time series* — a fermentation, a vintage‑over‑vintage trajectory — the dynamic engine would add the helmsman/regime/hold‑lock reads on top.)

## What a country‑level Canada/Portugal wine study would show (public‑data only)

Built strictly from public statistics (production by variety/region, export/import trade by destination — see `../DATA_NEEDS.md`), the engine would read:

- **Variety/style composition over time** per country — which varieties are gaining or losing relative share (helmsman), and *when the mix genuinely shifted* (hold‑lock), separated from year‑to‑year noise.
- **Trade‑destination composition** — how each country's export mix is concentrating or diversifying (K_eff), and any **deceptive drift** (a destination quietly concentrating).
- A **symbiotic, public read**: the sector‑level story, with every individual producer's data and identity kept private. The value to a partner is the capability and the public‑data picture; their own data stays theirs.

*No private content. Tier 1 on the public‑data run; the country‑level study is scaffolded, not yet run (awaiting the public sources in DATA_NEEDS).*
