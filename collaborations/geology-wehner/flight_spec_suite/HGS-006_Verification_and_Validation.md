# HGS-006 — Verification & Validation Plan + Verification Cross-Reference Matrix (VCRM)
**Program:** HGS · **Rev:** Draft A · 2026-06-09 · **Status:** DRAFT Pre-Phase A · **Refs:** HGS-002, HGS-008 (stages)

## 1 Approach
Verification is **staged** along the development route (HGS-008): each requirement is verified at the earliest stage where evidence is available, and re-verified at integration. The **ground digital twin** is a primary V&V asset — it reproduces flight outputs bit-for-bit, so many requirements are verifiable on the ground before flight. Methods: **T**est, **A**nalysis, **I**nspection, **D**emonstration.

## 2 Validation (are we building the right thing?)
Validated against the ConOps scenarios (HGS-001 §4): S1 field (geologist + grab-samples), S2 ground reprocessing (vs known mineral maps), S3 onboard demonstrator. **Domain validation authority: the geologist (M. Wehner).** The instrument's outputs are validated by correspondence with independently known geology — not by the instrument's own assertion.

## 3 Verification Cross-Reference Matrix (representative)
| Requirement | Method | Stage | Evidence |
|---|---|---|---|
| SYS-001 navigation correct | T | L-7 (now) | reproducible Frielingen-9 demo |
| SYS-002 one CNT per sensor | T | L-7 | geosensing simulation |
| SYS-003 reliability-weighted fusion | T,D | L-6 | field calibration w/ Matthew |
| SYS-004 GPCC bounds-checked | T | L-4/L-3 | command-table tests |
| SYS-007 determinism (bit-identical) | T | L-7→L-2 | hash reproduction; twin parity |
| SYS-008 hash provenance | I,T | L-7 | content_sha256 in outputs |
| SYS-009 bounded computation | I,A | L-7 | code inspection (islice; no unbounded recursion) |
| SYS-010 smart-downlink reduction | A,T | L-3 | benchmark on EMIT-class data |
| SYS-013 N-modular redundancy | T | L-2 | HIL voting tests |
| SYS-014 reversible / SAFE rollback | T,D | L-2 | twin rollback demo |
| SYS-016 environment survival | T | L-1 | rad/TVAC/vibration |
| SYS-019 ground twin parity | T,D | L-2 | flight-vs-twin bit-exact |
| SYS-020 NPR 7150.2 / 8739.8 assurance | I | all | audit per HGS-007 |

## 4 Notes
Several core requirements (SYS-001/002/007/008/009) already have **L-7 evidence in hand** (this session's reproducible demo, hash provenance, and the geosensing simulation). The remainder retire at their staged gates. Independent re-verification is enabled by the four-form code discipline (HGS-SW-015).

*Draft V&V — full VCRM covers every requirement at baseline.*
