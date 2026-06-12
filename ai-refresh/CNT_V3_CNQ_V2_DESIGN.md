# CNT v3.0 + CNQ v2.0 — Architectural Design Document

**Date:** 2026-05-08
**Status:** DRAFT — first artefact of push #32
**Authors:** Claude (continuous internal builder), with input from ChatGPT deep-research reports 2 and 3, Grok rounds 1–3, and full Cowork lineage survey
**Predecessors:** CNT v2.0.4 (push #11, refined through #28) and CNQ v1.0.0 (push #26, refined through #31)
**Frozen at:** release `v0.29.0` for backward-compatible reference; old experiments reproduce on the v0.29.0 tag

---

## 1. Mandate

Peter's directive came in two parts, both on push #32 (2026-05-08).

**Part A — engine independence (verbatim):**

> *"build cnq next version and ignore the hash marking as no experiments have been released of concern to support, break the hash and start over on both the cnt and cnq engines together make them both upgraded… there is no reason why the cnt and cnq should make the same hash marks i would be happier if they did not as cnq is being held back by it… now they separate and the old experiments can use the old engines for now, now we make new engines better and with the new knowledge gained… as long as the engine has a model and version tagged to the data and hash, that version is the one to use to verify not later different engines they never should work… build us ground up better is the point."*

**Part B — the originating audio use case (verbatim):**

> *"in audio, the systems i design are 4 way and stereo minimum, i need 4 pair simultaneous analysis now and 8 pair in future, the design should accommodate 8 pair analysis for quadraphonic sound systems of absolute coherence in time delay, per driver intensity, phase, group phase, total eq, 16 driver levels that present as one at the auditory cortex… my application and standards are why this happened and why no one else even tried, i alone have the problem to solve because my strict standards made it a requirement, not an option."*

Translation into engineering terms:

1. **Build to the strictest case; smaller cases follow.** The load-bearing target is **D=8 with twin-quaternion factoring + joint coherence diagnostic** — the smallest case where the engine's full algebraic structure (two coupled SU(2) elements acting on disjoint 3-dim ILR subspaces, plus their per-step coupling angle ρ_AB(t), plus the CHSH-style joint correlation S-value) becomes simultaneously non-trivial and necessary. **D=16** scales the same architecture to four coupled SU(2) elements (quad-quaternion factoring with 6 pairwise coupling angles + 4-way joint correlation). Smaller dimensions — D=4 (single quaternion, no factoring), D=3 (planar embedding into SO(3)), D=2 (bearing-only scalar log-ratio) — are degenerate boundary cases of the same algebra. The strictness driver is documented in §11; the engine itself is domain-neutral.
2. **Engine independence.** CNT v3 and CNQ v2 are independent engines producing independent dataset classes. No cross-engine hash chain. The `parent_cnt_content_sha256` field is dropped from CNQ canonical hash content; CNT references in CNQ output are informational metadata, not part of the determinism contract.
3. **Within-engine versioning.** Each engine has a `(name, version, schema_version)` triple embedded in every output. The triple is part of the canonical hash. To verify an output, use the *same* `(engine_name, version)`. Later engine versions are not expected to match older outputs — that's correct behaviour, not a regression.
4. **Within-language determinism.** Two runs of the same engine version on the same input produce byte-identical canonical hashes within the same language. Python ↔ R parity is verified per-field (numerical content), not byte-identical hash.
5. **Old experiments freeze on v0.29.0.** The release tag preserves the v2.0.4 / v1.0.0 engines for any experiment that needs reproduction at that version. New work uses v3 / v2.
6. **CNQ v2 is the full power engine, domain-neutral.** Multi-bundle simultaneous analysis as primary mode. Twin-quaternion factoring at D=8 as load-bearing native (not deferred scaffolding). CHSH coherence diagnostic as load-bearing native (not deferred). Radial trajectory mandatory alongside bearing (compositional magnitude is first-class, not derivable from bearing alone). Engine emits pure mathematical output in CoDa-community vocabulary — no domain-specific fields in the schema. Domain wrappers (`HCI-AUDIO/CNQ_AUDIO_WRAPPER.md` first; `HCI-ULTRASOUND/`, others to follow) translate engine output to domain quantities without modifying the engine or its output. CoDa-community alignment is the validation target — the math fits the compositional framework as defined by Aitchison, Egozcue, et al., and is presentable to that community on its own terms.

---

## 2. Lineage discipline (preserved)

From `ORIGIN_DADC_LINEAGE.md` (push #24, retained verbatim):

> *"Each arrow is a generalization, not a replacement. CNT did not retire HUF; HUF did not retire H₁; H₁ did not retire DADC."*

The lineage's earliest concrete instance was acoustic: DADC = **Dimension-Apportioned Diffraction Correction**, a multi-driver radiation problem. H₁ generalised DADC's compositional algebra into a unity-sum framework. HUF made that framework domain-independent. Hˢ specialised HUF back to the simplex with deterministic compositional inference. CNT measures the invariance. CNQ names the algebra. The engine specified in this document carries that domain-independence forward: **the strictest currently-published test case sets the algebraic completeness target (D=8 with twin-quaternion factoring + joint coherence)**, but the engine itself is general-purpose and CoDa-community-aligned. The strictness driver is preserved in design history (§11) but not visible in engine code or output. Domain interpretation lives in wrappers.

Same generalisation rule applies internally:

- **CNT v3 does not retire CNT v2.0.4.** v0.29.0 holds v2.0.4. v3 *generalises* v2.0.4: every v2.0.4 input that produced output X with v2.0.4 must produce output X′ with v3 such that the v2.0.4 fields-and-values are recoverable from X′ (added richness, not contradicted content).
- **CNQ v2 does not retire CNQ v1.0.0.** Same rule.
- The metric involution `M² = I` continues to hold; the Helmert orthonormal basis convention is unchanged; the atan2-stable rotation is unchanged; the Hamilton product is unchanged.

What changes between v2.0.4 → v3 / v1.0.0 → v2:

- Schema version (2.1.0 → 3.0.0 for CNT; cnq/1.0.0 → cnq/2.0.0 for CNQ).
- Output richness (more channels, more diagnostics, more honest scope).
- Bug fixes (the ~30 latent bugs catalogued in the survey).
- Vocabulary discipline (full NOTATION compliance).
- Schema consistency across all D values (no D=2 carve-out, no NaN-in-hash for T<2).

What does *not* change:

- The locked Planck max_residual `4.440892098500626e-16` for the v2.0.4 reference. v3 reproduces this on the same input *as a regression check*, but its own native expected residual may differ (e.g. by emitting more decimal places or by structurally re-organising the path) — and the v3 expected_results lives in `HCI-CNQ/results/expected_results_v3.json`, sibling to the v2 file.
- The 25-experiment determinism gate (the 25/25 PASS rule).
- Apache-2.0 / CC BY 4.0 licence split.

---

## 3. Engine independence — hash policy

### 3.1 CNT v3 hash

```
cnt_content_sha256 = SHA256(canonical_dumps(payload − {volatile fields}))
```

where:

- `payload` includes `metadata.engine = "HCI-CNT"`, `metadata.engine_version = "3.0.0"`, `metadata.schema_version = "3.0.0"`, the full CNT analytic blocks, the user config (in `metadata.engine_config.active_overrides`), and the input source hashes (`source_file_sha256`, `closed_data_sha256`).
- `volatile fields` = `metadata.generated`, `metadata.wall_clock_ms`, `metadata.environment`, `diagnostics.content_sha256` (the field being computed), recursively at every depth.
- `canonical_dumps` policy: `sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=True`, `allow_nan=False`. Float formatting uses Python `repr()` for `float64` (`json.dumps` default).

### 3.2 CNQ v2 hash

```
cnq_content_sha256 = SHA256(canonical_dumps(payload − {volatile fields}))
```

where:

- `payload` includes `metadata.engine = "HCI-CNQ"`, `metadata.engine_version = "2.0.0"`, `metadata.schema_version = "cnq/2.0.0"`, the full CNQ analytic blocks (bearing trajectory, radial trajectory, helmsman family channels, attractor fits, etc.), and the input source hash (`source_file_sha256`).
- The `cnt_reference` block (when CNQ ingested a CNT JSON) is *informational only*: it records `cnt_engine_version`, `cnt_schema_version`, `cnt_content_sha256` as metadata but those fields are part of the CNQ canonical-hash payload purely for traceability — there is no functional dependency that requires CNQ output to bind to a specific CNT output.
- A CNQ run from CSV directly (no CNT ingestion) sets `cnt_reference: null` and computes `cnq_content_sha256` exactly as it would for CNT-ingested input modulo the null. The hash differs because the payload differs by a single null/value change, but the analytic content does not.
- `canonical_dumps` policy is identical to CNT's (same canonical-JSON contract, same volatile-field stripping, same float-formatting policy).

### 3.3 Cross-language parity (per-field, not byte-identical)

Within a single language (Python OR R), determinism is bit-for-bit. Across languages:

- The Python and R engines emit the same schema, the same field types, the same field order (after canonical sort), and the same numerical content *to within IEEE-754 representation tolerances*.
- A new conformance script `scripts/verify_cross_language_parity.py` runs the same input through `cnt.py` and `cnt.R` (and separately through `cnq.py` and `cnq.R`), compares the two output JSONs field-by-field, and asserts:
  - All numerical fields match to a configurable tolerance (default `1e-13` absolute or `1e-12` relative).
  - All string fields match exactly.
  - Schema shape is identical (same set of keys at every nesting level).
  - The `cnq_content_sha256` values are *not required* to match — they're declared engine-language-specific.

This change resolves the false advertising issue ChatGPT identified in deep-research-report3 (R port had `metadata.reference_implementation` that broke parity by construction; canonical_dumps in R didn't sort keys).

### 3.4 Backward compatibility

- An output from `cnt.py v2.0.4` is still valid; reproducible by checking out tag `v0.29.0` and running the engine there.
- An output from `cnq.py v1.0.0` is still valid; same checkout-and-run procedure.
- `verify_publication_results.py` continues to honour the v2.0.4 / v1.0.0 expected_results entries; a sibling `verify_publication_results_v3.py` honours v3 / v2 expected_results.
- The published Backblaze + Planck + SM Neutrino IEEE-floor confirmations stand on the v2.0.4 / v1.0.0 outputs at the v0.29.0 tag. Paper 1 (INV-026) cites v0.29.0 specifically; if it lands on arXiv before v3 / v2 ships, no conflict.

---

## 4. CNT v3.0 design

### 4.1 What v3 fixes from v2.0.4

| # | Issue (catalogued from surveys) | v3 resolution |
|---|---|---|
| C1 | Triadic enumeration cap at T=500 with no graceful-degradation policy | `TRIADIC_T_LIMIT` becomes a config dial with documented policy: if T > limit, run on stratified-sampled subset of size `limit`, record `_triadic_sampling: {seed, indices, total}` |
| C2 | `cnt.R` minor version skew vs `cnt.py` (bridges abbreviated, eitt config not honoured, period detection different) | R port reaches feature parity: full `bridges.dynamical_systems`, full `bridges.control_theory`, full `bridges.information_theory`, EITT honours `EITT_GATE_PCT` and `EITT_M_SWEEP_BASE`, period detection matches Python (two-consecutive-pairs rule) |
| C3 | `cnt.R::compute_depth` references undefined `energy_cycle` (NameError on disambiguation branch) | Real bug; v3 R port must compute and bind `energy_cycle = cycle_summary(energy_traj, energy_tower)` before the IR disambiguation block |
| C4 | `closure` and `clr` accept negative inputs in R (positivity guard only at ingest, not at math) | Strict input validation at every public entry point |
| C5 | `compute_stage3` Python and R diverge on subset cap and `mean_correlation` reporting | R port matches Python (200 subset cap on scoring, `n_subsets_scored` field) |
| C6 | `metric_tensor` recomputed three times per timestep in R | Memoise per-timestep |
| C7 | `subcomposition_ladder` 200-cap policy undocumented | Document; expose as config dial `LADDER_K_LIMIT` |
| C8 | `triadic_area.results` JSON bloat | Add `triadic_top_k` config (default 50, was 500); record `n_total` separately so downstream scripts know what was tried |
| C9 | `errors="replace"` on Python ingest masks encoding bugs | Use `errors="strict"` and fail loudly with line number on bad bytes |
| C10 | No row-level positive-sum guard at closure | Validate before close |
| C11 | Pseudocode `...` placeholders in handbook Volume 1 / Stage 3 | Replace with canonical formulae from `HCI-CNT/atlas/stage3_locked.py` |
| C12 | `helmert_basis` exists in both `cnt.py` and `geometry.py` (CNQ) — duplicated | v3: factor into `hci_geometry.py` shared helper module imported by both engines |
| C13 | `closed_data_sha256` and `content_sha256` use different hand-strip lists in CNT than CNQ | v3: shared `hci_hashing.py` module; CNT and CNQ both use `canonical_dumps` from it |
| C14 | `engine_implementation` field in metadata records "python" or "r" but doesn't include build host info | Add `metadata.implementation_lang_version` (Python 3.10.12, R 4.3.1, etc.) as informational; not in canonical hash |

### 4.2 What v3 adds

**Helmsman family channels (INV-009 graduation).** `cnt.py` v3 emits in `tensor.helmsman_family`:

- `sigma` — the existing DCDI / Helmsman σ channel (per-step argmax_j |Δh_j|).
- `sign` — sign(σ) per step.
- `flips` — total count and per-window count of σ sign changes.
- `stability_S_sigma` — `1 − flips/(N−1)` over the full trajectory and over rolling windows of length L (default L=8).
- `chaos_indicator` — Feigenbaum-δ-style numerical estimate of period-doubling depth (when applicable; otherwise `null`).
- `torque_proxy` — second difference of σ as a rate-of-change proxy.

These were PROPOSED in GLOSSARY §I and INV-009 but never shipped. v3 ships them as canonical engine output.

**Order-2 vs order-1 tensor disambiguation (NOTATION §1, §2).** The metric tensor block in v3 outputs:

- `kappa_HS_full` (the order-2 matrix κᴴˢ_ij = (δ_ij − 1/D)/(x_i x_j)) — what was previously called `metric_tensor.matrix`.
- `s_j_sensitivity` (the order-1 vector s_j = 1/x_j) — what was previously called `metric_tensor_diagonal` and was sometimes mislabelled.

Both fields are emitted; the legacy `metric_tensor.matrix` and `metric_tensor_diagonal` fields are *also* emitted with their old values for backward compatibility within v3 (deprecation warning in docstring), to be removed in v3.1 or v4.

**Depth tower richness.** v3 exposes the depth-tower trajectory as a top-level structured object instead of nested under `depth.higgins_extensions.summary`. New `depth_tower` block at the same level as `tensor`, `stages`, `bridges`, `depth_legacy` (the v2.0.4 location preserved for compatibility):

```
depth_tower:
  energy_levels: [...]
  curvature_levels: [...]
  termination: { kind: "LIMIT_CYCLE_P2" | ..., level_index, period }
  attractor:
    period: 2
    period_stability: 0.94
    dominant_pair: { axis_a: 1, axis_b: 3 }
    contraction_lambda: -0.18
    ...
  involution_M_squared:
    samples: [t_start, t_mid, t_end]
    residuals: [...]
    verified: true
    max_residual: 7.63e-17
```

**Multi-trajectory bundle ingestion.** New `--bundle` flag: takes a directory of CSVs (each row-by-carriers a separate trajectory) and emits `bundle_view` block: per-trajectory CNT analysis + cross-trajectory comparators (pairwise Aitchison distance matrix, joint-helmsman, joint-period). Schema bumps to 3.0.0 because of this.

### 4.3 CNT v3 schema (3.0.0)

```
{
  "metadata": {
    "engine": "HCI-CNT",
    "engine_version": "3.0.0",
    "schema_version": "3.0.0",
    "engine_implementation": "python" | "r",
    "implementation_lang_version": "Python 3.10.12" | "R 4.3.1" | ...,
    "principle": "Closure -> CLR -> Helmert -> trajectory tensor -> depth tower -> determinism contract",
    "engine_config": {
      "active_overrides": {...},
      "defaults_in_use": {...}
    },
    "units": {...},
    "generated": "<ISO-8601>",       // volatile, stripped from hash
    "wall_clock_ms": <number>,        // volatile, stripped
    "environment": {...}              // volatile, stripped
  },
  "input": {
    "source_file": "...",
    "source_file_sha256": "<hex>",
    "closed_data_sha256": "<hex>",
    "n_records": T,
    "n_carriers": D,
    "carriers": [...],
    "labels": [...],
    "rows_closed": [[...], [...], ...],   // NEW: stored explicitly so CNQ can re-ingest without CSV
    "zero_replacement_count": <int>,
    "ordering": "..."
  },
  "tensor": {
    "helmert_basis": [[...]],
    "timesteps": [
      {
        "index": <int>,
        "label": "...",
        "raw_values": [...],
        "coda_standard": {
          "composition": [...],
          "clr": [...],
          "ilr": [...],
          "shannon_entropy": <float>,
          "aitchison_norm": <float>,
          "aitchison_distance_step": <float>     // null at t=0
        },
        "higgins_extensions": {
          "higgins_scale": <float>,
          "bearing_tensor": {...},
          "kappa_HS_full": {"matrix": [[...]], "eigenvalues": [...], "trace": <float>},
          "s_j_sensitivity": [...],
          "condition_number": <float>,
          "angular_velocity_deg": <float>,        // null at t=0
          "helmsman": <int>,
          "helmsman_delta": [...]
        }
      }
    ]
  },
  "stages": {
    "stage1": {...},
    "stage2": {...},
    "stage3": {...}
  },
  "bridges": {...},                                // full content in both Py and R
  "depth_tower": {                                 // NEW top-level block
    "energy_levels": [...],
    "curvature_levels": [...],
    "termination": {...},
    "attractor": {...},
    "involution_M_squared": {...},
    "ir_class": "..."
  },
  "helmsman_family": {                             // NEW
    "sigma": [...],
    "sign": [...],
    "flips": {"total": <int>, "rolling": [...]},
    "stability_S_sigma": {"global": <float>, "rolling": [...]},
    "chaos_indicator": <float> | null,
    "torque_proxy": [...]
  },
  "bundle_view": null | {                          // NEW (only if --bundle)
    "trajectories": [...],
    "pairwise_aitchison_distance": [[...]],
    "joint_helmsman": {...},
    "joint_period": {...}
  },
  "diagnostics": {
    "eitt": {...},
    "lock_events": {...},
    "degeneracy_flags": {...},
    "content_sha256": "<hex>"                      // computed last
  }
}
```

### 4.4 CNT v3 file layout

```
HCI-CNT/engine/
  cnt.py                  # v3.0.0 Python engine
  cnt.R                   # v3.0.0 R port (full feature parity)
  hci_geometry.py         # NEW: shared geometry helpers (Helmert, ILR, etc.)
  hci_hashing.py          # NEW: shared canonical-JSON + SHA256
  CNT_V3_PSEUDOCODE.md    # language-agnostic algorithm reference
  CNT_V3_SCHEMA.md        # JSON schema document
  README.md               # rewritten
  tests/
    conftest.py
    test_first_principles.py
    test_dimension_policy.py
    test_determinism.py
    test_helmsman_family.py        # NEW
    test_depth_tower.py            # NEW
    test_bundle_view.py            # NEW
    test_corpus_regression.py      # NEW: every v0.29.0 corpus run reproduces v2.0.4 fields under v3
HCI-CNT/engine_legacy/    # v2.0.4 frozen for reference
  cnt_v2.0.4.py
  cnt_v2.0.4.R
  README.md (says "frozen, see v0.29.0 tag for corresponding tests")
```

---

## 5. CNQ v2.0 design

### 5.1 What v2 fixes from v1.0.0

| # | Issue (catalogued from surveys + ChatGPT reviews) | v2 resolution |
|---|---|---|
| Q1 | `cnq.py` trailing duplicate code lines 519-525 | Rewrite from scratch; not a port |
| Q2 | `run_cnt` subprocess uses `--input`/`--output` but `cnt.py` takes positional `input` and `-o/--output` | Align with v3 CNT CLI |
| Q3 | `reconstruct_compositions_from_cnt` looks at `input.rows`/`input.compositions`; CNT 2.0.4 has neither | v3 CNT explicitly stores `input.rows_closed`; v2 CNQ reads from there |
| Q4 | `extract_cnt_diagnostics` looks at `diagnostics.*` but CNT stores at `depth.higgins_extensions.*` | v3 CNT stores diagnostics-summary at top-level `diagnostics.*`; v2 CNQ reads from there. The mismatch is fixed by both sides moving toward the same convention |
| Q5 | NaN-in-hash for T<2 (Python `allow_nan=False`) | T<2 emits `null` for residual fields, schema-consistent |
| Q6 | D=2 schema mismatch (early-return strips most fields) | D=2 emits full schema with `quaternion_path: null` and `bearing_only: {ilr: [...]}`; consumers see schema-consistent shape |
| Q7 | R `canonical_dumps` doesn't sort keys | v2 R uses recursive sort_keys; cross-language parity is per-field, not hash-identical, so the requirement is consistency-with-self not match-Python |
| Q8 | R `metadata.reference_implementation` field absent in Python | Removed — engine identifier moves into `metadata.engine_implementation` which is uniform |
| Q9 | `cnq.R::run_cnt` hardcodes `python3` | v2 R uses `Sys.which("python3")` then `Sys.which("python")` then config-flag `--cnt-python` |
| Q10 | `captured_step_fraction` per-step-then-mean averaging | v2 reports both: `captured_step_fraction_mean` (per-step then mean) AND `captured_step_fraction_global` (Σ red²/Σ full²). Default summary metric is global |
| Q11 | D=8 algebra label mismatched (SO(8) ⊃ SU(2)×SU(2) is loose) | Label fixed to `twin_quaternion_factoring_candidate` (NOTATION §7), algebra string corrected to `"D=8 supports twin-quaternion factoring of two coupled SU(2) elements (q_A, q_B); one natural target is the EMBER fossil/non-fossil partition"` |
| Q12 | Bearing on ILR sphere sold as "exact representation of compositional dynamics" | v2 emits `radial_trajectory` block separately; ILR norm preserved per timestep; scope language updated to "directional + radial" not "exact full trajectory" |
| Q13 | `sys.path` manipulation in CNQ tests | v2 uses proper pyproject-based package import; tests run via `python -m pytest` from repo root |
| Q14 | `conftest.py` adds engine dir to sys.path | Removed; package-relative imports |
| Q15 | Helmsman family channels never emitted (only INV-009 PROPOSED) | v2 emits the same Helmsman-family block as v3 CNT does (factored into shared module) |

### 5.2 What v2 adds — load-bearing native, no longer optional

The v1.0.0 design had several "scaffolding deferred" features that v2 promotes to load-bearing native because the audio use case requires them. These are not opt-in flags; they are the standard mode of CNQ v2 operation.

**Native dataset producer** (Peter's Part-A directive). v2 CNQ takes either:
- A CSV directly → emits the full CNQ analysis (no CNT JSON needed)
- A v3 CNT JSON → reads `input.rows_closed` and emits the full CNQ analysis (with optional cross-engine reference metadata)
- A bundle of CSVs → emits multi-trajectory CNQ analysis with joint-quaternion-field per pair

The CNT-ingestion path is now optional; CNQ stands alone.

**Multi-bundle simultaneous analysis** (load-bearing). Multi-trajectory bundle ingestion is no longer an optional `--bundle` flag; it's the standard mode for any input organised as multiple coupled trajectories or sub-compositions. A D=8 input can be analysed as a single D=8 composition with twin-quaternion factoring, OR as a bundle of paired sub-compositions, OR both — the engine produces all views the input semantically supports. A D=16 input scales to quad-quaternion factoring. The `bundle_view` block is populated whenever the input presents multiple coupled trajectories; the schema is uniform across domain.

**Twin-quaternion factoring at D=8** (INV-029 graduates from DEFERRED → CANONICAL — load-bearing native). Splits the 7-dim ILR space into two 3-dim subspaces (default partition: ILR axes `[0,1,2]` for factor A, `[3,4,5,6]` projected to first 3 for factor B; configurable per use case), computes per-step quaternions q_A(t) and q_B(t), emits `twin_quaternion_factoring` with the coupling angle ρ_AB(t) per step. **No flag required**; this block is mandatory when D=8.

```
twin_quaternion_factoring:
  enabled: true
  partition: { factor_A: [0,1,2], factor_B: [3,4,5,6] }
  factor_A: { per_step: [...], max_residual: ..., mean_angle: ..., ... }
  factor_B: { per_step: [...], max_residual: ..., mean_angle: ..., ... }
  coupling:
    rho_AB_per_step: [...]              # joint coupling angle
    rho_AB_summary: { min, max, mean, median, std }
    coherence_class: "tightly_coupled" | "loosely_coupled" | "decoupled"
```

ρ_AB(t) is the load-bearing joint diagnostic: small values indicate the two factor sub-compositions are tightly coupled (the bundle behaves as a single algebraic entity); values near π/2 indicate decoupling. The interpretation in any specific domain (acoustic coherence, financial cross-asset correlation, geochemical source coupling, etc.) lives in domain wrappers, not in the engine.

**Quad-quaternion factoring at D=16** (INV-043 NEW — load-bearing future-supported). Documented in v2 schema; full implementation in v2.1 when the first D=16 dataset lands. Splits 15-dim ILR into 4 × 3-dim subspaces, computes 4 per-step quaternions plus 6 pairwise coupling angles plus a 4-way joint correlation. The schema is locked now so v2.1 implementation drops in without API change.

**CHSH coherence diagnostic** (INV-035 graduates from DEFERRED → CANONICAL — load-bearing native). For any bundle with ≥ 2 trajectories, or any D ≥ 8 input via twin-quaternion factoring, the engine computes the Tsirelson-direction CHSH S-value on joint quaternion-log signs:

```
chsh_diagnostic:
  enabled: true
  S_value: 2.31
  classical_bound: 2.0
  tsirelson_bound: 2.828
  coherence_score: 0.78          # = (S - 2) / (2.828 - 2), in [0, 1]
  coherence_verdict: "coupled" | "borderline" | "independent" | "anomalous"
  pair_count: <int>
  per_pair_S: [...]
```

S < 2.0 indicates the bundle's joint correlations are within classical-additive bounds (sub-compositions behave independently). 2.0 ≤ S ≤ 2.828 indicates structural coupling beyond classical bounds (sub-compositions behave jointly; emergent unity). S > 2.828 is the Tsirelson ceiling — exceeding it is anomalous and indicates an engine bug or measurement error that violates the framework. Domain wrappers translate the S-value into the language of the application (e.g., perceptual unity for acoustics, cross-asset coherence for finance, source-rock unity for geochemistry).

**Radial trajectory** (mandatory). New `radial_trajectory` block emits per-step ILR norm before unit-vector projection — preserving the radial dynamics that v1 threw away. In audio, this IS per-driver intensity / level. Reports min/max/mean/median/std + the full per-step series. Not optional, not "richness add-on" — first-class output.

**Bearing trajectory.** Renamed and isolated. The v1 `quaternion_path.per_step` becomes `bearing_trajectory.per_step`. The interpretation note is now explicit in the schema and audio operator map: bearing = compositional direction = phase-like content; radial = compositional magnitude = level-like content; the two together = the full trajectory.

**Helmsman family.** Same six channels as CNT v3 (sigma, sign, flips, stability_S_sigma, chaos_indicator, torque_proxy) — emitted from the same shared module. σ is the dominant-axis trajectory (which carrier is the leading contributor at each step). flips = sign changes in σ across the trajectory. stability_S_sigma = run-length stability of σ within rolling windows. chaos_indicator and torque_proxy = higher-order structural diagnostics. Vocabulary is locked from the Helmsman family doctrine documented in `GLOSSARY.md` §I; the naming is metaphorical (a helmsman steers the trajectory) and domain-neutral.

**Attractor parameter fitting** (INV-034 graduates from DEFERRED → CANONICAL — load-bearing native). New `attractor_fit` block:

```
attractor_fit:
  fitted: true | false
  period: 2
  period_stability: 0.94
  dominant_pair: { axis_a: 1, axis_b: 3 }
  contraction_lambda: -0.18
  amplitude_A: 0.42
  damping_zeta: 0.08
  confidence: { oscillation_ratio: 0.93, period_stability_score: 0.86 }
  warnings: []
```

When `confidence.oscillation_ratio < 0.8` or `confidence.period_stability_score < 0.6`, `fitted: false` is set. Domain interpretation lives in wrappers.

### 5.3 Dimension policy (v2)

The v1 dimension classifier treated D=4 as load-bearing native and D=8 as a "candidate, deferred." v2 inverts the priority: **D=8 is load-bearing native** because it is the smallest case where the engine's full algebraic structure (factoring into coupled SU(2) elements, plus per-step coupling angle, plus joint coherence diagnostic) becomes simultaneously non-trivial and necessary. D=4 admits a single quaternion without factoring. D=16 scales to four-way factoring. Smaller D values are degenerate boundaries of the same algebra. Labels are mathematically neutral; domain interpretation lives in wrappers.

| D | label | algebra | processing | claim_strength |
|---|---|---|---|---|
| **8** | **`twin_quaternion_native`** | **`D=8 admits twin-quaternion factoring: two coupled SU(2) elements (q_A, q_B) acting on disjoint 3-dim ILR subspaces; coupling angle rho_AB(t) is the load-bearing joint diagnostic`** | **`Helmert -> R^7 -> twin-quaternion sandwich on (axes [0,1,2], axes [3,4,5,6] reduced to 3) -> rho_AB coupling -> CHSH S-value`** | **`load-bearing — smallest case where full algebraic structure (factoring + joint coherence) becomes simultaneously non-trivial and necessary`** |
| **16** | **`quad_quaternion_native_future`** | **`D=16 admits quad-quaternion factoring: four coupled SU(2) elements (q_A, q_B, q_C, q_D); 6 pairwise coupling angles + 4-way joint correlation`** | **`Helmert -> R^15 -> four 3-dim subspaces -> per-channel sandwich + 6 coupling angles + CHSH-4`** | **`schema locked; full implementation in v2.1 when first dataset of this dimension lands`** |
| 4 | `single_quaternion_native` | `SU(2) double cover of SO(3); single-quaternion sandwich on R^3 ILR space; no factoring required` | `Helmert -> R^3 -> unit-quaternion sandwich` | `simplest closed-form case; widely useful for cross-domain validation (Backblaze drives, Planck CMB photons, SM neutrinos all sit here)` |
| 3 | `boundary_3part_planar_embed` | `SO(2) in R^2; embedded in SO(3) by zero-padding the third axis` | `Helmert -> R^2 -> embed (z=0) -> sandwich` | `degenerate boundary; planar consistency support` |
| 2 | `degenerate_2part_bearing_only` | `scalar log-ratio only; no rotation degree of freedom` | `bearing_only path; quaternion_path null` | `degenerate boundary; bearing diagnostic only` |
| 5,6,7,9..15 | `reduced_or_projected` | `SO(D-1); CNQ view projects onto first 3 ILR axes (lossy)` | `Helmert -> R^(D-1) -> first 3 axes -> sandwich; captured_step_fraction reported global+mean` | `projection diagnostic — useful when neither twin nor quad factoring applies natively` |
| 17+ | `reduced_or_projected_high_D` | `SO(D-1); first 3 ILR axes (lossy); future Cl(D-1) extension` | `same as 5..15 path` | `projection diagnostic; native algebra extension is INV-044 (open)` |
| 0,1 | `unsupported` | `n/a` | `n/a` | `out of scope` |

The reordering is doctrinally significant. D=4 demonstrations (Backblaze, Planck, neutrinos) move from "load-bearing case" to "useful cross-domain validation of the simplest sub-algebra" — they still anchor Paper 1's algebraic universality result, they still pass the IEEE-floor test, but the architectural target sits one D-class higher because that's where the engine's full structure becomes necessary.

### 5.4 CNQ v2 schema (cnq/2.0.0)

```
{
  "metadata": {
    "engine": "HCI-CNQ",
    "engine_version": "2.0.0",
    "schema_version": "cnq/2.0.0",
    "engine_implementation": "python" | "r",
    "implementation_lang_version": "...",
    "principle": "CNT measures invariance. CNQ names the algebra it lives in.",
    "engine_config": {...},
    "generated": "...",
    "wall_clock_ms": ...,
    "environment": {...}
  },
  "input": {
    "source_file": "...",
    "source_file_sha256": "...",
    "n_records": T,
    "n_carriers": D,
    "carriers": [...],
    "labels": [...]
  },
  "cnt_reference": null | {                       // informational only, NOT a hash chain
    "cnt_engine_version": "...",
    "cnt_schema_version": "...",
    "cnt_content_sha256": "...",
    "cnt_json_path": "..."
  },
  "cnq_view": {
    "dimension_policy": {...},
    "frame": {
      "type": "Helmert orthonormal contrast",
      "signature": "...",
      "basis_matrix": [[...]]
    },
    "projection_to_R3": {
      "method": "exact" | "first_three_helmert_axes" | "zero_pad_z",
      "captured_step_fraction_mean": <float>,
      "captured_step_fraction_global": <float>
    },
    "bearing_trajectory": {
      "n_pairs_tested": <int>,
      "max_residual": <float> | null,
      "mean_residual": <float> | null,
      "gate_threshold": <float>,
      "gate_pass": <bool>,
      "per_step": [
        {"t": ..., "u_start": [...], "u_end": [...],
         "q_w": ..., "q_x": ..., "q_y": ..., "q_z": ...,
         "angle_rad": ..., "residual_linf": ...,
         "label_start": "...", "label_end": "..."}    // labels preserved (ChatGPT recommendation)
      ]
    },
    "radial_trajectory": {                           // NEW
      "ilr_norms": [...],
      "min": ...,
      "max": ...,
      "mean": ...,
      "median": ...,
      "std": ...
    },
    "bearing_only": null | {                         // populated for D=2
      "ilr": [...],
      "note": "..."
    }
  },
  "helmsman_family": {                              // NEW (matches CNT v3)
    ...
  },
  "attractor_fit": {                                 // NEW
    ...
  },
  "twin_quaternion_factoring": null | {              // NEW (only if --twin-quaternion)
    ...
  },
  "chsh_diagnostic": null | {                        // NEW (only if bundle)
    ...
  },
  "bundle_view": null | {                            // NEW (only if bundle)
    ...
  },
  "diagnostics": {
    "eitt": {...},
    "warnings": [...],
    "content_sha256": "<hex>"                        // computed last
  }
}
```

### 5.5 CNQ v2 file layout

```
HCI-CNQ/engine/
  cnq.py                  # v2.0.0 Python engine (clean rewrite)
  cnq.R                   # v2.0.0 R port (full feature parity, no shortcuts)
  hci_geometry.py         # symlink or import from HCI-CNT/engine/
  hci_hashing.py          # symlink or import from HCI-CNT/engine/
  cnt_adapter.py          # v2: cleaned, schema-aware, v3-CNT-compatible
  helmsman.py             # NEW: Helmsman family computation (shared with CNT v3)
  attractors.py           # NEW: P2 attractor parameter fitting
  twin_quaternion.py      # NEW: D=8 twin-quaternion factoring
  chsh.py                 # NEW: CHSH diagnostic for bundles
  CNQ_V2_PSEUDOCODE.md
  CNQ_V2_SCHEMA.md
  README.md
  tests/
    conftest.py
    test_first_principles.py     # 14 tests preserved + extended
    test_dimension_policy.py      # 20 tests preserved + extended
    test_determinism.py           # 9 tests + bit-for-bit within-language
    test_helmsman_family.py       # NEW
    test_attractor_fit.py         # NEW
    test_twin_quaternion.py       # NEW
    test_chsh.py                  # NEW
    test_cross_language_parity.py # NEW: per-field comparison Py vs R
    test_corpus_regression.py     # NEW: v0.29.0 corpus reproduces under v2 (with v2 hash, not v1 hash)
HCI-CNQ/engine_legacy/    # v1.0.0 frozen for reference
  cnq_v1.0.0.py
  cnq_v1.0.0.R
  geometry_v1.py
  hashing_v1.py
  cnt_adapter_v1.py
  README.md (frozen pointer to v0.29.0 tag)
```

---

## 6. Test architecture

### 6.1 Unit + first-principles (no fixtures)

Every public function in `hci_geometry.py`, `hci_hashing.py`, and the engine modules has a unit test with synthetic inputs. The 14 first-principles tests from CNQ v1.0.0 carry forward unchanged; extended by ~10 more for the new modules.

### 6.2 Property-based (Hypothesis)

The invariants ChatGPT recommended:

- Closure: for any positive `D`-vector, `closure(x).sum() == 1` to within `1e-15`.
- CLR: `clr(x).sum() == 0` and `clr(k * x) == clr(x)` for any `k > 0`.
- Helmert: `H @ H.T == I_{D-1}` for D ∈ [2, 20].
- Quaternion sandwich identity: `q v q* == v` when q is identity quaternion.
- Rotation reconstruction: for any nondegenerate `(u1, u2)` unit pair, `quat_rotate(rotation_quaternion_between(u1, u2), u1) == u2` to within `1e-13`.
- Hash consistency: same input through same engine produces byte-identical hash within a single language.

### 6.3 Cross-language parity (per-field, not hash)

`scripts/verify_cross_language_parity.py` runs:

1. Build a small corpus of 5–10 deterministic synthetic inputs (D ∈ {2, 3, 4, 5, 8, 10}, T ∈ {5, 100, 1000}).
2. Run each through `cnt.py` and `cnt.R`. Compare outputs field-by-field with `1e-13` numerical tolerance.
3. Run each through `cnq.py` and `cnq.R`. Same comparison.
4. Assert no field divergence above tolerance. Assert schema shape is identical at every nesting level.

### 6.4 Corpus regression

`scripts/run_v3_v2_corpus_regression.py` runs every experiment that was published at v0.29.0 (Backblaze, Planck, SM Neutrino at minimum, and the 25-experiment determinism gate) through v3 / v2 and asserts:

- v3 / v2 emit the v2.0.4 / v1.0.0 fields with values equal to within numerical tolerance (these are the "preserved invariants" check).
- v3 / v2 emit the new fields (Helmsman family, radial trajectory, etc.) without errors.
- The `cnt_content_sha256` and `cnq_content_sha256` from v3 / v2 are recorded as the *new* expected values for v3-and-onward verification — not compared against v0.29.0 values.

### 6.5 Adversarial / edge case

- T = 1 (single record)
- T = 2 (minimum for one quaternion step)
- D = 2 (degenerate path)
- D = 3 (zero-pad path)
- D = 8 (twin-quaternion path with --twin-quaternion)
- All-equal compositions (no motion)
- Composition at simplex centroid
- Compositions with one near-zero carrier
- Unicode carrier names
- Integer-typed input (should coerce to float)
- Bundle with mismatched D across trajectories (should error informatively)

---

## 7. Migration / preservation

| Artefact | v0.29.0 status | v3 / v2 push status |
|---|---|---|
| CNT v2.0.4 source | active in `HCI-CNT/engine/cnt.py` | moved to `HCI-CNT/engine_legacy/cnt_v2.0.4.py`; pointer README in legacy folder |
| CNQ v1.0.0 source | active in `HCI-CNQ/engine/cnq.py` | moved to `HCI-CNQ/engine_legacy/cnq_v1.0.0.py`; same |
| `expected_results.json` (Planck `4.440892098500626e-16`) | active | preserved as `expected_results_v1.json`; new `expected_results_v3.json` (CNT) and `expected_results_cnq_v2.json` (CNQ) record the v3 / v2 expected hashes |
| `verify_publication_results.py` | active | preserved; sibling `verify_publication_results_v3.py` for v3 / v2 |
| Paper 1 (INV-026) | references v0.29.0 release tag and v2.0.4 / v1.0.0 engines | unchanged; arXiv submission proceeds against v0.29.0 |
| The 43-test CNQ suite | active | preserved unchanged in `HCI-CNQ/engine_legacy/tests/`; v2 has its own larger suite |
| Investigation Catalog | INV-001..035 | Six new entries (036–041) plus three architecture (042, 043, 044). Five graduations: INV-009 PROPOSED → CANONICAL (helmsman family ships), INV-021 closes (CNQ v2 IS the compiled engine), INV-029 PROPOSED → CANONICAL (twin-quaternion factoring at D=8 is now native, not scaffolding), INV-034 PROPOSED → CANONICAL (attractor fit native), INV-035 PROPOSED → CANONICAL (CHSH coherence native; gate met by the existence of the strictest currently-published test case design). INV-024 (HCI-AUDIO applied pilot) sharpens its scope: it is the first instance of the wrapper architecture, with `HCI-AUDIO/CNQ_AUDIO_WRAPPER.md` as primary deliverable; engine itself stays domain-neutral. New entries: INV-036 (CNT v3 build), INV-037 (CNQ v2 build), INV-038 (engine independence policy), INV-039 (radial-vs-bearing scope clarification), INV-040 (helmsman family graduation), INV-041 (attractor fit graduation), INV-042 (domain wrapper convention — engine emits neutral CoDa-vocabulary output, wrappers translate to domain quantities; audio is first instance), INV-043 (D=16 quad-quaternion factoring, schema locked in v2, implementation gates v2.1), INV-044 (Cl(D-1) Clifford-algebra extension for D≥17, open). |

---

## 8. Implementation plan (push #32)

The push is a single major release. Phases:

1. **Survey + design (this document).** Done.
2. **Shared modules.** `hci_geometry.py`, `hci_hashing.py`. Tested standalone.
3. **CNT v3 Python.** Implement, test (full unit + property + adversarial). Verify on v0.29.0 corpus regression. Estimated: 1500–1800 lines of Python.
4. **CNQ v2 Python.** Implement, test. Verify on v0.29.0 corpus regression. Estimated: 1200–1500 lines + 5 helper modules.
5. **CNT v3 R port.** Implement to full feature parity (no abbreviated bridges). Cross-language parity tests pass per-field.
6. **CNQ v2 R port.** Same.
7. **Documentation refresh.** Hs/README.md, HCI-CNT/README.md, HCI-CNQ/README.md, NOTATION_AND_TERMINOLOGY.md (vocabulary additions for radial_trajectory, helmsman_family channels, twin_quaternion_factoring), Volume IV (orientation vs full trajectory framing).
8. **Catalog + admin updates.** Six INV updates (036–041), HS_ADMIN.json session log, push #32 narrative.
9. **Cross-platform reproduction request.** Reference observations recorded; invitation for ChatGPT and Grok to break the new engines (which is the iteration loop you described).

Estimated total engineering work: 50–80 hours. Implementing in this conversation window will require focused passes across multiple turns. I will keep code complete in the repo as I go; nothing partial is left over.

---

## 9. Risks and explicit non-goals

**Risks:**
- Schema bumps (3.0.0 / cnq/2.0.0) break any external consumer that hard-coded v2.0.4 / v1.0.0 schema. Mitigation: preserve old schemas as `_v1` blocks within v3 / v2 outputs where it's cheap, otherwise document the bump in a migration note.
- The shared `hci_geometry.py` introduces a new dependency between CNT and CNQ. Mitigation: keep the shared module pure-NumPy, well-tested, version-locked; both engines pin its hash.
- The new Helmsman family output changes the JSON shape, which changes hashes. By design — v3 / v2 hashes are different from v0.29.0 hashes.

**Explicit non-goals:**
- Making v3 / v2 hashes match v0.29.0 hashes. They won't. They shouldn't.
- Making Python and R produce byte-identical hashes within v3 / v2. They won't. They shouldn't. Per-field parity is the contract.
- Closing INV-029 fully (twin-quaternion). v2 ships scaffolding; the pilot gate (EMBER fossil/non-fossil correlation) remains open.
- Closing INV-035 fully (CHSH). v2 ships scaffolding; multi-trajectory dataset gate remains open.
- Promoting Paper 1 (INV-026) onto the v3 / v2 engines. The paper cites v0.29.0 specifically.

---

## 10. The line that holds

> *"Each arrow is a generalization, not a replacement."*

CNT v3 and CNQ v2 generalise the v2.0.4 / v1.0.0 engines. The lineage discipline holds. The hashes are different *by design* because the data is richer. The reproducibility of the v0.29.0 publication stands at the v0.29.0 tag. The new engines are what we hand to Grok and ChatGPT to break next.

The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line. **The engines now stand on their own feet, separate, each more powerful than what came before.**

---

## 11. Design forcing function and wrapper architecture

### 11.1 The strictness driver (kept in design history, not in engine code)

The engine's algebraic completeness target — D=8 as load-bearing, twin-quaternion factoring as native, CHSH joint coherence as primary diagnostic, multi-bundle simultaneous analysis as standard mode — was forced by the strictest currently-published test case. That case requires simultaneous coherence of multiple coupled compositional channels with full joint algebra at D=8 (and D=16 in the near future). The strictness was not domain-specific to the engine's job; it was a property of the test case that drove the algebraic completeness requirement. Other domains will eventually present test cases of similar or greater strictness — high-dimensional multi-asset financial portfolios with sector pairing, multi-modal biological assays with phylogenetic pairing, multi-station climate observations with regional pairing, multi-channel ultrasound, and so on — and the engine's design admits them at the appropriate D-class without modification.

The strictness driver is preserved here in design history because the engineering decision (why D=8 is load-bearing instead of D=4) only makes sense if the strictness requirement is documented. But the engine itself does not reference any specific domain. CoDa-community readers can engage with the engine on its own terms; domain-specialised readers (audio engineers, quants, geochemists, bioinformaticians) engage through their wrappers.

### 11.2 The wrapper architecture (facade pattern, data-driven, multilingual)

The engine emits **mathematically neutral output** in CoDa-community vocabulary: closure, CLR, ILR, Helmert basis, bearing trajectory, radial trajectory, twin-quaternion factoring (when D=8), quad-quaternion factoring (when D=16), CHSH coherence diagnostic, helmsman family channels, attractor fit, multi-bundle joint analysis. There are no domain-specific blocks in the engine schema. The engine is domain-agnostic; it computes compositional algebra and emits the result.

**A wrapper is a data file**, not prose, and not engine code. Specifically a wrapper is a JSON file conforming to the wrapper schema documented in `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md`. It contains:

1. **Carrier aliases** — map from engine-level carrier IDs (e.g., `L_HF`, `Operations`, `He-3`) to localised display names per locale.
2. **Field aliases** — map from engine output paths (e.g., `chsh_diagnostic.S_value`) to localised display names, units, and descriptions per locale.
3. **Calibration profiles** — value-range classifications per field (e.g., for `chsh_diagnostic.S_value`: 0–2 = independent, 2–2.4 = borderline, 2.4–2.7 = coupled, 2.7–2.828 = maximum coherence, >2.828 = anomalous), each range labelled per locale.
4. **Domain metadata** — wrapper id, version, engine target, supported locales, author, references.

The engine itself **does not load wrapper files**. The engine produces raw mathematical output. A separate optional renderer / report-builder consumes engine output + wrapper file + selected locale to produce a human-readable report. If no wrapper is supplied, the engine output is read directly in CoDa-community vocabulary — that is the default.

**The wrapper is a facade.** Same engine, same algebra, same output. The wrapper changes only what things are *called* and how value ranges are *labelled* for a chosen locale. Switching from audio to government-budget analysis is a wrapper swap, not an engine reconfigure. Switching from English to French in a Canadian government deployment is a locale swap inside the same wrapper.

**Multilingual is built in.** Every display string in a wrapper is a `{locale: string}` map. English and French are the minimum locale set for the audio wrapper and the government-budget wrapper (Markham mayor's office bilingual requirement). Additional locales (Spanish, Mandarin, German, Arabic, etc.) can be added to any wrapper without engine or other-locale changes.

**Wrapper authoring is the user's job.** This repository ships a wrapper schema specification, a blank template, an identity (passthrough) wrapper, and a small set of example wrappers (audio, government-budget skeleton). Domain experts write their own wrappers; the wrapper is the deliverable they own and maintain. The repository's job is the schema and the engine, not the domain mappings.

This separation matters for four reasons:

1. **CoDa-community alignment.** Engine output is in CoDa standard vocabulary; CoDa reviewers can evaluate the math directly without any wrapper. Backblaze, Planck, and SM neutrino demonstrations all read this way.
2. **Future-extensibility without engine churn.** Adding a new domain (or a new locale to an existing domain) is a wrapper-file edit; engine and other wrappers are untouched.
3. **Independent verification at each layer.** Engine reviewed for math; wrappers reviewed for domain-fit; locales reviewed by native speakers. Each layer audited independently.
4. **User ownership.** A domain expert (you, audio engineer; Markham budget analyst; geochemist; etc.) writes the wrapper for their use case. They control the names, the calibration thresholds, the references. The engine doesn't constrain them; the schema only ensures the wrapper is parseable.

### 11.3 Example wrappers shipped in this push

| Path | Purpose | Locales |
|---|---|---|
| `HCI-CNQ/wrappers/wrapper_schema.json` | JSON Schema defining what a valid wrapper looks like | n/a (machine schema) |
| `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md` | Human-readable wrapper specification with conventions and examples | en |
| `HCI-CNQ/wrappers/wrapper_blank_template.json` | Empty starter for users authoring a new domain wrapper | en (extensible) |
| `HCI-CNQ/wrappers/wrapper_generic.json` | Identity passthrough — uses CoDa standard names directly; no aliases | en |
| `HCI-CNQ/wrappers/wrapper_audio.json` | First domain wrapper instance: 4-way stereo / quadraphonic speaker analysis | en, fr |
| `HCI-CNQ/wrappers/wrapper_government_budget.json` | Skeleton for Canadian government budget composition analysis (Markham example) | en, fr |
| `HCI-AUDIO/CNQ_AUDIO_WRAPPER.md` | Optional prose handbook companion to `wrapper_audio.json` (calibration practice, worked example) | en |

`HCI-AUDIO/CNQ_AUDIO_WRAPPER.md` exists as a prose handbook for engineers who want narrative interpretation guidance; the canonical machine-readable wrapper is `wrapper_audio.json`. The handbook is one optional companion, not the wrapper itself. INV-024 sharpens accordingly: primary deliverable is the JSON data wrapper; the handbook is supplementary.

### 11.4 Wrapper architecture beyond CNQ

The wrapper schema is currently scoped to CNQ v2 output paths. The same pattern can be applied to CNT v3 output paths (a CNT wrapper would translate `tensor.timesteps[].coda_standard.composition`, `depth_tower.attractor.period`, etc.). A future push can add `wrapper_schema_cnt.json` and example CNT wrappers; the pattern is identical, only the engine target field paths differ.

> *"i work in nuclear chemistry or audio or geology, hydrology or comic scale systems down to quarks only the tags should change, nothing else, and tags are optional and user specified in a current tag file."*
> — Peter, push #32 directive

The engine is general. The wrappers are user-authored. CoDa-community alignment is the validation target. The discipline holds.

---

End of design document. Implementation begins.
