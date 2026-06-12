# Hs Change Control v1.0

**Status:** STAGED (INV-063). Scaffolding shipped in push #46 (2026-05-12). Doctrine graduates to CANONICAL after successful end-to-end application to DCP-001.
**Purpose:** Controlled discovery-to-baseline propagation system for Higgins Decomposition.

---

## The problem this addresses

Higgins Decomposition is a coherent system by design. Every significant new concept — a new engine version, a sharpened claim, an external review, an AI-platform finding, a schema bump — can ripple through README, AI loaders, runbooks, papers, tests, claim tables, terminology, and expected results.

Without a controlled crossflow process, the repo accumulates stale facts and contradictory current-state files. ChatGPT's review in cross-check archive `chatgpt_change_control_design_2026-05-12.md` documented the failure mode concretely: live AI-facing files disagree on engine versions, CNQ shipped status, investigation counts, and CCTT engine target.

**The goal is not to prevent ripple. The goal is to control ripple.**

A spacecraft survives millions of parts because every part has an identifier, revision, owner, interface, drawing, verification method, failure modes, and change history. Hs needs the same discipline for concepts, claims, engines, schemas, protocols, and AI-facing context.

---

## Operating doctrine

Eight rules, all encoded in `CONFIGURATION_ITEMS.json`:

1. **HCC-R001 — Single live source of truth.** `HS_FAST_REFRESH.json` is the live current-state source of truth for AI-facing repository state unless a later explicit baseline file supersedes it.
2. **HCC-R002 — No unmanaged version numbers.** Live AI-facing files must not carry independent engine versions, corpus counts, investigation counts, or current-status claims unless they are generated from or checked against `HS_FAST_REFRESH.json`.
3. **HCC-R003 — Discovery enters as investigation.** Every substantial new concept, defect, external-model suggestion, or architecture change enters through the Investigation Catalog or a Discovery Change Packet before it becomes public doctrine.
4. **HCC-R004 — Archive is preserved.** Historical AI_REFRESH narratives, cross-check archives, falsified hypotheses, and old push records are not deleted. They are marked historical and excluded from live-current consistency rules.
5. **HCC-R005 — Ripple requires impact map.** Any change of severity S3 or higher requires an impact map listing affected files, interfaces, controlled values, and verification checks.
6. **HCC-R006 — Claim changes require evidence.** Any upgrade from candidate or staged to canonical or confirmed must cite the evidence artifact, test, corpus result, external validation, or review packet that justifies promotion.
7. **HCC-R007 — Current-state files must agree.** README current-state block, llms.txt, AI_AGENTS.md, .well-known/ai-context.json, HS_FAST_REFRESH.md, and CCTT current protocol must not contradict HS_FAST_REFRESH.json on live facts.
8. **HCC-R008 — Human governs release.** Claude may implement and validate in the working repo, but Peter controls canonical commit, push, and public release.

---

## Severity classes for change

| Class | Name | Definition | Required action |
|---|---|---|---|
| **S0** | Archive-only | Historical record, archived AI output, false positive, obsolete narrative. | Preserve. Mark historical if unclear. Excluded from live-current consistency checks. |
| **S1** | Local patch | Typo, broken link, wording fix, single file. | Patch file. Optional note in push summary. |
| **S2** | Linked terminology / doc change | Affects multiple docs using the same term or concept; no engine/schema impact. | Update notation/terminology. Search and update dependent docs. Add catalog entry if substantive. |
| **S3** | Interface or AI-current-state change | Affects current-state claims, AI loaders, protocol pointers, or discovery-chain routing. | **Create a Discovery Change Packet.** Update CONFIGURATION_ITEMS.json / INTERFACE_CONTROL.json if needed. Run the consistency checker. |
| **S4** | Engine / schema / verification baseline change | Affects runtime output shape, engine behavior, schema version, expected results, or deterministic verification. | DCP + TRACEABILITY_MATRIX update + runbook update + engine tests + verification evidence. |
| **S5** | Scientific claim baseline change | Affects public scientific claim strength, canonical doctrine, paper framing, external-review posture. | DCP + CLAIM_STRENGTH_TABLE update + paper/talk updates + evidence record + release note. |

Most pain in the project to date has come from S3–S5 changes being handled as S1. The change-control system makes that mistake impossible by making the severity classification an explicit step.

---

## Discovery-to-baseline workflow

```
Discovery → Investigation → Impact Analysis → Candidate → Baseline → Release
   |              |               |              |          |          |
   |        catalog entry    DCP created    drafted in    HS_FAST_     pushed
   |        in INVESTIGATION  if S3+        affected     REFRESH.json  + CI green
   |        _CATALOG.json                   files        updated
   ↓
external AI session
Grok / ChatGPT note
Peter observation
pilot result
```

A concept should not jump from discovery to public coherence. It enters at one of these gates and is promoted explicitly.

---

## Configuration item registry

The current set of controlled items lives in `CONFIGURATION_ITEMS.json`. Each item has:

