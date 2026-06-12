# DCP-003 CANDIDATE — Add CHK-DISPOSITION-001 catalog disposition transition validation

**Status:** **proposed** — staged in advance per pre-conference lockdown allowed-actions list. NOT executed during lockdown. First post-conference push window (opens 2026-06-06) is the earliest execution window.
**Severity:** S3 (interface or AI-current-state change — adds new rule to the consistency checker interface)
**Filed by:** Claude (Opus 4.6) at Peter directive 2026-05-12 *"update huf-gov within hs to Claude determined optimum fixes as suggested"*
**Authorizing parent doctrine:** HUF Governance Charter Article VII (accountable resolution) + HAGF-001 Principle 5 (human primacy)
**Reference implementation:** specification only in this document; concrete code lands during DCP execution.

---

## Why this DCP exists

The 2026-05-12 breaker test of HCC-R008 (human governs release) surfaced a small enforcement gap: the consistency checker currently does not validate that any Investigation Catalog disposition change (e.g., STAGED → CANONICAL, OPEN → DEFERRED) is logged in HS_ADMIN session_log against a corresponding DCP entry. The procedural breaker fires reliably — Peter sees disposition changes during commit review — but a malicious or accidental autonomous disposition change could in principle slip through if commit review is rushed.

Per the breaker test report:

> **Verdict: TRIPPED with NOTE.** Procedural enforcement works. The consistency checker could be extended to verify that any catalog disposition change is logged in HS_ADMIN session_log against a DCP entry — that would close the gap.

This DCP closes that gap by adding a new mechanical rule.

---

## What the DCP does

**Add** a new rule `CHK-DISPOSITION-001` to `scripts/check_ai_refresh_consistency.py` that:

1. **Reads** the current state of `ai-refresh/INVESTIGATION_CATALOG.json` and extracts every INV entry's current `disposition` and `last_modified_push` (or equivalent provenance field).
2. **Reads** `ai-refresh/HS_ADMIN.json` session_log entries.
3. **Reads** `ai-refresh/change_packets/*.json` for active DCP filings.
4. **Cross-references** every disposition that differs from a snapshot baseline against a session_log entry naming that INV id, AND against a DCP entry that lists the INV id in its scope.
5. **Trips on:**
   - Disposition value that doesn't match the disposition recorded in the corresponding session_log entry
   - Disposition value with no corresponding session_log entry at all (orphan change)
   - Disposition value where the session_log entry exists but no DCP entry references the INV id (procedural skip)

**Baseline snapshot.** The rule requires a comparable previous state. Options:

- **Option A (simpler):** maintain a file `ai-refresh/INVESTIGATION_CATALOG_BASELINE_SHA.txt` containing the SHA-256 of the last `released`-verified INV catalog. The rule checks current state against this baseline.
- **Option B (more thorough):** maintain a separate `ai-refresh/INVESTIGATION_DISPOSITION_HISTORY.json` log that records every disposition change over time. The rule checks for unauthorized transitions.

Option A is leaner and fits the existing checker style. Option B would be cleaner long-term but requires a larger DCP. **Recommendation:** start with Option A in DCP-003. Defer Option B to a future DCP if Option A proves insufficient.

---

## Impact map (HCC-R005 required)

**Files modified.**

1. `scripts/check_ai_refresh_consistency.py` — add new rule function `_check_disposition_transitions()` returning Pass/Warning/Error per INV entry.
2. `ai-refresh/INVESTIGATION_CATALOG_BASELINE_SHA.txt` — new file containing the baseline SHA. Initially populated with the SHA-256 of the current `released`-verified INV catalog at the time of DCP-003 execution.

**Files NOT modified.**

- `ai-refresh/INVESTIGATION_CATALOG.json` — content unchanged; rule reads it.
- `ai-refresh/HS_ADMIN.json` — content unchanged; rule reads it.
- `ai-refresh/CHANGE_PACKET_TEMPLATE.json` — content unchanged; rule reads filed packets.
- No engine code, no schema, no claim-strength changes.

**Downstream consumers of the rule.**

- DCP lifecycle: any future DCP that promotes / demotes / changes an INV entry's disposition will trigger CHK-DISPOSITION-001 on the next checker run. The DCP must reference the INV id explicitly in its scope or the rule trips.
- HUF AI Collective: AIs reading checker output will see a new rule ID + new error class. AI_AGENTS.md should be updated to reference CHK-DISPOSITION-001 in §2.1 grounding test.
- Cross-check archive: future archive entries can cite the rule by ID.

