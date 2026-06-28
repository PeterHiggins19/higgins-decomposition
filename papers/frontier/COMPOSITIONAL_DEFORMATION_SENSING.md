# Compositional deformation sensing — a sheet of quaternions reads a surface

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. A refinement
that lands the exact rung, the blindness suite, and the skin-of-sensors on a classic engineering problem:
**measuring deformation.** Quaternions and deformation are well-suited because deformation *is* rotation plus
stretch; Hˢ reads the rotation exactly and the stretch compositionally; a sheet of patches reads a surface in
detail. Receipt `6e9426ac…`. Honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## 1. The fit (why quaternions and deformation belong together)

Continuum mechanics already says the right thing: the local **deformation gradient** `F` factors by the
**polar decomposition** into `F = R·U`, where `R ∈ SO(3)` is a pure **rotation** and `U` is the symmetric
positive-definite **stretch** tensor. These are exactly the two objects Hˢ reads exactly:

- **R → a unit quaternion** (the D=4 exact rung, `q v q*` = SO(3) to the IEEE floor). The local *rotation* of a
  patch is read to machine precision.
- **U → a composition + a size.** Its principal stretches `(λ₁,λ₂,λ₃)` are parts of the deformation; closed,
  they are a **shape composition** (which direction stretched most), and their product `det U` is the **volume
  change (size)**.

So **each patch's deformation = rotation (quaternion) ⊕ shape (stretch composition) ⊕ size (volume)** — the
exact rotation/shape/size split already named in the blindness suite, now physical.

## 2. The sheet (the skin of sensors, sensing strain)

A single patch reads one local deformation; a **sheet** of patches reads a whole surface — the skin-of-sensors
manifold, where more patches = finer spatial detail (and, per dimension-is-the-message, more readable states).
Each patch contributes one `(quaternion, shape, size)` reading; the sheet is a **detailed, deterministic,
hash-receipted deformation field.**

## 3. Measured (synthetic sheet, planted bend + central stretch; `6e9426ac…`)

| quantity | result |
|---|---|
| **rotation read, clean** | residual **1.1×10⁻¹⁶** — exact quaternion (the D=4 rung) |
| rotation field, noisy (σ=0.001) | max error **0.0018 rad** across the 64-patch sheet |
| stretch field, noisy | max error **0.003** |
| decomposition | every patch split into rotation (quaternion) · shape (composition) · size (volume) |

The planted **bend** (rotation growing across the sheet, 0 → 0.8 rad) and the **central stretch bump** are both
recovered as fields: rotation exact, shape and volume compositional — a full surface deformation map from a
sheet of compositional-quaternion patches.

## 4. Where the value is (and the honest scope)

- **Value:** an exact, interpretable, deterministic, receipted surface-deformation reader — rotation to the
  floor, strain split into the engineering-meaningful *shape vs volume* parts, over an arbitrarily detailed
  sheet. Natural fits: structural-health monitoring (a skin on a wing, a bridge, a pressure vessel), tactile/
  robotic skin, geomechanics (a deforming stratum — the geology lineage), morphometrics.
- **Honest scope:** the polar decomposition and strain tensors are **standard continuum mechanics** — Hˢ does
  not reinvent them. The contribution is the **exact quaternion rotation read**, the **compositional strain
  read** (shape vs volume as a composition), and the **deterministic, hash-receipted field over a sensor
  sheet** — a measurement *discipline*, not new mechanics. T2 until run on real sensor/DIC data; the decisive
  test is a real deforming-surface dataset (digital image correlation, a strain-gauge skin) read field-wide.

## 5. Tiers

- **T1 (measured):** the exact quaternion rotation read (1.1e-16); the recovered noisy bend + stretch fields;
  the rotation/shape/size decomposition; receipt `6e9426ac…`.
- **T2 (reasoned):** the sheet as a deformation sensor; the structural-health / tactile-skin / geomechanics
  use cases — sound, demonstrated in simulation, named real-data test pending.
- **T3 (open):** any deployed deformation-sensing skin — to earn on real data.

*Cross-refs: `../../experiments/deformation_sheet_2026-06/`, `SO4_SPIN4_FUTURE_COMPONENT.md` (the dual-quaternion
6-DOF reading), `../../library/THE_BLINDNESS_SUITE.md` (rotation/shape/size), `../../library/THE_LANGUAGE_OF_Hs.md`
(the skin of sensors), `../../experiments/exact_dim4_generator_2026-06/` (the exact rung). Peter is the sole
gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
