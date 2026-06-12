# High-Dimensional Scaling of Hs as a Purely Deterministic System

*Concept note — 2026-06-10. Status: instrument-level reasoning + standard mathematics, claim-tiered. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Triggered by the post-CoDaWork question: build native D=8 / D=16 quaternion "twin/quad" engines, or carry the exact D=4 algebra to high D by tiling + mapping? Target horizon: D ≈ 100,000 (microbiome), with medical and oceanography as adjacent high-D compositional domains.*

---

## 0 · The verdict, up front

**Do not build "native" D=8 or D=16 quaternion engines.** The thing those names point to does not exist with the properties Hs depends on. The exactness that makes CNQ valuable is a property of **D=4 specifically**, and the correct way to take it to any higher D is to **tile D=4 charts and glue them with explicit, deterministic transition maps** — exactly the construction already prototyped for the Frielingen-9 mudstone demo.

If a truly *native* high-dimensional exact rotor is ever wanted, the mathematically correct vehicle is **not** a "bigger quaternion" — it is a **Clifford-algebra rotor (Spin(n))**, which stays associative and exact in every dimension. That is noted below as the principled alternative, but for D ≈ 100,000 the pragmatic, code-reusing, interpretable path is **D=4 tiling + a domain-aware atlas**.

Hs stays deterministic at every layer. That is the moat. Most of the field reaches for statistics and lossy reduction at high D; Hs does not have to, and should not start now.

---

## 1 · Why D=4 is special (the real reason, not a convenience)

CNQ is exact at D=4 because of a coincidence of structure that has a name and a theorem behind it.

A 4-part composition has **3 isometric-log-ratio (ILR) coordinates**. Three is exactly the dimension of the imaginary part of the quaternions **H**, and the unit quaternions form the 3-sphere **S³ = SU(2)**, which double-covers the rotation group **SO(3)**. So a 4-part compositional *move* maps cleanly onto a *rotation*, the sandwich product `q v q*` **is** that rotation, composing rotations **is** multiplying quaternions, and reversing a path **is** conjugation. Everything downstream — bearing, helmsman/handedness, geodesic distance, SLERP — inherits exactness and numerical stability (the atan2-stable angle recovers ~8 digits near 0°/180°; IEEE-754 floor ~2.2e-16).

The normed division algebras over the reals exist in **only four dimensions: 1 (ℝ), 2 (ℂ), 4 (ℍ), 8 (𝕆)** — Hurwitz's theorem. Of those, only ℝ, ℂ, ℍ are **associative**, which is what lets unit elements form a *group* whose multiplication composes rotations. So **D=4 (ℍ) is the largest case where compositional moves become a clean rotation group.** This is not a limitation to work around; it is the reason the construction is exact, and the reason tiling is the right answer rather than a fallback.

The Cayley–Dickson ladder is precisely the "twin/quad" idea, and it shows what breaks:

| Step | Algebra | Dim | What you keep | What you lose |
|---|---|---|---|---|
| quaternion | ℍ | 4 | associative group S³=SU(2), exact rotations | (commutativity — already gone, and harmless) |
| **"twin"** | 𝕆 octonions | 8 | norm, division | **associativity** → unit elements are *not a group*; sandwich conjugation no longer composes as multiplication → the transition-map / holonomy / SLERP machinery has no clean group to live in |
| **"quad"** | sedenions | 16 | (algebra structure only) | **the division property itself** — sedenions have **zero divisors** (nonzero × nonzero = 0) → inversion and exact, reversible navigation break *at the algebra level* |

So "native D=16 quaternion" is, strictly, a category error: at 16 you are in the sedenions, which are not a division algebra at all. A D=8 "twin" (octonions) keeps division but throws away the associativity that the entire CNQ apparatus is built on. **Neither buys the exact, deterministic, composable structure that D=4 gives for free.**

---

## 2 · The two *exact* paths to high D (both deterministic)

There are exactly two ways to reach high D **without** giving up exactness or determinism:

**(A) D=4 quaternion tiling + mapping — recommended.** Cover the high-D simplex with overlapping exact 4-part charts; glue them with the explicit ILR→quaternion transition maps. Verified core (see §4): for charts {1,2,3,4} and {1,2,3,5} the shared contrasts are invariant and only the swapped contrast shifts, by exactly −(√3/2)·ln(x₅/x₄). You never instantiate a higher-D algebra; you reuse the existing engine and keep the 3-DOF-per-chart **interpretability** (helmsman, bearing) that field scientists actually read.

**(B) Clifford-rotor / Spin(n) native engine — the principled alternative.** Clifford (geometric) algebras are **associative in every dimension**; their even-subalgebra unit elements form **Spin(n)**, a Lie group double-covering SO(n), acting by exact sandwich rotations on any number of axes. Quaternions are literally the n=3 case (ℍ ≅ Cl⁺(3) = Spin(3)). This is the *correct* meaning of "go native to higher D" — a clean generalization that preserves exactness and determinism. The cost is a from-scratch rotor engine and the loss of the tidy per-axis 3D picture; rotors mix many planes at once and are harder to read as a "helmsman."

Both (A) and (B) are deterministic and hash-chainable. The choice between them is engineering, not mathematics: **(A) reuses code, stays interpretable, and is already partway built; (B) is the cleaner generalization but a larger build with less intuitive output.** For the microbiome horizon, (A) wins on reuse and interpretability; (B) is worth keeping on record as the rigorous "native" option if a future mission ever needs a single high-D rotor in hardware.

What you should **not** do is spend effort on octonion/sedenion "twin/quad" engines — they sit in the one place that sacrifices the properties Hs sells.

