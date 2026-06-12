# HGS-003 — Software Requirements Specification (SRS)
**Program:** HGS · **Rev:** Draft A · 2026-06-09 · **Status:** DRAFT Pre-Phase A · **Refs:** HGS-000/001/002, NPR 7150.2, `../CNTT_FLIGHT_CONTROL_SPEC.md`

## 1 Scope
Software requirements for the CN-TT engine, the Geologist Protocol Control Code (GPCC), the Coherence Supervisor, and their integration as NASA core Flight System (cFS) applications. Traces to HGS-002.

## 2 Engine (CN-TT)
| ID | Requirement | Traces |
|---|---|---|
| HGS-SW-001 | The engine shall implement closure → CLR → Helmert-ILR → per-step navigation per HUF-STD-002 (CNT). | SYS-001 |
| HGS-SW-002 | CNQ shall be computed **natively at D = 4** (quaternion); above D=4 per declared tier. | SYS-001 |
| HGS-SW-003 | The engine shall emit canonical CNT/CNQ JSON with `content_sha256`. | SYS-008 |
| HGS-SW-004 | Numerics shall use the **flight profile** (TBR-04) guaranteeing bit-identical results flight ↔ twin. | SYS-007, SYS-019 |
| HGS-SW-005 | **Upstream zero-treatment** (structural-drop + multiplicative replacement) shall run before the engine. | SYS-001 |
| HGS-SW-006 | All loops shall be bounded (e.g. subcomposition ladder via `itertools.islice`); no recursion without a static bound. | SYS-009 |

## 3 Control (GPCC)
| ID | Requirement | Traces |
|---|---|---|
| HGS-SW-007 | The GPCC shall expose only the whitelisted primitive set (SELECT/ADD/DROP_CARRIER, SET_PARAM, SET_FUSION_WEIGHTS, APPLY_DELTA, SET_ZERO_TREATMENT, FREEZE/UNFREEZE, ROLLBACK). | SYS-004 |
| HGS-SW-008 | GPCC commands shall be delivered as cFS **Table Services** + **Stored Command**; bounds enforced by **Limit Checker**; ingest via **Command Ingest** (CCSDS). | SYS-004, SYS-018 |
| HGS-SW-009 | Each command shall be versioned, hash-stamped, event-logged, and reversible. | SYS-014 |
| HGS-SW-010 | Structure-altering commands shall require an authorised (two-key) path. | SYS-005 |

## 4 Supervision (Coherence Supervisor)
| ID | Requirement | Traces |
|---|---|---|
| HGS-SW-011 | Each sensor CNT shall run as an **independent cFS application** on the software bus. | SYS-002 |
| HGS-SW-012 | The Supervisor shall verify the **tiling cocycle** (shared-part agreement) across overlapping charts every cycle. | SYS-006 |
| HGS-SW-013 | The Supervisor shall perform voting, FDIR, and SAFE-mode arbitration (cFS Health & Safety class), with memory scrubbing (Checksum/Memory Manager). | SYS-013, SYS-015 |
| HGS-SW-014 | The Supervisor shall rank facets by activation for **smart-downlink** (carrier filter). | SYS-010 |

## 5 Assurance
| ID | Requirement | Traces |
|---|---|---|
| HGS-SW-015 | Every algorithm shall exist in the **four forms** (Python + R + pseudocode + HUF-STD-002 spec) for independent re-implementation. | SYS-020 |
| HGS-SW-016 | Event log + hash chain (cFS Event + File services) shall record every command and state transition. | SYS-008, SYS-014 |
| HGS-SW-017 | Code shall follow a MISRA-style, bounded, branch-free-where-feasible standard amenable to formal verification. | SYS-009, SYS-020 |

*Draft SRS — detailed FDIR logic in HGS-005; interfaces in HGS-004.*
