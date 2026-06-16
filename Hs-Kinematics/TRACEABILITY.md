# Traceability — a required feature of Hˢ

*Full traceability is a required, specified property of the Hˢ instrument, not an add‑on. This note states the requirement and shows where each part is implemented. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker. Tier 1.*

---

## The requirement

> **Given any Hˢ result, one can recover — and independently re‑derive — the exact input that produced it, the exact operations applied, the exact engine version, and the confidence tier of every number. A result that cannot be traced this way is not a valid Hˢ result.**

This is the metrology stance the framework inherits from its origin: a measuring instrument that cannot tell you how it arrived at a reading cannot be trusted in a system with consequences. Traceability is therefore a *gate*, the same way the guards are a gate.

## The five links, and where each lives

| # | Link | Mechanism | Where |
|---|---|---|---|
| 1 | **Result receipt** | SHA‑256 over the 12‑dp, key‑sorted payload — on *every* output | `hs_kinematics_engine.stable_hash` → `content_hash`; `hs_diagnosis` utterance hash; `hs_budget` budget hash |
| 2 | **Input provenance** | a manifest recording source path, config, shape, carriers, and the output's SHA‑256 | `hs_data_prep.write_ready` → `*.manifest.json` |
| 3 | **The chain** | each stage carries the prior hash forward (HUF‑STD‑002 "Tensor Train") | `raw → prep(manifest) → engine(content_hash) → diagnosis/budget(hashes)` |
| 4 | **Verifiability** | value‑determinism — identical hashes cross‑platform (Windows ≡ Linux) | conformance anchor, `HS_KINEMATICS_SPECIFICATION.md` §11 |
| 5 | **Epistemic provenance** | claim tiers (1 measured / 2 reasoned / 3 exploratory) travel with each quantity | every spec section + every report |

## What this buys

- **Reproducibility.** Anyone re‑running the chain reproduces the receipts exactly, or the divergence is located to the link (`ADAPTIVE_ANTICIPATION.md`).
- **Auditability.** A result can be walked backward — receipt → engine version → manifest → source — with no gap where "someone decided."
- **Trust without authority.** Because the chain is verifiable by hash, a peer (or a peer *node*, in a distributed deployment — `../HCI-CNTT/DISTRIBUTED_CONTROL_AND_LEADER_ELECTION.md`) confirms a result by recomputation, not by taking anyone's word.
- **Regulatory readiness.** This is the shape that ISO/GUM/MSA‑style trust requires of a measurement method (`../stewardship/iso-standards/PATH_TO_A_STANDARD.md`).

## The standing rule

Emit no Hˢ reading without its receipt; keep the manifest with the data; carry the tier with the number; re‑verify after every change. Traceability is the feature that makes every other feature *trustable* — and it is required, always.
