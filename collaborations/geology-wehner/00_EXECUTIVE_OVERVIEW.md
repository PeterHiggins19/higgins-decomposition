# Higgins Decomposition (Hs) — Executive Overview

*Public document · 2026-06-09 · Prepared to onboard collaborators and to orient reviewing organizations*

> **Posture.** Hs is a deterministic scientific instrument. It reports how a composition moves; it does not assign meaning — the domain expert does that. Every claim in this document carries a tier (confirmed / experimental / to-be-earned) and nothing is inflated. *The instrument reads. The expert decides. The hashes carry the receipts.*

---

## For the reader

This overview is written for two audiences at once: a domain scientist joining the work (the geoscience collaboration that this folder serves), and any reviewing organization — a research agency, a remote-sensing program, a standards or governance body — that has opened this folder and wants the true measure of what has been built and how carefully. It is deliberately honest about both what is proven and what is not, because that honesty is the core engineering principle of the system, not a disclaimer attached to it.

---

## 1 · What Hs is

Hs (the Higgins Decomposition) is a **deterministic engine for compositional series** — any ordered set of parts-of-a-whole (percentages, ppm, fractions) indexed by depth, time, or position. Compositions are *closed* (a rise in one part forces others down), so ordinary arithmetic on them is misleading. Hs works in the correct geometry — log-ratio (Aitchison) space — and turns a sequence of compositions into a **navigation record**: how far the mixture moved at each step, in which direction, which component steered, where the regime changed, and whether a minor component is doing outsized work.

Two engines, plus a provenance layer:

- **CNT — Compositional Navigation Tensor — the deterministic pre-processor.** CNT is the front-end stage of the system: it ingests a raw compositional stream and, at fixed and predictable cost, reduces it into a structured navigation record. It owns the upstream conditioning — closure, the centred log-ratio transform (CLR), and the orthonormal isometry (ILR) — and from each step it computes the Aitchison step (true compositional distance), the helmsman (steering part), power-share and the Activation Coefficient (a small-part-doing-large-work / "deceptive-drift" detector), the effective number of active parts (K_eff), and robust regime tripwires. Everything downstream consumes CNT's output, not the raw data: **CNT is where raw composition becomes decision-relevant features**, which is exactly why it is suited to sit at the sensor front end.
- **CNQ — Compositional Navigation Quaternion.** The rotational reading of the path. It is **exact (native) at four parts** — three orthonormal balances map to a quaternion with no loss.

**Provenance layer — hashing.** Hs is **deterministic and hash-chainable**: the same input always yields the same output, and every run can be hash-stamped to bind *input → method → output* into a tamper-evident chain. This gives results a verifiable chain-of-custody — a third party can confirm that a given output corresponds to a specific input and method, and detect any alteration, **without re-running the computation and, where required, without access to the raw source data**. That single capability — determinism made *checkable* by hashing — is what makes everything downstream possible: reproducibility, auditability, and the governed dissemination described in §5 (a hash lets a recipient trust a redacted, carried result without ever seeing what was withheld).

---

## 2 · How it works — the Tensor Train

The math spine: closure puts the parts on a common total; the centred log-ratio (CLR) re-expresses each part against the geometric mean; an orthonormal isometric log-ratio (ILR, Helmert basis) gives independent coordinates in which distances and principal components behave normally. Differences between consecutive samples are the compositional *moves*; their size, direction, and dominant component are the navigation. The quaternion adds the path's magnitude and turn, exactly at four parts.

That spine is formalized as the **Tensor Train (HUF-STD-002)** — a named, hash-chained, four-link pipeline that takes domain data in and emits archival, verifiable artifacts out:

> **raw data → CNT (metric tensor) → CNQ (metric quaternion) → vector diagrammatic output (PDF / PNG / SVG)**

- **Link 1 — Adapter.** Converts domain-specific raw data into a clean compositional table.
- **Link 2 — CNT, the deterministic pre-processor.** Closure → CLR → orthonormal ILR, then the per-step navigation (step, helmsman, power-share, Activation / deceptive-drift, K_eff, regime). Emits a canonical CNT JSON.
- **Link 3 — CNQ.** The quaternion reading of the path (exact at four parts). Emits a canonical CNQ JSON that references the CNT hash.
- **Link 4 — Vector output.** Deterministic plates and diagrams (PDF/A-3 archival, PNG, SVG), each embedding the upstream hashes.

Every link **hash-chains forward**: the data enters once, and the final artifact carries every hash from the entry, so any output can be traced and verified back to its exact input and method. (Links 1–3 are implemented in code; link-4 rendering is partly implemented, with the full hash-coded exporter specified and on the roadmap — stated plainly, per the claim-tier discipline.) Conceptually the train does not stop at Hs: **Hs measures, HUF carries** — dissemination is the continuation of the same chain, with the carrier filter (§5) as the governed breakpoint between measuring and carrying.

