# Concept & basic math — the SMT line as a chain of compositions

*Internal · planning. Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001.
2026‑06‑23. The minimum math to see why the Hˢ instrument reads an electronics‑assembly line natively. Honest‑
broker tiered; nothing posted; Peter is the sole gate.*

---

## 1. The four objects, and the one operation

| object on the line | the composition / exact object | the Hˢ read |
|---|---|---|
| **a dispense deposit** | quality budget `{volume, height, footprint, voids}` (parts of one deposit) + material shares `{metal, flux, solvent}` | closure → log‑ratio → arrow / character / silent‑drift |
| **a placement** | a **6‑DOF pose** = rotation `R` (unit quaternion, exact) + translation `t` (dual quaternion) | the SO(4)/dual‑quaternion 6‑DOF read, to the IEEE floor |
| **a deposit / joint geometry** | deformation gradient `F = R·U` → rotation ⊕ shape (stretch composition) ⊕ size (volume) | the compositional deformation read |
| **a work cell's health** | `{placement, thermal, feeder, throughput}` (a conserved health budget) | the cell composition in motion; the closed loop |

**One operation** runs on all four: closure (`c = x/Σx`, which rejects any common gain — a global level/flow
change cannot fool it), the isometric log‑ratio (`ilr`), the kinematic read, the coherence gate, and a SHA‑256
receipt. Detect, transmit, decode, decide, and act are therefore **one language** end to end.

## 2. Why the ratios catch faults early (the core value)

A deposit can have every single channel in spec while the *ratios* are already moving — a nozzle clog lowers
volume and raises voids together, the **silent (ratio‑blind) drift** that level/threshold monitors miss. The
log‑ratio read sees it first. *Measured (planning anchor):* a simulated clog flagged in the ratios **20
deposits before** the single‑channel volume alarm fired (`ca9e6c0d…`, `dispense_drift.py`). The same logic is
the fleet/fault‑location signal already measured on a real drive fleet (159 silent‑drift events, `058fde30`).

## 3. Why placement is exactly a quaternion (the exact rung)

A placement is a rigid motion: rotate the part (`R ∈ SO(3)`) and translate it (`t`). The rotation is **exactly**
a unit quaternion (the D=4 rung, `q v q*` to ≈10⁻¹⁶); rotation+translation together are a **dual quaternion**
(SE(3), the 6‑DOF read). So a Fuji‑class placement's orientation and offset are read as one exact object, and a
*sheet* of placements is a deformation/registration field over the board (the skin of sensors).

## 4. The cell, and the loop (cross‑flow)

The cell health composition is driven toward a healthy **setpoint** (homeostasis) by a SafeLoop — sensing flows
**up**, control flows **down**, and the operator's **Breaker 16** is the fixed point (control only when armed).
*Measured:* armed → the cell holds at the setpoint; tripped → it drifts to fault; a governing node locates the
worst cell across a fleet, hash‑verified (`c17e9ceb…`). Scale is by composition of compositions: deposit → pad
→ board → cell → line → plant, the same operation, more dimension, more sensitivity.

## 5. Tiers

- **T1 (measured):** dispense silent‑drift early flag (`ca9e6c0d`); the closed‑loop cross‑flow (`c17e9ceb`);
  the exact 6‑DOF read; the deformation read (`6e9426ac`).
- **T2 (reasoned):** the equipment mappings (dispense/placement/cell as compositions) — sound, planning.
- **T3 (to earn):** real‑line data, hardware integration, vendor relationships — none implied.

*Cross‑refs: `NORDSON_CASE.md`, `FUJI_SMT_CASE.md`, `PHYSICAL_IMPLEMENTATION.md`,
`../../papers/frontier/SO4_SPIN4_FUTURE_COMPONENT.md`, `../../library/THE_BLINDNESS_SUITE.md`. Peter is the sole gate.*
