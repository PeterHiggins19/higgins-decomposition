# Energy showcase — Canada & Portugal electricity mix (new engine, public EMBER)

*Hˢ (new guard‑aware engine) on the public **EMBER** monthly electricity‑generation‑by‑fuel mix. Public data only; no private or business content. Tier 1 on the engine reads (real data, reproducible); reading the dates into specific policy events is left to the analyst (Tier 2). Reproduce: `python ../run_showcase.py`. Source: EMBER monthly full‑release (electricity generation, by fuel, TWh).*

---

## Canada — 193 months (2010–2026), D = 9 fuels

| Read | Result |
|---|---|
| Driver (helmsman) | **Other Renewables** — CLR *and* coherent helmsman agree (a small, fast‑growing carrier; its share is small but its log‑ratio motion is large) |
| Effective rank | **2.12 of 8** — the whole national transition moves on a ~2‑D surface |
| Effective diversity K_eff | **3.14 → 3.84** — the mix **diversifies** as coal exits and renewables enter |
| Genuine structural transitions (hold‑lock) | **6**, at 2011‑08, 2012‑12, 2013‑12, 2015‑05, 2016‑02, 2022‑08 — self‑calibrated, chatter‑free |
| Deceptive‑drift months | **40** — concentration shifting under quiet motion (the small‑carrier‑doing‑large‑work pattern) |

**The new‑engine improvement, made concrete here.** The earlier Canada study (yearly, old engine) had to be run *manually at D = 8* because Canada reports **zero "Other Renewables"** in early years — the old engine floored that absent carrier and injected an artifact (CLR ≈ −33). The new engine's **zero/sparsity guard handles the zero‑carrier months natively** (here: Other Renewables and Solar both have zero months), so the full D = 9 monthly mix runs clean with no manual workaround. That is the guard layer earning its keep on a real national dataset.

## Portugal — 135 months (2015–2026), D = 7 fuels

| Read | Result |
|---|---|
| Driver (helmsman) | **Coal** — CLR and coherent helmsman agree; Portugal's coal generation falls to zero over the window (its last coal plant closed in 2021), so coal's log‑ratio motion dominates the whole transition |
| Effective rank | **1.37 of 6** — a nearly **one‑dimensional** transition: essentially "coal out → gas/renewables in" |
| Effective diversity K_eff | **4.85 → 4.25** — a slight **concentration** as a carrier (coal) leaves the mix |
| Genuine structural transitions (hold‑lock) | **4**, at 2019‑09, 2020‑06, 2020‑09, 2022‑01 — clustered around the coal phase‑out |
| Deceptive‑drift months | **29** |
| Zero‑carrier handling | **Coal** goes to zero post‑2021 — handled natively by the new zero guard |

## What a sector reader takes from this

- **Who is actually driving the transition** is named and dated automatically, on public data, for each country — and the driver is often a *small* carrier (Canada's Other Renewables) whose share a magnitude view would dismiss.
- **When the system genuinely changed state** (6 transitions for Canada, 4 for Portugal) is separated from month‑to‑month noise by the self‑calibrating hold‑lock — not a fixed threshold.
- The two countries have **different transition shapes**: Canada diversifies on a 2‑D surface led by renewables on a hydro backbone; Portugal runs a near‑1‑D coal‑exit. The same instrument reads both.
- **The honest limit:** the national aggregate masks the **provincial** story (Canada's provinces are a strong multi‑archetype corpus — hydro‑heavy QC/BC/MB, gas AB, coal‑exit ON). EMBER is country‑level only; going provincial needs a public StatCan / Canada Energy Regulator loader — see `../DATA_NEEDS.md`.

*Tier 1 (real public data, reproducible). Reading specific dates into named policy events is the analyst's, not the instrument's.*
