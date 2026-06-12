# CNQ v2 — Audio Wrapper (Prose Handbook Companion)

**Date:** 2026-05-08
**Wrapper data file:** `HCI-CNQ/wrappers/wrapper_audio.json` (canonical machine-readable wrapper)
**Wrapper version:** audio-wrapper/1.0
**Engine target:** CNQ v2.0.0 (schema `cnq/2.0.0`)
**Type:** prose handbook — narrative companion to the data wrapper at `HCI-CNQ/wrappers/wrapper_audio.json`
**Audience:** audio engineers using CNQ v2 to diagnose multi-way multi-channel speaker systems; AI assistants engaging with the engine for audio applications
**Catalog:** INV-024 (HCI-AUDIO applied pilot — first wrapper instance), INV-042 (domain wrapper convention)

---

## 0. What this document is, and what it is not

**This is the prose handbook companion to a wrapper data file.** The canonical machine-readable wrapper for the audio domain is `HCI-CNQ/wrappers/wrapper_audio.json` — a JSON file conforming to the wrapper schema documented in `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md`. That JSON file holds the carrier aliases, field aliases, calibration thresholds, and bilingual (English / French) display names that any renderer / report-builder uses to translate engine output to audio-engineering quantities.

**This handbook is optional supplementary material.** It provides narrative interpretation guidance, calibration practice, listening-test correlation advice, and a worked diagnostic example — content that doesn't fit naturally into the JSON data wrapper. Engineers who only need the data tags can use `wrapper_audio.json` directly; engineers who want the practitioner's view come here.

**The engine itself does not consume either file.** The engine emits CoDa-community vocabulary (closure, CLR, ILR, bearing trajectory, radial trajectory, twin-quaternion factoring, CHSH coherence diagnostic, helmsman family, attractor fit). The wrapper data file translates that vocabulary to audio-engineering quantities (time delay, intensity, phase, group phase, EQ coherence, perceptual unity at the auditory cortex). This handbook explains how to use those translated outputs in design and diagnosis.

**Any other domain (finance, geochemistry, government budget, nuclear chemistry, climate, bioinformatics) can have its own wrapper following the same pattern** — a JSON data file in `HCI-CNQ/wrappers/`, optionally accompanied by a domain-specific prose handbook elsewhere in the repo (e.g., `HCI-ULTRASOUND/CNQ_ULTRASOUND_WRAPPER.md` for the ultrasound wrapper when it lands).

---

## 1. The audio engineering problem this wrapper addresses

A multi-way multi-channel speaker system (4-way stereo = 8 drivers, 4-way quadraphonic = 16 drivers) must radiate as a **single coherent source** at the listener's auditory cortex. This requires simultaneous coherence of five quantities across all drivers and all frequencies:

1. **Time delay** — drivers fire in the right relative order so wavefronts arrive in phase.
2. **Per-driver intensity** — levels balance across the band; no driver dominates or vanishes.
3. **Instantaneous phase** — at each frequency, phase relationships between drivers are correct.
4. **Group phase / group delay** — the rate of phase change with frequency is consistent; transients stay sharp.
5. **Total EQ** — combined frequency response is flat or correctly shaped; no crossover gaps or peaks.

When all five hold, the auditory cortex fuses N drivers into a single perceived source. When any one fails, the percept collapses to "multiple sources" or "smeared image." This is the binary listening test that defines high-end speaker design.

The five quantities **cannot be independently optimised** — they trade off against each other through the crossover network and the room interaction. The system has to be solved jointly. That is what CNQ v2's algebraic structure measures, expressed in mathematical terms; this wrapper translates back to audio terms.

---

## 2. The dataset shape — how audio data enters CNQ v2

### 2.1 Driver-as-carrier convention

Each driver is a CNQ carrier (a column in the input CSV). For a 4-way stereo system: 8 carriers. For 4-way quadraphonic: 16 carriers.

Carrier naming convention (recommended):

