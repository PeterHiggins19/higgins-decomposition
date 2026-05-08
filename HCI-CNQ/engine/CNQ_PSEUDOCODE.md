# CNQ Engine Pseudocode — language-agnostic algorithm reference

**Schema version:** 1.0.0
**Engine version:** 1.0.0
**Reference implementations:** [`cnq.py`](cnq.py) (Python), [`cnq.R`](cnq.R) (R)
**Schema doc:** [`CNQ_SCHEMA.md`](CNQ_SCHEMA.md)
**Notation:** see [`../../HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md`](../../HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md)

This document is the **canonical algorithm**. The Python and R reference implementations are faithful translations of the steps below. Any future port (Julia, Rust, JavaScript, C++) must reproduce the bit-identical `cnq_content_sha256` on the same CNT JSON input — that is the conformance test.

---

## 1. Inputs

The engine accepts two equivalent input modes:

```
INPUT MODE A (preferred):
    cnt_json_path       — path to an existing CNT JSON
    input_csv_path      — optional, used as fallback if CNT JSON does not store input rows

INPUT MODE B (CNT not yet run):
    input_csv_path      — path to a CCTT-style CSV
    repo_root           — path to the higgins-decomposition repo (or its Hs/ subdir)
    cnt_engine          — optional override for cnt.py location

Either cnt_json_path or input_csv_path MUST be provided.
```

The CSV format is CCTT-standard: first column is a label (time index, ID, multipole, etc.), remaining columns are positive carrier values. D = number of carrier columns. T = number of data rows.

---

## 2. Top-level flow

```
function run_cnq(cnt_json_path, input_csv_path, out_path, repo_root, cnt_engine):
    # Step A: ensure we have a CNT JSON
    if cnt_json_path is None:
        repo_root := find_repo_root(repo_root)            # walk up for .git / HCI-CNT marker
        cnt_engine := find_cnt_engine(repo_root, cnt_engine)
        cnt_json_path := out_path with suffix ".cnt.json"
        run_cnt(input_csv_path, cnt_json_path, cnt_engine)

    # Step B: load the CNT JSON, extract diagnostics
    cnt_json := load_json(cnt_json_path)
    cnt_diag := extract_cnt_diagnostics(cnt_json)         # parent_cnt_content_sha256, IR class, etc.

    # Step C: get the row-level data
    carriers, rows := reconstruct_compositions_from_cnt(cnt_json)
    if rows is None:
        if input_csv_path is None:
            raise "CNT JSON does not contain input rows; supply --input-csv"
        carriers, rows := read_csv_compositions(input_csv_path)

    # Step D: classify dimension and compute the CNQ view
    D := number of columns in rows
    policy := classify_dimension(D)                       # see §4
    cnq_view := run_cnq_view(rows, carriers, policy)      # see §5

    # Step E: assemble the deterministic output
    payload := assemble_cnq_output(cnt_json, cnt_diag, cnq_view, ...)
    cnq_hash := canonical_sha256(payload)                 # see §7
    payload.cnq_content_sha256 := cnq_hash

    # Step F: write to disk (sorted keys, indent=2, ascii-safe)
    write_json(payload, out_path)
    return payload
```

---

## 3. Geometry primitives

These are the load-bearing math operations. Both reference implementations use the same conventions.

### 3.1 Aitchison closure

```
function closure(x):                                      # x: D-vector, all positive
    return x / sum(x)
```

### 3.2 Centred log-ratio (CLR)

```
function clr(x):                                          # x: closed composition
    g := exp(mean(log(x)))                                # geometric mean
    return log(x / g)                                     # sums to zero
```

### 3.3 Helmert orthonormal contrast matrix

The framework's canonical ILR basis. Row k (zero-indexed, k ∈ {0, ..., D-2}):

```
function helmert_basis(D):                                # returns (D-1) x D matrix
    H := zero matrix of shape (D-1, D)
    for k from 0 to D-2:
        n := k + 1
        norm := 1 / sqrt(n * (n + 1))
        for j from 0 to n-1:
            H[k, j] := norm                               # k+1 entries of +norm
        H[k, n] := -n * norm                              # one entry of -n*norm
        # remaining entries stay zero
    return H
```

This convention matches the legacy `QD_round_2.py` Helmert basis exactly. Any port using a different ILR basis (e.g. principal-axis ILR or named scientific balances) MUST declare the alternate `frame_signature` in its CNQ output and SHOULD NOT claim bit-identical reproduction with the canonical Helmert frame.

### 3.4 Quaternion algebra

Quaternions are stored as `(w, x, y, z)` with `w` as the scalar part.

