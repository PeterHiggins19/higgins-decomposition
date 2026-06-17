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

## Canonicalization profile for cross‑platform hash parity (the single source of truth)

The content hash is a SHA‑256 over a **canonical JSON string**. For two implementations (Python, R, any language) to produce a *byte‑identical* hash, they must serialize identically. The canonical profile, from `hs_kinematics_engine.stable_hash`, is exactly five steps:

1. **Round every float to 12 decimals, recursively** (through dicts and lists). Integers stay integers.
2. **Serialize with `json.dumps(obj, sort_keys=True, default=str)`** — keys sorted lexicographically at every level; non‑JSON types coerced to their string form.
3. **Use Python's default separators `", "` and `": "` — WITH the spaces.** *(This is the most common port mismatch: R's `jsonlite::toJSON` omits these spaces by default.)*
4. **Encode UTF‑8.**
5. **SHA‑256** the bytes.

**Byte‑for‑byte test vector** (so a porter can iterate without running the whole engine):

```
input  = {"b": 1.1234567890123456, "a": [0.1, 2, 3.0], "c": "x", "nested": {"z": 1.234e-12, "y": -1.5}}
canonical string =
{"a": [0.1, 2, 3.0], "b": 1.123456789012, "c": "x", "nested": {"y": -1.5, "z": 1e-12}}
SHA-256 = d614fcf13e49ae25da46459f52cc9f79780ff7ece34bf5c9edc019a5f63f5c05
```

Read off the divergence points a port must match: keys **sorted** (`a,b,c,nested`; inside: `y,z`); the float `1.1234567890123456` **rounded to 12 dp** → `1.123456789012`; the tiny float `1.234e-12` rounds to `1e-12` and serializes in **Python's exponential form** (`1e-12`, not `0.000000000001`); the integer `2` stays `2` while the float `3.0` stays `3.0`; **spaces after `,` and `:`**. An R port matches the hash only when `jsonlite` (or a hand‑rolled serializer) reproduces all of these.

**Conformance check.** A port is conformant when it reproduces (a) this test‑vector hash `d614fcf1…` and (b) the full‑engine reference hash `fcae0ebe…` (`HS_KINEMATICS_SPECIFICATION.md` §11) on the reference matrix. Per‑field numerical agreement at the IEEE floor is the Tier‑1 substance and is *separable* from byte‑hash parity — verify it first, then chase the canonicalization. *(Pinned 2026‑06‑15 to unblock the R‑port faithfulness check and the cross‑platform hash reproduction.)*

## The standing rule

Emit no Hˢ reading without its receipt; keep the manifest with the data; carry the tier with the number; re‑verify after every change. Traceability is the feature that makes every other feature *trustable* — and it is required, always.
