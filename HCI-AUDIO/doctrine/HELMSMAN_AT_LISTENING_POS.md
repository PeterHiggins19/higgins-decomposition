# Helmsman Extraction at the Listening Position

**Status:** doctrine, push #24 (2026-05-08).
**Companion docs:** [ERB_BAND_MAPPING.md](ERB_BAND_MAPPING.md), [QUATERNION_PHASE_MAPPING.md](QUATERNION_PHASE_MAPPING.md), [ALIGNMENT_TARGETS.md](ALIGNMENT_TARGETS.md).
**Glossary:** [`../../HCI-CNT/handbook/GLOSSARY.md`](../../HCI-CNT/handbook/GLOSSARY.md) §I (Helmsman family extensions, proposed).

---

## Three helmsman views in HCI-AUDIO

For a 4-way active loudspeaker measured at the listening position, there are three useful helmsman views, each answering a different question:

| View | Question answered | Carrier set |
|---|---|---|
| **Per-band helmsman** | Which driver is dominating in this ERB band right now? | 4 drivers in a single band |
| **Per-driver helmsman** | Which ERB band is dominating for this specific driver? | 40 ERB bands for one driver |
| **Joint helmsman** | Which driver–band combination is steering the overall sound right now? | 40 × 4 = 160 carriers (sparse) |

All three are extracted from the same underlying compositional data plus the joint quaternion field defined in [`QUATERNION_PHASE_MAPPING.md`](QUATERNION_PHASE_MAPPING.md).

---

## Per-band helmsman

For each ERB band, identify the driver currently exerting the strongest weighted directional influence on the energy in that band:

```
σ̂_band(t, b) = argmax_{k=1..4} ( |Δx_{k,b}(t)| · w_{k,b}(t) )
```

where Δx_{k,b} is the change in driver k's contribution to band b, and w_{k,b} is the local intensity weight.

**Interpretation:** at the crossover between two drivers, σ̂_band typically alternates between the two — a sustained period-2 pattern (LIMIT_CYCLE_P2) is the signature of a well-behaved crossover. Sudden flips outside the crossover region indicate problems (room mode, diffraction peak, or misalignment).

---

## Per-driver helmsman

For each driver, identify which ERB band is dominating its current contribution:

```
σ̂_driver(t, k) = argmax_{b=1..40} ( |Δx_{k,b}(t)| · w_{k,b}(t) )
```

**Interpretation:** σ̂_driver should sit firmly inside the driver's intended pass-band when the system is well aligned. Excursions outside the pass-band indicate filter slope problems or insufficient attenuation.

---

## Joint helmsman

The joint helmsman is extracted from the quaternion logarithm of the joint quaternion field across drivers (per [`QUATERNION_PHASE_MAPPING.md`](QUATERNION_PHASE_MAPPING.md)):

```
σ̂_joint(t) = argmax over imaginary directions of |Im(log(q_joint(t)))|
sign        = sign of that dominant component
```

This identifies which driver-relationship is currently dominating the *phase* state at the listening position. It is the most diagnostic of the three — combining amplitude and phase information into one steering direction on S³.

---

## Helmsman Stability metrics

Three stability scalars are produced per measurement:

| Metric | Range | Audio-system meaning |
|---|---|---|
| S_band(b) | [0, 1] | Stability of dominant driver within band b. High value = clean modal lock; low value = rapid driver-trading (often ringing or interference). |
| S_driver(k) | [0, 1] | Stability of dominant band for driver k. High value = driver is staying in its intended pass-band. |
| S_joint | [0, 1] | Stability of the joint helmsman across all bands and drivers. Primary scalar for "imaging stability". |

Aggregate metric: `S_joint > 0.85` is the proposed alignment target for high-quality 4-way systems (see [`ALIGNMENT_TARGETS.md`](ALIGNMENT_TARGETS.md)).

---

## Helmsman flips and their audio meaning

Helmsman flips (changes in the dominant carrier) have specific audio-system interpretations depending on where they occur:

| Flip pattern | Likely cause | Audible effect |
|---|---|---|
| Periodic flips between two drivers in the crossover region (LIMIT_CYCLE_P2 with measurable damping ζ < 0) | Well-designed crossover handoff | Smooth transition, no audible artefact |
| Rapid aperiodic flips in midrange | Room modes or insufficient damping | Coloration, "muddy" imaging |
| Sudden helmsman flip away from intended driver outside its pass-band | Filter alignment problem | Image shift, frequency-response anomaly |
| Drop in S_joint below ~0.6 over a wide frequency range | Major phase or time-alignment problem | Diffuse imaging, lost focus |

These connect to the IR taxonomy and the Volume IV interpretation of P2 attractors as universal compositional signatures.

---

## Connection to DADC (the historical origin)

The original DADC question was *"which cabinet dimension is currently carrying most of the 6.02 dB diffraction budget?"* That is exactly the per-dimension helmsman question. The HCI-AUDIO version replaces "cabinet dimension" with "ERB band × driver" and replaces "near-field diffraction" with "listening-position perceptual energy + phase," but the question is the same. The simplex closure that DADC enforced makes the helmsman well-defined; without it, the maximum is ill-conditioned.

---

## Out of scope

- Specific implementation algorithms for sliding-window stability (engineering concern).
- Hysteresis thresholds for flip detection (tuneable, not doctrinal).
- Real-time visualisation of helmsman trajectories at the listening position (a tooling concern; will land when pilot work begins).

---

*Helmsman = "which part is currently carrying the budget" — the same question, asked at the right scale.*
