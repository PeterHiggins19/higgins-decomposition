# CNT JSON Schema

**Schema version:** 2.0.0
**Engine version supported:** 2.0.3 (Python reference implementation; cnt.R port at 2.0.2)
**Status:** Authoritative
**Last revised:** 2026-05-05

**Major change from 1.0.0:** Every analytic block (tensor, stages, bridges,
depth, diagnostics) is now split into `coda_standard/` and `higgins_extensions/`
sub-blocks. Every analytic block declares its functional role (`_function`:
composer / review / formatter). Section 8 documents the CoDa↔Higgins
mathematical mapping.

**Engine fix log within 2.0.x:**

| Engine version | Fix |
|---|---|
| 2.0.0 | Initial split into coda_standard / higgins_extensions sub-blocks |
| 2.0.1 | `detect_period` requires TWO consecutive convergences for period-1 (was 1; fixed false-positive on USA EMBER and Ball/TAS) |
| 2.0.1 | `derived_curvature` corrected to use 1/x_j² (was 1/x_j) — matches Math Handbook Ch 19.2(b) |
| 2.0.1 | `TRIADIC_T_LIMIT` default lowered from 1000 to 500 |
| 2.0.2 | `metadata.engine_config` block added — REQUIRED field (see §1.2) |
| 2.0.2 | `eitt_residuals.M_sweep[i].pass_5pct` renamed to `pass_gate` (more general; reflects user-configurable EITT_GATE_PCT) |
| 2.0.3 | IR taxonomy refined: `DEGENERATE` is split into three more-informative classes — `ENERGY_STABLE_FIXED_POINT` (energy depth ≥ DEPTH_MAX_LEVELS with stable A), `CURVATURE_VERTEX_FLAT` (curvature recursion driven to vertex by single-carrier dominance), `D2_DEGENERATE` (genuine D=2 limitation; only one independent compositional axis). Python only — cnt.R remains at the 2.0.2 single-`DEGENERATE` taxonomy. |

---

## Reading This Schema

The CNT engine ingests a compositional dataset and emits exactly one JSON
conforming to this document. Downstream tools read only this JSON. The
schema is the contract; the engine and the viewers honour it.

The schema follows semantic versioning. Field additions bump the minor
version. Field removals or type changes bump the major version. Old
viewers continue to work under any minor bump.

---

## Two Orthogonal Classifications

Every analytic field carries two labels:

**Ownership** — whether the field is part of the CoDa standard (Aitchison /
Egozcue / Pawlowsky-Glahn / Shannon lineage) or a Higgins-framework
extension. A CoDa-community reviewer can read just `coda_standard/`
fields and audit the engine's compositional analysis without engaging
Higgins-specific machinery. The mapping in §8 shows that every Higgins
extension is computable from CoDa-standard quantities — it is a *reading*
of the simplex, not a deviation from it.

**Function** — the role the block plays in the engine pipeline:

| `_function`  | Role                                                              |
|--------------|-------------------------------------------------------------------|
| `composer`   | Creates compositional structure from raw data (closure, CLR, etc.)|
| `review`     | Analyses the composed structure (variation matrix, attractor)     |
| `formatter`  | Prepares specific representations for display (atlas, ledger)     |
| `provenance` | Identity, hashes, environment — neither computation nor display   |

This functional split clarifies *who reads what*: a viewer building a
projector reads `composer` blocks; a viewer building an analytical
report reads `review` blocks; a viewer building plates reads
`formatter` blocks.

---

## Top-Level Structure

```json
{
  "metadata":    { ... },     // _function: provenance
  "input":       { ... },     // _function: provenance + composer prep
  "tensor":      { ... },     // _function: composer
  "stages": {
    "stage1":    { ... },     // _function: formatter
    "stage2":    { ... },     // _function: review
    "stage3":    { ... }      // _function: review
  },
  "bridges":     { ... },     // _function: review
  "depth":       { ... },     // _function: review
  "diagnostics": { ... }      // _function: review
}
```

