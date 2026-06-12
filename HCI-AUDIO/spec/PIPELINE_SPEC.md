# HCI-AUDIO Pipeline Specification

**Status:** specification, push #24 (2026-05-08).
**Companion docs:** [PSYCHOACOUSTIC_4WAY_ADAPTER_SPEC.md](PSYCHOACOUSTIC_4WAY_ADAPTER_SPEC.md), doctrine in [`../doctrine/`](../doctrine/).

---

## Pipeline architecture

HCI-AUDIO does not have its own engine. It is an **application layer** that flows through the existing CNT engine and (optionally) the CNQ tier.

```
Listening-position measurement (WAV / FRF / Smaart / REW)
        │
        ▼
Psychoacoustic4WayAdapter   (HCI-AUDIO/spec/PSYCHOACOUSTIC_4WAY_ADAPTER_SPEC.md)
        │  → canonical [40 ERB bands × 4 drivers] simplex matrix
        │  → joint quaternion field per band
        ▼
CNT engine (HCI-CNT/engine/cnt.py)
        │  → standard CNT JSON (depth towers, IR class, channels θ ω κ σ)
        │  → content_sha256
        ▼
HCI-AUDIO Helmsman extraction (per HCI-AUDIO/doctrine/HELMSMAN_AT_LISTENING_POS.md)
        │  → per-band, per-driver, joint helmsman + stability
        ▼
(Optional) CNQ joint analysis (HCI-CNQ/)
        │  → joint helmsman correlations across stereo / quad channels
        │  → CHSH-like S between channel pairs
        ▼
HCI-AUDIO Alignment report
        ↓
JSON output + alignment plot suite + per-experiment JOURNAL.md
```

---

## Inputs at each stage

| Stage | Input | Output |
|---|---|---|
| 1. Adapter | Raw measurement + config | Canonical compositional matrix [40 × 4] + per-band joint quaternion field |
| 2. CNT engine | Canonical matrix | Standard CNT JSON (existing engine, no changes) |
| 3. Helmsman extraction | CNT JSON + joint quaternion field | helmsman time series + stability metrics |
| 4. (Optional) CNQ joint | Multi-channel measurements (e.g. stereo) | Joint correlations between channels |
| 5. Report | All above | Alignment report against [`../doctrine/ALIGNMENT_TARGETS.md`](../doctrine/ALIGNMENT_TARGETS.md) |

---

## Determinism guarantees (preserved from Hˢ-wide contract)

- Same measurement input + same config → bit-identical content_sha256 at every stage.
- The CNT engine is unchanged from canonical 2.0.4. HCI-AUDIO does not modify it.
- The adapter and helmsman extraction are deterministic: closed-form, parameter-free, no fitting.
- The alignment report is a pure function of the upstream JSON + the targets in [`../doctrine/ALIGNMENT_TARGETS.md`](../doctrine/ALIGNMENT_TARGETS.md).

This is the same determinism contract that applies across the rest of the repo (handbook Volume III). HCI-AUDIO inherits it without modification.

---

## What this spec doesn't lock down

- The exact Python implementation of the adapter and helmsman extraction (lands with first pilot).
- The visualisation layer (plot conventions, dashboard layout) — engineering concern, not doctrinal.
- Specific format of the alignment report — likely a JOURNAL.md plus a JSON summary, but not committed.

---

*Pipeline = adapter → CNT → helmsman → (optional) CNQ → report. Each stage deterministic, hash-chained, traceable.*
