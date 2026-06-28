# What is needed for both studies — public sources only

*Exactly what public data each study needs to go deeper, and what is explicitly **not** needed (anything private). The rule throughout: public, citable, sector‑level. No business‑level or personal data is required, requested, or stored.*

---

## Energy — to go from national to provincial (Canada) and finer (Portugal)

**Have (done):** EMBER monthly electricity generation by fuel, national, for Canada (D=9) and Portugal (D=7) — already run (see `energy/RESULTS_energy.md`).

**Need for the in‑depth provincial Canada study (the strong multi‑archetype corpus):**
- **Statistics Canada** electricity generation by source **by province/territory** (e.g. Table 25‑10‑0015 / 25‑10‑0020), monthly or annual — public.
- **Canada Energy Regulator (CER)** provincial generation profiles — public.
- A small loader that maps those to the same fuel‑carrier template (EMBER is country‑level only, so this is a separate public loader, not yet built).
- *Payoff:* the provincial archetypes (hydro‑dominant QC/BC/MB, gas AB, coal‑exit ON, wind PEI, transitioning SK/NS) — each a distinct compositional character the national aggregate masks.

**Need for finer Portugal:** REN / DGEG (Portuguese grid operator / energy directorate) public generation series for sub‑annual or technology‑split depth, if more than EMBER's national monthly is wanted.

## Wine — to go from the public chemistry demo to a country‑level sector study

**Need (all public, sector‑level — never producer‑level):**
- **Production by variety / region over time** — OIV (International Organisation of Vine and Wine) statistics; national statistics agencies (Statistics Canada; Instituto da Vinha e do Vinho, Portugal) — public aggregates.
- **Trade composition** — export/import by destination/origin over time — UN Comtrade / national trade statistics (HS codes 2204) — public.
- Optionally, **public** wine‑chemistry reference datasets (like the UCI set used in the demo) for the static chemical‑profile read.

## What is explicitly NOT needed (and will not be collected or stored)

- **No producer‑level, winery‑level, or business‑level data.** No names, brands, volumes, prices, or customer lists of any specific business.
- **No personal data, correspondence, proposals, or deal terms.** Any real engagement is private and lives off the public repository.
- The studies are built to be **fully reproducible from public sources alone** — which is what makes them a showcase rather than an exposure. A partner's own data, if they ever chose to share it privately, would be a separate private conversation under their control.

*Public data in, engine performance out. The capability is shown; the privacy is kept.*
