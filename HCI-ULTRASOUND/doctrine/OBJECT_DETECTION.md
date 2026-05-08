# Object Detection in HCI-ULTRASOUND

**Status:** doctrine, push #24 (2026-05-08).
**Companion:** [GEOMETRY_LOCK_PROBE.md](GEOMETRY_LOCK_PROBE.md), [AUTOFOCUS_AND_STABILIZATION.md](AUTOFOCUS_AND_STABILIZATION.md).

---

## What "object detection" means here

Object detection in CNQ language is **the appearance of a recognisable Helmsman pattern** in the joint quaternion field of the return signal. A new object enters the probe's field of view when the helmsman shifts to a new dominant carrier (or carrier combination) that is characteristic of that object's geometric/material signature.

This is a different framing than classical ultrasound thresholding. Classical methods look for amplitude exceedances; CNQ object detection looks for **structural changes in the steering of the return signal**.

---

## Detection signatures

| Signature | Interpretation |
|---|---|
| Sustained Helmsman flip onto a new carrier | A new object has entered the field, with that carrier as its compositional fingerprint |
| Increase in Helmsman Stability after a flip | The new object is stably in the field (not a transient artefact) |
| Periodic helmsman flip pattern (LIMIT_CYCLE_P2) between two carriers | Two distinct features are simultaneously present and contributing to the return |
| Helmsman Chaos (rapid aperiodic flips) | Cluttered field, multiple objects, or strong specular interference |
| Drop in stability without flip | The object is moving or the probe is drifting, but the same object is still dominant |

These map directly onto the Helmsman family extensions in [`../../HCI-CNT/handbook/GLOSSARY.md`](../../HCI-CNT/handbook/GLOSSARY.md) §I.

---

## False-positive control

The framework's determinism contract gives a strong false-positive rejection mechanism:

- **Bit-identical reproduction**: the same measurement always produces the same helmsman. Random noise spikes that would trigger classical amplitude thresholds do not flip the helmsman because the simplex closure normalises them out.
- **Stability gating**: a detection is only registered when Helmsman Stability holds above threshold for a configurable window (e.g., S_σ > 0.7 for 5 consecutive frames).
- **M² = I check**: physical objects produce stable involution residuals at the IEEE floor; ephemeral artefacts do not.

This is a different (and complementary) approach to classical CFAR (Constant False Alarm Rate) detection.

---

## Object identity (signature library)

The framework can be extended with a **signature library** — a collection of known helmsman patterns associated with specific object/material types. Detection then becomes a two-step:

1. Detect that an object is present (helmsman flip + stability gate).
2. Match the helmsman pattern to entries in the signature library to identify what object it is.

This is left as future work. The signature library would itself be a hash-chained, deterministic artefact (consistent with the rest of the framework) — same content_sha256, same matched identity.

---

## Out of scope

- Specific signature-library populating (would be its own pilot).
- Machine-learning classifiers on top of the helmsman patterns (an obvious extension, but orthogonal to doctrine).
- Real-time alerting or display conventions.

---

*Detection = a structural change in steering. Identity = a match in the signature library.*
