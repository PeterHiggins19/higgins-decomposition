# Geometry Lock Probe — Doctrine

**Status:** doctrine, push #24 (2026-05-08).
**Companion docs:** [OBJECT_DETECTION.md](OBJECT_DETECTION.md), [AUTOFOCUS_AND_STABILIZATION.md](AUTOFOCUS_AND_STABILIZATION.md), [MEDICAL_VS_INDUSTRIAL.md](MEDICAL_VS_INDUSTRIAL.md).
**CNQ machinery:** [`../../HCI-CNQ/`](../../HCI-CNQ/) (joint quaternion field, helmsman, M² = I).

---

## What a geometry lock probe is

A **Geometry Lock Probe** is an ultrasound probe — handheld, robotic, or fixed — that uses CNT/CNQ-driven feedback to actively maintain measurement on a specific geometric feature of the target (an edge, a curvature, a tissue interface, a defect, a specular reflector, etc.) under relative motion or noise.

The probe is not aiming at a *coordinate*; it is aiming at a *feature defined by its compositional signature*. The framework's job is to identify, lock onto, and maintain that signature using the same Joint Helmsman machinery already developed for HCI-CNQ.

---

## Carriers (compositional parts)

The probe forms a compositional vector from its return signal at each measurement instant. The carriers can be any of:

| Carrier set | When useful |
|---|---|
| **Frequency bands** | Broadband or chirped probes — the spectral signature of the return identifies the target |
| **Angular sectors** | Beamformed array probes — the angular distribution of return identifies the target |
| **Array channels** | Multi-element transducers — the per-element amplitude/phase identifies the target |
| **Range gates** | Time-of-flight bins — the depth distribution of return identifies the target |

In practice the most diagnostic carrier set is usually a hybrid: angular-sector × range-gate, with frequency-band as a secondary structure. The simplex closure runs over the chosen carrier set.

---

## Joint quaternion field

For each measurement instant, the probe constructs a unit quaternion per carrier (combining amplitude and phase / time-of-flight) and forms the joint quaternion field per the standard procedure in [`../../HCI-CNQ/`](../../HCI-CNQ/):

```
q_joint(t) = N(  Σ w_k * q_k(t)  )       k = 1..K carriers
```

- `w_k` is the per-carrier amplitude (from the simplex-closed compositional vector).
- `q_k` is the unit-quaternion lift of the per-carrier amplitude+phase.
- `N` is the unit-norm normalisation.

The Joint Helmsman σ̂_joint(t) and Helmsman Stability S_σ(t) are then extracted as in [`../../HCI-CNT/handbook/GLOSSARY.md`](../../HCI-CNT/handbook/GLOSSARY.md) §I.

---

## What "lock" means in this language

The probe is **locked on the target geometry** when:

1. Joint Helmsman σ̂_joint identifies a specific carrier (or stable combination of carriers) characteristic of the target feature.
2. Helmsman Stability S_σ stays above a target threshold (e.g., S_σ > 0.85) over a sliding window.
3. The metric involution `M² = I` residual stays within IEEE floor (consistent with stable geometric structure).
4. The Joint Quaternion rotation angle θ stays bounded and predictably evolving (no sudden flips).

The probe is **out of lock** when any of these criteria fail. Each failure mode has a specific recovery action (see "Control loop" below).

---

## Control loop

The geometry-lock probe runs the following loop at the probe's measurement rate:

```
1. Transmit pulse(s).
2. Receive returns; form per-carrier amplitude+phase vector.
3. Close to simplex on amplitudes; build q_joint.
4. Extract σ̂_joint and S_σ.
5. Compare to lock criteria.
6. If locked:
     - Maintain transmission parameters.
     - Output measurement at the locked geometry.
7. If out of lock, classify failure mode and act:
     - Helmsman flipped: re-center on the previous stable axis.
     - Stability dropped without flip: increase integration time, narrow gates.
     - Both: trigger search/scan to re-acquire.
```

The control loop is **first-order** in the same way the pilot-wave guidance equation we derived earlier is first-order: the probe's command at time `t` is a function of the joint helmsman at time `t`, not of accumulated state. This keeps it responsive and analytically tractable.

---

## Success criteria for a geometry-lock pilot

When a first pilot is run, it is considered a success when:

1. The probe maintains S_σ > 0.85 on the target feature for ≥ 5 seconds of relative motion.
2. After deliberate perturbation (e.g., tap), the probe re-acquires lock within 200 ms.
3. The bit-identical determinism contract is preserved on stationary measurements (same input → same content_sha256).
4. The measurement output at the locked geometry has lower variance than an unlocked equivalent at the same position.

---

## Connection to DADC (the historical origin)

DADC was a **passive** apportionment of a fixed total across cabinet dimensions. The geometry-lock probe is its **active** descendant: the probe still apportions a fixed total (the return signal) across parts (carriers), but it also actively steers to keep the apportionment locked onto a desired pattern. The closure principle is preserved; the new ingredient is the control loop.

---

## Out of scope for this doctrine

- Specific probe hardware (frequencies, array geometries, bandwidth).
- Beamforming algorithms (engineering layer; the doctrine consumes their output).
- Specific feature-identification algorithms (machine learning, classical edge detection, etc. — orthogonal to the framework).
- Real-time visualisation conventions.

These are practitioner-level concerns; doctrine defines what locked means and how to measure it, not how to build the probe.

---

*Active sensing on a fixed compositional total. The same closure rule that began at BTL, now closing the loop.*
