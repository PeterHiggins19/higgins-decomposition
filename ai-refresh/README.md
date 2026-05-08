# ai-refresh — Admin files, AI helpers, and the operations protocol

This folder is the home of every file an AI assistant or user / researcher
collaborator needs to come up to speed on the Hs / HCI-CNT system, plus the
canonical admin JSONs that record what state the project is in.

If you are landing here for the first time, start with the **two protocols**
shipped in May 2026 — they make the rest of this folder navigable.

---

## The two protocols

### 🆕 CCTT v1.0 — CNT Compositional Tensor Train

Lets any user — by hand or with an AI assistant — produce a CNT-grade
compositional analysis from a raw dataset, end-to-end with hash-chained
provenance. Same 7-phase protocol works for both User-mode and User + AI-mode.

| File | Purpose |
|---|---|
| [`CCTT_QUICKSTART.md`](CCTT_QUICKSTART.md) | One-page intro — start here |
| [`CCTT_RUNBOOK.md`](CCTT_RUNBOOK.md) | Narrative protocol — read end-to-end (User or AI) |
| [`CCTT_BUILD_INSTRUCTION_v1.0.json`](CCTT_BUILD_INSTRUCTION_v1.0.json) | Machine-readable spec — AI consumes this |
| [`CCTT_PILOT_REPORT.md`](CCTT_PILOT_REPORT.md) | Acceptance test on `geochem_tappe_kim1` — bit-for-bit reproduction proof |

### 🆕 OPERATIONS_PROTOCOL v1.0 — Gawande meta-checklist

Front-door map of every operational transition in the repo (starting an
analysis, pushing, cowork session start/end, AI cold-start, recovery from
push failure or corpus drift, …). Lives at the **repo root**:

| File | Purpose |
|---|---|
| [`../OPERATIONS_PROTOCOL.md`](../OPERATIONS_PROTOCOL.md) | The transition map — 12 sections, each with a binary checklist |
| [`../OPERATIONS_PROTOCOL_PILOT_REPORT.md`](../OPERATIONS_PROTOCOL_PILOT_REPORT.md) | End-to-end exercise of two transitions against today's live evidence |

---

## Admin / state files

The canonical record of where the project is right now. Future Cowork sessions
read these on cold-start.

| File | Purpose |
|---|---|
| [`HS_ADMIN.json`](HS_ADMIN.json) | Authoritative state: engine version, push history, fault-tolerance protocol, CCTT registration, operations-protocol registration, full 25-experiment table |
| [`HS_MACHINE_MANIFEST.json`](HS_MACHINE_MANIFEST.json) | "Where is everything" pointer block. Includes the dual-folder fault-tolerance protocol |
| [`HS_GITHUB_CONFIG.json`](HS_GITHUB_CONFIG.json) | GitHub workflow + repo configuration |
| [`HS_MAINTENANCE.json`](HS_MAINTENANCE.json) | Open maintenance items and step-by-step procedures |
| [`HS_SYSTEM_BACKUP.json`](HS_SYSTEM_BACKUP.json) | Periodic full-state file-tree snapshot |
| [`HS_SYSTEM_INVENTORY.json`](HS_SYSTEM_INVENTORY.json) | File inventory by domain |
| [`PREPARE_FOR_REPO.json`](PREPARE_FOR_REPO.json) | 16-item push pre-flight checklist (Section 5 of the operations protocol) |
| [`PROJECT_HISTORY.json`](PROJECT_HISTORY.json) | Long-form project history |
| [`WORKSPACE_AUDIT_2026-05-05.{json,md}`](WORKSPACE_AUDIT_2026-05-05.md) | Last full workspace audit |

---

## AI refresh files

Dated cold-start refresh notes. A new session reads the most recent
`AI_REFRESH_*.md` to see what changed since the last cycle.

| File | Date / scope |
|---|---|
| [`AI_REFRESH_2026-05-06_push_19_and_dual_folder.md`](AI_REFRESH_2026-05-06_push_19_and_dual_folder.md) | Most recent — push #19 verified + dual-folder protocol formalised |
| [`AI_REFRESH_2026-05-06_HCI-CNT_migration.md`](AI_REFRESH_2026-05-06_HCI-CNT_migration.md) | HCI-CNT folded into Hˢ repo |
| [`AI_REFRESH_2026-05-05_v1.1.x.md`](AI_REFRESH_2026-05-05_v1.1.x.md) | v1.1.x consolidation cycle |
| [`AI_REFRESH_2026-05-05.md`](AI_REFRESH_2026-05-05.md) | Pre-consolidation snapshot |
| [`AI_REFRESH_2026-05-03.md`](AI_REFRESH_2026-05-03.md), [`AI_REFRESH_2026-05-02.md`](AI_REFRESH_2026-05-02.md), [`AI_REFRESH_2026-04-30.md`](AI_REFRESH_2026-04-30.md), [`AI_REFRESH_2026-04-27.md`](AI_REFRESH_2026-04-27.md) | Earlier refresh cycles |
| [`AI_VERIFICATION_SINCE_PUSH12.md`](AI_VERIFICATION_SINCE_PUSH12.md) | Verification trail since push #12 |

---

## Per-push audit reports

One report per significant push. Together they're the audit trail of how the
repo evolved across the v1.1.x consolidation cycle.

- [`PUSH15_AUDIT_REPORT_2026-05-06.md`](PUSH15_AUDIT_REPORT_2026-05-06.md) — HCI-CNT migration
- [`PUSH16_AUDIT_REPORT_2026-05-06.md`](PUSH16_AUDIT_REPORT_2026-05-06.md) — INDEX engine version refresh
- [`PUSH17_AUDIT_REPORT_2026-05-06.md`](PUSH17_AUDIT_REPORT_2026-05-06.md) — community-presence assets
- [`PUSH18_AUDIT_REPORT_2026-05-06.md`](PUSH18_AUDIT_REPORT_2026-05-06.md) — Hs-CNT_2026-05 corpus + 102 folder READMEs
- [`PUSH19_AUDIT_REPORT_2026-05-06.md`](PUSH19_AUDIT_REPORT_2026-05-06.md) — talk_deck cleanup
- [`../PUSH_BUNDLE_AUDIT.md`](../PUSH_BUNDLE_AUDIT.md) — bundled audit covering #18+#19+#20

---

## How this folder is meant to be used

For a fresh AI session on cold-start, the **tier-1 reading list** is short:

1. [`HS_MACHINE_MANIFEST.json`](HS_MACHINE_MANIFEST.json) — pointer block + dual-folder protocol
2. [`HS_ADMIN.json`](HS_ADMIN.json) — current state, push history, registered helpers
3. [`../OPERATIONS_PROTOCOL.md`](../OPERATIONS_PROTOCOL.md) — the transition map
4. [`CCTT_RUNBOOK.md`](CCTT_RUNBOOK.md) — if the session involves a compositional analysis

Then read the most recent `AI_REFRESH_*.md` for what changed since last cycle.
That's about 30 minutes of context, after which the session is operationally
current.

For a user / researcher collaborator landing fresh, the same reading list works
in the same order — `OPERATIONS_PROTOCOL.md` and the `CCTT_RUNBOOK.md` are written
to be readable by either audience.

---

Peter Higgins / Rogue Wave Audio / CC BY 4.0

*The instrument reads. The expert decides. The hashes carry the receipts.*
