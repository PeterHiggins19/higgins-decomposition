# DCP-002 CANDIDATE — Upgrade CHK-CNQ-001 to regex semantic-class matching

**Status:** **proposed** — staged in advance per pre-conference lockdown allowed-actions list. NOT executed during lockdown. First post-conference push window (opens 2026-06-06) is the earliest execution window.
**Severity:** S3 (interface or AI-current-state change — the consistency checker is an interface that scans live AI-facing files)
**Filed by:** Claude (Opus 4.6) at Peter directive 2026-05-12 *"update huf-gov within hs to Claude determined optimum fixes as suggested"*
**Authorizing parent doctrine:** HUF Governance Charter Article V (commitment 2 — visibility at correction)
**Reference implementation:** `Hs/huf-gov/candidates/upgraded_chk_cnq_001.py`

---

## Why this DCP exists

The 2026-05-12 breaker test (see `papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`) verified that the consistency checker's CHK-CNQ-001 rule catches all six literal phrases in its phrase list but **misses paraphrased violations**. Specifically:

- Phrase `cnq.py is pending` → caught
- Paraphrase `cnq.py engine is pending implementation` → NOT caught

The miss occurred because the rule uses literal-substring matching against a fixed phrase list rather than a semantic-class pattern. The HUF AI Collective cross-check catches most paraphrased drift in review, but the mechanical net has a documented hole. This DCP closes the hole.

The discovered gap was specifically called out in the breaker test report as a candidate for post-conference execution. It is non-fatal but it is a real falsifiability finding — a breaker that returned all-green would have been more suspicious. The honest finding is that the literal-string matcher needs a small upgrade.

---

## What the DCP does

**Replace** the existing CHK-CNQ-001 literal-string rule in `scripts/check_ai_refresh_consistency.py` with a regex pattern that catches the semantic class of "cnq.py is not yet shipped / is pending / is missing / etc." while preserving:

- File-level legacy-marker bypass (existing functionality)
- All 6 literal phrases that the current rule catches (backward compatibility)
- Exit-code semantics (exit 0 = clean, exit 1 = drift detected)
- The same warning + error reporting format

**Add** a regex pattern of the form:

```python
CNQ_DRIFT_PATTERN = re.compile(
    r'\bcnq\.py\b[^.\n]{0,40}\b(pending|missing|not\s+(?:yet\s+)?(?:implemented|built|shipped|done|finished|coded)|to\s+be\s+(?:built|implemented|shipped|coded)|incomplete|stub|placeholder|future\s+work)\b',
    re.IGNORECASE
)
```

The pattern matches `cnq.py` followed within 40 characters by any word in the drift vocabulary set (pending, missing, not yet implemented, to be built, incomplete, stub, placeholder, future work, etc.). Word boundary anchors prevent false matches inside larger words.

**Preserve** the existing legacy-marker bypass:

```python
if file_marked_legacy(file_path):
    return Pass(rule_id="CHK-CNQ-001",
                file=file_path,
                message="file-level legacy marker present; stale phrases allowed")
```

**Test** the new rule against:

1. The current 23-pass clean baseline (must still exit 0).
2. The 6 literal phrases from the existing rule (must trip on each).
3. A set of paraphrase test cases including:
   - `cnq.py engine is pending implementation` → must trip
   - `cnq.py is not yet built` → must trip
   - `cnq.py to be implemented in a future release` → must trip
   - `the cnq.py module is incomplete` → must trip
   - `cnq.py is currently a placeholder` → must trip
   - `cnq.py — future work` → must trip
   - `cnq.py was shipped at v2.0.0` → must NOT trip (positive statement)
   - `cnq.py adapter ran on Backblaze` → must NOT trip (operational statement)

The reference implementation in `Hs/huf-gov/candidates/upgraded_chk_cnq_001.py` is the test harness.

---

## Impact map (HCC-R005 required)

**Files modified.** Exactly one:
- `scripts/check_ai_refresh_consistency.py` — replace the `_check_cnq_status` function or equivalent CHK-CNQ-001 logic with the regex pattern.

**Files NOT modified.** Any document with stale CNQ phrasing that the upgraded rule newly catches needs to be either fixed or legacy-marked. The current Hs repo state passes the new rule cleanly — verified via dry-run on 2026-05-12 against the live checker baseline. Zero false positives expected.

