# Pre-Conference Lockdown — 2026-05-12 through 2026-06-06

**Status:** ACTIVE
**Window:** 2026-05-12 (push #49 lockdown declared) → 2026-06-06 (post-CoDaWork 2026, Coimbra)
**Authority:** Peter Higgins (sole authorization gate)
**Doctrine:** Hs Change Control v1.0 (INV-063 STAGED), specifically the Phase 5 conference-window discipline

---

## What this declares

The repository is in **conference-window lockdown** until 2026-06-06. The CoDaWork 2026 talk in Coimbra, Portugal (1–5 June 2026) is the active priority. The repo state at this lockdown is the state that will be presented at the conference — no last-minute structural changes, no engine moves, no claim shifts.

## What is locked

| Element | Status | Until |
|---|---|---|
| Engine code (`HCI-CNT/engine/cnt.py`, `HCI-CNQ/engine/cnq.py`, `hci_shared/*`) | **LOCKED** at CNT v3.1.0 / CNQ v2.0.0 | 2026-06-06 |
| Engine tests | **LOCKED** | 2026-06-06 |
| Engine schema (3.1.0 + cnq/2.0.0) | **LOCKED** | 2026-06-06 |
| `HCI-CNQ/results/expected_results.json` | **LOCKED** | 2026-06-06 |
| `HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md` | **LOCKED** | 2026-06-06 |
| `HCI-CNQ/CLAIM_STRENGTH_TABLE.md` | **LOCKED** | 2026-06-06 |
| Investigation Catalog disposition counts (63 / 33 / 8 / 12 / 8 / 1 / 1) | **LOCKED** | 2026-06-06 |
| Six NO-CREATE files (Ascent Path Phase 5 list) | **REMAIN UNCREATED** | 2026-06-06 |
| Talk material in `papers/codawork2026/talk/` | **LOCKED** at push #45 state | 2026-06-06 |

## What remains allowed during the lockdown

- **S1 fixes:** typos, broken links, single-file wording corrections (no DCP required, just push with note in `session_log`).
- **S2 fixes:** linked terminology corrections that don't affect engine/claim — only if catching a real reader-confusion bug.
- **Post-push admin sync:** the standard pattern of recording SHA + CI run number after any commit. This is the recording mechanism, not a change.
- **Cross-check archive entries:** any AI session or external review that produces material can be archived under `ai-refresh/cross_check_archive/` without a DCP. Archive entries are evidence, not changes.
- **DCP filing without execution:** if a new concept or external review surfaces, file a DCP at status `proposed` with the work scoped. Do NOT execute (`in_progress` → `implemented` → `verified` → `released`) until post-conference unless **all three** of the following hold:
  1. The finding is severity S0 catastrophic (would invalidate the talk's claims at the lectern).
  2. The fix is fully scoped and reviewable in under one hour.
  3. Peter explicitly authorizes mid-lockdown release.

## What is explicitly forbidden during the lockdown

- **No engine code changes.** S4 packets are queued for post-conference.
- **No new tests or test-suite restructuring.** Engine test plane stays as-is.
- **No claim promotions.** STAGED entries (INV-054, INV-056, INV-057, INV-058, INV-060, INV-061, INV-062, INV-063) stay STAGED.
- **No new CANONICAL claims.** Five reviews already validated INV-059 humble-invitation framing; no further promotions until after the talk.
- **No creation of the six NO-CREATE files:** `docs/HS_ASCENT_PATH.md`, `CLAIMS_REGISTER.md`, `GLOSSARY_CANON.md`, `PROMOTION_LOG.md`, `PROMOTION_PACKET_TEMPLATE.md`, `STAGED_ASCENT_MAP.md`.
- **No new CCTT v1.1 build.** CCTT v1.0 has a clean legacy marker; v1.1 is post-conference work.
- **No `hs_cnq_pdf_exporter.py` implementation.** INV-062 spec is filed; build it post-conference as DCP-002 candidate.
- **No QFT / QWT / quaternion-edge-detection implementation.** Grok r6 theoretical extensions need derivation review post-conference.

## What the lockdown does NOT cover

- Speaker preparation (mooting, SPEAKER_BRIEF re-reads, CHEAT_SHEET review) — Peter's pre-conference workflow. Continue normally.
- Travel logistics — passport, flight, hotel, conference registration. Continue normally.
- Reading PEDAGOGICAL_TABLES.md — Q&A depth backup, expected use.
- Talk delivery itself at the conference — the lockdown ends 2026-06-06.
- Replying to email or external review with the repo's current state — encouraged. Use `HS_FAST_REFRESH.json._meta.current_commit_sha` to cite SHA, and direct readers to `CHANGELOG.md` for the digest.

## Lockdown rationale

The repo went through 11 pushes over 8 days (#38 through #48) building, validating, and consolidating the conference-prep work. Today's work alone (#44 through #48, five pushes) completed:

- The cross-AI coordination apparatus (push #44)
- Grok r6 intake + INV-062 + pedagogical tables (push #45)
- Hs Change Control v1.0 doctrine + first DCP filed (push #46)
- DCP-001 executed end-to-end, lifecycle proposed → released (push #47)
- Cache-lag mitigation + maintenance gap fixes, self-bootstrapping (push #48)

This is a natural inflection point. The next 20 days are speaker preparation, not repo work. Continued repo activity in this window risks introducing changes that don't get the proper review attention because the speaker is rightly focused on the lectern.

The lockdown also provides external reviewers (and the next AI session that lands on this repo) explicit grounds to decline "build this now" requests. Push #48 introduced the cache-lag mitigation; push #49 introduces the conference-window lock as the final structural support for the next 20 days.

## If a critical defect IS found

The lockdown does not block defect fixes. The protocol:

1. **Identify the defect** with concrete evidence (file path, line number, error reproduction).
2. **File an S0 DCP** at `ai-refresh/change_packets/DCP-NNN_CRITICAL_<short_name>.json` with status `proposed`, full impact map, and explicit Peter-authorization request.
3. **Wait for Peter's explicit authorization.** Do not execute without it.
4. **If authorized:** standard DCP cycle, with the lockdown record-keeping noting that an S0 packet was exercised mid-lockdown.
5. **If not authorized:** the DCP stays at `proposed` until post-conference.

The threshold is "would invalidate a load-bearing claim in the talk at the lectern." Comfort fixes, polish, and new features do not meet the threshold.

## Lockdown clear point: 2026-06-06

At 2026-06-06, the lockdown lifts. The first post-conference push (likely DCP-002, building `hs_cnq_pdf_exporter.py` per INV-062 STAGED spec) becomes the cleanest pivot point:

- DCP-002 executes end-to-end (builds the CNQ vector PDF exporter, exercises against EMBER Germany, captures veraPDF receipt)
- INV-062 STAGED → CANONICAL on the new evidence
- INV-063 STAGED → CANONICAL because DCP-002 satisfies gate 6 (second DCP processed successfully)
- The change-control system is fully validated

After that, the post-conference roadmap (8 STAGED entries) unfolds at normal pace.

---

## Repository state at lockdown declaration

- **Latest push:** #49 (this push, declaring the lockdown)
- **Commit SHA at lockdown:** see `HS_FAST_REFRESH.json._meta.current_commit_sha`
- **Engine versions:** CNT Python v3.1.0 / schema 3.1.0, CNQ Python v2.0.0 / schema cnq/2.0.0
- **Catalog:** 63 / 33 CANONICAL / 8 STAGED / 12 DEFERRED / 8 OPEN / 1 FALSIFIED / 1 CLOSED
- **CI runs in conference-prep arc:** 12 (all green, push #36 "HCI Coherence" through push #45 "Cache-lag mitigation"; #49 pending)
- **Consistency checker:** exit 0 with 23 passes / 0 warnings / 0 errors

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*The repo holds. The speaker walks to the lectern.*
