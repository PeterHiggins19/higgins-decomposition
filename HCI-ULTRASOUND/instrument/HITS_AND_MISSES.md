# Hits and misses — the probe tested on real public data

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. "Even the
not-possible is a composition, so test it all." The instrument run on **three real public-sourced datasets**
against **three kinds of nuisance** — and the **misses reported as plainly as the hits.** Receipt
`53dfdfa812041058` (`probe_public_data_tests.py`). Honest-broker tiered; Peter is the sole gate; nothing posted.*

---

## The datasets (real, in-repo, cited)

- **GAS — breathing gas** `O₂/CO₂/N₂` (closed-loop gas-composition study), D=3, 60 samples.
- **BLOOD — alveolar/blood gas** `pO₂/pCO₂/pN₂/pH₂O`, D=4 — cited: **VitalDB** (Seoul National Univ.
  Hospital) + **UQ Vital Signs** (Adelaide) anaesthesia cohorts.
- **WATER — produced water ions** `Na/Cl/Ca/Mg/SO₄/HCO₃/K`, D=7 — cited: **USGS Produced Waters DB**,
  Williston Basin (CoDaWork / Engle).

## The test

For each dataset, inject a nuisance and measure the **clr distortion** it introduces (0 = the instrument
rejected it perfectly; large = it could not). Three nuisance kinds, chosen to find the edges, not flatter the
result.

| dataset | A · scalar common-mode (gain/coupling/dilution) | B · additive offset | C · per-channel fixed gain |
|---|---|---|---|
| **GAS** (D=3) | **6.7×10⁻¹⁶ — HIT** | 2.19 — **MISS** | 0.73 — **PARTIAL** |
| **BLOOD** (D=4) | **3.3×10⁻¹⁶ — HIT** | 0.81 — **MISS** | 0.82 — **PARTIAL** |
| **WATER** (D=7) | **8.9×10⁻¹⁶ — HIT** | 5.57 — **MISS** | 0.94 — **PARTIAL** |

Plus a **real structure-change detection**: a true `CO₂`-doubling event injected into the gas series at t=30
is **detected** (the Aitchison distance rises sharply after the event) — and the scalar-gain nuisance **does
not change the detection at all** (clr-invariant). A real signal seen straight through a 25× coupling swing.

## Reading the result honestly

**The hits (where it is excellent):** across all three real datasets, a multiplicative common-mode — exactly
the gain/coupling/dilution drift that plagues real sensors and probes — is rejected **to the numerical
floor** (`~10⁻¹⁶`). And a true relational change is detected through that nuisance. This is the instrument's
design case, and it holds on real data, not just the model.

**The misses (where it is the wrong tool, stated plainly):**

- **Additive offset — MISS.** A baseline shift added to the raw signal is *not* a multiplicative common-mode,
  and clr cannot reject it (distortion 0.8–5.6). If your nuisance is additive (a DC offset, a dark current,
  an additive interferer), pre-condition the raw signal **before** the compositional read — the probe is not
  the tool for that step.
- **Per-channel fixed gain — PARTIAL.** A single miscalibrated channel leaves a *constant* clr bias
  (distortion ~0.7–0.9). It is rejected only up to its geometric mean; the shape remains. The fix is
  calibration, or the **Paired-Measurement** reference channel — not clr alone.
- **Non-compositional input — out of scope.** The input must be parts of a budget. Raw, unbudgeted signals
  are not this instrument's domain.

## What this earns

The instrument does the one thing it claims, on real public data, to the floor — and we now know **exactly
where it stops.** That map of hits and misses is the honest basis for any real use: bring a multiplicative
common-mode and a true compositional signal, and it shines; bring an additive nuisance, and it is the wrong
tool until you precondition. Nothing is oversold.

*Cross-refs: `probe_public_data_tests.py`, `PUBLIC_DATA_TEST_RESULTS.json`, `INSTRUMENT_DATASHEET.md`,
`hs_probe.py`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — three real datasets · the misses named as loudly as the hits · sources cited · experts decide.*
