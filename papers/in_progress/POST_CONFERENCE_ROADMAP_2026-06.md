# Post-Conference Research Roadmap — Beyond the Simplex

**Filed:** 2026-05-22 (during pre-conference lockdown; doc-only, S2-class).
**Triggers:** Peter's reflection on H₁'s Hilbert-space generalization and the question *"what other portions can this be applied to, do the transcendentals and other components allow for work where a budget is flexible or almost chaotic, is the CNT tower useful for this, attractors?"* — followed by the directive: *"document it fully and file it for work to complete after CoDa along with a list of other projects that are scheduled to revise."*
**Status:** Working roadmap. Not yet committed to as work plan; the document organizes the *space* of post-conference research and engineering and identifies which structures must be added in which order. Sequencing of actual work happens after the 2026-06-06 lockdown clears.
**Companion documents:**
- `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2 — the mathematical foundation this roadmap extends.
- `papers/POST_CODA_PARTNERSHIP_TARGETS.md` v4 — the 14-system metabolism matrix (the *who-to-engage* roadmap; this document is the *what-to-build* counterpart).
- `huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json` `post_conference_implementation_targets` — the 5-order engine-side work list.
- `ai-refresh/INVESTIGATION_CATALOG.json` — 8 STAGED entries scheduled for promotion to CANONICAL after the conference.

**Scope discipline.** This document lives at `papers/in_progress/`, outside the `CODAwork2026/` lockdown surface and outside the engine/schema lockdown. It develops freely; nothing committed here disturbs anything in the conference-prep arc. Items proposed here are *candidates* for post-conference work, not commitments — the framework's discipline is that each promotion to CANONICAL passes through DCP review per Hs Change Control v1.0.

---

## 1. Where we stand at v2.2

The framework as it stands today handles **fixed-budget compositional time-series on a closed simplex with a known partition structure**. The closure constraint Σ pᵢ = 1 is enforced; the apportionment is rigid; the budget is a measured invariant. CNT reads the static partition; CNQ reads the dynamic trajectory; the unified formula (Theorem 1 of the flagship) ties them together. The lemma chain (Banach, Helmholtz, Rayleigh-Sommerfeld, Gershgorin, group-delay-as-rotation, closure invariance under CLR) closes the mathematical core.

This is one portion of a much larger space. The H₁ paper (2026-02) already shows the next move — `H₁|ψ⟩ = μ(|ψ⟩) · u` is defined for any normed inner-product space with any projector P. The simplex case lives inside H₁ as a specific instance; H₁ supports portions the simplex framework does not yet reach.

**The question of this roadmap is: which portions does the framework support natively, which are reachable by adding bounded structure, and which are open frontiers?**

---

## 2. The H₁ generalization ladder — five steps from fixed to chaotic

The path from the current Hˢ framework to the chaotic / attractor regime runs through five increments. Each step preserves the previous one as a special case; each step adds bounded structure that the existing engine code can absorb without disturbing the locked components.

### Step 1 — Fixed-budget simplex (current strength, CANONICAL)

Σ pᵢ = c with c a known invariant (6.02 dB for acoustic; 100 % for any normalized compositional system). ADAC defends the budget against environmental drift; the open-by-default loop preserves the researcher's interpretive judgment. This is where the empirical record is strongest and the mathematical core is closed.

### Step 2 — Slowly varying budget (extensible from current engine)

Σ pᵢ(t) = c(t) where c(t) drifts on a time scale long compared to the iteration. The Banach contraction proof of Lemma 4 still applies if the iteration's contraction rate beats the budget's drift rate. ADAC, currently used to defend a constant c against measurement drift, becomes the natural mechanism to *track* a slowly-varying c. **The work to add:** an explicit `c(t)` field in the CNT engine output, with a tracking-rate diagnostic per step. **Estimated effort:** small. **Application targets:** stellar fusion (Gamow peak shifts with temperature), urban infrastructure (demand drifts with population), industrial production (capacity drifts with line conditions).

### Step 3 — Stochastic budget (Banach-Higgins extension)

`c` is drawn from a distribution at each step. The Banach-Higgins extension `H_B(x) = f(x/‖x‖) · x/‖x‖` where `f : B → [0, 1]` is a continuous functional on the unit sphere already covers this case in the H₁ paper. The iteration converges in expectation if `|⟨f⟩| < 1`. **The work to add:** ensemble-averaging machinery in CNT (run the iteration N times with budget samples; report ensemble fixed point + variance); a `stochastic_closure` block in the engine output. **Estimated effort:** moderate. **Application targets:** EUV lithography wavefront control (shot noise on photon counts), medical ultrasound (return-signal stochasticity in tissue), Backblaze-style fleet reliability (failure rate stochasticity).

### Step 4 — Strange-attractor budget (frontier)

`c(t)` wanders on a strange attractor in budget space. The framework moves from describing the budget to describing the **attractor of the budget trajectory**. This is where the **transcendental library** earns its keep: the chaotic trajectory may not settle at a single value but tends to *concentrate near* specific transcendentals (1/(π^e), e/2, 4·log₂(3), …). The transcendentals become **basins of attraction** in budget space rather than candidate constants. **The work to add:** Lyapunov-exponent block in CNT; correlation-dimension estimator; multifractal-spectrum module; transcendental-proximity matcher run against the empirical attractor distribution. **Estimated effort:** substantial; requires new engine module. **Application targets:** Conformal Cyclic Cosmology (Higgins Bounce; Planck CMB anomalies), turbulent fluid dynamics (energy-cascade composition), neural attractor dynamics (compositional state of brain regions), climate dynamics (energy-balance composition under chaos).

### Step 5 — Entangled-carrier closure (frontier; see §3 below)

The closure constraint is supplemented by *correlation constraints* between carriers that go beyond the simplex. The classical Bell-CHSH inequality becomes a measurable diagnostic — if the composition's carriers exhibit correlations exceeding the classical bound, the system is in an *entangled* state in the compositional-data sense. CNQ's twin-quaternion factoring at D=8 already touches this; the systematic theory is the next layer.

---

## 3. Entanglement structure — pairwise and groupwise

Peter's framing: *"the power of entanglement by pairwise and groupwise association and coherence and other CoDa instruments and HUF methods."* The framework already has the operations table for this on side 2 of the UN-6 handout (CHSH joint coherence, twin-quaternion factoring). What it does not yet have is a *systematic doctrine* on how entanglement-style structure works on the simplex.

### 3.1 Pairwise entanglement on the simplex

Two carriers (i, j) are *pairwise entangled* if their joint behavior carries information that neither alone carries — i.e., the joint distribution of (pᵢ, pⱼ) does not factor into marginals beyond the closure constraint. The detection diagnostic is the CHSH-style inequality applied to compositional log-ratios:

```
S_ij  =  |E(clrᵢ, clrⱼ)|  +  |E(clrᵢ, Δclrⱼ)|  +  |E(Δclrᵢ, clrⱼ)|  −  |E(Δclrᵢ, Δclrⱼ)|
```

where E is the time-averaged correlation. If `S_ij > 2` (classical bound), the carrier pair is non-classically correlated. If `S_ij` approaches `2√2` (Tsirelson bound), the correlation is maximally non-classical in the quantum-information sense.

**What to add:** a `pairwise_entanglement_matrix` output block in CNT — D×D matrix of S_ij values per timestep, with diagnostic for which pairs exceed the classical bound. **Application targets:** energy carriers where coal-decline and gas-rise are coupled by policy (electrical-mix data); microbiome species pairs coupled by metabolic exchange (microbiome compositions); gene-pair regulatory entanglement (transcriptomics).

### 3.2 Groupwise entanglement and twin-quaternion factoring

Beyond pairs, *N-carrier* groups can exhibit collective entanglement. The CNQ engine's existing twin-quaternion factoring at D=8 is the explicit machinery for this: the 8-carrier state factors into a *pair of quaternions* (each living on S³) that, combined, reproduce the joint state but separately characterize different facets of the multi-carrier coherence. This is the Hˢ-side analog of the *qubit-pair* structure in quantum information.

The CHSH inequality is *two-party*; the Mermin inequality is *N-party*. For D = 8 carriers, the relevant inequality is the Greenberger-Horne-Zeilinger (GHZ) bound applied to the compositional log-ratio vector. **What to add:** N-party joint-coherence diagnostic in CNQ — vector of GHZ-style bounds for k-tuples of carriers for k ∈ {3, 4, 5}; visual surface on Stage 3 plate. **Application targets:** stellar fusion at the Gamow peak (multi-channel reaction pathway entanglement); CMB polarization modes (E/B mode coupling); economic sector entanglement under crisis.

### 3.3 Coherence as the connecting structure

*Coherence* is the phase-side correlate of *entanglement* — it is what survives the magnitude readout. CNQ's joint quaternion field Q(t, f) at the listening position is the canonical instance: each driver's phase relative to the others is a coherence relationship; the four drivers in the BTL system are coherent precisely when their relative phases are time-invariant.

The general framework: coherence is the *persistence* of correlation structure under the framework's natural transformations (closure operator, CLR transform, ILR rotation, Hamilton product on S³). A pair of carriers that exhibits CHSH violation *and* maintains the violation across multiple transformations is *coherently* entangled — not a statistical artefact, but a structural property of the joint distribution. **What to add:** a coherence-persistence test that applies the framework's transforms in sequence and verifies the entanglement diagnostic survives. **Application targets:** medical imaging artifact detection (real structure vs noise), industrial quality control (real defect vs measurement variance), wavefront aberration classification (Zernike-mode entanglement).

---

## 4. What other structures rein in chaos

Peter's question explicitly asks for the structural inventory needed to extend the framework's reach into the chaotic regime. The mathematical objects that handle chaos are well-developed in dynamical systems theory; the question for Hˢ is which ones to absorb and in what order.

### 4.1 Lyapunov exponents (essential; Order 1 for chaos work)

The local rate of divergence of nearby trajectories. For an Hˢ trajectory on the simplex, the maximum Lyapunov exponent λ_max distinguishes:

- λ_max < 0: trajectory converges to a fixed point (LIMIT_CYCLE_P1, already classified)
- λ_max = 0: trajectory on a quasi-periodic orbit (LIMIT_CYCLE_PN)
- λ_max > 0: trajectory on a strange attractor

**What to add:** Lyapunov-block in CNT — λ_max, λ_2, …, λ_D estimates per trajectory. Pesin's identity ties the sum of positive Lyapunov exponents to the Kolmogorov-Sinai entropy of the dynamics, which is a natural complement to the framework's Shannon-entropy diagnostics already in CNT. **Effort:** moderate (well-known algorithm; the Wolf-Swift-Swinney algorithm or its modern variants).

### 4.2 Correlation dimension and multifractal spectrum

For a strange attractor, the correlation dimension D₂ measures the local clustering of the attractor (D₂ between integer dimensions indicates fractal structure). The multifractal spectrum f(α) extends this to a *spectrum* of dimensions — different parts of the attractor may have different scaling. **What to add:** correlation-dimension estimator (Grassberger-Procaccia algorithm) and multifractal spectrum (box-counting variants) in CNT. **Application targets:** financial market composition under stress (multifractal scaling of return composition), turbulence (multifractal energy cascade), seismicity (multifractal energy release composition).

### 4.3 Symbolic dynamics

Encoding a trajectory on an attractor as a sequence of symbols (partition the attractor into cells; each timestep visits a cell; the symbol is the cell label). This converts continuous chaos into a discrete language whose statistics encode the dynamics. **Why this matters for Hˢ:** the framework already has a natural partition (the simplex carriers); the *symbol sequence* of which carrier is the Helmsman at each timestep is already an output. Lifting this to formal symbolic dynamics gives access to topological entropy, periodic-orbit theory, and zeta-function methods for counting unstable periodic orbits. **Effort:** moderate; mostly diagnostic at first, deeper integration over time. **Application targets:** speech / language analysis (compositional structure of phoneme transitions), chemical reaction networks (state-space symbolic encoding).

### 4.4 Recurrence quantification analysis (RQA)

Recurrence plots reveal hidden periodicity and laminar phases in apparently chaotic time series. Quantifying the recurrence plot (recurrence rate, determinism, laminarity, trapping time) yields diagnostics that detect regime changes invisible to standard statistical tests. **What to add:** RQA block in CNT — recurrence matrix per trajectory plus the standard quantifiers. **Application targets:** ECG composition (heart-rhythm compositional analysis), polysomnography (sleep-stage composition transitions), industrial process monitoring (regime drift detection).

### 4.5 Transfer entropy and mutual information

Information-theoretic measures of directed coupling between carriers. Transfer entropy TE(i → j) measures how much knowing carrier i's history reduces uncertainty about carrier j's future. **Why this matters for Hˢ:** pairwise entanglement (§3.1) is *symmetric*; transfer entropy is *directed* — it tells you which carrier *leads* which. This is the engineering analog of "causal arrow" detection on the simplex. The Hs-01 experiment (Gold/Silver ratio) already invokes transfer entropy informally; formalizing it as a standard CNT output is straightforward. **What to add:** TE matrix per trajectory; visual surface on Stage 3 plate; cross-link to the pairwise-entanglement matrix from §3.1. **Effort:** small-to-moderate. **Application targets:** market lead-lag detection (which sectors lead which), neural causal flow (region-to-region directed coupling), supply-chain propagation (upstream→downstream cause-effect).

### 4.6 Ergodic theory and SRB measures

The mathematical framework for *natural invariant measures* on chaotic attractors. The Sinai-Ruelle-Bowen (SRB) measure is the invariant measure that arises from time-averaging an arbitrary initial condition on a hyperbolic attractor. This is the rigorous form of "what does the trajectory spend its time doing in the long run." **What to add:** time-averaged versus ensemble-averaged diagnostic comparison in CNT — if they disagree, ergodicity is broken (the attractor is *not* mixing in the time-average sense, which itself is a diagnostic). **Effort:** moderate. **Application targets:** climate scenario comparison (do different initial conditions reach the same long-term composition?), neural-circuit stability (does the same brain region reach the same compositional balance regardless of starting state?), economic equilibrium analysis.

### 4.7 Information geometry

The Fisher information metric on the simplex turns the simplex into a Riemannian manifold with a natural geometry that is *distinct* from the Aitchison geometry the framework currently uses. Aitchison geometry is the natural geometry of *log-ratio differences*; Fisher information is the natural geometry of *parameter estimation under the composition*. They agree on the closure constraint but diverge in their notion of "distance" on the simplex. **What to add:** Fisher-metric tensor as a sibling to the Aitchison metric in CNT; cross-link to the Higgins Steering Metric Tensor κᴴˢ (Order 2 already in the engine). The relationship between Aitchison and Fisher geometries is itself worth a paper. **Effort:** substantial; involves mathematical work beyond pure engineering. **Application targets:** statistical inference on compositions under parameter uncertainty; Bayesian compositional inference.

### 4.8 Renormalization group and scale invariance

For systems that exhibit scale invariance (Conformal Cyclic Cosmology, turbulence, critical phenomena), the renormalization group is the natural tool. The Hˢ amalgamation engine `hs_amalgamation.py` already exists and tests amalgamation stability of compositional classification across carrier merges — this is a *coarse-graining* operation in the RG sense. Formalizing the amalgamation engine as a *renormalization-group flow* on the simplex would connect Hˢ directly to the critical-phenomena literature. **What to add:** RG flow visualization on Stage 4 plate; fixed-point analysis of the amalgamation map; classification of attractor types under amalgamation (relevant operators / irrelevant operators / marginal operators in RG language). **Effort:** substantial; mathematically rich. **Application targets:** Conformal Cyclic Cosmology (CCC) — the framework would gain a natural language for the conformal-rescaling step between aeons; critical-phenomena physics; multi-scale infrastructure (city → metro → region → nation rescaling).

### 4.9 Manifold-category classification of the Hˢ projection (filed 2026-05-24)

A question that arose late in pre-conference prep: in which of the standard manifold categories — topological (TOP), smooth (DIFF), piecewise-linear (PL), or synthetic (Kock-Lawvere SDG) — does the Hˢ projection live? The short answer is that the projection is layered: the underlying mathematical object is **smooth** (open simplex Sᴰ⁻¹ with the Aitchison Riemannian structure; CNQ phase space S³ ≅ SU(2) is a smooth analytic Lie group), the discrete sampling and the HTML renderer are **piecewise-linear** (T-timestep polygonal trajectories; n-gon plates with vertices at θⱼ = (j/D)·2π − π/2), the regime taxonomy lives in **topological** structure (Helmsman family / IR class / closure-failure flag — invariant under metric rescaling), and the operator-level statements (Banach contraction, group-delay-as-rotation as a one-parameter Lie subgroup of SU(2), closure invariance under CLR) are **synthetic-compatible** — coordinate-free formulations that could be hosted in SDG without leaving the existing engine behind. (The standalone working note has been moved off-repo as internal.) **What to add post-conference:** a short paper formalising the four-category layering; an explicit map from each engine output field to the category it lives in; an exploratory note on whether SDG would make the renormalization-group extension of §4.8 cleaner (the conformal-rescaling step between CCC aeons is a candidate for synthetic treatment). **Effort:** moderate (mostly clarification and bookkeeping); the layered answer is already known, the work is to write it down and check it against every engine field. **Application targets:** mainly internal — sharpens the framework's mathematical identity for the reviewer audience; opens the synthetic-formalisation question as a real possibility rather than a hand-wave.

### 4.10 Gauge-theoretic reading of the Hˢ framework (filed 2026-05-24)

A second question that arose the same day: how does gauge theory apply to Hˢ? The answer turned out to be that substantial gauge-theoretic structure is already present in the framework, named in pieces across the system over multiple discovery rounds and never consolidated. A coworker-folder scan identified four prior pieces: (1) the HUF QIT Primer's master CoDa↔Quantum correspondence table, item I — *"basis ambiguity / log-ratio choice ALR/CLR/ILR / gauge freedom"* — files the CLR-as-gauge-fixing reading explicitly; (2) the HUF Topography Conjecture §6 *"the manifold grows organically from the data"* + the conjectural Riemannian structure on the induced manifold — exactly the *data-driven* + *manifold-could-be-anything* premise; (3) the V∞Core RWA archive's extensive Yang-Mills / SU(2) / Berry-connection / gauge-invariance reference material accumulated across discovery rounds; (4) the Hˢ measurement-systems *Gauge R&R* discipline throughout the working chain — a productive vocabulary coincidence whose operational meaning (bit-identical reproducibility) is the corollary of the abstract gauge structure (Ward identity from CLR invariance). The consolidated reading: **closure Σpᵢ = 1 is a gauge constraint under (ℝ₊, ·)**; **CLR is the gauge fixing**; **clr(λp) = clr(p) is a Ward identity**; **CNQ's S³ ≅ SU(2) is a non-abelian gauge group**; **group-delay-as-rotation is a Wilson-line holonomy on that gauge group**; **closure-failure flag is an anomaly indicator**; **ADAC is anomaly cancellation in the open loop**; **DADI is parallel transport with Banach-bounded holonomy**; **CNT and CNQ are two principal bundles over the same base**. Peter's three new points sharpen this further: **(a) data-driven** — the engine reads data first, the manifold emerges; **(b) inert-and-universal** — because the engine imposes no domain-specific structure, Hˢ can be used to generate *any* manifold any compositional dataset carries; **(c) manifold diagnostic / classifier** — the engine outputs (gauge group from dynamics; Riemannian curvature from κᴴˢ; topological invariants from Helmsman/IR class; anomaly content from closure-failure flag) constitute a complete characterisation of the manifold the data carries. (The standalone working note has been moved off-repo as internal.) **What to add post-conference:** a short paper (12–16 pages) *"Hˢ as a Gauge Theory: Closure, Holonomy, and Anomaly in Compositional Dynamics"* consolidating the four prior pieces + the three new points + the flagship lemma chain re-stated in gauge-theoretic language; an engine-documentation pass adding a gauge-theoretic glossary entry to every README; an empirical-record re-read identifying which published INV entries are anomalies (gauge-theoretic sense) vs bundle-structure observations vs Ward-identity validations; a DCP candidate to consider promoting the HUF Topography Conjecture §6 from `[CONJECTURE]` if the gauge framing provides the formal underpinning; cross-link to §4.9 (the synthetic layer is the natural formalism for the gauge-theoretic statements). **Effort:** moderate — most of the material exists; the work is integration plus a choice of formalism (analytic / synthetic / both). **Application targets:** broadens the audience — adds theoretical physicists, differential geometers, dynamical-systems theorists, and category theorists to the existing CoDa-practitioner / time-series-statistician / domain-specialist audience. The framework's reach grows by *recognising* what it already does, not by *adding* new capability. **Sequencing:** second post-conference sprint per §8 (weeks 5–10), after the H₁ Banach-Higgins extension lands; converges with §4.9 synthetic-formalisation work.

### 4.11 SHOCK overlay enhancement — temporal-profile classifier + dual-encoding visual (filed 2026-05-25)

Two related observations from pre-conference projector review surfaced an enhancement worth filing for post-conference development.

**Observation 1 — calendar arithmetic vs visual expectation.** Peter noticed during projector inspection that Japan's 2011 perimeter does not light up bright red under the SHOCK overlay, even though Fukushima is the canonical external shock in the corpus. The technical reason is calendar arithmetic plus the engine's step-indexing convention: the SHOCK overlay computes `d.step[t] = ‖CLR(t) − CLR(t−1)‖` indexed at the *end* of the step (lines 194–196 of `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`), with the tint at year t proportional to `d.step[t] / d.stepMax`. Fukushima (March 2011) triggered a *gradual* nuclear shutdown through 2011 — by year-end 2011 only 5 of 54 Japanese reactors were operational; by 2012 zero for a long stretch. Annualised, the 2011 mix carries a half-year of normal nuclear operation, so the 2010→2011 step is material but moderate. The 2011→2012 step is the *larger* one, because 2012 captures the full post-Fukushima composition. The bright red therefore lands on 2012, not 2011. The diagnostic is correct — Aitchison-distance 2011→2012 ≈ 3× neighbouring-year baseline is exactly what slide 8 of the talk reports. The visual mismatch with naming convention ("Fukushima 2011") is calendar-integration of an event that happened mid-year. Worth documenting in the projector's PROJECTION info panel so reviewers don't read the absence of red on 2011 as a framework defect.

**Observation 2 — color-only encoding fails near-red carriers.** Peter's second observation: the SHOCK signal is hard to read on country plates whose carrier palette includes warm tones (biomass / oil / coal-on-some-palettes). The shock-tint algorithm shifts the *stroke colour* toward red proportional to step magnitude — `stroke → red as ‖Δclr(t)‖ / max → 1` per the spec — but when carrier colours already sit near red in HSL space, the shift is visually subtle. Color alone is insufficient as the SHOCK indicator. Standard accessibility / visualization-design solution: dual-encoding via stroke *width* in addition to stroke *colour*, so the SHOCK signal is readable independent of the base palette. Proposed: stroke width = `baseStroke + k · (d.step[t] / d.stepMax)` with `k` ≈ `2–3 × baseStroke`, so the strongest shocks render at 3–4× normal thickness — visible against any palette including dark themes, color-blind viewers, or printed projector handouts.

**Observation 3 — the SHOCK overlay is a magnitude detector, not a cause classifier.** The current implementation tints proportional to `‖Δclr(t)‖` regardless of pattern. But the framework can distinguish three temporal profiles that a magnitude-only signal collapses together: **external shock + multi-year reorganisation** (single large step followed by elevated-but-smaller steps over many years — Japan 2011→2012 spike then 2013–2018 elevated baseline); **internal drift** (sustained pattern of moderate steps over many years — Germany's smooth-arc signature with no single dominant step); **regime change with re-stabilisation** (sharp single step then rapid return to a new baseline — UK's coal-exit jump-and-return signature). These three correspond to the three archetype labels already in the talk (slides 5–11) but the SHOCK overlay does not currently surface them. A temporal-profile classifier extension would compute, alongside `d.step[t]`, the local-temporal-context: was the previous year quiet (suggesting an isolated shock event onset)? Is the next 3–5 year window elevated (suggesting multi-year reorganisation)? Does the trajectory return to baseline within ~2 years (suggesting regime change)? Same Aitchison-step data, additional pattern-recognition layer.

**What to add post-conference:**

1. **Calendar-integration documentation in the PROJECTION info panel** — small UI text noting that the SHOCK tint at year t reflects the year-over-year step *into* year t, and that mid-year events (Fukushima March 2011) show their strongest tint at year t+1 due to annual aggregation. *Effort: trivial; ~10 minutes of HTML edit.*

2. **Dual-encoding stroke-width modulation** — *superseded 2026-05-25 by the simpler v2.2 design below.* The original proposal: modify the projector's draw function so SHOCK toggles both stroke colour AND stroke width per step magnitude. Implemented briefly as v2.1 then replaced — see *channel-discipline doctrine* note below.

   **v2.2 actual implementation (2026-05-25, in the working tree, held for push #64):** the SHOCK signal moved off the perimeter stroke entirely and onto the **year/plate text label**. When SHOCK is on and `smag > 0.5`, the year label flips to the **chromatic opposite** of the plate's base color: `lblR = 255−cr, lblG = 255−cg, lblB = 255−cb`, with a small alpha bump (≤ +0.2). Carrier identity stays clean in the perimeter line (color unchanged, width unchanged); the SHOCK indicator gets a previously-unused visual channel of its own. One `ctx.fillStyle` assignment per labelled year; no interference with carrier-color encoding; high contrast against any palette by RGB-complement math. *Effort: trivial; ~15 minutes of JavaScript edit. Visual QA on JPN + BARY + SHOCK confirms 2012 (smag ≈ 1.0) flips to bright chromatic-opposite; 2011 (smag ≈ 0.3) stays gold — consistent with the threshold and with the calendar-arithmetic explanation captured in Observation 1 above.*

3. **Temporal-profile classifier** — add a Helmsman-family-style label per country trajectory derived from the temporal context of SHOCK signals: `external_shock_with_reorganisation` (Japan); `regime_change_jump_and_return` (UK coal exit); `internal_drift` (Germany Energiewende); plus the null label `no_significant_shock` for trajectories where `max(d.step[t]) / median(d.step[t])` does not exceed a configurable threshold (~3×). Surface the label in the projector's info panel and in the per-country CNT JSON output as a `temporal_profile_classification` field. *Effort: moderate; involves engine-side computation (CNT v3.x diagnostic block extension) + schema bump + projector UI surface + classifier-threshold calibration on the 9-country corpus + null-model justification. S1 push class — requires DCP lifecycle per Hs Change Control v1.0; queued for post-conference promotion.*

**Why this matters.** Conference attendees who experiment with the live projector will form their impression of the framework partly through the SHOCK overlay. A SHOCK signal that is *visually subtle on certain palettes* and *visually misindexed by one year on annual data* reads as a framework limitation when it is actually correct behaviour insufficiently surfaced. The fix is small at the projector layer and modest at the engine layer; the *interpretive payoff* is that the SHOCK overlay becomes a classifier of dynamics-type rather than just a magnitude detector. The three temporal profiles correspond exactly to the three archetypes the talk introduces on slide 5 — Germany's continuous arc, Japan's loop-and-reorganise, UK's jump-and-return — so the classifier extension closes the loop between the verbal labels and the live visualization.

**Application targets:** primary — Hˢ projector and per-country CNT JSON output. Secondary — applies to any compositional time-series with annualised data covering events that span calendar years (electricity transitions, financial shocks at fiscal-year boundaries, climate-event annualisation). The dual-encoding visual fix generalises to any color-coded compositional visualization. The temporal-profile classifier generalises wherever the framework wants to distinguish shock-then-reorganisation from drift from regime-change in the same observable.

**Sequencing:** items 1 and 2 (documentation + dual-encoding) are S2 doc/UI-only and lockdown-compatible *after* the conference — land them in the first post-conference sprint. Item 3 (temporal-profile classifier) is S1 — engine-touching plus schema bump — and lands in the second post-conference sprint after DCP review.

**Trigger:** Peter's projector observation 2026-05-25 during pre-conference QA: *"on the Japan html when shock is activated the 2011 year does not light up with a red perimeter is this because it is identified as an external shock and not internal drift"* followed by *"i think also the colors and the red highlight are not clear, could the line thickness also increase, so the color is not the only indicator of shock, it is hard to see on colors close to red."* The first observation surfaced the calendar-arithmetic explanation + the magnitude-vs-classifier distinction; the second surfaced the dual-encoding fix. Then immediately after the v2.1 dual-encoding was implemented, Peter's third observation: *"instead of lighting the band red, simplify, make the year/plate markers the chromatic opposite color as a marker by text change, simple, and removes messing with the line colors and widths."* This third move triggered the v2.2 redesign and surfaced the channel-discipline doctrine recorded below.

**Channel-discipline doctrine — small but real, captured here as the worked-example of a principle that should travel.** The v2.1 → v2.2 redesign was not just a simplification; it was a recognition that visual channels are like driver bands in an active loudspeaker — *each one owns one job, and crossover overlap is always lossier than it looks*. The plate perimeter stroke was already doing two jobs: (i) carrier identity via base color, (ii) perspective depth via base line width. v2.1 attempted to add a third job — SHOCK magnitude — to those same two channels via color shift and width modulation. Every additional encoding axis stacked onto an existing channel costs more in interference than it gains in salience; the SHOCK signal *fought* the carrier-identity signal for the line color, and the visual cost was that the SHOCK signal read as subtle where the line was already loud. v2.2's move — *find a clean channel that isn't yet doing any work* — recognised that the year-label text color was idle (it only had to render "this is the year stamp" in a fixed gold), and gave the SHOCK indicator that empty lane. One channel, one job. The change went from fifteen lines of color-shift + width-multiplier logic to five lines of `lblR/lblG/lblB` assignment, *and the visual result is clearer at the production-render layer because the renderer no longer recomputes color shifts AND width AND stroke per-frame on every plate.* Simpler design + faster runtime + cleaner separation of concerns, simultaneously. The principle to record:

> **Each visual channel owns one job. Adding a diagnostic = find a clean channel, not stack onto a busy one. If no clean channel exists, the diagnostic isn't ready yet — refine the diagnostic until it fits a single channel.**

This is the same physics as the **constant-power Butterworth crossover decision from BTL** (flagship §4.2). Let each driver own its band cleanly; don't ask one driver to do two jobs at the crossover boundary because crossover compromises are always lossier than they look. Acoustic engineering taught the discipline at the BTL acoustic layer in 2024; the projector inherited it at the visualization layer in 2026. The framework's recursion-test pattern in action: *the framework that walked from BTL to Hˢ knows things about itself it learned at the previous level.*

**Applications of the doctrine.** Future diagnostic visualizations on Stage 4 plates that don't exist yet; HUD overlays on the projector; per-country plate annotations under the temporal-profile classifier (item 3); any future tier (HCI-AUDIO listening-position alignment indicators, HCI-ULTRASOUND non-contact-measurement readiness markers) where a new diagnostic needs a visual home. The discipline is to inventory the busy channels first, find the idle ones, and assign new work to the idle ones. Where every channel is busy, the diagnostic is one design iteration premature — refine it until it fits a single previously-unused channel, or accept that the diagnostic is fundamentally a multi-channel object that needs explicit coordination rather than overlay.

### 4.12 Attractor morphology + transcendental basins (filed 2026-05-27)

Consolidation of §4.1–§4.6 + §4 Step 4 under one organising principle. Peter's mid-conference-prep flash, *"strange attractor analysis, it just flashed, what does it mean? what could cnt do with it?"* — followed by the synthesis *"the transcendentals and the complex conjugates and the old html demos and the morphological analysis is in my thinking i believe."* — surfaced that six separately-listed roadmap entries (Lyapunov, correlation dimension, symbolic dynamics, RQA, ergodic theory + SRB measures, the transcendental basin hypothesis) are all members of one diagnostic suite: **the attractor fingerprint**. Per-trajectory seven-component signature consisting of Lyapunov spectrum {λ₁,…,λᴅ₋₁}, correlation dimension D₂, embedding dimension dₑ (Takens delay-coordinate reconstruction), RQA block (RR / DET / LAM / TT / L_max), topological entropy h_top, UPO skeleton (unstable-periodic-orbit decomposition), and SRB-measure transcendental-proximity matcher (matches the empirical SRB-measure moments against the framework's existing transcendental library — finally formalising the §4 Step 4 hypothesis as a measurable quantity). The framework's substrate is already in place: CNT trajectories on the simplex are bounded by closure (a strange-attractor mathematical precondition); the Aitchison-step time series `‖Δclr(t)‖` is the input for Lyapunov computation; the CLR-space trajectory is the input for correlation dimension; the scalar Helmsman-index time series is the input for Takens embedding; CNQ's quaternion algebra (q · v · q* sandwich; complex-conjugate eigenvalue pairs in S³ ≅ SU(2)) is *the natural algebraic carrier* for the spectral signature; the framework's Helmsman family taxonomy is a coarse first-pass morphological classifier that the strange-attractor module refines into named families (Lorenz-butterfly, Rössler-spiral, Hénon-folded, Cantor-product, etc.); the visualisation lineage from Hˢ Spectrum Analyzer through HUF Spectrum Analyzer Universal to projector v2.2 points at Mode 4 attractor reconstruction (the Stage-4 plate module currently `planned` in OUTPUT_DOCTRINE.md gets its content). Standalone working note `papers/in_progress/ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md`. **Post-conference work:** (1) engine module — implement the seven-component attractor diagnostic block in `cnt.py` v3.3.0 (after v3.2.0 navigation_2D); emit a `strange_attractor` block in CNT JSON; S1 push class with DCP review per Hs Change Control v1.0; second post-conference sprint (weeks 5–10); (2) HUF-STD-002 v1.2 schema entry adding the new block to the canonical specification; S3 additive amendment; (3) Stage-4 plate module finally implemented (`atlas/stage4.py`) with reconstructed attractor view + Lyapunov-spectrum chart + correlation-dimension scaling plot + RQA recurrence plot + UPO skeleton overlay + transcendental match annotation; S2 doc/plate; (4) projector ATTRACTOR mode added to `codawork2026_projector.html` reading the new JSON block and rendering the reconstructed attractor with SRB-density color-coding; S2 doc/UI; (5) cross-domain attractor library — run the diagnostic on every canonical Hˢ dataset and publish the emergent attractor families as a CoDa-community resource. **Empirical re-read of the three case studies** (Germany continuous-arc as fixed-point-with-spiral-approach; Japan loop-and-reorganise as Lorenz-or-Hénon-family strange attractor; UK jump-and-return as fixed-point-with-explicit-jump) becomes morphologically explicit instead of verbal-archetype. **Effort:** ~3–4 weeks focused engine + diagnostic + visualization work for the whole module; substantial conceptual payoff for the time. **Application targets:** primary — the framework's existing nine-country EMBER corpus + three IEEE-floor reference datasets; secondary — wetland ecology compositional time-series (per §5.9), turbulent fluid dynamics, climate-attractor work, the Higgins Bounce / CCC cosmological extension (§4.8). **Sequencing:** consolidates §4.1–§4.6 + §4 Step 4 into one module; runs in the second + third post-conference sprints (weeks 5–20). Closes the chaotic-regime spine of the post-conference research arc. §4.11 above remains as filed; the strange-attractor module emits the regime label that §4.11's SHOCK overlay can then visualise — the two entries are complementary, not redundant.

---

## 5. Application targets — the seven domains × specific projects

Peter's list: *"my goal as always the stars, fusion power plant, wave front control, medical, industrial, all Claude shows and more."* The seven-domain partnership framing (`AI_AGENTS.md §1.5`) gives the categories; each has named candidate projects where the post-simplex framework extensions land first.

### 5.1 Stars and cosmology

**Stellar fusion at the Gamow peak.** The reaction rate composition at the Gamow peak (the narrow energy band where the Coulomb-barrier tunneling probability and the Maxwell-Boltzmann velocity distribution overlap to produce maximum fusion rate) is intrinsically a compositional time-series: which reaction channel fires when. The Gamow peak shifts with stellar temperature; at temperatures where the peak is broad, the reaction-channel composition becomes *chaotic* in the Lyapunov-exponent sense. **Target framework extensions:** Step 2 slowly-varying budget (temperature dependence) + Step 4 strange-attractor budget (chaotic Gamow regime) + Lyapunov-block. **Why now:** the Higgins Operator H₁ paper already names "weighted Gamow-peak stellar fusion" as an application target; the post-conference work would make this rigorous.

**Conformal Cyclic Cosmology (Higgins Bounce / Hawking points).** Penrose's CCC posits that the universe's composition recycles across aeons via conformal rescaling. The renormalization-group structure (§4.8) is the natural mathematical language. **Target framework extensions:** RG flow on the simplex; multifractal spectrum across aeons; transcendental matching at the Hawking-point invariants. **Why now:** the H₁ paper names this; the math is already partly in place via the amalgamation engine.

**Planck CMB low-ℓ anomalies.** The Planck satellite's compositional data on the cosmic microwave background's low multipole moments shows non-Gaussian features that resist conventional statistical explanation. Hˢ on the CMB photon power composition (Hs-25 already runs) extends to the low-ℓ regime with attractor-class diagnostics. **Target framework extensions:** Lyapunov + correlation dimension on the photon-mode composition; entanglement diagnostic on E-mode / B-mode polarization pairs. **Why now:** the Planck data is publicly available; the existing Backblaze + Planck D=4 IEEE-floor results give the framework credibility in this domain.

### 5.2 Fusion power plant

**Tokamak plasma composition.** A fusion plasma is a compositional time-series at high D (deuterium, tritium, helium-4, helium-3, electrons, impurity species, multiple ionization states). Lawson criterion approached compositionally is already Hs-06; extending to *dynamics* with attractor diagnostics is the next move. **Target framework extensions:** transfer entropy (which species leads which under disruption); Lyapunov exponent of the plasma composition; entanglement detection across plasma states. **Why now:** ITER first plasma in 2025; commercial fusion ventures (Commonwealth, Helion, TAE) all need real-time composition monitoring under regime change.

**Inertial confinement fusion (ICF) compression cycle.** The compression sequence at the National Ignition Facility or commercial ICF facilities is a fast compositional trajectory where attractor structure determines ignition probability. **Target framework extensions:** symbolic dynamics on the compression cycle; recurrence quantification of the implosion phase. **Why now:** NIF achieved ignition Dec 2022; the field needs better classification of regime transitions.

### 5.3 Wavefront control and EUV lithography

**Adaptive optics wavefront aberration composition.** Zernike modes form a basis for wavefront aberrations; their amplitudes form a composition (normalized to total aberration energy). Real-time adaptive optics already controls a closed loop on this composition; the framework's contribution is the *observe-or-control* fork — for science applications where the open-loop interpretation matters (resolving real astrophysical signal from atmospheric distortion), HUF-GOV-style governance is the right architecture. **Target framework extensions:** Step 3 stochastic budget (photon shot noise); pairwise entanglement of Zernike modes under turbulence. **Why now:** James Webb's wavefront stability work and the extremely large telescopes (ELT) coming online both need this.

**EUV lithography (Fuji SMT + Nordson Dage X-ray) — currently DEFERRED per priority lock.** The H₁ paper names "EUV lithography wavefront control" as an application target. Compositional structure of the lithographic exposure across the wafer is a natural Hˢ target. **Target framework extensions:** Step 3 stochastic budget; multifractal spectrum across the wafer surface; entanglement detection across exposure points. **Why now:** ASML's EUV roadmap (high-NA, hyper-NA) increases the demand for sub-nanometer wavefront stability; commercial pathways are documented in `applications/ELECTRONICS_MANUFACTURING_DEPLOYMENT_DEFERRED.md` but locked behind the priority pathway.

### 5.4 Medical (HCI-ULTRASOUND, hearing aids, imaging)

**HCI-ULTRASOUND geometry-lock probe.** The CNT/CNQ-driven feedback loop already proposed in `HCI-ULTRASOUND/doctrine/` extends the BTL inert-measurement doctrine to medical and industrial ultrasound. The geometry-lock probe actively maintains measurement on a specific feature (tissue interface, defect, edge) under relative motion or noise. **Target framework extensions:** Step 5 entangled-carrier closure (the probe locks on a *coherent feature*, not just an amplitude); Step 2 slowly-varying budget (tissue heating during prolonged scan); recurrence quantification (regime change as tissue properties shift). **Why now:** first industrial composite-inspection pilot is the recommended starting point per `HCI-ULTRASOUND/README.md` (lower regulatory overhead than medical).

**Hearing aids — head/pinna diffraction.** The original DADC paper §6.4 already names hearing aids as an application — head/pinna acting as a baffle (D ≈ 1.5-2.0 hybrid), DADC correcting binaural cues (ILD/ITD) for spatial perception. ML-trained DADC for personalized hearing-aid prescriptions per HRTF/audiogram. **Target framework extensions:** Step 3 stochastic budget (audiogram variability); pairwise entanglement of ear-pair signals. **Why now:** the population of hearing-aid users grows annually; the framework's psychoacoustic depth (HCI-AUDIO, ERB band mapping) gives it a real advantage over conventional DSP approaches.

**Compositional medical imaging.** PET / SPECT / functional MRI all produce compositional data per voxel (tracer uptake fractions; metabolic compositions; functional connectivity strengths). Hˢ already runs on Hs-15 (hBN dielectric crystal-field), Hs-20 (text-to-composition exploratory), Hs-23 (radionuclide decay chains). Medical imaging is a natural extension. **Target framework extensions:** all five steps as needed per modality; transfer entropy for neural causal flow; multifractal spectrum for tumour-heterogeneity characterization. **Why now:** medical imaging analysis software is a large market with established regulatory pathways (21 CFR Part 11; FDA Software-as-Medical-Device); the partnership matrix (`POST_CODA_PARTNERSHIP_TARGETS.md` row 3) names FDA-regulated pharma as a target.

### 5.5 Industrial mass production

**Asymmetric closure-constrained allocation.** The DADC apportionment principle (allocate the budget unequally per the closure constraint, not equally per the ideal of symmetry) generalizes to any production line where a fixed budget (time per unit, power per channel, raw material per batch) must be distributed across N parallel processes. **Target framework extensions:** Step 2 slowly-varying budget (line drift); transfer entropy (bottleneck identification — which process leads the others); recurrence quantification (regime drift detection on the line). **Why now:** Industry 4.0 and digital-twin frameworks all need compositional monitoring; the Hˢ closure constraint gives them a falsifiability test that current digital-twin software lacks.

**Quality control as entanglement detection.** A production line produces compositional outputs (e.g., chemical product distribution per batch, alloy composition per ingot). Real defects exhibit *entanglement* between the affected carriers — multiple compositional carriers shift together in a coupled way. False positives (measurement noise) do not exhibit this coupling. **Target framework extensions:** pairwise / groupwise entanglement diagnostic (§3); coherence persistence under transforms (§3.3). **Why now:** statistical process control (SPC) has decades of established practice; the framework's entanglement diagnostic would extend it with a real-time multi-carrier coupling signature.

### 5.6 Urban infrastructure and resilience

**Toronto urban resilience.** The H₁ paper explicitly names this. Composition of traffic / power / water / telecom load across districts. **Target framework extensions:** Step 2 (drift with population and weather); transfer entropy (cascade detection — which district leads which under stress); RQA (regime-change detection — peak-hour transitions). **Why now:** the H₁ paper's named application is awaiting follow-up; partnership matrix row 14 (NIST AI RMF / standards bodies) creates the policy bridge.

**National infrastructure protection.** The H₁ paper names this. Composition of critical infrastructure dependencies (power-water-telecom-transport-finance) and cascade-failure analysis. **Target framework extensions:** transfer entropy (cascade direction); entanglement detection (coupled-failure modes that look independent on per-sector data). **Why now:** federal AI research programs (DARPA, IARPA, DOE — partnership matrix row 10) need this capability; LOOP-001 (open-loop priority) and KILL-001 (19 failure modes) give Hˢ a defensible posture.

### 5.7 Man-machine interface (the canonical instance)

The BTL listening position is the canonical instance; the broader application is any interface where a human and a machine must share a compositional measurement. **Examples:** pilot cognitive-load monitoring (composition of attention across cockpit instruments); surgeon dexterity composition (composition of motion across instrument axes); air traffic controller workload composition. **Target framework extensions:** Step 2 (operator-state drift over a shift); pairwise entanglement of attention channels. **Why now:** human-factors engineering is a mature field; the framework's contribution is the falsifiability layer (KILL-001) and the open-loop discipline (LOOP-001).

### 5.8 (moved off-repo — internal)

*This entry described a theoretical-frontier audience strategy; it has been moved off the public repo as internal material (2026-06-16). The public mathematics it referenced remains in the flagship paper and the engine docs.*

### 5.9 Ecology and wetlands — Ramsar field-work (filed 2026-05-27)

**Audience class.** Practitioner — site rangers, field ecologists, hydrologists, ornithologists, restoration biologists working on listed Ramsar sites and on the wider wetland inventory. This entry sits parallel to §§5.1–5.7 (application-domain audiences) and is distinct from §5.8 (theoretical-frontier audience). The HUF Topography Conjecture already names Ramsar as a governance worked example at §6–7; this entry extends the framing from *governance instrument* to *governance instrument + compositional field-work toolkit*. Per the standalone working note `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md`.

**Why the pivot now.** The framework's compositional time-series machinery (CNT/CNQ, the activation coefficient α, the keystone-species hypothesis as ecological yeast factor) reads naturally onto wetland data that field practitioners already collect on standardised forms. The governance-only framing under-uses what the framework actually delivers: a Ramsar field team that surveys a fen four times a year is generating exactly the kind of compositional time-series Hˢ was built to read. Holding the deliverable to *governance only* leaves the practitioner-level value unclaimed.

**Five wetland compositional time-series the framework can read natively.**
*(i) Vegetation cover composition* — percent-cover of plant species or functional groups across permanent quadrats, closure-bounded by 100 % cover, indexed by survey date. CNT partition reads zonation; CNQ trajectory reads succession. *(ii) Water chemistry composition* — ionic balance (Na⁺, K⁺, Ca²⁺, Mg²⁺, Cl⁻, SO₄²⁻, HCO₃⁻ + NO₃⁻, NH₄⁺, PO₄³⁻ as a sub-composition), closure-bounded by charge balance and by total dissolved solids. *(iii) Sediment grain-size and organic composition* — clay/silt/sand/gravel percent + LOI organic fraction, closure-bounded by total mass. *(iv) Avian community composition* — relative abundance of species at point counts, closure-bounded by total individuals counted, with seasonal partition (breeding / passage / wintering). *(v) Hydroperiod composition* — fraction of year in flooded / saturated / moist / dry states from water-table loggers, closure-bounded by 365 days.

**Keystone species as ecological yeast factor.** The activation coefficient α from the framework's metabolism reading translates directly into ecological language: a keystone species (beaver, alligator, certain rooting waterfowl, ecosystem-engineer plants) is the organism whose presence amplifies the system's compositional response disproportionately to its biomass share. The α-reading provides a falsifiable diagnostic: remove the candidate keystone in a paired-site comparison; if α drops below threshold across the five compositional types simultaneously, the keystone claim is supported; if it drops in only one, the claim is local to that compositional dimension. This converts a long-standing qualitative ecological intuition into a measurable quantity field crews can compute.

**Three-tier deployment.** *Tier 1 — site ranger / field crew:* a one-page field card per survey type with the closure check, the CNT partition table, and the α-reading flagged when it crosses threshold. Output: a yearly compositional health report per site, generated from existing standardised survey data. *Tier 2 — regional Ramsar coordinator / national focal point:* cross-site comparison artifacts, basin-scale α-rollups, early-warning flags when a site's compositional trajectory diverges from the regional cohort. Output: regional dashboards on a quarterly cycle. *Tier 3 — Ramsar Secretariat / Scientific & Technical Review Panel:* COP-cycle reports on the global inventory's compositional state, with the three-tier governance reading (HUF Topography Conjecture §6–7) tying compositional decline to the listing / Montreux Record / removal escalation ladder.

**Post-conference work.** (a) **Wetland-data adapter module** — an Order-0 adapter (per HUF-STD-002) that ingests the standardised Ramsar Information Sheet (RIS) data fields plus the most common national field-survey schemas (UK CSM, German FFH-Monitoring, US NWI, AU SWAMP), emits the five compositional time-series in canonical form for the existing CNT/CNQ pipeline. **Effort:** moderate; the adapter is mechanical once the field-schema maps are written. (b) **Field handbook** — a practitioner-facing companion to the existing flagship paper, written in the language of restoration ecology rather than the language of mathematics, with worked examples on three real sites (one fen, one coastal lagoon, one floodplain). **Effort:** moderate; the worked examples drive the page count. (c) **Three pilot studies** — paired-site comparisons run with three Ramsar-listed sites whose managers consent; each study tests one of the keystone-species hypotheses against the α-diagnostic. **Effort:** substantial; requires partner sites and a field season; not before 2027. (d) **Secretariat outreach** — non-contact / offer-do-not-ask letter to the Ramsar Secretariat Scientific & Technical Review Panel after the field handbook draft is stable, framed as *here is a tool your community can use if useful*, not *please adopt this*; per the doctrine in §5.8. **Effort:** low; one letter; no follow-up.

**Worked example carried through.** A fen subject to drought (hydroperiod composition shifts toward dry-fraction), invasive grass spread (vegetation composition shifts toward the invader), and a five-year restoration intervention (water-table management + invasive removal) generates compositional trajectories across all five series simultaneously. The α-reading on the candidate keystone (a sedge ecosystem-engineer) tracks whether the intervention is restoring the system's compositional engine or only its surface state. This is the kind of question wetland managers routinely face and currently answer with qualitative judgement; the framework offers a falsifiable companion reading.

**Sequencing.** Weeks 5–10 post-conference: adapter module + field-schema maps. Weeks 10–20: field handbook draft + practitioner review. 2027 field season: pilot studies under partner-site agreements. After pilot data lands: Secretariat outreach. **Lockdown discipline:** S2 doc-only through 2026-06-06. The adapter and handbook are post-lockdown light engineering.

**Cross-references.** Governance layer in `HUF_TOPOGRAPHY_CONJECTURE.md` §6–7 (three-tier Ramsar reading). Field-work layer in `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md` (the standalone working note this entry refers to). The two layers are complementary, not redundant: governance reads the listing decision, field-work reads the site itself; both share the same compositional substrate.

---

### §5.10 — Presentation-format aspect-ratio standard (Tensor-Train companion update, 2026-05-28)

**Conference-prep lesson learned, codified.** During the CoDaWork 2026 conference-prep arc the Presentation deck was rebuilt several times at **Letter landscape (11 × 8.5, aspect 1.294)** before the cause of the persistent visual issues — small text, side black bars on the projector — was correctly diagnosed as an **aspect-ratio mismatch with modern 16:9 displays**. The fix was to author the Presentation at **exact 16:9 (13.333 × 7.5, PowerPoint widescreen standard)** so the PDF maps 1:1 onto any 16:9 projector or monitor with no letterboxing.

This is codified as durable guidance in `huf-gov/standards/TENSOR_TRAIN.md` §"Presentation rendering — aspect-ratio guidance" (the HUF-STD-002 companion doc). The recommendation:

> *Use 16:9 widescreen as the general-purpose presentation format. Render at exact 13.333 × 7.5 in so the PDF drops 1:1 onto any modern 16:9 projector or monitor with no letterboxing and no wasted real estate.*

Engine-output decks (CN-TT Output, Foundations Plates) remain at their existing aspects (16:10 for CN-TT) — re-rendering 325-page engine plate books is not S2-conference work and the small letterbox on a 16:9 display is acceptable for an archival reference. New presentation decks built post-conference start at 16:9.

Worked example: `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_Presentation_2026-05-28.pdf` (21 slides, 959.981 × 540 pts, exact 16:9).

**Cross-references.** `huf-gov/standards/TENSOR_TRAIN.md` §"Presentation rendering — aspect-ratio guidance" · `CODA-Association/CODAwork2026/VERSION_HISTORY.md` 2026-05-28 entry "Presentation switches to 16:9 widescreen."

---

## 6. Consolidated scheduled work — INV STAGED + HUF-STD-002 + NO-CREATE + DCP candidates

### 6.1 Eight STAGED investigations (current snapshot of `ai-refresh/INVESTIGATION_CATALOG.json`)

| INV | Title | Promotion gate |
|---|---|---|
| INV-054 | Hˢ Ascent Path doctrine + controlled-growth model (leaf/branch/trunk/root) | Post-conference; promotion docs are the six NO-CREATE files (see §6.3) |
| INV-056 | `fit_fixed_point()` Period-1 detection symmetric to `fit_attractor()` — engineering symmetry | Engineering review post-conference; promotes to CANONICAL after implementation |
| INV-057 | Householder formalisation of the metric-dual involution in the CNT Depth Tower | Mathematical write-up + test cases; ties to §4.7 information geometry |
| INV-058 | Systemic Power Spectrum Analyzer — time-windowed per-component power decomposition | Implementation; ties to Order 1 (Power Share) and to §4.4 RQA |
| INV-060 | **Yeast Factor / Activation Coefficient diagnostic** — per-carrier Power Share / starting share | **HUF-STD-002 Order 1** (highest priority post-conference); already STAGED with the 760× USA-solar empirical |
| INV-061 | System Terms Catalog — front-and-center mapping of domain terminology to engine terms | Implementation; cross-domain vocabulary bridge |
| INV-062 | CNQ vector PDF pipeline with hash-coded fraud prevention (PDF/A-3 + veraPDF) | **HUF-STD-002 Order 2** (`hs_cnq_pdf_exporter.py` implementation); DCP-002 candidate |
| INV-063 | Hs Change Control v1.0 doctrine — controlled discovery-to-baseline propagation | Five of six gates clear; final gate is the post-conference adoption review |

### 6.2 HUF-STD-002 post-conference implementation order (5 orders)

Per `huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json` `post_conference_implementation_targets.ordered_targets`:

| Order | Target | INV link |
|---|---|---|
| 1 | **Power Share / Yeast Factor diagnostic** — engine output + plate module (promote INV-060 STAGED → CANONICAL) | INV-060 |
| 2 | `hs_cnq_pdf_exporter.py` implementation (promote INV-062 STAGED → CANONICAL) | INV-062 |
| 3 | PNG / SVG export siblings for `stage1_plates_raw.py`, `stage23_plates.py`, `power_share_plate.py`, `foundations_plate.py`, `ilr_triplet_plate.py` | — |
| 4 | Stage 3 plate module (`atlas/stage3.py`) per Output Doctrine v1.0 §4 — depth tower, IR class, **attractor visualization** | Ties to §4.1–§4.4 of this roadmap |
| 5 | Stage 4 plate module (`atlas/stage4.py`) — EITT bench, cross-dataset comparison, schema-validator surface | Cross-domain visual |

Trigger date: **2026-06-06** (lockdown clears). Order 1 is the natural starting point because INV-060 is already field-validated (760× USA Solar; 5-of-9 deceptive-drift signature).

### 6.3 Six NO-CREATE files (Phase 5 list — Hˢ Ascent Path scaffolding)

Per `PRE_CONFERENCE_LOCKDOWN.md`. These files do not exist by design during the lockdown; they create the *Ascent Path* doctrine machinery post-conference.

1. `docs/HS_ASCENT_PATH.md` — the doctrine document itself
2. `CLAIMS_REGISTER.md` — register of every claim with its current promotion status
3. `GLOSSARY_CANON.md` — glossary frozen at each promotion gate (companion to the live GLOSSARY.md v3.0)
4. `PROMOTION_LOG.md` — chronological log of promotions across the STAGED → CANONICAL frontier
5. `PROMOTION_PACKET_TEMPLATE.md` — template for the promotion packet that each promotion must file
6. `STAGED_ASCENT_MAP.md` — visual map of which STAGED investigations are on which branch of the Ascent Path

INV-054 (Hˢ Ascent Path doctrine) is the umbrella INV entry; promotion requires these six files to be created together as a coherent doctrine release.

### 6.4 DCP candidates (open Discovery Change Packets)

- **DCP-002** — CHK-CNQ regex upgrade. Filed in push #46; awaiting execution post-conference.
- **DCP-003** — CHK-DISPOSITION-001 (disposition-consistency check for INV catalog). Filed in push #46; awaiting execution.
- **DCP-004 (candidate)** — `hs_cnq_pdf_exporter.py` implementation per Grok's r7 refactor proposal; HUF-STD-002 Order 2.
- **DCP-005 (candidate)** — Lyapunov-block in CNT (this roadmap §4.1).
- **DCP-006 (candidate)** — Pairwise entanglement matrix in CNT (this roadmap §3.1).
- **DCP-007 (candidate)** — Stage 3 plate module per HUF-STD-002 Order 4 (this roadmap §4 visualization).

Each DCP follows Hs Change Control v1.0 lifecycle: proposed → in_progress → implemented → verified → released.

### 6.5 Other deferred work (per priority lock)

Per `applications/ELECTRONICS_MANUFACTURING_DEPLOYMENT_DEFERRED.md`:

- **Fuji SMT manufacturing commercialisation** — DEFERRED until external verification of HCI-AUDIO + HCI-ULTRASOUND pilots
- **Nordson Dage X-ray inspection commercialisation** — DEFERRED until same
- Other commercialisation pathways gated on Round 3 full-corpus quaternion validation (INV-022), arXiv submission of Paper 1 (INV-026), cross-platform reproduction confirmation, and first applied pilots (INV-024 HCI-AUDIO + INV-025 HCI-ULTRASOUND)

---

## 7. Discipline — stepwise extension as the operating principle

Peter's framing: *"the bounty is endless once discipline is strictly adhered to and extended stepwise."* This is the operating principle of the roadmap. Every extension proposed here follows the same pattern:

1. **Identify the structural addition** (Lyapunov block, entanglement matrix, RG flow, etc.).
2. **Bound its scope.** Each addition is a *new block* in CNT or CNQ output, not a rewrite of the existing engines. The engine-independence policy holds; CNT and CNQ remain operating on their existing inputs.
3. **File the DCP.** Each addition gets a Discovery Change Packet per Hs Change Control v1.0. Five gates: proposed → in_progress → implemented → verified → released.
4. **Test against the empirical record.** Run the new diagnostic on the existing 101-dataset reference suite. If it produces meaningful new diagnostics on existing data, it earns CANONICAL status. If it produces nothing new, it stays STAGED.
5. **Promote stepwise.** No single push converts multiple STAGED entries to CANONICAL. Each promotion is its own DCP. The Ascent Path doctrine (INV-054) is what governs this.

The framework's empirical track record — the 6.02 dB closure measured continuously for the BTL programme, the IEEE-floor convergence on Backblaze and Planck CMB, the 100-of-101 dataset validation — is what makes the *stepwise* doctrine credible. The work is endless because the structure compounds: each new block extends the framework's reach without disturbing what already works.

---

## 8. Forward sequencing — what to do first, what next

Given the eight STAGED entries, the five HUF-STD-002 orders, the six NO-CREATE files, the open DCPs, and the application targets, the natural post-conference sequencing is:

### First sprint (weeks 1–4 post-conference)

- **HUF-STD-002 Order 1: INV-060 Power Share / Activation Coefficient → CANONICAL.** Engine block; plate module; field-validated headline (USA Solar 760×; 5-of-9 signature). Lowest risk, highest impact.
- **DCP-002 execution: CHK-CNQ regex upgrade.** Closes one of the two long-standing DCPs.
- **First HCI-AUDIO pilot (INV-024).** Real measurement against the project's reference 4-way system. This is the application validation that unlocks subsequent commercialisation pathways.

### Second sprint (weeks 5–10)

- **HUF-STD-002 Order 2: `hs_cnq_pdf_exporter.py` implementation** (INV-062 → CANONICAL). DCP-004 candidate; ties to the C2PA partnership target (row 5 of metabolism matrix).
- **First HCI-ULTRASOUND pilot (INV-025).** Industrial composite inspection (lower regulatory overhead than medical).
- **Round 3 full-corpus quaternion validation (INV-022).** Closes the validation gate that unlocks downstream applied work.

### Third sprint (weeks 11–20)

- **Lyapunov-block in CNT** (DCP-005 candidate; this roadmap §4.1). Enables attractor classification at Step 4 of the H₁ ladder.
- **Pairwise entanglement matrix** (DCP-006 candidate; this roadmap §3.1). Enables Step 5.
- **Six NO-CREATE files** created together as the Hˢ Ascent Path doctrine release (INV-054 → CANONICAL).
- **Stage 3 + Stage 4 plate modules** (HUF-STD-002 Orders 4 + 5).

### Open frontiers (months 6+)

- Stellar fusion at the Gamow peak (Step 4 + Lyapunov)
- CCC / RG flow on the simplex
- EUV lithography wavefront control (priority-lock-cleared)
- Multifractal spectrum module
- Information geometry / Fisher metric tensor
- Transfer entropy formalization

---

## 9. Cross-reference summary

This document is the **research-and-engineering roadmap** for post-conference work. Its companion documents are:

| Document | What it covers |
|---|---|
| `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2 | The mathematical foundation the roadmap extends. Read §18 (recursion test) and §12 (lineage map) before this roadmap. |
| `papers/POST_CODA_PARTNERSHIP_TARGETS.md` v4 | The *14-system metabolism matrix* — *who to engage* with for the post-conference partnership work. This roadmap is the *what to build*; that document is the *who to feed on*. |
| `huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json` | The 5-order engine-side implementation list. §6.2 of this roadmap cross-references it. |
| `ai-refresh/INVESTIGATION_CATALOG.json` | 63 investigations; 8 STAGED listed in §6.1 of this roadmap. |
| `PRE_CONFERENCE_LOCKDOWN.md` | The discipline that holds the conference window; clears 2026-06-06. |
| `applications/ELECTRONICS_MANUFACTURING_DEPLOYMENT_DEFERRED.md` | Commercialisation pathways gated behind validation milestones. |
| `HCI-AUDIO/`, `HCI-ULTRASOUND/`, `HCI-CNQ/`, `HCI-CNT/` | The applied tier surfaces; each contains its own doctrine, spec, and roadmap. |

