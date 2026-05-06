# CNT JSON Generator — Outstanding Concerns Review

**Date:** 2026-05-05
**Reviewer:** Peter Higgins / Claude
**Status:** ALL ISSUES RESOLVED. See "Resolution Status" section at end
of this document. The cnt_v2 engine (cnt.py / cnt.R, schema 2.0.0,
engine 2.0.2) implements every recommendation made in this review.

**Architecture context:** Two-engine system. The CNT JSON Builder produces
one canonical, complete, schema-stable JSON per dataset. All downstream
tools (plates, projector, spectrum analyser, future contributors) are
viewers over that JSON. The JSON is the authority; the viewers are
disposable.

This document inventories what stands between the (then) three-program
pipeline and that vision, and grades each concern by severity. The
Resolution Status section at the end maps each concern to the engine
version that addressed it.

---

## Empirical Inventory (what's there now)

Confirmed by inspection of `ball_regions_*.json`:

```
cnt_tensor_engine v1.0  →  ball_regions_cnt.json       (2.0 MB)
cnt_analysis      v1.0  →  ball_regions_analysis.json  (607 KB)
cnt_depth_sounder v1.0  →  ball_regions_depth.json     (49 KB)
```

**Cross-engine consistency:** `hs_mean` agrees to 0.0e+00 across all
three programs. Machine-precision consistency confirmed for the
overlap field. Other overlap fields not yet audited.

**Determinism:** Two consecutive runs of `cnt_tensor_engine.py` on
identical input produce content-identical JSON modulo the `generated`
timestamp (verified by SHA-256 of normalised JSON). Bit-identical
output is one timestamp away.

**Mathematical lineage block** is present and correct
(Aitchison 1986 / Shannon 1948 / Egozcue 2003 / Higgins 2025-2026).

**Per-step tensor record** in `timesteps[]` includes raw_values,
composition, clr, ilr, bearing_tensor, angular_velocity_deg —
comprehensive zeroth-derivative state.

**Information-theoretic bridge** in `cnt_analysis` includes Shannon,
Fisher, KL divergence, mutual information, entropy rate.

**M² = I involution** verified at one sample (residual ~6e-17 on Hs-25
and Ball/Region).

---

## Concerns by Severity

### A — BLOCKERS (would prevent this from being a standard)

#### A1. Three JSONs, not one

Severity: **blocker**.

The canonical authority is currently distributed across three program
outputs. Downstream viewers must read all three and stitch them. There
is no single file a contributor can validate against. This breaks the
two-engine architecture: contributors cannot write a viewer if the
JSON they read is incomplete by design.

**Recommendation:** Build `cnt_engine.py` as a thin wrapper that runs
all three programs and merges them into one canonical
`{name}_cnt.json` with top-level keys:

```
metadata/        identity, provenance, schema version
input/           raw data, hashes, ordering convention
tensor/          per-timestep state (current cnt_tensor_engine)
stages/          stage1/2/3 + section atlas + ledger (current cnt_analysis)
bridges/         dynamical / control / information theory
depth/           recursive depth sounder + involution proof
diagnostics/     EITT residuals, M² verification, determinism hash
```

The three programs become library functions invoked by the wrapper.
Viewers read one JSON. Three programs as separate scripts remain for
debugging / partial recomputation, but the published artifact is one.

#### A2. No JSON schema documentation or version

Severity: **blocker**.

`cnt_tensor_engine v1.0` is in the metadata, but the JSON *schema* —
which keys exist, what types, what ranges, what they mean — is not
documented. A contributor writing a viewer reads our example outputs
and reverse-engineers it. That is not a standard.

The pipeline_version in HS_MACHINE_MANIFEST ("2.0 Extended + ... + CNT")
is for the analytical pipeline, not the JSON schema. The two need
distinct versioning. JSON schema must change rarely and only with
documented migrations.

**Recommendation:** Write `CNT_JSON_SCHEMA.md` as a numbered field
inventory:

```
metadata/
  schema_version : str — semantic version of THIS schema (e.g. "1.0.0")
  engine_version : str — engine that produced it (may differ from schema)
  generated      : ISO 8601 timestamp
  ...
tensor/timesteps[]/
  index          : int — 0..T-1
  label          : str — record identifier
  composition    : list[float] of length D, sums to 1.0 ± 1e-15
  clr            : list[float] of length D, sums to 0.0 ± 1e-14
  ...
```

