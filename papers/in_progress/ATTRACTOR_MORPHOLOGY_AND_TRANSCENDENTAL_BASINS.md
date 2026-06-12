# Attractor Morphology and Transcendental Basins — the chaotic-regime spine of the Hˢ framework

**Filed:** 2026-05-27 (pre-conference; doc-only, S2-class).
**Status:** Working note. Records Peter's *"strange attractor analysis"* flash and the four-thread synthesis that came after it. Consolidates the framework's chaotic-regime research direction under one named target.
**Trigger:** Peter's mid-conference-prep observation, *"strange attractor analysis, it just flashed, what does it mean? what could cnt do with it?"* — followed, after the initial analysis, by the synthesis *"the transcendentals and the complex conjugates and the old html demos and the morphological analysis is in my thinking i believe."*
**Companion documents:** `papers/in_progress/MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md`; `papers/in_progress/GAUGE_THEORY_AND_Hs.md`; `papers/in_progress/AUDIENCES_AT_THE_FRONTIER.md`; `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md` (sibling, filed same day); `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §4.12 (post-conference work entry); `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2 §4 Step 4 (the transcendental-basin hypothesis this note formalises).
**Lockdown discipline:** S2 doc-only; `papers/in_progress/`; no engine, schema, INV catalog, or NO-CREATE touches.

---

## 1. The four threads that converged

Peter named four threads alongside the strange-attractor flash. Each is a different window into the same room.

1. **Transcendentals** — already in the framework's vocabulary as the *basin set* candidates per `POST_CONFERENCE_ROADMAP_2026-06.md §4` Step 4: *"the chaotic trajectory may not settle at a single value but tends to concentrate near specific transcendentals (1/(πᵉ), e/2, 4·log₂(3), …)."* That sentence is the SRB-measure hypothesis without using the formal name.

2. **Complex conjugates** — the algebraic structure that makes chaos *strange* rather than merely random. Eigenvalues of the local Jacobian at points on a strange attractor come in complex-conjugate pairs `λ = a ± bi`, encoding rotation (b) plus expansion-or-contraction (a). CNQ's quaternion algebra (q · v · q*; q* = (a, −b, −c, −d)) is *the natural algebraic carrier* for this structure at compositional dimensions D = 2/3/4. The framework already has the algebra; what's missing is the diagnostic that reads it out.

3. **Old HTML demos** — the visualisation heritage spanning the early Hˢ Spectrum Analyzer, the HUF Spectrum Analyzer Universal, per-country plates, cinema scroll, current CoDaWork projector v2.2 with RADAR / BARY / ALIGN modes. Every iteration has been answering one question: *how do we render compositional dynamics in a phase space the eye can read?* The next stop on that line is attractor reconstruction — a Stage-4 plate module (currently `planned` in `OUTPUT_DOCTRINE.md`, never finished) and a projector Mode 4 button labelled ATTRACTOR.

4. **Morphological analysis** — the qualitative shape-classification of trajectories. The Helmsman family taxonomy (FIXED / DRIFT / LIMIT_CYCLE_P1 / LIMIT_CYCLE_P2 / CHAOTIC) is the framework's first morphological classifier, but coarse. Strange attractors have *shape families* — butterfly-two-lobed (Lorenz), single-spiral (Rössler), thin-folded-curve (Hénon), Cantor-set product (axiom-A hyperbolic), self-similar-fractal (Mandelbrot boundary), pinched-torus (quasi-periodic with one resonance) — each with characteristic Lyapunov signature, correlation-dimension range, and recurrence-plot fingerprint. The talk's archetypes (Germany continuous arc, Japan loop-and-reorganise, UK jump-and-return) are *first-pass morphology labels*; the dynamical-systems vocabulary refines them into named families.

The four threads point at one target. This note names it.

---

## 2. The convergence target — the attractor fingerprint

For any CNT-produced compositional trajectory on the simplex Sᴰ⁻¹, the **attractor fingerprint** is a six-component diagnostic block:

