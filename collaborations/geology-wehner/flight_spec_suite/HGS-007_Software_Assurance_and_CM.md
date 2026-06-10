# HGS-007 — Software Assurance & Configuration Management Plan
**Program:** HGS · **Rev:** Draft A · 2026-06-09 · **Status:** DRAFT Pre-Phase A · **Refs:** NPR 7150.2, NASA-STD-8739.8, HUF-STD-001/002

## 1 Software assurance
- Engineered and assured per **NPR 7150.2** (software engineering) and **NASA-STD-8739.8** (software assurance & software safety).
- **Four-form discipline** (Python + R + language-agnostic pseudocode + formal HUF-STD-002 I/O spec) enables independent re-implementation and cross-checking — a standing assurance asset.
- **Bounded, deterministic, MISRA-style** code amenable to static analysis and (for the kernel) formal verification.
- **Claim tiers** (confirmed / experimental / not-implemented) attached to every output and requirement; no tier inflation.
- **AI Use Declaration** per HUF-STD-001: AI tools assist build/documentation/verification; **human-only authorship**; AI tools are not authors; the human is the sole commit authority.

## 2 Configuration management — the hash chain as CM backbone
- Every engine output, every config, and every GPCC command is **content-addressed (SHA-256) and hash-chained**. This *is* the configuration identification + status accounting: any artifact is traceable to its exact inputs, method version, and authorising command.
- **Baselines** are sets of content hashes; **rollback** = select a prior baseline hash (provably the intended state).
- Change control: human-gated; structure-altering changes via the two-key authorised path (HGS-SW-010); the standing push/commit protocol governs repository baselines.
- **Provenance/audit:** the event + hash log (cFS Event + File services) gives a complete, replayable record for ground review.

## 3 Reviews & gates
Standard milestone reviews (SRR/PDR/CDR analogues) align to the HGS-008 stage gates; each gate retires its TBD/TBR set (HGS-000 §6) and re-runs the VCRM (HGS-006).

*Draft Assurance/CM — formal SA/CM artifacts produced at project formulation (Phase A→B).*
