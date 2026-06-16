# The moving budget — and Hˢ as a control/test primitive for any budgeted system

*Peter's extension: the Backblaze method generalizes to any high‑complexity budgeted system — CPU/GPU performance, channel voting, data centres, distributed systems at scale, national and world grids (D proven to 10⁶) — because **all realms are compositions**, and a dynamic system has a **moving budget** that must be tracked alongside the mix. This note adds the size co‑tracker (`hs_budget.py`) and the framing. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; computation Tier 1, framing Tier 2.*

---

## Shape and size — the half the engine sets aside

A composition has two parts: a **shape** (the proportions, scale‑free — what closure keeps and the kinematics engine reads) and a **size** (the total before closure — the **budget**). Standard compositional analysis discards size on purpose, because for *proportional* questions only the mix matters. But for **control and test of a budgeted system**, size is information: a fleet's total capacity, a grid's total generation, a processor's total throughput, a data centre's total power — these are real magnitudes, and in a **dynamic** system they *move*. The shape says *where the mix is going*; the moving budget says *whether the whole thing is growing, shrinking, steady, or lurching* — and you cannot control a system on half of that.

This is the natural generalization of the founding ground state. The loudspeaker's budget was **fixed** (6.02 dB, conserved, apportioned). A dynamic system relaxes that: the budget itself becomes a tracked, moving quantity. Fixed budget → moving budget is the step from the static instrument to the dynamic one.

## Tracking the moving budget (`hs_budget.py`)

Given the raw, **un‑closed** matrix, the size is `N(t) = Σ parts`. The tracker reads its motion with the same discipline the engine applies to the shape:

- **Budget size / total magnitude** — start, end, total growth factor.
- **Budget velocity / growth rate** — the multiplicative growth `d(log N)/dt`, and the CAGR per step.
- **Budget acceleration**, and **budget coherence** — `|Σ growth| / Σ|growth| ∈ [0,1]`: 1 = steady, directed growth/decline; 0 = a churning, volatile budget.
- **Budget regimes** — the discovered‑floor + hold‑lock hysteresis applied to `log N`: *when the growth regime changed* (same anti‑flap logic as the shape engine).
- **Size–shape coupling** — the correlation between budget motion and mix motion: does the mixture reshape *when* the budget moves (coupled), or independently (decoupled)?

Deterministic, hash‑receipted, numpy + stdlib — a companion to the shape engine, not a change to it.

## Demonstration — same shape story, opposite budget stories (real EMBER, absolute TWh)

| System | Total (TWh) | Growth | Budget coherence | Budget regimes | Reading |
|---|---|---|---|---|---|
| **World** | 15,279 → 31,772 (×2.08) | +3.0%/yr | 0.97 | none | steady growth |
| **China** | 1,356 → 10,583 (×7.81) | +8.6%/yr | 1.00 | none | steady growth (coupled, 0.35) |
| **Germany** | 569 → 500 (×0.88) | −0.5%/yr | 0.19 | 2 (idx 13, 25) | **volatile / shrinking** |

Every one of these tells the *same shape story* — coal out, wind and solar in. The **budget** story is where they diverge completely: China's total exploded almost eightfold in a perfectly steady ramp; the World's doubled smoothly; **Germany's total actually shrank and did so volatilely, with two growth‑regime breaks.** Germany shedding coal while its whole budget contracts is a fundamentally different system‑state than China adding renewables while its budget explodes — and *only the moving‑budget read distinguishes them.* For a controller, that distinction is everything (manage a growing system vs. a contracting one).

## Why this makes the method a general control/test primitive

All realms that conserve‑and‑apportion are compositions, and Hˢ reads them at any scale (the CNQ tiling proves the exact reading to **D = 10⁶**, IEEE floor). So the same primitive — **read the shape's motion, track the budget's motion, watch their coupling, behind guards and breakers, hash‑receipted, non‑contact** — applies across:

- **Processors / GPUs** — utilisation/thermal/error composition per core or card; budget = total throughput; pre‑fault and load‑balance by measured performance (the fleet method, §`../experiments/Hs-17_Backblaze/FLEET_PREFAULT_MIGRATION_CONCEPT.md`).
- **Channels / links** — traffic‑class composition per channel; budget = total bandwidth; coherence‑weighted **leader voting** (§`../HCI-CNTT/DISTRIBUTED_CONTROL_AND_LEADER_ELECTION.md`).
- **Data centres / distributed systems at scale** — workload/power/failure‑mode composition; budget = total capacity or power; tier and migrate by performance.
- **National & world grids** — generation‑mix shape + the moving generation budget (demonstrated above); the same read scales from one country to the world.

In each case the control question is the same shape‑and‑budget pair, and the test question is the same guards‑and‑hash. **High complexity is not a barrier — it is the design point** (D to a million, the diagnosis language expands with the complexity, the guards report what cannot be resolved).

## Honest edges

- The size/shape split is standard; tracking the size's **kinematics and its coupling to the shape** is the addition, and it is a simple, sound one (Tier 1 computation). The *framing* as a universal control/test primitive is Tier 2 — sound, assembled from Tier‑1 parts, not yet deployed in a live controller.
- Size is only meaningful when the total is a real magnitude (TWh, IOPS, watts) — for purely proportional data the budget read is correctly inert.
- Coupling is a correlation, not a cause; it flags *that* shape and budget move together, not *why*.
- Next step: run the moving budget inside the fleet backtest and the N‑node bench, so the controller acts on the shape **and** the budget together.

*The mix tells you where the system is headed; the moving budget tells you whether it is growing into that destination or shrinking out of it. A controller for a budgeted system needs both — and now reads both, deterministically, at any scale.*