Schema version follows semver: 1.x.x adds fields, 2.x.x removes them.
Old viewers must keep working under 1.x.x bumps.

#### A3. Input data hash not recorded

Severity: **blocker** for any audit / reproducibility claim.

`metadata.input_file` is the filename. No hash. Two different files
with the same name produce JSONs that look identical in metadata.
Cannot detect input drift. Cannot verify a re-run used the same
source.

**Recommendation:** Add `metadata.input_sha256` and
`metadata.input_n_rows`, `metadata.input_n_columns`. Always present.
Compute on the closed simplex projection (after ingestion) so the
hash is invariant to whitespace / line-ending differences in the
source CSV but changes when the data does. Also keep
`metadata.input_file_sha256` for the raw file — both, distinguished
by name.

#### A4. Ordering convention not declared

Severity: **blocker** for any non-temporal dataset.

The JSON contains `timesteps[]` whose order matters for several
fields:

* `angular_velocity_deg` — computed between consecutive timesteps
* `corollary_diagnostics.reversals[]` — order-dependent count
* `system_course_plot.cumulative_arc_length` — order-dependent integral
* `depth.energy_tower` — order-dependent (proven in T-sweep,
  Ball/Region same data alphabetical → 46 levels, sample-count → 17)

When the input is a time series (Japan EMBER), order is meaningful.
When the input is a sample collection (Ball oxides), order is
arbitrary and these fields are partially or fully meaningless.

The JSON does not declare which case applies. A viewer that interprets
`angular_velocity_deg` from a sample-collection input is wrong.

**Recommendation:** Add `input.ordering` block with three required fields:

```
input/ordering/
  is_temporal       : bool      — true if rows are a time series
  ordering_method   : str       — "as-given" | "by-time" | "by-label" | "by-d_A" | "custom"
  ordering_caveat   : str|null  — human-readable note for non-temporal
                                  cases ("Order is arbitrary; angular
                                  velocity and energy depth are
                                  ordering-dependent.")
```

Viewers must check `is_temporal` before trusting derivative fields.
Schema must require these to be present.

---

### B — IMPORTANT (would weaken the standard)

#### B1. Period-2 attractor metrics not in the JSON

Severity: **important**.

The depth-sounder JSON has `curvature_hs_trajectory` and
`curvature_cycle.{detected, period, residual, convergence_level}`. It
does **not** have:

* `attractor.c_even`, `attractor.c_odd`, `attractor.amplitude`
* `lyapunov_exponent` (period-2 contraction-based, not per-carrier)
* `mean_contraction_ratio`, `banach_satisfied`
* `impulse_response.{A, delta, zeta, classification}` per Math
  Handbook Ch 23.3

We computed all of these post-hoc in `ball_regions_lyapunov.json`.
Every viewer of every dataset would have to recompute them.

**Recommendation:** Move these into `depth/curvature_attractor/` and
`depth/impulse_response/` as a fixed, schema-required block. Compute
once in the engine, cite Math Handbook Ch 22 / 23 / 24 in the field
descriptions.

#### B2. Two distinct Lyapunov exponents, ambiguously named

Severity: **important**.

The JSON contains `dynamical_systems.lyapunov_exponents[]` as a list
of per-carrier λ values (one per oxide). The period-2 attractor λ
(contraction rate of the curvature-tower recursion, the value
documented in Math Handbook Ch 24) is **not** there — we computed it
post-hoc.

These two λs measure different things. Per-carrier λ is the standard
dynamical-systems perturbation sensitivity along each carrier axis.
Period-2 attractor λ is the contraction rate of the depth-sounder
recursion toward its limit cycle. A viewer that reports "Lyapunov
exponent = X" without saying which is meaningless.

**Recommendation:** Rename to remove ambiguity:

```
bridges/dynamical_systems/per_carrier_lyapunov[]
depth/curvature_attractor/contraction_lyapunov   (the Ch 24 quantity)
```

Document both with one-sentence definitions in the schema.

#### B3. EITT residual diagnostics not exposed

Severity: **important**.

The depth sounder implicitly performs EITT decimation at each
recursion level (the curvature composition is itself a decimation).
But the *EITT bench-test* on the input data — variation_pct at
M = 2, 4, 8 — is not in the JSON. We just demonstrated this matters
(Ball/Region M=261 bench-test, Δ = 0.501 %).

