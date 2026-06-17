# CN‑TT v4 — Complete Specification

*Authoritative consolidated specification, 2026-06-10. Engine: `HCI-CNTT v4.0.0` (schema `cntt/4.0.0`). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. This is the single reference spec; it consolidates `CNTT_V4_ENGINE_DESIGN.md`, `MODULAR_ARCHITECTURE.md`, `CONTROL_POINTS_AND_REMOTE_ADAPTATION.md`, `ENGINE_INTEROP_REGISTRY.md`, `CNTT_CHAIN_COMPLETENESS_MAP.md`. Source of truth on any conflict: `HS_FAST_REFRESH.json`.*

---

## 1 · Identity & status
- **Name / version / schema:** `HCI-CNTT` / `4.0.0` / `cntt/4.0.0`. Reference implementation of **HUF‑STD‑002 (Tensor Train)**.
- **Relationship to the oracle:** the frozen **CNT v3.2.0 + CNQ v2.0.0** are the validation baseline; v4 supersedes them and retires them only after certified parity (it has already passed Tier‑A parity on real Backblaze data, §11). The interop registry preserves the oracle's data legacy after retirement.
- **Lockdown:** the oracle code, the HUF‑STD schemas, and the INV catalog are not modified; v4 is additive.

## 2 · Purpose & scope
CN‑TT reads the **dynamics of compositional data** — vectors of parts carrying only relative information — deterministically and auditably. It is domain‑neutral: the same engine serves mudstone chemostratigraphy, field/flight geosensing, microbiome and medical monitoring, and energy/market analysis. Domain interpretation lives in wrappers, never in the engine. The instrument reads; the expert decides.

## 3 · Architecture — the Tensor Train (4 hash‑linked links) + modular sections
```
RAW ─▶ L1 Ingest+Treat+Calibrate ─▶ L2 Geometry ─▶ L3 Tile/Atlas ─▶ L4 Navigate+Emit ─▶ OUT(+receipts)
```
Each link is realized by one or more **`Stage`** objects. A Stage is simultaneously (i) a **control point** — bounded `config` clamped to `config_bounds`; (ii) a **test point** — `self_test()`; (iii) a **hash‑cacheable unit** — keyed by `(input‑digest, config, version)` so identical work is never repeated, and a config change recomputes only that section and what is downstream of it. The math is **locked in the middle, contracted at the edges**.

## 4 · The stages

| Stage | Link | Role | Control‑point config (bounds) | Status |
|---|---|---|---|---|
| `AdaptStage` | L0/L1 | domain raw → (carriers, labels, matrix) | (per‑adapter) | ✅ basic (CSV/array); more adapters TBD |
| `TreatStage` | L1 | zero‑treatment (multiplicative replacement of rounded zeros) | `frac ∈ [0.5,0.8]` | ✅ |
| `CalibrateStage` | L1 | identity / bounded linear gain·offset; calibration‑gating | `gain, offset` | ✅ basic; calibration‑map interface TBD |
| `GeometryStage` | L2 | closure → CLR → Helmert‑ILR → radial | — (locked math) | ✅ |
| `AtlasStage` | L3 | sliding/hierarchical tiling + lossless reconstruction | `strategy ∈ {sliding, hierarchical}` | ✅ |
| `NavigateStage` | L4 | the navigation family (§6) | `regime_k ∈ [1.5,3], regime_threshold ∈ [0.02,0.1]` | ✅ core family; full parity TBD |

## 5 · The tile/atlas core (L3)
- **D=4 primitive:** a four‑part composition's 3 ILR coordinates identify with a unit quaternion on **S³ = SU(2)**; the sandwich product `q v q*` reads the move as an exact rotation; bearing/handedness from the quaternion; angles via the **stable form** `2·atan2(‖û−v̂‖, ‖û+v̂‖)` (exact in any dimension; the documented improvement over `arccos`).
- **Atlas:** cover a D‑part composition with overlapping exact 4‑part charts. `sliding_window` (band, overlap‑3) or `hierarchical` (balanced 4‑ary tree; for microbiome this tree is the **phylogeny**).
- **Lossless reconstruction:** chart log‑ratios stack into `A c = b`; `AᵀA` is the co‑occurrence graph Laplacian; the full CLR is recovered (up to sum‑zero) **iff the graph is connected** (overlap necessary — verified: connected ≈1e‑13, disjoint fails). Conditioning ∝ graph diameter → the **hierarchical atlas (O(log D) diameter)** holds machine precision at scale (≈4e‑12 at D=10⁶; ≤1.6e‑13 on sparse microbiome data to D=10,000, §11).

## 6 · The navigation family (L4) — definitions & status
Per step (all built ✅, ported faithfully from the oracle except where noted):
- `shannon_entropy`, **`k_eff = exp(entropy)`** (effective carriers / concentration), `higgins_scale = 1 − H/log D` + `ring_class` (Hs‑1..6 at 0.1/0.3/0.5/0.7/0.9).
- `aitchison_norm = ‖clr‖`, `aitchison_step = ‖Δclr‖`, `tv_distance = ½Σ|Δp|`.
- **`helmsman = argmax|Δclr|`** (which carrier steers the change).
- **`angular_velocity`** — stable any‑D angle (⚑ improvement over oracle `arccos`).
- **`concentration_regime`** — tightening / loosening / **deceptive** (tightening ∧ TV ≤ series median) / stable, threshold 0.05.
- `kappa_HS_trace`, `s_j_sensitivity`, `bearing_pairs` (atan2; O(D²) — emitted at low D only).
- Series: `regime_boundaries` (`mean + k·std` on step distance), `k_eff` summary, `regime_counts`, lock events, degeneracy flags.

