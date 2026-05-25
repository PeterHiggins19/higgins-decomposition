# Gauge Theory and the Hˢ Framework

**Filed:** 2026-05-24 (pre-conference; doc-only, S2-class)
**Status:** Working note. Captures a gauge-theoretic reading of the Hˢ framework, consolidates four prior pieces already in the system, adds three new points of consideration, files the topic for post-conference development.
**Trigger:** Peter's question, *"how does Gauge theory apply to hs? seems like a natural fit"* — followed by three points of consideration: *"data driven; manifold could be anything, hs could be used to generate any manifold given the data as hs is inert and transforms anything compositional; hs could be used as a manifold diagnostic tool and classifier"* — and the directive: *"update the system with this and all past information on this topic, do a quick coworker folder scan for past history on this, as it has come up in pieces before."*
**Companion documents:** `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2; `papers/in_progress/MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md`; `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §4.10 (post-conference work entry).
**Lockdown discipline:** S2 doc-only; `papers/in_progress/`; no engine, schema, INV catalog, or NO-CREATE touches.

---

## 1. The question

In modern physics and mathematics, **gauge theory** is the study of fields and dynamics that are invariant under a continuous group of *local* (point-dependent) transformations. The structure has four elements: a *base manifold* (typically spacetime); a *gauge group* (typically a Lie group — U(1) for electromagnetism, SU(2) for weak isospin, SU(3) for the strong force); a *gauge field* / *connection* on a principal bundle; and a *covariant derivative* / *curvature* / *holonomy* derived from the connection. The framework is unusually general — general relativity, the Standard Model, condensed-matter topological phases, and much of modern differential geometry are gauge-theoretic in this sense.

The question for Hˢ: how much of this structure is already present, how much would have to be added, and how does the gauge-theoretic reading change what the framework can be used for?

The short answer is that *substantial gauge-theoretic structure is already present*, named in pieces across the system over multiple discovery rounds, but never consolidated. This note consolidates.

---

## 2. Prior history — four pieces already in the system

A coworker-folder scan turns up four prior pieces. The gauge-theory reading is not new to the framework; it has been arriving in fragments since the early HUF discovery work.

### Piece 1 — `HUF/science/quantum/Book0_HUF_QIT_Primer.md` line 335 (explicit identification)

The HUF Quantum-Information-Theory Primer's structural-isomorphism table identifies nine deep correspondences between quantum mechanics and compositional data analysis. The very first row reads:

> **# I — Basis ambiguity (Quantum) ↔ Log-ratio choice ALR/CLR/ILR (CoDa) — Mechanism: Gauge freedom**

This is the central correspondence of this note, already stated as item I of the master CoDa↔Quantum table. *The framework has known that log-ratio basis choice is a gauge freedom since the QIT Primer was filed.* The rest of this note builds out the implications.

### Piece 2 — `HUF/science/quantum/HUF_Topography_Conjecture_v1.0.md` §6 "The Induced Manifold" (data-driven manifold premise)

The HUF Topography Conjecture states explicitly:

> **§5.4** "The manifold grows organically from the data, never imposing resolution where the system does not demand it."
> **§6.1 [CONJECTURE]** "When data induces a manifold M embedded in the simplex, it inherits a Riemannian metric from the ambient Aitchison geometry."
> **§6.1 [CONJECTURE]** "The solution manifold M minimizes a distortion energy functional: E = ∫_M MDG(dρ) vol_g — where MDG acts as local strain (drift intensity) and vol_g is the Riemannian volume form."
> **§6.2 [ANALOGY]** "The Sufficiency Frontier, where HUF monitoring ceases to be valid (component reaches zero, information is lost), corresponds to the boundary ∂M of the manifold."

This is exactly the *"manifold could be anything"* and *"Hˢ is inert"* points Peter named, already filed as a CONJECTURE under HUF topography. The framework has known that the manifold is data-induced (not data-imposed) since the Topography Conjecture was filed. *The CONJECTURE status is significant — it has been provisionally stated, awaiting empirical and theoretical validation.*

### Piece 3 — `Current-Repo/RWA/concepts/v-infinity-core/V_Infinity_Core_Project.txt` and `V_Infinity_Core_Dialog.txt` (V∞Core archive — extensive gauge-theoretic reference material)