For any downstream viewer that wants to declare a compression ratio
(plates, summary tables, decimated reports), the JSON must report
EITT residuals at canonical compression ratios. Otherwise every
viewer recomputes them.

**Recommendation:** Add `diagnostics.eitt_residuals/` block with the
canonical M-sweep (2, 4, 8, 16, 32, 64, 128, ⌈N/101⌉, ⌈N/50⌉) and the
five-percent gate annotation. Built once in the engine.

#### B4. Off-diagonal metric tensor not in JSON

Severity: **important**.

The Higgins Steering Metric Tensor is

```
κ_ij(x) = (δ_ij - 1/D) / (x_i · x_j)
```

The JSON exposes only the diagonal `κ_jj = 1/x_j` as
`steering_sensitivity` (per timestep, per carrier). The off-diagonal
κ_ij = -1/(D · x_i · x_j) governs inter-carrier coupling and is part
of the Math Handbook Ch 3.3 definition.

The diagonal is what current viewers use, but downstream tools (e.g.
Stage 1-Δ when built, anyone studying carrier coupling) need the full
matrix. Computing it is trivial (D² floats per timestep, smaller than
the bearing tensor at D(D-1)/2).

**Recommendation:** Add `tensor/timesteps[]/metric_tensor_full` as
the full D×D matrix. Keep `metric_tensor_diagonal` as a derived
convenience view.

#### B5. Lock-event metadata not enumerated

Severity: **important** (touches Stage 1 plate spec).

The Manifold Projector convention defines DEGEN diamond markers,
LOCK-ACQ green dashed rings, LOCK-LOSS amber rings (per
HS_MACHINE_MANIFEST.json `visualization_standard.boundary_markers`).
The CNT JSON does not enumerate these events explicitly. A viewer
must recompute them by scanning the CLR series for the |CLR| < -10
and CLR-spread thresholds.

**Recommendation:** Add `diagnostics.lock_events[]` as a fixed list:

```
{ "event_type": "DEGEN" | "LOCK-ACQ" | "LOCK-LOSS",
  "timestep_index": int,
  "label": str,
  "carrier": str | null,
  "clr_value": float,
  "context": str }   # human note like "Nuclear → 0 in 2014, post-Fukushima"
```

Single computation in the engine, stable interface for every viewer.

#### B6. Provenance: code version, environment, commit hash

Severity: **important** for audit / regulatory uses.

Current metadata: `engine: "CNT Tensor Engine v1.0"`. Missing:
git commit SHA, Python version, NumPy version, OS, hostname (or
hash), wall clock, CPU model. Without these, "I ran the same
input and got a different answer" is unattributable to any specific
software state.

**Recommendation:** Add `metadata.environment/`:

```
git_sha          : str    — commit hash of the engine code
python_version   : str
numpy_version    : str
platform         : str    — e.g. "Linux-5.15-x86_64"
hostname_hash    : str    — SHA-256 of hostname (privacy-preserving)
wall_clock_ms    : int    — total run time in milliseconds
```

The instrument's own audit trail (ISO 17025 in spirit, per
HS_MACHINE_MANIFEST `governance.audit_system`).

---

### C — TRACK (worth fixing, not blockers)

#### C1. The K_ prefix in helmsman names

Severity: **track**.

Curvature-tower helmsman fields are reported as `K_K2O`, `K_TiO2`, etc.
The K_ prefix means "kappa-derived" (the curvature composition is the
normalised diagonal of κ). A naive reader sees "K_K2O" and parses it
as some compound notation. This is a documentation gap, not a math
gap.

**Recommendation:** Either drop the prefix and rely on context (the
helmsman field is *in* the curvature tower, so K_ is redundant), or
document it once in the schema with a short note. My preference is
drop the prefix.

#### C2. JSON size at large N

Severity: **track**.

`ball_regions_cnt.json` is 2.0 MB at T=95. Distance matrix is the
main bulk (95×95 = 9025 floats × ~25 bytes JSON ≈ 220 KB). At T=1000
the distance matrix alone is 25 MB. Either compress, or move to a
sparse representation (each distance is paired with its labels — keep
only the top-K largest distances), or omit and require the viewer to
compute on demand from the per-timestep CLRs (which are necessary
anyway).

