# Manifold-Category Classification of the Hˢ Projection

**Filed:** 2026-05-24 (pre-conference; doc-only, S2-class)
**Status:** Working note. Captures a layered answer to a question that arose during pre-conference review, files it for post-conference development.
**Trigger:** Peter's question, *"the html, what kind of the 3 category of manifolds is the hs projection, topological, smooth, PL? synthetic?"*
**Companion documents:** `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2 (mathematical foundation); `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §4.9 (post-conference work entry).
**Lockdown discipline:** lives in `papers/in_progress/`, outside the `CODAwork2026/` lockdown surface and outside the engine/schema lockdown. No engine touches; no schema touches; no INV catalog changes; no NO-CREATE file creations. S2 doc-only.

---

## 1. The question

The standard categories of manifolds in modern topology and differential geometry are:

- **TOP** — topological manifolds (locally homeomorphic to ℝⁿ; no smooth structure required)
- **DIFF** — smooth manifolds (a maximal C∞ atlas; calculus is defined)
- **PL** — piecewise-linear manifolds (a triangulation where transition maps are piecewise linear)
- **Synthetic** — manifolds in the sense of synthetic differential geometry (Kock-Lawvere SDG, axiomatic infinitesimals, coordinate-free formulations in topos-theoretic settings)

These categories are not exclusive. In low dimensions every TOP manifold admits a unique DIFF structure (Moise's theorem in dim ≤ 3); in higher dimensions the categories genuinely separate (Milnor's exotic spheres; Donaldson invariants on 4-manifolds). The choice of category determines which tools are available: TOP gives you homotopy and homology; DIFF gives you tangent bundles, connections, curvature, integration of differential forms; PL gives you finite combinatorics and constructive proofs; synthetic gives you coordinate-free reasoning with axiomatic nilpotent infinitesimals.

The question for Hˢ: in which of these categories does **the projection** — the thing the engine produces, the thing rendered in the HTML, the thing read by a downstream consumer — actually live?

---

## 2. The layered answer

The Hˢ projection is **not** a single object in a single category. It is a layered construction where different categories appear at different levels. The layers are:

### Layer A — underlying mathematical object: **smooth (DIFF)**

The open simplex Sᴰ⁻¹ = { p ∈ ℝᴰ : pᵢ > 0, Σ pᵢ = 1 } is a smooth manifold of dimension D−1. With the Aitchison inner product on its tangent space it becomes a Riemannian manifold isometric to (ℝᴰ⁻¹, Euclidean) via the ILR-Helmert chart (Egozcue et al. 2003). The CNQ phase space S³ ≅ SU(2) is a smooth analytic Lie group manifold of dimension 3, with a bi-invariant Riemannian metric. The group-delay-as-rotation map (Lemma 5 of the flagship) is a smooth one-parameter subgroup of SU(2). The Banach contraction proof of Lemma 4 lives entirely in the smooth category.

So *the mathematical object the engine is doing analysis on* is a smooth Riemannian manifold (the simplex with Aitchison structure) coupled to a smooth Lie group (S³ ≅ SU(2) for the quaternionic phase).

### Layer B — discrete sampling and HTML rendering: **piecewise-linear (PL)**

The engine reads T discrete timesteps. The trajectory is a polygonal path with T−1 segments; per-step quantities (Helmsman index, Power Share, Activation Coefficient, Aitchison-step magnitude, κᴴˢ entries) are defined on the PL structure, not on the smooth one. The HTML projector renders the partition as a regular n-gon plate with D vertices at θⱼ = (j/D) · 2π − π/2 and radii rⱼ = R · (0.1 + 0.9 · ηⱼ); the BARY-mode trajectory is a polyline; CSS 3D transforms are applied per frame. The renderer is PL in two senses simultaneously: spatially (n-gon plates, polyline trajectories) and temporally (frame-by-frame, no interpolation across frames in the canonical mode).

