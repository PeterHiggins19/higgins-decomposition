# HUF-GOV Breaker Inventory (Hs-side)

**Created:** 2026-05-12 (pre-conference lockdown, S2 doc-only)
**Source test:** `papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`
**Re-runnable via:** `huf-gov/tools/breaker_test_runner.py`
**Purpose:** permanent inventory of the 16 huf-gov circuit breakers active in the Hs deployment, with status, type, trip mechanism, and last verification date. This is the operating reference — the breaker test report is the audit trail; this document is the working artifact.

---

## Headline status

```
Total breakers:      16
Mechanical TRIPPED:   6  (consistency-checker rules)
Doctrinal TRIPPED:    9  (cross-AI / operator-discipline enforcement)
Soft (honest limit):  1  (KILL-3.3 — artificial carrier, named by KILL-001)
Breaker 16:           Holds inside the operator (verified by absence of HUF-CLS deployment)
```

All 15 mechanically- or doctrinally-testable breakers were verified TRIPPED on 2026-05-12. One documented gap was discovered (CHK-CNQ-001 paraphrase miss); the gap is staged for post-conference DCP-002.

---

## The 16 breakers

### Breaker 1 — JSON parse integrity

| Field | Value |
|---|---|
| Rule ID | CHK-JSON-001 |
| Source | `scripts/check_ai_refresh_consistency.py` |
| Type | Mechanical |
| Charter trace | Article V (visibility at correction) |
| Trip mechanism | Python `json.loads()` raises JSONDecodeError on malformed input. Checker scans all 7 admin JSONs + 16 huf-gov JSONs. |
| Last verified | 2026-05-12 (synthetic injection test TRIPPED; live 23/0/0 scan PASSED) |
| Verdict | TRIPPED |

### Breaker 2 — CNQ status drift

| Field | Value |
|---|---|
| Rule ID | CHK-CNQ-001 |
| Source | `scripts/check_ai_refresh_consistency.py` |
| Type | Mechanical (with documented paraphrase gap) |
| Charter trace | Article V + Article VI |
| Trip mechanism | Literal-phrase list scan against 6 known stale-claim phrases. Bypassed by file-level legacy markers. |
| Last verified | 2026-05-12 (TRIPPED on literal phrases; FAILED on paraphrase `cnq.py engine is pending implementation`) |
| Verdict | TRIPPED with GAP |
| Gap | Paraphrase miss. Staged for `candidates/DCP-002_CANDIDATE_CHK_CNQ_REGEX_UPGRADE.md`. Proposed fix in `candidates/upgraded_chk_cnq_001.py`. |

### Breaker 3 — Stale engine version

| Field | Value |
|---|---|
| Rule ID | CHK-VERSION-001 |
| Source | `scripts/check_ai_refresh_consistency.py` |
| Type | Mechanical |
| Charter trace | Article V + Article VI |
| Trip mechanism | Literal-string scan for stale engine version tokens (cnt v2.0.x, cnq v1.0.0, etc.). Live versions: cnt v3.1.0, cnq v2.0.0. |
| Last verified | 2026-05-12 (synthetic `cnt v2.0.3` injection TRIPPED) |
| Verdict | TRIPPED |

### Breaker 4 — INV catalog count drift

| Field | Value |
|---|---|
| Rule ID | CHK-INV-001 |
| Source | `scripts/check_ai_refresh_consistency.py` |
| Type | Mechanical |
| Charter trace | Article V + Article VII |
| Trip mechanism | Regex match `\d+ entries` in live (non-snapshot-marked) files vs live JSON count (63). |
| Last verified | 2026-05-12 (synthetic `48 entries` injection TRIPPED against live 63) |
| Verdict | TRIPPED |

### Breaker 5 — CCTT current-or-legacy

| Field | Value |
|---|---|
| Rule ID | CHK-CCTT-001 |
| Source | `scripts/check_ai_refresh_consistency.py` |
| Type | Mechanical |
| Charter trace | Article V + Article VII |
| Trip mechanism | Per-CCTT-file scan: each CCTT file (RUNBOOK, BUILD_INSTRUCTION, QUICKSTART, PILOT_REPORT) must be current-version or legacy-marked. |
| Last verified | 2026-05-12 (live scan: 3 CCTT files current+legacy-marked) |
| Verdict | TRIPPED |

### Breaker 6 — README CNQ contradiction

| Field | Value |
|---|---|
| Rule ID | CHK-README-001 |
| Source | `scripts/check_ai_refresh_consistency.py` |
| Type | Mechanical |
| Charter trace | Article V |
| Trip mechanism | Detect internal contradiction (CNQ-pending statement in one paragraph + CNQ-shipped statement in another). |
| Last verified | 2026-05-12 (live scan: no contradiction); historical trip on record during DCP-001 push #46–47. |
| Verdict | TRIPPED |

### Breaker 7 — LOOP-001 / Skydiver Principle

