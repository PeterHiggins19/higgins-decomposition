# Hˢ kinematics — the full system in one read, explained

> **The working name, from 2026‑06‑14.** This is where the matured instrument lives as one engine: it reads the *most a composition can be known to say*, with honest confidence, **named for the navigator and the physicist at once**, and revealed **down to the computational floor**. New work uses this convention.

*Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker. The engine is `hs_kinematics_engine.py` (numpy only; deterministic; hash‑receipted). It is the distilled engine — the frozen‑oracle binary adds the depth‑tower/IR/CNQ recursion. Naming + lineage: `../NAMING_AND_FRINGE_ARCHITECTURE_2026-06-14.md`; vocabulary: `../HCI-CNTT/TERMINOLOGY_BRIDGE.md`; the mechanics derivation: `../HCI-CNTT/COMPOSITIONAL_MECHANICS.md`.*

---

## What it is, plainly

Give it a table of **parts of a whole, tracked in order** (an energy mix over years, ions down a borehole, taxa over days). It tells you the complete, deterministic story of how that mixture *moves* — who is steering, where the weight is going, how sharply it is turning, when it changed state, how concentrated it is, and exactly **where the data stops being able to tell you more.** Every reading is named twice so you can use the word your field uses, and it ends with a receipt (a hash) so anyone, anywhere, gets the same answer.

## What it reads (each named for the navigator / the physicist)

