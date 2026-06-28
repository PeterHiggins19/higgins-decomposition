＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
  APPLICATION NOTE  AN-001
  Deterministic Noise Rejection with the HS-CN1 (MC-4) Instrument
  Common-mode (multiplicative) + structured/off-subspace (additive)   Rev A · 2026-06-23
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. Written backwards from
measured, receipted results. Aerospace-component style: theory of operation → design equations → suggested
circuit → pseudocode → application examples → honest limits → traceability. Honest-broker tiered.*

---

## 1. SCOPE

How to use the HS-CN1 as a **deterministic noise-rejection front-end** for compositional signals (conserved-
budget telemetry: power/thermal mixes, generation shares, fleet-health fractions, gas/ion composition,
spectral occupancy, allocation weights). Covers what it removes **exactly**, what it removes **conditionally**,
and what it **cannot** remove — because the value of a deterministic part is that it answers **yes or no**.

## 2. THEORY OF OPERATION

Observed signal model (per channel i, time t):

```
   x_i(t) = g(t) · s_i(t) + n_i(t)
            └ common-mode    └ signal   └ additive
              gain (mult.)     (shape)    noise
```

**Stage 1 — Common-mode rejection (multiplicative), EXACT.** Closure then log-ratio:
`clr(g·s) = clr(s)`. Any gain common to all parts (level, distance, room/antenna gain, illumination, a common
broadband interferer) **cancels by reciprocation** — the multiplicative twin of a balanced/BTL line. *Measured:
**313 dB** rejection of a 26.7 dB gain swing, residual 5×10⁻¹⁶ (`d8c21c70`).* This is the RWA ground-state law:
the barycentre is the zero, the ratio measures the coherent departure.

**Stage 2 — Additive rejection, by structure (conditional, deterministic).** Closure does **not** cancel
additive noise. But the signal occupies only `k` of the `D−1` log-ratio dimensions (its effective dimension),
and the magnitude channel is kept. So:

- noise **off** the coherent k-subspace is **orthogonal to the signal** → projected out **exactly**.
  Gain `= 10·log₁₀((D−1)/k) dB` (measured = theory ±0.04 dB; 8.4 dB at k=1, 0 dB at k=D−1).
- **known-structure** noise (periodic / low-rank / a known reference) is deterministic → least-squares
  detect and subtract to the floor (**28 dB** demo).
- **in-subspace random** noise overlaps the signal completely → **not separable**; the instrument returns
  **0 dB** and reports the floor. (The honest NO.)

**Stage 3 — Coherence gate.** The read is returned only where coherent; the incoherent residual is **withheld**,
not reported as signal. Pure extraction = only the ground-state-relative coherent part leaves the output.

## 3. DESIGN EQUATIONS

```
   closure:        c = x / Σx                       (removes common-mode gain g)
   log-ratio:      z = clr(c) = log c − mean(log c) (differential; reciprocal-antisymmetric)
   ILR:            y = z · Hᵀ                        (D−1 orthonormal coords; H = Helmert)
   subspace:       U_k = topᵏ right-singular vecs of a CLEAN calibration block   (deterministic)
   denoise:        ŷ = mean + (y − mean) U_k U_kᵀ    (project onto signal subspace)
   residual:       r = y − ŷ                          (inverted noise estimate at output)
   known-struct:   ŷ ← ŷ − B (Bᵀ ŷ)  for known basis B (e.g. [sin, cos] @ f₀)   (loop)
   denoise gain:   G_dn = 10·log₁₀((D−1)/k)  dB       (off-subspace, exact)
```

## 4. SUGGESTED CIRCUIT (signal flow)