**Pending for full oracle‑output parity (P2 remainder):** helmsman rolling‑window family (flips/torque/etc.), attractor fit (P2 limit cycle), depth tower (energy/curvature levels, M²=I involution, IR class), stage1/2/3 (variation matrix, triadic area, subcomposition ladder), EITT bench, navigation_2d PCA. Parity expected; unproven until ported.

## 6b · Guard, resolvability & control layer (additive, built 2026‑06)

Beyond the navigation family, the engine now reads **the boundary of what it can honestly resolve**, and can act behind breakers. All additive, observe‑only by default, oracle untouched; each module self‑tests PASS (kill‑tests in `experiments/engine_killtest_2026-06/`). Full rationale + the before/after table: **`ENGINE_CAPABILITIES_DELTA_2026-06.md`**; codes: `CNTT_DIAGNOSTIC_CODES.md §7`.

- **Resolvability guard** (`engine/helmsman_guard.py`): at rest → `HM‑NUL‑WRN` (no resolvable helmsman, not a noise leader); tie → `HM‑TIE‑WRN` (not broken by index); reports magnitude + margin.
- **Coherent helmsman** (`engine/structural_guards.py`): pairwise‑log‑ratio (closure‑invariant) helmsman — unchanged when an irrelevant carrier is added (fixes CLR subcompositional incoherence).
- **Effective‑rank guard** (`structural_guards.effective_rank`): `DG‑RNK‑WRN` when motion collapses into a subspace (an `eigh`‑instability sibling of the carrier guard).
- **Hold‑lock + hysteresis** (`structural_guards.hold_lock`): discovers the trigger from `max(system, engine)` noise floor; ties down near‑zero drift, registers a structural change only when sustained; the held state is announced (`L4‑HLD‑INF`), never silent. A self‑calibrating, chatter‑free upgrade of the `mean+k·std` regime boundary.
- **Sparsity detector + Bayesian‑multiplicative** (`engine/zero_methods.py`): `GD‑SPZ‑WRN` when the CLR geometry is replacement‑δ‑dominated; `GD‑ZBM‑CAL` count‑aware zero treatment. E‑21 multi‑method zero registry (`GD‑ZRC/CNC/ZRP/ZUN`) replaces silent `nan` on a degenerate carrier.
- **precise_ops** (`engine/precise_ops.py`): Neumaier compensated reductions for the closure/CLR zeros + an error‑feedback accumulator for stateful integrators (precision in the carrier).
- **SafeLoop** (`engine/loop_control.py`): the first time the engine may *act* — a closed‑loop controller, OBSERVE→ACTIVE→TRIPPED, behind mandatory breakers (`LC‑TRIP‑*`) + manual `LC‑ESTOP` + a time‑boxed window (`LC‑WIN‑END`), bounded/dithered/anti‑windup, deterministic.

Doctrine: `DESIGN_PHILOSOPHY_THE_EXPERT_ENGINE_AND_THE_GUARDS.md`, `PRECISION_AND_CONTROL.md`, `DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md`.

## 7 · Determinism & provenance
- **Determinism:** same input + same config → same output, bit‑for‑bit. No statistics/sampling in the science path. Any sampling (e.g. an optional cap) uses a fixed declared seed.
- **Cross‑platform determinism contract:** `stable_hash` normalizes floats to a declared precision (`DETERMINISM_DECIMALS = 12`) before hashing, so receipts match across platforms (rover ↔ ground) to 1e‑12. (Honest limit: hash stability to declared precision; full bit‑identity of raw floats across BLAS/FMA is a separate, harder guarantee.)
- **Hashing:** per‑link/section hashes + a `_chain_hash`; a canonical `cntt_content_sha256` over the payload. Per‑engine hashes are independent of CNT/CNQ by design (INV‑038).