```
4-way stereo (D=8):
  L_HF, L_HMF, L_LMF, L_LF, R_HF, R_HMF, R_LMF, R_LF

4-way quadraphonic (D=16):
  FL_HF, FL_HMF, FL_LMF, FL_LF,
  FR_HF, FR_HMF, FR_LMF, FR_LF,
  RL_HF, RL_HMF, RL_LMF, RL_LF,
  RR_HF, RR_HMF, RR_LMF, RR_LF
```

Where channels are `L`/`R` for stereo or `FL`/`FR`/`RL`/`RR` for quadraphonic, and bands are `HF` (high-frequency) / `HMF` (high-mid) / `LMF` (low-mid) / `LF` (low-frequency) for a 4-way crossover. The naming is wrapper convention; the engine treats them as opaque carrier names.

### 2.2 Carrier value semantics

Each row of the input CSV is one analysis point. The value at carrier `i` is the **per-driver acoustic energy contribution at that analysis point**, in linear-power units (e.g., μPa², or W/m², or any consistent positive measure proportional to acoustic power). Energy because composition closes naturally on the simplex: the relative power across drivers is a composition.

### 2.3 What T (the trajectory dimension) represents

T is the parameter swept across rows. Common audio choices:

| T-axis | Meaning | What CNQ measures |
|---|---|---|
| **Frequency** (T = number of FFT bins) | Acoustic energy distribution at each frequency | Coherence of drivers across the band — most common audio analysis |
| Time (T = impulse response samples) | Energy distribution at each time sample of the system impulse response | Time-domain coherence — leading-driver attribution and group-delay structure |
| Listener position (T = positions in the room) | Energy distribution at each listening position | Off-axis coherence — how the unified-source percept holds across the listening area |
| SPL level (T = test signal levels) | Energy distribution at each input level | Compression / nonlinearity coherence — how driver behaviour scales with level |

The engine is agnostic about T's semantics; the user labels what T represents in `metadata.engine_config.t_axis_label` for downstream readability.

### 2.4 Why this is a composition

At any fixed analysis point (e.g., one frequency bin), the relative acoustic energies across the N drivers form a positive vector that closes to a probability simplex. The total absolute level is captured separately by the radial trajectory. The compositional structure carries the relative coupling that defines coherence; the radial structure carries the magnitude balance. Both matter; both must be measured.

---

## 3. The output channel map — every CNQ v2 field, with audio meaning

### 3.1 Input metadata

| CNQ field | Audio meaning | Calibration note |
|---|---|---|
| `input.n_carriers` | Number of drivers (D=8 stereo, D=16 quadraphonic) | Must match physical system |
| `input.n_records` | Number of analysis points (frequency bins, time samples, etc.) | Choose T based on resolution required; T ≥ 256 typical for FFT-based analysis |
| `input.carriers` | Driver names | Use channel-band convention from §2.1 for downstream interpretability |
| `input.source_file_sha256` | Hash of input dataset | Locks the measurement; any reanalysis with same input gives same output |

### 3.2 Bearing trajectory (compositional direction = phase-like content)

| CNQ field | Audio meaning | Well-tuned system | Misaligned system |
|---|---|---|---|
| `cnq_view.bearing_trajectory.per_step[t].q_w/x/y/z` | Per-step rotation quaternion = how the energy distribution rotates from frequency f_t to f_{t+1} | Quaternions slowly varying across frequency, mostly real (q_w near 1), small imaginary parts | Quaternions with sudden jumps at crossover frequencies; large imaginary components mid-band |
| `cnq_view.bearing_trajectory.per_step[t].angle_rad` | Magnitude of step rotation (radians) | < 0.05 rad for adjacent FFT bins in well-tuned mid-band; up to 0.3 rad through crossover | > 0.5 rad steps anywhere in audible band = phase incoherence event |
| `cnq_view.bearing_trajectory.per_step[t].residual_linf` | Quaternion sandwich reconstruction residual | < 1e-13 always (this is a numerical sanity check, not an engineering metric) | If above 1e-12, indicates numerical degenerate input (e.g., zero-energy driver) |
| `cnq_view.bearing_trajectory.max_residual` | Worst-case sandwich residual over the trajectory | < 1e-12 | > 1e-10 indicates numerical instability; check for near-zero rows |
| `cnq_view.bearing_trajectory.gate_pass` | Did the trajectory satisfy the IEEE-floor reconstruction gate? | `true` always (this is engine numerical health) | `false` indicates degenerate input data, not engineering failure |