```
  sensors ─►(Σ)─► magnitude M ───────────────────────────────────────────┐ (kept: size channel)
     │                                                                    │
     └─► parts x ─►[QUALIFIER]─►[÷M : CLOSURE]─►[CLR/ILR]─►[SUBSPACE PROJECT U_k]─►[KNOWN-STRUCT NULL]─►[COHERENCE GATE]─► clean read
                    reject non-   (common-mode    (differential   (off-subspace        (periodic/low-rank   (withhold
                    compositional  rejection,313dB) reciprocal)     noise removed)       interferer subtract) incoherent)
                                                                         │
                                                                         └─►(residual r)─►[STRUCTURE DETECT]─► if deterministic: loop back & subtract
                                                                                                              else: report floor (NO)
   ◄──────────────────────── SHA-256 receipt stamped on the clean read (integrity) ────────────────────────►
```

*Analogy for hardware engineers:* CLOSURE ≈ an exact AGC (common-mode/level normalizer); CLR ≈ a balanced
differential stage (common-mode-rejecting); SUBSPACE PROJECT ≈ a deterministic adaptive canceller with the
filter fixed by calibration (no dither, no drift); COHERENCE GATE ≈ a squelch that opens only on coherent
signal.

## 5. PSEUDOCODE (engine addon — deterministic only)

```
function denoise(x_block, calibration_block, k, known_bases=[]):
    c   = closure(x_block)                 # Stage 1: common-mode gain cancelled
    y   = ilr(c)                            #          differential coords
    U_k = top_k_right_singular(center(ilr(closure(calibration_block))), k)
    yh  = project(center(y), U_k) + mean(ilr(closure(calibration_block)))   # Stage 2a
    for B in known_bases:                   # Stage 2b: deterministic structured noise
        yh = yh - B @ lstsq(B, yh)
    coh = coherence(yh)                     # Stage 3
    return where(coh >= floor, yh, WITHHOLD), sha256(canonical(yh))
# If residual (y - yh) has no detectable deterministic structure -> stop. Return NO, report floor.
```

## 6. APPLICATION EXAMPLES

- **Constellation/fleet telemetry (AN-002 lineage):** reject bus-common gain drift exactly; project sensor
  noise off the ~1.7-eff-dim health subspace; flag the rotation-blind size events. Integrity by receipt.
- **Space radio source layer (AN-003):** encode telemetry in ILR before the QAM modem — error-graceful
  delivery (≈700× at 12 dB, `f502c15d`) plus this denoiser; the modem is untouched.
- **Sensor-array conductor (AN-004):** each sensor is a part; common-mode environment cancels; the coherent
  cross-sensor signal survives; the gate withholds when the array disagrees.
- **Audio / BTL origin:** the original use — automatic common-mode noise cancellation by reciprocation; this
  AN is that design law generalized and receipted.

## 7. LIMITS — WHAT THIS WILL NOT DO (read before design-in)

- Will **not** cancel in-subspace random (white) noise — returns 0 dB and says so. Use averaging/coherence
  (statistical, **not** part of the deterministic engine) externally if needed.
- Will **not** exceed the Shannon limit, the rate-distortion bound, or claim "lossless at scale."
- Requires the input to be a genuine composition and (for Stage 2) a clean calibration reference + low
  effective dimension. No structure → no deterministic gain; the instrument reports this honestly.

## 8. TRACEABILITY

Receipts: common-mode `d8c21c70` · additive `cb0c3f52` · radio `f502c15d` · compression `305cc0db` ·
conformance master `d7ac6530`. Reproduce each via the cited `experiments/…` script. Determinism contract
HS-EPS-1; conformance HS-GOLD-1.

## 9. TIERS

**T1** §2–§3 measured behaviors + the denoise law. **T2** the application examples (architectures, reasoned).
**T3** statistical denoising — **suggested, not provided** (not deterministic); any hardware figure — to earn.

*Cross-refs: `HS-CN1_DATASHEET.md`, `../../experiments/deterministic_denoise_2026-06/`,
`../../experiments/ground_state_noise_cancel_2026-06/`, `../flagship/PURE_SIGNAL_EXTRACTION_FROM_THE_GROUND_STATE.md`,
`../frontier/HS_ENGINE_MORPHOLOGY_AND_CODEC.md`. Operator is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*
