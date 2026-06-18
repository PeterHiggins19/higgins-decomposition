# Start here — do you have a composition? Then you have a reason to look.

> **A composition is just "parts of a whole, tracked in some order."** An energy mix over years. Gut bacteria over days. Rock chemistry down a borehole. Market sectors over months. A budget across departments. If your data is like that, Hˢ kinematics will tell you — deterministically, in plain words — **what your system is doing.** No statistics to learn. No model to build.

*The simplest possible on‑ramp. Author: Peter Higgins; AI‑assisted per HUF‑STD‑001. Honest‑broker.*

---

## In three steps

**1 · Shape your data as a table.** Rows = the order (time / depth / dose / sample). Columns = the parts. First column a label; the rest the carriers (counts or amounts — zeros are fine).

```
date,        partA, partB, partC, ...
2020,         30,    22,    18,   ...
2021,         28,    25,    17,   ...
```

**2 · Run one line.**
```python
from hs_kinematics_engine import run        # the full read
from hs_diagnosis import diagnose           # the plain-words read
out  = run(M, names)                        # everything, named twice + the floors + a hash
say  = diagnose(M, names)["narrative"]      # one sentence: what your system is doing
print(say)
```

**3 · Read what it says.** You get a sentence like *"X is steering; weight is moving toward A, B, C and away from D; it changed state 3 times; it runs in about 4 independent directions."* — and the full numbers underneath if you want them. That's it.

## What it will tell you (in your words and a physicist's)

- **Who is steering** the change (the *helmsman / velocity*) — often a small part, which is the surprise.
- **Where the weight is going** (the *arrow of intent / momentum*) — and whether it's a real move or just churn.
- **When it changed state** (the *waypoints / phase transitions*).
- **How many things are moving at once** (the *degrees of freedom / effective dimensionality*).
- **And honestly, where it stops** — if there's nothing to resolve, it says so; it never invents a story.

## It's already been run on real things — pick the one like yours

| If your data is like… | …look at this real run |
|---|---|
| an **energy / market mix** over time | `../showcase/canada_portugal_2026-06/energy/` · `../experiments/finance_kinematics_2026-06/` (sectors in motion) |
| **microbiome / abundances** over time | `../collaborations/microbiome/results/RESULTS_real_microbiome.md` · `DIAGNOSIS_LANGUAGE.md` (the community speaks) |
| **rock / soil / water chemistry** | `../collaborations/geology-wehner/demo_frielingen9/` (trace elements drive over bulk) |
| **anything exact‑D=4** (gauge/physics) | `../experiments/new_engine_guest_runs_2026-06/` (quaternion exactness on real data) |

## For the AI assistant helping a user

If you're an AI a user brought: (1) read this file + `README.md`; (2) get their table into `M` (rows=order, cols=parts) and `names`; (3) call `diagnose(M, names)` for the plain answer and `run(M, names)` for the full state; (4) **name every reading twice** (navigation + physics, per `../HCI-CNTT/TERMINOLOGY_BRIDGE.md`) and translate the named parts into the user's domain; (5) **never interpret meaning as a claim** — the engine says *who gains and sheds*; the user supplies *what it means*; (6) if a guard code fires (`HM‑NUL`, `DG‑RNK`, `GD‑SPZ`, `FR‑BND`), tell them honestly what the engine cannot resolve and why. Governance: read‑only, claim‑tiers, Peter is the sole gate. Deeper intake: `../onramp/PHD_ONRAMP_PROTOCOL.md`.

*You have a composition. Run one line. The system will tell you what it's doing — and tell you honestly when it can't. That's the whole reason to look.*