Every analytic block (tensor, each stage, bridges, depth, diagnostics)
carries `_function`, `_description`, `coda_standard/`, and
`higgins_extensions/`. `coda_standard/` may be `{}` when the entire
block is HUF-specific (e.g. `depth/` is wholly Higgins; the curvature
tower is not part of the CoDa canon).

---

## 1 — `metadata/`

`_function: "provenance"`. Identity, schema version, run-time provenance.

| Field                        | Type   | Notes                                                                  |
|------------------------------|--------|------------------------------------------------------------------------|
| `schema_version`             | str    | "2.0.0".                                                               |
| `engine_version`             | str    | E.g. "cnt 2.0.3".                                                      |
| `engine_implementation`      | str    | "python" \| "R".                                                       |
| `generated`                  | str    | ISO-8601 UTC timestamp.                                                |
| `wall_clock_ms`              | int    | Total run time in milliseconds.                                        |
| `mathematical_lineage`       | object | Citations: Aitchison 1986, Shannon 1948, Egozcue 2003, Higgins 2026.   |
| `engine_config/`             | object | **REQUIRED** (added 2.0.2). Active values from USER CONFIG block.      |
| `environment/`               | object | git_sha, language_version, numerical_lib, platform, hostname_hash.    |

### 1.1 — `metadata/engine_config/` — REQUIRED (added 2.0.2)

Active values from the engine's USER CONFIGURATION block at the top of
`cnt.py` / `cnt.R`. The block is part of the deterministic content and
included in `diagnostics.content_sha256`. Two runs with identical
config and identical input produce identical content_sha256; two runs
with different config produce different content_sha256.

| Field                       | Type      | Default              | Notes                                                                       |
|-----------------------------|-----------|----------------------|-----------------------------------------------------------------------------|
| `_description`              | str       | (fixed)              | Plain-language note about the deterministic contract.                       |
| `DEFAULT_DELTA`             | float     | 1e-15                | Zero-replacement floor.                                                     |
| `DEGEN_THRESHOLD`           | float     | 1e-4                 | CLR-spread threshold for DEGEN lock event.                                  |
| `LOCK_CLR_THRESHOLD`        | float     | -10.0                | CLR threshold for LOCK-ACQ / LOCK-LOSS events.                              |
| `DEPTH_MAX_LEVELS`          | int       | 50                   | Hard cap on depth-tower length.                                             |
| `DEPTH_PRECISION_TARGET`    | float     | 0.01                 | Relative precision for period detection (1%).                               |
| `NOISE_FLOOR_OMEGA_VAR`     | float     | 1e-6                 | OMEGA_FLAT termination threshold.                                           |
| `TRIADIC_T_LIMIT`           | int       | 500                  | Above this T, Stage 3 day-triad enumeration is skipped.                    |
| `TRIADIC_K_DEFAULT`         | int       | 500                  | When triadic enumeration runs, store top-K results by area.                 |
| `EITT_GATE_PCT`             | float     | 5.0                  | Variation_pct gate for EITT bench-test.                                     |
| `EITT_M_SWEEP_BASE`         | list[int] | [2,4,8,16,32,64,128] | Base M-sweep compression ratios.                                            |

The user is the operator. The engine reports its active configuration
in every JSON it produces.

---

## 2 — `input/`

`_function: "provenance"` (raw data record) + `composer` (the closed canonical form).

| Field                  | Type        | Notes                                                                 |
|------------------------|-------------|-----------------------------------------------------------------------|
| `source_file`          | str         | Filename of the source CSV (basename only).                           |
| `source_file_sha256`   | str         | SHA-256 of the raw bytes of `source_file`.                            |
| `closed_data_sha256`   | str         | SHA-256 of the closed canonical simplex form (post-ingestion).        |
| `n_records`            | int         | Number of compositional records (T).                                  |
| `n_carriers`           | int         | Number of compositional parts (D).                                    |
| `carriers`             | list[str]   | Carrier names, length D.                                              |
| `labels`               | list[str]   | Per-record labels.                                                    |
| `zero_replacement/`    | object      | { method, delta, applied, n_replacements }.                           |
| `ordering/`            | object      | REQUIRED. { is_temporal, ordering_method, caveat }.                   |