```
function quat_from_axis_angle(axis, angle):
    if norm(axis) < 1e-15:
        return (1, 0, 0, 0)                               # identity
    axis := axis / norm(axis)
    half := angle / 2
    return (cos(half), sin(half) * axis[0],
                       sin(half) * axis[1],
                       sin(half) * axis[2])

function quat_conj(q):
    return (q[0], -q[1], -q[2], -q[3])

function quat_mul(p, q):                                  # Hamilton product
    return (
        p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3],
        p[0]*q[1] + p[1]*q[0] + p[2]*q[3] - p[3]*q[2],
        p[0]*q[2] - p[1]*q[3] + p[2]*q[0] + p[3]*q[1],
        p[0]*q[3] + p[1]*q[2] - p[2]*q[1] + p[3]*q[0]
    )

function quat_rotate(q, v):                               # sandwich product q v q*
    p := (0, v[0], v[1], v[2])                            # lift v to a pure-vector quaternion
    rotated := quat_mul(quat_mul(q, p), quat_conj(q))
    return rotated[1:4]                                   # drop scalar part
```

### 3.5 Rotation quaternion between two unit 3-vectors (atan2-stable)

This is the load-bearing operation. The atan2 form is numerically stable in regimes where `arccos(dot)` would lose precision.

```
function rotation_quaternion_between(u1, u2, eps = 1e-15):
    u1 := u1 / norm(u1)
    u2 := u2 / norm(u2)
    dot := clip(dot_product(u1, u2), -1, 1)

    if dot > 1 - eps:
        return (1, 0, 0, 0)                               # already aligned

    if dot < -1 + eps:
        # antiparallel: pick any axis perpendicular to u1
        axis := cross_product(u1, (1, 0, 0))
        if norm(axis) < 1e-10:
            axis := cross_product(u1, (0, 1, 0))
        axis := axis / norm(axis)
        return quat_from_axis_angle(axis, pi)

    cross := cross_product(u1, u2)
    angle := atan2(norm(cross), dot)                      # the atan2-stable form
    return quat_from_axis_angle(cross, angle)
```

---

## 4. Dimension policy

Every CNQ output declares an explicit dimension label. Behaviour depends on D:

```
function classify_dimension(D):
    if D == 4:
        label := "native_quaternion"                      # confirmed, load-bearing
        algebra := "SU(2) double cover of SO(3); Aitchison rotation in R^3"
        processing := "Helmert -> R^3 -> unit-quaternion sandwich"

    elif D == 3:
        label := "boundary_or_degenerate_support"         # consistency channel
        algebra := "SO(2)-equivalent in R^2; promoted to R^3 by zero-padding"
        processing := "Helmert -> R^2 -> embed in R^3 with z=0 -> sandwich"

    elif D == 2:
        label := "degenerate_below_quaternion"            # bearing only
        algebra := "scalar log-ratio only; no rotation degree of freedom"
        processing := "bearing computation only"

    elif D == 8:
        label := "bi_quaternion_factoring_candidate"      # DEFERRED INV-029
        algebra := "SO(8) sup SU(2) x SU(2); two coupled quaternion paths"
        processing := "Helmert -> R^7; reduced view = first 3 axes; "
                      "twin-quaternion factoring scaffolded but DEFERRED"
        # NOTE: 'twin-quaternion' is the formal name per
        # NOTATION_AND_TERMINOLOGY.md §7. Legacy 'bi-quaternion' kept for
        # the dimension label only.

    elif D >= 5:                                          # D in {5, 6, 7, 9, 10, ...}
        label := "reduced_or_projected"
        algebra := "SO(D-1); projection to first 3 ILR axes"
        processing := "Helmert -> R^(D-1) -> first 3 axes -> sandwich (lossy)"

    else:                                                 # D = 0 or 1
        label := "unsupported"

    return { D, label, algebra, processing, claim_strength: ... }
```

---

## 5. CNQ view computation

The core of the engine. Given the row-level compositions and the dimension policy, compute the quaternion-native view.

