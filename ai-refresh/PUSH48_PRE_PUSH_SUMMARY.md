# PUSH #48 — pre-push summary (HOLD-TO-PUSH) — CACHE-LAG MITIGATION + MAINTENANCE GAP FIXES

**Date prepared:** 2026-05-12
**Push status:** **PREPARED locally — HOLD-TO-PUSH pending Peter authorization.**
**Push type:** doc-only maintenance + cache-lag mitigation (gap-closing)
**Active priority:** CoDaWork 2026 conference talk (Coimbra, Portugal, 1–5 June 2026)
**Engine / tests / schema unchanged.**

---

## Why this push exists

Peter directive 2026-05-12: *"do a full maintenance push and update as suggested include gap fixes on all that can be identified and closed. then prepare for push."*

Trigger: Grok's 2026-05-12 connector-cache-lag confusion. Minutes after push #46+#47 (commit `7f996e7`, CI #44 "Document Control Protocol (DCP-001)") landed, Grok ran a check, reported DCP-001 as "Not Found", and offered to build a new Document Control Protocol from scratch. Only when given the direct raw URL did Grok find the file. The repo state was fine; Grok's connector cache was minutes behind. This is a recurring AI-side failure mode that every AI session encountering this repo at high commit velocity will hit.

Push #48 closes the gaps that would have prevented Grok's confusion (and will prevent every future AI session's equivalent confusion) without changing any canonical state. Five concrete fixes.

---

## What's in the bundle

### 5 patched files + 1 new file + 1 evidence file

