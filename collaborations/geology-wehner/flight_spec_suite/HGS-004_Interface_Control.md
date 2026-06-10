# HGS-004 — Interface Control Document (ICD)
**Program:** HGS · **Rev:** Draft A · 2026-06-09 · **Status:** DRAFT Pre-Phase A (outline + key interfaces) · **Refs:** HGS-000/002/003

## 1 Scope
Defines the HGS internal and external interfaces. Detailed signal/packet definitions are TBD pending instrument and platform selection (TBR-01, TBD-02).

## 2 Interface register
| IF ID | From → To | Type | Content | Standard | Status |
|---|---|---|---|---|---|
| IF-1 | Sensor → Adapter | data | raw sensor reading (spectral / scalar / image) | sensor-native | TBD-03 |
| IF-2 | Adapter → Engine | data | compositional vector `[t, carrier_1..D]` | HUF-STD-002 Link-1 | defined |
| IF-3 | Engine → Supervisor | data | canonical CNT/CNQ JSON + `content_sha256` | HUF-STD-002 | defined |
| IF-4 | Ground → Instrument (uplink) | command | GPCC parameter/command tables | CCSDS TC · cFS Table/Stored-Cmd | defined (schema TBD) |
| IF-5 | Instrument → Ground (downlink) | telemetry | ranked facets + health + event/hash log | CCSDS TM · smart-downlink | defined (rates TBR-06) |
| IF-6 | Instrument ↔ Ground Digital Twin | sync | config + command + input log for bit-exact replay | hash-addressed | defined |
| IF-7 | Engine apps ↔ Supervisor | IPC | software-bus messages | cFS Software Bus | defined |
| IF-8 | Instrument → Platform | power/mech/thermal | envelopes | platform ICD | TBD-09 |

## 3 Key rules
- **IF-2/IF-3** are the stable, standard-defined core (the Tensor Train contract); they do not change with platform.
- **IF-4** carries *only* whitelisted GPCC primitives, bounds-checked (HGS-SW-008).
- **IF-6** is unique to a deterministic engine: the twin replays from the hash-addressed log to reproduce flight state exactly.

*Draft ICD — packet/signal tables to be completed at L-4 Instrument Definition.*