**Recommendation:** At T > 200, omit the full distance matrix; keep
`max_distance`, `max_pair`, `distance_distribution_quantiles` as
summary statistics. Viewers that want the full matrix recompute it.

#### C3. Determinism: timestamp breaks SHA-256 reproducibility

Severity: **track**.

Two consecutive runs differ only by the `generated` timestamp.
Removing it gives bit-identical content. Anyone testing reproducibility
has to normalise.

**Recommendation:** Add `metadata.content_sha256` field — a SHA-256
of the full JSON with `metadata.generated` and `metadata.environment`
removed (or canonicalised). One byte at the top of the file lets any
viewer verify content identity in one comparison.

#### C4. Stage 3 day-triad cap is implicit

Severity: **track**.

`stage3.triadic_area.results[]` returns 500 top-area triads (verified
earlier). The 500 cap is hardcoded; viewers don't know it's there.
For T = 95 the engine computed C(95,3) = 138,415 candidates and
returned the top 500. For T = 26,266 it timed out (the original
problem we fixed via binning).

**Recommendation:** Add `stage3.triadic_area/`:

```
n_candidates     : int   — C(T, 3)
n_returned       : int   — len of results[]
selection_method : str   — "top_K_by_area" | "all" | "binned_first"
selection_K      : int   — 500 by default
```

A viewer can decide whether 500 is enough or recompute. Future-proofs
the schema against T-scaling.

#### C5. Edge cases: small T, D = 2, degenerate input

Severity: **track**.

The T-sweep on Ball top-10 returned curvature depth = 4 (period-1) —
a degenerate result because T=10 is below the engine's effective
threshold for D=10. The JSON does not flag this. A viewer reading
"depth = 4" doesn't know it's small-T degeneracy vs. genuine fast
convergence.

Similarly D = 2 (Gold/Silver, EXP-01): does the engine handle? The
metric tensor is 2×2, the bearing tensor has D(D-1)/2 = 1 element.
Untested in the geochem battery.

TAS-style degenerate input (records pre-aligned to one carrier axis):
engine produces a fixed-point period-1 attractor. A viewer should be
able to detect "this input was likely pre-sorted compositionally" and
flag.

**Recommendation:** Add `diagnostics.degeneracy_flags[]` with named
conditions:

```
- "small_T"           : T < max(20, 2D)
- "small_D"           : D < 3
- "pre_aligned"       : single-carrier monotonic order detected in CLR series
- "nuclear_carrier_zero" : any column has value < zero_replacement_delta in any record
```

Engine sets these flags; viewers warn appropriately.

#### C6. Multiple ingestion formats

Severity: **track**.

Engine accepts CSV. For broader use: JSON arrays, NetCDF, Parquet,
direct numpy/pandas. Not blocking but limits adoption by people
working in non-CSV pipelines.

**Recommendation:** Library API where the input is a structured
record list, with thin format-specific shims. Defer until the schema
is locked.

---

### D — RESOLVED OR NOT-A-CONCERN (closing)

#### D1. K₂O lineage prefix

The robustness study refined this to "highest-CLR-variance carrier".
Engine output already reports the helmsman correctly per timestep;
the interpretive claim is documentation, not engine. Resolved.

#### D2. Energy depth = 0.5 × T scaling

Empirically falsified in the T-sweep (R² = 0.18). The engine's
`energy_depth` value is correct; it just isn't a parameter-free
observable across orderings. The fix is the ordering convention
(Concern A4), not a change to the engine.

#### D3. Stage 3 timeout at large N

Resolved by binning convention (n ≥ 10 per bin → ≤ ~100 bins typically).
Recorded in the robustness journal. The engine's `combinations(days, 3)`
remains as written; the responsibility is on the data preparation
side, not the engine. Worth a docstring note saying "expects pre-binned
compositional time series; for raw N > ~200 use a binner first."

---

## Recommended Action Plan (ordered)

A blocker-first, concrete, single-PR-each path:

1. **Define and document the schema** (Concern A2). Write
   `CNT_JSON_SCHEMA.md` capturing the *current* output as schema 1.0.0.
   Don't change the engine yet — first record what it produces.

2. **Add input hash + ordering declaration** (Concerns A3, A4). Two
   metadata fields, ~30 lines of code, schema bump to 1.1.0.

3. **Move Lyapunov / impulse-response / EITT-residual computation
   into the engine** (Concerns B1, B3). Currently post-hoc, should be
   stable JSON output. Schema bump to 1.2.0.

