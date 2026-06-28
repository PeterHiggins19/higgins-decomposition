# RESULTS — EUV stochastic valley‑of‑death as a composition (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. Receipt
`877516b6`. `euv_stochastic_drift.py` (numpy + scipy). Honest‑broker tiered; no vendor relationship implied;
Peter is the sole gate.*

---

## Setup

Deterministic analytic‑Poisson model of the two‑sided EUV stochastic cliff. ~2000 photons/feature nominal;
under‑exposure (`k < 1740`, ~5.8 σ) → *missing/broken*; over‑exposure (`k > 2260`) → *bridge/merge*. A slow
downward dose drift of **1.000 → 0.975 over a 100‑wafer lot** (resist aging / source droop). Per‑wafer the
defect composition `{OK, missing, bridge}` is computed from the Poisson CDF (no sampling noise). Yield spec:
total stochastic defectivity `NOK = missing + bridge > 0.1 ppm`.

## Result

| quantity | value |
|---|---|
| Hˢ silent‑drift flag | **wafer 7** |
| total defectivity at the Hˢ flag | **0.0056 ppm** (far under spec) |
| single‑channel yield alarm (NOK > 0.1 ppm) | **wafer 69** |
| **Hˢ lead time** | **62 wafers** |
| arrow of intent | **missing/broken → steer dose UP** |
| nominal total NOK | 0.007 ppm |
| photon energy | 91.8 eV (13.5 nm) |

## Reading

1. **The ratio leads the count.** Hˢ flags while defectivity is ~0.006 ppm — about 18× under the 0.1 ppm spec —
   because the *log‑ratio* `missing/OK` moves long before the absolute count reaches the cliff edge. The total
   defect number is the late alarm; the composition is the early warning.
2. **The arrow is a signed correction.** Because the cliff is two‑sided, the read tells the operator *which way*
   to move dose (here: up, away from the missing‑contact cliff). A scalar total‑defect monitor is
   direction‑blind — it climbs on both sides of the valley.
3. **Same mechanism, hardest process.** This is the dispense‑clog silent drift (`cf9bf72f`) at the most advanced
   node on Earth: read the ratios, not the totals, and act early.

## Honest fences

- **Model numbers, not fab numbers.** Physics‑grounded (photon shot noise) but illustrative (T2). Real resist
  *chemical* stochastics ride on top of photon shot noise; the composition read is mechanism‑agnostic but the
  magnitudes here are from the model.
- **Lead time is spec‑ and drift‑dependent.** 62 wafers is for *this* spec and *this* drift rate; the durable
  claim is qualitative: the ratio is a leading indicator of the stochastic cliff.
- **Complement, not controller.** Hˢ advises; the process owner sets dose; the operator holds Breaker 16; full
  automation is never reached.

## Next (T3 — the proof a litho engineer will respect)

Run this exact composition read on **public imec / fab stochastic‑defect datasets** (dose–defect curves, NOK(CD)
data) and measure whether the ratio drift truly *leads* the yield excursion, and by how much. Only measured
output on cited public data may leave Tier 3.

*Cross‑refs: `README.md`, `CONCEPT_AND_MATH.md`, `../electronics-assembly-smt/COHERENCE_AND_LASERS.md`.
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited‑or‑fenced · math proven + receipted · value shown · experts decide.*