**The bearing trajectory tells you about phase relationships between drivers across the frequency sweep.** Smooth, slowly-varying quaternions = phase coherence. Sharp jumps = crossover misalignment.

### 3.3 Radial trajectory (compositional magnitude = level/intensity content)

| CNQ field | Audio meaning | Well-tuned system | Misaligned system |
|---|---|---|---|
| `cnq_view.radial_trajectory.ilr_norms[t]` | Magnitude of energy-distribution vector at frequency t in ILR space | Smooth across band; slowly increasing toward midrange peak | Sharp dips at crossover regions = energy holes; sharp peaks = crossover overlap |
| `cnq_view.radial_trajectory.min/max/mean/std` | Distribution of energy magnitudes across band | std/mean ratio < 0.3 indicates well-balanced system | std/mean > 0.5 indicates significant level imbalance somewhere in the band |
| `cnq_view.radial_trajectory.median` | Middle of energy magnitude distribution | Close to mean (symmetric distribution) | Far from mean (skewed) = response is dominated by one band |

**The radial trajectory tells you about per-driver intensity balance.** Smooth norm across the band = level coherence. Dips and peaks = crossover problems and EQ imbalance.

### 3.4 Helmsman family (leading-driver attribution dynamics)

| CNQ field | Audio meaning | Well-tuned system | Misaligned system |
|---|---|---|---|
| `helmsman_family.sigma[t]` | Index of dominant carrier (leading driver) at analysis point t | Sigma transitions at expected crossover frequencies (e.g., LF→LMF at 250 Hz, LMF→HMF at 1.5 kHz, HMF→HF at 5 kHz) | Sigma jumping unexpectedly mid-band; chattering between two carriers; never settling on one driver |
| `helmsman_family.flips.total` | Total count of dominant-driver changes over the trajectory | Equal to (number of crossover regions) ± 1 (e.g., 3 for a 4-way system) | Significantly higher = chattering; significantly lower = one driver dominates everywhere (response not flat) |
| `helmsman_family.flips.rolling[w]` | Count of σ flips in rolling window of length w | Concentrated at crossover frequency neighbourhoods | Distributed throughout band = chattering |
| `helmsman_family.stability_S_sigma.global` | Fraction of bins where σ unchanged from previous bin | > 0.9 for a clean 4-way system | < 0.7 indicates instability in driver attribution |
| `helmsman_family.stability_S_sigma.rolling[w]` | Same metric in rolling window | High in passband regions; lower at crossovers | Low everywhere = system has no clear band structure |
| `helmsman_family.chaos_indicator` | Feigenbaum-δ-style estimate of period-doubling depth | `null` or low for clean systems | Non-trivial values may indicate sub-harmonic distortion or feedback |
| `helmsman_family.torque_proxy[t]` | Second difference of σ — rate of change of dominant driver | Spikes at crossover transitions, near-zero elsewhere | Uniformly non-zero across band = unstable attribution |

**Helmsman σ is the engine's answer to "which driver is leading the impulse at this frequency."** A 4-way crossover should have exactly 3 transitions in σ across the band (one per crossover region). More transitions = chatter. Fewer = response not actually 4-way.

### 3.5 Twin-quaternion factoring (D=8, load-bearing for stereo systems)

