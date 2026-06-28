# The full-featured Hˢ engine — specification (v5, the integration)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The full
package, fully specified: **the determinism math engine first, every compute channel built around it, probing
from the ceiling down and down as far as the data will support — non-invasively.** This is the integration
layer that composes the session's receipted components into one pipeline. Reference orchestrator:
`hs_full_engine.py` (engine receipt `cebfe37a06831c9f`). Honest-broker tiered; Peter is the sole gate;
nothing posted.*

---

## The shape (determinism first, everything else a support channel)

```
                 ┌───────────────────────────────────────────────┐
   data  ───────▶│  CORE · determinism math (FIRST)              │
   (a moving     │  closure → clr → ILR → eff-dim → helmsman → ⊞ │   ⊞ = SHA-256 receipt
    composition) └───────────────────────────────────────────────┘
                          │ the exact read is the spine; all else hangs off it
        ┌─────────────────┼───────────────────────────────────────────┐
        ▼                 ▼                 ▼                          ▼
  CH-INERT          CH-PROBE           CH-TRIAD                   CH-SUPPORT
  non-invasive      ceiling-down       cross-verify               guards · 3ⁿ confidence
  differential      probe ladder       (Q/Hs/DUT)                 · staged-use tier
        └─────────────────┴───────── MASTER RECEIPT ──────────────────┘
                                   (one read, one hash)
```

**The ordering is the doctrine.** The determinism math is computed *first and alone*; it is exact and it is
the thing every other channel cross-checks against. Nothing in the support channels can promote a result the
core did not produce — the channels *add coverage and certification*, never new claims.

## CORE — the determinism math engine (T1)

The exact compositional read: `closure → clr → ILR (Helmert) → effective dimension → helmsman
(argmax|Δclr|) → SHA-256 content receipt`. Same input, same output, same receipt, on any machine. This is the
canonical Hˢ-Kinematics pipeline; here it is the first stage and the source of truth for the rest.

## CH-INERT — non-invasive active probing (T1)

The read is **inert: it imprints nothing.** The engine confirms this every run with a round-trip
(`closure → clr → clr⁻¹`); the residual returns to the numerical floor (measured `5.6×10⁻¹⁷`), proving the
measurement does not alter the data. A *localized* large residual is then meaningful — it is a real feature
(the knock-and-read differential of the P2 seed), not damage. This is the X-ray/non-contact doctrine made
operational: **active probing, zero imprint.**

## CH-PROBE — the ceiling-down probe ladder (T2)

"Know the knowable" with a hard edge. The engine probes **from the coarsest grouping down and down** —
`L = 2, 4, 8, …` — reading the composition at each grain and reporting **what each level adds** (the
information gain in effective dimension, and any new helmsman that emerges). It descends **only as far as the
finest grain the data and compute *jointly* support** — the max-power frontier
`D_max = min(D_stat ≈ N/βw, D_comp ≈ C/κw)` — and **stops there.** Past the floor the read would be
manufactured, not known, so the engine refuses to go finer. Component-web density `w` sets the grain;
data-vs-compute sets which ceiling binds (`library/max_power_hs.py`).

## CH-TRIAD — cross-verify (T1 where applicable)

When the read carries a coherence observable, the engine co-computes it three independent ways — **Q-algebra,
DUT native physics (ODE), Hˢ geometry** — and certifies only on coherence (`TRIAD-CON`), isolating the
outlier route otherwise (`triad-backbone/`). Three different maths agreeing is the strong certificate.

## CH-SUPPORT — guards, confidence, staged tier (mixed)

The honest envelope: the **all-zero/constant-carrier guard** (E-21), the **effective-rank coherence gate**
(refuse to read when there is no shared structure), the **3ⁿ confidence** rung (opinion → agreement →
validation-and-locate), and the **staged-use tier** the read qualifies for (§ below). A guard trip/hold
blocks promotion — the engine withholds rather than guess.

## The staged-use ladder (which tier a read earns)

`0 blocked (a guard held)` → `1 basic (read)` → `4 verified (receipted, non-invasive)` →
`5 triad-certified (coherence across maths)` → `6 frame-locked transmission (encoding+integrity)` →
`7 keyed-secure (only with a real cipher)`. The engine reports the highest tier a read *earns*, never one it
does not (the P3 seed; confidentiality is fenced — Hˢ is not a cipher).

## Measured — the engine running end-to-end (receipt `cebfe37a06831c9f`)

A hierarchically-structured `D=16` composition, 200 samples, run two ways:

| run | CORE eff-dim | INERT | PROBE | TRIAD | tier |
|---|---|---|---|---|---|
| **ample budget + coherence** | 12.72 | 5.6×10⁻¹⁷ (non-invasive) | descends to native `L=16` (compute-bound, room to spare) | `TRIAD-CON` certified | **5 · triad-certified** |
| **tight budget** | 12.72 | 5.6×10⁻¹⁷ (non-invasive) | **stops at `L=8` — the data floor** (`D_max=8 < D=16`, statistics-bound) | channel idle (no observable) | **4 · verified** |

The two runs show the whole point: the same exact core, and the engine **descending as far as the evidence
allows and no further** — full native resolution when the budget supports it, an honest early stop at the
data floor when it does not. The probe ladder's per-level information gain (1.5 → 3.2 → 6.4 …) is the "down
and down and down" made visible and bounded.

## Governance (the fixed point)

Every component steers the read (closure: no inert part; the helmsman rotates) — that is honored by design
(`huf-gov/COMPONENT_REQUEST_ESCALATION_DOCTRINE.md` §6). The **one fixed point** is the operator's last
breaker: the engine certifies, withholds, and reports tiers, but **the human holds the gate**. Full
automation is never reached; coherence is offered, never imposed.

## Honest tiers

- **T1 (built + receipted):** the CORE read, CH-INERT non-invasiveness, CH-TRIAD certification, the guards.
- **T2 (specified + reference-orchestrated):** the single-pipeline PACKAGE and the CH-PROBE depth law (the
  scaling forms are standard; the constants are illustrative). This orchestrator is the *integration layer*;
  the canonical production core remains the Hˢ-Kinematics engine.
- **T3 (to earn):** the differential engine (CH-INERT's localized-residual feature read) on real hardware;
  CH-PROBE depth law calibrated on a real field; tiers 6–7 of the staged ladder.

## Run / extend

`python3 hs_full_engine.py` → the two demo runs + the master receipt. To read your own field: pass a
`samples × D` array, your `(N, C, w)` budget, and an optional `Q` for the coherence channel. Add a channel by
writing a function that consumes the CORE read and returns a receipted verdict — never one that promotes a
claim the core did not make.

*Cross-refs: `hs_full_engine.py`, `HS_FULL_ENGINE_RESULTS.json`, `../triad-backbone/THE_TRIAD_BACKBONE.md`,
`../library/max_power_hs.py`, `../library/KNOW_THE_KNOWABLE.md`, `../library/THE_BLINDNESS_SUITE.md`,
`../papers/UNWRITTEN_CONNECTIONS_SEEDS.md` (P2/P3), `../huf-gov/COMPONENT_REQUEST_ESCALATION_DOCTRINE.md`.
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — determinism first · channels add coverage not claims · the probe stops at the supported floor · tiers earned not asserted · the human holds the gate.*
