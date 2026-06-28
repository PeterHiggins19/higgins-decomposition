# Where Hˢ actually stands — an honest competitive scoping (incl. SO(4))

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-22. A sober
answer to "how many systems use SO(4)-like computation, is Hˢ's SO(4) use real, are we the leader, and who
competes on our terms." Its main job is to **scope the "leader" claim honestly** so it does not become mortar.
Tiered; conforms to the Proof & Honesty Standard. Nothing posted; Peter is the sole gate.*

---

## 1. SO(4) / quaternion computation is huge and mature — Hˢ is **not** a leader there

Quaternion (SO(3) / Spin(3)) and dual-quaternion / SO(4) / Spin(4) computation is **ubiquitous and decades
old** across established fields (general engineering knowledge, not an Hˢ result):

- **Spacecraft attitude (ADCS)** — quaternions are the standard attitude representation on essentially every
  satellite (no gimbal lock; stable kinematics).
- **Robotics & SLAM** — quaternions and **dual quaternions** for rigid-body pose (rotation + translation),
  kinematics, screw motion, and pose-graph optimisation.
- **Computer graphics / game engines** — quaternion rotation and **dual-quaternion skinning** are textbook.
- **Molecular dynamics / structural biology** — quaternion superposition / RMSD alignment.
- **Physics** — Spin(4) and the self-dual/anti-self-dual split in gauge theory, instantons, twistors; the
  hydrogen atom's hidden SO(4); Riemann–Silberstein two-helicity light.
- **Quantum computing / signal processing / vision** — SU(2)/Bloch sphere, quaternion transforms, rotation
  averaging, pose estimation.

So **the math is owned by mature communities.** Any claim that Hˢ leads "SO(4) computation" or "high-
dimensional analysis" broadly would be false — those spaces contain giants (the CoDa community; all of
robotics/graphics; the whole ML/manifold-learning field).

## 2. Hˢ's SO(4) use is real but **still a proposal (T2)** — be exact

Hˢ does **not** ship an SO(4) capability today. What is **measured (T1)** is the *D=4 SO(3)* exact rung (the
sandwich `q v q*`) and its tiling. The **SO(4)/Spin(4)** material is a **future component (T2)**: the verified
left/right generators, and the *dual-quaternion 6-DOF* direction (rotation + translation as one exact object),
whose first prototype is **named but not built** (`frontier/SO4_SPIN4_FUTURE_COMPONENT.md` §3, §5). The
honest status: *a sound, well-posed mapping awaiting one worked, receipted construction.*

## 3. The actual niche — narrow, distinctive, and the only honest place to say "leader"

Hˢ's distinctive position is **not** SO(4), and **not** "high-D analysis." It is a specific *intersection*:

> **the exact, deterministic, hash-receipted reading of compositions** (parts of a conserved whole, Aitchison
> geometry) **as kinematics** — the message in the ratios, read to the IEEE floor, tiled to scale, with guards
> that withhold when the evidence is thin.

That intersection is genuinely uncommon. **But defining your own terms means few compete on them — which is a
real differentiator *and* a thin moat.** The moat is only as wide as the demand for *exactness + determinism +
receipts* on *compositional* problems — which the three measured witnesses (microbiome, mudstone, fleet)
suggest is real in at least those domains, and unproven beyond them.

## 4. Who competes "on Hˢ's terms" right now — honestly

- **Compositional-data (CoDa) software** — `compositions`, `robCompositions`, `zCompositions`, `easyCODA`.
  These own log-ratio analysis and are mature, but they **do not** treat determinism, a conformance hash, an
  explicit withholding guard, the quaternion/Spin(4) exact reading, or the kinematic ("navigation") layer as
  first-class. *Closest neighbours; they compete on CoDa, not on the exact/deterministic/kinematic combination.*
- **The SO(4)/dual-quaternion world** (robotics/graphics/SLAM) — owns the geometry, but **not on compositions**
  (conserved-budget data); different problem.
- **Stochastic Portfolio Theory / manifold learning / ML** — adjacent readers of high-D structure, but
  model-based or statistical, **not** deterministic-exact-receipted.

**On the exact intersection (§3), direct competition is thin.** Stated without triumph: that is partly because
the intersection is *self-defined*; thin competition on terms you set yourself is not the same as market
leadership. The honest claim is **"a credible, distinctive niche with a few real use cases and a thin-but-real
moat,"** not "leader of a field."

## 5. "If we don't do it, who will?" — the honest answer

The honest answer is the project's own doctrine, not a territorial claim:

- **The moat is reproducible by anyone who adopts the discipline** — determinism + exactness + receipts +
  honest tiers. That is a *feature*, not a vulnerability: it means the contribution survives even if someone
  else builds it, because it is checkable. Leadership here is **earned by receipts, not claimed by priority.**
- So the answer to "who will" is: *whoever measures it first and shows the receipt.* The way to lead is to
  **ship the one decisive prototype** (the dual-quaternion 6-DOF demo; the storm-backtest) — a measured result
  beats a positioning statement every time. The invitation is open (`library/FOR_THE_NEXT_EXPLORER.md`); the
  lead is held only as long as the receipts are freshest.

## 6. Tiers

- **T1 (measured):** the D=4 SO(3) exact rung + tiling; the three witnesses; determinism + receipts.
- **T2 (reasoned):** the SO(4)/dual-quaternion direction; the "distinctive intersection" niche.
- **T3 (open / not claimed):** any "leader of high-D analysis" or "leader of SO(4)" claim — **rejected**;
  market/real-world leadership beyond the measured domains — **unproven**; the SO(4) capability itself —
  **not yet built.**

*The exact, deterministic, receipted compositional reading is a real and distinctive thing; SO(4) is a
promising future component, not a shipped advantage; "leader" is honest only for the narrow self-defined niche;
and the only durable lead is the next measured receipt. Cross-refs: `frontier/SO4_SPIN4_FUTURE_COMPONENT.md`,
`PROOF_AND_HONESTY_STANDARD.md`, `library/FOR_THE_NEXT_EXPLORER.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide. See [`PROOF_AND_HONESTY_STANDARD.md`](PROOF_AND_HONESTY_STANDARD.md).*