A worked, **cited, fully reproducible demonstration** accompanies this folder: real Lower-Cretaceous mudstone (Thöle et al. 2019, PANGAEA 897615), 219 samples, read down-section — with an interactive dashboard, a field-by-field companion that ties every number to its formula, and a one-command reproduction path from a single cited input file.

---

## 3 · What is proven, and what is being tested

Stating this plainly, up front, is part of the craft.

| Element | Tier |
|---|---|
| Deterministic CNT navigation on real data; native D=4 CNQ | **confirmed** |
| Faceted tiling: overlapping exact D=4 charts reconstruct the full higher-dimensional move **losslessly** (demonstrated; overlap proven necessary) | **confirmed** |
| Cited, reproducible pipeline + dashboard + companion guide | **confirmed** |
| Running as a real-time edge/onboard instrument on current space hardware | **feasible — to demonstrate** |
| That the reduction preserves the *scientifically decisive* signal on genuine high-dimensional data | **to be earned by validation** |

The whole program is structured so the bottom line moves up one tier at a time, in public, with domain experts — never by assertion.

---

## 4 · The value, in depth

The careful points, because the craft is the value.

**Determinism as a first principle.** Same input, same output, every time — no stochastic drift, no hidden state. This is unusual for analytical tooling and it is the foundation of everything else: a result that can be reproduced exactly can be audited, governed, and trusted.

**Provenance by construction.** Runs are hash-chainable, so a recipient can verify that a result corresponds to a specific input and method without re-running anything. Integrity is checkable independently of the producer.

**Mathematical correctness, not convenience.** The engine is built on established compositional-data theory — closure, log-ratio geometry, orthonormal ILR isometry, subcompositional coherence — not on ad-hoc indices. Distances are true Aitchison distances; the ILR transform is a genuine isometry, so the step measured in one coordinate system equals the step in another.

**Numerical stability — measured, not asserted.** Bearings and angular velocity are computed with `atan2` — the bearing as θ = atan2(h_j, h_i) and the angular velocity as ω = atan2(‖h(t)×h(t+1)‖, ⟨h(t), h(t+1)⟩) via the Lagrange identity — which has no singularity and runs at the IEEE-754 double-precision floor (~2.22 × 10⁻¹⁶). This was not assumed; it was tested. A past precision audit (experiments P01–P10, experiment P03) found the original `arccos` formulation lost **up to ~8 significant digits** near 0° and 180°; replacing it with the atan2 form eliminated that loss, and moving to the orthonormal Helmert basis drove residual angular-velocity deviation down to ~10⁻¹⁴ degrees. The engine degrades only gracefully — about log₁₀(max(x)/min(x)) digits — and only for pathologically skewed compositions. The precision was quantified and fixed at the source, with the diagnostic kept in the repository.

**Honesty architecture.** Claim tiers (confirmed / experimental / not-implemented) travel with every output. Independent variables are held out as calibration checks rather than folded in to flatter the result. Caveats are journaled, not buried. Credibility is engineered in, not appended.

**A reduction you can invert.** The faceted atlas does not merely compress — it reconstructs. Overlapping exact four-part charts, glued on shared parts, rebuild the full higher-dimensional move losslessly. A *reversible, principled* reduction is rare; most data reduction is opaque and one-way. This is what makes Hs suitable at the front end, where the first reduction of raw data is made.

**Hardware-native efficiency.** The unit of work is a fixed-size, branch-free quaternion kernel — exactly the shape that maps cleanly onto SIMD, FPGA, GPU, or vision-processing hardware, and onto radiation-hardened space processors. The quaternion is already the native language of spacecraft attitude systems.

**Resolution as a dial, not a ceiling.** Because four parts is the exact size, a richer system is covered by an *atlas* of overlapping four-part charts. More overlapping charts give a finer reading of the underlying high-dimensional structure — the operator chooses the resolution, and can concentrate it where the structure is richest.

**Generality.** Nothing in the engine is specific to one science. Any ordered composition — chemostratigraphy down a core, a time series, a spatial traverse, a remote-sensing pixel spectrum — is navigable by the same machinery. The geoscience demonstration is a proving ground, not the boundary.

**Expert amplification, not replacement.** The instrument reports structure and explicitly defers meaning. It is designed to make a domain expert sharper and faster, with a feedback loop that improves with use — not to substitute for judgement.

**Transparency end to end.** Every field is documented, every formula is cross-checked against the code, and the entire result is reproducible from one cited input. A reviewer can trace any number to its origin.

