# Changelog

This is the discoverable digest of changes to Higgins Decomposition (Hs). The authoritative chronological log lives at [`ai-refresh/PUSHES_INDEX.md`](ai-refresh/PUSHES_INDEX.md) — that file has the full table of all pushes with commit SHAs, CI run numbers, catalog state per push, and cross-check archive verdicts.

**Live current state:** [`HS_FAST_REFRESH.json`](HS_FAST_REFRESH.json) — the single source of truth per Hs Change Control v1.0 rule HCC-R001. The `_meta.current_commit_sha` field carries the live SHA. The `_meta.last_push` field carries the latest push number.

**For AI assistants:** if your view of any state below differs from `HS_FAST_REFRESH.json`, your connector cache is stale. See [`AI_AGENTS.md` §2.1](AI_AGENTS.md) for cache-lag refresh guidance.

---

## Conference-prep arc (May 2026)

The most recent push window is the CoDaWork 2026 conference-preparation arc: pushes #38 through the current head. Catalog grew from 48 entries to 63 (33 CANONICAL, 8 STAGED) during this arc, with the STAGED disposition introduced in push #41 to capture canonical content with deferred ripple per Phase 5 discipline.

| Push | SHA | CI run | Theme |
|---|---|---|---|
| **#49** | *(this push, HOLD-TO-PUSH)* | *pending* | **Pre-Conference Lockdown** declared 2026-05-12 → 2026-06-06. PRE_CONFERENCE_LOCKDOWN.md + Root README Conference Status section + lockdown baseline receipt. |
| **#48** | `eca9604` | #45 ("Cache-lag mitigation") | Cache-lag mitigation + maintenance gap fixes (AI_AGENTS §2.1, SHA promotion, grounding test, manifest legacy marker, this CHANGELOG.md) |
| **#47** | `7f996e7` (combined) | #44 ("Document Control Protocol (DCP-001)") | DCP-001 executed end-to-end under Hs Change Control v1.0 |
| **#46** | `7f996e7` (combined) | #44 | Hs Change Control v1.0 scaffolding + INV-063 STAGED + DCP-001 filed |
| **#45** | `32e4018` | #43 ("CNQ Vector PDF") | Grok r6 intake + INV-062 STAGED + pedagogical tables |
| **#44** | `8acadfb` | #42 ("Coordination") | Spring cleaning + cross-AI coordination apparatus |
| **#43** | `e1f95e7` | #40 ("Investigation catalog") | Grok r5 intake + 6 new INV entries |
| **#42** | `7bd8e91` | #39 ("CODAWORK2026 Conference") | Talk delivery infrastructure (19 files) |
| **#41** | `f176e2c` | #38 ("Three open questions") | Grok r4 + ChatGPT s2 + Ascent Path STAGED |
| **#40** | `50b7e61` | #37 | ChatGPT review intake + INV-052 |
| **#39** | `50b7e61` | #37 | Three open questions + MC-4 sharpening |
| **#38** | `34913f8` | #36 | Two named findings + external review invite |

Full chronological detail with cross-check archive verdicts and hand-off docs: [`ai-refresh/PUSHES_INDEX.md`](ai-refresh/PUSHES_INDEX.md).

---

## Where to find things

| If you want to … | Read this |
|---|---|
| Get oriented in 30 seconds | [`QUICKSTART.md`](QUICKSTART.md) |
| Get the live current state (engines, counts, SHA) | [`HS_FAST_REFRESH.json`](HS_FAST_REFRESH.json) |
| See the chronological push log with SHAs and CI runs | [`ai-refresh/PUSHES_INDEX.md`](ai-refresh/PUSHES_INDEX.md) |
| Find a specific Discovery Change Packet | [`ai-refresh/change_packets/`](ai-refresh/change_packets/) |
| Understand the change-control doctrine | [`ai-refresh/CHANGE_CONTROL_README.md`](ai-refresh/CHANGE_CONTROL_README.md) |
| See controlled items + interfaces + traceability | [`ai-refresh/CONFIGURATION_ITEMS.json`](ai-refresh/CONFIGURATION_ITEMS.json), [`INTERFACE_CONTROL.json`](ai-refresh/INTERFACE_CONTROL.json), [`TRACEABILITY_MATRIX.json`](ai-refresh/TRACEABILITY_MATRIX.json) |
| See the investigation catalog (63 entries) | [`ai-refresh/INVESTIGATION_CATALOG.json`](ai-refresh/INVESTIGATION_CATALOG.json) |
| See cross-AI coordination | [`ai-refresh/CROSS_AI_COORDINATION.md`](ai-refresh/CROSS_AI_COORDINATION.md) |
| AI-assistant operating guide | [`AI_AGENTS.md`](AI_AGENTS.md) |

---

## Pre-conference status as of push #47

- **Engines:** CNT Python v3.1.0 / schema 3.1.0; CNQ Python v2.0.0 / schema cnq/2.0.0. Engine code unchanged across the entire conference-prep arc.
- **Catalog:** 63 / 33 CANONICAL / 8 STAGED / 12 DEFERRED / 8 OPEN / 1 FALSIFIED / 1 CLOSED.
- **Conference:** CoDaWork 2026, Coimbra, Portugal, 1–5 June 2026 (~20 days away).
- **Phase 5 conference-window discipline:** six NO-CREATE files still uncreated; no engine/tests/schema changes since push #37.
- **First Discovery Change Packet (DCP-001):** fully released and verified. INV-063 STAGED (Hs Change Control v1.0) is five of six gates clear.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*Discovery enters as investigation. Ripple is mapped. Change is packetized. Release is gated.*
