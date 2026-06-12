# HCI-AUDIO Test Fixtures (starter set)

**Status:** starter fixtures — full audio test corpus is Phase C5+ work, gated on the audio applied pilot (INV-024) which is months away per push #32 priority lock. These two CSVs exercise the CNQ v2 engine end-to-end on synthetic 4-way stereo (D=8) input so the audio wrapper has matched test data to demonstrate against.

## Files

| File | Purpose |
|---|---|
| `baseline_coherent_4way_stereo.csv` | 4-way stereo (L_HF, L_HMF, L_LMF, L_LF, R_HF, R_HMF, R_LMF, R_LF) with L=R per-band response across 64 log-spaced frequency bins (20 Hz to 20 kHz). All four crossover bands present at canonical band-pass shapes. |
| `delayed_lf_4way_stereo.csv` | Same baseline plus a synthetic perturbation: L_LF attenuated by 45% across the LF band (20–250 Hz). Models a per-driver misalignment in one channel of one band. |

## Smoke test results

Running `cnq.cnq_run(input_csv=...)` on each:

| Fixture | rho_AB.mean | coherence_class | CHSH S | helmsman.flips |
|---|---|---|---|---|
| baseline_coherent_4way_stereo | 0.076 rad | tightly_coupled | 0.29 | 10 |
| delayed_lf_4way_stereo | 0.077 rad | tightly_coupled | 0.29 | 10 |

Both fixtures land in the `tightly_coupled` bucket because the synthetic L_LF attenuation is small (45%) and most of the spectrum remains symmetric. To push the diagnostic past the `loosely_coupled` (rho_AB > 0.2) threshold, the perturbation needs to be more aggressive (e.g., complete phase inversion in a band, or multi-band cross-channel mixing).

## What this fixture set demonstrates

- The engine reads audio-style CSV (driver columns × frequency bins) without modification — the wrapper convention from `HCI-CNQ/wrappers/wrapper_audio.json` is correct
- Twin-quaternion factoring at D=8 produces ρ_AB measurements in the expected radian range
- CHSH S-value computed end-to-end on the twin factor outputs
- Helmsman family populates with reasonable per-frequency dominant-driver attributions
- Hash fingerprint differs between the two fixtures (correctness of the determinism contract — different inputs → different hashes)

## What this fixture set does NOT demonstrate (yet)

- Strong-perturbation misalignments that would drive ρ_AB above 0.2 or push CHSH S above 2.0
- Calibration against listening-test correlation (the eventual deployment validation)
- Cross-language parity verification (R port not exercised in this sandbox; run `scripts/verify_cross_language_parity.py --engine cnq --input-csv <fixture>` once R is installed)

The full corpus is gated on the audio applied pilot (INV-024) when it lands. For now these two fixtures validate the wrapper's `wrapper_audio.json` field paths against actual engine output and provide a baseline for regression testing.

## How to extend

A more comprehensive fixture set would include:

1. **`time_delay_misaligned_4way_stereo.csv`** — strong L_LF time-delay perturbation that drives ρ_AB.mean above 0.5 in the LF band specifically
2. **`level_imbalanced_4way_stereo.csv`** — uniform-band L_LF level reduction by 6 dB across the entire band
3. **`phase_incoherent_4way_stereo.csv`** — random phase perturbation in one driver pair
4. **`group_delay_drifting_4way_stereo.csv`** — group delay drift across the band
5. **`crossover_misaligned_4way_stereo.csv`** — exact synthetic match to the audio wrapper §5 worked example
6. **`reference_quadraphonic_4way_d16.csv`** — D=16 fixture once the quad-quaternion implementation lands (v2.1)

Each with locked expected_results.json entries for regression testing.

This is Phase C5+ work, deferred per the push #32 priority lock until after Round 3 + arXiv + the audio applied pilot.
