# HGS-001 — Concept of Operations (ConOps)
**Program:** HGS · **Rev:** Draft A · 2026-06-09 · **Status:** DRAFT Pre-Phase A · **Refs:** HGS-000

## 1 Scope
How the Hs Geosensing Instrument is used operationally, across its staged life: hand-held field tool → ground reprocessing service → onboard flight demonstrator. One article, one architecture, three operating regimes.

## 2 Operating concept
A **multi-sensor probe** (camera, magnetometer, GPS/IMU, + Raman/pXRF clip-on) is moved across a target (an outcrop, a core, a planetary surface). Each sensor stream is navigated by **one deterministic CNT**; streams are **fused by reliability** (weights set by calibration); the **Coherence Supervisor** votes redundant engines, checks the tiling-coherence law, and decides what to report/downlink. The operator (or the autonomy layer) steers via the **Geologist Protocol Control Code (GPCC)**.

## 3 Operational modes
| Mode | Description | Entry / exit |
|---|---|---|
| **NOMINAL** | Continuous multi-sensor navigation; per-step boundary/driver/regime output. | default |
| **CALIBRATION** | Onsite grab-sample(s) set reliability weights + delta-corrections; GPCC `SET_FUSION_WEIGHTS`/`APPLY_DELTA`. | operator/scheduled |
| **DISCOVERY/RECONFIG** | New carrier added on a discovery; structure vector space updated (GPCC `ADD_CARRIER`), atlas grows facets. | authorised command |
| **AUTONOMY** | High activation-coefficient anomaly cues a sample/closer look (sense → sample). | flag-driven (flight only) |
| **SAFE** | Roll back to last-good hash-stamped config; hold; await ground. | fault / watchdog |

## 4 Operational scenarios
- **S1 · Field (now-near):** geologist walks a wall; the device maps layer boundaries + driving element live; a few hammer samples calibrate it. *(L-6 test route.)*
- **S2 · Ground reprocessing:** the same engine runs over EMIT/CRISM hyperspectral archives, producing a navigation/regime layer benchmarked against known mineral maps. *(L-5.)*
- **S3 · Onboard demonstrator:** the hardware-locked engine runs on a flight processor; GPCC commands uplinked as parameter tables; facets + flags downlinked (smart-downlink); the **ground digital twin** mirrors the flight engine bit-for-bit for pre-validation and review. *(L-2..L.)*

## 5 Stakeholders / actors
Field geologist (operator + calibrator + interpreter — M. Wehner as the domain lead); mission operations (uplink/telemetry, ground twin); the instrument autonomy layer; reviewing organisations (USGS ground science; NASA flight). The instrument **reports**; the expert **interprets** — meaning is never assigned by the instrument.

## 6 Key operational constraints
Deterministic, bounded, auditable at all times; no opaque self-modification; every adaptation logged + reversible; bandwidth-limited downlink (delta/triage native); power-limited (adaptive facet resolution).

*Draft ConOps — operational specifics carry TBD/TBR per HGS-000 §6.*