| Path | Change |
|---|---|
| `AI_AGENTS.md` | §2 grounding test refreshed with current commit SHA `7f996e7` (CI #44) + new "Does DCP-001 exist?" question. **§2.1 new section "Connector cache lag — recognising and working around it"** — detection signals (stale `last_push` answer, files reported missing that exist, `v0.29.0` tag without later SHA), raw-URL refresh pattern, GitHub API endpoints, SHA-citation discipline, repo-side guarantees. §5 platform-capability table updated with Grok's 2026-05-12 cache-lag experience. |
| `HS_FAST_REFRESH.json` | `_meta.current_commit_sha` + `_meta.current_commit_sha_full` + `_meta.current_ci_run` + `_meta.current_ci_run_name` + `_meta.current_ci_duration_seconds` + `_meta.cache_lag_check_url` + `_meta.cache_lag_note` promoted as top-level `_meta` fields. SHA is now programmatically discoverable without parsing the `push_*_completed` string. |
| `.well-known/ai-context.json` | `grounding_test.questions` rewritten — 4 questions (Q1 = `_meta.last_push` + `current_commit_sha` answer; Q2 = cnq.py existence; Q3 = DCP-001 existence; Q4 = author). `_cache_lag_note` field added. `_metadata.last_aligned_in_push = #48`. `ai_platform_capability_observed.grok` updated. |
| `ai-refresh/HS_MACHINE_MANIFEST.json` | `_meta._status` LEGACY SNAPSHOT marker added — file was push #35 era with stale `engine_version: 2.0.4`, `last_push: #35`, `"engine_status": "cnq.py pending (~14 days)"`, and absolute Cowork sandbox paths. Preserved per HCC-R004; refreshed manifest queued as post-conference DCP candidate. |
| `ai-refresh/PUSHES_INDEX.md` | Push #48 row added with full description of the five fixes. After-#48 catalog row. PUSH48_PRE_PUSH_SUMMARY.md added to hand-off table. |
| **`CHANGELOG.md`** (NEW, at repo root) | Discoverable digest pointer to `ai-refresh/PUSHES_INDEX.md`. Lists last 11 pushes inline. "Where to find things" table. Pre-conference status block. Cache-lag guidance for AI assistants. |
| `ai-refresh/change_packets/push_48_post_maintenance_checker_output_2026-05-12.txt` (NEW) | Consistency checker output post-maintenance: 23 passes / 0 warnings / 0 errors / exit 0. Evidence that the push doesn't introduce new drift. |

---

## What this addresses, gap by gap

### Gap 1: AI-facing files had no cache-lag guidance

**Before:** An AI hitting this repo after a fresh push could report files as missing, treat stale state as canon, or offer to rebuild things that already exist. No guidance on detecting or working around connector cache lag.

**After:** `AI_AGENTS.md §2.1` is a dedicated section. Any AI reading the file's first 2KB now knows: detection signals, refresh patterns, raw-URL conventions, the GitHub API endpoint to verify SHA, and the SHA-citation discipline.

### Gap 2: Live commit SHA wasn't programmatically discoverable

**Before:** `HS_FAST_REFRESH.json._meta.push_47_completed` contained the SHA as a string fragment (`"2026-05-12 PUSHED 7f996e7 CI #44 ..."`). AIs had to parse the string to extract the SHA.

**After:** `_meta.current_commit_sha`, `_meta.current_ci_run`, `_meta.current_ci_run_name`, and `_meta.cache_lag_check_url` are top-level fields. An AI can read them directly without regex.

### Gap 3: `.well-known/ai-context.json` grounding test didn't catch stale state

**Before:** The grounding test asked about file existence and authorship. It didn't ask the AI for the current push number, so a cache-stale AI couldn't self-diagnose.

**After:** Q1 explicitly asks for `_meta.last_push` + `current_commit_sha`. An AI that can't answer with `#47` and `7f996e7` (or higher post-push-#48) now knows its view is stale, and the `stale_state_diagnostic` field tells it what's missing. New Q3 specifically tests DCP-001 existence as a recent-state marker.

### Gap 4: `HS_MACHINE_MANIFEST.json` had stale claims and absolute sandbox paths

**Before:** ChatGPT flagged this file as containing `"engine_status": "cnq.py pending (~14 days)"` and absolute Cowork sandbox paths that won't exist on any other machine. The file wasn't in the consistency checker's `LIVE_CURRENT_FILES` list, so the checker didn't flag it.

**After:** `_meta._status` LEGACY SNAPSHOT marker explicitly declares the file historical and points at `HS_FAST_REFRESH.json` as the live source of truth. File preserved per HCC-R004. Any AI reading the manifest now sees the legacy marker first.

### Gap 5: PUSHES_INDEX.md wasn't discoverable from repo root

**Before:** The chronological push log lived deep in `ai-refresh/PUSHES_INDEX.md`. Grok's search "across the entire repository" didn't surface it. External reviewers landing on the repo home page had no obvious entry point to the change history.

**After:** `CHANGELOG.md` at repo root points at `PUSHES_INDEX.md` as authoritative + inlines the last 11 pushes + has a "where to find things" table. This is the front-door digest Peter referenced earlier — *"on repo digest of changes document and window for all."*

---

## What's explicitly NOT in this push

- No engine code changes
- No schema changes
- No `expected_results.json` changes
- No new NO-CREATE files
- No catalog changes (still 63 / 33 / 8)
- No new INV entries (the work here is implementation of HCC-R001/R002/R007 doctrine, not new claims)
- No new DCP filed (this is doc-only maintenance under the existing change-control system, not a new packet — small fixes that don't cross severity-class threshold to require a DCP)

The 6 NO-CREATE files remain uncreated. Phase 5 conference-window discipline intact.

---

## Hold-to-push protocol (when you authorize release)

Standard 8-step:

1. Update `HS_FAST_REFRESH.json._meta.last_push` from `#47` → `#48`
2. Remove `push_48_prepared_held` from `HS_FAST_REFRESH.json._meta`
3. Remove `push_48_status` HOLD line from `HS_ADMIN.json._meta`
4. Set `push_48_completed = 2026-05-12`
5. Flip session_log push #48 `push_status` from HOLD to `PUSHED <SHA> 2026-05-12 CI run #<N>`
6. Write `PUSH48_READY_FOR_COMMIT.md`
7. Peter runs git commit + push locally
8. Post-push sync: record SHA + CI run number; bump `_meta.current_commit_sha` to the new SHA + `_meta.current_ci_run` to the new CI run number

---

## Pre-flight checks

| Check | Expected |
|---|---|
| 5 admin JSONs parse | OK |
| `.well-known/ai-context.json` parses with new grounding test | OK |
| `HS_FAST_REFRESH.json` has `_meta.current_commit_sha = "7f996e7"` | OK |
| `HS_MACHINE_MANIFEST.json` has `_meta._status` legacy marker | OK |
| `AI_AGENTS.md` contains `§2.1 Connector cache lag` section | OK |
| `CHANGELOG.md` exists at repo root with PUSHES_INDEX.md pointer | OK |
| `ai-refresh/change_packets/push_48_post_maintenance_checker_output_2026-05-12.txt` exists | OK |
| Consistency checker exits 0 (23 passes / 0 warnings / 0 errors) | OK (verified) |
| 6 NO-CREATE files still uncreated | OK |
| INV catalog math 63 / 63 / 63 / 63 | OK (unchanged) |
| Push #48 session_log entry present with 6 changes | OK |

---

## Recommended commit message

```
push #48 — Cache-lag mitigation + maintenance gap fixes

Doc-only maintenance push. No engine/tests/schema/NO-CREATE
changes. Phase 5 intact. Triggered by Grok's 2026-05-12
connector cache-lag confusion.

Five gap fixes:
  AI_AGENTS.md — §2 grounding test refreshed with current
    SHA 7f996e7 + DCP-001 existence question. §2.1 NEW
    "Connector cache lag" section: detection signals,
    raw-URL refresh, GitHub API endpoints, SHA-citation
    discipline. §5 Grok platform-capability updated.
  HS_FAST_REFRESH.json — _meta.current_commit_sha +
    current_ci_run + cache_lag_check_url + cache_lag_note
    promoted to top-level fields for programmatic discovery.
  .well-known/ai-context.json — grounding_test.questions
    rewritten with stale-state self-check + DCP-001
    existence question. _metadata.last_aligned_in_push = #48.
  ai-refresh/HS_MACHINE_MANIFEST.json — _status LEGACY
    SNAPSHOT marker added (was push #35 era with stale
    engine versions + absolute sandbox paths). Preserved
    per HCC-R004.
  CHANGELOG.md (NEW at repo root) — discoverable digest
    pointer to PUSHES_INDEX.md with last 11 pushes inline +
    where-to-find-things table.

Evidence:
  ai-refresh/change_packets/push_48_post_maintenance_checker
    _output_2026-05-12.txt — consistency checker still
    exits 0 with 23 passes / 0 warnings / 0 errors.

Catalog state unchanged: 63 / 33 CANONICAL / 8 STAGED /
                          12 DEFERRED / 8 OPEN / 1 FALSIFIED / 1 CLOSED.

No engine / test / schema changes.
```

---

*Prepared 2026-05-12 in push #48. Fifth push of the day, all maintenance + governance + cache-lag mitigation. The change-control system is now exercised AND improved within the same 24-hour window.*