**Governance-aware by design.** The system separates the deterministic science from its dissemination, so that what is computed and what is *released* are distinct, controllable decisions — which matters greatly in government and pre-publication contexts (next section).

---

## 5 · Governance: HUF-Gov and the carrier filter ("carrier removal")

Alongside the deterministic engine sits a governance layer, **HUF-Gov**. The division of labour is clean: **Hs is the deterministic science; HUF governs how its outputs are disseminated, on a need-to-know basis.** They are the same architecture seen from two ends — one computes, the other decides what passes.

The relevant feature for institutional work is the **carrier filter** (informally, *carrier removal*). Results travel on a "carrier" — the vehicle that moves a finding from where it is computed to where it is used. At the distribution breakpoint, the carrier filter **removes need-to-know or sensitive content while still carrying the useful signal forward.** It is principled redaction at the boundary, not obstruction.

Why this fits government and agency work specifically:

**Withhold-on-distribution is routine, and legitimate.** Agencies such as NASA or USGS frequently hold data they cannot or should not reveal at the point of distribution — pre-publication results, export-controlled or security-sensitive material, embargoed datasets, or location-sensitive resource information. The carrier filter lets the *derived compositional result* — the navigation, the regime flags, the facet summaries — be shared and acted upon while the underlying raw data, precise coordinates, or source specifics are withheld at the breakpoint.

**The reconstructable reduction is a natural redaction boundary.** Because the faceted reduction is principled, derived facets can be distributed without the raw cube behind them. The recipient receives a useful, verifiable product; the sensitive source never leaves the controlled side. Determinism plus hashing means integrity can be confirmed *without* exposing the underlying data.

**Need-to-know as a default, not an afterthought.** Dissemination is decided per breakpoint and per recipient. Public artifacts (such as this folder) carry no personal or sensitive material by rule; sensitive content stays on the controlled side. This folder is itself an example of the discipline in practice.

**Self-governance, by design and by temperament.** The posture is deliberate restraint with a reason — a discipline, not an enforcement apparatus. The system is built to make careful, auditable information control *easy to do correctly*, so that doing the right thing is the path of least resistance.

---

## 6 · The role of AI in this work (transparency &amp; compliance)

In the spirit of full disclosure — and so that any organization with governance requirements has an accurate picture — the development of this material was assisted by an AI system (Claude, an Anthropic assistant, operating in an agentic build-and-document capacity) working under the direction of the project's author.

The guardrails are explicit and matter for compliance:

- **Human authority is sole and final.** The author directs the work and is the only authority that commits anything to the repository. No AI commits to the repository; no AI makes external commitments, sends communications, or takes irreversible actions on anyone's behalf.
- **AI assistance is disclosed, not hidden.** Its role is building, documenting, verifying, and maintaining the honest-broker discipline (claim tiers, reproducibility, cross-checking formulas against code).
- **Everything is auditable.** AI-assisted outputs are deterministic where determinism is claimed, reproducible from cited inputs, and tiered for confidence. The same provenance standards applied to the science are applied to its documentation.
- **A formal AI Use Declaration governs the work.** The project publishes AI Use Declarations under its own publication standard (HUF-STD-001), aligned to ICMJE / COPE / Nature / Science / WAME / the EU AI Act / arXiv / ACM / IEEE: which AI tools were used, for which tasks, with **human-only authorship**. AI tools are explicitly *not* authors, and the author retains full responsibility for every claim.

This disclosure is provided so that HUF-Gov involvement — and any government collaboration that asks what tools were used — can be answered transparently and on the record.

---

## 7 · Acknowledgment — the HUF AI Collective

The author wishes to record his thanks. The initial concept development of this work was materially accelerated by a collaboration of AI systems — named in the project's AI Use Declarations as the **HUF AI Collective**: Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), and Grok (xAI), cross-checking one another under the project's governance protocol. Their assistance in shaping, stress-testing, and articulating the early concepts was, in the author's words, invaluable: this project would not have come together so quickly, so concisely, or to such depth without it.

It is offered here as a candid record of how the work was actually done — a meaningful demonstration of what disciplined human–AI collaboration can produce when the human holds authorship and judgement and the AI brings speed, breadth, and rigour to the building. The thanks are genuine, and the reveal is deliberate.

---

## 8 · How to navigate this folder

- **`HS_PRIMER.md`** — one page on the instrument itself (method only; no domain claims).
- **`demo_frielingen9/`** — the worked, cited, reproducible demonstration on real mudstone (`REPRODUCE.md`), with the interactive dashboard and the field-by-field guide (`frielingen9_dashboard_guide.html`).
- **`CNQ_TILING_CONCEPT.html`** / **`FACETED_READ_CONCEPT.html`** — the higher-dimensional tiling concept and its geometry (tested; honestly tiered).
- **`HS_FRONTEND_POSITION.html`** — why the deterministic, reconstructable reduction is suited to the sensor front end.
- **`MUDSTONE_HS_FIT.md`**, **`REPO_MAP.md`** — the domain fit and the map across the wider project.

