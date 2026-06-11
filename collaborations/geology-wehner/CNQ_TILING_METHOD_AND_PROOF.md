# CNQ-Tiling — Method, Proof of Concept, and Compute-vs-Dimension Limits Guide

*Full reference document — 2026-06-10. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Companion to `HIGHD_DETERMINISTIC_SCALING.md` (the strategic case) and `experiments/cnq_tiling_highd_2026-06/` (the runnable proof). Status: claim-tiered throughout; every number marked "measured" comes from the journaled experiment in that folder.*

---

## 1 · What CNQ-tiling is, in one paragraph

A 4-part composition is the one case where a compositional *move* is exactly a *rotation*: three isometric-log-ratio (ILR) coordinates map onto the imaginary part of the quaternions, unit quaternions are S³=SU(2), and the sandwich product `q v q*` is the rotation. CNQ reads that rotation exactly (bearing, helmsman/handedness, time-reversal by conjugation). **CNQ-tiling** carries this to any number of parts D by covering the composition with **overlapping exact 4-part charts** and gluing them with explicit, deterministic transition maps. You never build a higher-dimensional algebra; you tile the one dimension where the algebra is exact. This document proves the construction works, is lossless, and scales — and tabulates the compute limits as a function of D.

---

## 2 · The core result (and why it is true)

**Claim.** A *connected* atlas of overlapping 4-part charts reconstructs the full D-part composition losslessly; a *disjoint* atlas cannot.

**Why.** Each 4-part chart measures the three independent log-ratios among its parts (its local Helmert-ILR coordinates are an invertible linear map of them). Every log-ratio is a difference of centered-log-ratio (CLR) components: `log(xᵢ/xⱼ) = clrᵢ − clrⱼ`. Stack all chart log-ratios into a linear system **A c = b** on the CLR vector **c** (which is in one-to-one correspondence with the composition on the simplex, under the sum-zero constraint). The normal matrix **AᵀA is the graph Laplacian** of the part co-occurrence graph defined by the atlas. A Laplacian determines its vector up to a per-component constant; with the global sum-zero constraint, **c is recovered exactly iff the graph is connected.** Overlap is what connects the graph — it lets you chain `log(xᵢ/xₖ) = log(xᵢ/xⱼ) + log(xⱼ/xₖ)` across charts that share parts.

This is a standard, deterministic linear-algebra fact (Tier 2). It needs no statistics, no sampling, no tolerance to tune. The reconstruction is a single sparse solve.

**Measured (Tier 1, from the journal):**
- Connected atlas: **max reconstruction error 2.1×10⁻¹³** (machine precision).
- Disjoint atlas: **error 1.16** (order-1 failure); graph splits into D/4 components.
- Quaternion sandwich vs. Rodrigues: **2.2×10⁻¹⁵**; atan2 angle exact where arccos hits 100% error near 0°.
- A random **D=16 move reconstructed from D=4 charts: 2.2×10⁻¹⁵** — the literal demonstration that a native D=16 engine is unnecessary.

---

## 3 · Why "native D=8 / D=16" is the wrong build (settled, not opinion)

