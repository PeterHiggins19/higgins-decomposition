# Onboarding from zero — for a group blind to every aspect (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑23. The teach‑
from‑nothing path: a reader who knows neither compositional analysis, nor Hˢ, nor this application can follow
this to understanding and a running pilot. No prior knowledge assumed. Honest‑broker tiered; nothing posted;
Peter is the sole gate.*

---

## Step 0 — the one idea (no math)

Your line makes things by *mixing and placing in proportions*. A glob of paste is mostly metal, some flux, a
little void. A placed part sits at an angle and an offset. A cell spends its "health" across accuracy, heat,
feeders, throughput. **Every one of these is a set of parts that add up to a whole — a *composition*.** The
secret: *the meaning is in the proportions, not the totals.* A fault usually shows in the **ratios** long
before any one number trips an alarm.

## Step 1 — the one tool (what Hˢ does)

Hˢ is a calculator that reads a composition and tells you, in plain words: **which part is rising or falling
(the arrow), how committed the change is (the character), how complex it is (the dimension), and whether it's
real or noise (the coherence)** — and it stamps every answer with a fingerprint (a hash) so anyone can re‑run
it and get the *same* answer. It refuses to guess when the data is unclear. *It reads; you decide.*

## Step 2 — see it work in five minutes

Run the planning demo (`python dispense_drift.py`). It simulates a dispense nozzle slowly clogging. You will
see Hˢ flag the clog **20 deposits before** a normal volume alarm would — because it watched the *ratio*
(volume falling while voids rose), not the single number. That 20‑deposit head start is scrap you didn't make.

## Step 3 — the four objects on your line (the map)

| you see on the line | Hˢ sees | what it tells you |
|---|---|---|
| a paste/adhesive deposit | a composition of `{volume, height, footprint, voids}` | a clog/wear drift, early |
| a placed component | a 6‑DOF pose (an exact rotation + offset) | registration drift; a board‑wide deformation map |
| a cell | a health composition | which subsystem is failing, before it fails |
| a line / plant | a composition of cells / lines | which cell is worst, kept in balance |

## Step 4 — how it stays safe (the one rule)

Control only flows *down* when the **operator arms Breaker 16**. Sensing always flows *up*. The human is the
fixed point — the system advises and, only when armed, gently nudges a parameter back toward healthy; it never
runs the machine on its own. *(Demonstrated: armed → the cell holds healthy; the operator can always stop it.)*

## Step 5 — the staged pilot (you can start small)

1. Tap **one cell's** existing data (read‑only). Compose it. Run Hˢ. Watch the advisory.
2. Compare its early flags against your real maintenance events — *the honest test.*
3. If it earns trust, roll to a line; later, add the gated nudge behind Breaker 16.

Each step is small and reversible. **If a step fails, that is information — the failure points the way.** A
good solution to a hard problem is worth testing precisely because you learn either way.

## Step 6 — where to go deeper

`CONCEPT_AND_MATH.md` (the math) → `NORDSON_CASE.md` / `FUJI_SMT_CASE.md` (your equipment) →
`PHYSICAL_IMPLEMENTATION.md` (how to wire it) → the engine, the manuals (`../../manuals/`), and the conformance
check (`hs_gold_fixtures.py --verify`) so you can prove the tool to yourself.

*The whole promise in one line: read your line's compositions with one deterministic, auditable instrument —
catch drift in the ratios early, read placement exactly, keep each cell healthy behind your own breaker.*

*Tiers: T1 the receipted demos · T2 the equipment mapping · T3 deployment (to earn; no vendor relationship
implied). Peter is the sole gate; nothing posted.*