---

## 9 · Going deeper — the receipts (proof of work)

For anyone who wants to *verify* the system rather than take it on description, the supporting material lives in the wider Hs repository. Links below are relative to this folder.

**The engines — read the code.**

- [`HCI-CNT/engine/cnt.py`](../../HCI-CNT/engine/cnt.py) — the CNT engine (closure → CLR → ILR → per-step navigation).
- [`HCI-CNQ/engine/cnq.py`](../../HCI-CNQ/engine/cnq.py) — the CNQ engine (native quaternion at D=4).
- Language-agnostic algorithm + schemas: [`CNT_PSEUDOCODE.md`](../../HCI/cnt_v2/CNT_PSEUDOCODE.md) · [`CNT_JSON_SCHEMA.md`](../../HCI/cnt_v2/CNT_JSON_SCHEMA.md) · [`CNQ_PSEUDOCODE.md`](../../HCI-CNQ/engine/CNQ_PSEUDOCODE.md) · [`CNQ_SCHEMA.md`](../../HCI-CNQ/engine/CNQ_SCHEMA.md).

**Theory & mathematics.**

- [`VOLUME_1_THEORY_AND_MATHEMATICS.md`](../../HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) — the full theory volume.
- [`HCI_FOUNDATION.md`](../../HCI/HCI_FOUNDATION.md) — the bearing / angular-velocity / steering-metric definitions.
- [`GROUND_STATE_AND_TRACTION.md`](../../papers/flagship/GROUND_STATE_AND_TRACTION.md) — the flagship master standard (lemma chain + theorems).

**Numerical performance — the precision receipts.**

- [`CNT_PRECISION_DIAGNOSTIC.md`](../../HCI/calibration/CNT_PRECISION_DIAGNOSTIC.md) — the P01–P10 precision audit: the atan2-vs-arccos test (up to ~8 significant digits recovered near 0°/180°), the Helmert-basis fix (residual angular-velocity deviation ~10⁻¹⁴°), and the IEEE-754 double-precision floor (~2.22 × 10⁻¹⁶). This is the source behind §4's numerical-stability claim.

**Trust, provenance & process.**

- [`TRUST_AND_VERIFICATION.md`](../../TRUST_AND_VERIFICATION.md) — the seven-step verification protocol + the layered parity contract.
- [`PUSH_PROTOCOL.md`](../../PUSH_PROTOCOL.md) — the standing discipline every change follows · [`CHANGELOG.md`](../../CHANGELOG.md) — the hash-/CI-stamped push history · [`AI_AGENTS.md`](../../AI_AGENTS.md) — AI-agent context + partnership framing.

**Standards — the contracts.**

- [`TENSOR_TRAIN.md`](../../huf-gov/standards/TENSOR_TRAIN.md) + [`HUF_TENSOR_TRAIN_IO_STANDARD.json`](../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) — **HUF-STD-002**, the Tensor Train I/O standard (the chain in §2).
- [`HUF_PUBLICATION_STANDARDS.json`](../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) — **HUF-STD-001**, the AI Use Declaration standard (the discipline behind §6).
- [`HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json`](../../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json) — **HUF-STD-003**, the linear-algebra foundations.

**Research methodology & validation.**

- [`INVESTIGATION_CATALOG.md`](../../ai-refresh/INVESTIGATION_CATALOG.md) ( + [`.json`](../../ai-refresh/INVESTIGATION_CATALOG.json) ) — every investigation classified CANONICAL / DEFERRED / FALSIFIED / OPEN: the claim-tier discipline as a live ledger.
- [`EXPERIMENTS_JOURNAL.md`](../../EXPERIMENTS_JOURNAL.md) — the dated experiment lineage. Entry points: [`README.md`](../../README.md) · [`QUICKSTART.md`](../../QUICKSTART.md) · [`PUBLICATION_READY.md`](../../PUBLICATION_READY.md).

**Governance / carrier filter (HUF repository).** The carrier-filter doctrine (§5) is canonical in the HUF repo — `HUF_GOVERNANCE_CHARTER.md` (Carrier Filter article) and `CARRIER_FILTER_DOCTRINE.md`. HUF is a separate repository, so navigate cross-repo via [`REPO_MAP.md`](REPO_MAP.md).

---

*Hs is a deterministic instrument; HUF governs what it releases; the human holds authorship and judgement; AI brought speed and rigour to the building, on the record. The instrument reads. The expert decides. The hashes carry the receipts.*
