# The law, the components, and the gap — the return signal is where you refine (back-EMF)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter's
turn from the unanswerable to the workable: the question of higher-dimensional control is confounded by any
number of knowns in the system, so don't chase it — instead *"use the total answer, including what just popped
out, work backwards to where the gap happened, and focus there."* The system **is under law**; so **measure
the law, the components, and the gaps, coherently** — and the **return signal** (the part that pops out,
unexplained) shows where to refine, **like back-EMF.** Made an instrument: `law_components_gaps.py` (receipt
`a70234691986199c`). Honest-broker tiered; Peter is the sole gate; nothing posted.*

---

## The move (from the cosmic question back to the bench)

The directed-universe study ended at a wall: from inside, a directed path can't be told from a lawful one
(Breaker 16). Peter's response is not to push on the wall but to **turn around and use what the measurement
left in your hands.** The total answer has two parts — the part the **law** explains, and the part that
**pops out** unexplained (the residual). The unexplained part is not noise to discard; it is the **return
signal**, and it points, backwards, to **exactly where the gap opened.** Focus there. That is the whole method,
and it is the diagnostic-constructive duality once more: *the same math that finds the flaw refines the system.*

## Back-EMF — why the return signal is the right thing to read

In a motor, **back-EMF** is the voltage the motor's own motion sends back against the drive. You don't fight
it — you **read** it: it tells you the rotor's state, and sensorless controllers steer on it without a separate
sensor. The compositional analogue: fit the law, and the system's own **residual return** — `data − law` —
carries the information about where it departs from the law. You don't need an external oracle for "where is
the problem"; the system tells you, through what it returns. The gap *is* the sensor.

## The instrument (measured, receipted)

`law_components_gaps.py` runs the full loop on a lawful system with one hidden gap injected (a bump in
component 2 over a window), receipt `a70234691986199c`:

1. **Measure the law.** Fit the smooth, lawful clr trajectory per component — the known part, *measured, not
   re-derived.*
2. **Read the components.** The clr components are the parts of the budget.
3. **Take the gap = the return signal.** `residual = clr(data) − clr(law)`. The back-EMF.
4. **Work backwards — localize.** Residual energy by component: **[0.25, 0.22, 3.44, 0.23, 0.27]** — component
   2 carries **~13×** the rest. The gap is found, and its **window** recovered ([46–55], inside the true
   [40–60]). You now know *where* to focus, from the return alone.
5. **Verify coherently.** A *second, independent* statistic (max single-step deviation) points to the **same
   component 2.** Two different maths, one answer — the triad cross-check; the gap is real, not an artifact.
6. **Refine (the back-EMF loop).** Feed the located gap back into the law and re-read: residual energy drops
   **4.415 → 1.633, −63%.** The return signal, used, refined the system.

All four checks pass: right component, two routes agree, window overlaps, residual collapses. The method does
what Peter described — total answer → backwards to the gap → focus → refine, coherently.

## Why this is the efficient path

You do **not** re-derive the law (it's known — measure it and move on), and you do **not** chase the
unmeasurable (whether the law is "directed" — Breaker 16). You spend all the effort on the **gap**, which is
where the unmodeled physics, the drift, or the next refinement actually lives — and the system *hands you its
location* through the return signal. That is the cheapest possible search: the residual is both the alarm and
the map. "Departure from uniform is where the information lives" (the duality's internal origin), turned into a
control loop.

## Honest scope

- **T1 (measured):** the localization (component 2, ~13× energy), the two-route coherence, the window
  recovery, and the −63% residual drop are measured and reproduce (`a70234691986199c`).
- **T2 (the method / doctrine):** "measure law + components + gaps coherently; refine on the return signal" is
  a general method, demonstrated here on a synthetic lawful system; real deployment needs the **domain's
  actual law**, not a fitted smooth stand-in. Back-EMF is an analogy for the return signal, not a circuit
  claim.
- **The fence that matters:** the residual localizes **where** a gap is; it does **not** name **why** —
  attributing a cause to the gap (unmodeled physics vs new law vs design) is the operator's implication leap,
  **Breaker 16.** The instrument finds and refines; the meaning stays the human's. **Nothing posted; Peter is
  the sole gate.**

*Cross-refs: `law_components_gaps.py`, `../simulations/directed-universe/THE_INSTRUMENT_TURNED_OUTWARD.md` (the
wall this turns back from), `../huf-gov/THE_IMPLICATION_LEAP_IS_BREAKER_16.md` (where-not-why = the leap),
`../papers/diagnostic-constructive-duality/THE_DIAGNOSTIC_CONSTRUCTIVE_DUALITY.md` (same math finds and fixes),
`../HCI-ULTRASOUND/THE_FILTER_INJECTION_PROBE.md` (inject known, read the return as perturbed — the same return-signal idea).
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the law is measured not re-derived · the gap is localized by two coherent routes ·
the return signal refines the system (−63%, receipted) · where-not-why keeps the cause as the operator's leap ·
the human keeps the gate.*