`ordering/` flags whether the input is a time series. Several derivative
fields in `tensor/`, `stages/`, and `depth/` are order-dependent
(angular velocity, energy tower depth, bearing reversals). Viewers must
check `ordering.is_temporal` before interpreting derivative quantities.

---

## 3 — `tensor/`

```
_function:    "composer"
_description: "Per-record compositional state computed by applying
               operators to the input."
```

### 3.1 — `tensor/helmert_basis/`

Always present. Used by both `coda_standard.ilr` and downstream Higgins
machinery.

| Field          | Type        | Notes                                                  |
|----------------|-------------|--------------------------------------------------------|
| `D`            | int         | Carrier count.                                         |
| `dim`          | int         | D − 1 (rank).                                          |
| `coefficients` | list[list]  | (D−1) × D matrix.                                      |

### 3.2 — `tensor/timesteps[i]/`

For each record i ∈ [0, T):

```json
{
  "index": <int>,
  "label": <str>,
  "raw_values": [<float>...],
  "coda_standard": {
    "composition":             [...],   // closure to simplex, sums to 1
    "clr":                     [...],   // CLR transform
    "ilr":                     [...],   // ILR projection (Helmert)
    "shannon_entropy":         <float>, // -sum x_j ln x_j
    "aitchison_norm":          <float>, // ||clr(x)||
    "aitchison_distance_step": <float>  // present iff i >= 1
  },
  "higgins_extensions": {
    "higgins_scale":           <float>, // Hs = 1 - H/ln(D), in [0,1]
    "bearing_tensor": {
      "pairs": [
        { "carrier_i": <str>, "carrier_j": <str>, "theta_deg": <float> },
        ...                                  // D(D-1)/2 entries
      ]
    },
    "metric_tensor": {
      "matrix":      [...],              // full D x D Aitchison metric
      "eigenvalues": [...],              // length D, ascending
      "trace":       <float>
    },
    "metric_tensor_diagonal":  [...],    // (1 - 1/D) / x_j^2 per j
    "condition_number":        <float>,  // max(x)/min(x)
    "angular_velocity_deg":    <float>,  // present iff i >= 1
    "helmsman":                <str>,    // present iff i >= 1
    "helmsman_delta":          <float>   // present iff i >= 1
  }
}
```

`coda_standard/` is the CoDa-community-recognised core. `higgins_extensions/`
are Higgins-framework readings of the same simplex. The mapping in §8
shows each extension as a function of `coda_standard/` quantities.

---

## 4 — `stages/`

Stage 1 / 2 / 3 cross-examinations. Each stage has its own `_function`.

### 4.1 — `stages/stage1/` — formatter

```
_function:    "formatter"
_description: "Cube-face projections and per-record metric ledger
               formatted for plate display."
```

| `coda_standard/`    | `higgins_extensions/`            |
|---------------------|----------------------------------|
| (empty — Stage 1 outputs are display formatters specific to HUF/CBS) | `section_atlas[]`, `metric_ledger[]` |

`section_atlas[i]` per record: { index, label, xy_face, xz_face, yz_face,
metric_tensor_trace, condition_number, angular_velocity_deg }.

`metric_ledger[i]` per record: { index, label, hs, ring, omega_deg,
helmsman, energy, condition }.

### 4.2 — `stages/stage2/` — review

```
_function:    "review"
_description: "Pairwise cross-examination of compositional behaviour."
```

