# HGS-002 — System Requirements Document (SRD)
**Program:** HGS · **Rev:** Draft A · 2026-06-09 · **Status:** DRAFT Pre-Phase A · **Refs:** HGS-000, HGS-001

## 1 Scope
Level-1 system requirements for the Hs Geosensing Instrument. Verification methods: **T**=Test, **A**=Analysis, **I**=Inspection, **D**=Demonstration. Tier: confirmed / design / earn. TBD/TBR per HGS-000 §6.

## 2 Functional
| ID | Requirement | Verify | Tier |
|---|---|---|---|
| HGS-SYS-001 | The system shall compute compositional navigation (Aitchison step, helmsman, K_eff, regime tripwire) per HUF-STD-002. | T | confirmed |
| HGS-SYS-002 | The system shall ingest ≥ 2 sensor streams and run **one CNT instance per stream**. | T | confirmed |
| HGS-SYS-003 | The system shall fuse per-sensor results by **reliability weights** derived from onsite calibration samples. | T,D | design |
| HGS-SYS-004 | The system shall accept **GPCC** commands only from a whitelisted, bounds-checked primitive set; out-of-bounds commands shall be rejected and logged. | T | design |
| HGS-SYS-005 | On a discovery, the system shall reconfigure the **structure vector space** (add/drop carrier) via an authorised GPCC command, deterministically. | T,D | design |
| HGS-SYS-006 | The Coherence Supervisor shall verify cross-engine consistency (tiling cocycle) and isolate faults each cycle. | T | design |

## 3 Performance & determinism
| ID | Requirement | Verify | Tier |
|---|---|---|---|
| HGS-SYS-007 | The system shall be **deterministic**: identical input + config → bit-identical output and content hash. | T | confirmed (principle) |
| HGS-SYS-008 | Every output shall be **hash-stamped**, binding input → method → config → output. | I,T | confirmed |
| HGS-SYS-009 | Computation shall be **bounded** (no unbounded loops/recursion; fixed-size kernels). | I,A | confirmed |
| HGS-SYS-010 | The system shall downlink decision-relevant facets ranked by activation, achieving ≥ **TBR-06** reduction vs raw. | A,T | earn |
| HGS-SYS-011 | Per-cycle latency shall be ≤ **TBR-07** on the selected processor (TBD-02). | T | earn |
| HGS-SYS-012 | Facet resolution shall adapt to the available **power** budget (TBD-08). | A,T | design |

## 4 Dependability & environment
| ID | Requirement | Verify | Tier |
|---|---|---|---|
| HGS-SYS-013 | The system shall provide **N-modular redundancy** with per-output voting, augmented by **deterministic-replay** self-check. | T | design |
| HGS-SYS-014 | Every configuration change shall be versioned, logged, and **reversible**; SAFE mode = rollback to last-good hash-stamped config. | T,D | sound |
| HGS-SYS-015 | On detected fault, the system shall enter SAFE mode within **TBR-07**. | T | design |
| HGS-SYS-016 | The system shall survive the mission radiation / thermal / vibration environment (**TBD-10**). | T | earn |
| HGS-SYS-017 | The system shall operate within **TBD-09** mass/volume/power envelopes. | A,I | TBD |

## 5 Interfaces & assurance
| ID | Requirement | Verify | Tier |
|---|---|---|---|
| HGS-SYS-018 | The system shall command/telemeter over **CCSDS** and run as **cFS** applications. | I,T | design |
| HGS-SYS-019 | A **bit-exact ground digital twin** shall reproduce any flight output and pre-validate any GPCC command before uplink. | T,D | sound |
| HGS-SYS-020 | Software shall be engineered and assured per **NPR 7150.2** and **NASA-STD-8739.8**, with claim tiers and an AI Use Declaration (HUF-STD-001). | I | design |

*Draft SRD — a representative Level-1 set; full decomposition + TBD/TBR retirement at the milestone gates (HGS-008).*
