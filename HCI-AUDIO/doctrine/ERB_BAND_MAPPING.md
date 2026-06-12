# ERB Band Mapping for HCI-AUDIO

**Status:** doctrine, push #24 (2026-05-08).
**Companion docs:** [QUATERNION_PHASE_MAPPING.md](QUATERNION_PHASE_MAPPING.md), [HELMSMAN_AT_LISTENING_POS.md](HELMSMAN_AT_LISTENING_POS.md), [ALIGNMENT_TARGETS.md](ALIGNMENT_TARGETS.md).

---

## Why ERB and not octaves

The ERB (Equivalent Rectangular Bandwidth) scale (Glasberg & Moore, 1990) models how the cochlea actually filters sound. Compared with octave or 1/3-octave bands, ERB:

- Has variable bandwidth that increases with frequency, matching cochlear filter widths.
- Is the modern standard in perceptual audio coding, hearing aid design, and high-quality loudspeaker work.
- Better tracks human masking, loudness perception, and timbre discrimination.

A 4-way active loudspeaker measured at the listening position is ultimately judged by ear, so the carriers should be perceptually meaningful. ERB is the right choice.

---

## Reference formulae (Glasberg & Moore 1990)

ERB bandwidth (Hz) at center frequency f (Hz):

```
ERB(f) = 24.7 * (4.37 * f / 1000 + 1)
```

ERB-rate (perceptual band number, dimensionless):

```
ERB_rate(f) = 21.4 * log10(0.00437 * f + 1)
```

Across 20 Hz – 20 kHz this spans ~40.9 ERB-rate units. Using 40 bands gives near-uniform perceptual spacing.

---

## Recommended configuration for HCI-AUDIO

| Parameter | Value | Reason |
|---|---|---|
| Number of bands | 40 | High resolution across full audible range |
| Frequency range | 20 Hz – 20 kHz | Standard human hearing limits |
| Spacing | linear in ERB-rate (not Hz) | Perceptually uniform |
| Loudness weighting | Moore-Glasberg loudness model OR ISO 226 equal-loudness contours | Convert intensity → perceived loudness per band |
| Driver contribution | per-band per-driver intensity matrix | Critical for simplex closure across drivers |
| Closure | multiplicative zero replacement, ε = 1e-10 | Same convention as Hˢ-wide |

---

## How the carriers are constructed at the listening position

The HCI-AUDIO measurement procedure (in summary, full spec in [`../spec/PSYCHOACOUSTIC_4WAY_ADAPTER_SPEC.md`](../spec/PSYCHOACOUSTIC_4WAY_ADAPTER_SPEC.md)):

1. **Filter each driver** through its 4th-order Butterworth crossover and any additional EQ / low-pass.
2. **Apply individual driver level, phase, and time delay** in the active processing chain.
3. **Account for diffraction** — cabinet plus room, as measured at the listening position.
4. **Per ERB band, compute** the contribution from each of the four drivers.
5. **Sum** per-band contributions to get total energy/loudness per band.
6. **Normalise** across the 40 bands to produce the compositional vector on the simplex.

Optionally a per-driver compositional vector is also produced (driver share per band), enabling per-driver helmsman extraction (see [`HELMSMAN_AT_LISTENING_POS.md`](HELMSMAN_AT_LISTENING_POS.md)).

---

## Connection to DADC (the historical origin)

The original DADC work apportioned a fixed 6.02 dB diffraction budget across three cabinet dimensions (W/H/D). The modern listening-position version apportions perceptual energy across 40 ERB bands and 4 drivers. The closure principle is preserved — only the dimensionality and the location of the measurement have changed. See [`../../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](../../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md) for the full narrative.

---

## Out of scope for this doctrine

- Specific ERB band centre frequencies and edges (a 40-row table is straightforward to compute from the formulae above; it lives in the adapter spec, not the doctrine).
- Calibration procedures for measurement microphones at the listening position.
- Room correction (handled separately; HCI-AUDIO consumes corrected measurements as input).

These are practitioner-level concerns, not doctrinal ones.

---

*Same closure principle. Different scale. Same instrument.*
