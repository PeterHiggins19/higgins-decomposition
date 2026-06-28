# HS-PROBE — datasheet (the filter-injection differential instrument)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The
actual instrument built from the ultrasonic-probe test: a non-invasive, reciprocation-based reader that
**locks onto a composition's structure by differencing the return against a known reference**, rejecting a
multiplicative common-mode exactly. Module: `hs_probe.py` (self-test fixture `ff9c68156d7af68a`).
**RESEARCH / QA INSTRUMENT ONLY — not a clinical or diagnostic device.** Honest-broker tiered; Peter is the
sole gate; nothing posted.*

---

## What it does

Given a **known reference** (an injected filter signal, or a healthy/baseline template) and a **return**
(the measured composition), the instrument computes the structural deviation in log-ratio space:

```
   z = clr(return) − clr(reference)
```

Because `clr(g·x) = clr(x)`, any **multiplicative common-mode** `g` — source level, coupling/couplant
efficiency, sensor gain, dilution — is **reciprocated away exactly**. What remains, `z`, is the structure:
the relational signature of the part under test, with the dominant deviating component located (`lock`) and a
drift/flaw distance reported (`detect`).

## Interface

| call | purpose |
|---|---|
| `HsProbe(reference)` | set the known injection / healthy template |
| `.read(return)` | `z` = structure deviation (common-mode rejected) |
| `.lock(z)` | the dominant deviating component (index + magnitude) — the geometry lock |
| `.detect(return, thresh)` | Aitchison drift distance + a flag |
| `.receipt(obj)` | SHA-256 content seal |
| `self_test()` | known-hash conformance (10× common-mode → identical read) |

## Operating envelope (where it works — and where it does not)

| nuisance present | behavior | use |
|---|---|---|
| **scalar multiplicative** (gain, coupling, source level, dilution) | **rejected exactly** (~10⁻¹⁶) | the design case — read structure through it |
| **true relational change** (a real shift in proportions) | **detected** (Aitchison distance rises) | the signal you want |
| **additive offset / baseline** | **NOT rejected** | pre-condition the raw signal first; clr is not the tool for additive |
| **per-channel fixed gain** (miscalibration) | **partially** rejected (a constant clr bias remains) | calibrate, or use the Paired-Measurement reference channel |
| **non-compositional raw signal** | out of scope | the input must be parts of a budget (a composition) |

## Honest tiers

- **T1 (exact, measured):** the scalar common-mode cancellation and the known-hash self-test. Verified on
  three real public datasets (see `HITS_AND_MISSES.md`).
- **T2 (model):** the ultrasonic realization (`../THE_FILTER_INJECTION_PROBE.md`) uses synthetic transfer
  functions; numbers there are model numbers.
- **T3 (to earn):** real ultrasonic NDE hardware data; a real breathing-gas / sensor-drift dataset; the
  Paired-Measurement reference channel for frequency-shaped nuisances.

## The firm bar (medical)

This is a **research / quality-assurance instrument**. It is **not** a clinical, diagnostic, or
life-support control device, and must not be used as one. Any medical application requires validation to the
applicable standards (IEC 62304 software lifecycle, ISO 13485 quality system, and the relevant regulatory
clearance). The instrument reads compositions; it does not make medical decisions. The operator holds the
gate.

*Cross-refs: `hs_probe.py`, `probe_public_data_tests.py`, `PUBLIC_DATA_TEST_RESULTS.json`, `HITS_AND_MISSES.md`,
`../THE_FILTER_INJECTION_PROBE.md`, `../../papers/datasheets/AN-001_DETERMINISTIC_NOISE_REJECTION.md`.
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the cancellation is exact · the limits are listed, not hidden · medical use is fenced · experts decide.*
