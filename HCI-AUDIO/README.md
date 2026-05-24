# HCI-AUDIO — Higgins Compositional Instrument for Audio Systems

**Status:** canonical sibling tier, doctrine-only (push #24, 2026-05-08).
**Sibling of:** [`HCI-CNT/`](../HCI-CNT/), [`HCI-CNQ/`](../HCI-CNQ/), and the [`HCI/`](../HCI/) instrument family.
**Origin:** direct modern descendant of the original DADC (Dimension-Apportioned Diffraction Correction) work documented in the [Rogue-Wave-Audio repository](https://github.com/PeterHiggins19/Rogue-Wave-Audio). See [`../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md) and the master-standard flagship paper [`../papers/flagship/GROUND_STATE_AND_TRACTION.md`](../papers/flagship/GROUND_STATE_AND_TRACTION.md) v2.2 — the latter formalises the unified isotropic-radiation ground-state formula that the BTL acoustic apparatus has been measuring continuously.
**Engine status:** no compiled engine yet. Doctrine and design specifications only. The `cnt.py` engine (canonical) produces the underlying compositional data; HCI-AUDIO is the application layer.

> **🛡️ Verify before you trust.** The underlying CNT and CNQ engines ship in four forms (Python + R + language-agnostic pseudocode + HUF-STD-002 specification). See [`../TRUST_AND_VERIFICATION.md`](../TRUST_AND_VERIFICATION.md). HCI-AUDIO doctrine documents in this folder describe *how the engine output is applied* to the loudspeaker-listening-position problem; the engine itself is independently verifiable from the pseudocode without running the published code.

---

## What this folder is

This is the canonical home for **applied audio work** in the Hˢ system: 4-way active loudspeaker alignment, room correction at the listening position, and any acoustic-system optimisation that uses the CNT/CNQ machinery on real audio data.

The headline use case is the active flagship application:

- 4 physical drivers per cabinet (woofer / mid-woofer / midrange / tweeter)
- Classical filters: low-pass EQ + 4th-order Butterworth crossovers
- Crossover partitions mapped to **ERB (equivalent rectangular bandwidth) psychoacoustic bands** rather than arbitrary engineering bands
- Per-driver level, phase, and time-delay control
- Diffraction measured at the **listening position** (not near-field)

Everything here is built on the same simplex closure principle that began at BTL — the Binaural Test Lab — with the 6.02 dB diffraction budget.

---

## How this relates to DADC (the historical origin)

The original DADC question was:

> *Which of the three cabinet dimensions is currently carrying most of the fixed 6.02 dB diffraction budget?*

The HCI-AUDIO question for a 4-way active system at the listening position is the same question, generalised:

> *Which driver, in which ERB band, is currently dominating the perceptual energy and phase steering at the listener's ear?*

The fixed total is no longer a near-field 6.02 dB; it is the perceptual energy arriving at the listening position. The parts are no longer three cabinet dimensions; they are ERB bands × driver contributions. The closure rule remains.

---

## Folder map

```
HCI-AUDIO/
├── README.md                       (this file)
├── HCI-AUDIO_ADMIN.json            tier admin and provenance (push #24)
│
├── doctrine/                       what HCI-AUDIO measures and why
│   ├── ERB_BAND_MAPPING.md         ERB carriers, 40-band recommended config, perceptual weighting
│   ├── QUATERNION_PHASE_MAPPING.md phase + time delay as quaternion / joint quaternion field
│   ├── HELMSMAN_AT_LISTENING_POS.md per-driver, per-band, and joint helmsman extraction
│   └── ALIGNMENT_TARGETS.md        metric definitions for what a "well-aligned" 4-way system looks like
│
└── spec/                           specifications for future engines / pipelines
    ├── PSYCHOACOUSTIC_4WAY_ADAPTER_SPEC.md  adapter that takes WAV/measurement → canonical compositional
    └── PIPELINE_SPEC.md            how HCI-AUDIO output flows through CNT then CNQ
```

---

## What's here today (push #24)

This is a **doctrine-only** scaffold. The folder exists so that when pilot work lands it has a canonical home, and so that the framework's claims about applied audio are testable and citable. Specifically:

- The doctrine documents define the carriers (40 ERB bands × 4 drivers), the phase/time-delay mapping into the quaternion algebra, and the alignment metrics that a future implementation must produce.
- The spec documents define the input format for measurement data and the pipeline through CNT → CNQ.
- No compiled adapter, no example datasets, no journals yet. Those land in subsequent pushes when pilot measurements are run.

---

## What's *not* here yet

- Compiled `Psychoacoustic4WayAdapter` (only the spec).
- Reference measurement datasets.
- Per-experiment journals (no experiments yet).
- Validation against real 4-way systems.
- Integration with audio measurement tools (Smaart, REW, etc.).

These are the next pilots. Until one lands, the doctrine here is testable in the same sense that Volume IV was testable before HCI-CNQ was promoted: the math is laid out, the predictions are stated, and the measurements that would falsify or confirm it are specified.

---

## Why this is its own tier (and not just a folder under HCI-CNQ)

The CNQ tier is general (applies to any quaternion-lifted compositional system). HCI-AUDIO has its own tier because:

- It has a specific carrier convention (ERB bands × drivers) that is not part of the general CNQ vocabulary.
- It has a specific measurement convention (listening-position, not near-field) that is not part of CNT's default usage.
- It is the historical home of the entire framework — promoting it to a sibling tier honours that lineage explicitly.
- Future audio-specific tooling (psychoacoustic adapters, room-correction pipelines, calibration utilities) belongs here, not in HCI-CNQ.

---

## Pointers

- Origin lineage: [`../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md)
- CNT engine (used as the back-end for HCI-AUDIO data flow): [`../HCI-CNT/`](../HCI-CNT/)
- CNQ tier (used for the quaternion / joint-helmsman parts): [`../HCI-CNQ/`](../HCI-CNQ/)
- Helmsman-family vocabulary (proposed extensions): [`../HCI-CNT/handbook/GLOSSARY.md`](../HCI-CNT/handbook/GLOSSARY.md) §I
- Original work: https://github.com/PeterHiggins19/Rogue-Wave-Audio

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
*From a 6.02 dB diffraction budget to ERB bands at the listening position — the same closure principle, applied at the right scale.*
