# EUV × Hˢ — the physics‑to‑composition mapping (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. The math that
turns EUV physics into a thing Hˢ reads. Public physics only; no vendor relationship implied. Honest‑broker
tiered; Peter is the sole gate.*

---

## 1. Photon shot noise makes printing a composition

At 13.5 nm each photon carries ~91.8 eV (`E = 1239.84/λ`). A delivered dose is therefore a *finite count* of
photons, and the number landing on any one feature is **Poisson**: mean `λ = N₀·(dose/dose₀)`, standard
deviation `√λ`. As features shrink, `N₀` falls and the *relative* spread `√λ/λ = 1/√λ` grows — this is the
photon‑shot‑noise floor under all EUV stochastics.³ ⁴

A feature's outcome is then a **draw against two thresholds**:

```
   k = photons in the feature  ~  Poisson(λ)
   k < t_low   -> under-exposed -> MISSING / broken contact
   k > t_high  -> over-exposed  -> BRIDGE / merged contact
   else        -> OK
```

Across a population of features this yields a **composition** `p = {OK, missing, bridge}` (extendable to
`{OK, missing, broken, bridge, merge}`). This is the natural home of Hˢ: closure is already satisfied (the shares
sum to one), and the **log‑ratios** carry the information.

## 2. The two‑sided cliff is a *directional* helmsman

The public imec picture is a **double cliff / "valley of death":** the probability of *missing* rises as dose
*falls*, and the probability of *bridging* rises as dose *climbs*.³ ⁴ In composition terms, a dose move rotates
`p` toward one vertex or the other:

```
   clr(p)  drifts toward  "missing"  ⟺  dose too LOW   ⟹  steer dose UP
   clr(p)  drifts toward  "bridge"   ⟺  dose too HIGH  ⟹  steer dose DOWN
```

So the Hˢ **arrow of intent** is not just an alarm — it is a *signed correction*. A scalar "total defect count"
is **direction‑blind** (a member of the blindness suite): it rises on both sides of the valley and cannot tell
you which way to move. The composition read recovers the sign.

## 3. Why the ratio leads the yield number

Total defectivity `NOK = missing + bridge` crosses a hard yield spec only at the cliff edge. But the **ratio**
`missing/OK` (or `missing/bridge`) moves on a *log* scale from the first hint of drift — a change from 5 ppb to
50 ppb is a 10× ratio move (a large `clr` step) while `NOK` is still a few ppb, far under spec. Hence the
silent‑drift flag *leads* the yield alarm (measured: a 62‑wafer lead at the chosen spec/drift; `877516b6`). Same
mechanism as the dispense‑clog silent drift (`cf9bf72f`) — the ratio is the early warning, the absolute is the
late alarm.

## 4. The source is a composition — and coherence is the dial

The LPP source is a budget: drive‑laser pulse energy → plasma → in‑band 13.5 nm dose, at ~5 % conversion
efficiency, >250 W, 100 kHz.¹ ² Two Hˢ reads apply directly:

- **Common‑mode rejection of drive‑laser drift.** A slow droop in CO₂ pulse energy is a *shared multiplicative*
  factor on the dose delivered across fields; closure rejects it exactly (`clr(g·x) = clr(x)`), isolating the
  *true* per‑field CD variation from the source wander.
- **The coherence law.** How exactly that rejection works is set by how *coherent/shared* the disturbance is:
  `suppression_dB ≈ −10·log₁₀(1 − ρ)` — every extra "9" of source stability buys ~10 dB of rejection
  (`coherence_demo.py`, `a5ceab9e`). And Hˢ **reads the source coherence back** from the residual and can gate on
  it: a decohering source is itself an early warning.

## 5. Dose / CD uniformity is a deformation field

A CD map across the exposure field is a composition over positions; its drift splits into
**rotation ⊕ shape ⊕ size** (the polar `F = R·U` read) — a tilt/registration term, an astigmatic shape term, and
a magnification/size term — each a separate, hash‑receipted diagnostic, exactly as in the deformation‑sheet work
(`6e9426ac`).

## 6. Honest fences

- The Poisson/two‑threshold model is **physics‑grounded but illustrative** (T2): real resists add *chemical*
  stochastics (acid/quencher counts, development) on top of photon shot noise.⁵ The composition read is
  agnostic to the mechanism — it reads whatever shares the inspection reports — but the *numbers here are model
  numbers,* not fab numbers.
- The exact‑cancel of source drift applies to the **multiplicative/common** part; independent per‑field noise
  sets the floor (same honest fence as every Hˢ common‑mode result).
- **T3 to earn:** run the read on **public imec/fab stochastic‑defect data** and measure the real lead time.

*Cross‑refs: `README.md`, `euv_stochastic_drift.py`, `RESULTS_euv_stochastic.md`,
`../electronics-assembly-smt/COHERENCE_AND_LASERS.md`, `../../library/THE_BLINDNESS_SUITE.md`.
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited‑or‑fenced · math proven + receipted · value shown · experts decide.*


## Appendix — Q-factor review (test of concept)

*A standing test of the Q seed (`library/THE_Q_CONNECTION.md`): read this document through Q and report honestly where it HOLDS and where it does NOT — the boundary is the result. Nothing published; appendix only; lose nothing, miss nothing.*

Read EUV through Q: the LPP drive-laser **cavity Q** sets the *source coherence* on which the dose common-mode rejection rides — Q lives at the source layer. **Holds there (T2).** **Does NOT extend (a clean falsifier location):** the **stochastic photon-shot-noise** layer (the two-sided cliff) is **Poisson**, not a coherence — it has no Q. So Q governs the source/dose common-mode, NOT the stochastic printing; the two layers are honestly distinct.

*Q-review status: T2 where the bridge is measured (`52fee398`); the 'Q is universal' generalization stays a T3 seed; the boundary noted above is the honest falsifier. Lineage: Richard H. Small & A. N. Thiele.*