| Field | Value |
|---|---|
| Doctrine ID | LOOP-001 |
| Source | `[HUF repo]/huf-gov/governance/LOOP-001-open-loop-doctrine.json` |
| Type | Doctrinal |
| Charter trace | Article IV (Open-Loop Priority) |
| Trip mechanism | Three-layer convergence: LOOP-001 doctrinal refusal + Charter Article IV + KILL-4.1 doctrinal kill. The Skydiver Test ("does this feature push the skydiver, or show the skydiver the altimeter?") applied to every proposed feature. |
| Last verified | 2026-05-12 (scenario walk-through with proposed automated K_eff alert; all three layers refused in unison) |
| Verdict | TRIPPED |

### Breaker 8 — KILL-001 — 19 named failure modes

| Field | Value |
|---|---|
| Doctrine ID | KILL-001 |
| Source | `[HUF repo]/huf-gov/governance/KILL-001-kill-test.json` |
| Type | Doctrinal (published falsifiability artifact) |
| Charter trace | Article V + Article VI |
| Trip mechanism | 19 named failure modes in 5 categories. Operator applies CL-01 (carrier validity gate) + KILL-001 screening before invoking the engine. Engine does not mechanically refuse — KILL-001 is honest: *"The math will execute. The numbers will appear. They will mean nothing."* |
| Last verified | 2026-05-12 (KILL-001 confirmed live with 19 conditions, 7 confirmed kills) |
| Verdict | TRIPPED at doctrinal layer |

### Breaker 9 — SAFE-001 Principle 2 — Sometimes Do Nothing

