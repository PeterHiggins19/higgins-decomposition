# Mudstone CNT/CNQ — available data + test plan (public)

**Verdict: yes, it can be done now.** CNT runs on any down-section compositional series (lossless at any D). CNQ is exact only at D=4, so for a native quaternion reading we reduce to **four geological balances**; at full element count CNQ runs as a projected diagnostic (`captured_step_fraction` reported). Open mudstone data exists and is test-ready.

## Test-ready open datasets
1. **Thöle et al. (2019), PANGAEA — best first test.** XRF core-scan **and conventional (quantitative) XRF**, plus grain size, bulk organic δ¹³C, CaCO₃ and **TOC**, of **Lower Cretaceous mudstones**, eastern Lower Saxony Basin, Germany — elemental composition over depth. It is *literally mudstone*, has calibrated wt% (not just counts), and carries **TOC / CaCO₃** so we can calibrate CNT readings against geologically meaningful targets (TOC estimation from chemostratigraphy is squarely the published Wehner-style application). `doi.org/10.1594/PANGAEA.898094`
2. **Gong et al. (2022), PANGAEA — IODP Site U1483** XRF-scanning elemental data (10 kV & 30 kV), high-resolution down-core. `PANGAEA.948034` / `948032`
3. **Other PANGAEA XRF core-scanner sets** (GeoB cores; Lake Alchichica, Safaierad et al. 2026) — abundant open composition-vs-depth.
4. **Calibration target if shared:** the published Eagle Ford / Wolfcamp XRF sections (Wehner et al.; UTA theses Nikirk, Abdi) — ideal because the surfaces are already interpreted.

## Test design (first pass)
1. **Basis:** use calibrated wt% (conventional XRF) for rigor; a coherent ~8–12-part major set (Si, Al, Ti, K, Fe, Ca, Mg, Mn, P, S) with a redox trace sub-suite (V, Mo, Ni, U) handled as its own closed sub-composition.
2. **Zeros:** Bayesian-multiplicative replacement for below-detection trace values (mandatory — not the 1e-15 floor); record the constant.
3. **CNT down-depth:** Aitchison step (→ candidate surfaces), helmsman (→ driver: detrital ↔ carbonate ↔ redox), flips/directness (→ trend vs reorganization), regime tripwires (→ candidate boundaries), deceptive-drift on the trace sub-suite (→ subtle redox/ash/provenance markers).
4. **CNQ:** (a) **native D=4** on four geological balances — e.g. detrital-vs-carbonate, redox, productivity, grain-size proxy — for an exact quaternion reading; or (b) projected diagnostic at full D with `captured_step_fraction`.
5. **Calibrate:** do the regime tripwires land on known surfaces/facies? does deceptive-drift flag the redox/TOC excursions (Thöle's TOC column is the check)?

## Honest caveats
- Prefer calibrated wt% over raw scanner counts (counts are semi-quantitative); Thöle provides both.
- Keep D modest (~≤12) for the first run (the `compute_stage3` ladder caveat bites at high D — see working notes §5).
- Research-grade, calibration-gated; CNT flags candidates, the geologist interprets.

## Next step
Fetch the Thöle dataset, run a first CNT pass (+ the D=4-balance CNQ), and overlay the readings on its TOC/CaCO₃ and any published surfaces — a self-contained, reproducible proof on real mudstone. Ready to run on request.

## Sources
- [Thöle et al. 2019 — Lower Cretaceous mudstones XRF + TOC (PANGAEA)](https://doi.pangaea.de/10.1594/PANGAEA.898094)
- [Gong et al. 2022 — IODP U1483 XRF-scanning (PANGAEA)](https://doi.pangaea.de/10.1594/PANGAEA.948034)
- [Eagle Ford chemostratigraphy thesis (Nikirk, UTA)](https://mavmatrix.uta.edu/ees_theses/7/) · [Austin Chalk / Upper Eagle Ford (Abdi, UTA)](https://mavmatrix.uta.edu/ees_theses/108/)
