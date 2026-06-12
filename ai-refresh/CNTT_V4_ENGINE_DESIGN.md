# CN‑TT v4 — Tile‑Native Engine Design Specification

*Design spec, 2026-06-10. Status: DRAFT for Peter's approval — no kernel code is written until this is signed off. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Successor design doc to `ai-refresh/CNT_V3_CNQ_V2_DESIGN.md`. Build target chosen: design-spec-first; v1 scope = kernel + navigation parity; stack = port-ready Python core.*

---

## 0 · Decision of record

Build a **new engine** (`CN‑TT v4`, tile‑native) from a clean feedforward design. **Leave the existing engines frozen** — `HCI-CNT v3.2.0` (`cnt.py`) and `HCI-CNQ v2.0.0` (`cnq.py`) become the **oracle**: the ground truth the new engine must reproduce. **Nothing is archived until parity is proven** against the old engines, the experiment corpus, the conference numbers, and the tiling proofs. The past is a stepping stone for *design* and a commitment for *validation* — every divergence found is adjudicated as either a documented improvement or a regression to fix, never silently accepted.

This is also how the **Stage‑1 "verify the basics" gate closes**: the new engine's acceptance criterion *is* "reproduces the validated corpus + the tiling proofs," which is a stronger, forward‑looking verification than re‑running the old Round‑3 on a frozen artifact.

---

## 1 · Why a new engine (not a patch)

The frozen engines were built global‑first: `closure → CLR → Helmert‑ILR → trajectory tensor` over the *whole* D‑dimensional composition, with the quaternion layer (`cnq.py`) **exact only at D=4** and everything else a compromise:

- `classify_dimension` (cnq.py) sends **D=8** to "twin‑quaternion," **D=16** to a *schema‑locked, unimplemented* "quad‑quaternion (INV‑043)," and **D=5–15 / D≥17** to a **lossy projection onto the first 3 ILR axes** (`captured_step_fraction < 1`). That is precisely the native‑higher‑D path we have now ruled out (octonions lose associativity; sedenions lose division — see `collaborations/geology-wehner/HIGHD_DETERMINISTIC_SCALING.md`).
- The 2026‑06‑10 proof (`experiments/cnq_tiling_highd_2026-06/`) showed the **tile‑native** alternative: overlapping exact D=4 charts on a connected atlas reconstruct any‑D composition **losslessly** (≈4e‑12 to D=10⁶ on a hierarchical/phylogenetic atlas), deterministically, in seconds.

So the architecture itself changed. Retrofitting a tile‑native primitive into a locked global engine is more work and less clean than a fresh design built **to the goal** (deterministic, hash‑chained, edge/flight‑grade, arbitrary‑D, NASA/USGS‑bound). Hence: new engine, old frozen as oracle.

### Known weaknesses in the oracle that v4 fixes by design (each is a *documented improvement*, not a silent change)
1. **`angular_velocity_deg` uses `arccos(clip(dot))`** (cnt.py L259‑267) — collapses near 0°/180°. v4 uses the **atan2‑stable** form `atan2(‖a×b‖, a·b)` (recovers ~8 digits near the poles; verified 2026‑06‑10).
2. **D>4 CNQ is lossy** (first‑3‑axes projection). v4 reconstructs **losslessly** via the D=4 atlas.
3. **Zero handling is a hard `1e‑15` floor** in `ingest_csv` (cnt.py L941‑944). v4 uses the validated **`zero_treatment`** adapter (structural drop + multiplicative replacement) upstream.
4. **`compute_stage3` materializes `list(combinations(range(D), k))` before slicing** (cnt.py L655) — memory blow‑up at high D. v4 uses lazy `itertools.islice` (or atlas‑scoped subsets) — the open Stage‑1 engine fix.

---

## 2 · Scope