| `coda_standard/`            | `higgins_extensions/`              |
|-----------------------------|------------------------------------|
| `variation_matrix` (Aitchison τ_ij = var(ln(x_i/x_j)), D × D) | `carrier_pair_examination[]` (per-pair pearson_r, co_movement, opposition, bearing_spread, locked-flag) |

### 4.3 — `stages/stage3/` — review

```
_function:    "review"
_description: "Higher-degree subcompositional and triadic analysis."
```

| `coda_standard/`              | `higgins_extensions/`                                |
|-------------------------------|-------------------------------------------------------|
| `subcomposition_ladder[]` (degree k ∈ [2, D−1]) | `triadic_area/`, `carrier_triads[]`, `regime_detection/` |

`triadic_area/` declares `n_candidates`, `n_returned`, `selection_method`
(`top_K_by_area` / `none_T_too_small` / `none_T_too_large`),
`selection_K`, and `results[]`.

---

## 5 — `bridges/`

```
_function:    "review"
_description: "Connections to dynamical / control / information theory."
```

| `coda_standard/`                                 | `higgins_extensions/`                               |
|--------------------------------------------------|-----------------------------------------------------|
| `information_theory/` (entropy_series, fisher_information, kl_divergence, mutual_information, entropy_rate) | `dynamical_systems/` (per_carrier_lyapunov, velocity_field, recurrence_analysis), `control_theory/` (state_space_model, observability) |

The information-theory bridge is in `coda_standard/` because Shannon
entropy and its derivatives are not exclusively CoDa, but the CoDa
community uses them on log-ratio coordinates. The dynamical and control
bridges are Higgins extensions.

---

## 6 — `depth/`

```
_function:    "review"
_description: "Recursive depth sounder, period-2 attractor, impulse response.
               Wholly Higgins-framework — no CoDa-standard analogue."
```

| `coda_standard/`     | `higgins_extensions/`                                                                   |
|----------------------|-----------------------------------------------------------------------------------------|
| `{}` — empty by design. The depth sounder, energy/curvature towers, period-2 attractor, and impulse response are Higgins extensions; they have no CoDa-canon equivalent. | `involution_proof/`, `level_0/`, `energy_tower[]`, `curvature_tower[]`, `curvature_attractor/`, `impulse_response/`, `energy_cycle/`, `curvature_cycle/`, `summary/` |

### 6.1 — `depth/higgins_extensions/curvature_attractor/`

| Field                   | Type   | Notes                                                          |
|-------------------------|--------|----------------------------------------------------------------|
| `period`                | int    | 1 (fixed point) or 2 (limit cycle). 0 if no attractor detected.|
| `c_even`                | float  | Mean Hs at even-parity tail levels.                            |
| `c_odd`                 | float  | Mean Hs at odd-parity tail levels.                             |
| `amplitude`             | float  | \|c_even − c_odd\|.                                            |
| `convergence_level`     | int    | Recursion level at which detected.                             |
| `residual`              | float  | Final residual at convergence.                                 |
| `contraction_lyapunov`  | float  | Same-parity contraction Lyapunov exponent.                     |
| `mean_contraction_ratio`| float  | Mean of \|Δ(n+2)\|/\|Δ(n)\|.                                   |
| `banach_satisfied`      | bool   | mean_contraction_ratio < 1.                                    |

### 6.2 — `depth/higgins_extensions/impulse_response/`

| Field            | Type   | Notes                                                          |
|------------------|--------|----------------------------------------------------------------|
| `amplitude_A`    | float  | Same as `curvature_attractor.amplitude`.                       |
| `depth_delta`    | int    | Curvature tower convergence level.                             |
| `damping_zeta`   | float  | −ln(A_final/A_initial) / depth_delta.                          |
| `classification` | str    | CRITICALLY_DAMPED / LIGHTLY_DAMPED / UNDAMPED / OVERDAMPED_EXTREME / MODERATELY_DAMPED. |

---

## 7 — `diagnostics/`