```
function run_cnq_view(rows, carriers, policy):
    T, D := shape of rows

    # Step 5a: closure -> CLR -> Helmert (full ILR projection)
    closed := [closure(row) for row in rows]              # (T, D)
    clr_vecs := [clr(c) for c in closed]                  # (T, D), each row sums to 0
    H := helmert_basis(D)                                 # (D-1, D)
    ilr := clr_vecs @ H.T                                 # (T, D-1)

    # Step 5b: project to R^3 according to dimension policy
    if D == 4:
        ilr3 := ilr                                       # already R^3, exact
    elif D == 3:
        ilr3 := stack(ilr, zero_column(T))                # (T, 2) -> (T, 3) with z=0
    elif D == 2:
        return { dimension_policy: policy,
                 quaternion_path: None,
                 bearing_only: { ilr: ilr_flatten,
                                 note: "D=2 has no rotation DOF" } }
    else:                                                 # D >= 5 (incl. D=8)
        ilr3 := first 3 columns of ilr                    # lossy projection

    # Step 5c: captured energy fraction (per ChatGPT round-2 audit)
    if D in {2, 3, 4}:
        captured_step_fraction := 1.0
    else:
        full_steps := diff along time axis of ilr         # (T-1, D-1)
        red_steps := diff along time axis of ilr3         # (T-1, 3)
        full_norm2 := sum of squares per row of full_steps
        red_norm2 := sum of squares per row of red_steps
        ratio := where full_norm2 > 1e-30:
                     red_norm2 / full_norm2
                 else:
                     1.0
        captured_step_fraction := mean(ratio)

    # Step 5d: normalize to S^2
    radii3 := [norm(v) for v in ilr3]                     # (T,)
    units := [v / r if r > 1e-15 else (0,0,0)
              for v, r in zip(ilr3, radii3)]              # (T, 3)

    # Step 5e: per-step quaternion sandwich reconstruction
    n_pairs := T - 1
    residuals := []                                       # length T-1
    quats := []                                           # length T-1
    angles := []                                          # length T-1
    for t from 0 to T-2:
        q := rotation_quaternion_between(units[t], units[t+1])
        u_reconstructed := quat_rotate(q, units[t])
        residuals[t] := max_abs(u_reconstructed - units[t+1])   # L-infinity
        quats[t] := q
        angles[t] := 2 * atan2(norm(q[1:4]), q[0])

    # Step 5f: gate
    max_residual := max(residuals)                        # if n_pairs > 0 else NaN
    mean_residual := mean(residuals)
    gate_threshold := 1e-12
    gate_pass := max_residual <= gate_threshold

    # Step 5g: per-step ledger
    per_step := []
    for t from 0 to n_pairs - 1:
        per_step.append({
            t, u_start: units[t], u_end: units[t+1],
            q_w: quats[t][0], q_x: quats[t][1],
            q_y: quats[t][2], q_z: quats[t][3],
            angle_rad: angles[t], residual_linf: residuals[t]
        })

    return {
        dimension_policy: policy,
        n_records_T: T,
        n_carriers_D: D,
        carrier_names: carriers,
        frame_type: "Helmert orthonormal contrast (legacy QD convention)",
        frame_signature: "row k: 1/sqrt(k(k+1)) [k blocks of +1, then -k]",
        projection_to_R3: { method, note: capture_note },
        captured_step_fraction,
        quaternion_path: {
            n_pairs_tested: n_pairs,
            max_residual, mean_residual,
            gate_threshold, gate_pass,
            per_step
        },
        radii: { min, max, mean }
    }
```

---

## 6. Output assembly

```
function assemble_cnq_output(cnt_json, cnt_diag, cnq_view, cnt_json_path, input_csv_path):
    parent_hash := cnt_diag.content_sha256
    source_hash := cnt_diag.source_file_sha256
    if input_csv_path provided and source_hash is None:
        source_hash := file_sha256(input_csv_path)

    payload := {
        metadata: {
            schema: "cnq/1.0.0",
            engine: "HCI-CNQ",
            engine_version: "1.0.0",
            generated: utc_iso8601_now(),                 # STRIPPED from hash
            principle: "CNT measures invariance. CNQ names the algebra it lives in."
        },
        provenance: {
            parent_engine: "HCI-CNT",
            parent_engine_version: cnt_diag.cnt_engine_version,
            parent_schema: cnt_diag.cnt_schema_version,
            parent_cnt_content_sha256: parent_hash,
            source_file_sha256: source_hash,
            cnt_json_path, input_csv_path
        },
        cnt_diagnostics_carried_forward: {
            cnt_termination, ir_class,
            amplitude_A, damping_zeta, helmsman_sigma
        },
        cnq_view
    }

    # Now hash and patch back in
    cnq_hash := canonical_sha256(payload)
    payload.cnq_content_sha256 := cnq_hash
    return payload
```

---

## 7. Determinism contract (canonical hashing)

This is the critical contract: any platform implementing the algorithm must produce bit-identical `cnq_content_sha256`.

```
function canonical_sha256(payload):
    stripped := strip_volatile_fields(payload)
    canonical_string := json_dumps(
        stripped,
        sort_keys = True,
        separators = (",", ":"),                          # no whitespace
        ensure_ascii = True,
        allow_nan = False
    )
    return sha256_hex(canonical_string.encode("utf-8"))

function strip_volatile_fields(obj):
    # Recursively remove clock-dependent fields. Returns a deep copy.
    EXCLUDED := {"generated", "timestamp", "wall_clock", "_run_clock"}
    if isinstance(obj, dict):
        return { k: strip_volatile_fields(v)
                 for k, v in obj.items()
                 if k not in EXCLUDED }
    if isinstance(obj, list):
        return [ strip_volatile_fields(v) for v in obj ]
    return obj
```

