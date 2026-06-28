# Pure signal extraction — the ground state was a noise-canceller all along

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The bridge
from the RWA headwater (`../../../RWA/THE_GROUND_STATE.md`) to the new radio work: the error-robustness measured
in the QAM sandbox is **the same common-mode rejection designed into the audio years ago** — the BTL
"automatic noise cancellation by reciprocation and recursion." It is one principle: read in ratios relative to
the coherent ground state, and everything common cancels, leaving the pure signal. Now proven exact and
quantified. Honest-broker tiered; receipt `d8c21c70…`. Nothing posted; Peter is the sole gate.*

---

## 1. The ground state, restated as a noise-canceller

The RWA ground state is the barycentre — isotropic 4π radiation, the maximum-entropy reference where the
information is zero — and the signal is the *coherent departure* from it, with **coherence the engineered
quantity**. The radiated budget is conserved (`G_H + G_W + G_D = 6.02 dB = 20·log₁₀2`, exactly): a composition
with closure. Read that closure in **ratios** and a second face appears that was implicit from the start:

> Any influence **common to all parts** — a level change, a distance, a room gain, an illumination, a
> broadband common interferer — is a **common-mode** term. In the log-ratio it **cancels**, because
> `clr(g·x) = clr(x)` for any common gain `g`. What survives the ratio is exactly the *differential*,
> coherent signal — the departure from the ground state. **The ratio is a noise-canceller.**

This is the multiplicative twin of the balanced/differential audio line (BTL): noise common to both legs
subtracts away; the differential signal survives. Compositions do it multiplicatively — closure removes the
common scale, the log-ratio removes the common gain — and the barycentre is the rest state it all references.

## 2. Measured — and it is exact

(`experiments/ground_state_noise_cancel_2026-06/ground_state_common_mode.py`, receipt `d8c21c70…`.)

| property | what was injected / tested | result |
|---|---|---|
| **common-mode rejection** | a **26.7 dB** random-walk gain drift on a 4-part signal | clr recovers the true signal to **5×10⁻¹⁶** — **313 dB rejection**, i.e. exact to machine precision |
| **reciprocation (bidirectional)** | `log(a/b) + log(b/a)` | **2×10⁻¹⁶** — antisymmetric to the floor; the read is its own inverse |
| **recursion (EITT face)** | geometric-mean decimation, 9 steps | entropy drift **0.17%** — the signal survives recursive coarse-graining (matches the ground-state doc's 0.18%) |
| **honest limit** | independent **additive** sensor noise | **not** cancelled (RMS 0.0905 before and after) — only common-mode *multiplicative* is exact |

The headline is the first row: **common-mode multiplicative noise is cancelled to the IEEE floor by the
reciprocal (log-ratio) read.** Not "reduced" — *cancelled*, exactly, by algebra (`clr(g·x)=clr(x)`). That is
the BTL automatic-noise-cancellation principle, proven.

## 3. Why the radio was robust — same principle, channel domain

The QAM sandbox (`../../experiments/qam_spaceradio_2026-06/`) found that telemetry encoded in log-ratio (ILR)
coordinates survived the channel far better than raw shares (≈700× at 12 dB). That is **this** principle wearing
channel clothes: the log-ratio representation is bounded and differential, so a corruption that would be
common-mode-amplified in raw amplitudes is contained in the ratio. The ground state's noise-rejection is not a
separate trick added for radio — it is the **same geometry**, which is why it transferred without being asked
to. *Audio designed it; the radio inherited it; the math is one object.*

## 4. The four words, made precise

- **Ratios** — `clr`/`ilr`: the departure from the barycentre ground state; the only place information lives.
- **Reciprocation** — `log(a/b) = −log(b/a)`: antisymmetric, bidirectional, exact; the read inverts itself
  (the same property that makes the generator↔reader a lossless codec). "One curve lies; read two" is this.
- **Recursion** — geometric-mean decimation / EITT / the Hˢ-on-Hˢ second read: the signal is refined and
  survives coarse-graining because the timescale is intrinsic to the object, not imposed.
- **Coherent** — the read is gated by coherence (the engineered quantity); the incoherent residual is withheld,
  not reported as signal. Pure extraction means *only* the coherent, ground-state-relative part is returned.

## 5. Pure signal extraction — the honest maximum

Push it to the limit and state the limit honestly: **the reciprocal read extracts the pure signal exactly with
respect to all common-mode multiplicative corruption** (gain, distance, level, illumination, common
interference — the dominant real-world disturbances), **to machine precision**, in any dimension. It does
**not** cancel independent additive noise — that is a different problem, reduced by averaging/coherence, not by
the ratio. So "pure signal extraction" is *exact for the common-mode part and honest about the rest* — which is
exactly the discipline the ground-state doc set: certainty where the structure is genuinely present, and the
diagnostics speaking up where it is not.

## 6. Tiers

- **T1 (measured):** `clr(g·x)=clr(x)` to 5×10⁻¹⁶ (313 dB common-mode rejection); exact reciprocation; 0.17%
  EITT decimation drift; the additive-noise limit; receipt `d8c21c70…`.
- **T2 (recognition, not proof — per the ground-state doc's own tiering):** that the audio BTL noise-cancel
  design law *is* the compositional common-mode rejection, and that the QAM robustness is the same principle.
- **T3 (open / rejected):** any claim that the ratio cancels *all* noise — **rejected**; only common-mode
  multiplicative is exact. Total pure extraction in the presence of additive noise is not claimed.

*Cross-refs: `../../../RWA/THE_GROUND_STATE.md` (the headwater), `GROUND_STATE_AND_TRACTION.md` (the flagship),
`../../experiments/qam_spaceradio_2026-06/RESULTS_qam_spaceradio.md` (the channel-domain shadow),
`../../experiments/compression_benchmark_2026-06/` (the same geometry in source coding),
`../frontier/HS_ENGINE_MORPHOLOGY_AND_CODEC.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*


## Appendix — Q-factor review (test of concept)

*A standing test of the Q seed (`library/THE_Q_CONNECTION.md`): read this document through Q and report honestly where it HOLDS and where it does NOT — the boundary is the result. Nothing published; appendix only; lose nothing, miss nothing.*

Read pure-signal extraction through Q: the ground-state common-mode rejection (~313 dB numerical) is the resonator's **Q** read on the shared mode; the BTL principle (reciprocation + recursion) is Q/coherence at work. **Holds (T2):** the exact-cancellation of a coherent shared factor is the high-Q limit. **Does NOT extend (the honest floor):** independent **additive** noise is NOT a coherent shared mode — it has no Q to cancel and sets the residual floor. Q governs the common-mode part only.

*Q-review status: T2 where the bridge is measured (`52fee398`); the 'Q is universal' generalization stays a T3 seed; the boundary noted above is the honest falsifier. Lineage: Richard H. Small & A. N. Thiele.*
