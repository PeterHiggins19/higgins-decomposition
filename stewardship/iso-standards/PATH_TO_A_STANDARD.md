# Path to a Standard — how MC‑4 becomes a recognized method

*Updates and extends the ISO/MC‑4 root (`README.md` here, distilled from `MC4_ISO_Positioning_Document.docx`, Higgins, April 2026) with what the instrument has since become: a deterministic, gauge‑R&R‑clean, conformance‑testable reference. This is the strategy on the record — honest about where it stands. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; a proposal, not an accepted standard — interest expressed is never endorsement acquired. Standards‑adoption itself is Tier 3 (to earn).*

---

## Why this document exists now

The April‑2026 positioning root already made the gap case correctly: MC‑1 (magnitude), MC‑2 (identity), and MC‑3 (trend) each have mature ISO homes (ISO 17025 and the GUM/JCGM 100; ISO 5725; ISO 7870 / 22514) under TC 69; **MC‑4 (composition) has none.** It also named, precisely, the piece that was missing — *"the operational and institutional scaffolding to deploy that mathematics as a formal monitoring standard, and the deterministic instrument that makes a composition read reproducible and auditable."* That piece now exists. This document is the bridge from the gap argument to a realistic path, given the instrument the project has built since.

## Three barriers, not one — and why work stops at MC‑3

Composition is often the *more* important read (every helmsman result shows the driver is frequently a minor component). Work stops at MC‑3 not because the fourth category matters less, but because it has cost the practitioner three things at once:

- **Effort** — the simplex and log‑ratio geometry are counterintuitive; Euclidean instincts give systematically wrong answers.
- **Awareness** — most practitioners do not know that ratio blindness is a condition they already suffer from.
- **Tooling** — until now there was no turnkey, reproducible way to simply *run* it.

A standard cannot be written against a method that demands a research program to apply. The instrument plus the onramp (`Hs/onramp/`) clear all three: the AI carries the CoDa (effort), each real‑data run is a concrete demonstration of the blind spot (awareness), and the engine is push‑button with a content hash (tooling). That is the precondition for standardization — converting a guild art into a procedure.

## The decisive property: the read is a function

A standard is built on reproducibility, not on a result. **IEEE 754 did not standardize an answer; it standardized reproducible arithmetic** so any conforming implementation returns the same bits. Hˢ has exactly that shape: a composition series in → readings + a deterministic content hash out, bit‑identical across platforms, with the engine's contribution to gauge R&R at machine epsilon (see `HCI-CNTT/DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md`). This is what makes a *method* certifiable rather than a *result* arguable:

- a **reference implementation** (CN‑TT v4) plus a frozen validation oracle;
- a **conformance test vector** — any tool that reproduces the published hash on the reference data is certified conformant;
- a **determinism certificate** (re‑run → identical hash) that is *stronger* than an estimated %GRR because it is exact;
- exact **uncertainty propagation** that is GUM‑compatible (the instrument adds none, it carries the user's).

So the framing is not "ask ISO to adopt a concept" — concepts do not standardize. It is: **Hˢ can be the reproducibility reference for compositional measurement — the IEEE‑754 of the simplex.**

## The wedge: extend the standards they already hold

ISO adoption is an institutional consensus process, not a technical verdict — technical readiness is necessary and not sufficient. The realistic move is therefore not to propose a new philosophy but to **extend a standard TC 69 already maintains.** Measurement‑Systems Analysis and its kin (the GUM on uncertainty, ISO 5725 on accuracy/precision, ISO 7870 on control charts, ISO 22514 on process capability) already define how a measurement system is qualified — *for magnitude, identity, and trend.* The proposal meets them where they stand: **composition is the fourth category MSA is currently blind to**, and the same qualification machinery (repeatability, reproducibility, capability, control limits) can be defined for a compositional read once the read is deterministic. A compositional extension of MSA is an easier institutional ask than a standalone MC‑4 standard, and it is the same destination.

## The evidence has four independent legs

A standards case is strongest when no single leg carries it, and this one has four that fail independently:

1. **CoDaWork science** — peer‑reviewed compositional geometry (Aitchison 1982 onward; Egozcue, Pawlowsky‑Glahn, Hron, et al.). The mathematics is *recognition, not invention*; it is not the project's alone.
2. **Hˢ reproducibility** — a deterministic reference implementation, a validation corpus across many domains, content hashes, and the gauge‑R&R/determinism doctrine.
3. **HUF governance** — claim tiers, honest‑broker discipline, auditable provenance; the claims were not reverse‑engineered to a desired conclusion.
4. **RWA physical origin** — MC‑4 was *forced by loudspeaker diffraction physics* (the DADC→MC‑4 bridge) before it was ever a compositional claim — the best possible defense against curve‑fitting to a flattering result.

Peer‑reviewed foundation, reproducible instrument, auditable governance, independent physical origin: that is precisely the portfolio a standards body needs to see.

## The honest ladder — and where the project actually stands

| Rung | What it is | Status |
|---|---|---|
| Reference implementation + conformance vector | CN‑TT v4 + frozen oracle + published hashes | **Have** (Tier 1) |
| Determinism certificate + gauge‑R&R framing | The doctrine note + self‑tests | **Have** (Tier 1) |
| Cross‑domain validation corpus | 20+ real‑data runs, blind‑test record | **Have** (Tier 1) |
| Governance + provenance | HUF‑gov, claim tiers, the origin bridge | **Have** |
| Method / benchmark paper | The CoDaWork submissions in progress | **In progress** |
| Community position / endorsement | CoDaWork backing | **To earn** (not assumed) |
| Standards‑body engagement (TC 69) | A sponsor, a study item, consensus | **Not initiated** |
| ISO/TR, guideline, or standard | The destination | **Tier 3** |

The instrument has moved the early rungs from "research program" to "done." The later rungs are an institutional campaign that the technical readiness has, for the first time, made *winnable* — but consensus must still be built, one demonstrated result and one convinced colleague at a time.

## The onramp is the consensus flywheel

The same mechanism that gives a field‑expert PhD a fast result (`Hs/onramp/`) is the mechanism that builds the consensus a standard needs: every researcher who walks away with a real finding and intact, correctly‑applied CoDa methods is also a future voice in the community that would have to endorse the standard. Adoption and standardization are not two campaigns; they are one flywheel.

## Honest scope (unchanged from the root)

The mathematics is standard CoDa‑compatible geometry; the contribution is the deterministic monitoring instrument and the proposal to recognize composition as a fourth standardizable category. MC‑4 is **recognition, not invention.** Today it is a **proposal** — no ISO work item, no committee engagement, no endorsement. Nothing here is initiated. *The instrument reads. The expert decides. A standard is written against what can be reproduced.*

---

*Integral references: this folder's `README.md` (the ISO root) · the full `HUF/science/coda-monitoring/MC4_ISO_Positioning_Document.docx` · `HUF/science/reference/02_THE_FOUR_MONITORING_CATEGORIES.md` (the MC‑1..4 source) · `HUF/huf-gov/RATIO_BLINDNESS_DOCTRINE.md` · `HCI-CNTT/DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md` · `HCI-CNTT/DESIGN_PHILOSOPHY_THE_EXPERT_ENGINE_AND_THE_GUARDS.md` · `onramp/PHD_ONRAMP_PROTOCOL.md` · roots map: `ai-refresh/REDISCOVERY_INVENTORY_2026-06-14.md`.*
