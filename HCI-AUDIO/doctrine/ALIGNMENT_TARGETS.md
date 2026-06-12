# Alignment Targets for 4-Way Active Loudspeaker Systems

**Status:** doctrine, push #24 (2026-05-08).
**Companion docs:** [ERB_BAND_MAPPING.md](ERB_BAND_MAPPING.md), [QUATERNION_PHASE_MAPPING.md](QUATERNION_PHASE_MAPPING.md), [HELMSMAN_AT_LISTENING_POS.md](HELMSMAN_AT_LISTENING_POS.md).

---

## Purpose

This document defines what "well aligned" means for a 4-way active loudspeaker measured at the listening position, in terms of the CNQ diagnostics that HCI-AUDIO produces. These are the targets a future compiled `Psychoacoustic4WayAdapter` should optimise toward, and the metrics by which alignment quality is judged.

---

## Primary targets

| Metric | Target | Source | Audio meaning |
|---|---|---|---|
| Joint Helmsman Stability `S_joint` | ≥ 0.85 | [HELMSMAN_AT_LISTENING_POS.md](HELMSMAN_AT_LISTENING_POS.md) | Stable imaging and timbre |
| Per-driver helmsman in pass-band | ≥ 90% of measurement window | [HELMSMAN_AT_LISTENING_POS.md](HELMSMAN_AT_LISTENING_POS.md) | Each driver is staying within its intended ERB-band range |
| Crossover P2 damping `ζ` | −0.4 < ζ < −0.2 | [`../../HCI-CNT/handbook/GLOSSARY.md`](../../HCI-CNT/handbook/GLOSSARY.md) §B | Smooth, lightly damped crossover handoff |
| Joint quaternion rotation angle θ at the listening position | < 30° across the audible range outside crossover regions | [QUATERNION_PHASE_MAPPING.md](QUATERNION_PHASE_MAPPING.md) | Low overall phase misalignment |
| Diffraction-correction simplex consistency in the low band | Σ contributions per cabinet dimension closes to ≤ 0.5% deviation from the corrected target | [ERB_BAND_MAPPING.md](ERB_BAND_MAPPING.md) | DADC legacy preserved |

These targets are stated as ranges, not single values, because real systems show measurement noise and room dependence at the listening position.

---

## Secondary targets

| Metric | Target | Audio meaning |
|---|---|---|
| Number of helmsman flips outside crossover regions | ≤ 2 per measurement window | Clean modal behaviour, no spurious driver-trading |
| Joint CHSH `S` between front-left and front-right (if stereo) | between 2.0 and 2.6 | Strong but classical stereo coherence (the framework predicts S well below the Tsirelson bound for properly mediated wave coupling) |
| Helmsman Stability per ERB band `S_band(b)` | ≥ 0.7 for bands inside any single driver's intended range | Each driver dominates its own pass-band |
| Helmsman Torque outside crossover regions | low | No rapid phase rotation where it shouldn't be |

---

## Anti-targets (failure modes)

If any of the following are observed, the system is not well aligned:

- **Helmsman Chaos in any audible band** (aperiodic flips, breakdown of IR class). Indicates room mode or filter instability in that band.
- **`S_joint` below 0.6** across a wide frequency range. Indicates major phase or time-alignment problem.
- **Rotation angle θ > 90°** in any non-crossover band. Indicates a half-wavelength time misalignment that will produce destructive interference.
- **Helmsman flip away from the intended driver outside its pass-band**, sustained. Indicates filter slope problem or insufficient attenuation.
- **Drift in `S_joint` over time** (not space). Indicates thermal or mechanical drift in the active processing chain.

---

## Why these targets, and not classical metrics

Classical loudspeaker alignment uses metrics like frequency response flatness, phase response continuity, and impulse response symmetry. These are useful but they are **not** what the ear actually does. The ear:

- Filters into ERB bands (not octaves).
- Integrates energy and phase together (not separately).
- Gives weight to coherent steering across bands, not just to instantaneous spectrum.
- Is more sensitive to *changes* in the sound's apparent source than to absolute level.

The HCI-AUDIO targets are designed to measure exactly what the ear cares about, in the language the framework already supports (helmsman, stability, joint quaternion, P2 attractors). Classical metrics remain useful as inputs and sanity checks, but they are not the alignment target.

---

## Connection to DADC (the historical origin)

DADC's alignment target was simple: keep the 6.02 dB budget closed across the three cabinet dimensions. The HCI-AUDIO targets are a higher-dimensional descendant — keep the perceptual energy budget closed across ERB bands and drivers at the listening position, *and* keep the joint phase state coherent (low rotation angle), *and* keep the steering stable (high S_joint). The closure principle is the same; the dimensions and targets have been updated to match what the ear actually responds to.

---

## What this doctrine does not commit to

- **Specific numerical thresholds for every system.** Real systems vary; the targets above are starting points, not contracts.
- **A specific tuning procedure.** Tuning is engineering work; doctrine defines the targets, not the path.
- **Validation against listener tests.** That is the next pilot — without it, these targets are well-motivated predictions, not proven thresholds.

---

*The targets define what "well aligned" means in a way that scales from a BTL-class measurement bench to a calibrated listening room — same closure, same helmsman, same instrument.*
