# CN‑TT v4 — Modular Section Architecture (built + documented)

*2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Documents the modular engine layer built this session and verified by `engine/self_test/modular_self_test.py` (all checks green). Companion to `CONTROL_POINTS_AND_REMOTE_ADAPTATION.md`, `ENGINE_INTEROP_REGISTRY.md`, `../ai-refresh/CNTT_V4_ENGINE_DESIGN.md`, `../ai-refresh/CNTT_CHAIN_COMPLETENESS_MAP.md`.*

---

## 0 · The idea, made real

Each processing section of the engine is now a single uniform object — a **`Stage`** — that is, at once:
- an **adaptability unit** — bounded `config` clamped to `config_bounds` (a control point);
- a **test point** — `self_test()` returns `(ok, detail)`, runnable in isolation;
- a **hashed, cacheable unit** — the pipeline keys each section by `(input‑digest, config, version)` so identical work is **never repeated**. *Why repeat history at the cost of time and effort?*

The math stays **locked in the middle** (geometry, quaternion, atlas reconstruction are unchanged kernel functions); modularity, adaptability, testing, and caching are added **around** it. This is the space‑ready posture: a frozen exact core, a bounded and individually‑testable control surface.

## 1 · The interface (`engine/stage.py`)
```
class Stage:
    name, version
    default_config: dict
    config_bounds: dict          # {param: (lo, hi)} -> clamped  (control-point bounds)
    configure(overrides) -> cfg  # merge + clamp
    run(ctx, cfg) -> dict        # pure: reads ctx, returns NEW outputs to merge
    self_test() -> (ok, detail)  # the test point
```
Stages are **pure**: no I/O, no global state; given the same `ctx` + `cfg` they return the same outputs. That purity is what makes them hashable, cacheable, and verifiable.

## 2 · The pipeline (`engine/pipeline.py`)
Threads an ordered list of stages, building a **provenance chain** and a **hash‑keyed memo cache**:
- before each stage, digest the current `ctx` (`stable_hash`); key = `hash(stage, version, config, input‑digest)`;
- **cache hit → reuse** (the section is not recomputed); **miss → run + store**;
- record per‑stage `{stage, version, config, out_hash, cached}`; emit a `_chain_hash` over the section hashes.
**Consequence (verified):** a rerun with identical input recomputes nothing; a config change recomputes **only the changed section and everything downstream of it** — the upstream stays cached. Adaptation, delta‑testing, and "don't repeat history" are the same mechanism.

## 3 · The determinism contract (`engine/provenance.py`)
`stable_hash()` normalizes floats to a **declared precision** (`DETERMINISM_DECIMALS = 12`) before hashing, so a receipt is **identical across platforms** (rover vs ground) to 1e‑12 — the cross‑platform‑determinism layer the chain‑completeness map called out as essential to the remote‑hash story. Honest limit: this makes the **hash** stable to the declared precision; full bit‑identity of raw floats across different BLAS/FMA implementations is a separate, harder guarantee and is not claimed. Per‑engine hashes stay independent of CNT/CNQ (INV‑038).

## 4 · The sections (built this session)

| Section | Stage | Role | Control‑point config | Test point | Status |
|---|---|---|---|---|---|
| L0 Adapt | `AdaptStage` | domain raw → (carriers, labels, matrix) | — | parse round‑trip | ✅ basic (CSV/array); more adapters to add |
| L1 Treat | `TreatStage` | zero‑treatment (multiplicative) | `frac∈[0.5,0.8]` | a zero → positive replacement | ✅ |
| L1 Calibrate | `CalibrateStage` | identity / bounded linear gain·offset | `gain, offset` | identity preserved; gain applied | ✅ basic; calibration‑map interface to extend |
| L2 Geometry | `GeometryStage` | closure → CLR → Helmert‑ILR → radial | — (locked math) | `sum(clr_row)≈0` | ✅ |
| L3 Atlas | `AtlasStage` | sliding/hierarchical tiling + lossless reconstruction | `strategy` | connected lossless on D=16 | ✅ |
| L4 Navigate | `NavigateStage` | the navigation family | `regime_k∈[1.5,3], regime_threshold∈[0.02,0.1]` | k_eff sanity | ✅ **core family ported** (P2 start) |

**Navigate — what's ported (P2 core):** Shannon entropy, K_eff, higgins_scale + ring class, TV distance, Aitchison norm/step, **stable angular velocity** (`2·atan2(‖û−v̂‖,‖û+v̂‖)` — stable in any D, the documented improvement over arccos), helmsman index (`argmax|Δclr|`), concentration‑regime tagging (incl. deceptive‑drift), regime boundaries (`mean + k·std`). **Pending for full oracle parity:** helmsman rolling‑window family, attractor fit, κ_HS, s_j sensitivity, bearing pairs, EITT, nav‑2D PCA, lock/degeneracy events.

## 5 · Verified properties (`modular_self_test.py`, all PASS)
1. **Every section is a test point** — all six `self_test()` green.
2. **Deterministic** — rerun → identical `_chain_hash`.
3. **History not repeated** — rerun → all six sections `cached=True`.
4. **Adaptability + delta isolation** — change `atlas.strategy` → `adapt/treat/calibrate/geometry` stay cached, only `atlas/navigate` recompute; chain hash changes. (Plus: navigation family runs end‑to‑end; atlas lossless in‑chain at ~4e‑16.)

## 6 · How this is space‑ready
- **Bounded control surface:** every adaptable knob is clamped to declared bounds (the CP‑1…CP‑8 map); no opaque self‑modification.
- **Per‑section receipts:** the provenance chain + section hashes give an audit trail a ground receiver / Coherence Supervisor can verify section‑by‑section.
- **Delta‑testable:** any single adaptation is an isolated, reproducible delta (the cache shows exactly what changed).
- **Cross‑platform receipts:** the determinism contract makes the hashes mean the same thing on the instrument and on the ground.
- **No wasted recompute:** cached sections are never re‑run — critical where compute and power are scarce.

## 7 · Built vs still pending (honest)
- **Built this session:** the Stage/Pipeline framework, the determinism contract + stable hashing, the six sections (adapter/treat/calibrate/geometry/atlas/navigate with the core nav family), the modular self‑test.
- **Pending (next):** full navigation parity (the rest of §4); the parity harness (P3) that certifies v4 = oracle and emits the interop transforms; the interop registry + resolver; the Coherence Supervisor wiring; input‑uncertainty propagation and streaming mode (the two highest‑value still‑missing layers, per the completeness map); the `config` block in the emitted payload + `CNTT_V4_SCHEMA.md`; an `ANTI_SPECIFICATION.md` (failure modes).

## 8 · Claim tiers
- **Tier 1 (verified):** all §5 properties (self‑test green); the kernel math; the determinism‑to‑1e‑12 hashing.
- **Tier 2 (sound engineering):** the section architecture, the cache/delta semantics, the space‑readiness mapping.
- **Tier 3 (to build):** full nav parity; harness‑certified equivalence to the oracle; uncertainty/streaming; the remaining completeness‑map items.

*Locked in the middle, contracted at the edges, hashed at every section. The instrument reads. The expert decides. The hashes carry the receipts.*