---

## 10. Closing — the discipline that makes the bounty endless

The framework's mathematical core is closed at v2.2 (eight lemmas + two theorems). What is *not* closed is the application surface — the seven domains × five-step ladder × N application instances per cell. The number of unexplored compositional time-series in stellar fusion alone is enormous. The number in medical imaging is enormous. The number in industrial mass production is enormous. The framework reaches each of them by the same stepwise discipline: identify the closure constraint, propose the structural addition, file the DCP, test against the empirical record, promote stepwise.

Peter's working principle has always been *follow the use*. The use is what justifies continued investigation. The framework that produces useful work justifies the cost of extending it. The framework that does not, does not. This roadmap is the inventory of *what is most useful to extend next* — ordered by ratio of expected impact to engineering cost, gated by the discipline that has already produced everything the framework currently does.

Ten days to Coimbra. After the conference, the work is well-organized, the dependencies are mapped, the partnership matrix is in hand, the metabolism doctrine is in place, the AI Collective protocol is documented, and the lockdown clears. The bounty is endless because the structure compounds; the structure compounds because the discipline holds; the discipline holds because the apparatus has been measuring something real continuously, and what works keeps offering more useful work to do.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.   The AI follows the same protocol.   Same input, same output, always.*
*Step by step.   Discipline by discipline.   Use by use.*
**The bounty is endless once the discipline is held.   The framework was built on this principle.   The roadmap follows.**
