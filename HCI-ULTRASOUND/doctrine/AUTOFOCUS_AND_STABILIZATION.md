# Autofocus and Image Stabilisation in HCI-ULTRASOUND

**Status:** doctrine, push #24 (2026-05-08).
**Companion:** [GEOMETRY_LOCK_PROBE.md](GEOMETRY_LOCK_PROBE.md), [OBJECT_DETECTION.md](OBJECT_DETECTION.md).

---

## Autofocus as a Helmsman optimisation

Classical ultrasound autofocus optimises for sharpness or echo amplitude. In CNQ language, autofocus is the operation of:

> *Adjusting transmit focus and beamforming parameters to maximise Joint Helmsman Stability on the target feature.*

The Helmsman Stability scalar S_σ (proposed extension, see [`../../HCI-CNT/handbook/GLOSSARY.md`](../../HCI-CNT/handbook/GLOSSARY.md) §I) provides a smooth, differentiable cost function that the probe can optimise without explicit feature detection. When the focus is correct on the target feature, the helmsman locks; when it is not, the helmsman either flips or destabilises.

This is a different approach than classical sharpness-based autofocus and has two advantages:

1. **Robust to specular reflectors**: classical methods can be fooled by glints; helmsman stability requires *consistent* steering, not just high amplitude.
2. **Works in cluttered fields**: the simplex closure normalises out background returns; only the dominant feature contributes to the helmsman.

---

## Image stabilisation as Helmsman lock

Image stabilisation in CNQ language is **maintaining a fixed Joint Helmsman across frames** as the probe or target moves. The probe's stabilisation actuator (mechanical or electronic) is commanded to whatever pose maintains lock.

The control objective is:

```
minimise:  d/dt [ σ̂_joint ]   subject to constraints on probe pose
```

That is: minimise helmsman flips and minimise rotation rate of the joint quaternion field with respect to the target. Static helmsman = static image of the target.

---

## Implementation pattern

For a robotic or actuated probe:

1. Measure at current pose; extract σ̂_joint, S_σ, and joint quaternion rotation angle θ.
2. If the helmsman is stable on the target: hold pose.
3. If the helmsman starts to flip: command pose adjustment in the direction that the joint quaternion log indicates would reverse the flip.
4. If stability drops without flip: command translation along the probe axis (likely loss of focus, not loss of target).
5. Re-measure and iterate.

This is essentially the geometry-lock control loop from [GEOMETRY_LOCK_PROBE.md](GEOMETRY_LOCK_PROBE.md), with autofocus and stabilisation as two specific sub-targets of "maintain lock."

---

## Distinction from classical autofocus / stabilisation

| Concern | Classical | CNQ-based |
|---|---|---|
| Cost function | Sharpness, contrast, amplitude, etc. | Helmsman Stability S_σ |
| Robustness to specular returns | Often fooled by glints | Naturally robust (steering, not amplitude) |
| Robustness to clutter | Requires complex masking | Simplex closure handles it |
| Determinism | Implementation-dependent | Bit-identical (Hˢ-wide contract) |
| Provenance | Typically none | Full hash chain |

CNQ-based autofocus does not replace classical methods — it complements them, and the two can be combined (use S_σ as a primary cost, fall back to classical sharpness as a secondary).

---

## Out of scope

- Specific actuator hardware (mechanical gimbals, phased-array beamforming, etc.).
- Latency budgets and real-time constraints.
- Comparison with specific commercial autofocus implementations.

---

*Stable helmsman = stable image. Optimise stability, you've optimised autofocus.*