| CNQ field | Audio meaning | Well-tuned system | Misaligned system |
|---|---|---|---|
| `twin_quaternion_factoring.factor_A.per_step` | Quaternion path of L-channel composite axes | Smooth, mostly-real quaternions | Sudden jumps = L-channel internal crossover misalignment |
| `twin_quaternion_factoring.factor_B.per_step` | Quaternion path of R-channel composite axes | Smooth, structurally similar to factor_A | Different from factor_A = L-R asymmetry |
| `twin_quaternion_factoring.coupling.rho_AB_per_step[t]` | L-R joint coherence angle (radians) at analysis point t | Small (< 0.1 rad) and stable across band | Drift across band = L-R group phase incoherence; large values mid-band = stereo image collapse |
| `twin_quaternion_factoring.coupling.rho_AB_summary.mean` | Average L-R coherence | < 0.2 rad for well-aligned stereo pair | > 0.5 rad indicates significant L-R decoupling |
| `twin_quaternion_factoring.coupling.rho_AB_summary.std` | Variability of L-R coherence across band | < 0.1 rad (stable coupling) | > 0.3 rad (band-dependent coupling = group-phase issue) |
| `twin_quaternion_factoring.coupling.coherence_class` | One of `tightly_coupled`, `loosely_coupled`, `decoupled` | `tightly_coupled` for well-tuned stereo | `loosely_coupled` or `decoupled` indicates real engineering problem |

**ρ_AB(t) is the central audio diagnostic for stereo coherence.** It's the angle between the L-channel quaternion and the R-channel quaternion at each frequency bin, measuring how well-aligned the two channels are in compositional rotation space. Small ρ_AB everywhere = stereo image holds. Drifting ρ_AB = stereo image moves with frequency = poor imaging.

The wrapper convention assigns factor_A to ILR axes [0,1,2] (the L-channel composite) and factor_B to ILR axes [3,4,5,6] reduced to 3 (the R-channel composite). The carrier-naming convention from §2.1 ensures this assignment is consistent.

### 3.6 Quad-quaternion factoring (D=16, future-supported for quadraphonic)

| CNQ field | Audio meaning |
|---|---|
| `quad_quaternion_factoring.factor_A/B/C/D.per_step` | Quaternion paths for FL, FR, RL, RR channels |
| `quad_quaternion_factoring.coupling.rho_AB_per_step` | FL-FR coherence (front stereo) |
| `quad_quaternion_factoring.coupling.rho_CD_per_step` | RL-RR coherence (rear stereo) |
| `quad_quaternion_factoring.coupling.rho_AC_per_step` | FL-RL coherence (left depth) |
| `quad_quaternion_factoring.coupling.rho_BD_per_step` | FR-RR coherence (right depth) |
| `quad_quaternion_factoring.coupling.rho_AD_per_step` | FL-RR diagonal coherence |
| `quad_quaternion_factoring.coupling.rho_BC_per_step` | FR-RL diagonal coherence |
| `quad_quaternion_factoring.coupling.joint_4way_score` | Single score combining all 6 pairwise angles into 4-channel unity metric |

For quadraphonic: stereo coherence within each pair, depth coherence between pairs, and a joint 4-channel unity score. Schema is locked in v2; full implementation in v2.1.

### 3.7 Attractor fit (group-phase / crossover stability)

| CNQ field | Audio meaning | Well-tuned system | Misaligned system |
|---|---|---|---|
| `attractor_fit.period` | Compositional period of dominant rotation | 2 (period-2 limit cycle = stable structure) | Other values, or low confidence = no clear periodic structure |
| `attractor_fit.period_stability` | How stable the period is across the band | > 0.9 (locked period) | < 0.6 (period drifting = group-delay drift) |
| `attractor_fit.dominant_pair` | Which two ILR axes dominate the attractor structure | Specific to system; consistent across measurements | Changes between measurements = not robust |
| `attractor_fit.contraction_lambda` | Lyapunov-style contraction rate | Negative, magnitude > 0.05 (attractor is contracting; system is stable) | Positive (system is diverging) or near zero (marginally stable) |
| `attractor_fit.amplitude_A` | Amplitude of period-2 oscillation | Modest (0.2–0.6); reflects normal crossover behaviour | Very large (> 0.8) = system in heavy oscillation; very small (< 0.05) = no detectable structure |
| `attractor_fit.damping_zeta` | Effective damping ratio | Between 0.05 and 0.3 (lightly damped) | < 0.01 (undamped — system rings) or > 1 (overdamped — sluggish) |
| `attractor_fit.fitted` | Did the fit converge with high confidence? | `true` | `false` indicates the system has no clean attractor structure (often a sign of misalignment or noise contamination) |