```
_function:    "review"
_description: "Engine self-checks: EITT residuals, lock events,
               degeneracy flags, content hash."
```

| `coda_standard/`     | `higgins_extensions/`                                                       |
|----------------------|-----------------------------------------------------------------------------|
| `{}` — diagnostics are HUF-engine-specific health checks; they do not correspond to CoDa-canon procedures. | `eitt_residuals/`, `lock_events[]`, `degeneracy_flags[]` |

`content_sha256` (top-level under `diagnostics/`, outside both sub-blocks)
is the reproducibility hash. SHA-256 of the canonicalised JSON with
`metadata.generated`, `metadata.wall_clock_ms`, `metadata.environment`,
and `diagnostics.content_sha256` removed. Two runs of the engine on
identical input produce identical `content_sha256`.

`eitt_residuals/` carries the explicit framing note (Egozcue 2026):
*"Empirical observation of trajectory smoothness under temporal
decimation, not a geometric theorem. Shannon entropy is not
scale-invariant; the apparent preservation reflects compositional
smoothness of the trajectory, not Aitchison invariance."*

---

## 8 — CoDa ↔ Higgins Mapping

Every Higgins extension is a function of `coda_standard/` quantities.
A CoDa reviewer can verify by inspection that the extension reduces to
or builds upon recognised CoDa primitives.

### 8.1 — Higgins extensions defined per record

| Higgins field                    | Equation                                                            | CoDa primitives used        |
|----------------------------------|---------------------------------------------------------------------|----------------------------|
| `higgins_scale`                  | `Hs = 1 - shannon_entropy / ln(D)`                                  | composition, D             |
| `bearing_tensor.pairs[k].theta_deg` | `θ_ij = atan2(clr_j, clr_i)` × (180/π)                            | clr                        |
| `metric_tensor.matrix[i][j]`     | `κ_ij = (δ_ij − 1/D) / (x_i × x_j)` — Aitchison pullback metric     | composition (x), D         |
| `metric_tensor.eigenvalues`      | `eigvals(κ)`                                                        | metric_tensor.matrix       |
| `metric_tensor.trace`            | `tr(κ) = Σ_j (1 − 1/D) / x_j²`                                      | composition, D             |
| `metric_tensor_diagonal[j]`      | `κ_jj = (1 − 1/D) / x_j²`                                            | composition, D             |
| `condition_number`               | `max(x) / min(x)`                                                   | composition                |
| `angular_velocity_deg`           | `ω = atan2(‖clr_t × clr_{t-1}‖, ⟨clr_t, clr_{t-1}⟩)` × (180/π)      | clr at t and t−1           |
| `helmsman`                       | `argmax_j |clr_j(t) − clr_j(t-1)|`                                  | clr at t and t−1           |
| `helmsman_delta`                 | `max_j |clr_j(t) − clr_j(t-1)|`                                     | clr at t and t−1           |

The Aitchison metric κ_ij is part of CoDa (Egozcue & Pawlowsky-Glahn
discussions of the simplex inner product), but the explicit coordinate
form, the bearing tensor reading via atan2, and the helmsman /
condition number diagnostics are Higgins-specific framings.

### 8.2 — Stage 2 / Stage 3 mappings

| Higgins field                                | Equation / Definition                                                  |
|----------------------------------------------|------------------------------------------------------------------------|
| `carrier_pair_examination[k].pearson_r`      | Pearson r on the CLR-projected series for carrier pair (i, j)          |
| `carrier_pair_examination[k].bearing_spread_deg` | `max_t θ_ij(t) − min_t θ_ij(t)` over the trajectory                |
| `carrier_pair_examination[k].locked`         | `bearing_spread_deg < 10°`                                              |
| `triadic_area.results[k].area`               | Heron's formula in CLR space on three time-indexed CLR vectors         |
| `regime_detection.boundaries[k]`             | step indices where `aitchison_distance_step > mean + 2·std`            |

### 8.3 — Bridge mappings