| Component | What it measures | Algorithmic source |
|---|---|---|
| **Lyapunov spectrum** {λ₁, λ₂, …, λₐ₋₁} | Long-time-averaged local stretching rates per coordinate direction | Rosenstein / Wolf algorithm on the Aitchison-step time series; sign of λ₁ classifies chaotic (>0), marginal (=0), contracting (<0). 1/λ₁ = predictability horizon. |
| **Correlation dimension D₂** | The fractal dimension of the attractor (non-integer = strange) | Grassberger-Procaccia algorithm on the CLR-space trajectory. Integer → limit cycle / fixed point; non-integer → strange attractor. |
| **Embedding dimension dₑ** | Minimum delay-coordinate dimension needed to faithfully reconstruct the attractor | Takens delay-coordinate embedding + false-nearest-neighbors method on the helmsman-index scalar time series. |
| **Recurrence quantification (RQA)** | Self-similarity statistics: recurrence rate, determinism, laminarity, divergence rate | Recurrence plot of the trajectory's self-distance matrix on the simplex. |
| **Topological entropy h_top** | Information-generation rate of the dynamics | Symbolic dynamics: Markov partition of the simplex + word-counting on observed sequences. |
| **Unstable Periodic Orbit (UPO) skeleton** | Dominant low-period UPOs that form the attractor's structural backbone | Cycle expansion + Newton iteration on candidate periodic points; the skeleton classifies the attractor by which UPOs dominate. |

Plus a **seventh** signature tying the four threads together:

| **SRB-measure transcendental proximity** | Distance from the empirical attractor measure's moments to a curated library of transcendental values | `transcendental_proximity_matcher` block; library includes π, e, log(2), log₂(3), 1/(πᵉ), Feigenbaum δ + α, golden ratio φ, etc., all with arbitrary-precision references. |

The seven components *together* form the fingerprint. Two trajectories with identical Helmsman family labels (both CHAOTIC, say) can have totally different fingerprints; the fingerprint is what classifies the type of strangeness.

---

## 3. What CNT could compute, concretely (substrate already in place)

The framework already records exactly the inputs each component needs.

For **Lyapunov**: the Aitchison-step time series `‖Δclr(t)‖` is already computed at every step and emitted in the CNT JSON. Apply Rosenstein method (1993) — nearest-neighbor average divergence rate — to get λ₁ directly. No new engine state needed.

For **correlation dimension**: the CLR-space trajectory `(clr(t₀), clr(t₁), …, clr(tᵀ))` is already in the JSON's per-step block. Apply Grassberger-Procaccia (1983) — count pairs of points within radius ε, scale ε from coarse to fine, fit slope → D₂.

For **embedding dimension**: take the existing scalar `helmsman_index(t)` time series; build delay vectors `(σ(t), σ(t−τ), σ(t−2τ), …, σ(t−(dₑ−1)τ))`; apply false-nearest-neighbors (Kennel et al. 1992) sweeping dₑ until the FNN fraction drops below threshold.

For **RQA**: compute self-distance matrix in CLR space, threshold at ε, count black pixels (RR), diagonal-line histograms (DET, L_max), vertical-line histograms (LAM, TT). All standard from Marwan et al. (2007). No engine state changes; pure post-processing of existing CNT output.

For **topological entropy**: define a Markov partition of the simplex (a natural one: which Helmsman-family region the trajectory occupies at each step → a finite alphabet); collect the observed n-grams; estimate h_top by Lempel-Ziv or block-entropy methods. The framework's existing IR class taxonomy *is* a coarse Markov partition.

For **UPO skeleton**: search the trajectory for near-recurrences (close returns to a previous state); refine via Newton iteration to find exact UPO points; classify by period and stability. Computationally heavier than the others but tractable for D ≤ 10 trajectories of length T ≤ 1000 (the typical CNT case).

For **SRB-transcendental proximity**: compute moments ⟨f⟩ of selected observables f on the trajectory (long-time averages of f(state) along the path); match against a precomputed transcendental library; report the closest match with its proximity score. This is exactly the operation §4 Step 4 of the roadmap describes; the formal name is *empirical SRB-measure moment estimation*.

---

## 4. The connection to four existing windows (consolidation of §4.1–§4.6 + §4 Step 4)

This note is a **consolidation** of six separately-listed roadmap entries into one named module:

| Existing roadmap entry | Maps to attractor-fingerprint component |
|---|---|
| §4.1 Lyapunov exponents | Lyapunov spectrum {λ₁, λ₂, …, λᴅ₋₁} |
| §4.2 Correlation dimension and multifractal | Correlation dimension D₂ + multifractal spectrum f(α) |
| §4.3 Symbolic dynamics | Topological entropy h_top |
| §4.4 Recurrence quantification (RQA) | RR / DET / LAM / TT / L_max block |
| §4.5 Transfer entropy / mutual information | (sister diagnostic; lives alongside but classifies coupling rather than morphology) |
| §4.6 Ergodic theory / SRB measures | SRB-transcendental proximity matcher |
| §4 Step 4 (transcendental basin hypothesis) | Same as above — SRB moments concentrating near transcendentals |