## 8 · Control points & remote adaptation
Ten bounded, whitelisted, hash‑stamped, reversible control points across the links (CP‑1 carrier set · CP‑2 zero‑treatment · CP‑3 basis · CP‑4 atlas/tree — *where a domain collaborator's geo codes plug in* · CP‑5 chart focus · CP‑6 fusion weights · CP‑7 nav thresholds · CP‑8 delta correction · CP‑9 freeze/rollback · CP‑10 config hash stamp). No control point touches the locked math/code; adaptation is config within whitelists, vetted by the **Coherence Supervisor**. Remote update changes the config hash → the ground receiver reads the hash, looks it up in the interop registry, and interprets correctly. The same machinery yields **delta‑testing** (each adaptation = a certified, reproducible delta). Full: `CONTROL_POINTS_AND_REMOTE_ADAPTATION.md`.

## 9 · Engine interop registry
A version registry + per‑pair **hash‑certified transforms** above the engines, so any v4+ engine reads any other (the original oracle is a readable node, not a reader). Transform taxonomy: identity / reparameterization / correction / lossy‑down; **lossy‑up ⇒ `RE_RUN_FROM_SOURCE`, never faked** (a transform preserves information, never manufactures it). The **parity harness generates and certifies the transforms** — interop falls out of the planned validation work. Full: `ENGINE_INTEROP_REGISTRY.md`.

## 10 · I/O — payload schema (`cntt/4.0.0`)
```
metadata:   {engine, engine_version, schema_version, principle, atlas_strategy, config}
input:      {n_records, n_carriers, carriers, labels, source_hash, zero_replacement, calibration}
geometry:   {radial summary}            atlas: {strategy, n_charts, n_edges, connected, recon_max_err, lossless}
navigation: {per‑step family (§6), series summary, regime boundaries}
diagnostics:{lock_events, degeneracy_flags, claim_tier, cntt_content_sha256}
provenance: {per‑section chain: stage, version, config, out_hash, cached}, _chain_hash
```
(The explicit `config` block + a formal `CNTT_V4_SCHEMA.md` are a near‑term completion item.)

## 11 · Verification evidence (run these)
- **Kernel self‑test** (`engine/self_test/run_self_test.py`): quaternion sandwich = Rodrigues 2.7e‑15; atan2 exact where arccos fails; lossless tiling ~1e‑13; overlap necessity; D=16‑from‑D=4 1.3e‑15; tree atlas 3.8e‑13 at D=10⁵; determinism. **All green.**
- **Modular self‑test** (`engine/self_test/modular_self_test.py`): every section a test point; deterministic chain hash; full cache reuse on rerun; delta isolation on config change. **All green.**
- **Real‑data parity** (`experiments/backblaze_v4_parity_2026-06/`): v4 vs the frozen oracle on the full Backblaze fleet series (731×4) — **TIER‑A: bit‑identical** across the core family; only diff = the atan2 angle (5e‑11°).
- **Microbiome sniff** (`experiments/microbiome_sniff_2026-06/`): lossless tree‑atlas reconstruction to **D=10,000** (≤1.6e‑13, 7 ms/sample, 0.3 MB); navigation reads an injected diversity collapse with a correct helmsman; deterministic. Reference: coda4microbiome (Calle, Pujolassos & Susin 2023).

## 12 · Chain completeness — built vs pending
- **Built:** the four links + modular sections + determinism contract + caching + the core navigation family + lossless tiling/hierarchical atlas + zero‑treatment + basic adapter/calibration + **the guard/resolvability/control layer (§6b): E‑21 zero registry, resolvability + coherent helmsman, effective‑rank guard, hold‑lock hysteresis, sparsity detector, precise_ops, SafeLoop.**
- **Pending (the completion backlog, prioritized):** (1) full navigation‑parity (§6 remainder) → (2) the parity harness (certifies v4=oracle corpus‑wide, emits interop transforms) → (3) calibration‑map interface + unified adapter contract (Canada loader, microbiome real data) → (4) output `config` block + `CNTT_V4_SCHEMA.md` + `ANTI_SPECIFICATION.md` + CI corpus → (5) **input‑uncertainty propagation** + **streaming mode** (the two highest‑value still‑missing layers) → (6) interop registry + control‑point config layer + Coherence Supervisor/FDIR → (7) smart‑downlink + consumer/visualization → (8) formal extension contracts. Full gap analysis: `CNTT_CHAIN_COMPLETENESS_MAP.md`.

## 13 · Claim tiers
- **Tier 1 (verified):** §11 results; the kernel math; the lossless‑iff‑connected condition; the determinism‑to‑1e‑12 hashing.
- **Tier 2 (standard, soundly applied):** the reconstruction theorem (Greenacre) / synchronization (Singer/Fiedler) basis; Hurwitz/Cayley‑Dickson (no native D≥8); the architecture, control‑point, interop, and delta‑testing designs.
- **Tier 3 (to earn):** full oracle‑output parity; the pending backlog (§12); any domain interpretation; the absolute novelty of the quaternion‑composition reading (final Scholar/ADS/patent pass).

## 14 · References
Aitchison 1986; Egozcue et al. 2003 (ILR); Greenacre 2019/2020 (log‑ratio‑graph reconstruction); Singer 2011, Fiedler 1973, Chung 1997 (synchronization / Laplacian); Hartley 2013, Govindu 2004 (rotation averaging); Zhang & Zha 2004 (LTSA), Brand 2002 (charting a manifold), Lee 2012 (atlas); Silverman et al. 2017 (PhILR), Calle, Pujolassos & Susin 2023 (coda4microbiome); Hurwitz 1898, Baez 2002 (division algebras); Gallier 2011, Hopf 1931 (quaternions/S³/SU(2)). Full positioning: `collaborations/geology-wehner/CNQ_TILING_CONTRIBUTION.md`.

*Locked in the middle, contracted at the edges, hashed at every section. The instrument reads. The expert decides. The hashes carry the receipts.*
