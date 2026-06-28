# The distributed Carnot engine — an orbital data‑center constellation read as a thermodynamic composition

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑22. An
extension of the constellation study: read a fleet of **compute satellites** as a *distributed heat engine*
whose conserved budget — solar power in → useful computation out → waste heat radiated to space — is a
**composition**, and orchestrate it with the HUF control surface toward maximum performance within the
thermodynamic limit. Honest‑broker tiered: the real‑world programs are facts (cited); the composition framing
is established physics applied (T2); the orbital optimisation is a proposal (T3); **no orbital data is read
here.** The one caveat that must hold — information entropy is **not** thermodynamic entropy — is stated in
§7. Names off the public repo; no contact with any party; Peter is the sole gate; nothing posted.*

---

## 1. Why now (the real frontier, not a metaphor)

Orbital data centers are being filed and flown **right now**: SpaceX has filed with the FCC for ~**1 million**
solar‑powered orbital data‑center satellites (~100 GW/yr of AI compute); **Starcloud** filed for ~88,000 and
has already run an NVIDIA H100‑class system and an LLM in orbit; **Blue Origin** filed ~51,600; **Google's
Project Suncatcher** (Nov 2025) targets TPU data centers in space with prototypes by early 2027. Every one of
them names the same binding constraint: in vacuum the **only** way to shed heat is **radiation** — there is no
air to convect into. A compute satellite is therefore, unavoidably, a **heat engine**: power in, work
(computation) out, heat rejected to a cold sink. A fleet of them is a **distributed Carnot‑engine
composition** — exactly the conserved‑budget object this whole project began on.

## 2. It is the ground state, at orbital scale (the grounding — T2)

The Hˢ origin is a loudspeaker: a **conserved energy budget apportioned across parts** (the simplex). A
compute satellite is the *same object*: its input power is conserved and apportioned across

> `(useful computation · communication · station‑keeping/attitude · rejected heat + losses)`

— a four‑part composition that closes to the total power drawn. So the engine's machinery applies **unchanged**:
the exact D=4 rung reads the per‑satellite energy budget to the IEEE floor; tiling carries it to fleet scale;
the read is deterministic and hash‑receipted. The acoustic origin returns as thermodynamics — the budget that
became the simplex is now a power budget in orbit. *This is why the framing is not a stretch: an energy budget
is a textbook composition, and Hˢ is a composition reader.*

## 3. The Carnot frame (established physics — T2)

A heat engine's efficiency is bounded by `η_C = 1 − T_c/T_h`. In orbit:

- **The cold side is radiative.** Rejected power `P_rad = ε σ A (T_r⁴ − T_space⁴) ≈ ε σ A T_r⁴` (the
  ~2.7 K background is negligible against a radiator at hundreds of K). The **radiator area A and temperature
  T_r set the ceiling on compute power** — you can only compute as fast as you can radiate.
- **"Engineering hot" is a real, constrained optimum.** Because radiated power scales as `T⁴`, running the
  radiators (and junctions) **hotter** rejects dramatically more heat per unit area — more compute per
  kilogram of radiator. But hotter silicon raises leakage and fails sooner. So "run hot to efficiency" is a
  **constrained maximisation**: push `T_h` up for throughput density, against a reliability/leakage wall —
  exactly the kind of *push‑to‑the‑limit* trade the HUF control is built to hold, with a breaker at the wall.

## 4. The fleet as one distributed engine (the reach — T3)

The fleet is not N independent engines; it is **one engine with N cylinders**, and the budget moves:

- **Power follows the sun.** Input swings with eclipse, beta angle, and pointing; the **moving budget** (the
  size co‑tracker) is the total fleet compute capacity rising and falling with available power.
- **Load‑balance work *and* heat.** Route computation to units that have power *and* radiator headroom; let
  others idle‑cool; phase the fleet so the aggregate runs near its thermodynamic ceiling without any single
  unit tipping into thermal runaway.
- **The FCI gains a thermodynamic coherence term** `C_thermo` — how coherently the fleet's power→work→heat
  budgets move together — composed up the tetrahedral/3ⁿ tree alongside the geometric/kinematic/spectral
  terms. **Radiator saturation / thermal runaway is a breaker** at the node; the operator holds the last one.

## 5. HUF control, pushed to maximum performance (the reach — T3)

