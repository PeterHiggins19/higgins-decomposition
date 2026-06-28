# P‑C (seed) — Deterministic compositional coding and noise rejection

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The channel
paper of the series — the communications substrate beneath the pinnacle (P‑Ω): how a composition encodes,
self-protects, and denoises, all deterministically and receipted. Off the public repo (abstracts only);
honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## Abstract (working)

We present the compositional coding layer that makes deterministic compositional communication (P‑Ω) work. A
message is carried in the `D−1` isometric-log-ratio channels of a composition; the encoder and reader are exact
mutual inverses (a fixed point, `742f1b5a…`). The composition **self-protects**: closure rejects any
common-mode multiplicative gain exactly (`clr(g·x)=clr(x)`; measured rejection of a 26.7 dB swing at residual
8.9×10⁻¹⁶ — numerical, ADC-bounded). Additive noise **off** the signal's coherent k-subspace is removed exactly
at `10·log₁₀((D−1)/k)` dB; **known-structure** noise is subtracted to the floor; **in-subspace random** noise is
provably not separable and the coder returns NO. As a source coder, the compositional representation reaches a
target fidelity at ~3.5× fewer bits than a structure-agnostic baseline and ~10× smaller than lossless float,
within ~10% of the entropy of its own symbols. We validate a 16-QAM/AWGN link against theory and show the
**log-ratio representation is far more error-robust than raw shares** at equal modulation/power (≈700× lower
delivered distortion at 12 dB), because a corrupted log-ratio degrades gracefully while a corrupted raw share
blows up through the closure-and-log. Everything is deterministic and hash-receipted. *Tier 1 throughout; no
Shannon limit is beaten.*

## 1. The codec

Bytes (or any structure) map to the `D−1` ilr coordinates of a composition; closure + log-ratio recover them
exactly. `R∘E = id` measured **1500/1500 exact** over D = 3…48 (`742f1b5a…`). Capacity per composition is
`(D−1)·(bits/symbol)` and **grows with D** (`bf24c615…`).

## 2. Noise rejection (the three stages)

- **Common-mode (multiplicative), exact.** Closure cancels any gain common to all parts — the RWA ground-state
  law in communications dress. *(313 dB numerical; `d8c21c70…`.)*
- **Additive, off-subspace + structured, deterministic.** Projection onto the coherent k-subspace removes
  off-subspace noise at `10·log₁₀((D−1)/k)` dB (measured = theory ±0.04 dB); known-structure interferers are
  subtracted to the floor (28 dB). *(`cb0c3f52…`.)*
- **Additive, in-subspace random — the honest NO.** Not deterministically separable; the coder returns 0 dB and
  reports the floor.

## 3. Source coding (compression)

On real 8-part energy-mix data: ~3.5× fewer bits than a structure-agnostic baseline, ~10× smaller than lossless
float, within ~10% of symbol entropy. The win is the compositional geometry, not a capacity violation.
*(`305cc0db…`.)*

## 4. On a real modulation (16-QAM / AWGN)

Simulator validated against the closed-form M-QAM BER. The compositional (ilr) source representation delivers
telemetry **≈700× more accurately than raw shares at 12 dB**, at identical modulation/power — a representation
effect, stackable on any modulation and FEC. *(`f502c15d…`.)*

## 5. The generator (the data factory)

Inverting the reader gives an exact SO(n) generator to **n = 1024** (rotor = planar to ~10⁻¹⁶), used to
synthesize structured test sets and (named) differential-unitary constellations. *(`8107b173…`.)*

## 6. Honest cap & tiers

No Shannon limit is beaten; the 313 dB is numerical/ADC-bounded; in-subspace random noise is not removed.
**T1:** all §1–§4 measurements. **T2:** the coding layer as the substrate for P‑Ω. **T3:** the unitary
constellation and hardware comparisons — to earn.

*Cross-refs: `P_OMEGA_THE_DATA_IS_THE_CARRIER_SEED.md`, `frontier/HS_ENGINE_MORPHOLOGY_AND_CODEC.md`,
`../experiments/conformance_fixtures_2026-06/`, `../experiments/ground_state_noise_cancel_2026-06/`,
`../experiments/deterministic_denoise_2026-06/`, `../experiments/compression_benchmark_2026-06/`,
`../experiments/qam_spaceradio_2026-06/`, `../datasheets/AN-001_DETERMINISTIC_NOISE_REJECTION.md`. Peter is the
sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