**Float handling.** Floats are serialised by the host language's default `json.dumps` (Python) or `jsonlite::toJSON` (R) representation of float64. As long as both implementations emit the same canonical decimal representation of each float, hashes match. The reference Python and R implementations have been tested to produce identical hashes on the three confirmation experiments.

**Float drift contingency.** If a port emits a different decimal representation (e.g. extra trailing zeros, scientific-notation differences), the hashes will differ even though the numerical content is identical. Such ports should document their exact float-formatting policy and provide a translation layer when claiming bit-identical reproduction.

---

## 8. CLI surface (both reference implementations)

```
USAGE:
    cnq.py --cnt-json PATH [--input-csv PATH] --out PATH
    cnq.py --input-csv PATH [--cnt-json PATH] --out PATH [--repo-root PATH] [--cnt-engine PATH]

    Rscript cnq.R --cnt-json PATH [--input-csv PATH] --out PATH
    Rscript cnq.R --input-csv PATH [--cnt-json PATH] --out PATH [--repo-root PATH] [--cnt-engine PATH]

ARGUMENTS:
    --cnt-json PATH    Path to existing CNT JSON (preferred; skips CNT invocation)
    --input-csv PATH   Path to CCTT-style CSV (required if --cnt-json omitted, fallback otherwise)
    --out PATH         Output CNQ JSON path
    --repo-root PATH   Hs/ root override (auto-detected if omitted)
    --cnt-engine PATH  cnt.py location override (auto-detected via cnt_adapter)

EXIT CODES:
    0    success
    2    error (path not found, ValueError, RuntimeError; message printed to stderr)
```

---

## 9. Cross-platform conformance test

Two implementations are conformant if:

1. They produce the same `max_residual` to ≤ 1 ULP on the three published confirmation experiments (Backblaze D=4, Planck CMB D=4, SM Neutrino D=3).
2. They produce identical `parent_cnt_content_sha256` (carried forward from CNT JSON byte-for-byte).
3. They produce identical `cnq_content_sha256` after the canonical-JSON serialization.

The reference Python implementation produces, on Linux x86_64 / Python 3.10 / numpy 1.x:

| Experiment | max_residual | cnq_content_sha256 |
|---|---|---|
| Planck CMB D=4 | 4.440892098500626e-16 | `927af6a381f425945475a914d72c0c63812ee571701079b66a642bd114075b64` |
| SM Neutrino D=3 | 3.3306690738754696e-16 | `f64741cb76eef302699c17adebf5fbd1fb4dc1e73b4cf9562997a7afc5154183` |

(Backblaze D=4 added on first cnq.py corpus run; pending in `expected_results.json`.)

If your port produces the same `max_residual` but a different `cnq_content_sha256`, the discrepancy lives in the float-formatting layer, not in the math. File a GitHub issue with platform details + observed hash; this is a finding, not a failure.

---

## 10. Tests every port should pass

| Test | Contract |
|---|---|
| `test_determinism` | Two consecutive runs on the same CNT JSON produce identical `cnq_content_sha256` |
| `test_first_principles` | A hand-constructed D=4 trajectory with known rotation produces expected residual, expected dimension label, expected gate pass |
| `test_dimension_policy` | D=2,3,4,5,8,9 each produce the correct `dimension_policy.label` |
| `test_provenance_chain` | `parent_cnt_content_sha256` in CNQ output matches `diagnostics.content_sha256` in input CNT JSON |
| `test_cross_language_parity` (Python ↔ R) | Same input → same `max_residual` to 1 ULP and same `cnq_content_sha256` |

---

## Cross-references

- Canonical Python reference: [`cnq.py`](cnq.py)
- Canonical R reference: [`cnq.R`](cnq.R)
- Output schema: [`CNQ_SCHEMA.md`](CNQ_SCHEMA.md)
- Geometry primitives module: [`geometry.py`](geometry.py)
- Hashing contract module: [`hashing.py`](hashing.py)
- CNT adapter module: [`cnt_adapter.py`](cnt_adapter.py)
- Notation: [`../../HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md`](../../HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md)
- Scope and limits: [`../CNQ_SCOPE_AND_LIMITS.md`](../CNQ_SCOPE_AND_LIMITS.md)
- Claim strength: [`../CLAIM_STRENGTH_TABLE.md`](../CLAIM_STRENGTH_TABLE.md)
