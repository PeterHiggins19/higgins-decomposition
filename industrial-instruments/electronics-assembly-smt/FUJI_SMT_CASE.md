# Fuji‑class SMT case — placement as a 6‑DOF pose, the cell as a composition (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑23. Planning
case for applying Hˢ to Fuji‑class SMT placement systems. **No contact, partnership, or endorsement implied** —
"Fuji‑class" names an equipment domain. Honest‑broker tiered; nothing posted; Peter is the sole gate.*

---

## 1. A placement is exactly a 6‑DOF pose (the exact rung)

Every placement is a rigid motion: rotate the part (`R ∈ SO(3)`) and translate it to the pad (`t`). Hˢ reads
this as the **dual quaternion** (SE(3)) — rotation as a unit quaternion (the D=4 rung, exact to ≈10⁻¹⁶) and
translation in one exact object. So a Fuji‑class machine's placement orientation and offset are read **exactly,
deterministically, and hash‑receipted** — and a *board* of placements is a **registration/deformation field**
(the skin of sensors over the panel): where is the board stretching, where is registration drifting.

## 2. The cell health composition

A placement cell's health is a conserved budget `{placement_accuracy, thermal, feeder/nozzle, throughput}`. Hˢ
reads it in motion: the **arrow of intent** (which subsystem is degrading), the **character** (steady vs
churn), the **rotation‑blind size events** (a throughput/level shift with no accuracy turn), and the
**silent‑drift** toward a feeder/nozzle fault before a single‑channel alarm. *Measured precedent:* the
closed‑loop self‑maintenance + fleet fault‑location, hash‑verified (`c17e9ceb…`).

## 3. Where Hˢ plugs into Fuji‑class equipment

| Fuji‑class signal | the composition / exact object | the value |
|---|---|---|
| placement vision feedback (θ, Δx, Δy) | the 6‑DOF pose (dual quaternion) | exact registration read; per‑panel deformation field |
| feeder / nozzle health | cell health budget | silent‑drift early warning + setpoint nudge (behind Breaker 16) |
| per‑head / per‑spindle balance | head‑contribution composition | which head is drifting (arrow), before placement errors |
| line throughput / WIP | a composition over stations | bottleneck/coherence read; the conductor across cells |

## 4. The honest scope

- **T1 (measured):** the exact 6‑DOF read (the SO(4)/dual‑quaternion module); the closed‑loop cell + fleet
  location (`c17e9ceb`); the deformation field read (`6e9426ac`).
- **T2 (reasoned):** the placement/feeder/head mappings — sound, planning, to run on real placement logs.
- **T3 (to earn):** deployment on real Fuji‑class equipment; any vendor relationship — none implied.
- Hˢ is a **complement** beside the placement controller, not a controller of record; the operator holds
  Breaker 16; full automation is never reached.

*Cross‑refs: `CONCEPT_AND_MATH.md`, `NORDSON_CASE.md`, `PHYSICAL_IMPLEMENTATION.md`,
`../../papers/frontier/SO4_SPIN4_FUTURE_COMPONENT.md` (6‑DOF), `../../papers/frontier/COMPOSITIONAL_DEFORMATION_SENSING.md`,
`../../experiments/robotic_workcell_2026-06/`. Peter is the sole gate; nothing posted.*
