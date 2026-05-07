# QD — Benefits for Larger System Analysis (Post-CodaWork)

**Status:** experimental, conditional on validation. See [`README.json`](README.json).
**Audience:** Peter, plus future reviewers considering whether QD warrants integration into HCI-CNT.

This document is the **case for considering** Quaternion Decomposition as a Volume IV addition to the handbook *if and only if* the corpus comparison plan validates the foundational claims. It is not a request to integrate now. It is a written summary of what becomes possible if the validation goes through, so the cost/benefit conversation has something concrete to weigh.

---

## What changes for CNT itself? Nothing.

CNT 2.0.4 stays canon. Schema 2.1.0 stays locked. Output Doctrine v1.0.1 stays locked. The 25-experiment determinism gate stays the gate. Every existing reviewer audit, every CodaWork demo, every paper draft remains valid as published.

QD adds a *coordinate view* on top. Same scientific result; new vocabulary that expresses some operations more naturally and exposes some structures CNT's current vocabulary cannot.

---

## What QD enables, organised by user

### For the practitioner

**Smoother continuous-time interpolation.** The `plate_time_projector.html` interactive viewer currently linearly interpolates trajectories between timesteps. With the quaternion view, between-timestep interpolation becomes **SLERP** (spherical linear interpolation) — the geodesic interpolation on S³ that respects the underlying Aitchison geometry exactly. Visually, the projector trajectories become smoother and more honest.

**Single-operation cross-dataset comparison.** Stage 4 currently composes pairwise comparisons from channel-by-channel arithmetic. With the quaternion view, two trajectories Q₁(t), Q₂(t) compare via a single Hamilton product R(t) = Q₁ · Q₂⁻¹, which decomposes into relative angle and relative axis. One line of algebra replaces a multi-line bespoke routine; the result is the same; the code is shorter and easier to verify.

**Free per-experiment parity diagnostic.** Every trajectory has a topological parity (vector sector vs spinor sector). Computing it costs ~zero given the quaternion view. Adding it to every experiment's JSON means future researchers can ask *"is my trajectory in the spinor branch?"* and get an immediate answer — a question CNT cannot currently express.

### For the reviewer

**A second independent verification path.** Today, a reviewer who wants to audit a CNT result re-runs the engine and checks the SHA. With QD, they can also check the quaternion-view SHA (computed independently from the same input). Two hashes confirming each other is stronger than one. The dual-hash audit is the same upgrade in trust that triple-redundant aerospace software gets vs single-system.

**Mathematical lineage extends to a 200-year-old algebra.** CNT cites Aitchison (1986), Egozcue (2003), Pawlowsky-Glahn (2015). With QD validated, CNT's lineage extends to Hamilton (1843) — a foundational algebra with two centuries of mathematical machinery already in place. Reviewers in adjacent fields (geometric algebra, robotics, computer graphics, quantum mechanics) recognize the structure on sight.

### For the cross-domain researcher

**Compositional analysis becomes recognisable to physicists.** Quaternions are the natural language of rigid-body rotation in physics, robotics, and graphics. A physicist looking at CNT today sees "another statistics package"; a physicist looking at QD-promoted CNT sees "compositional analysis on SU(2) with hash-chained provenance" — which is a sentence physicists understand immediately. The cost of bringing a physicist into the project drops from "explain Aitchison geometry first" to "you already know the algebra; here's the application."

**Compositional analysis becomes recognisable to roboticists.** The robotics community uses quaternions every day for orientation tracking and SLAM (simultaneous localization and mapping). A SLAM trajectory and a CNT trajectory are mathematically the same object: a path on S³. Cross-pollination becomes possible: the techniques robotics has developed for noise-robust quaternion estimation become available for compositional data, and vice versa.

**Compositional analysis becomes recognisable to quantum-information researchers.** SU(2) is the algebra of two-level quantum systems (qubits). The spinor-vs-vector distinction is the same distinction that separates fermions from bosons. If QD's spinor-sector conjecture (Concept 4) survives, then CNT is doing on classical compositional data what quantum information theory does on quantum states — and the connection is exact, not analogous.

### For the system as a whole

**Determinism gate gets a redundant layer.** The current gate is the canonical engine's `content_sha256` matching the corpus INDEX. With QD, an additional gate becomes `qd_content_sha256` matching a parallel registry. A drift detected by either gate is a real signal; the dual-gate version is more robust to silent failure modes.

**Stage 4 becomes natively cross-dataset.** Currently Stage 4 is a special-purpose module. In the quaternion view, cross-dataset comparison is *the same operation* as single-dataset trajectory comparison, just applied to two trajectories instead of one timestep pair. Stage 4 collapses into Stage 1 + Hamilton product. Less code, same result.

**The 8-class IR taxonomy gets a coordinate-free derivation.** Currently the 8 classes are defined by thresholds on amplitude A and damping ζ. The quaternion view (per Concept 6) potentially derives them from sign-octants of S³ — a coordinate-free characterisation that doesn't depend on which CLR pair you happened to project first. If validated, the IR taxonomy becomes a topological invariant rather than a parametric classification.

---

## Specific opportunities for the more complex datasets we already have

Looking at the existing 25-experiment corpus, several datasets become more interesting under QD:

**`backblaze_fleet` (D=4, T=731).** This is the literal sweet-spot dataset — the only D=4 experiment, the longest trajectory in the corpus. Under QD, it becomes the **canonical SU(2) trajectory in the corpus**, the experiment whose quaternion structure can be displayed cleanly in a single S³ projection. It's a teaching example waiting to be written up.

