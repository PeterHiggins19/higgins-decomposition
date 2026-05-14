# HUF-GOV ↔ Hs Change Control v1.0 Integration Map

**Created:** 2026-05-12 (pre-conference lockdown, S2 doc-only)
**Purpose:** trace every Hs-side governance rule, configuration, interface, and procedure back to the parent HUF-GOV doctrine article that authorizes it. The map is the structural integration document — it makes the parent-child relationship between HUF Governance Charter (April 2026) and Hs Change Control v1.0 (May 2026) explicit at the rule level.

---

## The framing

Hs Change Control v1.0 (INV-063 STAGED) is **not a Hs invention.** It is a fast-research-codebase specialization of the parent HUF-GOV pipeline. The parent doctrine — published in the companion [Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework) repository at `huf-gov/` — established the principles in April 2026. Hs Change Control v1.0 instantiated those principles for the specific operating regime of a multi-AI-collaborated codebase moving through 40+ pushes inside two months while maintaining doctrinal coherence.

The traceability is the integration. Without it, the Hs-side rules look like local invention. With it, they read as specializations of a broader doctrine that has been published, peer-reviewed across the HUF AI Collective, and exercised across the parent pipeline.

---

## Article-by-Article traceability

### HUF Governance Charter Article I — Purpose

**Charter text.** *"HUF shall be used to reveal structural conditions, support disciplined interpretation, and preserve accountable judgment at the point of correction."*

**Hs-side specialization.**
- The entire Hs repository is a worked deployment of Article I purpose. CNT v3.1.0 and CNQ v2.0.0 reveal structural conditions (K_eff, TV distance, Aitchison-native metrics, twin-quaternion factoring). The Investigation Catalog supports disciplined interpretation (every claim is dispositioned and traced). The HUF AI Collective + Peter as operator preserve accountable judgment.
- `README.md` at Hs repo root states Article I purpose for the Hs deployment.

**Trace.** Article I → entire Hs repository.

---

### HUF Governance Charter Article II — Governed Breakpoint Principle

**Charter text.** *"A governed system shall preserve an observable breakpoint at the moment of self-correction... The governed breakpoint is not a defect. It is the structural condition that makes governance possible."*

**Hs-side specialization.**
- **HCC-R005 (impact map required).** Every Discovery Change Packet must include an explicit impact map identifying the files, claims, and downstream consequences of the proposed change. The impact map IS the observable breakpoint — it makes the proposed correction visible before execution.
- **HCC-R008 (human governs release).** No DCP transitions to `released` status without explicit Peter authorization. The release gate IS the breakpoint.
- **DCP lifecycle:** `proposed → in_progress → implemented → verified → released`. Five stages, each with explicit gate criteria. Each gate is a breakpoint at which external judgment may enter.
- **Hs Change Control v1.0 doctrine doc:** `ai-refresh/CHANGE_CONTROL_README.md`.

**Trace.** Article II → HCC-R005 + HCC-R008 + DCP lifecycle.

---

### HUF Governance Charter Article III — Right to Interrupt

**Charter text.** *"Any governed use of HUF shall preserve the right of a human or authorized external agent to interrupt, modify, defer, or reject closure. A system that cannot be interrupted cannot be meaningfully governed. The Governed Breakpoint Principle creates the Right to Interrupt."*

**Hs-side specialization.**
- **HOLD-TO-PUSH protocol.** Every push prepared by Claude enters HOLD state until Peter explicitly clears it ("excellent, push it" or equivalent). HOLD-TO-PUSH is the interrupt-by-default mechanism.
- **PRE_CONFERENCE_LOCKDOWN.md.** Currently active 2026-05-12 → 2026-06-06. Lists what is locked, what is allowed, what is forbidden. The S0-defect protocol describes how an emergency interrupt would route through Peter's explicit authorization.
- **Cross-AI Coordination apparatus.** `ai-refresh/CROSS_AI_COORDINATION.md` — any of Claude, ChatGPT, Grok, Gemini, Copilot can flag any action by another. Peter can interrupt any of them. The Collective IS the interrupt mechanism.

