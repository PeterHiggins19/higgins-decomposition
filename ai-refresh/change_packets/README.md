# Discovery Change Packets

This folder holds Discovery Change Packets (DCPs) for the Higgins Decomposition repository under Hs Change Control v1.0 (INV-063 STAGED).

## What is a DCP?

A Discovery Change Packet is a structured JSON document that captures a single coherent change to the repo, especially when the change ripples across multiple files. Each DCP names:

- the trigger (what caused the change to be needed)
- the source of truth (where the new authoritative value lives)
- the configuration items affected
- the interfaces affected
- the traceability records affected
- the files to update
- the verification required
- the success criteria
- the risk if not done
- the lifecycle history

The template is at [`../CHANGE_PACKET_TEMPLATE.json`](../CHANGE_PACKET_TEMPLATE.json).

## Naming convention

`DCP-NNN_SHORT_NAME.json` where NNN is the next sequential packet number, e.g. `DCP-001_AI_CURRENT_STATE_ALIGNMENT.json`.

## Lifecycle statuses

```
proposed → in_progress → implemented → verified → released
                                                ↘ superseded
                                                ↘ abandoned
```

A packet is `released` only after Peter has authorized, committed, pushed, and CI has returned green on origin/main. The `lifecycle_history` array inside each packet records the transitions.

## Active packets

| ID | Title | Severity | Status | Notes |
|---|---|---|---|---|
| DCP-001 | Align live AI-facing current-state files with HS_FAST_REFRESH.json | S3 | proposed | Pilot validation for Hs Change Control v1.0. Execution held pending Peter authorization. |

## When to create a packet

Per the severity table in `../CHANGE_CONTROL_README.md`:

- **S0–S2** (archive-only, local patch, linked terminology): no packet required, but keep a short note in the push summary.
- **S3+** (interface, engine/schema, scientific claim): create a DCP.

When in doubt, classify conservatively and file the packet.

## When to update a packet

- During `in_progress`: add notes to `implementation_notes`.
- At verification time: add the consistency-checker output or test results to `verification_evidence`.
- After release: add commit SHA + CI run number to `release_notes`.

## When NOT to modify a packet

Once a packet is `released`, it is part of the historical record. Subsequent corrections require a new packet that supersedes the old one.

---

*Discovery enters as investigation. Ripple is mapped. Change is packetized. Release is gated.*
