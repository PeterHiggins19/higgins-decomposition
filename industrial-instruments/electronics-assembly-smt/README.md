# Electronics‑Assembly SMT — compositional sensing & control for dispense and placement (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑23. **Internal,
planning‑stage** application study: applying the Hˢ compositional instrument and the distributed robotic system
model to electronics‑assembly equipment — **Nordson‑class** fluid dispense/coat/inspect and **Fuji‑class** SMT
placement. Built to grow: fill in ideas as they come. **No contact, partnership, or endorsement with any named
manufacturer is implied or sought** — "Nordson‑class" and "Fuji‑class" name *equipment domains* as planning
examples. Honest‑broker tiered; nothing posted; Peter is the sole gate.*

---

## The one‑paragraph case

An SMT line already *is* a chain of compositions. A **dispense** (solder paste, adhesive, underfill, coating)
is a composition over its quality budget — volume, height, footprint, voids, and material shares. A
**placement** is a 6‑DOF pose (rotation + translation) — exactly the dual‑quaternion object Hˢ reads to the
IEEE floor. A **cell's health** is a composition over its subsystems. So the instrument that reads compositions
reads this line natively: it catches **process drift in the ratios before any single‑channel alarm fires**
(measured: a dispense clog flagged **20 deposits early**, `ca9e6c0d…`), reads placement pose exactly, reads
deposit/joint geometry as rotation⊕shape⊕size, and closes a self‑maintaining control loop behind the operator's
Breaker 16 (`c17e9ceb…`). One language, sensor to decision, with a receipt at every hop.

## What's in this folder (the planning skeleton)

| file | what it holds |
|---|---|
| [`CONCEPT_AND_MATH.md`](CONCEPT_AND_MATH.md) | the basic math: dispense‑as‑composition, placement‑as‑6‑DOF, deposit‑as‑deformation, drift, the cell |
| [`CONTACT_POINT_DOCTRINE.md`](CONTACT_POINT_DOCTRINE.md) | **Peter's field law:** the machine is dirty where it touches product; clean the highest‑contact points first; rank by *Rᵢ = contacts × drift* |
| [`NORDSON_CASE.md`](NORDSON_CASE.md) | dispense / coat / inspect — the fluid composition + deposit geometry + early drift |
| [`FUJI_SMT_CASE.md`](FUJI_SMT_CASE.md) | placement 6‑DOF pose + feeder/nozzle health + the cell budget |
| [`PHYSICAL_IMPLEMENTATION.md`](PHYSICAL_IMPLEMENTATION.md) | how to accomplish it physically — the sensing skin, edge nodes, data taps, the loop |
| [`FUTURE_PROJECTS_FIBER_AND_Hs.md`](FUTURE_PROJECTS_FIBER_AND_Hs.md) | **reach‑for‑the‑stars:** fiber optics × Hˢ in the photonics‑packaging future of both domains — common‑mode rejection in glass (310 dB), fiber‑as‑skin, fiber‑as‑pathway, active alignment, validated on public data |
| [`COHERENCE_AND_LASERS.md`](COHERENCE_AND_LASERS.md) | the keystone: **Hˢ rejection = source coherence** — the law *suppression ≈ −10·log10(1−ρ)* (one "9" of coherence = 10 dB); Hˢ reads coherence back and gates on it |
| [`ONBOARDING_FROM_ZERO.md`](ONBOARDING_FROM_ZERO.md) | teach a group blind to every aspect, from nothing |
| `dispense_drift.py` | the planning anchor demo (the 20‑deposit early‑flag receipt) |

## Why now (and the honest stance)

Hˢ and HUF are ready; the open work is **making it real** — offering the exact system, the code, and the
how‑to‑use to a group that is blind to every aspect. A complex problem with a good solution is worth testing
*even if it fails*, because the failure points the way. So this folder is a **test of the journey**: it states
the case, the math, and a physical path, and invites the build. **T1** = the receipted anchors (dispense drift,
the closed loop, the 6‑DOF read, the deformation read); **T2** = the equipment mappings and the physical
proposal (reasoned, planning); **T3** = any deployment, any vendor relationship — to earn; none implied.

*Cross‑refs: `../../papers/frontier/DISTRIBUTED_COMPOSITIONAL_ROBOTIC_SYSTEM.md`, `../../library/THE_LANGUAGE_OF_Hs.md`,
`../../papers/frontier/SO4_SPIN4_FUTURE_COMPONENT.md` (6‑DOF), `../../papers/frontier/COMPOSITIONAL_DEFORMATION_SENSING.md`,
`../../experiments/robotic_workcell_2026-06/`, `../../huf-gov/COMPONENT_REQUEST_ESCALATION_DOCTRINE.md` (Breaker 16).
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited‑or‑fenced · math proven + receipted · value shown · experts decide.*