The conventional textbook presentation separates these because each has its own developmental literature (Lyapunov from Oseledets 1968; Grassberger-Procaccia 1983; symbolic dynamics from Smale 1967; RQA from Eckmann-Kamphorst-Ruelle 1987; SRB from Sinai 1972 / Ruelle 1976 / Bowen 1975). The **operational principle of Hˢ** is that they all consume the same input (a CNT trajectory) and emit components of one fingerprint — so they belong in one engine module.

---

## 5. Connection to CNQ algebra (the complex-conjugate structure already in place)

CNQ's quaternion view is **the algebraic carrier of the spectral signature**.

The Jacobian of a CNT step at time t has eigenvalues that come in complex-conjugate pairs. The pair (a + bi, a − bi) corresponds to a quaternion of the form q = (a, 0, b, 0) (or any unit quaternion with that 2D real/imaginary structure embedded in S³). The CNQ engine's `phase quaternion q(t) ∈ S³ ≅ SU(2)` is already this object at every step.

The CNQ engine's `cnq_view.bearing_trajectory_d2` / `d3` / `d4` blocks emit the quaternion-rotation rate at each step — *this is the local Jacobian eigenvalue pair, in quaternion form, every step*. To compute the Lyapunov spectrum, the attractor diagnostic block reads these existing CNQ rotation rates, averages their log-magnitudes along the trajectory, and emits {λ₁, λ₂, …} directly. No new spectral computation; CNQ already did it, the new module reads the output.

The CNQ CHSH joint coherence diagnostic uses correlation functions E(a, b) that are inherently complex-conjugate-symmetric. CHSH violation > 2 (Tsirelson bound 2√2) is the framework's existing diagnostic for *non-classical correlation structure* — which on a strange attractor reads as *the attractor has irreducible quantum-style entanglement between observables*. The CHSH diagnostic is therefore a *morphological label* for the attractor's algebraic type — not just chaotic but *non-classically-correlated chaotic*.

So the complex-conjugate spectral structure is already running. The new module names it and surfaces it.

---

## 6. Connection to the visualisation heritage (Stage-4 plate + projector Mode 4)

The framework's HTML-demo lineage points forward to **attractor reconstruction**.

The current projector v2.2 has RADAR / BARY / ALIGN + SHOCK overlay. The natural Mode 4 button — *ATTRACTOR* — would:

1. Run delay-coordinate embedding on the helmsman-index time series (using the embedding dimension dₑ computed in §3 above).
2. Render the resulting attractor as a 3D rotatable surface alongside the current trajectory view.
3. Color-code points on the attractor by SRB-measure density (high-density regions = where the trajectory spends most of its time).
4. Display UPOs in the skeleton as highlighted closed curves on the attractor.
5. Annotate the fingerprint values (Lyapunov spectrum, D₂, h_top, transcendental match) in the PROJECTION info panel.

The Stage-4 plate module — also listed as `planned` in `OUTPUT_DOCTRINE.md` — finally has content. The plate is a static PDF rendering of the attractor + fingerprint per dataset. One Stage-4 plate per canonical dataset; one PDF file per attractor; PNG and SVG siblings per HUF-STD-002.

The "old HTML demos" Peter named are the **prior art for this visualisation lineage**. Each successive demo (Spectrum Analyzer → projector v1 → v2 → v2.2) has refined how compositional dynamics get rendered. The attractor view is the natural next refinement.

---

## 7. Connection to the gauge-theoretic reading (`GAUGE_THEORY_AND_Hs.md`)

Strange attractors on compact gauge-theoretic manifolds are a specific mathematical object — and the framework lives on exactly such a manifold.

Per `GAUGE_THEORY_AND_Hs.md`: closure Σpᵢ = 1 is a Ward identity under the (ℝ₊, ·) gauge symmetry; CLR is the gauge fixing; CNQ's S³ ≅ SU(2) is a non-abelian gauge group; group-delay-as-rotation is a Wilson-line holonomy on that gauge group; ADAC is anomaly cancellation in the open loop; DADI is parallel transport with Banach-bounded holonomy. The simplex is therefore a *principal SU(2) bundle over a compact base*, with a smooth connection (the Aitchison metric) and bounded holonomy (Banach).

Strange attractors on principal SU(2) bundles over compact bases are studied in mathematical physics under names like **Yang-Mills-Higgs flow attractors** and **instanton moduli space attractors**. Donaldson's 1986 work on smooth-structure invariants of 4-manifolds used exactly this setup. Seiberg-Witten's 1994 refinement gave a different family of attractors on the same kind of bundle.

