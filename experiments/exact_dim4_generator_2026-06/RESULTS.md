# Exact native-dimension-four example generation — results

*A small, reproducible experiment. Hˢ is used as an inert, deterministic generator of exact
dimension-four objects and a lossless tiling of arbitrarily high-dimensional compositions into
dimension-four charts. Every number below is reproducible to a content hash. Author: Peter Higgins
(human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker: the numerics are Tier 1
(verified); whether any of this is useful to a given research programme is the reader's call.*

Run: `python3 exact_dim4.py` (numpy + scipy; fixed seed = 4; deterministic).
Receipt: `content_sha256 = f9fa4198d056b1c2a1dbb954157f6268326a3d4f4c0ebbe4dd4ef3de0202d0f8`.

## The idea

A recognisable move in experimental mathematics is to settle or represent a hard object by
constructing an exact, *adjacent* one — reduce the question you cannot see to a related object you
can. This experiment uses Hˢ in exactly that spirit: not to prove anything about a specific object,
but to **generate** exact objects in a category that a researcher already studies, computationally
and reproducibly, so the adjacencies are there to inspect.

## Construction 1 — D = 4 → S³ = SU(2) = Spin(3), exact

A four-part composition's three ILR coordinates are a point in ℝ³ ≅ Im(ℍ). An Aitchison rotation is
the quaternion sandwich `q v q*`. Reproduced over 2000 random trials:

- `q v q*` reproduces the SO(3) rotation of the ILR coordinate to **max residual 1.6×10⁻¹⁵**;
- the ILR norm is preserved to **4.4×10⁻¹⁶** (machine epsilon).

*(Tier 1 — exact at the IEEE floor.)*

## Construction 2 — D = 8 → Spin(4) = SU(2) × SU(2) = double cover of SO(4)

The "twin quaternion" `(qₗ, qᵣ)` acts on ℝ⁴ ≅ ℍ by `x ↦ qₗ · x · q̄ᵣ`. Over 2000 random trials the
resulting 4×4 map is:

- orthogonal to **8.9×10⁻¹⁶**, and
- has determinant +1 to **1.6×10⁻¹⁵** — a genuine element of **SO(4)**, realised as a pair of unit
  quaternions.

Spin(4) is the structure group over an oriented Riemannian 4-manifold, reached here by the standard
double cover — exactly and reproducibly. *(Tier 1 — exact at the IEEE floor.)*

## Construction 3 — the reverse case: an exact dim-4 atlas of a high-D object

Tile a high-dimensional composition into overlapping four-part (S³) charts and rebuild the whole
clr vector from the chart data:

| D (parts) | S³ charts | reconstruction residual |
|---:|---:|---:|
| 16   | 13    | 1.3×10⁻¹⁵ |
| 64   | 61    | 6.7×10⁻¹⁴ |
| 256  | 253   | 3.0×10⁻¹³ |
| 1024 | 1021  | 5.9×10⁻¹² |
| 4096 | 4093  | 2.9×10⁻¹¹ |

The per-chart D=4 map is **exact at the IEEE floor**; the high-D reconstruction is **floating-point
accumulation** that grows with D (≈3×10⁻¹¹ at D=4096) — **not** a mathematical identity at scale.
The repository's tree-atlas variant (`../cnq_tiling_highd_2026-06/`) carries the same reconstruction
to D = 10⁶ at ~4×10⁻¹² by keeping the chart graph's diameter ~log D. That is the precise, defensible
claim: locally exact, globally floating-point.

## Honest envelope

The four numbers above (D=4 rotation, D=8 → SO(4), the reverse atlas, the norm preservation) are
**Tier 1 — verified numerics**, reproducible to the hash on any machine. Whether an exact, scalable,
native-four chart atlas with reproducible transitions is *useful* in any particular research
programme is **Tier 3 — an open question for the reader**, posed in the field's language, with no
claim attached. The instrument generates; the mathematics of whether any adjacency matters is the
researcher's entirely.
