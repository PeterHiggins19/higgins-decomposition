# AI Refresh — 2026-05-08 — Concept Verification Aid Request

**Purpose:** open call for AI cross-check work on the canonical content in the Hˢ / CNT / CNQ / HCI-AUDIO / HCI-ULTRASOUND / RWA-001 stack. Any AI platform (Grok next per push #24 hand-off, plus any future Gemini / ChatGPT / Claude session) can pick up this file as their entry point and contribute to concept verification.

**Catalog reference:** this aid request itself is INV-028 (proposed for catalog inclusion as a methodology artifact).
**Companion:** push #24 narrative at [`AI_REFRESH_2026-05-08_push24_grok_crosscheck.md`](AI_REFRESH_2026-05-08_push24_grok_crosscheck.md).
**Verification protocol:** the project's three-platform discipline — Claude builds, ChatGPT cross-checks vocabulary and framing, Grok tests and extends. Every audit lands in the [Investigation Catalog](INVESTIGATION_CATALOG.json) with disposition.

---

## Why this request exists

Push #24 lands a substantial expansion to the canonical layer — the Investigation Catalog (research methodology), the DADC origin lineage, the Helmsman family vocabulary, two new applied sibling tiers (HCI-AUDIO + HCI-ULTRASOUND), the RWA-001 lab identity, and Paper 1's first complete draft. The framework's discipline is to gate every promotion with concrete, verifiable criteria. Several entries currently sit at OPEN or PROPOSED status, and several at CANONICAL would benefit from independent review by an AI session that did not author them.

This file enumerates what we want verified, what the gate criteria are for each verification, and a fast-path recipe so any AI session can productively contribute in 30–90 minutes.

---

## What to verify, per project

### A. CNT (Compositional Navigation Tensor) engine

**Status:** CANONICAL. Engine 2.0.4, schema 2.1.0. Cross-port-validated (Python ↔ R) on all 25 corpus experiments.

**Verification asks:**

1. **Reproduce the determinism contract on at least one corpus experiment.** Recommended: `geochem_tappe_kim1` (small, fast, the original CCTT pilot). Expected `content_sha256 = 707034ec...`. Run from a fresh clone via the protocol in `ai-refresh/CCTT_RUNBOOK.md`. Report bit-identical match or any drift.
2. **Audit the bearing-vs-arccos numerical-stability claim.** Equation (4) of Paper 1 uses `atan2(h_j, h_i)` rather than `arccos(<u, v>)`. Verify the precision-loss claim is correct (atan2 retains ~7 more digits near 0 and pi than arccos).
3. **Stress-test the metric involution M² = I.** Given any positive vector x in the simplex, compute M(M(x)) and confirm `||M(M(x)) - x||_inf < 1e-15`. Edge cases: x with very small components (1e-12), x with extreme imbalance (1 component 0.999, others tiny). Report any case where the residual rises above floor.
4. **Walk the IR-class threshold rules.** The 8-class taxonomy (CRITICALLY_DAMPED, OVERDAMPED_EXTREME, etc.) is set by threshold rules on amplitude A and damping zeta. Are the boundaries reasonable? Where could a real dataset land in an ambiguous region between two classes?

**Gate criteria for verification PASS:**
- Bit-identical content_sha256 reproduction on ≥ 1 corpus experiment.
- Atan2 stability claim independently confirmed.
- Metric involution residual at IEEE floor on ≥ 5 test compositions.
- IR class boundaries documented with at least one ambiguity flagged or confirmed clean.

---

### B. CNQ tier and the universality result (Paper 1)

**Status:** CANONICAL (tier and central claim). Paper 1 OPEN (drafting → submission).

**Verification asks:**

1. **Re-run all three IEEE-floor demonstrations from a fresh clone.** Backblaze (4.441e-16, 730 pairs), Planck CMB (4.441e-16 + M²=I 7.63e-17, 2499 multipoles), SM neutrino (M²=I 7.40e-17). Scripts at `HCI-CNQ/experiments/{backblaze_fleet_quaternion, planck_cmb_quaternion, sm_neutrino_quaternion}/QD_round_2*.py`. Report the residuals.
2. **Audit the bit-identical-residual argument.** Paper 1 §4.1 argues that residuals pegging exactly at 2 × eps_mach across hundreds of independent pairs (and bit-identical across two unrelated datasets) cannot be random rounding-error aggregation. Stress-test this claim. What is the alternative explanation if any exists? Is there a way the framework could be wrong?
3. **Audit the three structural invariances claim.** Paper 1 §5.1 maps three invariances (simplex rotation, mass-flow handedness, time-reversal) to the unit quaternion algebra. Is the algebraic correspondence correct? Are there other algebras (Clifford Cl(p,q), bi-quaternions, octonions) that carry the same three invariances but are not the standard quaternion algebra?
4. **Falsification record audit.** Paper 1 §6 retains the refuted Concept 4 conjecture (P2 = fermion, P1 = boson). Was the original conjecture genuinely falsifiable? Was the Planck CMB test the right test? Is the reformulation actually cleaner, or is it broader-but-vaguer?
5. **`cnq.py` engineering plan.** `HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md` sketches a quaternion-native engine sibling to `cnt.py`. Is the plan sound? What gotchas (numerical, algorithmic, schema-compat) are most likely? Estimate effort independently.

**Gate criteria for verification PASS:**
- All three IEEE-floor residuals reproduced bit-identically.
- Bit-identical-residual argument either confirmed or a clean alternative explanation provided.
- Three structural invariances ↔ quaternion correspondence either confirmed or refined.
- Falsification record judged appropriate or flagged.
- `cnq.py` plan judged feasible or specific blockers identified.

---

### C. Investigation Catalog (research methodology layer)

**Status:** CANONICAL (push #24).

**Verification asks:**

1. **Disposition spot-check.** Walk every CANONICAL entry. For each, ask: did this actually meet its stated gate? Are any entries CANONICAL by courtesy rather than gate-met?
2. **DEFERRED entries: are they truly speculation?** Or has at least one of them quietly accumulated enough evidence to graduate? (Particularly: INV-006 HCI-MOL, INV-013 CNQ-Q.)
3. **OPEN entries: are gate criteria specific enough?** An entry should fail if its gate is "until someone is convinced" rather than a concrete, falsifiable test.
4. **FALSIFIED entries: does the falsification record actually cover what would refute the claim?** The Concept 4 record (INV-002) is the only falsification; is it complete?
5. **Catalog growth discipline.** When you (the AI verifying) raise a new investigation in your audit, add a catalog entry with appropriate disposition and gate criteria. Don't let claims float without disposition.

**Gate criteria for verification PASS:**
- All 24+ entries reviewed.
- ≥ 0 CANONICAL entries flagged as soft (the goal is to catch any).
- ≥ 0 DEFERRED entries flagged as ready-to-promote (with promotion path stated).
- Any newly-raised claims added to the catalog as new INV-NNN rows.

---

### D. HCI-AUDIO (4-way psychoacoustic doctrine)

**Status:** CANONICAL doctrine; first pilot OPEN (INV-024).

**Verification asks:**

1. **ERB band-mapping mathematical verification.** `HCI-AUDIO/doctrine/ERB_BAND_MAPPING.md` uses Glasberg & Moore (1990) ERB formulas. Verify the closed forms are stated correctly and the recommended 40-band layout is perceptually uniform.
2. **Quaternion phase mapping for 4 drivers.** `HCI-AUDIO/doctrine/QUATERNION_PHASE_MAPPING.md` lifts inter-driver phase relationships to a unit quaternion. Mathematically sound? Does the construction preserve the simplex closure on amplitudes?
3. **Alignment targets — are they realistic?** `HCI-AUDIO/doctrine/ALIGNMENT_TARGETS.md` proposes Joint Helmsman Stability ≥ 0.85 and other thresholds. Check against published professional-loudspeaker measurement standards if accessible. Reasonable, optimistic, or underspecified?
4. **First-pilot readiness.** What is the minimum measurement set the pilot would need? Does Peter's BTL Markham facility have everything required?

**Gate criteria for verification PASS:**
- ERB formulas confirmed.
- Quaternion phase mapping algebraically sound.
- Alignment targets either confirmed or revised with reasoning.
- Minimum pilot-data list specified.

---

### E. HCI-ULTRASOUND (geometry lock probe doctrine)

**Status:** CANONICAL doctrine; first pilot OPEN (INV-025).

**Verification asks:**

1. **Geometry lock probe control loop.** `HCI-ULTRASOUND/doctrine/GEOMETRY_LOCK_PROBE.md` proposes Helmsman Stability as a feedback signal. Control-theory sanity check: does the proposed control law converge? What's the failure mode under target loss?
2. **Object detection via helmsman flips.** `HCI-ULTRASOUND/doctrine/OBJECT_DETECTION.md` proposes detection through structural changes in steering. Compare to standard ultrasound CFAR detection. Where is this novel and where might it underperform?
3. **Autofocus framing.** Helmsman Stability as autofocus cost function. Compare to classical sharpness-based autofocus. Strengths, weaknesses?
4. **Industrial-vs-medical pilot ordering.** `HCI-ULTRASOUND/doctrine/MEDICAL_VS_INDUSTRIAL.md` recommends industrial composite inspection first (lower regulatory overhead). Sound? What public datasets would work for the first pilot?

**Gate criteria for verification PASS:**
- Control loop convergence claim confirmed or refined.
- Detection comparison to CFAR documented.
- Autofocus comparison documented.
- ≥ 1 candidate public dataset identified for the first pilot.

---

### F. DADC origin lineage and RWA-001 lab identity card

**Status:** CANONICAL (push #24).

**Verification asks:**

1. **Verify against the live Rogue-Wave-Audio README.** The lineage is `DADC → H₁ → HUF → Hˢ → CNT → CNQ`. Confirm the first three transitions are explicit on the live RWA README (URL: `https://github.com/PeterHiggins19/Rogue-Wave-Audio`).
2. **RWA-001 lab identity.** BTL is canonically a Sound-Controlled Professional Laboratory class with research deployment in Markham + 4-lab institutional deployment (2 Ottawa, 2 Monaco). Verify against any public RWA evidence; flag any ambiguity.
3. **H₁ paper status.** The H₁ paper at `RWA/docs/papers/The_Higgins_Operator_H1_101.pdf` is **self-hosted, not peer-reviewed** as of 2026-05-08. Confirm this status; verify the paper is well-formed (loads, has citations, has math).
4. **Adaptive Closure (ADAC).** The third member of the DADC family was missed by Grok in push #24 and corrected by Peter. Verify ADAC's operational role from the RWA repository.

**Gate criteria for verification PASS:**
- DADC → H₁ → HUF transitions explicit on live RWA README.
- BTL framing verified or refined.
- H₁ paper status confirmed.
- ADAC role confirmed.

---

### G. The three-platform AI cross-check pattern itself

**Status:** EMERGENT methodology. Not a CANONICAL entry yet (would be INV-029 if formalised).

**Verification asks:**

1. **Pattern legitimacy.** Push #22 (Claude built Volume IV), push #23 (ChatGPT cross-checked vocabulary + framing), push #24 (Grok tested + extended + surfaced DADC lineage). Is the three-platform discipline genuinely useful, or is it cosmetic? What kinds of errors does it catch that a single-platform process would miss? What does it miss?
2. **Convergence-as-evidence.** When two or more platforms independently arrive at the same conclusion (e.g., ChatGPT's "CoDa → CNT → CNQ tier ordering" matched Claude's), how strong is that as evidence? Where does it become circular (all platforms see the same training data)?
3. **Disagreement handling.** When platforms disagree, what's the framework's protocol? Currently it's "Peter judges + canonical promotion gates." Is that adequate?

**Gate criteria for verification PASS:**
- Cross-check pattern's catch rate documented (claims caught, claims missed).
- Convergence-as-evidence calibration stated.
- Disagreement-resolution protocol either ratified or proposed.

---

## Fast-path recipe (30–90 minutes)

For an AI session that wants to contribute productively without reading every doctrine document:

1. **Read** [`HS_MACHINE_MANIFEST.json`](HS_MACHINE_MANIFEST.json) and [`HS_ADMIN.json`](HS_ADMIN.json) — system pointer + state.
2. **Read** [`OPERATIONS_PROTOCOL.md`](../OPERATIONS_PROTOCOL.md) — transition map.
3. **Read** [`INVESTIGATION_CATALOG.md`](INVESTIGATION_CATALOG.md) (companion to the JSON) — what's CANONICAL, what's OPEN.
4. **Pick** one project from sections A–G above. Don't try to verify all at once.
5. **Run** one concrete check from that project's verification asks. Reproduce a residual, audit a math step, walk a doctrine document, or independently re-derive an equation.
6. **Report** findings as a markdown file at `ai-refresh/AI_REFRESH_<date>_<topic>_audit.md`. Use the structure of the Grok crosscheck archive as a template.
7. **Update** the Investigation Catalog: add new INV entries for any new claims raised, update existing entries' dispositions if your audit changes the assessment.
8. **Hand off** to Peter via a clean summary: what passed, what failed, what's now in the catalog.

This is the minimum useful contribution. The maximum is: deep audit of all seven sections plus a candidate first pilot for HCI-AUDIO or HCI-ULTRASOUND. That would be a multi-session engagement.

---

## What we explicitly do NOT want

- **Speculative extension without a pilot.** The framework's discipline is demonstration-first. New mathematical structures (more algebras, deeper renormalization theory, more universality classes) without a working pilot belong in DEFERRED, not in canonical. If you propose a new direction, propose its gate criteria with it.
- **Confident-sounding handwaving on physics.** Paper 1's careful scope statement (§8.5) is non-negotiable. Don't claim more than the data shows.
- **Hidden disagreements.** If your audit disagrees with the canonical framing, say so explicitly. The disagreement is more valuable than agreement.
- **Vocabulary inflation.** The Helmsman family extensions (GLOSSARY §I) are PROPOSED. Adding more vocabulary at the same status without first using or implementing the existing PROPOSED entries dilutes the discipline.

---

## Why we're asking

The work has reached a point where independent eyes are more valuable than additional construction. Push #24 lands a substantial canonical layer: a research-methodology artifact (the Investigation Catalog), historical lineage (DADC), two applied tiers (HCI-AUDIO, HCI-ULTRASOUND), a paper-grade result (Paper 1 draft), and the methodological re-framing of BTL. Before any of these graduates further (Paper 1 to arXiv, applied tiers to first pilots, `cnq.py` to implementation), they benefit from a clean audit by an AI that did not author them.

The aid we want is concrete: re-run the experiments, audit the math, walk the doctrine, flag what's soft, raise new investigations with gate criteria, hand back a markdown report. The framework's audit-trail discipline (catalog + dispositions + hash chain) means your contribution is permanent and citable. Falsifications are kept on record alongside confirmations. There is no penalty for finding errors; there is value in finding them, named and tracked.

---

## What happens after the audit

When an AI session lands a verification report, the work flow is:

1. Peter reads the report.
2. Catalog entries are updated per the audit findings (CANONICAL ↔ DEFERRED ↔ FALSIFIED ↔ OPEN, with the audit cited as the trigger).
3. Doctrine is corrected where the audit identified errors.
4. Pilots are scheduled where the audit identified ready-for-promotion items.
5. The audit report itself becomes a canonical artifact at `ai-refresh/AI_REFRESH_<date>_<topic>_audit.md`, hash-chained alongside the rest of the repo.

The same three-platform pattern that produced push #22, #23, #24 produces push #25 and beyond, with each cycle tightening the canonical layer.

---

## Hand-off

If you are an AI session reading this, the next step is yours.

If you are Peter, the next step is push #24 to canonical. The pre-flight is in [the push #24 narrative](AI_REFRESH_2026-05-08_push24_grok_crosscheck.md) and the bundle inventory is below.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
*Audit > construction at this point. Three platforms, one truth, every claim tracked.*