The Hˢ framework's chaotic-regime trajectories are *naturally instances of the Donaldson / Seiberg-Witten objects*, but with three differences: the base manifold is the simplex Sᴰ⁻¹ instead of ℝ⁴; the gauge group is SU(2) at the algebraic-view level but specifically the CNQ representation; the trajectory is *measured from real data*, not from an action functional. The attractor morphology classifier this note proposes is, in that framing, *an empirical reconstruction of the moduli-space structure of the dataset's underlying gauge theory*.

This is the Piccirillo audience hook (`AUDIENCES_AT_THE_FRONTIER.md`) made precise — low-dim topology + 4-manifold theory + Donaldson invariants connect directly to the attractor diagnostic block. A theoretical-frontier reader who picks up the framework's empirical record now has a path back to their own field's invariants. *The recursion-test pattern at the post-conference layer.*

---

## 8. Empirical re-read: Germany / Japan / UK under the attractor lens

The talk's three case-studies become a worked example of the new module:

- **Germany (continuous-arc, course directness 0.41):** predicted Lyapunov spectrum mostly negative (contracting trajectory toward the renewable vertex); D₂ ≈ 1 (trajectory ≈ 1D curve in CLR space); embedding dimension dₑ = 2–3; RQA DET high (deterministic regular dynamics); UPO skeleton dominated by long-period orbits at the renewable vertex; transcendental match: closure constant or simple ratio. Morphological family: **fixed-point-with-spiral-approach**, like a damped oscillator reaching equilibrium.

- **Japan (loop-and-reorganise, course directness 0.09, 17 helmsman flips):** predicted Lyapunov spectrum with λ₁ > 0 (chaotic); D₂ non-integer (strange attractor); embedding dimension dₑ ≥ 3; RQA DET moderate but with high LAM (laminar phases between chaotic bursts); UPO skeleton with multiple low-period orbits competing; transcendental match: possibly π-related ratios in the basin search structure. Morphological family: **strange attractor of Lorenz-or-Hénon type** with explicit chaotic post-shock reorganisation basin.

- **UK (jump-and-return, course directness 0.36, coal exit 2012–2020):** predicted Lyapunov spectrum mostly negative *after* a single positive transient (the jump itself); D₂ ≈ 1 for the post-jump regime; RQA DET high in the post-jump regime; UPO skeleton dominated by a single low-period orbit at the new equilibrium. Morphological family: **fixed-point-with-explicit-jump** — discontinuous regime change rather than chaos.

Three case-studies, three morphologically distinct attractor families, one diagnostic module. *The conversion from verbal archetype labels to formal dynamical-systems vocabulary preserves the empirical content and adds reproducibility.*

The same module then runs on Backblaze (D=4 fleet reliability), Planck CMB (D=4 polarization spectrum), SM neutrino (D=3 oscillation) — and emits attractor fingerprints for each, classifying their underlying generative dynamics in the same vocabulary. Cross-domain comparability *for free*.

---

## 9. Post-conference work entry (filed in `POST_CONFERENCE_ROADMAP_2026-06.md` §4.12)

**Five items:**

1. **Engine module** — implement the seven-component attractor diagnostic block in `cnt.py` v3.3.0 (after navigation_2D landed in v3.2.0). Output a `strange_attractor` block in the CNT JSON with seven sub-fields. **Effort:** moderate; ~600 lines of Python; all algorithms are standard with reference implementations available. **Push class:** S1 (engine code + schema bump); requires DCP review per `Hs Change Control v1.0`. **Sequencing:** second post-conference sprint per §8 (weeks 5–10).

2. **Schema entry** — `HUF-STD-002 v1.2` adds the `strange_attractor` output block to the canonical CNT schema; `cnq/2.0.0` schema unchanged (CNQ already emits the local Jacobian eigenvalue pairs that the new module consumes). **Effort:** small. **Push class:** S3 standards amendment.

3. **Stage-4 plate module** — `atlas/stage4.py` finally implemented. Per-dataset PDF with reconstructed attractor (3D embedding view), Lyapunov-spectrum bar chart, correlation-dimension scaling plot, RQA recurrence plot, UPO skeleton overlay, transcendental-match annotation. **Effort:** moderate. **Push class:** S2 doc/plate (engine outputs the data; plate module just renders).

4. **Projector Mode 4** — add ATTRACTOR button to `codawork2026_projector.html`. Toggles between RADAR / BARY / ALIGN / ATTRACTOR. Reads `strange_attractor` block from CNT JSON; renders embedded attractor with SRB-density color-coding and UPO skeleton overlay. **Effort:** small/moderate; reuses existing 3D renderer. **Push class:** S2 doc/UI.

