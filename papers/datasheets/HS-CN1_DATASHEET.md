＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
  HS-CN1  ·  Compositional-Navigation Instrument  ·  MC-4 Class
  DETERMINISTIC · HASH-RECEIPTED · COHERENCE-GATED        DATASHEET — Rev A, 2026-06-23
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

*Manufacturer: Higgins Unified Framework (HUF) / Rogue Wave Audio lineage. Author: Peter Higgins (human
authorship for all claims); AI-assisted per HUF-STD-001. This datasheet is written **backwards from measured
results** — every characteristic cites a receipted experiment. Honest-broker tiered. Not for flight without
the operator's gate; full automation is never possible by design.*

---

## 1. DESCRIPTION

The **HS-CN1** is a deterministic instrument that reads **compositional data** — parts of a conserved whole
(power budgets, generation mixes, fleet-health fractions, gas/ion shares, allocation weights, spectral
occupancy) — as **motion in log-ratio (Aitchison) geometry**. It returns a structured, reproducible read of a
composition's *shape* and its *departure from the ground state*, with a **SHA-256 content receipt** so any
result can be re-verified bit-for-bit on any platform. It is a reader, a generator, a codec, and a noise
front-end in one exact map (the "morphology"). It flies nothing and replaces nothing; it is a second viewpoint
on data already collected.

**Measurement Category:** MC-4 (*composition monitoring* — the conserved-budget / relative-information class),
complementing the classical MC-1 (level/amplitude), MC-2 (spectral), MC-3 (statistical) categories. Where
MC-1…3 read magnitudes and distributions, **MC-4 reads the ratios** — and the HS-CN1 is the deterministic,
receipted MC-4 instrument.

## 2. FEATURES (each measured; receipt cited)

- **Exact at the rung.** 4-part composition ↔ unit quaternion; Aitchison perturbation = `q v q*` = SO(3) to
  **≈1.3×10⁻¹⁵** (IEEE floor). *(exact_dim4 / HS-GOLD-1 F1)*
- **Scales to any dimension.** Exact SO(n) generation/rotation to **n = 1024** (orthogonality ≈1.8×10⁻¹⁵);
  high-D compositions tiled into exact 4-charts. *(son_generator, `8107b173`)*
- **Deterministic.** Same input → same output → same SHA-256. Frozen conformance set **HS-GOLD-1**, master
  `d7ac6530…`.
- **Common-mode rejection: 313 dB (exact).** Closure + log-ratio cancels any gain common to all parts to
  machine precision. *(ground_state_common_mode, `d8c21c70`)*
- **Deterministic additive denoise.** Off-coherent-subspace noise removed at **10·log₁₀((D−1)/k) dB**;
  known-structure interferers subtracted to the floor (**28 dB** demo). *(deterministic_denoise, `cb0c3f52`)*
- **Source coder.** ~**3.5–10×** compression on real compositional data, within ~10% of symbol entropy
  (no Shannon claim). *(compression_benchmark, `305cc0db`)*
- **Codec.** Generator↔reader are exact inverses; byte-exact message round-trip over `⌊n/2⌋` rotation channels.
- **Self-knowing.** The *blindness suite* (ratio-/mass-/rotation-blind) names what each read cannot see; the
  coherence gate **withholds** rather than guessing.

## 3. ABSOLUTE MAXIMUM / OPERATING BOUNDARIES (the honest "abs-max")

| condition | rating | note |
|---|---|---|
| input must be a **composition** | parts of a conserved whole, strictly positive | else the qualifier gate refuses (instrument-not-data) |
| common-mode multiplicative noise | rejected **exactly**, any magnitude | by closure |
| additive noise OFF coherent subspace | removed exactly, `10log₁₀((D−1)/k)` dB | needs low effective dim k<D−1 |
| additive noise IN subspace, random | **NOT separable** — returns 0 dB | the instrument says NO, by design |
| high-D reconstruction | numerical (not bit-exact identity) above D=4 | tiling, not a native rotor |
| automation | permitted **behind breakers only**; operator holds Breaker 16 | full automation never possible |

