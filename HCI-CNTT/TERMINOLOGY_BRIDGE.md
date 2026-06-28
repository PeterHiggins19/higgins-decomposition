# The terminology bridge — navigation + physics, always paired

*The standing rule, from 2026‑06‑14: **every Hˢ output names each quantity by BOTH its navigation/systems term and its physics term, with a plain‑language meaning.** This solves the translation problem at the source — a field expert, an operator, a physicist, and a mathematician each find the same idea by a handle they already use, and can carry the result to their peers in the right language. The engine's name already carries the first half (Compositional **Navigation** — Tensor Train); this pairs it with the mechanics half. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; math tiers live in `COMPOSITIONAL_MECHANICS.md`.*

---

## The rule

> Name it twice, mean it once. Write **"the helmsman (the steerer / the fastest‑moving part)"**, **"compositional momentum (the arrow of intent / mass × velocity)"**, **"the hold‑lock (station‑keeping / at rest below the noise floor)"**. Lead with whichever term fits the reader, but always carry both. Never make someone learn our dialect to understand their own data.

## The canonical pairings

| Quantity (the math) | Navigation / systems term | Physics term | Plain meaning |
|---|---|---|---|
| `r = clr(x)` | position / bearing‑state | position (on the manifold) | where the system sits in composition‑space |
| `Δr` | drift / drift‑rate | **velocity** | how fast the mix is changing |
| `Δ²r` | change‑of‑drift | **acceleration** | speeding up or slowing down |
| `Δ³r` | lurch | **jerk** | how abrupt the change is |
| `argmax‖Δr‖` | **helmsman** (the steerer) | the fastest coordinate | which part is steering the change |
| `mass·velocity` | **arrow of intent** | **momentum** | where the *weight* is moving |
| `dp/dt` | reshaping pressure | **force** | what is pushing the composition |
| `½Σ m v²` | activity level | **kinetic energy** | how energetic the motion is |
| `K_eff = exp(H)` | effective spread / diversity | entropy / effective degrees of freedom | concentrated vs spread out |
| `‖Δr‖` | leg / step distance | **speed × dt** (displacement of a step) | distance moved this step |
| `Σ‖Δr‖` | journey / track length | **arc / path length** | total distance travelled |
| `‖r(T)−r(0)‖` | net course made good | **displacement** | net change, start to end |
| `displacement/path‑length` | course directness / on‑track ratio | **path efficiency** | straight & purposeful (≈1) vs wandering (≈0) |
| `κ` | turn rate / course change | **curvature** | how sharply the path bends |
| momentum coherence | heading consistency | directional persistence | a real arrow vs churn |
| `∫ T dt` | transit effort / total cost | **action** | the trajectory's total effort |
| `‖r∧p‖` | circulation / swirl | **angular momentum** | carriers orbiting one another |
| hold‑lock | **station‑keeping / hold** | equilibrium / dead‑band at rest | holding steady; no real change to report |
| regime boundary | **waypoint** / regime change | **phase transition** / state change | when the system changed state |
| deceptive drift | silent drift | adiabatic (quiet) drift | concentrating without the expected motion |
| effective rank | degrees of freedom in play | effective dimensionality / normal modes | how many independent directions are moving |
| max derivative order `N*` | sensor resolution limit | **Nyquist / noise floor of the jet** | the deepest derivative still signal, not noise |
| lossless tiling | chart‑stitching / dead reckoning | exact reconstruction | rebuild the whole from overlapping pieces |
| SafeLoop | **autopilot / helm control** | bounded feedback control | acting on the system — only behind breakers |
| breakers + e‑stop | cut‑outs / emergency stop | circuit breakers / fail‑safes | the conditions that halt the loop |
| determinism hash | the receipt / log entry | reproducible state | same input → same output, provably |
| confidence gate | go / no‑go | significance threshold (σ) | act only when the evidence clears the bar |

## Why pair them (the translation solved)

- A **navigator, pilot, plant operator, or engineer** reads *helmsman, drift, waypoint, station‑keeping, autopilot, course made good* and immediately has a mental model — these are working words.
- A **physicist, chemist, or mathematician** reads *velocity, momentum, force, curvature, action, phase transition* and maps it to mechanics they already command.
- A **domain expert with no quantitative background** reads the plain‑meaning column and is never blocked.
- Crucially, each can then **carry the finding to their own peers in the right register** — the geologist says "regime boundary / phase transition," the energy analyst says "the arrow of intent is moving to wind," the reviewer hears "momentum = mass × velocity, deterministic." One result, three correct vocabularies, no translation lost.

## How it's used from here

1. **Every reading is named twice** in docs, the onramp, results, and conversation — navigation term + physics term, plus plain meaning on first use.
2. The onramp (`onramp/PHD_ONRAMP_PROTOCOL.md`) leads with the reader's register and offers the others.
3. This table is the canonical source; the glossary and the designer spec point here.
4. Honesty unchanged: the physics terms are an honest communication bridge — the *mechanics framework* on the Aitchison manifold is Tier 2 (sound), the *computed values* Tier 1; nothing in the dual naming inflates a claim.

*Name it for the navigator and for the physicist, and the field expert who is neither still understands — which is the whole point: the instrument speaks every reader's language at once.*