The V∞Core RWA archive contains substantial gauge-theory reference content, accumulated across discovery rounds: Yang-Mills instantons (Belavin-Polyakov-Schwartz-Tyupkin 1975); pure SU(2) gauge theory; Yang-Mills self-duality F = *F; θ-vacuum / CP problem; Dirac operator on 4D manifolds with gauge field; AdS/CFT duality (N = 4 SU(N) super Yang-Mills CFT ↔ type IIB string theory on AdS5 × S5); gauge transformations and gauge invariance for Berry-phase wave functions; **Berry connection as U(1) gauge field** (𝒜ᵢ = i ⟨n | ∂_Rᵢ | n⟩); Chern number from Berry curvature with Dirac monopole quantization; SM gauge-group emergence in non-commutative geometry (Connes-Chamseddine spectral action); gauge field emergence fluctuation in V∞ proxies. This is reference background — the framework has the vocabulary already, accumulated from RWA-era research, awaiting consolidation back into the Hˢ working chain.

### Piece 4 — Hˢ "Gauge R&R" (productive coincidence — measurement-systems gauge throughout the framework)

The Hˢ framework uses **Gauge R&R** (Gauge Repeatability and Reproducibility) — a measurement-system-analysis concept from production engineering — as a discipline-level requirement. The phrase appears across the framework: `EXECUTIVE_SUMMARY.md` ("Gauge R&R confirmed deterministic"); `Hs_Reference_Standard_Library.md` ("Gauge R&R verified — bit-identical results"); `higgins_decomposition_12step.py` ("GAUGE R&R COMPARISON" section, `gauge_rr_compare(results_a, results_b)` function); `Hs_EXPERIMENT_RERUN_PLAN.json` ("Gauge R&R: state deterministic"); `HUF/codawork2026/experiments/gauge_rr_full.py`, `GAUGE_RR_canonical_results.json`, `GAUGE_RR_full_report.json` — a full empirical Gauge R&R experiment chain.

This is the *measurement-systems* sense of "gauge" (a calibrated instrument), not the *gauge-theory* sense (a continuous group of local transformations). The two are different English words historically — both descend from Old French *jauge*, "measuring rod" — but their meanings in modern physics and modern engineering diverged. **And yet the productive coincidence is real**: the framework's measurement-systems gauge (bit-identical reproducibility, SHA-256 hash verification, deterministic state) is the *operational corollary* of the abstract gauge-theory structure (closure as a constraint that survives the dynamics; CLR as a gauge fixing that produces a unique representative). A framework that takes its abstract gauge theory seriously *will* produce reproducible measurements; the empirical reproducibility *is* the framework's anomaly-cancellation in action. The two senses of "gauge" are not just a coincidence of vocabulary — they are dual aspects of the same disciplinary commitment.

---

## 3. The correspondences — gauge-theoretic reading of the Hˢ framework

With the prior pieces in view, the correspondences can be stated cleanly. Several are tight in the strict mathematical sense; several are suggestive but worth working out.

### 3.1 Tight correspondences

**Closure as a gauge constraint.** Σpᵢ = 1 is exactly a gauge constraint: the raw measurement vector lives in ℝᴰ₊ and the closure step quotients out the multiplicative positive reals (ℝ₊, ·). The CLR transform is *literally a gauge fixing* of that ℝ₊ symmetry — it picks the unique representative whose log-components have zero mean. The identity clr(λ · p) = clr(p) for any λ > 0 (Lemma 7 of the flagship paper) is a **Ward identity** in the strict sense: a conservation law that follows directly from gauge invariance. The ILR-Helmert transform is a second gauge fixing — an orthonormal-basis choice on the gauge-fixed surface. This is the QIT Primer line 335 correspondence stated at full strength.

**CNQ's phase space is a gauge group.** S³ ≅ SU(2) is not "like" a gauge group — it *is* the simplest non-abelian Yang-Mills gauge group (the gauge group of weak isospin in the Standard Model). The flagship paper's Lemma 5 (group-delay-as-rotation as a Lie one-parameter subgroup g(τ) = exp(τ · ξ) of SU(2)) is, in gauge-theoretic language, a **holonomy / Wilson-line** computation: integrate a connection along a path, ask what rotation accumulates. The unified formula (Theorem 1) reads as a sum of three holonomies — one in the Aitchison/ℝ₊ gauge, one in the SU(2) phase gauge, one in the closure-budget gauge.

