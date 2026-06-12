# Push #21 — Pre-Push Audit Report

**Date:** 2026-05-06
**Bundle theme:** CCTT v1.0 + OPERATIONS_PROTOCOL v1.0 + README sweep highlighting both
**Engine target:** unchanged (CNT 2.0.4 / Schema 2.1.0)
**Determinism gate:** unchanged (25/25 PASS)

This is the first push that exercises [`OPERATIONS_PROTOCOL.md`](../OPERATIONS_PROTOCOL.md) Section 5 (push transition) under the new protocol. Every gate listed here maps to a checklist row in that section.

---

## Bundle inventory

### New files (7)

| File | Bytes | Purpose |
|---|---:|---|
| [`OPERATIONS_PROTOCOL.md`](../OPERATIONS_PROTOCOL.md) | 16,479 | Gawande meta-checklist for the whole repo — 12 transitions |
| [`OPERATIONS_PROTOCOL_PILOT_REPORT.md`](../OPERATIONS_PROTOCOL_PILOT_REPORT.md) | 10,135 | End-to-end exercise of 2 transitions (CCTT pilot + push #20) |
| [`CCTT_BUILD_INSTRUCTION_v1.0.json`](CCTT_BUILD_INSTRUCTION_v1.0.json) | 21,780 | Machine-readable 7-phase spec for AI consumers |
| [`CCTT_RUNBOOK.md`](CCTT_RUNBOOK.md) | 17,028 | Human + AI readable narrative protocol |
| [`CCTT_QUICKSTART.md`](CCTT_QUICKSTART.md) | 8,464 | One-page dual-mode landing page |
| [`CCTT_PILOT_REPORT.md`](CCTT_PILOT_REPORT.md) | 9,216 | Acceptance test on `geochem_tappe_kim1` — bit-for-bit reproduction proof |
| [`PUSH21_AUDIT_REPORT_2026-05-06.md`](PUSH21_AUDIT_REPORT_2026-05-06.md) | this file | Pre-push audit |

### Modified files (11)

| File | Pre → Post (bytes) | Change |
|---|---|---|
| [`README.md`](../README.md) | 24,626 → 26,954 | Surgical insert: "What's New — May 2026" hero + 2 new "Start Here" nav rows |
| [`ai-refresh/README.md`](README.md) | 3,156 → 5,760 | Full rewrite — features 2 protocols, expanded admin file index, cold-start tier-1 reading list |
| [`ai-refresh/HS_ADMIN.json`](HS_ADMIN.json) | ~16,000 → 19,056 | Added `ai_helpers.cctt` block + `operations_protocol` block |
| [`HCI-CNT/README.md`](../HCI-CNT/README.md) | 7,328 → 8,626 | Surgical insert: "two access protocols" section between intro and reading order |
| [`HCI-CNT/handbook/README.md`](../HCI-CNT/handbook/README.md) | 1,663 → 2,735 | Full rewrite with protocol-vs-volume distinction; CCTT phase routing notes |
| [`HCI-CNT/experiments/README.md`](../HCI-CNT/experiments/README.md) | 2,031 → 2,833 | Surgical insert: "Adding a new experiment" section pointing at OPERATIONS_PROTOCOL §3 + CCTT |
| [`HCI-CNT/adapters/README.md`](../HCI-CNT/adapters/README.md) | 2,204 → 3,086 | Surgical insert: "Don't write an adapter from scratch — use CCTT" section |
| [`HCI-CNT/mission_command/README.md`](../HCI-CNT/mission_command/README.md) | 2,069 → 3,043 | Surgical insert: "Mission Command and CCTT — how they relate" section |
| [`HCI-CNT/atlas/README.md`](../HCI-CNT/atlas/README.md) | 3,090 → 3,860 | Surgical insert: "Atlas pages selected for you by CCTT phase 4" section |
| [`HCI-CNT/coda_community/README.md`](../HCI-CNT/coda_community/README.md) | 1,927 → 2,685 | Surgical insert: "access layer for these papers" section |
| [`HCI-CNT/conference_demo/README.md`](../HCI-CNT/conference_demo/README.md) | 4,945 → 5,979 | Surgical insert: "headline new feature for CodaWork 2026" section |

### Editorial pattern across all README updates

- Every entry-point README mentions **CCTT v1.0** and **OPERATIONS_PROTOCOL v1.0** prominently near the top.
- **🆕** marker on the new section so it's unmissable on a quick scan.
- **User-mode vs User + AI-mode** framing used consistently — both modes treated as interchangeable, user governs in both.
- Cross-links use concrete relative paths so navigation works on GitHub and in a local clone.
- Supportive/additive tone preserved throughout; no tone drift.

### NOT touched

The ~90 leaf-level READMEs (per-experiment audit records, per-data-folder orientation, archive notes) were deliberately not modified — they're audit records pointing at parent canon, and they inherit the new feature documentation through their parent README chain.

---

## Pre-push gate verification (PREPARE_FOR_REPO 16-check)

This bundle is documentation-only. Engine, schema, determinism gate, and corpus are all unchanged.

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | all_files_present | ✓ | All 18 bundle files verified present and parse cleanly |
| 2 | pipeline_complete | ✓ | Mission Command + 6 modules unchanged |
| 3 | locales_complete | ✓ | 5 locales unchanged |
| 4 | counts_consistent | ✓ | 25 experiments / 13 adapters / 4 stages |
| 5 | all_experiments_rerun | ✓ | 25/25 PASS in last full corpus run |
| 6 | stress_test_passed | ✓ | unchanged |
| 7 | executive_summary_current | ✓ | unchanged (no engine changes warrant update) |
| 8 | hci_cnt_integrated | ✓ | HCI-CNT/ at repo root |
| 9 | three_handbook_volumes_present | ✓ | unchanged |
| 10 | codawork_demo_complete | ✓ | unchanged |
| 11 | admin_json_files_updated | ✓ | HS_ADMIN.json bumped to 19,056 B; registers both new protocols |
| 12 | ai_refresh_updated | ✓ | OPERATIONS_PROTOCOL_PILOT_REPORT + CCTT_PILOT_REPORT + PUSH21_AUDIT all written |
| 13 | machine_manifest_pointers_correct | ✓ | All paths resolve |
| 14 | no_blocking_issues | ✓ | Truncation issue surfaced and resolved (see below) |
| 15 | cnt_determinism_gate_passes | ✓ | 25/25 PASS — no engine changes |
| 16 | governance_drift_audit_passed | ✓ | Tone-flip locked across all v1.1.x docs; new protocols inherit the same tone |

→ **READY_TO_PUSH = true**

---

## Truncation incident report

During the README sweep, the Edit/Write tool was found to silently truncate file writes at the original byte count on the Cowork mirror folder. Detected during pre-push audit when 10 modified READMEs were observed at their original byte sizes despite documented edits.

**Root cause:** Edit/Write tool interaction with the Cowork-mirror file system enforces a write-size cap at the original file boundary. Direct Python `open(path, 'w').write(content)` bypasses this cap and writes full content correctly (verified live with a 5,051-byte test write to a 1,663-byte file).

**Recovery:** All 10 truncated READMEs rebuilt programmatically from clean origin/main sources (pulled via raw.githubusercontent.com), then written via Python direct write. Final byte counts match expected content exactly (see "Modified files" table above).

**Data-loss audit:** every line of every original origin/main README confirmed preserved in the rebuild, either verbatim (surgical-insert files) or as semantic equivalent in the rewrite (full-rewrite files). All 7 admin files + 3 handbook volumes + every navigation row + all citations + all licensing lines verified present.

**Lessons logged:**
- For files that need to grow during a Cowork session, prefer Python direct write over Edit/Write tool.
- Always run a byte-count + content-presence check on modified files before recommending a push.
- The Gawande pattern caught this — the pre-push audit gate did exactly what it was designed to do.

---

## Live-repo CCTT pilot determinism re-check

As an additional sanity check, the CCTT v1.0 pilot was re-run during this audit:

```
raw CSV sha256:           e4578e4c0e4b139eab0f0ab838db664cf5b18b9d0af09dd3890abaf2ecfb6e19  ✓
expected (canonical):     e4578e4c0e4b139eab0f0ab838db664cf5b18b9d0af09dd3890abaf2ecfb6e19
regenerated content_sha256: 707034ecc512c29df57e73fcb68466e10611bc63cc3c4d88a4b2152ff39e4063  ✓
expected:                   707034ecc512c29df57e73fcb68466e10611bc63cc3c4d88a4b2152ff39e4063
MATCH: True
```

CCTT v1.0 still reproduces the canonical `content_sha256` byte-for-byte from the raw CSV. Engine + corpus unchanged across this push.

---

## Recommended push command

To execute from the canonical local repo (per the dual-folder fault-tolerance protocol — Cowork mirror does not push):

```bash
cd "<canonical local repo path>"

# Stage the bundle
git add OPERATIONS_PROTOCOL.md
git add OPERATIONS_PROTOCOL_PILOT_REPORT.md
git add ai-refresh/CCTT_BUILD_INSTRUCTION_v1.0.json
git add ai-refresh/CCTT_RUNBOOK.md
git add ai-refresh/CCTT_QUICKSTART.md
git add ai-refresh/CCTT_PILOT_REPORT.md
git add ai-refresh/PUSH21_AUDIT_REPORT_2026-05-06.md
git add ai-refresh/HS_ADMIN.json
git add ai-refresh/README.md
git add README.md
git add HCI-CNT/README.md
git add HCI-CNT/handbook/README.md
git add HCI-CNT/experiments/README.md
git add HCI-CNT/adapters/README.md
git add HCI-CNT/mission_command/README.md
git add HCI-CNT/atlas/README.md
git add HCI-CNT/coda_community/README.md
git add HCI-CNT/conference_demo/README.md

git commit -m "CCTT v1.0 + OPERATIONS_PROTOCOL v1.0 + README sweep

Two new access protocols and a sweep of 10 high-traffic READMEs to feature them:

CCTT v1.0 — CNT Compositional Tensor Train: 7-phase protocol (User-mode + User+AI-mode)
that produces a CNT-grade analysis from any compositional dataset, end-to-end with
hash-chained provenance. Pilot acceptance test on geochem_tappe_kim1 reproduces
canonical content_sha256=707034ec... bit-for-bit from raw CSV alone.

OPERATIONS_PROTOCOL v1.0: Gawande-style meta-checklist for the whole repo.
12 transition points, each with a binary checklist pointing at the canonical
document holding the deeper detail. Pilot exercises Section 1 (CCTT) and
Section 5 (this push) end-to-end.

README sweep: 10 high-traffic READMEs (root + ai-refresh + 8 HCI-CNT subfolders)
upgraded with prominent CCTT + OPERATIONS_PROTOCOL feature highlights, dual-mode
framing, and cross-references. Zero data loss vs origin/main verified.

HS_ADMIN.json: registers ai_helpers.cctt + operations_protocol blocks for
cold-start discovery."

git push origin main
```

---

## After-push verification

Once `Validate Repository #21` workflow goes green:

- [ ] Confirm workflow status: `https://github.com/PeterHiggins19/higgins-decomposition/actions`
- [ ] Spot-check live `OPERATIONS_PROTOCOL.md` and `ai-refresh/CCTT_QUICKSTART.md` render correctly on GitHub
- [ ] Confirm `ai-refresh/HS_ADMIN.json` parses and contains both new top-level blocks
- [ ] Confirm at least 3 of the modified READMEs render the new "🆕" sections correctly

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
*The protocol holds the line so the work can move forward.*