The normed division algebras over ℝ exist in **only** dimensions 1, 2, 4, 8 (Hurwitz's theorem), and only 1, 2, 4 are **associative**:

- **ℍ (D=4):** associative group S³=SU(2), exact composable rotations. This is the sweet spot.
- **Octonions (D=8, the "twin"):** keep division but **lose associativity** → unit elements are not a group; sandwich conjugation no longer composes as multiplication → the transition-map / SLERP / holonomy machinery has no group to live in.
- **Sedenions (D=16, the "quad"):** **lose the division property itself** (zero divisors: nonzero × nonzero = 0) → exact, invertible navigation breaks at the algebra level. "Native D=16 quaternion" is a category error.

If a genuinely *native* high-D exact rotor is ever wanted (e.g. one hardware engine), the correct object is a **Clifford / Spin(n) rotor** — associative in every dimension, quaternions being the n=3 case — **not** a bigger quaternion. For the D≈100k horizon, D=4 tiling wins on code reuse, interpretability (per-chart helmsman), and the fact that it is already proven here.

**Conclusion:** native D=16 is not necessary, and the proof in §2 shows D=4 tiling reproduces the exact high-D answer. Build the tiler, not the sedenion engine.

---

## 4 · Compute-vs-dimension limits guide

The two things that blow up with D are **not** in the tiling path:

- **Brute-force atlas** (all C(D,4) 4-subsets): ~1.2×10¹³ charts at D=4,096, ~10²² at D=10⁶. Never enumerate subsets — a **connected covering of ≈D charts** is all you need.
- **Dense global ILR basis** ((D−1)×D matrix): 80 GB at D=10⁵, **8 TB at D=10⁶**. Never form it — tiling only ever does local 4-part work plus a sparse solve.

What tiling actually costs (measured to D=10⁶ on a 2-core, 3.8 GB box; per single sample):

| D (parts) | atlas charts (≈D) | tiling solve time | tiling memory | recon error (sliding atlas) | dense-ILR wall (avoided) |
|---:|---:|---:|---:|---:|---:|
| 10² | ~100 | <1 ms | ~5 KB | 1e-14 | negligible |
| 10³ | ~1,000 | ~1 ms | ~50 KB | 8e-12 | 0.008 GB |
| 10⁴ | ~10,000 | ~10 ms | ~0.5 MB | ~2e-10 | 0.8 GB |
| 10⁵ | ~100,000 | **0.16 s** | ~5 MB | 1.6e-9 | 80 GB |
| 10⁶ | ~1,000,000 | **1.9 s** | 48 MB | 2.6e-7 | 8,000 GB |

### Guide: what math / software / hardware each regime needs

| D regime | Atlas & math (Tier) | Software | Hardware | Limiting factor to watch |
|---|---|---|---|---|
| **D ≤ ~50** | Any covering, even near-brute-force; dense or sparse solve. (T1) | numpy | any laptop | none — trivial |
| **D ~ 10²–10⁴** | Sliding-window (path) atlas; sparse solve. Machine-precision. (T1) | numpy + scipy.sparse | any laptop | none material |
| **D ~ 10⁴–10⁶** | Sparse band/tree atlas; sparse Laplacian solve. Path-atlas error degrades (see below) → prefer **hierarchical atlas** for precision. (T1 cost / T3 hierarchical precision) | scipy.sparse (`spsolve`); for many samples, batch over cores | laptop → workstation | **atlas conditioning** (path diameter), and **N samples** if a cohort |
| **D ~ 10⁶–10⁷** | **Hierarchical / tree atlas essential** (O(log D) diameter); chunked/streamed solve; still O(D). (T3 — predicted, not yet run) | sparse + out-of-core or GPU sparse | workstation / single GPU | memory bandwidth for very large N×D; conditioning |
| **D > 10⁷** | Hierarchical atlas + domain decomposition; one chart-block per worker. (T3) | distributed sparse | HPC node / cluster | I/O and orchestration, not the math |

Two notes on this guide:

- **The reduction itself is laptop-scale to D=10⁶** (≈2 s, <50 MB per sample). Hardware tiers above matter mainly for (a) **cohort size N** — total cost is ~O(N·D), embarrassingly parallel across samples — and (b) the **optional CNQ geometric diagnostics**, which are off by default.
- **Atlas conditioning is the real precision knob, not D.** The sliding-window atlas is a length-D path, so reconstruction error grows with chain length (measured: 2e-13 at D=64 → 2.6e-7 at D=10⁶ — still effectively lossless, but not bit-exact). A balanced **hierarchical (tree / phylogenetic) atlas** has O(log D) diameter and **fixes this — now confirmed (Tier 1):** measured graph diameter grows 3→10 over D=64→10⁶ (vs 21→333,333 for the path), and reconstruction error stays **flat at ~1e-13–4e-12** (vs the path's 2.05e-7 at D=10⁶), using ~D/3 charts. So a million-part composition reconstructs losslessly (≈4e-12), deterministically, in ~5 s / <50 MB. For microbiome this tree is the phylogeny. See the journal addendum and `cnq_tiling_tree_vs_path.png`.

---

## 5 · The microbiome / "days of compute" question — scoped honestly

Several CoDaWork 2026 attendees described **days of compute** for microbiome work at D in the tens of thousands. The honest, defensible statement:

> The **CNQ-tiling compositional reduction** — turning a D≈100,000 sample into its exact navigation read (helmsman, bearing, regime, Activation Coefficient) via a connected D=4 atlas — costs **sub-second per sample** and is deterministic and reproducible. For the subset of outputs that are *compositional steering / navigation reads*, this is dramatically cheaper than statistical high-D pipelines, and bit-for-bit reproducible where those are not.

What this does **not** claim (Tier-3 guardrail): it does **not** replace read assembly, taxonomic/phylogenetic placement, or full differential-abundance statistics with permutation testing — those are different tasks. The win is specific: the *dimensional reduction and navigation layer* becomes near-free and deterministic, which is exactly where statistical methods spend time and sacrifice reproducibility. Whether that collapses a given group's "days" to "minutes" depends on how much of their pipeline is reduction/navigation vs. the other tasks — a per-pipeline benchmark, not a blanket claim.

---

## 6 · What is proven vs. what is next

**Proven here (Tier 1):** quaternion exactness + atan2 advantage; lossless reconstruction on a connected atlas; overlap necessity; exact D=16-from-D=4; O(D) charts and sub-2-s / sub-50-MB reconstruction to D=10⁶; avoidance of the C(D,4) and dense-ILR walls; and the **hierarchical (tree/phylogenetic) atlas restoring near-machine precision (≈4e-12) to D=10⁶ via O(log D) diameter** — the conditioning fix, now measured rather than predicted.

**Standard math, soundly applied (Tier 2):** the Laplacian-connectivity reconstruction theorem; Hurwitz/Cayley-Dickson ruling out native D≥8 division algebras; Clifford/Spin(n) as the real native-rotor generalization.

**Next, to earn (Tier 3):**
1. **Per-pipeline microbiome benchmark** — take a real high-D dataset and a real phylogeny, build the tree atlas from the phylogeny (not a synthetic balanced tree), and measure end-to-end where tiling actually replaces compute, with honest before/after. (The atlas mechanism itself is now Tier 1; what remains is the real-data, real-tree demonstration.)
2. **The differential-geometry layer** (curvature, holonomy, Chern-Simons, Berry phase, instantons) explored in the source thread remains analogy: not computed, not implemented, the ILR-shift→quaternion-multiplication lift unproven. Keep it in a labelled research appendix, out of headline claims, until one invariant is defined and computed on real data.

*(The hierarchical-atlas item that stood here as the headline next experiment is now done — see §4 and the journal addendum — and has moved into the Tier-1 list above.)*

---

## 7 · Reproduce / artifacts

`experiments/cnq_tiling_highd_2026-06/` — `cnq_tiling_poc.py`, `big_d.py`, `make_fig.py`, `cnq_tiling_poc_results.json`, `cnq_tiling_scaling.png`, and the journal `RESULTS_cnq_tiling_highd.md`. Deterministic under fixed seeds.

*The instrument reads. The expert decides. The hashes carry the receipts.*
