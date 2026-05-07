# Handbook — three consolidated volumes

The canonical CNT documentation. Three volumes, each self-contained and
citable, that together cover the system end-to-end.

| Volume | Audience | Length |
|---|---|---|
| [Volume I — Theory and Mathematics](VOLUME_1_THEORY_AND_MATHEMATICS.md) | Mathematicians, reviewers | 16k words |
| [Volume II — Practitioner and Operations](VOLUME_2_PRACTITIONER_AND_OPERATIONS.md) | Users running the system | 24k words |
| [Volume III — Verification, Reference and Release](VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md) | Reviewers, journals, partner labs | 8k words |

---

## 🆕 Two access protocols sit in front of these volumes (May 2026)

You do not have to read the volumes to *use* CNT. Two new protocols give
both human researchers and AI assistants a guided on-ramp:

- **CCTT v1.0** — [`../../ai-refresh/CCTT_QUICKSTART.md`](../../ai-refresh/CCTT_QUICKSTART.md) → [`CCTT_RUNBOOK.md`](../../ai-refresh/CCTT_RUNBOOK.md). A 7-phase protocol for producing a CNT-grade analysis end-to-end from any compositional dataset, in either User-mode or User + AI-mode. Internally references the volumes only when depth is needed.
- **OPERATIONS_PROTOCOL v1.0** — [`../../OPERATIONS_PROTOCOL.md`](../../OPERATIONS_PROTOCOL.md). Front-door map of every operational transition in the repo (analysis, push, cowork session start/end, AI cold-start, recovery paths).

The volumes below are the *canonical reference*; the protocols above are the
*runtime guide*. Both share the same source of truth.

---

## Volume I — Theory and Mathematics

Foundations of compositional-data analysis (Aitchison, Egozcue,
Pawlowsky-Glahn) and how CNT extends them. Schema 2.1.0, doctrine v1.0.1
(integer orders, round-up rule), pseudocode for both the engine and
Stage 2, side-by-side balance against classical CoDa, and the glossary.

## Volume II — Practitioner and Operations

How to run the system end-to-end. Atlas (Stage 1, 2, 3, 4 + spectrum +
projector), Mission Command + module pipeline, adapters disclosure,
25-experiment walkthrough, conference demo package, ROI / use-case
decisions, Hs-Lab integration plan, raw-data swap-in checklist. **CCTT
phase 2 (adapter selection or generation) routes here for adapter
templates and disclosure conventions.**

## Volume III — Verification, Reference and Release

Determinism contract, hash-chain verification proposal to the CoDa
community, CodaWork 2026 talk plan + Q&A study list, public-trial
readiness audit, citations, license. **CCTT phase 6 (the gate) and
OPERATIONS_PROTOCOL Section 10 (corpus-drift recovery) route here for
the formal determinism semantics.**

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