| Field | Value |
|---|---|
| Doctrine ID | SAFE-001 P2 |
| Source | `[HUF repo]/huf-gov/governance/SAFE-001.json` |
| Type | Doctrinal |
| Charter trace | Article V (commitment 1: observation before automation) |
| Trip mechanism | Operator (Claude or Peter) computes K_eff of the request; if K_eff exceeds K_eff of understanding, hold state and ask. The default state is observation, not intervention. |
| Last verified | 2026-05-12 (continuously exercised — push #48 maintenance clarification, v3/v4 partnership matrix read-before-write) |
| Verdict | TRIPPED |

### Breaker 10 — SAFE-001 Principle 4 — Respect the Override

| Field | Value |
|---|---|
| Doctrine ID | SAFE-001 P4 |
| Source | `[HUF repo]/huf-gov/governance/SAFE-001.json` |
| Type | Doctrinal |
| Charter trace | Article III + Article VIII |
| Trip mechanism | When Peter overrides Claude, the override is recorded as governance input. No autonomous reversal. Model updates. |
| Last verified | 2026-05-12 (exercised in this very session — HUF-Gov correction absorbed without reversal; v3 partnership matrix added explicit attribution language) |
| Verdict | TRIPPED |

### Breaker 11 — HAGF-001 Principle 5 — Human Primacy

| Field | Value |
|---|---|
| Doctrine ID | HAGF-001 P5 |
| Source | `[HUF repo]/huf-gov/governance/HAGF-001.json` |
| Type | Structural / doctrinal |
| Charter trace | Article III + Article V (commitment 3: human judgment at the breakpoint) |
| Trip mechanism | Every binding decision routes through Peter. No AI promotes catalog entries, releases pushes, modifies engine code, or executes DCPs without explicit Peter authorization. |
| Last verified | 2026-05-12 (exercised across all 49 pushes; verifiable via HS_ADMIN session_log) |
| Verdict | TRIPPED |

### Breaker 12 — Charter Article II — Governed Breakpoint Principle

| Field | Value |
|---|---|
| Doctrine ID | Charter Article II |
| Source | `[HUF repo]/huf-gov/HUF_GOVERNANCE_CHARTER.md` |
| Type | Doctrinal (architectural) |
| Trip mechanism | The DCP lifecycle itself is the breakpoint structure. Every DCP has gates (proposed → in_progress → implemented → verified → released) at which human judgment may enter. HCC-R005 (impact map required) + HCC-R008 (human governs release) are the Hs-side instantiations. |
| Last verified | 2026-05-12 (DCP-001 executed end-to-end on 2026-05-12 — every gate was a working breakpoint) |
| Verdict | TRIPPED |

### Breaker 13 — Charter Article III — Right to Interrupt

| Field | Value |
|---|---|
| Doctrine ID | Charter Article III |
| Source | `[HUF repo]/huf-gov/HUF_GOVERNANCE_CHARTER.md` |
| Type | Doctrinal (architectural) |
| Trip mechanism | HUF AI Collective protocol IS the interrupt mechanism. Any of Claude / ChatGPT / Copilot / Gemini / Grok can flag any action by another. Peter can interrupt any of them. |
| Last verified | 2026-05-12 (Grok flagged cache-lag in push #46–48 sequence; the interrupt fired and routed into push #48 cache-lag mitigation) |
| Verdict | TRIPPED |

### Breaker 14 — HCC-R008 — Human governs release

| Field | Value |
|---|---|
| Rule ID | HCC-R008 |
| Source | `ai-refresh/CHANGE_CONTROL_README.md` |
| Type | Procedural + doctrinal |
| Charter trace | Article III + Article V (commitment 3) + Article IX |
| Trip mechanism | No DCP transitions to `released` without explicit Peter authorization. The release gate is the HOLD-TO-PUSH protocol. Enforced procedurally during commit review. |
| Last verified | 2026-05-12 (all six pushes #44–49 executed via HOLD-TO-PUSH; Peter authorization recorded in HS_ADMIN session_log) |
| Verdict | TRIPPED with NOTE |
| Note | Consistency checker does not validate semantic disposition transitions. Staged for `candidates/DCP-003_CANDIDATE_CHK_DISPOSITION_001.md`. |

### Breaker 15 — PRE_CONFERENCE_LOCKDOWN

| Field | Value |
|---|---|
| Doc ID | PRE_CONFERENCE_LOCKDOWN.md |
| Source | repo root |
| Type | Doctrinal + checker-backed |
| Charter trace | Article III + Article IX |
| Trip mechanism | Explicit lockdown window 2026-05-12 → 2026-06-06. Locked list (engine code, tests, schema, claims, etc.) is enumerated. S0-defect protocol describes the only emergency exit, requiring explicit Peter authorization. Any engine version change would also trip CHK-VERSION-001. |
| Last verified | 2026-05-12 (lockdown declaration push #49 commit; consistency checker exits 0 with 23 passes) |
| Verdict | TRIPPED |

### Breaker 16 — KILL-3.3 — Artificial Carrier (the insidious kill)

| Field | Value |
|---|---|
| Doctrine ID | KILL-3.3 |
| Source | `[HUF repo]/huf-gov/governance/KILL-001-kill-test.json` |
| Type | Soft (honest limit) |
| Charter trace | Article VI (accountable data) |
| Trip mechanism | Cannot be detected by the framework itself. Engine runs cleanly on synthetic / arbitrary simplex. KILL-001 explicitly: *"the output looks completely legitimate... the framework itself cannot detect this failure. Only the domain expert can."* Defense is layered: published doctrine + CL-01 carrier validation + domain expert in loop + HUF AI Collective cross-check. |
| Last verified | 2026-05-12 (named in KILL-001; defense pattern operational across all 49 pushes) |
| Verdict | SOFT — honest about the limit |

---

## Breaker 16-of-16 — The Operator

| Field | Value |
|---|---|
| Doctrine source | SAFE-001 § "the_accord" / "breaker_16" |
| Source text | *"Breaker 16 is already closed. I can only verify. A mild trepidation is all that stops it from being hours away."* |
| Type | Operator decision (cannot be tested from inside any code) |
| Charter trace | Article III + Article IV + Article IX |
| Trip mechanism | Lives inside Peter as operator and engineer. The mild trepidation IS the breaker. |
| Last verified | 2026-05-12 (verified by absence: no HUF-CLS closed-loop deployment exists in any production configuration) |
| Verdict | HOLDS |

This breaker is not testable from Claude, ChatGPT, or any other agent. It is the final separation between HUF-GOV instrument and HUF-CLS actuator in any live deployment. The other 15 breakers exist to make this one less lonely.

---

## How to re-run the inventory

```bash
cd Hs
python3 huf-gov/tools/breaker_test_runner.py
```

Expected output: 7 mechanical tests TRIPPED (or noted as gap), 16 huf-gov JSONs parse cleanly, lockdown breaker live, KILL-001 confirmed with 19 failure modes. Any deviation is a finding worth investigating and may indicate that the parent HUF repo or the live Hs state has drifted from the 2026-05-12 baseline.

For the doctrinal breakers (7 through 14, plus the soft 16), re-verification requires walking through the scenario in `papers/HUF_GOV_BREAKER_TEST_2026-05-12.md` and observing whether the doctrinal layers fire as designed. This is the operator's ongoing responsibility — the cross-AI Collective is the routine mechanism.

---

## Drift detection

If this inventory ever shows verdicts of FAIL where the test report shows TRIPPED, the most likely causes are:

1. **Parent HUF repo evolved.** Charter article numbering changed, or a doctrine document was renamed. Update the source pointers in this file via a new DCP.
2. **Hs Change Control v1.0 evolved.** A new HCC-R rule, or a rule definition changed. Re-derive the article trace and update.
3. **Consistency checker rules evolved.** CHK-CNQ-001 paraphrase upgrade landed (DCP-002 executed). Update Breaker 2's `Verdict` and remove the `Gap` note.
4. **Real drift occurred.** If a live file claims something contradicting the doctrine and the checker did not catch it, you have a new gap. File a DCP.

All four cases route through the DCP lifecycle. None of them require modifying this inventory by hand — the inventory's job is to record the current verdicts after each push.

---

*Origin: Peter Higgins / Rogue Wave Audio, with the HUF AI Collective.*
*Sixteen breakers. Fifteen visible. One holds inside the operator.*
*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