**In scope for v1 (kernel + navigation parity):**
- The tile‑native kernel: D=4 chart primitive, atlas builder (sliding‑window **and** hierarchical/tree), lossless reconstruction, zero‑treatment, hash provenance.
- The full **navigation layer at parity** with the oracle: `shannon_entropy`, `higgins_scale`, `k_eff = exp(H)`, `tv_distance` (half‑L1), Aitchison norm/distance, `kappa_HS_full`, `s_j_sensitivity`, bearing pairs (atan2), angular velocity (atan2‑stable), helmsman local index `argmax|Δclr|`, the helmsman family, the concentration‑regime tagger (tightening/loosening/deceptive/stable, threshold 0.05), `ring_class`, the D=4 quaternion sandwich/radial/bearing, attractor fit, lock events, degeneracy flags, EITT bench, `navigation_2d` PCA barycenter.
- A canonical, deterministic JSON payload with an embedded `cntt_content_sha256` and the engine/schema version triple.

**Deferred (post‑v1, named so they aren't forgotten):** twin/quad‑quaternion factoring + CHSH (deprecated — superseded by tiling; kept readable in the oracle only); the differential‑geometry research layer (curvature/holonomy/Chern‑Simons/Berry/instanton — quarantined until earned); R reference port; compiled flight port.

**Non‑goals:** no statistical/probabilistic substitution anywhere; no change to the frozen engines; no archiving before parity; no new canonical scientific claims introduced by the engine itself (it computes; claims stay human‑authored and tiered).

---

## 3 · Architecture — the Tensor Train, tile‑native

The engine is the reference implementation of **HUF‑STD‑002 (Tensor Train)**. Four hash‑linked links, each pure and independently testable:

```
 raw CSV ─▶ L1 Ingest&Treat ─▶ L2 Geometry ─▶ L3 Tile/Atlas ─▶ L4 Navigate&Emit
            (zero_treatment,     (closure,        (D=4 charts,      (CNT/CNQ readings,
             validate, hash)      CLR, Helmert     overlap atlas,    nav family, payload,
                                  ILR, radial)     reconstruct)      content hash)
```

- **L1 Ingest & Treat** — strict CSV read (label col + D carriers), `validate_rows`, **zero‑treatment** (replaces the 1e‑15 floor), source `file_sha256`. Records `zero_replacement_count` / structural‑drop list.
- **L2 Geometry** — `closure → clr → helmert_basis → ilr = clr @ Hᵀ`; radial = ‖ilr‖ per step. Pure, port‑ready, numpy‑only.
- **L3 Tile/Atlas** — the new core. Build an **atlas** of overlapping exact 4‑part charts; expose the **reconstruction** of the full CLR/ILR (and any subcomposition move) from chart‑local log‑ratios via the sparse Laplacian solve. Atlas strategies: `sliding_window` (overlap‑3 band) and `hierarchical`/`phylogenetic` (balanced 4‑ary tree, O(log D) diameter — the precision default at high D). Connectivity check = losslessness guarantee; disjoint ⇒ rejected.
- **L4 Navigate & Emit** — compute the navigation family (per §6) per chart and globally; assemble the canonical payload; compute `cntt_content_sha256` over the payload sans the hash field.

Each link emits a small link‑level hash so the chain is auditable end‑to‑end ("Hs measures, HUF carries"). At D=4 the atlas is a single chart and v4 reduces **exactly** to the oracle's native path.

---

## 4 · Core data contracts (interfaces a C/Rust port must honor)

- **Composition**: `x ∈ ℝ^D`, `x_i > 0` after treatment, closed to sum 1.
- **Chart**: an ordered tuple of 4 part‑indices `(a,b,c,d)`; carries its local Helmert‑ILR (3 coords) and unit quaternion.
- **Atlas**: `{charts: List[Chart], strategy, overlap, diameter, connected: bool}`. Contract: the part co‑occurrence graph is **connected** (else reconstruction is rejected as rank‑deficient).
- **Reconstruction**: `atlas + per‑chart log‑ratios → CLR (sum‑zero)`, exact when connected; returns `recon_error` against any available global reference.
- **NavigationRecord** (per step + series summary): the §6 quantities.
- **Payload**: `{metadata(version triple, config, env, hashes), input(source hash, carriers, labels, treatment), geometry, atlas, navigation, diagnostics(content hash, claim_tier flags)}`.

Versioning: `engine="HCI-CNTT"`, `engine_version="4.0.0"`, `schema_version="cntt/4.0.0"`. Hashes are **independent** of CNT/CNQ hashes by design (engine‑independence policy, INV‑038), but a `legacy_reference` block may record the oracle's `cnt_content_sha256`/`cnq_content_sha256` as informational metadata (not hash‑chained).

---

## 5 · The tile‑native kernel

- **D=4 primitive**: composition → Helmert unit vector in ℝ³ → unit quaternion; sandwich `q v q*` for the exact rotation; radial = ‖ilr‖; bearing/handedness from the quaternion. Reproduces `build_bearing_trajectory_d4` exactly; the only intended numeric change is the **atan2‑stable** angle.
- **Atlas builder**: `sliding_window(D)` (band, overlap‑3) and `hierarchical(D, k=4)` (group→representative→recurse; the tree whose leaves are parts and, for microbiome, *is* the phylogeny). Both O(D) charts; tree gives O(log D) diameter.
- **Reconstruction**: stack chart‑internal log‑ratios `log(x_i/x_j)=clr_i−clr_j` into `A c = b`; `AᵀA` is the co‑occurrence graph Laplacian; solve with one node pinned per component, recenter to sum‑zero. Lossless iff connected. (This is the proven 2026‑06‑10 result.)
- **Determinism**: no RNG in the kernel; if any sampling is ever needed (e.g. triadic cap), it uses a fixed declared seed exactly as the oracle does (seed=42) so output is reproducible bit‑for‑bit.

---

## 6 · Navigation layer — parity definitions (the contract with the oracle)

Reproduced exactly from `cnt.py`/`cnq.py` (constants in parentheses), with the four documented improvements flagged ⚑:

| Quantity | Definition (oracle) | v4 |
|---|---|---|
| closure / CLR / Helmert‑ILR | `clr = log x − mean log x`; `ilr = clr @ Hᵀ` | identical |
| shannon_entropy / k_eff | `H = −Σ p log p`; `k_eff = exp(H)` | identical |
| higgins_scale | `1 − H/log D`; `ring_class` Hs‑1..6 (0.1/0.3/0.5/0.7/0.9) | identical |
| Aitchison norm/distance | `‖clr‖`; `‖clrₐ−clr_b‖` | identical |
| tv_distance | `½Σ|pₐ−p_b|` | identical |
| kappa_HS_full | `K=(δ−1/D)/ (p⊗p)`; eigen/trace/cond | identical |
| s_j_sensitivity | inverse‑closed `(1/p)/Σ(1/p)` | identical |
| bearing pairs | `atan2(h_j, h_i)` per pair | identical (already atan2) |
| angular velocity | `arccos(clip(a·b/‖a‖‖b‖))` | ⚑ **atan2‑stable** `atan2(‖a×b‖, a·b)` |
| helmsman local | `argmax|Δclr|` | identical |
| helmsman family | rolling window 8 | identical (port `compute_helmsman_family`) |
| concentration regime | k_eff_yoy threshold 0.05; deceptive = tightening ∧ tv≤median | identical |
| regime boundaries | step‑distance `> mean + 2·std` | identical (note: oracle uses std, not MAD) |
| D=4 quaternion | sandwich residual gate `1e‑12` | identical (⚑ atan2 angle) |
| D>4 reading | first‑3‑axes **lossy** projection | ⚑ **lossless tiling reconstruction** |
| zero handling | hard `1e‑15` floor | ⚑ **zero_treatment** adapter |
| navigation_2d | PCA of centred ILR, disk‑scaled 0.85 | identical |
| attractor / lock / degeneracy / EITT | per oracle | identical (ported) |

`hci_shared` functions to re‑implement port‑ready: `closure`, `clr`, `helmert_basis`, `canonical_sha256`, `file_sha256`, `validate_rows`, `compositions_to_ilr`, `compositions_to_helmert_unit_vectors`, `quaternion_sandwich_residuals`, `fit_attractor`, `compute_helmsman_family`. (Twin/CHSH deprecated — not ported.)

---

## 7 · Determinism & provenance

Non‑negotiable, inherited and strengthened: deterministic (same input → same output, bit‑for‑bit), no statistics/sampling in the science path, canonical SHA‑256 content hash over the payload, per‑link hashes for the Tensor‑Train chain, embedded version triple + environment metadata, claim‑tier flags on every emitted block. The differential‑geometry research layer stays **out** of the canonical payload entirely.

---

## 8 · Port‑readiness rules (Python core, flight‑target later)

- **Kernel purity**: L2/L3/L4 math depends only on `numpy` and a small typed value layer — no pandas, no scipy *in the kernel hot path*. (Sparse reconstruction may use `scipy.sparse` behind an interface `solve_atlas(A, b)` that a C/Rust backend can replace; the band/tree Laplacian solve is simple enough to reimplement without scipy.)
- **Hard interface seams** at each Tensor‑Train link so links can be swapped for compiled implementations independently.
- **No hidden global state, no I/O in the math**; I/O confined to L1 and the emitter.
- **Deterministic types**: float64 throughout; declared rounding only at the emit boundary (as oracle does, 6 dp on bary_xy).
- **Spec‑first parity**: a language‑agnostic pseudocode doc (`CNTT_V4_PSEUDOCODE.md`) and JSON schema (`CNTT_V4_SCHEMA.md`) accompany the build, matching the oracle's documentation pattern.

---

## 9 · Parity / acceptance criteria (the archive gate)

The new engine is **accepted** — and only then may old material be archived — when every item below passes and every divergence is adjudicated.

**Tier A — must match the oracle to ≤1e‑12 (bit‑identical where integer/string):** all §6 "identical" quantities on **zero‑free** data, across the full experiment corpus (`experiments/Hs-01 … Hs‑25`, EMBER, geochemistry, the Frielingen‑9 demo). D=4 quaternion sandwich/radial/bearing exact.

**Tier B — must match within documented tolerance; divergence is a *known improvement* to record:**
- angular velocity near 0°/180° (atan2 vs arccos);
- D>4 readings (lossless tiling vs lossy projection) — report `recon_error` and the captured‑fraction the old engine lost;
- zero‑affected datasets (zero_treatment vs 1e‑15 floor) — reproduce the already‑validated all‑10‑EMBER deltas;
- high‑D `compute_stage3` (islice/atlas vs materialized list) — identical scored subset, lower memory.

**Tier C — new capability, no oracle baseline:** tiling beyond what the old engine could do (D≫4, tree atlas) — validated against the 2026‑06‑10 PoC numbers (lossless ≈4e‑12 to 10⁶; overlap‑necessity; D=16‑from‑D=4).

**Divergence adjudication protocol:** the harness emits, per experiment, `{old_hash, new_result, diff_class ∈ {identical, improvement, regression, unexplained}}`. **Improvement** → documented in an addendum + a one‑line finding. **Regression / unexplained** → blocks acceptance until fixed or explained. The conference (CoDaWork 2026) numbers were generated under v3.1.0 and are a **frozen external commitment**: v4 must reproduce them or explicitly, visibly supersede with a written reconciliation.

---

## 10 · Module layout, naming, versioning

```
HCI-CNTT/                       # new engine home (created at build time)
  engine/
    cntt.py                     # orchestrator (L1..L4)
    geometry.py                 # L2 (closure, clr, helmert, ilr, radial) — port-ready
    atlas.py                    # L3 (chart, sliding/hierarchical builders, reconstruct)
    navigate.py                 # L4 (the §6 navigation family)
    provenance.py               # canonical_sha256, link hashes, version triple
    quaternion.py               # D=4 sandwich, atan2-stable angles
  adapters/
    zero_treatment.py           # reuse the validated adapter (or import)
  CNTT_V4_PSEUDOCODE.md         # language-agnostic algorithm (port reference)
  CNTT_V4_SCHEMA.md             # output schema
  ANTI_SPECIFICATION.md         # failure-mode enumeration (oracle pattern)
  self_test/                    # BIST corpus + dated hash-signed receipt
validation/
  parity_harness.py             # §9 corpus sweep + diff classifier
  PARITY_REPORT_<date>.md/.json # the acceptance evidence
```

Identity: old = `HCI-CNT v3.2.0` + `HCI-CNQ v2.0.0` (**frozen oracle**, untouched); new = **`HCI-CNTT v4.0.0`**. Engine code remains under Peter's sole commit authority; no AI commits.

---

## 11 · Phased build roadmap

- **P0 — this spec** (approval gate). ◀ you are here
- **P1 — kernel**: L1‑L3 (`geometry`, `atlas`, `quaternion`, `provenance`) + self‑test; reproduce the 2026‑06‑10 PoC numbers from inside the engine.
- **P2 — navigation parity**: L4 — port the full §6 family; reach Tier‑A parity on the D=4 / zero‑free corpus.
- **P3 — parity harness**: `validation/parity_harness.py` sweeps **all experiments in all repos**, emits the diff‑class report.
- **P4 — feedback sweep**: run the harness corpus‑wide (Hs + HUF + RWA); collect Tier‑B improvements and any regressions; **likely surface new findings** (the bet — e.g., the lossless D>4 readings where the old engine was projecting lossily).
- **P5 — adjudicate**: resolve every divergence (improvement‑doc or fix); reconcile the conference numbers; write `PARITY_REPORT`.
- **P6 — archive**: only now move the old engine + superseded projects to a dated `_archive/`, leaving the oracle reachable and the parity report as the receipt.

Acceptance gate between P5 and P6 is hard: **no archiving until the parity report is green and every divergence is adjudicated.**

---

## 12 · Risks & open decisions

- **Scope creep** — mitigated by the v1 line (kernel + nav parity) and deferring twin/CHSH/diff‑geo. Hold the line.
- **`compute_helmsman_family` / `fit_attractor` internals** — defined in `hci_shared`; P2 must read them to port exactly (not yet harvested in this spec). Flagged for P1/P2.
- **Regime boundary metric** — oracle uses `mean + 2·std`; the corpus notes sometimes describe a MAD form. v4 reproduces the **code** (std) for parity; a MAD variant, if wanted, is a separate, flagged improvement — your call.
- **Conference‑number reconciliation** — the single most sensitive parity item; treat any divergence there as blocking until explicitly reconciled.
- **Open decisions — RESOLVED 2026-06-10 (Peter):** (a) engine name = **`HCI-CNTT v4.0.0`** (confirmed); (b) the differential‑geometry layer is **kept entirely out of v1** — revisited only if/when earned (one invariant defined and computed on real data), never in the canonical payload before then; (c) the feedback sweep (P4) is **Hs‑only first**, extended to HUF/RWA only after Hs‑corpus parity is green.
- **Engine Interop Registry (planned layer; see `ENGINE_INTEROP_REGISTRY.md`):** a version registry + per‑pair hash‑certified transforms above the engines so any v4+ engine can read any other engine's output (the original is readable, not a reader), making updates additive instead of orphaning. The **parity harness (P3) generates and certifies the transforms** — interop falls out of the planned work. Hard limit: transforms preserve information, never manufacture it (lossy‑up ⇒ `RE_RUN_FROM_SOURCE`, never faked). Per‑engine hashes stay independent (INV‑038); the registry is a layer on top.

---

## 13 · Claim tiers for this document

- **Tier 1 (verified):** the oracle's exact behaviors quoted here (read from `cnt.py`/`cnq.py` 2026‑06‑10); the tiling PoC numbers; the atan2 and lossless‑vs‑lossy facts.
- **Tier 2 (sound design):** the Tensor‑Train link architecture, the parity tiers, the port‑readiness seams.
- **Tier 3 (to earn in the build):** that v4 reaches full Tier‑A parity across the whole corpus; that the feedback sweep yields new findings; that the hierarchical atlas holds on real‑world (non‑synthetic) phylogenies.

*Source of truth on any conflict: `Hs/HS_FAST_REFRESH.json`. The instrument reads. The expert decides. The hashes carry the receipts.*