`per_carrier_lyapunov[j].lyapunov_exponent` — heuristic estimate of the
log-divergence rate of the CLR series for carrier j. Not a formal
Lyapunov exponent of a dynamical system; an approximation derived from
the CLR difference series.

`recurrence_analysis.recurrence_rate` — fraction of pairs (a, b) with
`aitchison_distance(x_a, x_b) < 0.1 × max_aitchison_distance` over the
trajectory.

`state_space_model.A_matrix` — least-squares AR(1) fit on the CLR series.

### 8.4 — Depth sounder mappings

The depth sounder is wholly Higgins. Each derived composition is
defined by an explicit equation:

| Field                      | Equation                                                         |
|----------------------------|------------------------------------------------------------------|
| `metric_dual M(x)_j`       | `(1/x_j) / Σ_k (1/x_k)` — involution: M² = identity, clr(M(x)) = −clr(x) |
| `derived_curvature c_j(t)` | `(1/x_j²) / Σ_k (1/x_k²)` — normalised diagonal of the Aitchison metric κ |
| `derived_energy e_j(t)`    | `(Δclr_j)² / Σ_k (Δclr_k)²` — kinetic energy in CLR space, normalised   |
| `level_k composition`      | Output of the previous level passed through the chosen derived constructor |
| `period-2 attractor`       | Empirical: the curvature recursion's Hs trajectory converges to a 2-cycle in 14/19 tested systems. NOT a theorem. |
| `contraction_lyapunov λ`   | `mean_n ln(|Δ(n+2)| / |Δ(n)|)` where Δ(n) = traj[n] − attractor |
| `impulse_response.A`       | `|c_even − c_odd|` — peak-to-peak attractor displacement         |
| `impulse_response.ζ`       | `−ln(A_final / A_initial) / depth_delta`                         |

### 8.5 — Diagnostics mappings

`eitt_residuals.M_sweep[k].variation_pct` —
`100 × |mean_t H(decimated_t at compression M) − mean_t H(x_t)| / mean_t H(x_t)`

This is an *observation* about compositional trajectory smoothness, not
a CoDa-geometric theorem. The schema records it as such.

`lock_events[k]` — events triggered by simple thresholds on CLR values:

| Event type   | Trigger condition                                         |
|--------------|------------------------------------------------------------|
| DEGEN        | max(clr) − min(clr) < 1e-4 (composition near barycenter)  |
| LOCK-ACQ     | clr_j < −10 with previous clr_j ≥ −10                      |
| LOCK-LOSS    | clr_j < −10 with subsequent clr_j ≥ −10                    |

These are display markers; they do not modify any analysis.

---

## 9 — Schema Validation

An engine is **schema-conformant** if and only if:

1. The output JSON has exactly the seven top-level keys above.
2. Every analytic block (tensor, each stage, bridges, depth, diagnostics)
   carries `_function` (one of: composer, review, formatter, provenance),
   `_description`, `coda_standard`, `higgins_extensions`.
3. All fields marked **REQUIRED** in this document are present.
4. All fields have the declared type.
5. `metadata/schema_version` matches the schema version in this document.
6. Numerical sanity holds (closure to 1 ± 1e-15, CLR sums to 0 ± 1e-14,
   M² residual < 1e-10).
7. `diagnostics/content_sha256` reproduces under re-run.

Conformant viewers can rely on the schema as a contract. Non-conformant
JSON is rejected at the viewer's input gate.

---

## 10 — Schema Versioning Policy

| Action                                       | Version bump |
|----------------------------------------------|--------------|
| Add a new optional field                     | minor (2.0 → 2.1)  |
| Add a new REQUIRED field                     | major (2.x → 3.0)  |
| Remove a field                               | major              |
| Change a field's type                        | major              |
| Move a field between coda_standard/higgins_extensions | major     |
| Move a field between functional blocks       | major              |
| Tighten a field's allowed values             | major              |
| Loosen a field's allowed values              | minor              |
| Fix typo in field description                | patch (2.0.0 → 2.0.1) |

