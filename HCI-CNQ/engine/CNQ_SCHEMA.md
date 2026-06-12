# CNQ JSON Schema v1.0.0

**Engine:** `HCI-CNQ/engine/cnq.py`
**Version:** 1.0.0 (push #26, 2026-05-08)
**Determinism contract:** see `hashing.py`. Two runs on the same CNT JSON produce identical `cnq_content_sha256`.

---

## Top-level structure

```
{
  "metadata":                   { ... }    # engine identity + clock (clock excluded from hash)
  "provenance":                 { ... }    # parent CNT hash + source file hash
  "cnt_diagnostics_carried_forward": { ... }  # CNT termination, IR class, etc., copied
  "cnq_view":                   { ... }    # the actual CNQ computation
  "cnq_content_sha256":         "..."      # hash of the canonical payload
}
```

## metadata

| Field | Type | Description |
|---|---|---|
| `schema` | str | Always `"cnq/1.0.0"` for this engine version. |
| `engine` | str | `"HCI-CNQ"`. |
| `engine_version` | str | Semver of `cnq.py`. |
| `generated` | str | UTC ISO-8601 timestamp. **Stripped from the hashed payload.** |
| `principle` | str | `"CNT measures invariance. CNQ names the algebra it lives in."` |

## provenance

| Field | Type | Description |
|---|---|---|
| `parent_engine` | str | `"HCI-CNT"`. |
| `parent_engine_version` | str | Semver of the cnt.py that produced the input. |
| `parent_schema` | str | Schema string of the parent CNT JSON. |
| `parent_cnt_content_sha256` | str | The CNT JSON's content hash. **The provenance chain.** |
| `source_file_sha256` | str | SHA-256 of the raw CSV input, when known. |
| `cnt_json_path` | str/null | Path to the CNT JSON consumed (informational). |
| `input_csv_path` | str/null | Path to the raw CSV (informational). |

## cnt_diagnostics_carried_forward

Copied verbatim from the parent CNT JSON. CNQ does NOT recompute these.

| Field | Type | Description |
|---|---|---|
| `cnt_termination` | str | e.g. `LIMIT_CYCLE_P2`. |
| `ir_class` | str | e.g. `OVERDAMPED_EXTREME`, `LIGHTLY_DAMPED`. |
| `amplitude_A` | float/null | CNT amplitude channel. |
| `damping_zeta` | float/null | CNT damping channel. |
| `helmsman_sigma` | mixed/null | Helmsman channel value. |

## cnq_view

The quaternion-native computation. Fields:

| Field | Type | Description |
|---|---|---|
| `dimension_policy` | obj | `{D, label, algebra, processing, claim_strength}`. See policy table below. |
| `n_records_T` | int | Trajectory length. |
| `n_carriers_D` | int | Carrier count. |
| `carrier_names` | list[str] | Carrier labels. |
| `frame_type` | str | `"Helmert orthonormal contrast (legacy QD convention)"` |
| `frame_signature` | str | Description of the Helmert sign convention used. |
| `projection_to_R3` | obj | `{method, note}` — how the trajectory was put into R^3. |
| `captured_step_fraction` | float | Per ChatGPT round-2 audit. 1.0 for D=4 native; <1.0 for projected high-D. |
| `quaternion_path` | obj | The per-step quaternions and the residual summary. |
| `radii` | obj | `{min, max, mean}` of the unit-vector radii before normalization. |

### dimension_policy labels

| `label` | Triggers when | Claim strength |
|---|---|---|
| `native_quaternion` | D == 4 | confirmed (load-bearing) |
| `boundary_or_degenerate_support` | D == 3 | consistency support (not native proof) |
| `degenerate_below_quaternion` | D == 2 | bearing only; quaternion view does not apply |
| `bi_quaternion_factoring_candidate` | D == 8 | experimental; pending pilot (INV-029) |
| `reduced_or_projected` | D >= 5 (and != 8) | projection diagnostic; full Cl(D-1) deferred |

### quaternion_path

| Field | Type | Description |
|---|---|---|
| `n_pairs_tested` | int | T - 1. |
| `max_residual` | float | L-infinity max of \|q v q* - v_next\| over all steps. |
| `mean_residual` | float | Mean of the per-step L-infinity residuals. |
| `gate_threshold` | float | Always `1e-12` in v1.0.0. |
| `gate_pass` | bool | `max_residual <= gate_threshold`. |
| `per_step` | list[obj] | Per-step ledger (see below). |

Each `per_step` entry:
```
{
  "t":            int,      # step index 0..T-2
  "u_start":      [x,y,z],  # unit vector at t
  "u_end":        [x,y,z],  # unit vector at t+1
  "q_w": float, "q_x": float, "q_y": float, "q_z": float,  # rotation quaternion
  "angle_rad":    float,    # 2 * atan2(||q_xyz||, q_w)
  "residual_linf": float    # max |q v q* - u_end|
}
```

## Determinism

The `cnq_content_sha256` is computed over the entire payload AFTER stripping `metadata.generated` (and any other clock-dependent fields). The serializer enforces:

- `sort_keys=True`
- `separators=(",", ":")`
- `ensure_ascii=True`
- `allow_nan=False`

Cross-platform reproduction: any AI platform or third-party reviewer can run `cnq.py` against the same CNT JSON on Linux / macOS / Windows / Python 3.9-3.13 and produce a bit-identical `cnq_content_sha256`. This is the fourth independent confirmation channel in the framework's verification stack.

## Provenance chain

```
raw CSV
  -> source_file_sha256 (SHA-256 of CSV bytes)
  -> CNT engine
  -> CNT JSON
  -> parent_cnt_content_sha256 (CNT determinism contract)
  -> CNQ engine
  -> CNQ JSON
  -> cnq_content_sha256 (CNQ determinism contract)
```

Three hashes. Three independent verification points. If any of them changes, the chain breaks visibly.
