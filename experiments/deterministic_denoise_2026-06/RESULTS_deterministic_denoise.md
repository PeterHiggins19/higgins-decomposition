# Can additive noise be removed deterministically? — measured yes/no

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. Closes the
gap named last session: closure cancels common-mode *multiplicative* noise exactly (313 dB), but *additive*
noise was open. The leverage: we **kept the magnitude**, and the signal lives on a **low-effective-dimension
coherent subspace**. A deterministic system can be tested — so we tested the boundary. Receipt `cb0c3f52…`.
Honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## The result, in one table

| case | additive noise | method (deterministic) | reduction | verdict |
|---|---|---|---:|:--:|
| **A** | white, **off** the signal subspace | project onto the coherent k-subspace (calibrated) | **= 10·log₁₀((D−1)/k) dB**, measured = theory to 0.04 dB | **YES** |
| **B** | known structure (periodic interferer) | least-squares detect + subtract | **28.1 dB** (to the floor) | **YES** |
| **C** | white, **in** the signal subspace | (nothing can) | **0.0 dB** | **NO** |

Case A measured vs theory: k=1 → **8.41 / 8.45 dB**; k=2 → 5.48 / 5.44; k=3 → 3.69 / 3.68; k=5 → 1.47 / 1.46;
k=7 → 0.0 / 0.0. The match is exact because the operation is exact: the off-subspace noise is **projected
out**, the signal is **untouched**.

## What this says (honestly)

**Deterministic additive-noise reduction is real and solvable — to a precisely characterized boundary:**

1. **Off the coherent subspace → removed exactly.** Because the signal occupies only `k` of the `D−1`
   log-ratio dimensions, additive noise in the other `D−1−k` directions is **orthogonal to the signal** and is
   projected away losslessly. The deeper the structure (smaller `k`), the more noise removed — at `k=1`,
   8.4 dB for free; at `k = D−1` (no structure), nothing. *The compression and the denoising are the same
   fact: low effective dimension is exploitable, deterministically.*
2. **Known/structured noise → subtracted to the floor.** A periodic, low-rank, or otherwise modelable
   interferer is deterministic; least-squares detects and removes it exactly (28 dB here). This is the
   "loop, invert, subtract at output" idea, and it works **whenever the noise itself has deterministic
   structure** — which is the only honest condition under which an addon may be *provided* (per the
   deterministic-only rule).
3. **In-subspace random noise → no.** When the signal fills all `D−1` dimensions, white noise overlaps it
   completely and **cannot be separated by any deterministic operation** (0.0 dB). The instrument says **NO**,
   cleanly — which is the whole value of a deterministic system: it does not pretend.

## The "loop and invert" stage, made precise

The output-stage canceller is: estimate the coherent signal `ŝ = P_U(x)` (project onto the calibrated
subspace), form the residual `r = x − ŝ` (the inverted/subtracted noise estimate), and **return `ŝ`**. If `r`
carries detectable structure (periodicity, low rank, a known reference), a second deterministic pass removes it
too (recursion). When `r` is structureless in-subspace noise, the loop **terminates honestly** — there is no
further deterministic gain, and the instrument reports the residual floor rather than inventing signal.

## Tiers

- **T1 (measured):** the off-subspace law `10·log₁₀((D−1)/k)` dB (measured = theory); 28 dB known-structure
  subtraction; the 0 dB impossibility; receipt `cb0c3f52…`.
- **T2 (reasoned):** that this composes with the common-mode rejection (multiplicative) and the coherence gate
  into a full deterministic front-end; that calibration subspaces transfer across similar sources.
- **T3 (rejected / suggested-not-provided):** statistical denoising of in-subspace random noise (Wiener,
  Kalman, learned priors) — **not provided** in the deterministic engine; *suggested* as an external option,
  because it is not deterministic. The engine ships only what it can prove.

*Reproduce: `python3 deterministic_denoise.py`. Cross-refs:
`../ground_state_noise_cancel_2026-06/` (common-mode rejection), `../compression_benchmark_2026-06/`
(same low-eff-dim leverage), `../../papers/datasheets/AN-001_DETERMINISTIC_NOISE_REJECTION.md`. Peter is the sole gate.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