**Closure-failure flag is an anomaly.** In gauge theory, an *anomaly* is an obstruction — a symmetry that holds classically but is violated by the dynamics. The Hˢ framework's `closure_failure_flag` is exactly that: it fires when the system's evolution violates the gauge constraint that was supposed to be conserved. ADAC, in this reading, is an **anomaly-cancellation mechanism**: it computes the counter-term needed to restore the constraint, applies it inside the closed loop, and reports the magnitude of the counter-term as a diagnostic. The Paired Measurement Doctrine ("one curve lies") becomes the statement that anomalies are visible only when two independent gauge-fixings disagree.

**DADI is parallel transport with Banach-bounded holonomy.** DADI iterates a contraction on the simplex; in gauge-theoretic language this is parallel transport along the iteration trajectory using the Aitchison connection. The Banach contraction κ < 1 (Lemma 4 of the flagship) is the statement that **the holonomy around any closed iteration loop is bounded** — the system cannot accumulate arbitrary phase, which is what makes the fixed-point well-defined. The convergence proof is then a statement about the curvature of the Aitchison connection being small enough relative to the iteration step.

### 3.2 Suggestive correspondences worth working out

**Helmsman family / IR class as topological-invariant gauge data.** The regime taxonomy labels (Helmsman family sign/stability/flips/chaos/torque/joint; IR class LIMIT_CYCLE_P1 / LIMIT_CYCLE_P2 / etc.) look very much like **Chern-class** / **winding-number** invariants in gauge theory. They classify topologically inequivalent flows on the principal bundle. Whether this is a formal correspondence or a structural analogy is the kind of question the post-conference work would settle.

**CNT and CNQ as two principal bundles over the same base.** The engine-independence policy (cnt_content_sha256 ⊥ cnq_content_sha256 by design) admits a natural gauge-theoretic reading: CNT is the bundle of static partition data over the closed simplex; CNQ is the bundle of dynamic phase data over the same base. They share the base (composition + budget) but live in different fibres. The engine-independence policy is then the statement that **the two gauge sectors are decoupled** — a hygienic choice that gauge theory has a clean language for.

**ADAC as gauge fixing in the open-by-default loop.** ADAC defends the budget c against environmental drift; in gauge-theoretic language this is *fixing a gauge in the presence of dynamics that would otherwise drift away from the chosen representative*. The HUF-GOV ↔ HUF-CLS fork at ADAC (observe-or-control) is then the choice between *gauge fixing as observation* (HUF-CLS) and *gauge fixing as control* (HUF-GOV).

**Renormalization group connection.** The roadmap §4.8 entry on RG / CCC becomes natural in this framing: RG flow on gauge couplings is standard physics; the amalgamation engine (`hs_amalgamation.py`) is a coarse-graining operation in RG sense; the conformal rescaling between CCC aeons is a gauge transformation in Penrose's original formulation. The RG extension *wants* to be gauge-theoretic.

---

## 4. Three new points of consideration (Peter, 2026-05-24)

These three points, raised in the trigger message, sharpen the gauge-theoretic reading into a stronger claim about *what Hˢ can be used for*.

### 4.1 Data-driven

The framework does not specify a manifold a priori and then read data on it. The framework *reads data first* and then realises whatever manifold the data carries. The CNT/CNQ engine is *inert* — it imposes no semantic content, no domain-specific structure, no application-specific assumptions. Closure, Aitchison metric, ILR basis, Helmsman taxonomy, CNQ quaternion phase — these are *general-purpose* operators that act on any compositional time-series, regardless of what the carriers physically are. The manifold that emerges is whatever the data induces.

