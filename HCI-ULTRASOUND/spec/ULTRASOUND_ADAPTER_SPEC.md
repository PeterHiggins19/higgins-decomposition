# Ultrasound Adapter — Specification

**Status:** specification, push #24 (2026-05-08). Implementation is the next milestone.
**Companion docs:** doctrine in [`../doctrine/`](../doctrine/).

---

## Purpose

`UltrasoundAdapter` is the canonical input adapter for HCI-ULTRASOUND. It takes raw ultrasound return-signal data (multi-frequency, multi-element, time-domain, or beamformed) and produces a canonical compositional dataset matching the schema used by the existing CNT engine, with HCI-ULTRASOUND-specific extensions (joint quaternion field per measurement instant, range-gate metadata, etc.).

---

## Inputs

| Input | Format | Notes |
|---|---|---|
| Raw RF returns per element | Binary or HDF5 per-element time series | most flexible; allows custom beamforming |
| Pre-beamformed signal per angular sector | CSV or HDF5 | useful for single-element broadband probes |
| Range-gated power | CSV with [time-gate × frequency × angle] | post-processed standard format |
| Configuration JSON | probe geometry, frequencies, gating, target carrier set | drives the adapter |

---

## Processing pipeline

1. **Load** raw or pre-processed return data.
2. **Apply beamforming / range-gating** (if not already done upstream) per the configuration.
3. **Form per-carrier amplitude + phase**:
   - Amplitude = power per carrier (frequency × angle × range-gate, or whichever subset).
   - Phase = time-of-flight relative to a reference carrier.
4. **Simplex closure** along the chosen carrier axis (multiplicative ε = 1e-10).
5. **Joint quaternion lift**: build q_joint per measurement instant using the standard procedure in [`../../HCI-CNQ/`](../../HCI-CNQ/).
6. **Hash everything**: content_sha256 over the canonical output.

---

## Outputs

```json
{
  "experiment_id": "HCI-ULTRASOUND-XXX",
  "domain": "NON_CONTACT_ULTRASOUND",
  "carriers": {
    "type": "frequency_x_angle_x_range",
    "n_carriers": "configurable, typically 32-256",
    "structure": "see config"
  },
  "data": {
    "compositional_per_instant": "[T x K] simplex-closed amplitude matrix",
    "joint_quaternion_per_instant": "[T x 4] unit quaternion trajectory",
    "phase_per_carrier": "optional [T x K] phase / time-of-flight matrix"
  },
  "metadata": {
    "probe": "...",
    "frequencies_hz": [...],
    "geometry": "...",
    "coupling": "air | gel | other",
    "domain": "medical | industrial"
  },
  "content_sha256": "..."
}
```

---

## Validation criteria for first pilot

1. **Determinism**: same raw measurement + same config → bit-identical content_sha256.
2. **Closure check**: simplex rows sum to 1 within 1e-9.
3. **Quaternion unit-norm**: |q_joint(t)| − 1 < 1e-12 at every instant.
4. **Helmsman extraction sanity**: on a known reference target (e.g., a flat plate at known distance), the helmsman locks on the expected carrier (e.g., specular range-gate at expected time-of-flight).
5. **Lock-loop closure on a controlled motion**: when the target is moved at a known rate, the joint quaternion rotation rate matches the expected geometric prediction.

---

## Out of scope

- Specific Python implementation (lands when first pilot data exists).
- Real-time / streaming versions.
- Integration with specific commercial probe APIs.
- Beamforming algorithm details (the adapter consumes beamformed signals; beamforming is upstream).

---

*Adapter spec defines what must be produced; implementation comes when the pilot needs it.*
