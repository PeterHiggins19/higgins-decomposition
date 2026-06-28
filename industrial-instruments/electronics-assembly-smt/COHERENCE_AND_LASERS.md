# Coherence and lasers — the same word, twice, for a reason (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. Why a laser
source and the Hˢ instrument fit so naturally: **coherence is exactly the resource Hˢ converts into rejection.**
Reach‑for‑the‑stars framing, honest‑broker tiered, receipted. **No vendor relationship implied.** Nothing
posted; Peter is the sole gate.*

---

> **The origin of this law is Q.** A resonator's coherence *is* its **Quality Factor** — `ρ = exp(−2π/Q)` per
> cycle — so the law below is the loudspeaker's Q (Thiele‑Small; Richard H. Small) read on any system. The
> coherence dial was called Q long before it was called ρ. See [`../../library/THE_Q_CONNECTION.md`](../../library/THE_Q_CONNECTION.md).

## The one sentence

> **Hˢ's common‑mode rejection is exactly as strong as the source is coherent.** A coherent laser makes the
> laser/thermal/connector disturbance a *true common mode* — the same on every channel — and closure+log‑ratio
> removes a true common mode exactly. Lose coherence and the disturbance decorrelates into per‑channel noise;
> now there is nothing "common" left to reject. So lasers and coherence go together — and coherence and Hˢ go
> together — because they are the *same property* read two ways.

## The law (measured, and it has a closed form)

Let **ρ ∈ [0,1]** be the *coherent fraction* of the disturbance — how much of the laser/thermal drift is shared
across channels versus decohered into independent per‑channel noise (a proxy for laser temporal/spatial
coherence and inter‑channel phase correlation). Closure+clr removes the shared part exactly, so the residual is
just the independent part:

```
    suppression_dB  ≈  −10 · log10(1 − ρ)
```

**Every extra "9" of coherence buys ~10 dB of rejection.** Measured (`coherence_demo.py`, receipt `a5ceab9e`):

| coherence ρ | Hˢ suppression (measured) | −10·log10(1−ρ) | Hˢ read‑back coherence |
|---|---|---|---|
| 0.0   | 0.6 dB    | 0 dB    | 0.13 |
| 0.5   | 3.6 dB    | 3 dB    | 0.56 |
| 0.9   | 10.6 dB   | 10 dB   | 0.91 |
| 0.99  | 20.5 dB   | 20 dB   | 0.99 |
| 0.999 | 30.6 dB   | 30 dB   | 0.999 |
| 0.9999| 40.7 dB   | 40 dB   | 0.9999 |
| 1.0   | 289 dB (numerical floor) | ∞ | 1.0 |

The measured curve tracks the closed form to a few tenths of a dB across four decades, and at perfect coherence
the rejection runs to the numerical floor — the same exact‑cancellation that gives the RWA ground‑state and the
fiber demo their hundreds of dB. *Coherence is the dial; rejection is the readout.*

## Three locks (why it's not a coincidence)

**1. Coherence is what makes the common mode *common*.** Closure rejects `clr(g·x) = clr(x)` only when `g` is the
*same* factor on every channel. A coherent source guarantees exactly that — one shared phase/intensity reference
imprinted identically on all channels. Decoherence breaks the "identical," and only the still‑shared fraction
cancels. The physics of the laser and the algebra of closure are describing the same condition.

**2. Hˢ can *read the coherence back* — and gate on it.** The residual after the read tells Hˢ what fraction was
truly shared: `coherence ≈ 1 − resid_var/total_var` (the table's last column recovers ρ to 3–4 places). So Hˢ
doesn't just *use* coherence, it *measures* it, and the **coherence gate** refuses to trust the relational read
when the read‑back coherence is too low — the honest‑broker "refuse to guess when there is no shared structure"
made into an optical‑coherence test. This is the Hˢ coherence reading and optical coherence turning out to be
the same measurement.

**3. Coherence also *adds dimensions* — the other half of the value.** Coherent optical detection recovers
**amplitude and phase** (and both polarizations) instead of intensity alone — more real dimensions per
wavelength, exactly the D‑grows‑the‑message object (`bf24c615`). Direct (incoherent) detection throws the phase
away — it is *phase‑blind*, a member of the blindness suite. So coherence buys Hˢ **both** exact rejection
(common‑mode) **and** capacity (dimension). A coherent laser is the ideal partner on both counts.

## What it means for the future projects

- **Fiber sensing skin (F1):** specify a coherent source and the disturbance becomes a true common mode → the
  310 dB‑class rejection of `fiber_hs_demo.py` is *available*, and Hˢ reports the live coherence as a health
  metric (a decohering source is itself an early warning).
- **Coherent fiber links (F2):** read amplitude+phase as the composition; capacity grows with the mode/quadrature
  count; common‑mode‑robust by construction.
- **Active alignment (F3):** interferometric/coherent feedback is the highest‑coherence signal on the line — the
  arrow it gives the aligner is the cleanest read Hˢ can make.

## Honest scope

- **T1 (measured):** the coherence→rejection law and read‑back (`a5ceab9e`); the fiber common‑mode demo
  (`e791ec63`); the ground‑state anchor (`d8c21c70`).
- **T2 (reasoned):** ρ as a proxy for real laser temporal/spatial coherence; the gate threshold — to calibrate on
  real interferometric data.
- **T3 (to earn):** run the coherence read on real coherent‑fiber data (e.g. a PubDAS coherent‑detection
  segment); report the measured coherence→rejection curve from a cited public file. No vendor relationship; none
  implied.

*Cross‑refs: `FUTURE_PROJECTS_FIBER_AND_Hs.md`, `coherence_demo.py`, `fiber_hs_demo.py`,
`../../papers/flagship/PURE_SIGNAL_EXTRACTION_FROM_THE_GROUND_STATE.md`, `../../library/THE_BLINDNESS_SUITE.md`,
`../../library/THE_DATA_IS_THE_CARRIER.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited‑or‑fenced · math proven + receipted · value shown · experts decide.*


## Appendix — Q-factor review (test of concept)

*A standing test of the Q seed (`library/THE_Q_CONNECTION.md`): read this document through Q and report honestly where it HOLDS and where it does NOT — the boundary is the result. Nothing published; appendix only; lose nothing, miss nothing.*

This document **is** the Q review: coherence is Quality Factor by another name, `rho=exp(-2pi/Q)`, and the law `suppression ~ -10*log10(1-rho)` is the loudspeaker's Q read on a laser/fiber. **Holds cleanly (T2, receipted `52fee398`/`a5ceab9e`):** Q -> coherence -> rejection. **Only fence:** that this coherence is *the same one* Hs reads in every non-optical domain remains a T3 seed.

*Q-review status: T2 where the bridge is measured (`52fee398`); the 'Q is universal' generalization stays a T3 seed; the boundary noted above is the honest falsifier. Lineage: Richard H. Small & A. N. Thiele.*