**Reversion path.** If the rule produces unexpected false positives (likely scenarios: disposition changes during routine catalog cleanup; minor disposition corrections that don't warrant a full DCP), revert by removing the rule function from the checker. The baseline file remains as historical record.

---

## Verification criteria (HCC-R007)

Before transitioning DCP-003 from `implemented` to `verified`:

1. **Live checker exits 0 on the current repo state after baseline is set.** Run with baseline = current state; rule reports 0 disposition transitions (all clean).
2. **Synthetic transition test trips correctly.** Manually edit a test copy of INV catalog to flip one INV from STAGED to CANONICAL without a corresponding session_log entry; rule must trip and report the orphan transition.
3. **Authorized transition passes.** Manually edit test copy + add corresponding session_log entry referencing the INV id + add DCP entry naming the INV in scope; rule must pass.
4. **No new false positives in live state.** Re-run on full Hs repo; pass count must equal or exceed pre-DCP baseline (currently 23 with DCP-002 expected to add 0 or 1).
5. **AI_AGENTS.md updated.** The grounding-test section reflects the new rule.

---

## Why this is a candidate, not an active DCP

Same lockdown reasoning as DCP-002:

> **ALLOWED during lockdown:**
> - DCP filing at `proposed` status (no execution)

This filing satisfies that allowance. The DCP is:

- **Filed** at `proposed` status in this candidate document.
- **NOT advanced** (no scripts/check_ai_refresh_consistency.py modification).
- **NOT executed** (no rule code added during lockdown).

When the lockdown clears 2026-06-06, this candidate document can be:

1. Read by the operator.
2. Copied into `ai-refresh/change_packets/DCP-003_CHK_DISPOSITION_001.json` in proper DCP JSON format.
3. Advanced through the standard DCP lifecycle.

---

## Estimated execution effort

- **Reading prep:** ~15 minutes (re-read this candidate doc; review existing checker patterns).
- **Implementation:** ~60 minutes (write the new rule function with Option A baseline; populate baseline file; integrate into checker; write unit tests).
- **Verification:** ~30 minutes (run synthetic-transition tests; confirm live state stays clean; update AI_AGENTS.md).
- **Documentation update:** ~15 minutes (update `BREAKER_INVENTORY.md` to remove the "NOTE" from Breaker 14; update HS_FAST_REFRESH.json with new rule reference).
- **Total:** ~2 hours from candidate-read to released.

Fits comfortably inside a single post-conference push. Could be bundled with DCP-002 in the same push if desired (DCP-002 is ~70 min; DCP-003 is ~2 hours; together ~3 hours — sound).

---

## Edge cases to handle

1. **Catalog count change with NO disposition change.** If 64 entries appear where 63 existed and all 63 prior entries preserve their dispositions, the rule should not trip on the existing 63. Only the new entry needs verification. The rule's baseline comparison should be per-INV-id, not over-aggregated.
2. **Catalog count change with disposition change.** A new entry (e.g., INV-064) appears with disposition STAGED. The session_log must reference its creation in a DCP scope. If yes, rule passes; if no, rule trips.
3. **Removed entries.** If an entry is deleted from the catalog (CLOSED with archive only, or genuine deletion), the rule should treat this as a disposition transition to "deleted" and require a session_log entry. Edge case worth testing.
4. **Bulk catalog reorganization.** If a future push restructures the catalog (e.g., re-IDs entries), the rule may produce many trips. Handle by allowing a `--baseline-reset` flag that resets the baseline SHA after Peter authorization.

---

## Related items

- **`Hs/huf-gov/candidates/DCP-002_CANDIDATE_CHK_CNQ_REGEX_UPGRADE.md`** — companion DCP for paraphrase upgrade.
- **`papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`** — original breaker test that surfaced the disposition-validation gap.
- **`scripts/check_ai_refresh_consistency.py`** — current checker (untouched during lockdown).
- **`ai-refresh/INVESTIGATION_CATALOG.json`** — current catalog (63 entries; current dispositions 33/8/12/8/1/1).
- **`ai-refresh/HS_ADMIN.json`** — session_log (read-source for the rule).

---

*Origin: Peter Higgins / Rogue Wave Audio, with the HUF AI Collective.*
*HCC-R008: human governs release. Mechanical enforcement now covers what procedural enforcement already covers.*
*Discovery enters as investigation. Ripple is mapped. Change is packetized. Release is gated.*
*Lockdown allows filing. Execution waits for Peter. The breakpoint holds.*