So *what the user actually looks at* is a PL approximation of the smooth underlying object — and the approximation is faithful in the sense that as T → ∞ and as the n-gon refinement increases, the PL projection approaches the smooth Riemannian object pointwise.

### Layer C — regime taxonomy: **topological (TOP)**

The Helmsman family (sign / stability / flips / chaos / torque / joint) and the IR class (LIMIT_CYCLE_P1 / LIMIT_CYCLE_P2 / OVERDAMPED / FIXED / DRIFT / CHAOTIC / etc.) and the closure-failure flag are *invariant under metric rescaling*. They do not depend on the Aitchison inner product being chosen rather than the Fisher metric; they depend only on the qualitative phase-portrait structure. This is topological data in the standard sense — analogous to the homotopy type of a vector field's phase portrait, or the topological-conjugacy class of a dynamical system.

So *the classification labels the engine emits* live in the topological category, not the smooth one.

### Layer D — operator-level statements: **synthetic-compatible**

The mathematical statements at the level of the operators themselves —

- the Banach contraction inequality d(T(x), T(y)) ≤ κ · d(x, y) with κ < 1,
- group-delay-as-rotation as a one-parameter Lie subgroup g(τ) = exp(τ · ξ) of SU(2),
- closure invariance under the centred-log-ratio transform: clr(λ · p) = clr(p) for any scalar λ > 0,
- the unified formula T_unified = (Aitchison-step) ⊕ (quaternionic-phase) ⊕ (closure-budget)

— are *coordinate-free*. They do not require a chart; they can be stated as axioms about morphisms in a smooth topos. This is what synthetic differential geometry was designed for. The engine itself is coordinate-based (Python and R code with explicit floating-point arithmetic), so the engine is *not* synthetic; but the underlying statements *are* synthetic-compatible, and a future formalisation in SDG would not require changing what the engine does, only how the framework is described.

So *the abstract theory* is synthetic-compatible even though the *implementation* is concrete.

### Short answer

**A PL rendering of a DIFF Riemannian-and-Lie-group object, with a TOP regime taxonomy, and synthetic-compatible operator statements.**

---

## 3. Why the layered answer matters

The reflex answer would be to pick one category. The disciplined answer is that *picking one category obscures what the framework actually does*. Each category does a different job:

The **DIFF** layer is what makes the lemma chain rigorous. Banach's theorem requires a complete metric space; the simplex with Aitchison distance qualifies. The Lie-group structure of S³ is what makes group-delay-as-rotation well-defined. The Riemannian metric is what makes "compositional distance" a meaningful quantity.

The **PL** layer is what makes the framework *implementable*. Real datasets are finite; real renderings are finite; real reproducibility is byte-exact. The PL approximation is not a regrettable concession to engineering — it is the only level at which the byte-exact reproducibility contract (cnt_content_sha256, cnq_content_sha256) can be enforced. The PL → DIFF correspondence is the mathematical analogue of the floating-point → real-number correspondence in numerical analysis.

The **TOP** layer is what makes the regime taxonomy *portable* across instances. The Helmsman family labels do not depend on whether the application is acoustic, financial, or cosmological; they classify the qualitative dynamics regardless of what the carriers physically are. Topological invariance is what lets the framework recognise the same pattern in unrelated domains.

The **synthetic** layer is what would make the framework *categorical* in the technical sense. The operators (CNT, CNQ, ADAC, DADI, DADC) would become morphisms in a category; the engine outputs would become natural transformations; the closure constraint would become an axiom. This is the level at which a category theorist would say "now I understand the framework." Until that work is done, the framework speaks the language of analysis (ε, δ, sup, inf) rather than the language of category theory (objects, morphisms, natural transformations, adjunctions).

The four layers correspond to four audiences: the **DIFF** layer is for the analysts and the geometers; the **PL** layer is for the engineers and the reproducibility reviewers; the **TOP** layer is for the dynamical-systems people and the cross-domain comparators; the **synthetic** layer is for the category theorists and the formal-verification people. The framework already serves the first three audiences; the fourth is the post-conference work.

