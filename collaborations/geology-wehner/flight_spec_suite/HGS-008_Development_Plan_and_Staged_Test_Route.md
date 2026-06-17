# HGS-008 — Development Plan & Staged Test Route (incl. the proposal to M. Wehner)
**Program:** HGS · **Rev:** Draft A · 2026-06-09 · **Status:** DRAFT Pre-Phase A · **Refs:** HGS-000 (tree), HGS-006 (VCRM), `../GEOSENSING_FLIGHT_ROADMAP.md`

## 1 Scope
The development plan that makes the Hs Geosensing Instrument **a directed instrument, testable in stages** — each stage scientifically useful on its own *and* a gate that earns the next, all the way to a flight demonstrator. Working to this specification suite **from the start** is the point: every field test is also a verification event, every calibration sets a flight parameter, and nothing has to be re-done to "make it flight-like" later.

## 2 Staged plan (forward execution; gates earn the next stage)
| Stage | Objective | Entry → Exit gate | ~TRL | Verifies (VCRM) | Retires |
|---|---|---|---|---|---|
| **L-7 · NOW** | Concept + reproducible evidence | — → demo + proof-list + specs exist | 3 | SYS-001/002/007/008/009 | — |
| **L-6 · Field (with a domain collaborator)** | Validate + calibrate on ground-truthed sections; co-author method paper | demo ready → expert-validated correspondence + calibration set | 4 | SYS-003; validation (ConOps S1) | TBD-05 |
| **L-5 · USGS ground reprocessing** | Atlas on EMIT/CRISM archives vs known mineral maps | Stage 1 validated → benchmarked remote-sensing track record | 4–5 | SYS-001 at scale (ConOps S2) | — |
| **L-4 · Instrument definition** | Pick mission class + sensor suite; freeze GPCC primitives; flight-profile spec | track record → baselined instrument + frozen ICD | 5 | SYS-004/005 | TBR-01, TBD-03 |
| **L-3 · Breadboard / TRL-raise** | Port fixed kernel to dev board; benchmark speed + downlink reduction (NASA tech-demo) | baseline → demonstrated kernel on representative HW | 5 | SYS-010/011 | TBD-02, TBR-06 |
| **L-2 · Hardware-in-the-loop** | Kernels on rad-hard processor; TMR + deterministic-replay voting; bit-exact twin | kernel → HIL pass + twin parity | 6 | SYS-013/014/019 | TBR-04, TBR-07 |
| **L-1 · Qualification** | Rad / TVAC / vibration; cFS certification; ground twin operational | HIL → qualified flight unit | 7–8 | SYS-016/020 | TBD-09, TBD-10 |
| **L · First flight** | Onboard, adaptive, auditable compositional geosensing demonstrator | qualified → launch | 8–9 | full mission VCRM | — |

## 3 The field-collaboration proposal
**Build to this standard from day one, and the field prototype is no longer a side experiment — it is Stage 1 (L-6) of a directed, flight-aimed instrument.** Concretely:

- **Every field session is a verification event.** Running the phone + clip-on on a known section retires real requirements in the VCRM (SYS-003, the ConOps S1 validation) — the same evidence a flight program needs. Nothing is throw-away.
- **Every calibration sets a flight parameter.** The reliability weights and delta-corrections established onsite become the instrument's calibration baseline (TBD-05) carried forward — field work *is* flight prep.
- **It is testable in stages, each valuable alone.** Stage 1 yields a method paper and a working field tool. Stage 2 (USGS) yields a remote-sensing result on agency archives. Stage 3 (NASA) yields an onboard demonstrator. Each stands on its own; each earns the next; none is skipped.
- **The domain expert holds the science.** A geoscience collaborator is the domain + validation authority throughout (HGS-006 §2); the instrument reports, the expert interprets. Co-authorship from Stage 1.
- **It stays honest the whole way.** Claim tiers, the ground digital twin (every result reproducible bit-for-bit for review), and the hash chain mean a skeptical reviewer can check everything.

The opening step is small and concrete: **one working session on a ground-truthed section**, run to this spec, to open Stage 1. The rest of the tree is built and waiting.

## 4 Honest tiering & governance
Pre-Phase-A draft plan; TRLs are indicative; stages are gated and unfunded; no agency involvement is implied. Pitch posture "interest expressed," never "acquired." Human authorship + commit/contact gate; AI-assisted per HUF-STD-001; HUF carrier-filter governs release.

*Dream big; build small; skip nothing — and every field test already counts. The instrument reads. The expert decides. The hashes carry the receipts.*