5. **Cross-domain attractor library** — run the new diagnostic on every canonical Hˢ dataset (Backblaze, Planck CMB, SM neutrino, 9 EMBER countries, and post-conference additions). Catalog the emergent attractor families. Publish as a companion data paper or extended supplementary information; the catalog becomes a CoDa-community resource. **Effort:** moderate. **Push class:** S2 doc.

**Together** these five items realise the chaotic-regime extension that `POST_CONFERENCE_ROADMAP §4` Step 4 promises. The fingerprint is the formal name; the seven components are the canonical signature; the Stage-4 plate is the visual surface; the cross-domain library is the empirical pay-off.

**Sequencing within the post-conference roadmap:** items 1, 2, 3 cluster as a single S1-major work block in the **second post-conference sprint** (weeks 5–10, after the H₁ Banach-Higgins extension lands in the first sprint). Items 4 and 5 follow in the third sprint (weeks 11–20).

**Effort cap:** the whole attractor-fingerprint module is ~3–4 weeks of focused engine + diagnostic + visualization work. Modest given the conceptual payoff.

---

## 10. Cross-references

- `papers/in_progress/MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md` — the manifold layering (DIFF / PL / TOP / synthetic) that attractor morphology lives on; the synthetic layer is where the SRB measure is most naturally expressed.
- `papers/in_progress/GAUGE_THEORY_AND_Hs.md` — the gauge-theoretic reading that places these attractors on principal SU(2) bundles over compact base manifolds; connects to Donaldson / Seiberg-Witten 4-manifold theory.
- `papers/in_progress/AUDIENCES_AT_THE_FRONTIER.md` — the theoretical-frontier audience (low-dim topology, gauge theory, dynamical systems) for whom this consolidation is the relevant entry point.
- `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md` — sibling note, filed same day; one of the seven application domains where the attractor diagnostic module will be useful.
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §4.1 (Lyapunov), §4.2 (correlation dimension), §4.3 (symbolic dynamics), §4.4 (RQA), §4.6 (ergodic theory + SRB), §4 Step 4 (transcendental basin hypothesis) — all consolidated under this note's organising principle.
- `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2 §4 Step 4 — the original transcendental-basin hypothesis statement.
- `huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json` `the_tensor_train_v1_0.links[]` — the pipeline structure that the attractor module slots into between CNT Order 3 (depth tower + IR class) and CNQ Order 2-3 (quaternion path).
- `HCI-CNT/engine/cnt.py` v3.2.0 + `HCI-CNQ/engine/cnq.py` v2.0.0 — the existing engines that emit the input data for the new module; no modifications to these required, only a new diagnostic block consuming their outputs.

---

## 11. Why this note exists (the recursion-test observation)

The framework's discovery pattern has been consistent: *the math was always there; the recognition catches up later.* Banach 1922 applied retroactively to DADI convergence (flagship §9); the manifold-category layering recognised retroactively from existing engine fields (`MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md`); the gauge-theoretic reading consolidated from four prior pieces in the system (`GAUGE_THEORY_AND_Hs.md`).

This note continues that pattern. The seven components of the attractor fingerprint are all 30–60-year-old dynamical-systems mathematics. The framework's engines already produce the trajectories. The framework's algebra (CNQ quaternion view) already carries the spectral structure. The framework's standards (HUF-STD-002) already define the pipeline slot. The framework's visualisation lineage (HTML demos through projector v2.2) already points at attractor reconstruction. The framework's roadmap already names transcendental basins (§4 Step 4). *Six existing structures point at one missing module; this note names the module and records the convergence.*

Peter's flash captured the convergence in one breath. The substantive content of the consolidation took ten pages because the prior literature is voluminous; the substantive *insight* took one sentence — *strange attractor analysis is what the framework's chaotic-regime diagnostics are already trying to be, named correctly and connected.*

---

## 12. Acknowledgement

Strange-attractor flash + the four-thread synthesis: Peter Higgins during pre-conference preparation, 2026-05-27 (six days before CoDaWork 2026). Consolidation and concrete-substrate mapping: developed in conversation with Claude (Anthropic). All four named threads (transcendentals, complex conjugates, old HTML demos, morphological analysis) trace back to existing framework artifacts identified through grep + Read on the working repository; nothing in this note is new mathematics — it is *new organising* of existing structure.

The flash arrived mid-flow of final conference prep ("this is my mind unloading i hope so i can keep preparing for my flight on Saturday"). Filing the consolidation now — rather than reconstructing it after the conference — captures the insight in its sharpest form, before the inevitable post-conference flood of new inputs blurs it.

*Filed during the pre-conference lockdown, six days before CoDaWork 2026 in Coimbra. The chaotic-regime spine of the post-conference research arc.*