**The attractor fit answers: is the crossover region producing a stable, well-damped, periodic structure, or is it drifting / ringing / dead?** A well-designed crossover gives `period=2`, `period_stability > 0.9`, `contraction_lambda < -0.05`, `damping_zeta` between 0.05 and 0.3.

### 3.8 CHSH coherence diagnostic (the single number for auditory-cortex unity)

| CNQ field | Audio meaning | Well-tuned system | Misaligned system |
|---|---|---|---|
| `chsh_diagnostic.S_value` | Auditory-cortex coherence index | Between 2.4 and 2.828 (drivers fuse into single percept) | < 2.0 (drivers heard separately) |
| `chsh_diagnostic.coherence_score` | S normalised to [0,1] = (S − 2)/(2.828 − 2) | > 0.5 (system is structurally coupled) | < 0.0 (independent), 0.0–0.3 (weakly coupled) |
| `chsh_diagnostic.coherence_verdict` | Classification: `coupled` / `borderline` / `independent` / `anomalous` | `coupled` | `borderline` or `independent` |
| `chsh_diagnostic.classical_bound` | 2.0 — the "drivers acting independently" threshold | (constant — for reference) | (constant — for reference) |
| `chsh_diagnostic.tsirelson_bound` | 2.828 — the maximum physical coherence | (constant — for reference) | (constant — for reference) |
| `chsh_diagnostic.per_pair_S` | S-value per channel pair | All > 2.0 | One or more < 2.0 = that pair is the weak link |

**S-value interpretation for audio:**

- `S < 2.0`: drivers are acting **independently**. The auditory cortex perceives multiple sources. Imaging is fragmented. Engineering action: identify which pair has low per-pair S and address that crossover region first.
- `2.0 ≤ S < 2.4`: drivers are **borderline coupled**. Image holds in some regions of the band but breaks elsewhere. Often a single-pair problem.
- `2.4 ≤ S < 2.7`: drivers are **structurally coupled**. The system passes most listening tests; image holds across the audible band. Most well-tuned commercial speakers land here.
- `2.7 ≤ S ≤ 2.828`: **maximum coherence**. The drivers fuse into a single emitter at the auditory cortex. This is the target for absolute-coherence designs.
- `S > 2.828`: **anomalous**. Should never happen physically; indicates a measurement error, engine bug, or input data with structure that violates the classical/Tsirelson framework. Investigate.

**This is the single number that answers the design question.** Every other diagnostic in CNQ v2 is decomposition that helps you find what's pulling S down when it's not where you want it.

---

## 4. Calibration practice — how to use CNQ v2 for audio system design

### 4.1 Standard measurement protocol

1. **Capture impulse responses** for each driver of the system using a calibrated reference microphone at the design listening position. Use a sweep tone or MLS test signal; per-driver IRs at 48 kHz / 24-bit / minimum 1 second window.
2. **Compute per-driver power spectra** via FFT (window: Hann or Blackman; bin resolution: 1/8-octave or finer).
3. **Build the input CSV**: rows = frequency bins (T values); columns = drivers (D values); value at row t, column j = per-driver acoustic power at frequency f_t.
4. **Run CNQ v2** with appropriate dimension (D=8 stereo, D=16 quadraphonic). The engine automatically applies twin-quaternion factoring at D=8 and quad-quaternion factoring at D=16 (when v2.1 ships).
5. **Read the report**, starting from `chsh_diagnostic.S_value` and drilling down through the per-pair S, then twin-quaternion ρ_AB, then helmsman σ chatter, then radial trajectory dips.

### 4.2 Iteration loop

The engineering loop is:

1. Measure the system. Compute S.
2. If S is below target, find the weakest sub-diagnostic (lowest per-pair S; largest ρ_AB drift; chatter region in σ; radial dip at a crossover).
3. Adjust the crossover, time alignment, or driver level for that region. Re-measure.
4. Repeat until S converges to the target band.

CNQ v2 doesn't tell you what physical adjustment to make. It tells you where the coherence is failing. The audio engineer's experience does the rest.

### 4.3 Listening-test correlation

The acceptance test is psychoacoustic. CNQ v2's job is to make the listening test **predictable**: when S > 2.7 across the audible band, the system should pass listening evaluation; when S < 2.4, it should fail. The exact correlation between numerical S and perceptual unity is a calibration that depends on the listener and the room. Recommended practice: track S alongside listening-test outcomes for a known reference system and establish the local correlation curve.

---

## 5. Worked example — a misaligned 4-way stereo

### 5.1 Setup

- D = 8 (4-way stereo, drivers `L_HF, L_HMF, L_LMF, L_LF, R_HF, R_HMF, R_LMF, R_LF`)
- T = 1024 (FFT bins, 20 Hz to 20 kHz logarithmic)
- Hypothetical system: L-LF driver is delayed 0.5 ms relative to spec (a common time-alignment error after rebuild)

### 5.2 Expected CNQ v2 output

- `chsh_diagnostic.S_value`: 2.18 — borderline. The single number says "system is not fully coherent."
- `chsh_diagnostic.per_pair_S`: 3 of 4 pairs above 2.4 except `(L_LF, R_LF)` at 1.83 — the weak pair.
- `twin_quaternion_factoring.coupling.rho_AB_summary`: mean 0.31 rad, std 0.42 — drifting coupling, large variation.
- `twin_quaternion_factoring.coupling.rho_AB_per_step`: small (< 0.1) at HF/HMF/LMF; jumps to > 0.6 in the LF region (below 250 Hz).
- `helmsman_family.sigma[t]`: clean 4-way structure for both channels at HF/HMF/LMF; sigma chatters between L_LF and R_LF below 250 Hz.
- `helmsman_family.flips.rolling[w=64]`: spike at the LF region.
- `cnq_view.radial_trajectory.ilr_norms[t]`: smooth across band — system EQ is fine; only phase/time alignment is off.
- `attractor_fit.period_stability`: 0.78 — period structure is somewhat stable but lower than expected for clean 4-way.

### 5.3 Diagnosis

The CHSH S-value flags non-coherence. The per-pair S identifies LF as the weak pair. ρ_AB(t) localises the issue to the LF region specifically. σ chatter between L_LF and R_LF confirms time-alignment failure (each driver alternately leading). Radial trajectory normal = not an EQ or level issue. Engineering action: re-align L_LF in time, re-measure, expect S to climb above 2.4.

This is the level of diagnostic specificity CNQ v2 provides when read through the audio wrapper.

---

## 6. Wrapper limits and engineer's role

This wrapper translates engine output to audio quantities; it does not extend or modify the engine. CNQ v2 measures coherence; the engineer interprets what the numbers mean for the specific system, room, and listening criterion. The math doesn't replace the listening test; it makes the listening test reproducible and the design iteration faster.

The full engine math is in `HCI-CNQ/engine/CNQ_V2_PSEUDOCODE.md`. The neutral schema is in `HCI-CNQ/engine/CNQ_V2_SCHEMA.md`. The architecture rationale (why D=8 is load-bearing, why the engine is domain-neutral, why wrappers exist) is in `ai-refresh/CNT_V3_CNQ_V2_DESIGN.md` §11. This document is the bridge from CoDa algebra to acoustics — what every engine output channel *means* when the input is sound.

> *"16 driver levels that present as one at the auditory cortex."*
> — Peter, push #32 directive, the design strictness driver

That is the design target this wrapper serves. CNQ v2 is the instrument that tells you whether you've reached it. The engine itself is general-purpose; this wrapper is the audio-specific lens through which audio engineers can read it.

---

End of audio wrapper.