---

## 3 · Options table (deterministic scaling to high D)

| Approach | Deterministic? | Exact algebra | How it reaches high D | Scales to D≈100k? | Honest status |
|---|---|---|---|---|---|
| **CNT only** (no CNQ) | Yes | No — navigation metrics only | Linear per-step reduction | **Yes, linear** | Tier 1/2: established, already implemented. The fast workhorse. |
| **Native "twin/quad"** (octonion D=8 / sedenion D=16) | In principle, but loses the structure that guarantees it | Lost (assoc. at 8; division at 16) | n/a — algebra itself breaks | No real gain | **Not recommended.** Category error at 16; loses associativity at 8. |
| **D=4 tiling + transition maps** | Yes, every step | Yes — full SU(2) per chart | Overlapping atlas + explicit maps | Feasible **with a smart atlas** | Core maps Tier 1 (verified §4); high-D atlas Tier 3 (to build/benchmark). |
| **D=4 tiling + phylogenetic/hierarchical atlas** | Yes | Yes | Taxonomic tree → 4-clade charts, sparse overlap | Plausibly near-linear | **Recommended direction.** Tier 3: sound idea, not yet built or benchmarked. |
| **Clifford rotor / Spin(n)** | Yes | Yes — associative all D | One native rotor in D−1 dims | Yes in principle | Tier 2 math; Tier 3 as an Hs engine (unbuilt). The principled "native" path. |

---

## 4 · What is actually established vs. what is aspiration (claim tiers)

Keeping these separate is the whole point of the discipline, and it is what lets this note go in the repo without inflating anything.

**Tier 1 — verified / computed.**
- The D=4 ILR→quaternion construction is exact (standard, and the engine runs deterministically).
- The 5-part transition map is correct: shared Helmert contrasts z₁,z₂ are normalization-invariant; only z₃ shifts, by −(√3/2)·ln(x₅/x₄). **Re-checked numerically on 2026-06-10: max deviation 3.6×10⁻¹⁵ over 100,000 random 5-part compositions.**
- CNT is deterministic and reduces each step in linear work.

**Tier 2 — standard mathematics, soundly applied.**
- Hurwitz's theorem and the Cayley–Dickson loss of associativity (D=8) then division (D=16) — textbook; the application to "don't build native twin/quad" is a direct, correct consequence.
- Clifford/Spin(n) rotors as the associative high-D generalization of quaternions — textbook geometric algebra.
- SLERP as the exact geodesic interpolation on S³.

**Tier 3 — interesting, unverified, NOT yet earned. Do not present as built.**
- That a *full atlas* of overlapping D=4 charts reconstructs an arbitrary high-D trajectory **losslessly at scale** — proven only on a small worked case; not demonstrated at large D, and the necessary atlas-construction algorithm does not yet exist.
- The phylogenetic/hierarchical atlas for D≈100k microbiome — a sound and natural idea, **unbuilt and unbenchmarked**.
- The entire differential-geometry tower explored in the source thread — **curvature 2-form, Ambrose–Singer holonomy, Chern–Weil classes, Chern–Simons 3-forms, Berry-phase monopoles, Yang–Mills instanton numbers** as applied to a "CNQ principal bundle." This is real mathematics by analogy. **None of it is computed, implemented, or shown to apply** to compositional data; the claimed isometry/connection structure of the CNQ bundle is asserted, not established. It is a research direction, possibly a rich one. It must **not** appear in any Matthew-facing, agency-facing, or repo headline material as a property the system *has*. If pursued, each piece has to be earned: define the bundle and connection precisely, prove the lift of an ILR shift to quaternion multiplication is actually a group homomorphism, then compute one invariant on real data and check it.

---

## 5 · The determinism moat

The reason to hold this line: at high D, the mainstream toolkit is statistical — PCA/UMAP-style reduction, probabilistic embeddings, sampling. Those discard information and are not reproducible bit-for-bit. Hs's value proposition is the opposite: **same input, same output, always**, with a hash chain from raw vector to result (HUF-STD-002). Both exact paths above (D=4 tiling and Clifford rotors) keep that property to D≈100k. Whatever is added on top — atlas logic, optional diagnostics — must preserve it, or it does not belong in Hs.

---

## 6 · Recommended path

1. **CNT as the linear-scaling workhorse** for the full D≈100k field — screening, navigation, outlier and regime detection. Already deterministic and implemented.
2. **D=4 CNQ-tiling applied selectively**, on phylogenetically/structurally coherent sub-manifolds where exact rotational read-out (helmsman, bearing) adds scientific value. Reuses the engine; keeps interpretability.
3. **Build the atlas layer** — for microbiome, a taxonomic-tree covering into overlapping 4-clade charts; benchmark charts-count and reconstruction error vs. D. This is the one genuinely new build, and the gating Tier-3→Tier-1 step.
4. **Record Clifford/Spin(n)** as the principled native-rotor alternative for a possible future single-engine hardware target; do not build it now.
5. **Quarantine the differential-geometry tower** as a clearly-labelled research appendix until at least one invariant is defined and computed on real data. Keep it out of claims.

The headline that is safe to carry anywhere: *Hs scales to arbitrarily high dimension while staying purely deterministic, by tiling the one dimension (D=4) where compositional moves are exact rotations — not by inventing a bigger algebra.*

---

*Companion to `CNQ_TILING_CONCEPT.html`, `FACETED_READ_CONCEPT.html`, and the `demo_frielingen9/` worked example. The instrument reads. The expert decides. The hashes carry the receipts.*
