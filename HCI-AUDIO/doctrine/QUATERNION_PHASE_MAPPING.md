# Quaternion Phase Mapping for HCI-AUDIO

**Status:** doctrine, push #24 (2026-05-08).
**Companion docs:** [ERB_BAND_MAPPING.md](ERB_BAND_MAPPING.md), [HELMSMAN_AT_LISTENING_POS.md](HELMSMAN_AT_LISTENING_POS.md), [ALIGNMENT_TARGETS.md](ALIGNMENT_TARGETS.md).
**CNQ side:** [`../../HCI-CNQ/`](../../HCI-CNQ/) (general quaternion machinery), [`../../HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](../../HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md) (algebraic foundation).

---

## Why phase is a quaternion problem in 4-way systems

In a 4-way active loudspeaker, the controllable variables include:

- Individual driver level (amplitude — a positive scalar)
- Per-driver phase (a circular variable)
- Per-driver time delay (group delay slope)
- Per-band crossover phase response
- Diffraction-induced phase shift at the listening position

Amplitude lives on the simplex (handled in [`ERB_BAND_MAPPING.md`](ERB_BAND_MAPPING.md)). Phase and time delay are **rotational** — they describe how the four drivers' waves interfere at the listening position. Standard complex numbers (2D) cannot cleanly encode the joint phase state of four interfering signals; **unit quaternions on S³** can.

---

## Per-driver phasor → unit quaternion

For each ERB band at the listening position, each driver contributes:

```
z_k(t, f) = A_k(t, f) * exp(i * φ_k(t, f))      for k = 1..4
```

where A_k is the per-band amplitude contribution and φ_k is the measured phase at the listening position.

Two construction approaches:

### Approach A — Reference-driver framing (recommended for diagnostics)

1. Pick the dominant driver in the current band as reference.
2. The other three relative phases φ_k − φ_ref become rotations around three independent imaginary axes (i, j, k of the quaternion).
3. The combined per-band state is a unit quaternion encoding all three relative phases.

### Approach B — Direct quaternion polar form (better for joint multi-band analysis)

For four signals with independent phases, the relative phase information can be encoded compactly via the quaternion polar form (θ, χ, φ + magnitude). This is the standard quaternion signal-processing representation for multi-channel audio.

Both approaches produce a unit quaternion per ERB band per timestep.

---

## Joint Quaternion Field

For an N-band measurement with four drivers, the joint quaternion field at each band is:

```
q_joint(band) = N(  Σ w_k * q_k(band)  )       k = 1..4
```

where w_k is the amplitude contribution of driver k (from the simplex closure step) and N is the unit-norm normalisation. This is exactly the joint quaternion field defined in [`../../HCI-CNQ/`](../../HCI-CNQ/) — instantiated for the four-driver case.

The joint quaternion across all 40 ERB bands forms a trajectory on S³ (the unit 3-sphere). All standard CNQ operators apply: log, exp, bearing, angular velocity, sandwich product, conjugation (M² = I).

---

## What `log(q_joint)` reveals about the system

The quaternion logarithm extracts the dominant rotation axis and angle:

| Diagnostic | Computation | Audio-system meaning |
|---|---|---|
| Rotation angle θ | norm of imaginary part of log(q_joint) | overall phase misalignment / effective group delay across drivers in this band |
| Dominant axis | argmax of \|imag(log(q_joint))\| | which driver-pair relationship is dominating the phase state |
| Sign of dominant component | sign of imag(log(q_joint))[i*] | handedness — direction of phase rotation |
| Angular velocity ω | atan2 between consecutive log(q_joint) | rate of phase change across frequency or time |

These connect directly to the Helmsman family (see [`HELMSMAN_AT_LISTENING_POS.md`](HELMSMAN_AT_LISTENING_POS.md)).

---

## Time delay → quaternion exponential

Pure time delay between drivers manifests as a constant rotation rate on S³ across frequency (group delay slope). Forward integration via the quaternion exponential map allows simulation of the effect of changing a driver's time-alignment by Δτ:

```
q_joint_new = q_joint * exp( -i * 2π * f * Δτ * n_driver )
```

where n_driver is the unit axis on S³ corresponding to that driver's phase contribution.

This makes "what-if" alignment a single-line operation.

---

## Connection to DADC (the historical origin)

DADC apportioned a fixed total *amplitude* (6.02 dB) across cabinet dimensions. It did not address phase. The modern listening-position version cannot avoid phase — the four drivers' waves interfere, and interference is fundamentally a phase phenomenon. The quaternion lift is what carries the DADC closure principle forward into the phase domain. The metric involution `M² = I` (quaternion conjugation) is the algebraic descendant of the ADAC adaptive-closure rule.

---

## Out of scope

- Real-time phase tracking algorithms (engineering concern, not doctrine).
- Specific quaternion arithmetic library choice (numpy + custom, or scipy.spatial.transform — both are fine).
- Detailed numerical stability concerns for phase unwrapping (handled by atan2-based extraction in the spec).

---

*Amplitude on the simplex. Phase on the 3-sphere. Both closed under their respective constraints.*