- `ci_id` — stable identifier (CI-001 through CI-015 as of push #46)
- `path` — file path in the repo
- `role` — what the item does in the system
- `owner` — conceptual responsibility group
- `change_authority` — who authorizes changes (Peter for all current items)
- `upstream_dependencies` — what this item depends on
- `downstream_consumers` — what depends on this item
- `verification` — what checks confirm the item is healthy

Adding a new controlled file requires adding an entry to this registry.

---

## Interface control registry

The current producer-consumer relationships live in `INTERFACE_CONTROL.json`. Each interface has:

- `interface_id` (IF-AI-001, IF-CCTT-001, IF-CLAIM-001, IF-TERM-001, IF-VERIFY-001 as of push #46)
- `producer` — the upstream source
- `consumers` — the downstream files
- `controlled_fields` — the specific facts/values that must stay aligned
- `failure_modes` — what goes wrong when the interface drifts
- `verification` — what check enforces the interface

Changing an interface requires updating the consumers in lockstep.

---

## Change packets

Discovery Change Packets live in `change_packets/DCP-NNN_TITLE.json`. The first packet, **DCP-001**, was filed in push #46 to validate the change-control process on a real backlog of drift.

A packet has these required fields: `id`, `title`, `severity`, `trigger`, `source_of_truth`, `affected_configuration_items`, `affected_interfaces`, `files_to_update`, `verification_required`, `status`, `owner`, `created_date`.

A packet moves through statuses: `proposed → in_progress → implemented → verified → released`. Releases happen only after Peter's explicit authorization and a green CI run.

`CHANGE_PACKET_TEMPLATE.json` shows the full required shape.

---

## Traceability matrix

`TRACEABILITY_MATRIX.json` connects concepts to requirements to affected files to verification checks. It is the "10 million parts not blow up" structural support — a way to ask *what does this change touch, and how do I know I didn't break it?*

---

## Consistency checks

`scripts/check_ai_refresh_consistency.py` is the static analyzer. It runs in stdlib Python and reports drift across live AI-facing files. Six checks:

| Check | What it catches |
|---|---|
| CHK-JSON-001 | Required JSON files parse cleanly |
| CHK-CNQ-001 | No live file says cnq.py is pending/missing |
| CHK-VERSION-001 | Engine versions align with HS_FAST_REFRESH.json |
| CHK-INV-001 | Investigation count current or marked as snapshot |
| CHK-CCTT-001 | CCTT current or legacy status is explicit |
| CHK-README-001 | README internal contradictions |

Run from repo root: `python scripts/check_ai_refresh_consistency.py`. Exit code 0 = no errors. Exit code 1 = errors found.

The first run against the live repo (push #46 baseline) is expected to **fail** because of the documented drift. That failure is recorded as the evidence in DCP-001 — it proves the system catches what it is supposed to catch.

---

## Claude implementation rules

When Claude operates on the repo under Hs Change Control v1.0:

1. Work in the local working repo. Build, verify, present HOLD-TO-PUSH.
2. Do not commit or push to GitHub. Peter holds that authority.
3. Do not delete historical files (cross_check_archive, old AI_REFRESH narratives, falsified entries).
4. Prefer additive scaffolding over disruptive reorganization.
5. When uncertain whether a stale phrase is live or archive, classify it conservatively and report it.
6. Do not change engine code as part of change-control work unless Peter authorizes an explicit S4 packet.
7. Do not change `expected_results.json` as part of DCP-001. That requires a separate S4 packet.
8. Keep implementations readable and inspectable. Stdlib Python only for the consistency checker.

---

## First validation packet: DCP-001

`change_packets/DCP-001_AI_CURRENT_STATE_ALIGNMENT.json` is the pilot. It targets the documented drift:

- `HS_FAST_REFRESH.md` still describes push #27 state (CNT 2.0.4, CNQ 1.0.0, 29 investigations)
- `.well-known/ai-context.json` engine block lists CNT 2.0.4 and CNQ 1.0.0
- `README.md` line 178 says cnq.py is "the next milestone" when CNQ shipped in push #26
- `ai-refresh/CCTT_RUNBOOK.md` engine target line 5 says CNT 2.0.4 / Schema 2.1.0
- `ai-refresh/CCTT_BUILD_INSTRUCTION_v1.0.json` targets old schema

**As of push #46, DCP-001 status is `proposed`.** The packet exists, the affected files are enumerated, the consistency checker has run and confirmed the drift, the evidence is recorded. The actual patches are queued for a subsequent push pending Peter's explicit authorization.

This split — scaffolding in #46, patches in #47 — is deliberate. The scaffolding is uncontroversial additive infrastructure. Patching live AI-facing public docs (especially README and CCTT_RUNBOOK) deserves a separate explicit decision, especially within the Coimbra conference window.

---

## Acceptance criteria for v1.0 doctrine promotion (STAGED → CANONICAL)

1. Scaffolding files exist and parse: `CONFIGURATION_ITEMS.json`, `INTERFACE_CONTROL.json`, `TRACEABILITY_MATRIX.json`, `CHANGE_PACKET_TEMPLATE.json`, this README.
2. Consistency checker runs from stdlib Python and exits non-zero on the documented drift.
3. DCP-001 is created with the drift evidence attached.
4. At least one DCP is executed end-to-end (status reaches `released`), demonstrating the workflow works.
5. The consistency checker exits 0 after the executed DCP.
6. A second DCP (any topic, any severity) is created and processed successfully, proving the system handles more than one pattern.

Earliest CANONICAL promotion: after Coimbra (2026-06-06+), after DCP-001 + one more DCP have been released cleanly.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*Discovery enters as investigation. Ripple is mapped. Change is packetized. Release is gated.*