---

## 4. Map from engine output fields to manifold layers

The CNT/CNQ engine outputs can be mapped to the layers explicitly. This is the bookkeeping the future short paper would systematise; the rough mapping today:

| Engine output field | Layer | Note |
|---|---|---|
| `Aitchison_step_magnitude` per step | PL (computation), DIFF (limit) | Discrete sample of the smooth Aitchison metric |
| `kappa_HS` matrix | PL (computation), DIFF (Riemannian metric tensor) | The Higgins Steering Metric Tensor |
| `bearing_radians` per step | PL (computation), DIFF (quaternionic phase) | One sample of a smooth S³ trajectory |
| `helmsman_index` | PL (computation), DIFF (limit) | Aitchison-rotation analogue |
| `helmsman_family` label | TOP | sign/stability/flips/chaos/torque/joint — metric-invariant |
| `IR_class` label | TOP | LIMIT_CYCLE_P1 etc. — phase-portrait invariant |
| `closure_failure_flag` | TOP | Boolean — axiomatic budget invariant |
| `bary_xy[t]` (HTML render) | PL | Polyline in regular n-gon |
| `theta_j = (j/D)·2π − π/2` (n-gon vertices) | PL | Discrete D-gon |
| `r_j = R·(0.1 + 0.9·η_j)` (vertex radii) | PL | Discrete vertex placement |
| `s_j` (per-axis spectral power) | PL (computation), DIFF (limit) | Smooth ground-state instance |
| `period_2_attractor_fit` | TOP | Period-2 / M² = I — categorical |
| `content_sha256` | byte-level | Reproducibility contract; not a manifold field |

The pattern: numerical fields are PL with a DIFF interpretation in the continuum limit; categorical labels are TOP; the reproducibility hash sits below all of this at the byte level.

---

## 5. Commentary on findings

### 5.1 The framework is already mathematically richer than its single-category description would suggest

Most working-day descriptions of Hˢ say "compositional time-series on the simplex," which would suggest a single-category object. The framework is in fact a four-layer construction where each layer does work. Recognising this explicitly is *housekeeping*, not new mathematics — but the housekeeping clarifies why the framework crosses domains. It crosses domains because the **TOP** regime taxonomy is metric-invariant; it admits rigorous proofs because the **DIFF** layer is properly Riemannian; it is reproducible because the **PL** computation has byte-exact contracts; and it is *extensible* to coordinate-free formalisation because the **synthetic** layer is compatible.

### 5.2 The PL renderer is not a compromise; it is the level at which reproducibility lives

A natural worry would be that the HTML renderer "loses information" relative to the smooth underlying object. The disciplined response: it does, *and that loss is what makes reproducibility possible*. Every PL projection at finite T is byte-exact under the determinism contract; no smooth representation is. The PL → DIFF refinement is the same kind of move as the floating-point → real-number refinement: the discrete approximation is where contracts live, the continuum limit is where proofs live, and a faithful framework needs both.

### 5.3 The synthetic layer is the natural language for the renormalization-group extension

The `POST_CONFERENCE_ROADMAP_2026-06.md §4.8` entry on renormalization group and scale invariance — particularly the Conformal Cyclic Cosmology / Higgins Bounce application — would benefit from being stated synthetically. The conformal rescaling between CCC aeons is a morphism between smooth topoi; the amalgamation map is a coarse-graining functor; the fixed-point analysis of the amalgamation flow is a study of fixed objects under a functor's action. These are statements that *can* be made coordinate-free, but the current engine code states them concretely with explicit Python arithmetic. If a future paper on the RG / CCC extension is to land in a category-theoretic or formal-verification venue, the synthetic framing is what it would need.

### 5.4 The layered answer changes what the right reviewer feedback is