A viewer that declares `min_schema_version: 2.0.0` works with all 2.x.x.

---

## Migration from 1.0.0

| 1.0.0 path                                       | 2.0.0 path                                                       |
|--------------------------------------------------|-------------------------------------------------------------------|
| `tensor.timesteps[i].composition`                | `tensor.timesteps[i].coda_standard.composition`                  |
| `tensor.timesteps[i].clr`                        | `tensor.timesteps[i].coda_standard.clr`                          |
| `tensor.timesteps[i].ilr`                        | `tensor.timesteps[i].coda_standard.ilr`                          |
| `tensor.timesteps[i].shannon_entropy`            | `tensor.timesteps[i].coda_standard.shannon_entropy`              |
| `tensor.timesteps[i].aitchison_norm`             | `tensor.timesteps[i].coda_standard.aitchison_norm`               |
| `tensor.timesteps[i].aitchison_distance_step`    | `tensor.timesteps[i].coda_standard.aitchison_distance_step`     |
| `tensor.timesteps[i].higgins_scale`              | `tensor.timesteps[i].higgins_extensions.higgins_scale`           |
| `tensor.timesteps[i].bearing_tensor`             | `tensor.timesteps[i].higgins_extensions.bearing_tensor`          |
| `tensor.timesteps[i].metric_tensor`              | `tensor.timesteps[i].higgins_extensions.metric_tensor`           |
| `tensor.timesteps[i].metric_tensor_diagonal`     | `tensor.timesteps[i].higgins_extensions.metric_tensor_diagonal`  |
| `tensor.timesteps[i].condition_number`           | `tensor.timesteps[i].higgins_extensions.condition_number`        |
| `tensor.timesteps[i].angular_velocity_deg`       | `tensor.timesteps[i].higgins_extensions.angular_velocity_deg`    |
| `tensor.timesteps[i].helmsman`                   | `tensor.timesteps[i].higgins_extensions.helmsman`                |
| `tensor.timesteps[i].helmsman_delta`             | `tensor.timesteps[i].higgins_extensions.helmsman_delta`          |
| `stages.stage1.section_atlas`                    | `stages.stage1.higgins_extensions.section_atlas`                 |
| `stages.stage1.metric_ledger`                    | `stages.stage1.higgins_extensions.metric_ledger`                 |
| `stages.stage2.variation_matrix`                 | `stages.stage2.coda_standard.variation_matrix`                   |
| `stages.stage2.carrier_pair_examination`         | `stages.stage2.higgins_extensions.carrier_pair_examination`      |
| `stages.stage3.subcomposition_ladder`            | `stages.stage3.coda_standard.subcomposition_ladder`              |
| `stages.stage3.{triadic_area,carrier_triads,regime_detection}` | `stages.stage3.higgins_extensions.{...}`         |
| `bridges.information_theory`                     | `bridges.coda_standard.information_theory`                       |
| `bridges.dynamical_systems`                      | `bridges.higgins_extensions.dynamical_systems`                   |
| `bridges.control_theory`                         | `bridges.higgins_extensions.control_theory`                      |
| All `depth.*` (involution_proof, level_0, towers, attractor, IR, summary, cycles) | `depth.higgins_extensions.{...}`               |
| All `diagnostics.*` (eitt_residuals, lock_events, degeneracy_flags) | `diagnostics.higgins_extensions.{...}`                |
| `diagnostics.content_sha256` (top-level)         | `diagnostics.content_sha256` (unchanged — outside the sub-blocks) |

---

*The instrument reads. The expert decides. The loop stays open.*
*The JSON is the read. The viewer is the eye. The schema is the
contract between them. Two classifications — by ownership and by
function — let CoDa reviewers, HUF practitioners, and downstream
viewers find the fields they need without reading past what they don't.*
