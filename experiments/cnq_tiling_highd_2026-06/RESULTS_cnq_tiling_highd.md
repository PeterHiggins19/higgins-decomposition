# Experiment Journal — CNQ-Tiling: Lossless High-D Reconstruction & Scaling

**Date:** 2026-06-10
**Author:** Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.
**Folder:** `experiments/cnq_tiling_highd_2026-06/`
**Code:** `cnq_tiling_poc.py` (main), `big_d.py` (D=10⁶ point), `make_fig.py` (figure)
**Artifacts:** `cnq_tiling_poc_results.json`, `cnq_tiling_scaling.png`
**Engine lockdown:** this is a standalone proof-of-concept. It does **not** modify `cnt.py`/`cnq.py`, schemas, or the INV catalog. It re-implements only the minimal Aitchison + quaternion + reconstruction primitives needed to test the claims independently.

---

## Why this experiment exists

Post-CoDaWork, a plan was floated to build "native" D=8 then D=16 quaternion engines for high-dimensional compositional work, with a stated horizon of **D ≈ 100,000** for microbiome (and adjacent medical / oceanography) data. The competing position — argued in `collaborations/geology-wehner/HIGHD_DETERMINISTIC_SCALING.md` — is that the exact algebra is a property of **D=4 only**, and that **tiling overlapping D=4 charts** carries it to any dimension **deterministically**, with no native higher-D algebra. This experiment was built to settle the question with numbers rather than assertion.

## Hypotheses (stated before running)

1. **H1 — Quaternion exactness (D=4).** The sandwich product reproduces 3-D rotations to machine precision, and the atan2 angle form is materially more accurate than arccos near 0°/180°.
2. **H2 — Lossless reconstruction.** A *connected* atlas of overlapping 4-part charts reconstructs the full D-part composition (its CLR vector) to machine precision.
3. **H3 — Overlap is necessary.** A *disjoint* atlas (charts sharing no parts) is rank-deficient and cannot reconstruct the composition.
4. **H4 — Native D=16 unnecessary.** A random D=16 compositional move is reconstructed exactly from D=4 charts, i.e. a D=4 tiler reproduces what a (nonexistent, see note) native D=16 engine would compute.
5. **H5 — Scaling.** Chart count grows O(D); per-sample reconstruction is near-linear in D and stays far below both the brute-force C(D,4) chart count and the dense global-ILR memory wall.

## Method

A 4-part chart can measure the **3 independent log-ratios** among its parts — its local Helmert-ILR coordinates are an invertible linear map of those log-ratios. Stacking every chart's internal log-ratios `log(x_i/x_j) = clr_i − clr_j` gives a linear system **A c = b** on the centered-log-ratio vector **c** (which is in bijection with the composition on the simplex). The normal-equation matrix **AᵀA is the graph Laplacian** of the part co-occurrence graph induced by the atlas. Standard result: **c is recoverable (up to the fixed sum-zero constraint) iff that graph is connected.** Reconstruction is therefore an exact, deterministic sparse linear solve — no statistics, no sampling, no iteration tolerance to tune.

Atlases tested: **sliding window** (4-part charts overlapping by 3 parts → co-occurrence = all pairs within distance 3, a connected band/path graph) and **disjoint blocks** (4-part charts sharing nothing → a disconnected graph of D/4 components). Compositions drawn from `Dirichlet(0.3·1)` (deliberately heavy-tailed, producing very small parts, to stress the log). Solve via `scipy.sparse.linalg.spsolve` on the Laplacian with one node pinned per component.

## Results (measured)

### H1 — Quaternion exactness ✅
Sandwich product vs. Rodrigues rotation, **max abs error 2.22×10⁻¹⁵** over 20,000 random rotations (= machine epsilon). Angle recovery near 0°:

| true angle | arccos rel-err | atan2 rel-err |
|---|---|---|
| 1e-1 | 5.6e-15 | 1.4e-16 |
| 1e-3 | 7.8e-12 | 0 |
| 1e-5 | 4.1e-08 | 0 |
| 1e-7 | 4.0e-04 | 0 |
| 1e-9 | **1.0 (100% wrong)** | 0 |

