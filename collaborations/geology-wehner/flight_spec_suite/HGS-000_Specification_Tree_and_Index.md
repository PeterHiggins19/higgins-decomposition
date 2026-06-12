# HGS-000 — Specification Tree & Document Index
### Hs Geosensing Instrument (HGS) — deterministic compositional geosensing for field and flight

| | |
|---|---|
| **Document** | HGS-000 Specification Tree & Document Index (controlling document) |
| **Program** | HGS — Hs Geosensing Instrument |
| **Revision** | Draft A · 2026-06-09 |
| **Status** | DRAFT · Pre-Phase A (concept) · working tree (publication at author's gate) |
| **Author** | Peter Higgins (human author). AI-assisted per HUF-STD-001 (AI Use Declaration); AI tools are not authors. |
| **Classification** | Public · no personal/contact data (HUF carrier-filter governance) |

## 1 Purpose
This document is the **controlling index and specification tree** for the HGS program: a deterministic, expert-steerable **compositional geosensing instrument** built on the Higgins Decomposition (Hs / CN-TT). It defines the document set, their relationships, status, applicable standards, and the TBD/TBR register. Per NASA systems-engineering practice (NPR 7123.1), every lower-tier specification traces to this tree.

## 2 What HGS is (one paragraph)
A multi-sensor probe whose composition stream is navigated by one deterministic CNT per sensor, fused by reliability (calibrated by onsite samples), with the core vector-space (quaternion) computation locked in hardware. It is **purpose-built to be a directed instrument, testable in stages** — the same article serving as a field tool today and a flight demonstrator tomorrow.

## 3 Applicable & reference documents
- **NPR 7120.5** (Program/Project Management), **NPR 7123.1** (Systems Engineering), **NPR 7150.2** (Software Engineering), **NASA-STD-8739.8** (Software Assurance & Safety).
- **CCSDS** telecommand/telemetry standards; NASA **core Flight System (cFS)**; triple-modular-redundancy practice.
- **HUF-STD-002** (Tensor Train I/O), **HUF-STD-001** (Publication / AI Use Declaration), **HUF-STD-003** (Linear-Algebra Foundations).
- HGS context: `../00_EXECUTIVE_OVERVIEW.md`, `../CNTT_FLIGHT_CONTROL_SPEC.md`, `../GEOSENSING_CONCEPT_PROPOSAL.md`, `../GEOSENSING_FLIGHT_ROADMAP.md`, `../FIELD_MULTISENSOR_TOOL_CONCEPT.md`.

## 4 Specification tree (document set)
| Doc ID | Title | Tier (NPR 7123.1) | Status |
|---|---|---|---|
| **HGS-000** | Specification Tree & Document Index *(this doc)* | controlling | Draft A |
| **HGS-001** | Concept of Operations (ConOps) | Level 0 | Draft A |
| **HGS-002** | System Requirements Document (SRD) | Level 1 | Draft A |
| **HGS-003** | Software Requirements Specification (SRS) | Level 2 | Draft A |
| **HGS-004** | Interface Control Document (ICD) | Level 2 | Draft A (outline + key IFs) |
| **HGS-005** | Fault Management / FDIR Plan | Level 2 | Draft A (refs CNTT_FLIGHT_CONTROL_SPEC) |
| **HGS-006** | Verification & Validation Plan + Verification Cross-Reference Matrix (VCRM) | Level 2 | Draft A |
| **HGS-007** | Software Assurance & Configuration Management Plan | Level 2 | Draft A |
| **HGS-008** | Development Plan & Staged Test Route (incl. the proposal to M. Wehner) | Level 1 | Draft A |

## 5 Convention — TBD / TBR
Per NASA practice: **TBD** = To Be Determined (value not yet known); **TBR** = To Be Resolved (placeholder value subject to change). Every TBD/TBR is registered in §6 and must be retired before the corresponding milestone gate (see HGS-008).

## 6 TBD/TBR register (open)
| Tag | Item | Owner | Retire by |
|---|---|---|---|
| TBR-01 | Mission class of the first flight (CubeSat / lander / rover payload) | program | L-4 Instrument Definition |
| TBD-02 | Flight processor selection (HPSC / VPU / rad-hard FPGA) | program | L-3 Breadboard |
| TBD-03 | Sensor suite for the purpose-built apparatus | M. Wehner + program | L-4 |
| TBR-04 | Determinism numeric profile (fixed-point vs canonical-float) | Hs | L-2 HIL |
| TBD-05 | Field calibration transfer functions + reliability weights | M. Wehner | L-6 Field |
| TBR-06 | Downlink-reduction and latency performance targets | program | L-3 |

## 7 Governance & honesty
Hs computes; **HUF governs what is released** (carrier filter / need-to-know). Claim tiers travel with every requirement (confirmed / experimental / to-be-earned). This is a **concept-stage draft specification suite**, not a flight-certified baseline, not a funded program, and not a statement of any agency's involvement.

*The instrument reads. The expert decides. The hashes carry the receipts.*