This is exactly the HUF Topography Conjecture §6 framing — *manifold grows organically from data* — and it is exactly inverted from the standard physics workflow. Standard physics: specify a manifold (Minkowski spacetime, an AdS5 × S5 background, a Riemann surface), specify a gauge group (U(1), SU(2), SU(3)), specify the matter content, derive the dynamics. Hˢ workflow: feed compositional measurements in, *observe* the gauge group (it will be ℝ₊ at minimum, plus SU(2) if quaternionic phase is in play, plus whatever the regime taxonomy reveals), observe the induced Riemannian metric (it will be Aitchison-like with whatever curvature the data carries), observe the topological invariants (Helmsman family, IR class). The framework is **gauge-theory from the data, not gauge-theory imposed on the data**.

### 4.2 The manifold could be anything — Hˢ as universal manifold generator

Because the framework is inert and the manifold is data-driven, **Hˢ can be used to generate any manifold that any compositional dataset carries**. The role of the framework is not to *be* a manifold; the role is to *produce* the manifold the data has. This reframes Hˢ from "an analysis tool for one kind of manifold" to "a universal manifold-construction kit for compositional data." The constraint is only that the data be compositional (closed, non-negative, finite-carrier). Within that constraint, the manifold can be anything — periodic, chaotic, fractal, multi-scale, entangled, anomalous — and the framework will produce the manifold that is there.

This is a strong claim. It rests on the inertness of the engine: the moment the engine starts imposing structure (a specific gauge group, a specific metric, a specific regime), it stops being a universal generator and becomes a specific instrument. The current Hˢ engine has been carefully kept inert — the lemma chain (Banach, Helmholtz, Rayleigh-Sommerfeld, Gershgorin, group-delay-as-rotation, closure invariance under CLR, equivalence of Aitchison representations, contraction-spectrum bound) imposes only the structure that *all* compositional time-series share, and leaves everything else for the data to fill in. *Inertness is the design choice that makes universality possible.*

### 4.3 Hˢ as manifold diagnostic and classifier

The corollary of universal manifold generation is **universal manifold diagnosis**. Once the framework produces the manifold the data carries, it can *classify* it:

- The **gauge group** is read from the dynamics — ℝ₊ alone (static closure); ℝ₊ × SU(2) (closure + quaternionic phase); ℝ₊ × SU(2) × (further structure) (closure + phase + entanglement, in the language of roadmap §5).
- The **Riemannian curvature** is read from the κᴴˢ matrix — flat regions indicate stable monitoring; high-curvature regions indicate tight clustering of drift events (per HUF Topography Conjecture §6.1).
- The **topological invariants** are read from the Helmsman family / IR class labels — period-2 vs limit-cycle vs chaotic vs anomalous; Chern-class-analogue winding numbers.
- The **anomaly content** is read from the closure-failure flag and the ADAC counter-term magnitude — a non-zero anomaly indicator means the gauge symmetry is being broken by the dynamics.
- The **bundle structure** is read from the CNT/CNQ independence — whether the static and dynamic sectors decouple cleanly or whether there is cross-talk that would indicate a deeper bundle structure.

Used this way, Hˢ becomes a **gauge-theoretic diagnostic instrument**: pour compositional data in, get out a complete characterisation of the manifold the data carries (group, metric, topology, anomalies, bundle structure). This is what Peter named — *"Hˢ could be used as a manifold diagnostic tool and classifier"* — and it is the natural endpoint of the inertness + data-driven framing.

---

## 5. Commentary on findings

### 5.1 The gauge-theoretic reading was already in the system, distributed

The most striking finding from the scan: every piece of the gauge-theoretic reading is already in the system somewhere. The CLR-as-gauge-freedom correspondence is in the QIT Primer (line 335, filed years ago). The data-driven manifold premise is in the HUF Topography Conjecture (§6, filed as a CONJECTURE awaiting validation). The Yang-Mills / SU(2) / Berry-connection vocabulary is in the V∞Core RWA archive (reference material from prior research rounds). The measurement-systems Gauge R&R discipline is throughout the Hˢ working chain. **What was missing is consolidation** — bringing the four pieces together under the heading "Hˢ is a gauge theory whose pieces are already here, awaiting bookkeeping." This note is that bookkeeping.

This is the same discovery pattern documented in the flagship's §9 and in the manifold-category note: *the math was always there; the recognition catches up later*. Banach's 1922 contraction theorem applied retroactively to DADI; the four-category manifold layering recognised retroactively from existing engine fields; now the gauge-theoretic reading recognised retroactively from QIT Primer + Topography Conjecture + V∞Core + Gauge R&R. The framework's discovery pattern is consistently *retroactive recognition of structure that the engineering already implements*.