**Downstream consumers of the rule.**
- DCP lifecycle: any future DCP that introduces a CNQ-status claim will be screened against the upgraded rule before `released` status. No protocol change.
- HUF AI Collective cross-check: AIs reading the checker output as a signal will see slightly different error messages. AI_AGENTS.md does not need updating.
- Cross-check archive: archive entries reference CHK-CNQ-001 by rule ID. Rule ID is preserved. No archive update needed.

**No engine code touched.** No schema touched. No catalog disposition touched. No claim-strength touched.

**Reversion path.** If the upgraded rule produces unexpected false positives in real operation, revert the function body to the pre-DCP literal-string list. Diff is small and reviewable. The reference implementation in `candidates/` remains as the documented intent.

---

## Verification criteria (HCC-R007)

Before transitioning DCP-002 from `implemented` to `verified`:

1. **Live checker exits 0 on the current repo state.** Run `python3 scripts/check_ai_refresh_consistency.py` and confirm 23 passes / 0 warnings / 0 errors (or the equivalent post-conference baseline at that time).
2. **All 6 historical literal phrases trip.** Run unit tests confirming each of the original 6 phrases is matched by the new regex.
3. **All 6+ paraphrase cases trip.** Run unit tests against the paraphrase test list above; each must produce a trip.
4. **All positive/operational statements pass.** Run unit tests against the 2+ negative test cases; each must NOT trip.
5. **No new false positives in live state.** Re-run the checker on the full Hs repo; pass count must equal or exceed pre-DCP baseline (currently 23). No new ERRORS or WARNINGS.
6. **Consistency checker self-test passes.** The checker has its own internal test harness (if any); confirm it still runs.

If any criterion fails, the DCP returns to `in_progress` for revision. If all pass, the DCP advances to `verified` and then to `released` upon Peter authorization.

---

## Why this is a candidate, not an active DCP

Per `PRE_CONFERENCE_LOCKDOWN.md` allowed-actions list:

> **ALLOWED during lockdown:**
> - DCP filing at `proposed` status (no execution)

This filing satisfies that allowance exactly. The DCP is:

- **Filed** at `proposed` status in this candidate document.
- **NOT advanced** to `in_progress` (no scripts/check_ai_refresh_consistency.py modification).
- **NOT executed** (no consistency-checker rewrite during lockdown).

When the lockdown clears 2026-06-06, this candidate document can be:

1. Read by the operator.
2. Copied (or directly moved) into `ai-refresh/change_packets/DCP-002_CHK_CNQ_REGEX_UPGRADE.json` in proper DCP JSON format.
3. Advanced through the standard DCP lifecycle.

The candidate-to-active transition is itself a candidate item for inclusion in the first post-conference push.

---

## Estimated execution effort

- **Reading prep:** ~10 minutes (re-read this candidate doc and the reference implementation).
- **Implementation:** ~30 minutes (replace the rule function; run unit tests; confirm live checker still green).
- **Verification:** ~15 minutes (run the test harness; check the test cases above; confirm 23-pass baseline preserved).
- **Documentation update:** ~15 minutes (update `ai-refresh/CHANGE_CONTROL_README.md` to reference DCP-002 if needed; update `BREAKER_INVENTORY.md` to remove the "Gap" note from Breaker 2).
- **Total:** ~70 minutes from candidate-read to released.

Fits comfortably inside a single post-conference push. Could be bundled with DCP-003 (the new CHK-DISPOSITION-001 rule) in the same push if desired.

---

## Related items

- **`Hs/huf-gov/candidates/upgraded_chk_cnq_001.py`** — reference implementation of the regex pattern with unit test harness.
- **`Hs/huf-gov/candidates/DCP-003_CANDIDATE_CHK_DISPOSITION_001.md`** — companion DCP for a new disposition-transition validation rule.
- **`papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`** — original breaker test that surfaced the gap.
- **`scripts/check_ai_refresh_consistency.py`** — current checker (untouched during lockdown).

---

*Origin: Peter Higgins / Rogue Wave Audio, with the HUF AI Collective.*
*Discovery enters as investigation. Ripple is mapped. Change is packetized. Release is gated.*
*Lockdown allows filing. Execution waits for Peter. The breakpoint holds.*
