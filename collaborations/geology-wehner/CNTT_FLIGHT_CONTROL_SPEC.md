# CN-TT Adaptive Flight Control Specification — the Geologist Protocol Control Code + the Coherence Supervisor

**A deterministic, expert-steerable, space-grade compositional engine.**
**Concept specification / forward look · 2026-06-09 · honest-broker, claim-tiered · working draft (publication at the author's gate).**

**Abstract.** This specifies an adaptive control + supervision layer over the Hs Tensor Train (**CN-TT**: data → CNT → CNQ → vector output) that lets a domain expert **reconfigure and correct the engine in flight** — on new discoveries, on detected data drift, or on detected method drift — **without breaking the determinism, boundedness, and auditability** that make Hs trustworthy. Two components: the **Geologist Protocol Control Code (GPCC)**, a bounded, declarative, hash-stamped instruction set; and the **Coherence Supervisor**, a master engine that monitors the ensemble of per-sensor CNT engines, votes redundant results, detects drift, and applies or escalates corrections. It maps directly onto NASA's core Flight System (cFS), triple-modular-redundancy practice, and NPR 7150.2.

**Keywords:** flight software, core Flight System, cFS, FDIR, triple modular redundancy, fault tolerance, deterministic computation, delta processing, telecommand, telemetry, CCSDS, parameter tables, reconfigurable, edge computing, compositional data analysis, CNT, CNQ, quaternion, geosensing, remote sensing, NASA, USGS, NPR 7150.2.

---

## 1 · Scope and the hard constraint
The request is in-flight adaptability: let the expert (or the system) **change the structure vector space, apply a delta-correction, or re-weight** when a new discovery, a mistake, or drift appears. The hard constraint is that Hs's value **is** its determinism and auditability. So the controlling rule of this spec:

> **Every adaptation is an explicit, versioned, hash-stamped configuration change — never hidden mutable state, never opaque self-modification.** Given the input stream and the command log, any output is exactly reproducible and any change is attributable and reversible.

This is also exactly what NASA flight-software assurance (NPR 7150.2) and the "no surprises" doctrine require.

## 2 · Design invariants (non-negotiable)
- **Determinism preserved.** Adaptation = swapping/parameterising a *config*, each a hash-stamped object; the kernels stay deterministic.
- **Bounded computation.** Fixed-size quaternion/CNT kernels; no unbounded loops/recursion (e.g. the subcomposition ladder iterates by `itertools.islice`, not full enumeration) — a flight requirement and already a standing Hs engine rule.
- **Auditable.** Every command + state transition is event-logged and hash-chained to the prior config (CN-TT already hash-chains each link).
- **Reversible.** "Safe mode" = roll back to the last-good hash-stamped config; rollback is verifiable because configs are content-addressed.
- **Claim tiers travel** with every adapted output (confirmed / experimental / corrected-by-delta).

## 3 · The Geologist Protocol Control Code (GPCC)
**Hs offers the basics that matter; the expert builds the geology on top.** The GPCC is **not** arbitrary uploaded code — that would void determinism and safety. It is a small, whitelisted, declarative set of **deterministic primitives** the expert sequences:

| Primitive | Effect (deterministic) | Use |
|---|---|---|
| `SELECT_CARRIERS` / `ADD_CARRIER` / `DROP_CARRIER` | redefine the composition (the structure vector space) | a new mineral phase is discovered → restructure |
| `SET_PARAM` | regime threshold, deceptive-drift guard, K_eff window | tune sensitivity to the section |
| `SET_FUSION_WEIGHTS` | per-sensor reliability weights | re-weight after calibration |
| `APPLY_DELTA` | a correction factor (offset/scale) with a recorded justification | correct a detected mistake or drift |
| `SET_ZERO_TREATMENT` | structural-drop vs multiplicative replacement | new zeros encountered |
| `FREEZE` / `UNFREEZE` / `ROLLBACK` | lock state, or revert to a prior hash-stamped config | safe-mode / audit |

**Matthew develops the geological decision logic** — *when* and *why* to invoke these — as an uplinkable rule/command table. Each GPCC command is bounds-validated (rejected if out of range), versioned, hash-stamped, and logged. Structure-altering commands take an authorised (two-key) path.

**cFS mapping:** the GPCC is delivered as cFS **Table Services** (parameter tables) + the **Stored Command** app (command sequences), bounds-enforced by the **Limit Checker** app, ingested via **Command Ingest** over CCSDS telecommand. Nothing exotic — it is the standard reconfigurable-flight-software pattern, with Hs's hash-chain added.

## 4 · In-flight adaptability and the delta-correction factor
Three drift sources, handled uniformly as a hash-stamped `APPLY_DELTA` (or structural) event:

- **Data drift** — sensor recalibration, a new phase, an environment shift → recalibrate inputs / restructure carriers.
- **Method drift ("us")** — a detected miscalibration in the model itself → adjust parameters or apply a correction offset.
- **Both** — a combined delta, recorded as two attributable events.

A **delta-correction** records: trigger, justification, before/after config hashes, and authoriser. On a discovery that *alters the structure vector space* (a new carrier), `ADD_CARRIER` re-parameterises the chain and the CNQ atlas grows new exact D=4 facets — deterministically, with the structural delta in the provenance. **Replay guarantee:** input + command log → identical output, always.

## 5 · The Coherence Supervisor — an engine that monitors the engines
The geosensing architecture already runs **one CNT per sensor / subcomposition / facet** (an ensemble). The Supervisor is the master coherence controller over that ensemble:

- **Coherence law (built-in).** Overlapping charts must agree on shared parts — the CN-TT tiling **cocycle / subcompositional-coherence** condition. The Supervisor checks it continuously; a violation localises a fault. (Hs polices Hs with Hs's own algebra.)
- **Drift / divergence detection.** Flags any engine departing the consensus or its calibration.
- **Redundancy voting.** Run N copies (triple-modular redundancy, as on the Artemis II flight computer); vote per output; outvoted modules flagged for scrub/reset.
- **FDIR.** Fault detection, isolation, recovery: isolate the bad engine, roll it to last-good config, escalate to the expert (GPCC) if structural.
- **Smart-downlink (carrier filter).** Decide what to carry — facets and flags, not raw cubes — on a need-to-know basis.
- **Master hash-chain + health log.** "or more": it is also the health monitor, the reconfiguration executor (applies validated GPCC), and the safe-mode arbiter.

**cFS mapping:** the Supervisor is a **Health & Safety**-class app plus a voting layer over redundant CNT apps; it uses **Checksum / Memory Dwell / Memory Manager** for integrity (memory scrubbing) and the **Stored Command** path for autonomous responses.

## 6 · What NASA expects — redundancy and data flexibility, addressed
**Redundancy / fault tolerance.** Triple- (or N-) modular redundancy with real-time voting; watchdog timers; memory scrubbing; **safe mode = rollback to the last-good hash-stamped config** (content-addressed, so provably the right state); ground-segment backup; the layered "each catches what the previous misses" model. The ensemble is *natively* redundant — extra copies are extra votes.

**Determinism & assurance.** Bounded, deterministic kernels; a published formal I/O contract (**HUF-STD-002**); a seven-step verification protocol; four-form code (Python + R + pseudocode + spec). This is what **NPR 7150.2** mandates and what `cFS` apps are built to satisfy.

**Data flexibility / delta processing.** Reconfiguration by **uplinked parameter/command tables** (the GPCC) over **CCSDS** telecommand; telemetry of facets + health; **onboard delta encoding, triage, and store-and-forward**; bandwidth-aware smart-downlink. Delta processing is the native mode, not an add-on.

**Auditability.** Every command and state change is hash-logged → the ground can verify and exactly replay any in-flight decision after the fact.

## 7 · Why Hs fits this seat uniquely
Determinism + hash provenance + fixed-size vector-space kernels + a **built-in coherence law** (the tiling cocycle) + **bounded, logged, reversible adaptation** = an engine that can adapt in flight *without* the opaque self-modification that flight assurance forbids. The adaptability is real; the trust is preserved. That combination is rare, and it is the entry ticket to the front-end / onboard seat.

## 8 · Division of labour
- **Hs provides:** the bounded primitive set, the coherence/consistency math, the determinism + hash-provenance contract, the fixed kernels.
- **Matthew (domain) provides:** the geological control logic atop the primitives, and the calibration that sets reliability weights and delta-corrections.
- **The agency provides:** the flight platform (cFS / rad-hard processor), the redundancy harness, and the mission requirements.

## 9 · Honest tiering
- **Determinism-preserving adaptation (versioned hash-stamped configs):** sound by construction — **confirmed in principle**; the primitive set is small and deterministic.
- **The cFS / TMR / NPR-7150.2 mapping:** an accurate fit to established flight practice — **design, to be implemented and certified**.
- **A working flight engine and the "above current standard" onsite performance:** **to be earned** — prototype, validate with Matthew, then TRL-raise with the agency.

## Sources
- NASA core Flight System (cFS): [coreflightsystem.net](https://www.coreflightsystem.net/) · [nasa/cFS (GitHub)](https://github.com/nasa/cFS) · [GSFC cFS](https://etd.gsfc.nasa.gov/capabilities/core-flight-system/)
- Triple-modular redundancy in flight computers (Artemis II): [WebProNews](https://www.webpronews.com/inside-the-machine-that-must-never-fail-how-nasa-engineered-artemis-iis-triple-redundant-flight-computer/) · [TMR (overview)](https://en.wikipedia.org/wiki/Triple_modular_redundancy)
- NASA software engineering standard: [NPR 7150.2](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7150_002D_&page_name=AppendixD)
- Hs context: `00_EXECUTIVE_OVERVIEW.md` · `HS_FRONTEND_POSITION.html` · `GEOSENSING_CONCEPT_PROPOSAL.md` · `../../huf-gov/standards/TENSOR_TRAIN.md` (HUF-STD-002).

*A controllable engine that never stops being auditable. The instrument reads. The expert decides. The hashes carry the receipts.*