- **Position** — where the mixture sits (`clr`).
- **Dead reckoning / lossless reconstruction** — the whole high‑dimensional structure rebuilt exactly from overlapping 4‑part charts, to the **IEEE floor (~1e‑15)**.
- **Helmsman (the steerer) / velocity** — which part is steering the change (often a *small* one — that's the point).
- **Effective spread / entropy** — concentrated vs spread out.
- **Waypoints / phase transitions** — when the system genuinely changed state.
- **The jet: drift→change‑of‑drift→lurch / velocity→acceleration→jerk** — the motion and its rates, computed **only as deep as the noise allows** (the engine reports the deepest derivative still signal — its **sensor limit / Nyquist‑noise floor**).
- **Turn rate / curvature** — how sharply the path bends.
- **Arrow of intent / momentum** — where the *weight* of the mixture is flowing (mass × velocity), and whether it's a real arrow or churn (coherence).
- **Reshaping pressure / force**, **activity / kinetic energy**, **circulation / angular momentum**, **transit effort / action** — the dynamics.
- **Course directness / path efficiency** — a straight, purposeful move (≈1) vs wandering (≈0).
- **Degrees of freedom / effective dimensionality** + the **motion modes** — how many independent directions are really moving.
- **Station‑keeping / equilibrium hold** — it *holds* when the motion is below its own discovered noise floor, and lists the genuine structural changes.
- **The guards** — it says, in codes, when it **cannot** resolve something (a noise leader at rest, a tie, a collapsed rank, too many zeros).

## EITT — explained, and its new job

**EITT** (the Entropy‑Invariant Time Transformer) is one of the old tools that got us here, and it still holds something. Here is the whole idea in one breath: if you take a structured composition and **average it down in time using the geometric mean** (the CoDa‑correct average), its **Shannon entropy barely changes** — the information *survives the compression*. That near‑invariance is a fingerprint of real temporal structure.

Its **new job** in this engine is a **boundary test**: when the entropy *does* drift under that averaging, the region has lost coherent structure — you've reached the **edge of what is analysable**, the boundary where the deterministic read runs out. So EITT now marks the fringe. It lives in the **Tier‑3 fringe layer** — *a clue for a human to look closer, never a claim.* (Demonstrated: a real energy series stays within‑regime; a structureless white mixture is flagged `FR‑BND‑INF`.)

## The floor — what "down to the computational floor" means

The engine ends by **showing its own limits**, because an honest instrument states where it stops: the **IEEE reconstruction floor** (how exact the lossless rebuild is), the **determinism precision** (12 decimals, so the receipt matches across machines), the **discovered noise floor** (the resting‑motion level it calibrated from your data), and the **maximum meaningful derivative order** (how deep the jet stays signal). Nothing is hidden below the floor; the floor is reported.

## Run it

```
python hs_kinematics_engine.py                 # built-in demo
```
or in code:
```python
from hs_kinematics_engine import run
out = run(M, names)     # M: rows = time/sample, cols = parts ; names: the carriers
```
`out` is the complete dual‑named state, with the floors and a `content_hash`. Replace the demo's `M, names` with your own — that's all.

## It can also speak — the diagnosis language

`hs_diagnosis.py` composes the same deterministic readings into **plain sentences**, and the language **expands with complexity**: a 2‑part system says a word or two; a real microbiome names a dozen taxa and says which are gaining vs shedding, how many directions the motion runs in, and when it changed state — *"g__Prevotella is steering (gaining); weight is moving toward … and away from Bacteroides …; concentrating."* Deterministic (same data → same words → same hash); the words are a description, the meaning is the expert's. See `DIAGNOSIS_LANGUAGE.md`.

## Reproducibility kit + full specification (v1.0, post‑Coimbra)

The engine is now a complete, portable platform — everything a reviewer, a porter, or a guest needs to reproduce and trust it:

- **[`HS_KINEMATICS_SPECIFICATION.md`](HS_KINEMATICS_SPECIFICATION.md)** — the full designer‑level spec: input contract, every stage (geometry → carrier guard → lossless tiling → navigation → guards → mechanics → spectral → fringe → hash), the output schema, the claim tiers, and the **conformance anchor**.
- **[`HS_KINEMATICS_PSEUDOCODE.md`](HS_KINEMATICS_PSEUDOCODE.md)** — language‑agnostic pseudocode; re‑implement in any language and check the hash.
- **[`hs_kinematics.R`](hs_kinematics.R)** — a 1:1 R port, **offered as‑is** (neither author nor the build sandbox could run R), provided *with* the pseudocode + Python + spec so an experienced R user can check and correct it against those three references; it likely works, the intent is cross‑platform usefulness, and fixes are welcome — conformance gate is the same reference hash.
- **[`HS_KINEMATICS_REPLICATION.ipynb`](HS_KINEMATICS_REPLICATION.ipynb)** — annotated notebook that runs the reference, reads every quantity, speaks the diagnosis, and asserts the determinism receipt.
- **[`DATA_PREP.md`](DATA_PREP.md)** / [`hs_data_prep.py`](hs_data_prep.py) — make any data zip / CSV / xlsx engine‑ready by streaming.
- **[`hs_budget.py`](hs_budget.py)** / [`MOVING_BUDGET_AND_CONTROL_PRIMITIVE.md`](MOVING_BUDGET_AND_CONTROL_PRIMITIVE.md) — the **moving‑budget co‑tracker**: the engine reads the *shape* (scale‑free mix); this reads the *size* (the total/budget) in motion — growth rate, budget regimes, coherence, and size–shape coupling. For control of a budgeted dynamic system you need both (e.g. real EMBER: same transition shape, but China's budget ×7.8 steady vs Germany's ×0.88 volatile).

**Conformance anchor (the determinism receipt).** On the fixed 12×6 energy reference, the engine yields lossless reconstruction at ~1.78e‑15, effective dimensionality 1.5, max meaningful order = acceleration, noise floor 0.16009, arrow of intent → Wind/Solar (coherence 0.938), and

```
content_hash = fcae0ebe5c4f443aa076d1900d3d04219c2628591323cd7745621e740a3d7ae7
```

Any port or refactor is conformant iff it reproduces this hash on this reference; a deviation is a located signal, not noise (`../HCI-CNTT/ADAPTIVE_ANTICIPATION.md`).

## The one line

*Hˢ kinematics reads the whole motion of a composition — for the navigator and the physicist at once — as far as the data can be known and not one step further, and hands you the receipt. The instrument reads with confidence; EITT watches the boundary; the floor is always shown.*