## 4. CHARACTERISTICS (measured)

| parameter | symbol | value | conditions / receipt |
|---|---|---:|---|
| Exact-rung residual | ε₄ | 1.3×10⁻¹⁵ | D=4 sandwich vs SO(3) · F1 |
| SO(n) generation residual | ε_gen | 1.8×10⁻¹⁵ | to n=1024 · `8107b173` |
| Common-mode rejection | CMRR | **313 dB** | 26.7 dB gain swing · `d8c21c70` |
| Reciprocation residual | — | 2×10⁻¹⁶ | log(a/b)+log(b/a) |
| Off-subspace denoise | G_dn | 10·log₁₀((D−1)/k) dB | measured = theory ±0.04 dB · `cb0c3f52` |
| Known-structure rejection | — | 28 dB | periodic interferer · `cb0c3f52` |
| Recursion (EITT) entropy drift | — | 0.17 % | 9× geometric-mean decimation |
| Compression vs lossless float | — | ~10× | real D=8 energy mix · `305cc0db` |
| Determinism | — | bit-exact | HS-GOLD-1 master `d7ac6530` |

> **Note on the 313 dB (read before comparing to an instrumentation amplifier).** This is a **numerical**
> rejection of common-mode *multiplicative* gain in exact float64 arithmetic — limited by machine epsilon
> (~10⁻¹⁵ ≈ 300 dB), **not** an analog CMRR. It is the multiplicative twin of CMRR, runs *after* digitization,
> and is bounded in any real system by the **ADC/sensor front end** (e.g. 24-bit ≈ 144 dB), not by the math.
> For reference, the best commercial instrumentation-amp CMRR ≈ 130 dB; idealized research topologies ≈
> 200–246 dB (simulation). The honest claim is **not** "a 313 dB instrument" but "the digital common-mode
> stage adds ~zero error of its own, so the front end is the only limit." T1 = the numerical figure; the
> end-to-end system figure is front-end-bound (T2).

## 5. FUNCTIONAL BLOCK DIAGRAM

```
   raw parts x_i ──► [QUALIFIER GATE] ──► [CLOSURE] ──► [CLR / ILR]  ──► [COHERENCE GATE] ──► read
   (conserved      reject if not       (÷ total =       (log-ratio =      (withhold if         (shape,
    budget)         compositional)      common-mode      differential      incoherent)          motion,
                                        rejection)        / reciprocal)                          faces)
                          │                                                      │
              magnitude M = Σx_i ───────────────────────────────────────────────┴──► size channel (kept!)
                                                                                       └► additive denoise
                                                                                          (subspace project)
   ◄──────────────────── SHA-256 content receipt stamped on every output ────────────────────►
```

## 6. APPLICATION CIRCUITS (see Application Notes)

- **AN-001 — Deterministic Noise Rejection** (common-mode + additive front-end). *This release.*
- Suggested: AN-002 fleet pre-fault monitor · AN-003 telemetry source-coder/codec · AN-004 sensor-array
  conductor (multi-expert fusion) · AN-005 non-coherent unitary constellation. *(named; built on demand.)*

## 7. CONFORMANCE / ORDERING

Conformance is the frozen **HS-GOLD-1** fixture set (`experiments/conformance_fixtures_2026-06/`); a build is
"genuine HS-CN1" iff `hs_gold_fixtures.py --verify` reproduces master `d7ac6530…`. Open determinism contract:
HS-EPS-1. Reference implementation + four-form port available. License/governance per repo.

## 8. TIERS & GOVERNANCE

**T1** all §4 characteristics (measured, receipted). **T2** application architectures (AN-002…005, reasoned).
**T3** any field/hardware number — to earn with a receipt; any "beats Shannon / cancels all noise / lossless at
scale" claim — **rejected**. Operator is the sole gate; nothing posted; instrument-not-data; safety dominant.

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
