# The tetrode test — making the data pay for its lack of determinism (3 independent witnesses)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. The sensitive
case (P-μ, cancer-incidence epidemiology) carries one concern: the DUT data is noisy and non-deterministic. The
answer is not to make Hˢ less exact — it is to **distribute the error across the DUT and let statistics + the
math of scale cancel it**, while Hˢ stays at the IEEE floor. This completes the test the project's own way:
**three independent witnesses** (3-to-locate), each receipted, plus the **tetrode (N=4)** extension for sensitive
cases. Measured: `hs_tetrode_determinism.py`, master receipt `8515f97ecb8f23f6`. Peter is the sole gate; nothing
posted.*

---

## The idea: the error is in the data, never in the instrument

A measurement of a composition is non-deterministic; the instrument that reads it need not be. So **make the data
pay for its lack of determinism.** Take N redundant elements of the same underlying composition (a **tetrode** =
4 — the sensitive-case extension) and split their error into two parts, each of which is removed by basic math:

- **Common-mode error** — a shared per-element multiplicative gain / scale. **Cancelled exactly** by the
  centered-log-ratio: `clr(g·x) = clr(x)`, so any common scale leaves no trace. Measured residual **~1×10⁻¹⁵**
  across all three witnesses — the **"never Hs"**: the instrument contributes nothing.
- **Independent error** — per-element, per-part noise. **Averaged down by the law of large numbers**, ~σ/√N:
  more elements, more ways to find the determinism hidden in the noise.

So: clr each element (kills the common mode), average across the N elements (kills the independent part),
exp + closure back. A non-deterministic read is made deterministic and receipted.

## The test, completed — three independent real witnesses (3-to-locate)

Run on **three independent real DUT datasets**, the repetition across domains being the signal:

| witness (real DUT) | parts D | common-mode residual | single (N=1) | **tetrode (N=4)** | N=16 | scale-law slope | Hˢ floor |
|---|---|---|---|---|---|---|---|
| **Energy** (EMBER India) | 8 | 9×10⁻¹⁶ | 0.398 | **0.198** | 0.101 | **−0.497** | 3×10⁻¹⁸ |
| **Geochemistry** (Ball oxides) | 10 | 6×10⁻¹⁶ | 0.452 | **0.227** | 0.110 | **−0.509** | 6×10⁻¹⁷ |
| **Commodities** (gold/silver) | 2 | 7×10⁻¹⁶ | 0.154 | **0.070** | 0.038 | **−0.522** | 1×10⁻¹⁶ |

All four checks pass on all three: the common mode is cancelled **exactly**; the **tetrode beats a single read**;
the independent error falls as **~1/√N** (slopes −0.50 ± 0.02 — the textbook law of scale); and **Hˢ sits at the
IEEE floor** (~10⁻¹⁷). Three independent domains, one behaviour — the concern is reduced not by argument but by
**independent reproduction plus redundancy.**

## What it gives the sensitive case (P-μ, and the medical family)

For a sensitive read like cancer-incidence epidemiology, the recommendation is concrete: **acquire the
composition on a tetrode — four independent channels** (e.g. four registries, four sub-cohorts, four assay runs).
The common-mode differences between channels (overall scale, reporting rate) vanish exactly under clr; the
independent noise drops by half at N=4 and keeps falling with more elements. The determinism the data lacks is
**recovered from its own redundancy**, with a receipt — and none of it is borrowed from Hˢ, which only ever
performs the exact read.

## Honest scope

- **T1 (measured):** the common-mode exactness (~10⁻¹⁵), the 1/√N law (slopes −0.50 ± 0.02), the tetrode
  improvement, and the Hˢ floor (~10⁻¹⁷), across three independent real datasets, reproduce (`8515f97ecb8f23f6`).
- **The boundary:** common-mode cancellation is **exact only for strictly-positive compositions** (the
  locked-discriminant precondition; structural zeros excluded, E-21). The 1/√N law assumes **independent**
  per-element noise; **in-subspace correlated noise is provably not separable** — redundancy cannot remove an
  error that is common to the signal you are reading. The real datasets supply realistic compositions; the DUT
  noise model is the controlled, declared part.
- **Sensitive-case fence (unchanged):** P-μ remains **population epidemiology, not clinical/diagnostic/treatment**;
  the tetrode improves the *measurement*, it does not change that line.
- **Sole gate:** Peter. **Nothing posted.**

*Cross-refs: `hs_tetrode_determinism.py` (`8515f97ecb8f23f6`); `A_RECEIPTED_READ_FOR_CANCER_EPIDEMIOLOGY.md`
(P-μ, the sensitive case); the common-mode-rejection lineage (313 dB, `papers/ABSTRACT_LEDGER.md` P-C/P-Ω);
`../../library/knowable_floor_one_law.py` (the scale law's cousin); `../TRIANGULATION_TRILOGY_PLAN.md`
(3-to-locate). Real data: EMBER, Ball geochemistry, commodities. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the error is placed in the DUT and cancelled by declared math, never in Hˢ · the
1/√N law and the exact common-mode rejection are measured on three independent real datasets · the
not-separable boundary stated plainly · the sensitive-case clinical fence unchanged · the human keeps the gate.*
