# Suspicion of Every Assumption — Anti-Specification Doctrine

**Doctrine ID:** SEA-1.0
**Adopted:** push #32 (2026-05-09)
**Authority:** project doctrine — applies to all HCI tiers, current and future
**Catalog reference:** INV-045
**Source:** Peter Higgins (push #32 directive)

---

## 1. The principle

> *"Suspicion of every assumption."*
> — Peter, push #32

For every public function, every output channel, every interpreted diagnostic, and every documented claim in the Hs framework, the author **enumerates the failure modes by which the artifact could fail to deliver its stated behaviour**, and **provides mitigation evidence** for each. The default presumption is that the artifact has failed; the author's job is to demonstrate, mode by mode, that it has not.

This inverts the conventional posture. Conventional development asks *"does this work?"* and answers with positive validation against good inputs. Anti-specification asks *"can I prove this does not fail?"* and answers by walking the failure space deliberately, dispatching each mode in turn.

The cycle time on bug discovery collapses from weeks (waiting for external auditors) to hours (during construction). The discovered failures of CNQ v1.0.0 — the NaN-in-hash at T<2, the D=2 schema mismatch, the R `canonical_dumps` not sorting keys, the `metadata.reference_implementation` parity-break, the `extract_cnt_diagnostics` path-mismatch, the corrupted file-tail — are exactly the kind of thing this method surfaces during construction, not after launch.

## 2. Why this discipline matters

**Asymmetry of search spaces.** The space of positive cases is small. The space of failure modes is much larger — for any real system the failure space is effectively infinite. Conventional testing samples the positive space and waits for the failure space to surface complaints. Anti-specification deliberately enumerates the failure space, dispatching what is enumerable and acknowledging the residue.

**Reframe of self-criticism.** The hardest part is not the enumeration but the willingness to treat one's own work as guilty until proven innocent. Most authors resist that posture. The pragmatic reframe is that each enumerated failure mode is a small mystery to either solve (mitigation found and proven) or document honestly (acknowledged limitation). The completed document is not a confession of weakness; it is a declaration that the author has entered every dark corner and turned the lights on.

**External-audit posture.** When a reviewer (ChatGPT, Grok, a CoDa-community auditor, a paper-1 referee) opens the project, an existing anti-specification document signals that the obvious problems have been catalogued and dispatched. Their work shifts from finding obvious failures to finding non-obvious ones — which is what external audit is *for*. The collaboration becomes complementary instead of redundant.

## 3. Scope — what the doctrine governs

The doctrine applies to:

- **Every engine** in the Hs framework: CNT v3, CNQ v2, future versions, future engines.
- **Every wrapper** (`HCI-CNQ/wrappers/wrapper_*.json` and prose handbooks): audio, government-budget, geochemistry, ultrasound, future domains, future locales.
- **Every applied tier**: HCI-AUDIO, HCI-ULTRASOUND, future HCI-* tiers when they ship instruments.
- **Every published claim** (Paper 1, Paper 2, future papers): each numerical figure or interpretive claim is enumerated as a potential failure mode.
- **Every wrapper schema and engine schema**: the schema specification itself is subject to anti-specification (what could be misused; what could be misinterpreted; what could be silently broken).

The doctrine does not apply to:

- One-off exploratory scripts (`experiments/`-level work that is not part of a shipping artifact)
- Prose narrative documents (push narratives, GLOSSARY, NOTATION, design docs — these are subject to the lockedvocabulary and lineage discipline already, not to anti-specification)
- Tooling artifacts that are not part of the user-facing release surface (admin JSONs, internal utilities)

When in doubt, apply the doctrine. The cost of an extra anti-specification document is small; the cost of skipping it on a load-bearing artifact is reviewer humiliation.

## 4. Failure-mode taxonomy

Every entry in an anti-specification belongs to exactly one of ten categories. These categories are exhaustive for the failure space of a numerical-engineering artifact; if a candidate failure does not fit, the taxonomy itself needs revision (open an investigation with the catalog).

| Code | Category | Examples |
|---|---|---|
| **NUM** | Numerical | IEEE-floor exceeded, NaN/Inf propagation, overflow/underflow, precision loss, condition-number explosion |
| **ALG** | Algorithmic | Math is incorrect, theorem violated, convention drift (e.g., scalar-first vs scalar-last quaternion), index-off-by-one, tie-break inconsistency |
| **SCH** | Schema | Output does not match documented schema, optional fields missing, units inconsistent, type drift between Python and R |
| **INV** | Input validation | Invalid input accepted silently, valid input rejected, edge cases unhandled (T=1, D=2, all-zero, near-singular) |
| **INT** | Integration | Engine-to-engine adapter broken, CSV parsing wrong, subprocess invocation incorrect, file path drift, missing dependency |
| **INTP** | Interpretation | Output over-interpreted in claim, claim-strength too strong for evidence, scope drift in language, metaphorical math taken literally |
| **REP** | Reproducibility | Determinism contract broken within a language, hash drift across runs, dependency-version sensitivity, platform-specific behaviour |
| **WRP** | Wrapper | Wrapper does not translate engine output correctly, locale fallback wrong, calibration profile incomplete, alias paths stale |
| **DOC** | Documentation | Spec does not match implementation, locked vocabulary violated, lineage misrepresented, citation incorrect |
| **ADV** | Adversarial | Crafted input causes engine to crash or produce misleading output; tool misuse; pathological data distributions |

Each entry must declare its category in the structured record. Reviewers can then audit by category — for example, the CoDa community might focus on ALG and DOC; a security auditor on ADV; a numerical-analysis auditor on NUM and REP.

## 5. Evidence types

Every failure-mode entry must provide evidence that the failure does not occur (or occurs only under documented conditions). Acceptable evidence types:

| Code | Type | Meaning |
|---|---|---|
| **TEST** | Unit / integration test | A test exists that exercises the failure condition and asserts the correct behaviour. Reference: file path + test name. |
| **PROP** | Property test | Hypothesis-style property check covering a parametric class of inputs. Reference: file path + property name. |
| **PROOF** | Mathematical derivation | A short proof showing the failure cannot occur given the algorithm's structure. Reference: location of proof (in-source comment, design doc, paper). |
| **EMPR** | Empirical demonstration | A measurement on a real or synthetic dataset showing the failure condition does not arise. Reference: dataset + run output. |
| **STRC** | Structural argument | A code-review observation showing the failure cannot occur without changing source structure (e.g., "function never called with this input shape because of upstream type-check"). |
| **DESN** | Design constraint | The failure is prevented at the architectural level (e.g., engine independence prevents cross-engine hash drift by construction). |

A given failure mode may have multiple pieces of evidence stacked. More evidence types per entry = stronger discharge.

## 6. Residual-risk classification

After mitigation evidence, every entry classifies the remaining risk:

- **`none`** — Mitigation is rigorous; failure cannot occur. Example: input-validator rejects negative carriers before any math runs.
- **`bounded`** — Failure can occur, but consequences are limited and documented. Example: T<2 triggers degenerate code path that emits null residuals; downstream consumers handle null. The engine doesn't crash; it produces a schema-consistent degenerate output.
- **`unverified`** — Mitigation is believed adequate but has not been formally proven or fully tested. Action item: upgrade evidence before next release.
- **`acknowledged_limitation`** — The engine genuinely does not handle this case, and the documentation says so. Example: D=16 quad-quaternion factoring is schema-locked but not implemented in v2.0.0; calls raise `NotImplementedError`; documented in design doc §5.2.

`unverified` entries are tracked as open work; a release should aim for zero `unverified` entries on its load-bearing artifacts.

## 7. Per-engine workflow

For each engine release (initial or version bump), the author follows this workflow:

1. **Build the engine** with strict input validation, vectorised math, and schema-consistent output.
2. **Walk the failure-mode taxonomy** for each public function, output channel, and documented claim. For each: ask "could this fail in category NUM? in ALG? in SCH? ..." until the obvious candidates have been listed.
3. **For each candidate failure mode**, provide mitigation evidence (test, prop, proof, empr, strc, desn) and classify residual risk.
4. **Write the entries** to `<engine>/ANTI_SPECIFICATION.md` (human-readable) and `<engine>/verity.json` (machine-readable, conforming to `docs/verity_schema.json`).
5. **Run the verity check**: a script (`scripts/verify_verity.py`, future) confirms that every test referenced in `verity.json` exists and passes; every proof reference resolves; every dataset reference resolves.
6. **Hand to external review**: ChatGPT, Grok, or other auditors. They look for failures NOT in the document. New failures found by external review get added with their mitigation in the next push.

The release is **gated** on the verity check passing. Without an `ANTI_SPECIFICATION.md` and a verity.json showing zero `unverified` entries, the engine is not a candidate for promotion to load-bearing status.

## 8. Per-wrapper workflow

Wrappers are simpler artifacts but the discipline still applies. For each wrapper (data file + optional prose handbook):

1. List the engine output paths the wrapper translates (every entry in `field_aliases`).
2. For each entry, enumerate failure modes in WRP, INTP, DOC, and SCH categories: could the alias be stale? could the locale fallback misfire? could the calibration threshold be wrong for the domain? could the description over-promise the engine output's meaning?
3. Provide evidence (typically EMPR — "tested against a known-correct domain dataset" — or STRC — "alias paths verified against current engine schema").
4. Write to `<wrapper-tier>/ANTI_SPECIFICATION.md`.
5. External audit by domain experts (audio engineers for the audio wrapper; budget analysts for government-budget; etc.).

A wrapper that fails its anti-specification check is not promotable to "first instance" status (per the wrapper architecture in `ai-refresh/CNT_V3_CNQ_V2_DESIGN.md` §11).

## 9. Per-claim workflow (papers and public statements)

For Paper 1, Paper 2, future papers, and any public claim about engine behaviour:

1. List every numerical figure (e.g., the locked Planck residual `4.440892098500626e-16`).
2. For each figure: enumerate INTP failure modes — could a reader interpret this figure more strongly than warranted? Could the figure's claim-strength be exceeded? Could the figure be cited out of context?
3. List every interpretive claim (e.g., "CNT measures invariance, CNQ names the algebra it lives in").
4. For each claim: enumerate DOC and INTP failure modes — could the claim be paraphrased into a stronger or different statement that is not supported by the engine?
5. Mitigations include the locked vocabulary, the lineage doctrine, and the explicit claim-strength language in Paper 1's Appendix A.
6. Write to `papers/<paper-id>/ANTI_SPECIFICATION.md`.

The Paper 1 anti-specification is part of the arXiv submission package.

## 10. Integration with existing doctrine

This doctrine is additive to and compatible with:

- **OPERATIONS_PROTOCOL.md** — the Gawande-style meta-checklist for transitions. SEA adds an anti-specification step to the engine-release checklist.
- **The priority lock** — basics-first ordering. SEA does not displace priority; it sharpens what counts as "basics complete."
- **The engine-independence policy** (push #32) — each engine has its own anti-specification; cross-engine assumptions are explicitly marked as INT-category failure modes.
- **The wrapper architecture** — wrappers have their own anti-specifications; the wrapper schema is itself anti-specified.
- **The lineage doctrine** — "each arrow is a generalisation, not a replacement." Anti-specification entries that reference older versions (e.g., "CNQ v1.0.0 had this failure mode; CNQ v2.0.0 fixes it via mitigation X") preserve the lineage.

## 11. The cycle of self-suspicion

Each anti-specification document is a snapshot, not a final certification. The cycle is:

1. **Author lists failure modes** they can think of (the productive irritant).
2. **External reviewer finds modes** the author missed (CoDa community, ChatGPT, Grok, audio engineer, budget analyst).
3. **Author dispatches new modes** with mitigation; bumps the document version.
4. **Repeat** at every release, every wrapper extension, every applied pilot.

Anti-specification is not a one-time gate; it is a **living discipline**. The verity.json schema includes a `last_audited` timestamp and a `next_audit_due` timestamp. Auditing cadence is suggested at every minor release for engines and at every domain extension for wrappers.

## 12. The principle, recapitulated

> *"Assume it has failed and prove it works by exhausting failure modes mathematically."*
> — Peter, push #32

The engine does not get the benefit of the doubt. The author's job is to remove every reasonable doubt one entry at a time. What remains, after that walk, is a document that says: "I have looked here, here, here, and here, and these are the things that did not break, with evidence; these are the things that broke and were fixed, with evidence; these are the things that remain limitations, honestly stated. The rest of the failure space is for the next reviewer."

That document is the engine's earned credibility, not its claim of perfection.

---

**Status:** doctrine adopted push #32. Applies to CNT v3, CNQ v2, audio wrapper v1, government-budget wrapper v0.1, and all future HCI artifacts.

**See also:**
- `docs/verity_schema.json` — machine-readable schema for verity.json files
- `HCI-CNQ/engine/ANTI_SPECIFICATION.md` — first instance, populated during Phase C2 of push #32
- `HCI-CNT/engine/ANTI_SPECIFICATION.md` — second instance, populated during Phase C1 of push #32
- `OPERATIONS_PROTOCOL.md` — integration of the SEA workflow step
- `ai-refresh/INVESTIGATION_CATALOG.json` — INV-045 records the doctrine adoption