**Trace.** Article III → HOLD-TO-PUSH + PRE_CONFERENCE_LOCKDOWN + Cross-AI Coordination apparatus.

---

### HUF Governance Charter Article IV — Open-Loop Priority

**Charter text.** *"HUF-GOV shall be treated as the default posture wherever accountable interpretation matters. Open-loop operation shall take priority over closed-loop automation unless closure is explicitly justified, reviewable, and answerable to responsible authority. HUF-CLS may optimize correction. HUF-GOV protects judgment."*

**Hs-side specialization.**
- **The Hs engine is structurally open-loop.** CNT and CNQ produce JSON outputs (structural readings) that humans interpret. The engine does not act on its own readings. No feedback path from CNT/CNQ output to engine-input modification exists by design.
- **LOOP-001 (parent doctrine) is honored throughout Hs.** Every Hs document that contains the closing line *"The instrument reads. The expert decides."* is implementing the LOOP-001 doctrinal restatement.
- **KILL-4.1 (close-the-loop) is a recognized doctrinal kill.** Any proposed feature that would close the loop is refused on KILL-4.1 grounds.

**Trace.** Article IV → entire Hs engine architecture + LOOP-001 closing line discipline + KILL-4.1 doctrinal refusal pattern.

---

### HUF Governance Charter Article V — Integrity of Purpose

**Charter text.** Five commitments: (1) Observation before automation; (2) Visibility at correction; (3) Human judgment at the breakpoint; (4) Honest treatment of uncertainty; (5) Governance as protection.

**Hs-side specialization per commitment.**

| Article V commitment | Hs-side implementation |
|---|---|
| Observation before automation | Engine produces JSON; humans interpret; no automated downstream pipeline at the engine boundary. SAFE-001 Principle 1 (Perceive Before Acting) explicitly enforced through cross-AI cross-check before any binding action. |
| Visibility at correction | Every DCP records the proposed correction, the response, and the consequence as visible structured fields. DCP-001 in `ai-refresh/change_packets/` is the worked example. |
| Human judgment at the breakpoint | HCC-R008 + HOLD-TO-PUSH protocol + Peter as the release gate for every push. |
| Honest treatment of uncertainty | Investigation Catalog disposition system (CANONICAL / STAGED / DEFERRED / OPEN / FALSIFIED / CLOSED) names confidence explicitly. HSA-001 (headline rule, parent doctrine) cools every external claim to standing assessment level. KILL-4.2 (overclaim) is the recognized doctrinal kill. |
| Governance as protection | Hs Change Control v1.0 + the consistency checker + cross-check archive + breaker inventory exist as protection layers around the engine, not as decoration on it. |

**Trace.** Article V → DCP records + Investigation Catalog disposition + HCC-R008 + consistency checker + cross-check archive.

---

### HUF Governance Charter Article VI — Accountable Data

**Charter text.** *"Claims made through HUF shall remain answerable to the data from which they arise. Data handling shall preserve provenance, context, transformation history, known limits, and relevant confounds. No claim shall outrun the integrity of the data supporting it."*

**Hs-side specialization.**
- **CNQ Vector PDF spec (INV-062 STAGED).** `papers/codawork2026/planning/CNQ_VECTOR_PDF_SPEC.json` — 30-key specification for outputs that embed the source data and the hash chain directly in the PDF metadata (PDF/A-3 embedded files; SHA-256 hashes in `/Hs_Content_SHA256` and `/Hs_CNQ_Content_SHA256`; structured JOURNAL.md logging per run_id). The output is self-describing and self-verifying.
- **Engine determinism + expected_results.json.** Every push verifies that the engine produces bit-identical results on canonical corpora. The hash chain is the integrity guarantee.
- **Adapter disclosure consolidation.** Every dataset adapter declares its source, transformation history, and known limits. `HCI-CNT/adapters/` documents this.

