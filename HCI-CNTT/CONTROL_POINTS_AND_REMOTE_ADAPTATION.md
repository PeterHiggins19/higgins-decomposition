# CN‑TT v4 — Engine Control Points & Remote Adaptation Map

*Design note, 2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Companion to `ai-refresh/CNTT_V4_ENGINE_DESIGN.md`, `ai-refresh/ENGINE_INTEROP_REGISTRY.md`, and `collaborations/geology-wehner/CNTT_FLIGHT_CONTROL_SPEC.md` (GPCC + Coherence Supervisor). Identifies WHERE on the engine adaptation may occur "if necessary" for the unexpected — the engine's contingency‑response surface.*

---

## 0 · Division of labor and the principle

**Matthew supplies the geo codes** — the domain content: what a given adaptation should respond to (a saturated channel, a new diagnostic element, a calibration drift, a facies/regime change). **This document supplies the engine's control surface** — the bounded set of places adaptation is *permitted*, and the rules that keep every adaptation deterministic and auditable.

Every control point obeys the same five rules (the GPCC contract):
1. **Whitelisted & bounded** — only the listed primitives, only within declared ranges; no arbitrary code, no opaque self‑modification.
2. **Reversible** — `FREEZE`/`ROLLBACK` to last‑known‑good is always available.
3. **Hash‑stamped** — every adaptation increments a config version and emits a new config + content hash, registered in the interop registry (§4).
4. **Determinism‑preserving** — same input + same config → same output, bit‑for‑bit. Adaptation changes the config, never the determinism.
5. **Logged** — every adaptation is an explicit, dated, signed entry; the Coherence Supervisor can veto or roll back.

## 1 · The locked core (what may NOT be adapted)
- **Engine code** (`geometry.py`, `quaternion.py`, `atlas.py`, `provenance.py`) — frozen per release; changing it is a *version update*, not an in‑flight adaptation.
- **The exact geometry math** (L2: closure, CLR, Helmert‑ILR, the D=4 quaternion sandwich) — the source of determinism and parity; not a control point.
- **The hashing/provenance** — the receipt mechanism itself is immutable.
Adaptation lives entirely in **configuration within whitelists**, never in the math or the code.

## 2 · The control points (by Tensor‑Train link)