arccos collapses to total error at small angles; atan2 stays exact. Confirms the corpus's atan2 precision claim independently.

### H2 — Lossless reconstruction (connected atlas) ✅
Over 15 runs (D = 16, 64, 256): **max reconstruction error 2.13×10⁻¹³**; the co-occurrence graph is always a single connected component. Lossless to machine precision.

### H3 — Overlap is necessary (disjoint atlas) ✅
Same compositions, disjoint atlas: **minimum error 1.16** (order-1 failure). The graph splits into D/4 components — (16→4), (64→16), (256→64) — and the relative levels between components are unrecoverable. Overlap is not decorative; it is what makes the atlas invertible. (Matches the prior corpus note: "overlap proven necessary; disjoint atlas rank-deficient.")

### H4 — Native D=16 unnecessary ✅
A random D=16 move (CLR difference of two random 16-part compositions) reconstructed from overlapping D=4 charts: **max abs error 2.22×10⁻¹⁵**. A D=4 tiler reproduces the full D=16 move exactly.

> **Note on "native D=16."** There is no normed division algebra at dimension 16 (Hurwitz): the sedenions have zero divisors. So "native D=16 quaternion engine" is not a thing one can build with the exactness Hs needs — and this result shows one does not need to: tiling D=4 already delivers the exact D=16 answer.

### H5 — Scaling to D = 1,000,000 ✅
Single sample, 2-core CPU, 3.8 GB box:

| D | charts (≈D) | tiling solve | tiling mem | recon err | dense global-ILR | brute-force C(D,4) |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1 | <1 ms | ~0.1 KB | 5.6e-17 | — | 1 |
| 16 | 13 | <1 ms | ~0.7 KB | 5.7e-15 | — | 1.8e3 |
| 64 | 61 | <1 ms | ~3 KB | 6.3e-14 | — | 6.4e5 |
| 256 | 253 | 1 ms | ~12 KB | 5.9e-14 | negligible | 1.7e8 |
| 1,024 | 1,021 | 1 ms | ~49 KB | 7.8e-12 | 0.008 GB | 4.6e10 |
| 4,096 | 4,093 | 2 ms | ~0.2 MB | 8.8e-12 | 0.13 GB | 1.2e13 |
| 16,384 | 16,381 | 14 ms | ~0.8 MB | 2.7e-10 | 2.15 GB | ~4e14 |
| 65,536 | 65,533 | 55 ms | ~3 MB | 1.2e-09 | 34.4 GB | ~1e18 |
| **100,000** | 99,997 | **0.16 s** | ~5 MB | 1.6e-09 | **80 GB** | ~4e18 |
| 500,000 | 499,997 | 1.56 s | 24 MB | 6.5e-08 | 2,000 GB | ~2e21 |
| **1,000,000** | 999,997 | **1.90 s** | **48 MB** | 2.6e-07 | **8,000 GB** | ~4e22 |

Charts grow linearly; reconstruction is sub-2-seconds at a **million** parts on a 2-core machine using **48 MB**, while the dense global-ILR basis would need **8 TB** and the brute-force all-4-subsets atlas would need ~10²² charts. Both "walls" are avoided entirely because tiling never forms a global basis and never enumerates subsets.

## Honest finding — atlas conditioning (not a defect; a design signal)

