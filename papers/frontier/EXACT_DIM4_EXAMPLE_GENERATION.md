# An exact dimension-four example generator for compositional data

*Hˢ — the deterministic compositional-kinematics engine in this repository — used as an inert
generator of exact dimension-four objects, their Spin(4) twins, and a lossless tiling of
arbitrarily high-dimensional compositions into dimension-four charts. Every number is reproducible
to a content hash. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.*

---

## Motivation

A standard and powerful move in low-dimensional topology is to settle a hard question by exhibiting
a different, *adjacent* object whose property decides the original — reducing a question you cannot
resolve directly to a related one you can build and check. The recent exemplar is Piccirillo (2020),
"The Conway knot is not slice," *Annals of Mathematics* 191(2), 581–591. The geometry used here is
the Aitchison/ILR programme of Egozcue & Pawlowsky-Glahn (2003).

Taking that idea seriously raises a constructive question: can an inert, deterministic instrument
*generate* exact objects in the category one already works in — at the IEEE floor, reproducibly, at
scale? The constructions below answer it.

## Where these sit in the larger system

Hˢ reads a compositional trajectory and returns a lossless geometric reading of it. Three of its
components compose into an example generator:

- the **D = 4 quaternion identity** is the atom — a four-part composition's ILR coordinate is a unit
  quaternion, and an Aitchison perturbation is an exact rotation;
- the **D = 8 twin** is the next rung — two quaternions act as a single SO(4) rotation;
- the **tiling** scales the atom to arbitrary dimension — overlapping four-part charts cover a
  high-dimensional composition and glue back losslessly.

Together they let the engine emit exact, hash-receipted objects in the S³ / SU(2) and PL→DIFF
setting from real compositional data.

## The constructions

Run `experiments/exact_dim4_generator_2026-06/exact_dim4.py` (numpy + scipy; fixed seed; deterministic).
Receipt: `content_sha256 = f9fa4198d056b1c2a1dbb954157f6268326a3d4f4c0ebbe4dd4ef3de0202d0f8`.

**1 — D = 4 → S³ = SU(2) = Spin(3).** A four-part composition's three ILR coordinates are a point in
ℝ³ ≅ Im(ℍ); an Aitchison rotation *is* the quaternion sandwich `q v q*`. Over 2000 trials the
sandwich reproduces the SO(3) rotation to **1.6×10⁻¹⁵**, with the ILR norm preserved to
**4.4×10⁻¹⁶**. Exact at the IEEE floor.

**2 — D = 8 → Spin(4) = SU(2) × SU(2), the double cover of SO(4).** The twin quaternion `(qₗ, qᵣ)`
acts on ℝ⁴ ≅ ℍ by `x ↦ qₗ · x · q̄ᵣ`. Over 2000 trials the resulting 4×4 map is orthogonal to
**8.9×10⁻¹⁶** with determinant +1 to **1.6×10⁻¹⁵** — a genuine element of **SO(4)**, realised as a
pair of unit quaternions. Spin(4) is the structure group over an oriented Riemannian 4-manifold,
reached here by the standard double cover.

**3 — the reverse case: an exact dim-4 atlas of a high-D object.** Tile a high-dimensional
composition into overlapping four-part (S³) charts and rebuild the whole losslessly:

| D (parts) | S³ charts | reconstruction residual |
|---:|---:|---:|
| 16   | 13    | 1.3×10⁻¹⁵ |
| 64   | 61    | 6.7×10⁻¹⁴ |
| 256  | 253   | 3.0×10⁻¹³ |
| 1024 | 1021  | 5.9×10⁻¹² |
| 4096 | 4093  | 2.9×10⁻¹¹ |

The per-chart D=4 map is exact at the IEEE floor; the high-D reconstruction is floating-point
accumulation that grows with D — locally exact, globally floating-point, not a mathematical identity
at scale. A tree-atlas variant (`experiments/cnq_tiling_highd_2026-06/`) keeps the chart-graph
diameter ~log D and carries the same reconstruction to D = 10⁶ at ~4×10⁻¹².

## What it produces

An exact, connected atlas of native-dimension-four (S³) charts covering an arbitrarily
high-dimensional simplex, with explicit transition data and a lossless gluing back to the whole —
every instance hash-receipted, so any object is reproduced or refuted exactly. As a data-driven
generator it produces exact Spin(4) elements and Spin(4)-structured trajectories at scale, and the
refinement parameters (timesteps, polygon resolution) increase toward the smooth ideal, giving a
computational PL→DIFF probe. The objects live in the smooth-vs-PL setting near dimension four —
knot concordance, slice genera, gauge-theoretic 4-manifold structures.

Hˢ does not compute knot invariants, slice obstructions, Khovanov or Heegaard–Floer homology, or
Rasmussen's s, and proves no theorems about specific manifolds. It is an experimental-mathematics
instrument that generates exact examples; what they are good for is a question to take up or leave.

## Honest envelope

The four constructions are verified numerics (Tier 1), reproducible to the hash on any machine.
Whether an exact, scalable, native-four chart atlas is a useful source of examples in a given
programme is an open mathematical question (Tier 3).
