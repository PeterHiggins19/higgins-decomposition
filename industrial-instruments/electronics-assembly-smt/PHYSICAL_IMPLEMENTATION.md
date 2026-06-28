# Physical implementation — how to actually accomplish it (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑23. A proposed
physical path from "the math fits" to "a running sensing‑and‑control skin on a real line." Planning‑stage; fill
in as ideas land. Honest‑broker tiered; nothing posted; Peter is the sole gate.*

---

## 1. The principle — a retrofit sensing skin, not a rip‑and‑replace

The machines already carry the sensors. The physical implementation is a **read‑only sensing skin + an
advisory/closed‑loop edge node**, overlaid on existing telemetry — Hˢ reads what the machine already produces,
composes it, and reports. *Instrument‑not‑data: Hˢ reads; the machine and the operator decide.*

## 2. The layers (sense up · control down · operator at top)

```
   [ sensors already on the machine ]  ── existing taps ──►  EDGE NODE (per cell)
   dispense: flow/pressure/weight/vision/X-ray                ├─ ingest streams (read-only)
   placement: vision feedback (theta,dx,dy), feeder, thermal  ├─ compose -> Hs read -> the sentence + receipt
                                                              ├─ silent-drift / 6-DOF / deformation
                                                              └─ advisory OR setpoint-nudge (behind Breaker 16)
        EDGE NODES ──► LINE NODE (composition of cells) ──► PLANT NODE (composition of lines)
                            cross-verify by hash                governing node + operator HMI (Breaker 16)
```

## 3. The data tap (how to read the machine)

- **Standard interfaces:** SECS/GEM, OPC‑UA, MQTT, the machine's CSV/log exports, or a vision/X‑ray image
  stream — whichever the equipment already exposes. Read‑only first.
- **Compose:** map each stream to its conserved‑budget composition (the tables in `CONCEPT_AND_MATH.md`).
- **Run Hˢ:** closure → log‑ratio → kinematic read → coherence gate → SHA‑256 receipt; emit the language
  sentence (`ARROW·CHARACTER·EFF‑DIM·COHERENCE·FACES·RECEIPT`).

## 4. The hardware (modest, edge‑first)

- **Edge node per cell:** a small industrial compute (the Hˢ engine is light — numpy‑class). Runs the read,
  holds the local receipts, talks up to the line node.
- **Sensing‑skin add‑ons (optional, where the machine is blind):** strain/temperature/flow patches forming an
  external composition where internal telemetry is thin (the "skin of sensors" — more patches, more
  sensitivity).
- **Operator HMI:** shows the sentence + the arrow + the drift early‑warning; **Breaker 16** is a physical/UI
  interlock the operator holds — control flows down only when armed.

## 5. The staged build (test the journey; failure points the way)

1. **Read‑only pilot.** Tap one cell's existing telemetry → compose → Hˢ read → advisory only. Validate the
   silent‑drift early flag against real events (the decisive test).
2. **Advisory line.** Roll to a line; the line node reads the composition of cells, locates the worst,
   hash‑verifies each.
3. **Closed loop (gated).** Add the setpoint‑nudge SafeLoop behind Breaker 16 on the most tolerant parameter
   first; the operator stays the fixed point.
4. **Plant.** Compose lines; the governing node + operator HMI.

Each stage is small, reversible, and falsifiable — *a complex problem worth testing even if a stage fails,
because the failure points the way.*

## 6. Honest scope & tiers

- **T1 (measured precedents):** the silent‑drift early flag (`ca9e6c0d`), the closed loop (`c17e9ceb`), the
  6‑DOF and deformation reads.
- **T2 (reasoned):** this physical architecture and the staged build — sound, planning, unbuilt.
- **T3 (to earn):** any real‑line integration; any vendor relationship — none implied. Read‑only first; the
  operator holds Breaker 16; Hˢ is a complement, never a controller of record; safety dominant.

*Cross‑refs: `README.md`, `CONCEPT_AND_MATH.md`, `NORDSON_CASE.md`, `FUJI_SMT_CASE.md`, `ONBOARDING_FROM_ZERO.md`,
`../../papers/frontier/DISTRIBUTED_COMPOSITIONAL_ROBOTIC_SYSTEM.md`. Peter is the sole gate; nothing posted.*