When a reviewer asks "what manifold is this?", the wrong reply is to name one category; the right reply is to identify which layer their question is *about*. A reviewer who asks because they want to apply a Bochner-type theorem to closure invariance is asking about the DIFF layer; a reviewer who asks because they want to run the engine on their dataset is asking about the PL layer; a reviewer who asks because they want to compare Hˢ regime classification to a paper on topological-conjugacy classes of dynamical systems is asking about the TOP layer; a reviewer who asks because they are reading Joyal-Moerdijk on smooth topoi is asking about the synthetic layer. The framework has an answer for each.

### 5.5 The discovery pattern is consistent with the rest of the framework's history

The four-layer structure was not designed deliberately; it accumulated. The DIFF object came first (acoustic experiments produced compositional measurements on a Riemannian-natural simplex). The PL implementation came next (the engine had to be written down in code that runs). The TOP regime taxonomy emerged as patterns repeated across domains and the metric-invariant labels stabilised. The synthetic compatibility was noticed retroactively, the same way Banach's 1922 contraction theorem was applied retroactively to DADI convergence (per §9 of the flagship). This is the framework's characteristic discovery pattern — *the math was always there; the bookkeeping caught up later*. The manifold-category question is one more instance.

### 5.6 What this is, and what it is not

This document is **not** a claim that the Hˢ framework has been formalised in any of these four categories beyond what the flagship's lemma chain achieves in DIFF. The flagship's eight lemmas and two theorems are stated and proved in standard analytic language; the engine outputs the fields catalogued in §4 above; the regime taxonomy is named in plain language and validated empirically on three IEEE-floor confirmation datasets. **This document is** a clarification of which mathematical category each of those existing pieces belongs to, and a sketch of what a future paper would need to do to make the synthetic-layer claim more than a sketch.

---

## 6. Post-conference work entry

Filed in `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` as a new §4.9 — "Manifold-category classification of the Hˢ projection." The work item is:

1. Short paper (8–12 pages) formalising the four-category layering with an explicit table mapping every CNT/CNQ output field to its category;
2. An exploratory note (not necessarily a paper) on whether SDG would make the RG extension of §4.8 cleaner, including a candidate axiom set for closure-as-budget-invariant and group-delay-as-rotation as Lie morphisms;
3. A reviewer-facing FAQ entry titled "What manifold is the Hˢ projection?" that gives the layered answer in a single screen of text — useful for the audience that wants the headline answer without the full paper.

**Lockdown discipline:** S2 doc-only; lives outside `CODAwork2026/`; no engine, schema, INV catalog, or NO-CREATE touches during the 2026-05-12 → 2026-06-06 window. The post-conference work itself is moderate effort — mostly clarification and bookkeeping rather than new mathematics — and lands naturally in the second post-conference sprint per `POST_CONFERENCE_ROADMAP_2026-06.md §8`.

---

## 7. Cross-references

- `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2 — the DIFF-layer proofs (Lemmas 1–8, Theorems 1–2) this note refers to.
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §4.7 (information geometry — Fisher metric as a sibling to Aitchison) and §4.8 (renormalization group; the natural place for synthetic framing); new §4.9 (this note's roadmap entry).
- `HCI-CNT/engine/CNT_PSEUDOCODE.md` — the PL-layer specification (deterministic, byte-exact).
- `HCI-CNT/engine/cnt.py`, `HCI-CNT/engine/cnt.R` — the PL-layer implementations whose byte-exact reproducibility the manifold layering helps explain.
- `AI_AGENTS.md` §1.5 — cross-domain partnership framing; the TOP regime taxonomy is what makes the cross-domain claim well-defined.

---

## 8. Acknowledgement

Question raised by Peter Higgins during pre-conference review, 2026-05-24. Layered answer developed in conversation with Claude (Anthropic); this document captures the conversation for post-conference development.

*Filed during the pre-conference lockdown, eight days before CoDaWork 2026.*