### 5.2 Inertness is the design choice that makes gauge-theoretic universality possible

The three new points (data-driven; manifold-could-be-anything; Hˢ-as-classifier) all depend on the **inertness** of the engine — the fact that the framework imposes only what *all* compositional time-series share, and leaves everything else for the data. Inertness is not a passive property; it is an active design discipline. Every time someone proposes to bake a specific gauge group, a specific metric, a specific regime model into the engine, the framework's universality shrinks. The lockdown discipline (NO-CREATE files; engine version policy; DCP review of every promotion) is, in this reading, the operational defence of inertness. *The framework stays universal by refusing to specialise prematurely.*

### 5.3 The four pieces consolidate into a single post-conference paper

The post-conference work item is to write a single paper consolidating the four pieces — provisional title *"Hˢ as a Gauge Theory: Closure, Holonomy, and Anomaly in Compositional Dynamics"* — with the structure:

1. The QIT Primer correspondence (CLR/ALR/ILR as gauge freedom)
2. The Topography Conjecture (data-induced manifold; manifold-as-classifier)
3. The flagship's lemma chain re-stated in gauge-theoretic language (closure = Ward identity; Banach contraction = bounded holonomy; group-delay = SU(2) one-parameter subgroup; closure-failure flag = anomaly indicator)
4. The three new points (data-driven; manifold-could-be-anything; Hˢ-as-classifier)
5. The application: Hˢ as universal gauge-theoretic diagnostic for compositional data
6. The synthetic-layer formalisation (per `MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md`) as the natural language for the final write-up

This is moderate effort — most of the material exists, the work is to integrate. It belongs in the second post-conference sprint per `POST_CONFERENCE_ROADMAP_2026-06.md §8`.

### 5.4 The reframing changes the framework's audience

Stated as "compositional time-series analysis on the simplex," Hˢ has an audience of CoDa practitioners, time-series statisticians, and domain specialists in the seven application domains. Stated as "a gauge-theoretic universal manifold-construction kit for compositional data," Hˢ has *additionally* an audience of theoretical physicists, differential geometers, dynamical-systems theorists, and category theorists. The post-conference paper would not change *what the framework does* — it would change *who recognises the framework as relevant to their work*. This is the manifold-category note's §5.4 observation applied to the gauge-theory reading: identifying the right vocabulary lets the right audience find the framework.

### 5.5 The framework's empirical record reads differently under the gauge-theoretic lens

Several entries in the empirical record read sharper under the gauge-theoretic framing:

- **Activation Coefficient INV-060** (760× USA Solar 2012→2013) — an anomaly in the gauge-theoretic sense: the system's evolution violated the conserved budget on a single-year timescale by a measured factor of 760. The ADAC mechanism *was* the anomaly-cancellation operator.
- **5-of-9 deceptive-drift signature INV-051** (AUS/CHN/GBR/IND/JPN) — a topological invariant of the monitoring structure (per Topography Conjecture §5.3 wording: "topological invariants of the monitoring structure itself, not of the data"); five non-trivial winding numbers in one signature.
- **Three IEEE-floor confirmation datasets** (Backblaze D=4, Planck CMB D=4, SM neutrino D=3) with max_residual = 4.441×10⁻¹⁶ — the Ward identity (closure invariance under CLR) holds to machine precision across three independent gauge configurations. This is the empirical statement that the gauge symmetry is preserved in the dynamics of three independent systems.
- **CCC / Higgins Bounce target** (roadmap §4.8) — the conformal rescaling between cosmological aeons is a gauge transformation in Penrose's original formulation; the framework already has the bookkeeping infrastructure for it.

Reading the empirical record this way doesn't change the numbers; it changes the *story* the numbers tell.

### 5.6 What this is, and what it is not

This document is **not** a claim that Hˢ has been formalised as a gauge theory in the technical sense. The flagship's lemma chain is stated in standard analytic language; the engine outputs are numerical fields; the regime taxonomy is named in plain language. **This document is** a consolidation of four prior pieces in the system that *together* articulate a gauge-theoretic structure already present in the framework, plus three new points (data-driven; inert-and-universal; manifold-classifier) that sharpen the framing into a stronger claim about what the framework can be used for. The post-conference work is to formalise the consolidation as a single paper.

