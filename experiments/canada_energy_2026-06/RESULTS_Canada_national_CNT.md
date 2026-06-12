# Canada energy study — national anchor (CNT, canonical engine)

**2026-06-09 · Cowork working tree (not committed). Instrument reports; interpretation is the analyst's.**

## Data
EMBER `yearly_full_release_long_format.csv` (in-corpus), national **Canada (CAN)**, electricity generation by fuel, **2000–2025 (26 years)**, TWh. Extracted to pipeline-ready form (`ember_CAN_Canada_generation_TWh.csv`) matching the existing 9-country EMBER set.

## Method
Run through the **canonical CNT engine v3.2.0** (`HCI-CNT/engine/cnt.py`) — closure → CLR → Helmert-ILR → per-step navigation, hash-stamped JSON (`ember_CAN_cnt_D8.json`). NB: this is the canonical engine binary, not a reimplementation — it also exercises the engine on a fresh country.

## Data-treatment note (honest)
Canada reports **zero "Other Renewables" in every year**. At the full 9-carrier template the engine floors that absent carrier to 1e-15, which injects an artifact (CLR ≈ −33, inflated Aitchison norm ≈ 36) that contaminates the navigation. The run was therefore done at Canada's **true dimensionality D = 8** (carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind). This is a concrete instance of the queued **Bayesian-multiplicative zero-treatment** to-do — structurally-absent carriers should be dropped (or treated) upstream, not floored.

## What the instrument reported (D = 8, observations only)
- **Helmsman (driver of each step):** Solar 11 · Wind 6 · Other Fossil 5 · Coal 2 · Nuclear 1. The down-the-years motion is carried mostly by **Solar and Wind** — which grew from near-zero bases (Solar 0.02→10.2 TWh, Wind 0.3→51.5 TWh), so their *log-ratio* motion is large even though their *shares* stay small.
- **Concentration regimes:** loosening 10 · stable 10 · **deceptive 4** · tightening 1. The deceptive-drift signature **fires** for Canada (4 transitions) — the small-carrier-doing-large-structural-work pattern.
- **K_eff (effective active carriers):** 3.36 → 4.16 (final 4.16) — the mix **diversifies** over the window as coal exits and renewables enter.
- **Biggest Aitchison steps (year · step · helmsman):** 2009 (1.05 · Solar), 2010 (0.92 · Solar), 2005 (0.81 · Solar), 2004 (0.79 · Solar), 2011 (0.76 · Solar), 2020 (0.73 · Other Fossil).
- **Raw compositional story (from the data, model-independent):** Coal 116→27 TWh, Gas 36→116, Wind 0.3→51, Solar 0→10, **Hydro stable ~345–383** — coal-exit + gas/renewables-in on a hydro-dominated backbone.

## For the analyst to determine
Whether the Solar/Wind-led steps and the 4 deceptive transitions align with known Canadian events (provincial coal phase-out regulations, solar/wind procurement programs, Ontario's 2014 coal exit) is an interpretation for the analyst, not a claim of the instrument. The national aggregate **masks the provincial archetypes** — the richer corpus.

## Caveats & next
- National aggregate only; **provinces/territories are the strong multi-archetype corpus** (ON coal-exit 2014, AB coal-to-gas, QC/BC/MB hydro-stable, SK/NS transitioning, NL hydro+Muskrat Falls, PEI wind) — they need a **separate StatCan / Canada Energy Regulator loader** (EMBER is country-level only); not yet built.
- Grain-dependence expected; report it when the provinces run.
- Not yet done: CNQ pass; the depth×composition dashboard; calibration against a policy timeline; the upstream zero-treatment module.

## Files
`ember_CAN_Canada_generation_TWh.csv` (D=9 source) · `ember_CAN_Canada_generation_TWh_D8.csv` (true-dimensionality input) · `ember_CAN_cnt_D8.json` (canonical CNT output, hash-stamped).

*The instrument reads. The expert decides.*
