# Engine Interop Registry — making version updates stop being a roadblock

*Design note, 2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Answers the question: can all engines read all other engines, via a version registry + routing + a compensation function, so updates stop orphaning past results? Yes — with one hard limit (§6). Companion to `CNTT_V4_ENGINE_DESIGN.md`; consistent with the engine‑independence policy (INV‑038).*

---

## 0 · The problem and the answer

**Problem.** Every engine version (CNT v3.2.0, CNQ v2.0.0, CN‑TT v4.0.0) emits its own deterministic content hash, independent by design. When the engine is updated, outputs and hashes change, so past results aren't directly comparable to new ones and every bump becomes a re‑validation roadblock.

**Answer.** Add a **version registry + per‑pair transform layer above the engines** (not a change to the hashing). Because every output is already self‑describing (engine/version/schema triple), deterministic, and hashed, a reader can route by producer and apply a **registered, hash‑certified transform** to bring any other engine's output into its own frame — for everything that is mathematically recoverable. The one thing no transform can do is recover information a prior version discarded (§6); those fields are flagged "re‑run from source," never faked.

## 1 · Prerequisites (already in place)
- **Self‑describing outputs:** each payload embeds `{engine, engine_version, schema_version}` (verified in `cnt.py`, `cnq.py`, and built into `HCI-CNTT/engine/provenance.py`).
- **Determinism:** same input → same output, bit‑for‑bit. A transform between versions is therefore itself testable and certifiable.
- **Content hashes:** each output carries a canonical SHA‑256. Transforms get their own receipts (§5).

## 2 · The registry (a small, append‑only, hash‑certified JSON)
One node per engine version:
```
{ engine, version, schema_version, hash_algorithm, field_schema,
  edges: [ { to: <version>, transforms: {field: <transform-spec>}, certified_by: <hash> }, ... ] }
```
Edges connect adjacent versions; multi‑step routes are the chained composition of edges (v2 → v3 → v4). The registry itself is versioned and hashed.

## 3 · The "compensation" = a per‑field transform (taxonomy)
The compensation Peter intuited is, precisely, a transform spec per field per version‑pair — usually a function + parameters, a single scalar only in special cases:
- **identity** — field computed identically in both versions (closure, CLR, ILR, Shannon entropy, K_eff, Aitchison norm/distance, TV). The majority. No work.
- **reparameterization** — a bijection (e.g. `H ↔ K_eff = exp(H)`); invertible both ways.
- **correction** — recompute from stored components (e.g. the v4 **atan2‑stable angle** vs the oracle's `arccos` angle — recoverable when the underlying vectors are in the record).
- **lossy‑down** (richer → poorer) — drop/aggregate to the older frame. Always possible.
- **lossy‑up** (poorer → richer) — **not a transform**; marker `RE_RUN_FROM_SOURCE` (§6).

## 4 · The reader contract
Any engine `vN` (N ≥ registry inception), given another output and its version tag, looks up the route `vM → vN`, composes the edge transforms, and emits the foreign output in its own frame — with explicit `RE_RUN_FROM_SOURCE` markers on any lossy‑up fields. Reading is total for losslessly‑transformable fields; honest (not silent) on the rest.

## 5 · Governance guardrails (so interop stays honest)
- **Append‑only:** transforms are added, never edited in place; a correction to a transform is a new, dated, hashed entry.
- **Hash‑certified:** each edge is certified by running it on the experiment corpus and recording the hash of `transform(old_output)` against the freshly‑computed `new_output`. The **parity harness** (engine build P3) is exactly what generates and certifies these — interop falls out of the work already planned.
- **Independence preserved:** per‑engine content hashes stay independent (INV‑038); the registry is a layer on top, not a re‑hash.
- **Lossy‑up never faked:** a field that needs information the source output lacks is marked for re‑run, not synthesized.

## 6 · The one hard limit (be explicit)
A transform can **preserve and re‑express** information, never **manufacture** it. So translation is always possible **richer → poorer**, and possible **poorer → richer only by re‑running from source data**, not by transforming the old output. This is the same fact as the CNQ‑tiling reconstruction (lossless **iff** the chart graph is connected): gluing/transforming moves information around; it cannot create what was discarded. Example: the oracle's lossy first‑3‑axes projection for D>4 cannot be "compensated" up to v4's lossless reading — only a re‑run recovers it.

## 7 · "The first engine cannot" — precisely
- A version can be made a **readable node** retroactively by registering a transform for its output format.
- To be a **reader**, a version must ship with registry‑consulting code.
- The original engine predates the registry, so it is **readable but not a reader**. Every version from the registry's inception forward is a **full peer** (reads all, read by all). Exactly as Peter framed it.

## 8 · Why this removes the roadblock
At each release a new version registers only its transforms to/from its immediate predecessor; the parity harness certifies them; thereafter all registry‑aware engines interoperate and **all past hashed artifacts remain first‑class** rather than orphaned. The engine can evolve without re‑validating the entire past by hand — the certified transforms are the bridge. Updates become additive, like the engine itself.

## 9 · Fit with v4 and next step
v4 should register, at parity time: **identity** transforms for all Tier‑A parity fields; **correction** transforms for the documented improvements (atan2 angle; zero‑treatment); and `RE_RUN_FROM_SOURCE` markers for the lossy‑up fields (D>4 lossless reconstruction the oracle could not produce). Concrete next step: add an `engine_registry.json` + a thin `read_foreign(output)` resolver to `HCI-CNTT/`, populated by the parity harness. (Build item; not yet implemented.)

## Claim tiers
- **Tier 1 (verified):** outputs are already self‑describing/deterministic/hashed; identity fields are bit‑identical across versions where the math is unchanged.
- **Tier 2 (sound engineering):** the registry + transform taxonomy + reader contract + governance; the lossy‑up limit (information‑theoretic, certain).
- **Tier 3 (to build):** the actual `engine_registry.json`, the resolver, and the harness‑generated certified transforms.

*The registry translates; it does not hallucinate lost precision. The instrument reads. The expert decides. The hashes carry the receipts.*
