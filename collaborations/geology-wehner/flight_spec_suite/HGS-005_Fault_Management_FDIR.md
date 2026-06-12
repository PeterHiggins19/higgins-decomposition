# HGS-005 — Fault Management / FDIR Plan
**Program:** HGS · **Rev:** Draft A · 2026-06-09 · **Status:** DRAFT Pre-Phase A · **Refs:** HGS-002/003, `../CNTT_FLIGHT_CONTROL_SPEC.md` (detailed control/coherence design)

## 1 Scope
Fault Detection, Isolation, and Recovery (FDIR) for the HGS instrument. The Coherence Supervisor is the fault-management authority.

## 2 Fault classes & responses
| Class | Detection | Isolation | Recovery |
|---|---|---|---|
| **Single-event upset (bit flip)** | deterministic-replay recompute-and-compare; content-hash mismatch; voting disagreement | identify the divergent engine/module | scrub memory; re-run; outvote |
| **Sensor fault / drift** | per-sensor CNT departs consensus / calibration; tiling-cocycle violation | localise to the sensor (shared-part disagreement) | downweight (fusion); flag; request recalibration (GPCC) |
| **Method drift ("us")** | calibration residual exceeds bound | n/a | `APPLY_DELTA` correction (logged), or escalate to operator |
| **Config / command fault** | bounds rejection (Limit Checker); cocycle/consistency failure post-command | last command | reject + log; or `ROLLBACK` to last-good config |
| **Processor / watchdog** | watchdog timeout; health beacon loss | module | reset; failover to redundant module; SAFE mode |

## 3 Redundancy approach
- **N-modular redundancy** with per-output voting (triple-modular baseline, as on contemporary flight computers).
- **Deterministic-replay self-check** — because the engine is deterministic + hash-stamped, an upset is caught by recomputing and comparing, giving redundancy coverage at reduced silicon cost (see CNTT_FLIGHT_CONTROL_SPEC Part-I §1).
- **Memory scrubbing** via cFS Checksum / Memory Manager.

## 4 SAFE mode
SAFE mode = **roll back to the last-good hash-stamped configuration** and hold, emitting health telemetry, awaiting ground/GPCC. Because configs are content-addressed, the recovered state is *provably* the intended one. Rollback target latency **TBR-07**.

## 5 Autonomy interaction
The sense → sample autonomy cue (high activation-coefficient anomaly) is **suspended** in SAFE mode and gated by the Supervisor in NOMINAL mode; it never overrides fault response.

*Draft FDIR — fault tree + FMECA to be completed at L-4/L-3; latencies are TBR.*