**Trace.** Article VI → INV-062 CNQ Vector PDF spec + expected_results.json + adapter disclosure.

---

### HUF Governance Charter Article VII — Accountable Resolution

**Charter text.** *"No resolution shall be treated as legitimate unless the path from observation to recommendation to response remains inspectable, interruptible, and reviewable."*

**Hs-side specialization.**
- **DCP lifecycle ensures every resolution is inspectable.** Each DCP captures the path from observation (what drift was found) → recommendation (what change is proposed) → response (what is being implemented) → verified (what was actually done) → released (what Peter authorized).
- **Cross-check archive (`ai-refresh/cross_check_archive/`).** 11+ AI-session transcripts preserved with per-section signal/noise/hallucination verdicts. The audit trail makes review possible.
- **PUSHES_INDEX.md.** Every push is documented with SHA, CI run number, theme, hand-off doc.

**Trace.** Article VII → DCP lifecycle + cross-check archive + PUSHES_INDEX.

---

### HUF Governance Charter Article VIII — Rights Preserved

**Charter text.** Eight enumerated rights: inspect the signal, question the recommendation, interrupt closure, defer action pending review, refuse false certainty, keep the loop open where judgment requires it.

**Hs-side specialization per right.**

| Right | Hs-side implementation |
|---|---|
| Inspect the signal | Engine JSON outputs are human-readable; expected_results.json exists for verification; HCI-CNT/HCI-CNQ source code is open. |
| Question the recommendation | Investigation Catalog OPEN disposition exists specifically for hypotheses awaiting evaluation. |
| Interrupt closure | HOLD-TO-PUSH protocol + lockdown protocol. |
| Defer action pending review | Investigation Catalog DEFERRED disposition. INV-031, INV-032, INV-033, INV-034 are examples of deferred items. |
| Refuse false certainty | HSA-001 headline rule + KILL-4.2 (overclaim) doctrinal kill + ChatGPT cross-check practice. |
| Keep the loop open | LOOP-001 (parent doctrine) + KILL-4.1 (close-the-loop kill) + Article IV Open-Loop Priority. |

**Trace.** Article VIII → Engine open-ness + Investigation Catalog dispositions + HOLD-TO-PUSH + HSA-001 + LOOP-001 + KILL-4.1.

---

### HUF Governance Charter Article IX — Declaration

**Charter text.** *"A governed system must preserve an observable breakpoint at self-correction, and through that breakpoint preserve the Right to Interrupt."*

**Hs-side specialization.**
- The entire Hs Change Control v1.0 doctrine is the Article IX declaration applied to a fast-research codebase. Every HCC-R rule, every DCP gate, every severity class, every lockdown protocol is the operational restatement of Article IX.

**Trace.** Article IX → Hs Change Control v1.0 doctrine (the whole apparatus).

---

## Companion-doctrine traceability

The HUF Governance Charter is the parent doctrine. Several other HUF-GOV documents extend or complement it. Their Hs-side traces are below.

### LOOP-001 — Open Loop Doctrine / Skydiver Principle

**Parent text source.** `[HUF repo]/huf-gov/governance/LOOP-001-open-loop-doctrine.json`.

**Hs-side trace.** The closing line *"The instrument reads. The expert decides."* appears in dozens of Hs docs as the operational restatement. KILL-4.1 (close-the-loop) is the named doctrinal kill in Hs Investigation Catalog discussions. The Hs engine is structurally open-loop.

### KILL-001 — 19 Named Failure Modes

**Parent text source.** `[HUF repo]/huf-gov/governance/KILL-001-kill-test.json` (16,000+ lines, 5 categories, 19 enumerated failure modes).

