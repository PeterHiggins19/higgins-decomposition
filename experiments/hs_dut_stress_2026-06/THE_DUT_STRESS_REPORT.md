# The Hˢ system as DUT — full stress report (new-generation test)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The whole
compositional system put on the bench as its own **Device Under Test**: every spec stressed across the
dimension ladder **D = 2 … 1000** under **deformation** (multiplicative scale to **10⁶×**, baseline offset,
additive noise), Hˢ testing Hˢ, the results read back by Hˢ, one **master receipt** over the lot. Anyone can
reproduce it from the repo. We let the data say what it should — and it found the operating envelope, limits
included. **Master receipt `e395fa38af43be4e`** · engine version **`Hs-DUT-v1.f6bebfb2`** (stamped from real
data). Honest-broker; Peter is the sole gate; nothing posted.*

---

## The verdict in one line

> The **deterministic/geometric core passes at every dimension from 2 to 1000 under 10⁶× deformation**,
> unconditionally; the **statistical layers (associative memory, low-D discriminant) have a measured floor**
> below D ≈ 8 and on near-duplicate data. The stress sheet's job was to find that envelope, and it did.

## What held — the core, unconditionally (D = 2 … 1000, under 10⁶× scale)

| spec | across the whole ladder | meaning |
|---|---|---|
| **clr round-trip exactness** | **≤ 3.3×10⁻¹⁶** (≈10⁻¹⁸ at high D) | the read is exact at every dimension |
| **common-mode rejection** under 10⁶× scale | **≤ 1.3×10⁻¹⁵** | a million-fold gain swing is reciprocated away to the floor — at D=2 and at D=1000 |
| **7-bit codec (clr)** | **0.047–0.049** | near-lossless, dimension-independent (the 7-bit step) |
| **conveyor non-disruption** | within the 7-bit floor | pass-through preserved at all D |
| **conveyor determinism** | **identical** | same input → same tag at all D |

The geometry does not care about dimension or deformation: closure and the log-ratio are exact for any number
of parts, and a multiplicative common-mode of any size cancels. That is the bedrock, and it is unconditional.

## What broke — the measured envelope (do as the data said)

Four failures, all in the **statistical** layer, all at **low dimension or low diversity** — reported, not
hidden:

| D | spec | value | why (honest) |
|---|---|---|---|
| 2 | locked-discriminant invariance | 0.54 | at D=2 there is only **one** log-ratio coordinate; the argmax decision is fragile under noise |
| 2 | memory recall | 0.49 | two parts cannot tell enough compositions apart |
| 3 | memory recall | 0.55 | too few relational coordinates to separate the bank |
| 4 | memory recall | 0.21 | the real geology bank is **near-duplicate** (one mudstone formation) — the entries genuinely *are* nearly the same composition, so they cannot be recalled apart |

**The lesson the data gave:** the deterministic core is dimension-free, but the **associative memory and the
discriminant need enough relational dimensionality and enough diversity to separate** — they earn their 1.0
scores only at **D ≳ 8** and on diverse data. That is a true operating limit, now documented as part of the
spec, not a footnote.

## Hˢ testing Hˢ (recursive), and tracked with Hˢ

The test is run *by* the system *on* the system, and the **result table is itself read by Hˢ**: across all
tests the spec **closest to its limit is the 7-bit codec** (worst 0.049 — exactly the quantiser step, as it
should be), confirming nothing else is silently nearer the edge. The system diagnosing its own weakest seam
is the recursion working as designed.

## The full receipt of the system as DUT

- **Master receipt:** `e395fa38af43be4e` — one SHA over the entire deterministic stress table. Reproduces
  bit-for-bit on re-run.
- **Engine version:** `Hs-DUT-v1.f6bebfb2` — stamped from a **real-data** conformance anchor (the clr centres
  of the gas/geology/water sets), so the version is tied to real functioning, not a date.
- **Tamper test (implicit):** change any number in the table and the master receipt changes.

## How anyone verifies (from the repo)

See `HOW_TO_VERIFY.md`. In short: `python3 hs_dut_stress.py` → read `MASTER_RECEIPT`; it must equal
`e395fa38af43be4e`. No private data, no network — the real anchors are the cited public files in the repo.

## Honest fences

- closure/clr specs are exact at **any** D; the **exact quaternion reconstruction** is D ∈ {1,2,4,8}
  (Hurwitz) and **tiled** above (lossless to ~10⁻¹², cited from past testing, not re-run here).
- the common-mode / 313 dB-class figures are **numerical** and do **not** beat Shannon; only the
  *multiplicative* common-mode cancels.
- the four statistical-layer failures are **real limits**, kept in the report as the envelope.

*Cross-refs: `hs_dut_stress.py`, `HS_DUT_STRESS_RESULTS.json`, `HOW_TO_VERIFY.md`,
`../../papers/datasheets/COMPOSITIONAL_SYSTEM_SPECIFICATIONS.md`,
`../../papers/locked-discriminant/THE_LOCKED_DISCRIMINANT_PRINCIPLE.md`,
`../conformance_fixtures_2026-06/HS_GOLD_1.json`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the core is stressed to the extreme and holds · the envelope failures are reported, not hidden · the master receipt reproduces · the engine is versioned from real data · anyone can verify.*