| CP | Link | What can adapt (the unexpected it answers) | GPCC primitive | Bounds / whitelist | Reversible | Safety class |
|----|------|---------------------------------------------|----------------|--------------------|:--:|:--:|
| **CP‑1** | L1 Ingest | Carrier set — add a newly‑relevant part; drop a dead/saturated sensor channel | `SELECT / ADD / DROP_CARRIER` | only from the available carrier list; ≥2 parts remain | yes | A (changes the composition) |
| **CP‑2** | L1 Treat | Zero‑treatment policy — detection‑limit fraction; structural vs rounded | `SET_ZERO_TREATMENT` | frac ∈ [0.5, 0.8]×DL; policy ∈ {drop, multiplicative} | yes | B |
| **CP‑3** | L2 Geometry | Basis selection among **pre‑registered orthonormal** bases / SBP orderings | `SET_BASIS` | registered orthonormal bases only (orthonormality enforced) | yes | A (mostly locked) |
| **CP‑4** | L3 Atlas | Atlas strategy & structure — sliding ↔ hierarchical; the tree/grouping (**Matthew's geo codes plug in here**) | `SET_ATLAS` | atlas must stay **connected** (losslessness condition); charts size 4 | yes | A |
| **CP‑5** | L3 Atlas | Chart focus — which charts get the full exact CNQ read (regions of interest) | `SELECT_CHARTS` | subset of the atlas; rest still reconstructed | yes | C |
| **CP‑6** | L4 Navigate | Fusion weights — calibration‑weighted multi‑sensor fusion (geosensing) | `SET_FUSION_WEIGHTS` | simplex weights, ≥0, Σ=1; from calibration windows | yes | B |
| **CP‑7** | L4 Navigate | Navigation thresholds — regime tripwire, activation guard, K_eff threshold, helmsman window | `SET_PARAM` | regime k·MAD/σ ∈ [1.5,3]; guard ρ ∈ [1e‑4,1e‑2]; K_eff thr ∈ [0.02,0.1]; window ∈ [4,16] | yes | B |
| **CP‑8** | L4 Navigate | Delta correction — a bounded in‑flight correction factor on a named quantity | `APPLY_DELTA` | per‑field, bounded magnitude; logged + reversible | yes | B |
| **CP‑9** | cross‑cutting | Freeze / revert to last‑known‑good | `FREEZE / ROLLBACK` | always available | n/a | safety |
| **CP‑10** | cross‑cutting | Config version stamp + hash on every adaptation | (automatic) | append‑only registry entry | n/a | provenance |

Safety classes: **A** = changes what is measured (highest scrutiny; Supervisor confirmation); **B** = changes how it is read (bounded); **C** = changes which detail is surfaced (low risk). Geometry (CP‑3) is held nearly locked on purpose — adaptation there is selection among certified bases only, never new math.

## 3 · The Coherence Supervisor over the control points
The engine‑monitoring‑engine (`CNTT_FLIGHT_CONTROL_SPEC.md`) watches the control surface: it bounds‑checks every requested adaptation, can **veto class‑A changes**, votes via redundancy (TMR) where available, and triggers `ROLLBACK` on incoherence. No control point self‑actuates without passing the Supervisor and emitting a logged, hashed config.

## 4 · Remote update + hash → ground receiver (why the hash matters more here)
In a remote/flight setting, an adaptation (or a full engine update) changes the config — and therefore the output's **config + content hash**. The hash is the ground receiver's proof of *what produced this data*:
1. The remote engine adapts at one or more control points → increments config version → emits the new **config hash + content hash** in the telemetry header.
2. The change registers in the **interop registry** (§ `ENGINE_INTEROP_REGISTRY.md`) as a new node with its certified transforms to the prior config.
3. The **ground receiver reads the hash, looks it up in the registry, and interprets the data in its own frame** — even though the remote engine has changed since launch. Lossless fields translate; any lossy‑up field is flagged `RE_RUN_FROM_SOURCE`, never faked.

So a remote engine can be updated or can adapt itself in flight, and the ground never loses the ability to read it correctly — the hash routes, the registry translates. This is the remote‑update case the interop registry was built for.

## 5 · The bonus: delta‑testing falls out for free
Because every control‑point change is a versioned, hash‑stamped config with a certified transform to its predecessor, the *same machinery* gives a **delta/regression test**: change one control point, hold the input fixed, and the registry transform **is** the measured delta between configs. You can therefore:
- characterize the effect of any single adaptation as a clean, reproducible delta;
- regression‑test an update by confirming the delta matches the certified transform (drift ⇒ a flagged divergence, exactly as in the parity harness);
- pre‑qualify a flight adaptation on the ground twin before uplinking it.

Adaptability and testability are the same capability viewed from two ends.

## 6 · How this gets built (next steps; not yet implemented)
- Add a `config` object to the engine payload (the active control‑point settings) + its own hash.
- Implement the whitelisted setters (CP‑1…CP‑8) as bounded, logged config mutations — no engine‑code path.
- Wire the Coherence Supervisor bounds‑checks + `FREEZE/ROLLBACK`.
- Populate the interop registry per config change (the parity harness certifies the transforms).
This is engine build phase P2/P3 work; the control surface above is the spec it implements.

## Claim tiers
- **Tier 1 (verified):** the engine is deterministic and self‑describing/hashed (basis for all of this); the parameters/bounds are taken from the harvested oracle + flight spec.
- **Tier 2 (sound engineering):** the control‑point map, the safety classes, the remote‑hash flow, the delta‑testing equivalence.
- **Tier 3 (to build):** the config object, the setters, the Supervisor wiring, the registry population; Matthew's geo codes that drive CP‑4 on real data.

*The control surface is bounded; the math is locked; the hash carries the receipt. The instrument reads. The expert decides.*
