# Compositional mechanics — the complete deterministic read, to its natural maximum

*From the momentum idea, the full chain: a compositional trajectory is a **curve on the Aitchison Riemannian manifold**, so the entire apparatus of the differential geometry of curves and classical mechanics applies — and **every quantity is a deterministic linear‑algebra reduction of the trajectory.** This is the catalogue of all values that can be determined, the physical meaning of each, and the **honest ceiling** the data imposes. Module: `engine/compositional_mechanics.py` (self‑test PASS). Reproduce: `experiments/compositional_mechanics_2026-06/run_mechanics_demo.py`. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; claim tiers at end.*

---

## The linking formula

> A composition `x(t)` tracked over an ordering is a curve `r(t) = clr(x(t))` on the simplex with the Aitchison (log‑ratio) metric. Therefore its **complete deterministic description** is its **jet** (the derivative tower), its **Frenet–Serret frame** (intrinsic geometry), its **mechanical quantities** under mass = share, its **integral invariants**, and its **spectral decomposition** — and the **natural maximum** is the derivative order `N*` at which the next derivative falls below the discovered noise floor. Every value is linear algebra; the tower is truncated by resolvability, not by choice.

This is the same honesty that runs through the engine: you compute everything the data supports, and you **stop where the next quantity is noise** — you do not take infinite derivatives of real data.

## The five families of derivable quantities

**1 · Kinematic — the jet (derivatives in time).**
`position r = clr(x)` → `velocity v = dr/dt` (the Aitchison velocity, Δclr) → `acceleration a = d²r/dt²` (is the motion speeding up / a force felt) → `jerk = d³r/dt³` (smoothness of the transition; abrupt shifts have high jerk) → `snap …`. Each finite difference amplifies noise by the white‑noise factors √2, √3, … per order, so the **amplification ratio** `‖dᵏr‖/‖dᵏ⁻¹r‖` rising toward ~2 marks the noise floor. `N*` = the deepest order with ratio < ~1.5.

**2 · Geometric — Frenet–Serret (the shape of the path).**
`speed = ‖v‖` · `curvature κ = ‖a⊥‖/‖v‖²` (the component of acceleration perpendicular to velocity — how sharply the trajectory turns) · the moving frame (tangent/normal/binormal) from `v, a`; torsion (twist out of the osculating plane) for D≥3. A straight drift has κ≈0; a turning transition has κ>0.

**3 · Dynamic — mechanics under mass = share.**
`momentum p = mass·v` (the arrow of intent, E‑29) · `force F = dp/dt` (Newton 2 — note variable mass: `F = m·a + (dm/dt)·v`) · `kinetic energy T = ½ Σ mⱼvⱼ²` (the energy of the motion) · `power = dT/dt` · `angular‑momentum bivector ‖r∧p‖` (rotational content — which carrier pairs circulate). A near‑conservation holds: `Σⱼ mⱼvⱼ ≈ 0` (closed‑system momentum), so the momentum vector is mass *redistribution*.

**4 · Integral — accumulated invariants.**
`path length = ∫‖v‖dt` (the odometer) · `displacement = ‖r(T)−r(0)‖` · **`path efficiency = displacement/path‑length ∈ [0,1]`** (straight directed drift ≈1 vs wandering ≈0) · `action = ∫T dt` (Maupertuis‑type, the trajectory's "effort") · `impulse = ∫F dt = Δp` (net momentum over a window).

**5 · Spectral — every linear‑algebra method.**
SVD of the centered trajectory → **motion modes** (singular values = the principal axes of the transition), **effective rank** (the participation ratio — true dimensionality) · **velocity‑covariance eigenstructure** (the diffusion modes; energy per mode) · the **dominant motion direction** (which carriers define the main mode) · velocity autocorrelation (persistence/memory) · the closure/CLR Jacobian (uncertainty propagation, GUM linearization). This is the "maximum determinable by linear algebra" — the complete normal‑mode picture.

## The natural maximum (the honest ceiling)

The "maximum deterministic output" is **not** an infinite tower. Each derivative loses a sample and amplifies noise; the trajectory's SNR sets `N*`. On a long, smooth, real series `N*` may reach acceleration or jerk; on short or noisy data it stops at velocity. The module computes `N*` from the amplification ratios and reports it — *the deepest level still carrying signal.* Beyond `N*` the values are real numbers but not real information, and the engine says so. This is the resolvability discipline applied to the calculus: **the maximum is where the next derivative drops below the floor.**

## Real‑data demonstration — two energy transitions, same instrument

| Quantity | **World** | **Germany** |
|---|---|---|
| Max meaningful derivative order | **2 (acceleration)** | **2 (acceleration)** — jerk ratio 1.55 → noise |
| Path efficiency | **0.95** (a near‑straight directed drift) | **0.43** (a wandering, contested path) |
| Effective rank (motion modes) | **1.27** (≈ one‑dimensional) | **2.93** (≈ three modes) |
| Curvature (median) | 1.08 (gentle) | 1.60 (turning hard) |
| Acceleration / velocity ratio | **0.42** (very smooth) | 1.34 (energetic) |
| Dominant motion carriers | Solar · Wind · Other Fossil | Other Renewables · Nuclear · Solar |

Read honestly: the **global** transition is a smooth, nearly‑straight, one‑dimensional drift toward Solar/Wind — a system moving with clear, low‑curvature intent. **Germany**'s is a wandering, three‑mode, high‑curvature path — a contested transition (nuclear phase‑out + coal + renewables all in motion at once). The *same deterministic mechanics* quantify the difference, and in **both** the honest derivative ceiling is acceleration — the 26 yearly points do not support a meaningful jerk.

## What this unlocks (Tier 2, to build into the payload)

A per‑step mechanical state ride‑along (speed, curvature, momentum‑arrow, force) with the hold‑lock marking when the **arrow turns** (force = a real redirection); the action and path‑efficiency as one‑number transition summaries; the velocity‑covariance modes as the "normal modes of the transition"; and — for the SafeLoop — momentum/force as the observed state a bounded controller damps toward a setpoint (behind breakers, still not a forecast).

## Claim tiers

- The computed quantities (the jet to `N*`, curvature, momentum/force/energy, the integral invariants, the spectral decomposition) and the noise‑bounded ceiling — **Tier 1** (deterministic, self‑tested, demonstrated on real data).
- The differential‑geometry‑of‑curves and Newton/Lagrange framework on the Aitchison manifold — **Tier 2** (standard mathematics, soundly applied; the simplex genuinely carries this geometry).
- A full Lagrangian/Hamiltonian dynamical‑systems theory with a physical potential `V` — **Tier 3** (to earn; here `V≡0`, so action = ∫T dt).

*Every value linear algebra, every value deterministic, the tower truncated where the data stops speaking. The instrument reads the whole mechanics of the motion — and tells you, honestly, the order at which it must stop reading.*