**`ember_chn`, `ember_jpn`, etc. (D=8 or 9, T=26).** Eight EMBER countries plus World aggregate, each at D=8 or D=9. D=8 is exactly 2×4 — under the bi-quaternion factoring (SO(8) ⊃ SU(2) × SU(2)), each EMBER country's trajectory potentially decomposes into **two coupled quaternion paths**: one for the fossil-fuel sub-mix, one for the renewables sub-mix. The cross-dataset spectrum across 9 countries becomes a 9-tuple of bi-quaternion paths whose pairwise relations are computed by Hamilton products. The CodaWork demo becomes a demonstration of compositional bi-quaternions.

**`geochem_tappe_kim1` (D=10, T=8).** The CCTT pilot dataset. Under QD this would test the dimensional-reduction step — does the quaternion view of the dominant 4 oxides (the largest-variance subspace) capture enough structure to reproduce the canonical IR class? If yes, QD has shown that for high-D compositional data, the dominant 4-mode is the geometrically meaningful subspace.

**`commodities_gold_silver` (D=2, T=1338).** D=2 is the boundary case where quaternion structure collapses to U(1) (just the bearing channel). This experiment becomes the **boundary test** — does QD recognize the degeneracy and gracefully reduce to bearing-only, or does it fail to handle the limit case? Either result is informative.

**`esa_planck_cosmic` (D=5, T=17).** D=5 is the smallest D where quaternions are not the natural fit. Under QD, this experiment requires **explicit dimensional reduction** to a 4D subspace before the quaternion view applies. The reduction error itself becomes a per-experiment diagnostic — "how much of the trajectory's structure is captured in the dominant 4-mode?" An answer of >99% means QD is essentially exact even for D > 4; an answer of <80% means QD only sees the projection, and the reviewer needs to know.

---

## What QD does NOT promise

Honest scope:

- **QD does not change any CNT result.** Hashes don't move. IR classes don't reclassify. Determinism gate doesn't shift. If the corpus matches today, it matches tomorrow.
- **QD does not extend to all compositional data trivially.** D=4 is the natural fit; D=2 collapses; D=8 plausibly factors; D=5, 6, 7, 10 require explicit reduction. The reduction is not free.
- **QD is not faster.** Quaternion algebra is not asymptotically faster than CNT's current channel arithmetic. The benefit is structural clarity and cross-domain recognisability, not performance.
- **QD does not replace CNT.** Promotion to integration would mean QD becomes a *view layer*, sitting alongside the existing channel view, sharing the same engine output, both audit-trailed.

---

## The integration cost, if validated

If all corpus tests pass and Peter approves promotion to integration:

| Component | Cost | Notes |
|---|---|---|
| Volume IV write-up | ~3 days | The math + worked examples + cross-references |
| `quaternion_view.py` engine sibling | ~5 days | Reads CNT JSON, computes quaternion path, outputs `qd.json` with parallel hash chain |
| Stage 4 simplification | ~2 days | Replace channel-by-channel logic with single Hamilton-product call (after validation against existing Stage 4 outputs) |
| SLERP upgrade for projector_html | ~1 day | Swap linear interpolation for SLERP in the existing widget |
| New parity diagnostic in JSON | ~0.5 day | Add a top-level field to the schema (would require schema 2.2.0 bump) |
| Updated handbook cross-references | ~1 day | Volumes I, II, III gain pointers to Volume IV where the quaternion-view notation is the cleaner expression |
| Documentation sweep | ~1 day | READMEs at relevant high-traffic folders gain a "Quaternion view" section, parallel to the CCTT and OPERATIONS_PROTOCOL features |

**Total: ~14 days of focused work**, distributed across one CNT release cycle. Most of this is documentation and verification; the actual quaternion-view code is small (the algebra is already mature, the integration is mostly plumbing).

This is the cost *only if validation succeeds*. Until then it's documents-only; the cost is what's already been spent (this round of writing).

---

## The case for considering integration, summarised in one paragraph

If QD validates against the corpus, CNT gains a second name for several of its operations — and that name comes from a 200-year-old algebra that physicists, roboticists, computer graphics engineers, and quantum-information researchers all already use natively. The CodaWork audience hears "compositional analysis"; the post-CodaWork audience hears "compositional analysis on SU(2) with hash-chained provenance and dual-mode AI/User access protocols," which is a sentence that opens doors into adjacent communities the current CNT framing does not. The hashes don't change. The reviewer audit doesn't change. The user-facing experience (CCTT, OPERATIONS_PROTOCOL) doesn't change. What changes is the surface area of the conversation CNT can have. That surface area, after CodaWork 2026, is what determines whether the project remains a single-author research line or grows into a community.

---

## What happens next

This document is documents-only. No action is requested. No promotion is triggered.

After CodaWork 2026 — if Peter wants to investigate further — Round 2 of QD would run Concept 1 and Concept 10 against backblaze_fleet and the calibration fixtures (per [`QD_CORPUS_COMPARISON_PLAN.md`](QD_CORPUS_COMPARISON_PLAN.md)). If both pass, the project advances to Round 3 with concrete evidence. If they don't, the project archives quietly and the canonical CNT system continues unchanged.

Until then, this folder sits at the workspace root, isolated from the canonical repo, available for any future Cowork session that wants to pick it up.

---

*Exploration. The instrument reads. The expert decides. The hashes carry the receipts. The protocol holds the line so the work can move forward.*
