# Psychoacoustic 4-Way Adapter — Specification

**Status:** specification, push #24 (2026-05-08). Implementation is the next milestone.
**Companion docs:** doctrine documents in [`../doctrine/`](../doctrine/), pipeline spec in [PIPELINE_SPEC.md](PIPELINE_SPEC.md).

---

## Purpose

`Psychoacoustic4WayAdapter` is the canonical input adapter for HCI-AUDIO. It takes raw acoustic measurements at the listening position (multi-channel audio, FRF data, or measurement-tool exports) and produces a canonical compositional dataset matching the schema used by the existing CNT engine (`HCI-CNT/engine/cnt.py`).

The adapter sits at the same architectural position as `AcousticAdapter` (proposed) and `EMAdapter` in the broader WaveMechanics-CNQ design — but it is specialised for the 4-driver psychoacoustic case.

---

## Inputs

| Input | Format | Notes |
|---|---|---|
| Multi-channel WAV recording | 4-channel WAV at the listening position | one channel per driver, OR a single composite recording if drivers are not separable |
| Measurement export | FRF (frequency response function) per driver | preferred for active systems where each driver can be measured independently |
| Smaart / REW export | CSV or vendor format | wrapper functions handle conversion |
| Configuration JSON | crossover frequencies, slopes, target ERB bands | drives the partitioning |

---

## Processing pipeline

1. **Load** measurement data and validate format.
2. **Per-driver processing**: apply the measurement-time crossover filter, EQ, level, phase, and time delay to recover each driver's contribution at the listening position.
3. **ERB binning**: bin per-driver intensity / power into 40 ERB bands per `../doctrine/ERB_BAND_MAPPING.md`.
4. **Loudness weighting** (optional): apply Moore-Glasberg or ISO 226 weighting to convert intensity to perceived loudness.
5. **Per-band per-driver matrix**: assemble a [40 bands × 4 drivers] matrix of intensity / loudness contributions.
6. **Simplex closure** along the band axis: each row (one ERB band) closes to sum 1 across the 4 drivers; multiplicative ε = 1e-10.
7. **Joint quaternion lift** per band: build q_joint(band) per `../doctrine/QUATERNION_PHASE_MAPPING.md`.
8. **Hash everything**: content_sha256 over the canonical output.

---

## Outputs

The adapter writes a canonical JSON file matching the structure used by HCI-CNT experiments, with HCI-AUDIO-specific extensions:

```json
{
  "experiment_id": "HCI-AUDIO-XXX",
  "domain": "PSYCHOACOUSTIC_4WAY",
  "carriers": {
    "primary": "ERB_psychoacoustic_bands",
    "count": 40,
    "secondary": "per_driver",
    "drivers": ["Woofer", "MidWoofer", "Midrange", "Tweeter"]
  },
  "data": {
    "per_band_per_driver": "[[40 x 4]] intensity / loudness matrix",
    "simplex_closed": true
  },
  "joint_quaternion_field": {
    "per_band_q_joint": "[[40 unit quaternions]]",
    "global_q_joint_trajectory": "[T x 4] across measurement frames"
  },
  "metadata": {
    "listening_position_geometry": "...",
    "measurement_microphone": "...",
    "room_temperature_C": "...",
    "crossover_config": "...",
    "diffraction_correction_applied": true
  },
  "content_sha256": "..."
}
```

---

## Validation criteria for first pilot

The first pilot of the adapter (when implementation lands) is considered validated when:

1. The same measurement, processed twice with the same config, produces bit-identical content_sha256 (same input → same output, always — preserved from Hˢ-wide).
2. The simplex closure check passes: row sums of the [bands × drivers] matrix close to 1 within 1e-9.
3. The joint quaternion field is unit-norm at every band: |q_joint(band)| − 1 < 1e-12.
4. Helmsman extraction (per [`../doctrine/HELMSMAN_AT_LISTENING_POS.md`](../doctrine/HELMSMAN_AT_LISTENING_POS.md)) produces sensible values when run on a known-good measurement (e.g., a calibrated reference loudspeaker).

---

## Out of scope for this spec

- Specific Python implementation (lands when pilot work begins).
- Real-time / streaming versions of the adapter.
- Integration with specific measurement tool APIs.
- Calibration of the listening-position microphone setup.

---

*The spec defines what the adapter must produce. The implementation comes when the first pilot needs it.*
