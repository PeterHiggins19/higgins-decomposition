# The triad backbone — one observable, three maths, coherence is the claim

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25.
The engine backbone: **Q-math, Hs-math, and DUT-math are co-computed simultaneously**, each taking a
**different mathematical route to the same observable, and the three must cohere.** The claim is
certified by their agreement — coherence across independent maths *is* the support. Measured demonstrator
with receipt `f8ee9f6fce466c0f`. Honest-broker tiered; Peter is the sole gate; nothing posted.*

---

## The one sentence

> A result earns trust not because one method computed it, but because **three different mathematical
> systems, taking three different routes, arrive at the same number.** The engine computes all three at
> once; their coherence is the certificate.

## Why three *different maths*, not three readers

The triple-channel reader already runs three readers (tiling · Clifford · matrix) over **one**
composition and votes 2-of-3. The triad backbone is a level above that: the three channels are **different
mathematical systems entirely** — the coherence algebra of Q, the Aitchison geometry of Hˢ, and the
device's own native physics (its differential equation). Three readers of one math catch a coding bug.
Three *maths* agreeing catch something deeper: that the model, the geometry, and the physics are telling
the same story. That is a stronger certificate, and it is the 3ⁿ confidence ladder's n=1 made literal —
three independent perspectives, and (because there are three) the **outlier can be located, not merely
detected.**

## The shared observable

The demonstrator's observable is the resonator's **per-cycle energy-retention coherence**

```
    rho = E(t+T) / E(t) = exp(-2*pi / Q)        (one "9" of coherence  ~  10 dB of rejection)
```

— the same `rho` that drives the coherence law `suppression_dB = -10*log10(1-rho)` (`a5ceab9e`) and the
Q bridge (`52fee398`). One number; three routes to it.

## The three routes (each through its own math system)

| route | math system | how it computes `rho` | independent of |
|---|---|---|---|
| **Q** | coherence algebra / Thiele-Small | `rho = exp(-2*pi/Q)`, with `Q` from the node law `1/Qts = sum 1/Q_i` | the ODE; the geometry |
| **DUT** | the device's native physics | integrate `x'' + (omega0/Q) x' + omega0^2 x = 0` (RK4 ring-down); measure the energy ratio over one period — **never uses the exp formula** | the algebra; the geometry |
| **Hs** | Aitchison / compositional geometry | read the per-cycle `{retained, dissipated}` energy as a 2-part composition; the clr balance is `log(rho/(1-rho))`; recover `rho` as the mean retained share | the ODE; the exp formula |

Each route could be wrong on its own and the others would not follow. That is what makes their agreement
meaningful.

## The verdict — how the backbone "supports the claim"

The engine compares the three and issues one of three codes (mirroring the channel reader):

| code | condition | meaning |
|---|---|---|
| **TRIAD-CON** | all three agree within tolerance | **claim SUPPORTED** — model, geometry, and physics cohere |
| **TRIAD-ISO** | one route is the outlier | isolate + warn — *and the disagreeing math is named* |
| **TRIAD-HLT** | no two agree | halt + report — the device, the model, or the math is wrong |

The claim is **not** asserted by any single route; it is *earned* only at TRIAD-CON. This is the backbone's
whole purpose: it refuses to certify a number that the three maths do not jointly confirm.

## Measured (receipt `f8ee9f6fce466c0f`)

A resonator with `Qts = 5.714` built from two nodes (`Qes = 8`, `Qms = 20`; the Thiele-Small node law),
`f0 = 55 Hz`:

| case | device | rho_Q | rho_DUT | rho_Hs | max pairwise diff | verdict |
|---|---|---|---|---|---|---|
| **A** | consistent resonant device | 0.33302 | 0.33163 | 0.33301 | 1.4×10⁻³ | **TRIAD-CON** (claim supported) |
| **B** | high-Q resonator (Q=12) | 0.59238 | 0.59212 | 0.59238 | 2.7×10⁻⁴ | **TRIAD-CON** (claim supported) |
| **C** | nameplate Q wrong (spec 11, real 12) | 0.56485 | 0.59212 | 0.59238 | 2.8×10⁻² | **TRIAD-ISO** → outlier **Q** located |

Cases A and B: the three maths cohere to ~10⁻³–10⁻⁴, so the coherence claim is certified. Case C: a wrong
**nameplate Q** makes the Q-route disagree while the DUT (physics) and Hˢ (geometry) still agree with each
other — the backbone flags TRIAD-ISO and **names the Q route as the outlier.** The physics and the geometry
witnessed the truth; the bad spec was caught. That is the backbone doing its job.

## What this requires of the engine (the standing spec)

1. **Co-compute, don't post-hoc check.** The three routes run together on every certified observable, not
   as an afterthought — the backbone is the computation, not a downstream audit.
2. **Routes must stay genuinely independent.** If two routes share a sub-calculation they stop being
   witnesses; keep the math systems separate (algebra ⟂ physics ⟂ geometry).
3. **Certify only at CON; locate at ISO; halt at HLT.** No observable is reported as supported unless the
   triad cohered.
4. **Receipt the triad.** The three values, the diffs, and the verdict are hashed together so any node can
   recompute and confirm.

## Honest fences

- **T1 (mechanism):** the three math routes are exact/standard, and the demonstrator is a canonical damped
  oscillator integrated to numerical agreement. The CON/ISO/HLT logic is deterministic and receipted.
- **T2 (reasoned):** that *every* Hˢ observable admits three independent routes. Coherence (Q) has a clean
  triad because it is shared by algebra, physics, and geometry; other observables must each be shown to
  have three genuinely independent routes — that is the work to extend this backbone across the engine.
- **The tolerance is a choice.** `tol` is set by the required confidence and the noise floor; it should be
  derived per application, not fixed globally.
- **Not a claim that three agreeing maths cannot all be wrong together** (a shared hidden assumption could
  fool all three) — only that independent agreement is far stronger evidence than a single route. The
  honest boundary is part of the result.

*Cross-refs: `triad_backbone.py`, `TRIAD_BACKBONE_RESULTS.json`,
`../library/THE_Q_CONNECTION.md`, `../industrial-instruments/electronics-assembly-smt/COHERENCE_AND_LASERS.md`,
`../ARC_OF_DISCOVERY.md` (step 8 the 3ⁿ index, step 9 the triple channel), `../library/THE_BLINDNESS_SUITE.md`.
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — three independent maths · coherence certifies · the outlier is located · the shared-assumption boundary is named · experts decide.*