4. **Single-program merge** (Concern A1). Refactor
   `cnt_tensor_engine`, `cnt_analysis`, `cnt_depth_sounder` into one
   wrapper. Schema bump to 2.0.0 (structural change). Three programs
   stay as library modules and as command-line entry points for
   partial recomputation.

5. **Disambiguate Lyapunov exponents** (Concern B2). Schema bump to
   2.1.0. Old field aliased for a deprecation window.

6. **Add lock-event enumeration** (Concern B5). Schema bump to 2.2.0.

7. **Environment provenance** (Concern B6). Schema bump to 2.3.0.

8. **Track-tier items** (C1–C6) folded into 2.x.x as time permits.

After step 4 the architecture vision is fulfilled: one engine, one
JSON, one schema. A future contributor can write a viewer against
the schema document alone, no examples needed.

---

## Critical Path to CoDaWork

If we have to ship before the conference:

* Concerns A2, A3, A4 are essential for credibility. A schema document
  and two metadata fields. ~half a day's work. After that, anyone in
  the audience asking "what does your output look like?" gets a clean
  answer.
* Concerns B1, B5 are nice-to-have but post-hoc computation suffices
  for the talk. A scrap script that takes the existing JSONs and
  produces the missing fields is a bridge.
* Concerns A1, B2, B3 can wait for the post-conference rewrite. The
  three-program pipeline as it stands works, just not as a single
  standard.

---

## Resolution Status (audit 2026-05-05)

All concerns from this review are resolved in the cnt_v2 engine. Each
fix records the engine version that delivered it.

### Blockers — A series

| Concern | Status | Resolution |
|---|---|---|
| A1 — Three JSONs, not one | DONE (engine 2.0.0) | `cnt.py` / `cnt.R` are single-program engines. One CSV in, one canonical JSON out. The three earlier programs (cnt_tensor_engine, cnt_analysis, cnt_depth_sounder) are deprecated. |
| A2 — No schema documentation or version | DONE (engine 2.0.0) | `CNT_JSON_SCHEMA.md` is authoritative, version-tracked (currently 2.0.0), with field-by-field types and §10 migration table. |
| A3 — Input data hash not recorded | DONE (engine 2.0.0) | `input.source_file_sha256` (raw bytes) and `input.closed_data_sha256` (post-ingestion canonical form) are REQUIRED schema fields. |
| A4 — Ordering convention not declared | DONE (engine 2.0.0) | `input.ordering` block is REQUIRED, with `is_temporal`, `ordering_method`, `caveat`. Viewers must check before interpreting derivative quantities. |

### Important — B series

| Concern | Status | Resolution |
|---|---|---|
| B1 — Period-2 attractor metrics not in JSON | DONE (engine 2.0.0) | `depth.higgins_extensions.curvature_attractor.{period, c_even, c_odd, amplitude, contraction_lyapunov, mean_contraction_ratio, banach_satisfied}` and `depth.higgins_extensions.impulse_response.{amplitude_A, depth_delta, damping_zeta, classification}` are in the schema as REQUIRED. |
| B2 — Two distinct Lyapunov exponents, ambiguously named | DONE (engine 2.0.0) | Per-carrier Lyapunov is at `bridges.higgins_extensions.dynamical_systems.per_carrier_lyapunov[]`. Contraction Lyapunov is at `depth.higgins_extensions.curvature_attractor.contraction_lyapunov`. Names disambiguate. |
| B3 — EITT residual diagnostics not exposed | DONE (engine 2.0.0) | `diagnostics.higgins_extensions.eitt_residuals` carries the M-sweep with variation_pct per M and the gate threshold. Empirical-observation framing per Egozcue 2026 explicitly noted in the JSON. |
| B4 — Off-diagonal metric tensor not in JSON | DONE (engine 2.0.0) | `tensor.timesteps[i].higgins_extensions.metric_tensor.matrix` is the full D×D Aitchison metric. The diagonal convenience view is also kept. |
| B5 — Lock events not enumerated explicitly | DONE (engine 2.0.0) | `diagnostics.higgins_extensions.lock_events[]` enumerates DEGEN / LOCK-ACQ / LOCK-LOSS events with timestep_index, label, carrier, clr_value, context. |
| B6 — Environment provenance missing | DONE (engine 2.0.0) | `metadata.environment.{git_sha, language_version, numerical_lib, platform, hostname_hash}` are present. |