---

## 6. Post-conference work entry (filed in `POST_CONFERENCE_ROADMAP_2026-06.md §4.10`)

The work item is:

1. **Short paper (12–16 pages):** *"Hˢ as a Gauge Theory: Closure, Holonomy, and Anomaly in Compositional Dynamics."* Integrates the four prior pieces + the three new points + the flagship lemma chain re-stated in gauge-theoretic language.
2. **Engine documentation pass:** add a gauge-theoretic glossary entry to every README explaining the four correspondences (closure = Ward; CLR = gauge fixing; S³ = SU(2); closure-failure = anomaly). Engineering-level — no engine touches; just adding a section to existing docs.
3. **Empirical record re-read:** review the published INV entries through the gauge-theoretic lens; identify which entries are anomalies (gauge-theoretic sense), which are bundle-structure observations, which are Ward-identity validations. Output: a new column in the INV catalog naming the gauge-theoretic interpretation.
4. **Conjecture promotion:** the HUF Topography Conjecture §6 (data-induced manifold) is currently `[CONJECTURE]`; the consolidated paper would either upgrade it (if the gauge-theoretic framing provides the formal underpinning) or leave it provisional (if not). DCP candidate after the conference.
5. **Cross-link to `MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md` §4.9** — the synthetic layer is the natural formalism for the gauge-theoretic statements; the two notes converge.

**Effort:** moderate. Mostly consolidation + clarification + bookkeeping. The hard part is choosing which level of formalism to write the consolidated paper in (analytic / synthetic / both). **Sequencing:** second post-conference sprint per roadmap §8 (weeks 5–10 post-conference), after the H₁ Banach-Higgins extension lands.

**Lockdown discipline:** all five steps are S2 doc-only or post-lockdown engineering. None of them touches the locked surfaces.

---

## 7. Cross-references

- `HUF/science/quantum/Book0_HUF_QIT_Primer.md` line 335 — the QIT Primer master correspondence table; item I (basis ambiguity ↔ log-ratio choice ↔ gauge freedom) is the seed of this entire reading.
- `HUF/science/quantum/HUF_Topography_Conjecture_v1.0.md` §§5.4, 6.1, 6.2 — data-driven manifold; Riemannian structure conjecture; sufficiency frontier as manifold boundary.
- `Current-Repo/RWA/concepts/v-infinity-core/V_Infinity_Core_Project.txt` (and `_Dialog.txt`) — Yang-Mills / SU(2) / Berry-connection / gauge invariance reference material accumulated across discovery rounds.
- `HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md` — CNQ quaternion view; the SU(2) phase structure that the gauge-theoretic reading lifts to a gauge group.
- `HCI-CNQ/doctrine/CENTRAL_CLAIM.md` and `Quaternion Decomposition/QD_CENTRAL_CLAIM.md` — CNQ central claim; quaternionic dynamics as the SU(2) sector.
- `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2 — Lemma 4 (Banach), Lemma 5 (group-delay-as-rotation), Lemma 7 (closure invariance under CLR) — the three lemmas that re-state most cleanly in gauge-theoretic language.
- `papers/in_progress/MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md` — the synthetic-layer companion to this gauge-theoretic note; the two converge.
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §4.8 (renormalization group; CCC), §4.9 (manifold-category classification), §4.10 (this note's roadmap entry).
- `EXECUTIVE_SUMMARY.md` line 28 and `tools/pipeline/higgins_decomposition_12step.py` lines 27, 297, 370, 1532–1534 — the measurement-systems "Gauge R&R" discipline that is the operational corollary of the abstract gauge-theory structure.

---

## 8. Acknowledgement

Question raised by Peter Higgins during pre-conference review, 2026-05-24, immediately after the manifold-category question of the same date. Gauge-theoretic reading developed in conversation with Claude (Anthropic); prior pieces in the system identified through coworker-folder scan at Peter's direction; three new points of consideration contributed by Peter as part of the same exchange. This document captures the conversation, the scan, and the consolidation for post-conference development.

*Filed during the pre-conference lockdown, eight days before CoDaWork 2026.*
