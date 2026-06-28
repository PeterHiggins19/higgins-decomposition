# Hˢ Industrial Instruments

*Public Hˢ applications where the engine acts as a deterministic **instrument** on industrial / device / operational compositional data. 2026‑06‑11. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Engine: **CN‑TT v4** ([`../HCI-CNTT/`](../HCI-CNTT/)). Claim‑tiered.*

---

## What this folder is

Hˢ reads any composition that drifts over time and reports **which carrier is steering the change, when the regime shifts, and whether a change is real or a sensor fault** — the **fourth monitoring category, MC‑4 (Composition Monitoring)**, that magnitude/threshold instruments miss. This folder holds the public, self‑standing studies that demonstrate Hˢ as an industrial instrument. They double as the public evidence base behind the HUF‑Gov **Ratio Blindness** doctrine ([`../../HUF/huf-gov/RATIO_BLINDNESS_DOCTRINE.md`](../../HUF/huf-gov/RATIO_BLINDNESS_DOCTRINE.md)): *three categories measure magnitude; the fourth reads the ratios — ignore it and ~¼ of the monitoring picture goes undiagnosed.*

## Studies

| Study collection | Domain | Status |
|---|---|---|
| [`gas-composition-study/`](gas-composition-study/) | **Gas & process‑fluid composition** — 4 studies | ✅ all four RUN (deterministic, lossless, hash‑receipted) |
| ↳ Study 1 — closed‑loop O₂/CO₂/N₂ life‑support | breathing / life support | lossless 8.9e‑16; 40/60 single‑channel alarms green while composition moved (ratio blindness) |
| ↳ Study 2 — [oil & gas produced water](gas-composition-study/produced-water-codawork/) | oil & gas (CoDaWork/Engle; USGS DB) | lossless 3.6e‑15; formation transition; censored values handled |
| ↳ Study 3 — [blood / alveolar gas](gas-composition-study/blood-gas/) | clinical / dissolved O₂ (D=4 CNQ‑native) | exact quaternion read 4.7e‑16; O₂/CO₂ drive desaturation |
| ↳ Study 4 — [spacecraft cabin atmosphere](gas-composition-study/cabin-atmosphere/) | closed‑loop life support (ISS‑style) | lossless 2.2e‑15; CO₂ duty cycle; VOC event caught |
| [`financial/`](financial/) | **Financial systems** — the composition that allocates and moves money; *study the system that studies the market*, not the price | ✅ RUN — S&P 500 ten‑sector composition, deterministic vector map (arrow of intent, ~5 effective directions, regime changes), hash `5b2a32d6…`. **Not statistics, not a forecast, not investment advice** — complements existing analysis |
| [`constellation-spacex/`](constellation-spacex/) | **Large LEO constellations (SpaceX/Starlink)** — the fleet read as a composition: deterministic fleet‑coherence, drift/anomaly detection, collision‑avoidance support, and dual‑use upper‑atmosphere sensing | 🌱 **SEED / concept** — research program, *no orbital run yet*; T2/T3 on top of P1's T1 engine. [`README`](constellation-spacex/README.md) |
| [`electronics-assembly-smt/`](electronics-assembly-smt/) | **Electronics‑assembly SMT** (Nordson‑class dispense + Fuji‑class placement) — deposit/placement/cell as compositions; the contact‑point doctrine; fiber‑optic × Hˢ future; the coherence law | 🛠️ **PLANNING / built demos** — dispense silent‑drift (`cf9bf72f`), contact‑rank (`ae19158b`), fiber common‑mode (`e791ec63`), coherence law (`a5ceab9e`). Equipment domains only. [`README`](electronics-assembly-smt/README.md) |
| [`euv-lithography/`](euv-lithography/) | **EUV lithography** — the stochastic valley‑of‑death as a `{OK, missing, bridge}` defect composition; LPP source as a laser+plasma budget; dose/CD as a deformation field | 🛠️ **BUILT** (from a Tier‑2 seed) — stochastic silent‑drift with a 62‑wafer lead + directional dose arrow (`877516b6`). Public physics only. [`README`](euv-lithography/README.md) |
| [`canada-open-data/`](canada-open-data/) | **Canada open‑data estate** — Hˢ reads the composition of all 47,462 open.canada.ca datasets (department/format/jurisdiction/collection shares, arrow, effective dimension) | 🛠️ **BUILT · DEMO** — two mandates = 43% of the estate; Yukon out‑publishes Ontario 3:1; receipt `209a8559`. Real public metadata, descriptive. [`README`](canada-open-data/README.md) |
| [`canada-program/`](canada-program/) | **Canada Program** — the all‑in‑one offer (intro email + prepared package from existing repos) + where Canada fits the world composition + early‑adoption momentum | 🛠️ **DRAFT** — Canada ~0.2% by mass but leading‑cluster by specialty; early standard‑adopter holds a compounding lead (`87fbaaa3`). Nothing transmitted; Peter's gate. [`README`](canada-program/README.md) |
| [`world-monetary-composition/`](world-monetary-composition/) | **World monetary composition** — the world economy read as a moving composition (real World Bank GDP): shares, arrow, momentum, concentration, laminar‑vs‑turbulent flow, country→bloc recursion | 🛠️ **BUILT · STUDY** — China 12.9→25.7%, Japan 13.2→5.9%; concentrating (eff‑dim 7.3→6.2); turbulence peaks 2015‑18 & 2019‑22 (`d03048c3`). Real data, descriptive. [`README`](world-monetary-composition/README.md) |

*Each study names a public‑data verification target. Experiments + science only — no outreach letters in this repo. More industrial studies added here as run.*

> **Forward orientation:** the deployment future and how the repo supports it (to the boundary, not past it) is in
> [`../huf-gov/doctrine/TARGET_THE_FUTURE.md`](../huf-gov/doctrine/TARGET_THE_FUTURE.md); the reusable read‑only
> pilot runbook is [`PILOT_KIT.md`](PILOT_KIT.md).

## Why "instrument," not "model"

Every study here is deterministic and hash‑chained: same input + configuration → byte‑identical output, with a content receipt. That is what lets an industrial result be **validated, audited, and reproduced** — and what makes a network of such validated, real‑world uses the credible path toward instrument‑grade and flight deployment (see [`../SPACE_READINESS_AND_CHALLENGE.md`](../SPACE_READINESS_AND_CHALLENGE.md)). Hˢ reads the structure; the domain engineer decides what it means.

## Governance & scope
- **Instrument, not data.** We read compositions where they live; we do not store or redistribute device or operational datasets.
- **Honest‑broker, claim‑tiered.** Tier 1 (verified), Tier 2 (sound), Tier 3 (to earn). Nulls reported.
- **Determinism + provenance** (HUF‑STD‑002). **Communications per RWA‑001.**
- **Carrier‑filter.** Specific commercial engagements are tracked privately, off the public repo, per [`../../HUF/huf-gov/CARRIER_FILTER_DOCTRINE.md`](../../HUF/huf-gov/CARRIER_FILTER_DOCTRINE.md). The public studies here name only the application area, never a private counterpart.

*The instrument reads. The expert decides. The hashes carry the receipts.*