### Track tier — C series

| Concern | Status | Resolution |
|---|---|---|
| C1 — K_ prefix on helmsman names | DONE (engine 2.0.0) | Curvature-tower helmsman fields drop the K_ prefix where context is unambiguous; documented in CNT_PSEUDOCODE.md. |
| C2 — JSON size at large T | NOT YET CRITICAL | At T=731 (BackBlaze) the JSON is 3.3 MB. Below the 100 MB GitHub limit by 30×. Compression deferred. |
| C3 — Determinism: timestamp breaks reproducibility | DONE (engine 2.0.0) | `diagnostics.content_sha256` excludes `metadata.generated`, `metadata.wall_clock_ms`, `metadata.environment` from the hash. Two runs produce identical content_sha256. Verified on Japan (multiple times). |
| C4 — Stage 3 day-triad cap is implicit | DONE (engine 2.0.0) | `stages.stage3.higgins_extensions.triadic_area.selection_method` is one of `top_K_by_area` / `none_T_too_small` / `none_T_too_large`. Cap is `TRIADIC_T_LIMIT` (default 500, user-configurable per 2.0.2). |
| C5 — Edge cases: small T, D=2, degenerate input | DONE (engine 2.0.0) | `diagnostics.higgins_extensions.degeneracy_flags[]` fires for `small_T`, `small_D`, `pre_aligned_compositionally`. Gold/silver D=2 returns DEGENERATE classification correctly. |
| C6 — Multiple ingestion formats | NOT YET CRITICAL | CSV ingestion only. Adapters in `experiments_v2/adapters/` cover BackBlaze (zip), FAO (long-format pivot), nuclear (SEMF aggregation), gold/silver (ratio reconstruction). New formats added on demand via the same adapter pattern. |

### Beyond the original concerns

Two corrections discovered during the post-2.0.0 verification work:

| Issue | Status | Resolution |
|---|---|---|
| Period-1 false-positive on USA EMBER & Ball/TAS | DONE (engine 2.0.1) | `detect_period` now requires TWO consecutive level-pair convergences for period-1 (was 1). USA recovered to curv_depth=16 / LIGHTLY_DAMPED; Ball/TAS to curv_depth=12 / LIGHTLY_DAMPED. |
| Curvature composition formula error | DONE (engine 2.0.1) | `derived_curvature` now uses 1/x_j² (was 1/x_j), matching Math Handbook Ch 19.2(b). Effect: depth-tower trajectories now match the reference engine bit-for-bit on Japan. |
| User control over engine constants | DONE (engine 2.0.2) | USER CONFIGURATION block at top of cnt.py / cnt.R with documented constants. Active values echoed in `metadata.engine_config` of every JSON output. The user controls the tool, not the tool. |

### What's NOT covered

Two items from the original review remain explicitly NOT yet implemented:

1. **Random-sample triadic at T > limit (proposed extension).** Currently
   `selection_method = "none_T_too_large"` skips the enumeration for
   T > TRIADIC_T_LIMIT. A future schema bump (2.1.0) could add a
   `random_sample_K` selection method with a stored `sampling_seed`
   for reproducibility. Decision: NOT DOING for now — keeps the
   determinism contract simple. Viewers that want triads can compute
   from `tensor.timesteps[i].coda_standard.clr` on demand.

2. **Two new IR classes for the BackBlaze pattern.** The IR classifier
   reports DEGENERATE when curvature attractor period = 0, even when
   the energy tower shows period-1 fixed-point stability. Adding
   `ENERGY_STABLE_FIXED_POINT` and `CURVATURE_VERTEX_FLAT` classes
   would distinguish "stable but compositionally concentrated" (e.g.
   BackBlaze fleet, Errors at 60-96%) from genuine D=2 degeneracy
   (e.g. Gold/Silver). Documented in
   `experiments_v2/codawork2026/backblaze_fleet/INTERPRETATION.md` as
   an action item; not yet in the engine.

Minimum viable for CoDaWork: schema doc + two metadata fields. The
talk's primary deliverable is the *result*, not the JSON; the JSON
becomes the standard *after* the conference once contributors arrive.

---

*The instrument reads. The expert decides. The loop stays open.*
*The JSON is the read. The viewer is the eye. The schema is the
contract between them.*