Reconstruction error is machine-precision at small D but **grows with D on the sliding-window atlas**: 2e-13 (D=64) → 1.6e-9 (D=100k) → 2.6e-7 (D=1M). Cause: the sliding window is a **path graph of length ~D**, so recovering a global level means summing ~D local log-ratio differences, and rounding accumulates along the chain (the Laplacian's condition number grows with diameter). 2.6e-7 is still effectively lossless against log-values of order 1–70, but it is not bit-exact at extreme D.

This directly motivates the recommended next build: a **hierarchical / tree atlas** (e.g. a phylogenetic tree for microbiome) has diameter **O(log D)** rather than O(D), which should hold reconstruction near machine precision at any D while keeping charts and cost linear. That is the concrete experiment to run next, and the step that would move "feasible at D≈100k" from Tier 3 to Tier 1.

## Claim tiers

- **Tier 1 (verified here):** quaternion exactness + atan2 advantage; lossless reconstruction on a connected atlas; overlap necessity; exact D=16-from-D=4; O(D) charts and sub-2-s / sub-50-MB reconstruction to D=10⁶; the dense-ILR and C(D,4) walls.
- **Tier 2 (standard, soundly applied):** the Laplacian-connectivity reconstruction theorem; Hurwitz/Cayley-Dickson ruling out native D≥8 division algebras.
- **Tier 3 (not yet earned):** that a hierarchical atlas restores machine precision at extreme D (predicted, not yet run); any claim that this replaces general microbiome compute pipelines (it addresses the *per-sample compositional reduction/navigation*, not assembly, phylogenetic placement, or full differential-abundance statistics).

## Addendum (same day, 2026-06-10) — Hierarchical tree atlas confirms the fix ✅

**Code:** `cnq_tiling_hierarchical.py`, `tree_1e6.py`, `make_fig2.py`. **Artifacts:** `cnq_tiling_hierarchical_results.json`, `cnq_tiling_tree_vs_path.png`.

**H6 (stated as the prediction above):** a balanced 4-ary **tree atlas** has co-occurrence-graph diameter **O(log D)**, so the reconstruction Laplacian stays well-conditioned and error holds near machine precision at any D.

**Construction (all real 4-part charts):** group the D parts into consecutive blocks of 4 → each block is a chart; the block's first part is its *representative*; the representatives form the next level; recurse to the root. Representatives chain every chart to the root (connected); depth = log₄D; any leaf→leaf distance ≤ 2·depth. **For microbiome this tree IS the phylogeny** — sibling taxa share the low-level charts; the same construction applies to any hierarchical clustering of the parts.

**Result (measured, path vs tree, same compositions/seed):**

| D | atlas | charts | graph diameter (ecc from node 0) | recon error | solve |
|---:|:--|---:|---:|---:|---:|
| 100,000 | path | 99,997 | 33,333 | 1.04e-9 | 0.08 s |
| 100,000 | **tree** | **33,336** | **9** | **8.3e-13** | 0.07 s |
| 1,000,000 | path | 999,997 | 333,333 | 2.05e-7 | 5.7 s |
| 1,000,000 | **tree** | **333,334** | **10** | **4.1e-12** | 4.5 s |

Across D = 64 → 10⁶ the tree-atlas diameter grows **3 → 10** (logarithmic) while the path grows **21 → 333,333** (linear); tree reconstruction error stays **flat at ~1e-13–4e-12** while the path climbs from 3e-14 to 2.05e-7. The tree also uses **fewer charts** (~D/3) and is always a single connected component (lossless). See `cnq_tiling_tree_vs_path.png`.

**Verdict:** the hierarchical/phylogenetic atlas is the high-D precision fix. This was the standing Tier-3 prediction; it is now **Tier 1 (measured)**. Net picture: D=4 tiling on a tree atlas reconstructs a million-part composition **losslessly (≈4e-12), deterministically, in ~5 s and <50 MB** — no native higher-D algebra, no statistics. Residual ~1e-12 (not bit-exact) is ordinary floating-point accumulation over ~10 tree levels; double-double arithmetic would close it if ever needed (not pursued — unnecessary for compositional log-values of order 1–70).

## Reproduce

```
cd experiments/cnq_tiling_highd_2026-06/
pip install numpy scipy matplotlib
python3 cnq_tiling_poc.py          # experiments 1–5, writes results JSON
python3 big_d.py                   # path atlas at D = 5×10⁵ and 10⁶
python3 cnq_tiling_hierarchical.py # path vs tree sweep to D=10⁵
python3 tree_1e6.py                # path vs tree at D=10⁶
python3 make_fig.py ; python3 make_fig2.py   # figures
```
Deterministic given the fixed seeds; same input → same output.

*The instrument reads. The expert decides. The hashes carry the receipts.*
