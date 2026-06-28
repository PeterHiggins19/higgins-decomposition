# P1 re-validation against the new engine — tested the most

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. P1
("Tiling the Simplex") is the math everything else cites, so it gets the heaviest re-test under the current
engine conventions (HS-GOLD-1 / SO(n)). **Every load-bearing claim re-confirms** — and one honest review
finding surfaced: the headline high-D residual is *solver-dependent* and the paper must name its solver.
Receipt `99ec0581…`. Honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## Result — all P1 claims hold on the new engine

| # | P1 claim | measured (new engine) | verdict |
|---|---|---|---|
| **T1** | D=4 sandwich `q v q*` = SO(3), ~4.4×10⁻¹⁶, bit-identical on 2 reference inputs | **4.4×10⁻¹⁶**; refs identical | ✅ |
| **T2** | su(2) generator relations `[G_i,G_j]=2ε_{ijk}G_k` | **exact (<10⁻¹²)** | ✅ |
| **T3** | balanced-tree atlas reconstructs to D=10⁶ at ~4.1×10⁻¹² (numerical, not identity); path atlas degrades | **tree → 1.5×10⁻¹²** at D=10⁶ (direct solver); **path → 7.1×10⁻¹⁰** at D=16k | ✅ |
| **T4** | reconstruction exact **iff** chart graph connected | connected **3.1×10⁻¹⁴**; disjoint **singular (NaN) → correctly fails** | ✅ |
| **T5** | determinism (same input → same output) | fixed input → fixed reconstruction | ✅ |

### T3 detail — the tree-vs-path story P1 sells, reproduced

| D | tree atlas (diam ~O(log D)) | path atlas (diam O(D)) |
|---:|---:|---:|
| 256 | 4.3×10⁻¹⁴ | 3.0×10⁻¹³ |
| 1,024 | 5.2×10⁻¹⁴ | 8.9×10⁻¹³ |
| 16,384 | 1.5×10⁻¹³ | **7.1×10⁻¹⁰** (degrading) |
| 65,536 | 3.4×10⁻¹³ | — |
| **1,048,576** | **1.5×10⁻¹²** | — |

The balanced-tree atlas stays at the 10⁻¹²–10⁻¹³ floor to a million parts; the path atlas degrades three orders
by D=16k. P1's central design claim — *the chart-graph diameter, not D, sets the error* — holds.

## The review finding (test-the-most earned one)

P1's headline "≈4.1×10⁻¹² at D=10⁶" is **solver-dependent**:

- **direct solver (`spsolve`):** 1.5×10⁻¹² at D=10⁶ — reproduces the paper (same order). ✅
- **iterative solver (`cg`, rtol 1e-14):** 1.2×10⁻⁸ — solver-limited, three orders looser.

Neither is "wrong" — they answer at different precisions. **Action for P1:** state the solver (direct sparse
Cholesky / `spsolve`) alongside the residual, and note the iterative-solver floor, so the figure reproduces
exactly. This is a one-line methods addition, not a result change — exactly the kind of thing a hard re-test
is supposed to catch before submission.

## What the new engine changed for P1 (nothing material — by design)

P1 uses only the **adjoint SO(3)** sandwich. The new engine's additions (the **SO(n) generator**, the
**dual-quaternion SO(4) module**) are *separate frontier components* (`HOW_FAR_THE_MATH_GOES.md`,
`SO4_SPIN4_FUTURE_COMPONENT.md`) — they extend *beyond* P1, they do not alter it. P1's claims are unchanged and
now re-receipted under HS-GOLD-1. The honesty boundary is intact: **high-D reconstruction is numerical, not
bit-exact identity** (the residual grows with diameter, exactly as the paper states).

## Tiers

- **T1 (measured):** all five checks + the solver-dependence; receipt `99ec0581…`.
- **T2 (reasoned):** that the tree-atlas advantage generalizes to any well-connected chart graph.
- **T3 (rejected):** "lossless at scale" — still rejected; D>4 is floating-point reconstruction.

*Reproduce: `python3 p1_revalidate.py`. Cross-refs: `arXiv/P1_cnq_tiling/` (the paper),
`../exact_dim4_generator_2026-06/` (the original construction), `../conformance_fixtures_2026-06/` (HS-GOLD-1),
`../../papers/PAPER_REFINEMENT_AND_RELEASE_PLAN_2026-06.md`. Peter is the sole gate.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