The control loop is the one already specified, with the thermodynamic composition as a new carrier set:
**read** each unit's power budget + the fleet aggregate; **gauge** it (within thermal+coherence limits = GO;
approaching the radiator/Carnot wall = CAUTION; violation = HALT); **orchestrate** to maximise aggregate
useful computation subject to the radiator ceiling, the Carnot bound, and the coherence constraint; **gate**
at the operator. Maximum performance is *defined by the physics, not guessed*: the fleet's compute throughput
is bounded by total radiated power, and the job of the control layer is to ride that bound coherently —
"engineering hot," distributed, breakered.

## 6. What we already hold on the ground (the measured precedent — T1)

We do not have orbital data, but we **do** have a real data‑center fleet read: **Backblaze** (Witness III)
reads a drive fleet as a four‑part composition that already includes a **Thermal** carrier, with 159
silent‑drift pre‑fault events caught (`058fde30806a8e6b`). A terrestrial data center is the *same object with
an easier heat sink*; the orbital one is the same read with **radiation as the only path**. So the
ground‑based prototype is buildable now from public data‑center power/thermal telemetry (PUE, thermal
time‑series), and it is the honest first rung beneath any orbital claim.

## 7. The caveat that must hold — information entropy is **not** thermodynamic entropy

This is the load‑bearing honest line, and the elder will press it: the "entropy" in EITT and the CMP is the
**Shannon entropy of a composition** (an information quantity), **not** the **thermodynamic entropy** (heat ÷
temperature) of the Carnot cycle. They are *structurally analogous*, and **Landauer's principle** (erasing a
bit costs at least `kT ln 2` of heat) is a genuine physical bridge between computation and heat worth testing
— but they are **distinct quantities, and the engine does not derive the Carnot bound or compute physical
entropy.** What Hˢ legitimately reads is the **energy budget as a composition** (energy is conserved and
apportioned — a real composition); the thermodynamic physics (η_C, radiative rejection, the second law) is the
**established domain science the read sits alongside**, not something Hˢ produces. *Conflating the two would be
exactly the overclaim the project exists to refuse.*

## 8. Tiers, what would make it real, and the gate

- **T1 (fact/measured):** the real‑world programs (SpaceX/Starcloud/Blue Origin/Google filings, cited); the
  Backblaze terrestrial data‑center fleet read (incl. Thermal); the exact D=4 rung + determinism the energy
  budget would be read with.
- **T2 (established/reasoned):** the energy budget as a composition; the Carnot/radiative‑rejection physics;
  the Landauer link as a testable bridge.
- **T3 (proposal):** the distributed‑Carnot orchestration, the `C_thermo` FCI term, "engineering hot"
  optimisation, the max‑performance control — **no orbital data; no performance number claimed.**
- **What would make it real:** (a) a ground prototype on a **public data‑center power/thermal composition**
  (does the compositional read track efficiency / lead a thermal pre‑fault, as on Backblaze?); (b) the same
  read on **published satellite thermal/power telemetry** when available; (c) a worked Landauer‑bound
  comparison on a real compute‑energy series. Real data, receipted; a null reported where found.
- **Gate & safety:** thermal runaway is a node breaker; the operator holds the last breaker; full automation
  never possible; no external contact; names off the public repo; Peter is the sole gate.

*Cross‑refs: `README.md`, `CONCEPT_AND_VALUE.md`, `FLEET_COHERENCE_METRIC.md`,
`THE_V_CORE_AND_THE_GROUNDED_EVIDENCE.md`, `../../papers/THE_HUF_CONSTELLATION_SYSTEM_PROPOSAL.md`,
`../../papers/triangulation/W3_FLEET_WITNESS.md` (the terrestrial data‑center precedent),
`../../RWA/THE_GROUND_STATE.md` (the energy‑budget origin). The energy budget that became the simplex is now a
power budget in orbit — read it, don't mythologise it. Peter is the sole gate; nothing posted.*

Sources: [SpaceX/Starcloud/Suncatcher overview (Fierce Network)](https://www.fierce-network.com/cloud/space-data-centers-starcloud-spacex-and-project-suncatcher-explained), [Orbital data‑center race 2026 (Introl)](https://introl.com/blog/orbital-data-centers-space-computing-race-2026), [Space‑based data center (Wikipedia)](https://en.wikipedia.org/wiki/Space-based_data_center).