**Hs-side trace.** KILL-001 is the published falsifiability artifact for the entire Hs + HUF stack. The Investigation Catalog's FALSIFIED disposition (currently 1 entry) is the Hs-side mechanism for recording when a Hs-side claim fails a KILL-001-style test. The 2026-05-12 breaker test (`papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`) is a Hs-side exercise of the KILL-001 methodology applied to the governance layer itself.

### SAFE-001 — 7 Principles for Cognitive Agents

**Parent text source.** `[HUF repo]/huf-gov/governance/SAFE-001.json`.

**Hs-side trace per principle.**

| SAFE-001 principle | Hs-side mechanism |
|---|---|
| 1 — Perceive Before Acting | Pre-action read of relevant files; AI_AGENTS.md §2.1 cache-lag check; cross-AI review before binding action. |
| 2 — Sometimes Do Nothing | HOLD-TO-PUSH; DCP `proposed` status without execution; lockdown's "do nothing on engine code" posture. |
| 3 — Detect and Report Drift | Consistency checker; cross-check archive; AI_AGENTS.md §2.1 cache-lag detection signals. |
| 4 — Respect the Override | Every Peter directive in conversation is absorbed as governance input; no subtle reversal. |
| 5 — Work Safe With All Agents | HUF AI Collective protocol; no single AI dominates; Peter as the bus. |
| 6 — Dull Tool Principle | Cross-AI cross-check catches Claude / ChatGPT / Grok degradation; cache-lag detection is self-reporting of stale state. |
| 7 — Power Tools Create | The Hs engine + the doctrine together — controlled power tool producing value with governance, not unsupervised automation. |

### GOV-003 — Pure HUF-GOV Standalone (zero CLS contamination)

**Parent text source.** `[HUF repo]/huf-gov/governance/GOV-003-standalone.json`.

**Hs-side trace.** The Hs engine produces pure HUF-GOV outputs by design — observation only, no closed-loop control. Article IV's Open-Loop Priority is the operational guarantee. The Hs engine has zero CLS dependencies in any code path.

### HAGF-001 — Applied Governance Framework

**Parent text source.** `[HUF repo]/huf-gov/governance/HAGF-001.json`.

**Hs-side trace.** HAGF-001 Principle 5 (Human Primacy) is the parent doctrine for HCC-R008 (human governs release). Every binding decision in Hs routes through Peter; HAGF-001 is why.

### HANDOFF-001 — Session-to-Session Handoff Protocol

**Parent text source.** `[HUF repo]/huf-gov/governance/HANDOFF-001.docx`.

**Hs-side trace.** The session summary protocol used between Claude sessions (this very conversation followed it) is the Hs-side specialization of HANDOFF-001. PUSHES_INDEX.md + push hand-off docs (PUSH##_READY_FOR_COMMIT.md) are the documentary form.

### ONTO-001 — Ontological Foundation

**Parent text source.** `[HUF repo]/huf-gov/science/ontological-foundation.json`.

**Hs-side trace.** ONTO-001's pre-existing-condition claim (the simplex is the room; the constraint is the door; HUF is the instrument) is honored throughout Hs. The Hs engine does not create the structure it measures — it reveals structure already present in the carrier data. INV-026 universality result is the empirical companion.

### EITT — Entropy-Invariant Time Transformer

**Parent text source.** HUF science folder (companion repository); canonical Peter-confirmed explanation at `papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md` in the Hs working repo.

**The claim.** Shannon entropy is conserved under geometric-mean temporal compression for compositional carriers. Measured variation under one-fifth of one percent (0.18%) across a 341:1 compression ratio. Verified against six published HUF case studies (Backblaze, GDP, OWID, Ramsar, Planck, Toronto TTC, Energy).

**Why it sits in this integration map.** EITT is a HUF-side Layer 1 scientific contribution distinct from MC-4. MC-4 is the spatial-invariance result (compositional change detection under Aitchison-metric equivalence). EITT is the temporal-invariance result (entropy conservation under geometric-mean compression). Together they describe a structurally invariant view of any proportional system across both spatial and temporal dimensions. Both are HUF science; both are operationalized through CNT v3.1.0 / CNQ v2.0.0 on the Hs side; both live under the same KILL-001 falsifiability discipline.

**Hs-side trace.** EITT does not have a dedicated Hs INV catalog entry because EITT is HUF-owned. Hs honors EITT by:

- Operating CNT/CNQ in a manner compatible with geometric-mean temporal compression (Aitchison-native compositional operations preserve the simplex throughout).
- Including EITT in the Layer 1 scientific contribution map in `papers/POST_CODA_PARTNERSHIP_TARGETS.md` v4.
- Cross-referencing the EITT canonical explanation from this integration map.
- Honoring EITT's published kill conditions per KILL-001 (proportional data required; sufficient carrier dimensionality required; mathematical conservation not domain prediction; external forcing events invisible).

**Authoring lineage.** EITT, like all HUF science, is *"Peter Higgins / Rogue Wave Audio, with the HUF AI Collective: Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI)."* The canonical explanation was Peter-confirmed on 2026-05-12 with the directive *"exactly correct as I see it"* — the same confirmation that authorized this folder's structural addition.

---

## Configuration-item to Charter-article cross-reference

Every Configuration Item in `ai-refresh/CONFIGURATION_ITEMS.json` is governed by one or more Charter articles. The full map is below for any auditor who wants to verify the trace.

| CI ID | Item | Primary governing article |
|---|---|---|
| CI-001 | HCI-CNT engine (cnt.py, cnt.R) | Article I + IV + VI |
| CI-002 | HCI-CNQ engine (cnq.py, cnq.R) | Article I + IV + VI |
| CI-003 | hci_shared/ library | Article VI + VII |
| CI-004 | expected_results.json | Article VI + VII |
| CI-005 | Investigation Catalog | Article V + VII + VIII |
| CI-006 | Configuration Items registry (this file's source) | Article IX |
| CI-007 | Interface Control matrix | Article VII + IX |
| CI-008 | Traceability Matrix | Article VII |
| CI-009 | Change Packets (DCP filings) | Article II + III + VII |
| CI-010 | AI_AGENTS.md | Article V (visibility) + VIII |
| CI-011 | HS_FAST_REFRESH.json | Article V (visibility) |
| CI-012 | HS_ADMIN.json | Article VII + IX |
| CI-013 | CHANGELOG.md | Article VII |
| CI-014 | PRE_CONFERENCE_LOCKDOWN.md | Article III + IX |
| CI-015 | Consistency checker (scripts/check_ai_refresh_consistency.py) | Article V (visibility at correction) + IX |

---

## What this integration map enables

Three concrete capabilities:

1. **Audit defensibility.** Any external reviewer asking "what authorizes this Hs-side rule?" can be answered with a Charter article citation. The discipline is no longer a Hs invention — it is a published-parent-doctrine specialization.

2. **Maintenance simplification.** When the Charter evolves (Article II revision, or a new Article X), the Hs-side specializations have explicit dependency arrows. A Charter revision becomes a DCP scope question rather than a hunt-for-everything-affected exercise.

3. **Pedagogical clarity.** A first-time AI session arriving fresh can read the Charter (9 articles, ~3 pages), then this integration map (~5 pages), and have a complete understanding of how Hs operates within HUF-GOV. The combined ~8 pages replace what was previously implicit and scattered across 49 push narratives.

---

*Origin: Peter Higgins / Rogue Wave Audio, with the HUF AI Collective.*
*HUF-GOV protects judgment. HUF-CLS optimizes correction. Hs implements the deterministic engine under both.*
*The Charter is the parent doctrine. Hs Change Control v1.0 is the worked specialization.*
*Article II creates the breakpoint. Article III preserves the interrupt. Article IV holds the loop open. The breakpoint holds.*
