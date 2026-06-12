# CNT Engine Pseudocode — language-agnostic algorithm reference

**Schema version:** 3.1.0
**Engine version:** 3.1.0 (Python canonical; R port at 3.0.0, v3.1.0 parity queued as EngPromo-2)
**Reference implementations:** [`cnt.py`](cnt.py) (Python), [`cnt.R`](cnt.R) (R)
**Schema / theory:** [`../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) Part E
**Notation:** [`../handbook/NOTATION_AND_TERMINOLOGY.md`](../handbook/NOTATION_AND_TERMINOLOGY.md), [`../handbook/GLOSSARY.md`](../handbook/GLOSSARY.md) v3.0
**Sibling pseudocode:** [`../../HCI-CNQ/engine/CNQ_PSEUDOCODE.md`](../../HCI-CNQ/engine/CNQ_PSEUDOCODE.md)

This document is **the canonical algorithm** for the CNT engine. The Python and R reference implementations are faithful translations of the steps below. Any future port (Julia, Rust, JavaScript, C++, Fortran, …) must reproduce the bit-identical `content_sha256` on the canonical reference inputs — that is the **conformance test**.

> **Purpose for the skeptical reader.** If you do not wish to run the published Python or R code, you can re-implement the engine in your own language using only this document. Then run your implementation against the canonical reference inputs (Backblaze fleet, Planck CMB photon power, SM neutrino oscillation — all hashed and pinned in [`../../HCI-CNQ/experiments/`](../../HCI-CNQ/experiments/)). Compute your output's `content_sha256` and compare against the published value. **If the hashes match, the published code is faithful to this pseudocode.** If they differ, either your implementation has a bug or this pseudocode has an ambiguity worth filing as an issue. The framework's IEEE-floor convergence on Backblaze and Planck (`max_residual = 4.441 × 10⁻¹⁶`, bit-identical on physically unrelated datasets) is the operational proof that the algorithm itself produces a measurable invariant — independent of language, OS, or BLAS.

---

## 1. Inputs

The engine consumes a CSV with one label column and D ≥ 2 carrier columns of positive numeric values.

```
input_csv_path     — path to CSV file
out_path           — path to write the output JSON (optional; if None, derived from input_csv_path)

CSV format:
    row 1:           header — first cell is the label column name; remaining cells are carrier names
    row 2..N+1:      data rows — first cell is the label (timestamp, year, ID, multipole index, etc.);
                                 remaining cells are positive floats representing the carrier values
                                 at that label

Constraints:
    D                ≥ 2     (number of carrier columns)
    T                ≥ 2     (number of data rows)
    all carrier values:  strictly positive (zeros are replaced by multiplicative zero replacement at ε = 1e-10)
    carrier names:       distinct, non-empty strings
    labels:              order-preserving (engine treats row order as time order unless overridden)
```

The CSV format is shared with the CCTT v1.0 standard ([`../../ai-refresh/CCTT_RUNBOOK.md`](../../ai-refresh/CCTT_RUNBOOK.md)). Any CSV that runs through CCTT runs through the engine.

---

## 2. Top-level flow

```
function cnt_run(input_csv_path, out_path):
    # Step A: ingest
    labels, carriers, rows_raw, T := ingest_csv(input_csv_path)         # §3
    D := length(carriers)

    # Step B: closure (Aitchison sense)
    rows_closed := closure(rows_raw)                                     # §4.1
        # rows_closed[t] = rows_raw[t] / sum(rows_raw[t]),  sums to 1.0 per row

    # Step C: log-ratio transforms
    clr_matrix := apply_clr_row_by_row(rows_closed)                      # §4.2
        # clr_matrix[t,j] = log(rows_closed[t,j]) - (1/D) Σ_k log(rows_closed[t,k])
    helmert_basis := make_helmert_basis(D)                               # §4.3
        # (D-1) × D orthonormal contrast matrix; V·Vᵀ = I_{D-1}
    ilr_matrix := helmert_basis @ clr_matrix.T                            # §4.4
        # shape: (D-1, T); the Helmert ILR coordinates

    # Step D: per-step tensor blocks
    timesteps := []
    for t in 0..T-1:
        ts_block := compute_timestep_block(t, rows_closed, clr_matrix, carriers, labels)  # §5
        timesteps.append(ts_block)

    # Step E: stages 1, 2, 3
    stage1 := compute_stage1(clr_matrix, carriers)                       # §6.1
    stage2 := compute_stage2(rows_closed, clr_matrix, carriers)          # §6.2
    stage3 := compute_stage3(timesteps, carriers, rows_closed, clr_matrix) # §6.3

    # Step F: depth tower
    depth_tower := compute_depth_tower(clr_matrix, helmert_basis, carriers)  # §7

    # Step G: navigation 2D (v3.1.0+ addition)
    navigation_2d := compute_navigation_2d(ilr_matrix)                   # §8

    # Step H: diagnostics
    lock_events := detect_lock_events(clr_matrix)                        # §9.1
    degeneracy := degeneracy_flags(rows_closed)                          # §9.2
    eitt := eitt_bench_test(rows_closed)                                 # §9.3

    # Step I: assemble output, hash, write
    output := assemble_output_json(
        labels, carriers, rows_closed, clr_matrix, helmert_basis,
        timesteps, stage1, stage2, stage3, depth_tower, navigation_2d,
        lock_events, degeneracy, eitt
    )
    output.metadata.content_sha256 := sha256(canonical_serialize(output_minus_metadata))  # §10
    write_json(output, out_path)
    return output
```

The pipeline is straight-through: every step depends only on prior steps. There are no implicit globals; every constant lives in the `USER CONFIGURATION` block at the top of `cnt.py` and is echoed in `metadata.engine_config` of every output.

---

## 3. Ingest

```
function ingest_csv(input_csv_path):
    raw := read_csv(input_csv_path)
    labels := raw[:, 0]                          # first column
    carriers := raw[0, 1:]                       # header row, carrier columns
    rows_raw := raw[1:, 1:].astype(float)        # T × D matrix
    T := number of data rows
    return labels, carriers, rows_raw, T
```

Reading is done by a standard CSV parser; the canonical Python implementation uses `numpy.loadtxt` or `pandas.read_csv` with the same numerical behaviour. Any parser that returns IEEE-754 float64 values byte-identically to numpy on the same input file is acceptable.

**Zero replacement.** If any `rows_raw[t,j] = 0`, replace with `ZERO_REPLACEMENT_EPS = 1e-10` *before* closure. This is the multiplicative zero replacement convention from Aitchison (1986); it preserves the closure constraint and produces finite log-ratios.

---

## 4. Closure, CLR, ILR-Helmert

### 4.1 Closure operator

```
function closure(rows):
    return rows / sum(rows, axis=row_axis)
```

For each row t: `rows_closed[t,j] = rows[t,j] / Σ_k rows[t,k]`. After closure, each row sums to exactly 1.0 (within float64 precision; cf. Lemma 8 of the flagship for the corresponding property under CLR).

### 4.2 CLR (centred log-ratio)

```
function clr(p):
    return log(p) - mean(log(p))
```

For a closed row p ∈ Δ^(D−1): `clr_i(p) = log(p_i) − (1/D) Σ_j log(p_j)`. The CLR vector sums to zero (closure invariance under CLR, flagship Lemma 8). Apply this row-by-row across the rows-closed matrix.

### 4.3 Helmert orthonormal basis

```
function make_helmert_basis(D):
    V := zeros((D-1, D))
    for k in 1..D-1:
        for j in 1..D:
            if j ≤ k:        V[k-1, j-1] := -1 / sqrt(k*(k+1))
            elif j == k+1:   V[k-1, j-1] := k / sqrt(k*(k+1))
            else:            V[k-1, j-1] := 0
    return V
```

The Helmert matrix V is (D−1) × D, orthonormal (V · Vᵀ = I_{D−1}), and its rows sum to zero (so V · 1_D = 0). This is the canonical basis used throughout the engine for the ILR transform. Any orthonormal contrast matrix would be valid mathematically, but the Helmert basis is deterministic, well-conditioned, and chosen for reproducibility across teams (no arbitrary basis-rotation choice).

### 4.4 ILR (isometric log-ratio)

```
function ilr(p, V):
    return V @ clr(p)
```

For a closed row p: `ilr(p) = V · clr(p)`, producing a (D−1)-vector in ℝ^(D−1). Across the full T × D rows-closed matrix: `ilr_matrix := V @ clr_matrix.T`, shape (D−1) × T. ILR carries the simplex isometrically into Euclidean space (flagship §13 Glossary "ILR").

---

## 5. Per-step tensor block

For each timestep t ∈ 0..T−1, compute the **timestep block** containing all per-step diagnostics:

```
function compute_timestep_block(t, rows_closed, clr_matrix, carriers, labels):
    p := rows_closed[t, :]              # current composition
    h := clr_matrix[t, :]               # current CLR coordinates

    H := shannon_entropy(p)             # §5.1
    K := k_eff(p)                       # §5.2 = exp(H)
    h_norm := aitchison_norm(h)         # §5.3 = ‖h‖₂
    regime := concentration_regime(p)   # §5.4 (concentrated / dispersed / mid)

    kappa := kappa_HS_full(p)           # §5.5  Higgins Steering Metric Tensor
    s_j := s_j_sensitivity(p)           # §5.6  diagonal carrier sensitivity = 1/p_j

    if t > 0:
        h_prev := clr_matrix[t-1, :]
        d_ait := aitchison_distance(h_prev, h)              # §5.7  ‖h_t − h_{t−1}‖₂
        omega := angular_velocity_deg(h_prev, h)            # §5.8  bearing change (degrees)
        sigma := helmsman_dcdi(h_prev, h)                   # §5.9  helmsman index (1..D)
        tv := tv_distance(rows_closed[t-1,:], p)            # §5.10 total variation
    else:
        d_ait := 0;  omega := 0;  sigma := none;  tv := 0

    bearings := bearing_pairs(h, carriers)                  # §5.11

    # Power Share — added per HUF-STD-002 Order 1 post-conference; in v3.1.0 as STAGED
    # (this block is reserved; v3.x output JSON includes a `power_share` field set to null
    #  pending INV-060 → CANONICAL promotion)

    return {
        "label": labels[t],
        "composition": p,
        "coda_standard": { "clr": h, "shannon_entropy": H, "k_eff": K },
        "higgins_extensions": {
            "metric_tensor": kappa,
            "sensitivity": { "s_j": s_j, "regime": regime },
            "bearing_tensor": { "pairs": bearings },
            "angular_velocity_deg": omega,
            "aitchison_step_norm": d_ait,
            "helmsman_index": sigma,
            "tv_distance_to_prev": tv,
        }
    }
```

The sub-procedures:

### 5.1 Shannon entropy

```
function shannon_entropy(p):
    p_safe := p where p > 0 else ε
    return - sum(p_safe * log(p_safe))
```

The natural-log version (entropy in nats). For p on the simplex with closure, `H ∈ [0, log(D)]`; H = log(D) at the barycenter; H → 0 as p concentrates at a vertex.

### 5.2 Effective number of carriers

```
function k_eff(p):
    return exp(shannon_entropy(p))
```

K_eff ∈ [1, D]; K_eff = D at the barycenter; K_eff → 1 as p concentrates at a vertex.

### 5.3 Aitchison norm

```
function aitchison_norm(clr_vec):
    return sqrt(sum(clr_vec^2))
```

The L₂ norm of the CLR vector. Aitchison-norm-zero ⟺ p is the barycenter ⟺ all carriers equal.

### 5.4 Concentration regime tag

```
function concentration_regime(p):
    if max(p) > 1 - CONCENTRATION_HIGH_THRESHOLD:  return "concentrated"
    elif max(p) < 1/D + CONCENTRATION_LOW_THRESHOLD:  return "dispersed"
    else:                                          return "mid"
```

Default thresholds: `CONCENTRATION_HIGH_THRESHOLD = 0.10` (i.e., one carrier > 90%), `CONCENTRATION_LOW_THRESHOLD = 0.05` (i.e., max within 5 percentage points of equal share). These are config-block constants echoed in metadata.

### 5.5 Higgins Steering Metric Tensor (kappa_HS)

```
function kappa_HS_full(p):
    D := length(p)
    kappa := D × D matrix
    for i in 0..D-1:
        for j in 0..D-1:
            if i == j:  kappa[i,j] := 1 / p[i]^2
            else:       kappa[i,j] := -1 / (p[i] * p[j])
    return {
        "matrix": kappa,
        "trace": sum(diagonal(kappa)) = sum(1/p_i^2),
        "condition_number": condition_number(kappa),
        "diagonal": diagonal(kappa),
    }
```

κᴴˢ is the Order-2 tensor in the Hˢ depth tower. Its diagonal is `1/p_i^2` (which matches the curvature composition convention from CNT v2.0.1); its trace measures the global concentration sensitivity; its condition number measures the carrier-to-carrier coupling.

### 5.6 s_j sensitivity (Order-1)

```
function s_j_sensitivity(p):
    return [1/p_j for p_j in p]
```

The Order-1 (vector) carrier sensitivity. Compare to κᴴˢ diagonal which is `1/p_j^2`; the two relate by `kappa_diag = s_j^2`.

### 5.7 Aitchison distance between consecutive CLR vectors

```
function aitchison_distance(clr_a, clr_b):
    return sqrt(sum((clr_a - clr_b)^2))
```

This is the L₂ distance between the two CLR vectors. By Lemma 8 of the flagship, it is the natural Aitchison distance on the simplex pulled back into Euclidean space.

### 5.8 Angular velocity (bearing change in degrees)

```
function angular_velocity_deg(h_prev, h_curr):
    cos_theta := dot(h_prev, h_curr) / (‖h_prev‖ * ‖h_curr‖)
    cos_theta := clamp(cos_theta, -1.0, 1.0)
    theta_rad := arccos(cos_theta)
    return theta_rad * (180 / π)
```

The angle between two consecutive CLR vectors, in degrees. Zero when the composition direction is unchanged; 180° when the composition reverses.

### 5.9 Helmsman index

```
function helmsman_dcdi(h_prev, h_curr):
    delta := h_curr - h_prev
    return argmax(|delta|)        # 1-indexed: returns the carrier index with the largest |Δclr|
```

The carrier index whose CLR coordinate moved the most in the current step. This is the *Helmsman of the step* — which carrier is steering the trajectory.

### 5.10 Total variation distance

```
function tv_distance(p_a, p_b):
    return 0.5 * sum(|p_a - p_b|)
```

The TV distance between two compositions; ∈ [0, 1]. Standard.

### 5.11 Bearing pairs

```
function bearing_pairs(h, carriers):
    D := length(carriers)
    pairs := []
    for i in 0..D-1:
        for j in i+1..D-1:
            theta := atan2(h[j], h[i]) * (180/π)         # atan2 — see GLOSSARY §27
            pairs.append({"carrier_i": carriers[i], "carrier_j": carriers[j], "theta_deg": theta})
    return pairs
```

For every unordered pair (i, j) of carriers, the bearing angle θ_ij in the CLR plane. `atan2` is used (not `atan`) to preserve quadrant information and to be safe around ±π boundary (cf. flagship pattern map row 5).

---

## 6. Stages 1, 2, 3

The Stage outputs are *atlas* views — distillations of the full trajectory into per-stage diagnostics that the CNT plate family visualises (Output Doctrine v1.0 §4).

### 6.1 Stage 1 — Section / atlas

```
function compute_stage1(clr_matrix, carriers):
    var_mat := variation_matrix(closed_from_clr(clr_matrix))     # symmetric D×D
    total_variation := sum(upper_triangle(var_mat))
    return {
        "variation_matrix": var_mat,
        "total_variation": total_variation,
        "carriers": carriers,
    }
```

The variation matrix entry `var_mat[i,j] = Var(log(p_i / p_j))` is the canonical CoDa Stage-1 statistic. The total variation is `Σ_{i<j} var_mat[i,j]`.

### 6.2 Stage 2 — Bearing + regime + triadic

```
function compute_stage2(rows_closed, clr_matrix, carriers):
    triadic := compute_triadic_examinations(rows_closed)         # examine triads of carriers
    regime := classify_regime_temporal(clr_matrix)               # temporal regime taxonomy
    return {
        "triadic_examinations": triadic,
        "temporal_regime": regime,
        ...
    }
```

For Stage 2's complete formal definition see [`../conference_demo/cnt_demo/05_doctrine/STAGE2_PSEUDOCODE.md`](../conference_demo/cnt_demo/05_doctrine/STAGE2_PSEUDOCODE.md). The Stage 2 algorithm is locked at Order 2 of HUF-STD-002 since 2026-05-05.

### 6.3 Stage 3 — Depth tower + attractor + IR class

```
function compute_stage3(timesteps, carriers, rows_closed, clr_matrix):
    fp := fit_attractor(clr_matrix)              # §7 below; period-2 attractor fit
    ir := ring_classify(higgins_scale_traj)      # §6.4 IR taxonomy
    return {
        "depth_tower_summary": ...,
        "fit_attractor": fp,
        "ir_class": ir,
    }
```

Stage 3 wraps the depth-tower work (§7) and produces the IR (Implicit Regime) classification.

### 6.4 IR class taxonomy (`ring_classify`)

```
function ring_classify(higgins_scale_value):
    hs := higgins_scale_value
    if hs > IR_THRESHOLDS["chaotic"]:                    return "CHAOTIC"
    elif hs > IR_THRESHOLDS["lightly_damped"]:           return "LIGHTLY_DAMPED"
    elif hs > IR_THRESHOLDS["overdamped"]:               return "OVERDAMPED"
    elif hs > IR_THRESHOLDS["overdamped_extreme"]:       return "OVERDAMPED_EXTREME"
    elif energy_depth_reached_max:                        return "ENERGY_STABLE_FIXED_POINT"
    elif curvature_vertex_flat:                           return "CURVATURE_VERTEX_FLAT"
    elif D == 2:                                          return "D2_DEGENERATE"
    else:                                                 return "LIMIT_CYCLE_P2"   # default for period-2 attractors
```

The IR taxonomy split (`ENERGY_STABLE_FIXED_POINT` / `CURVATURE_VERTEX_FLAT` / `D2_DEGENERATE`) was introduced in CNT v2.0.3; the v3.x engine retains it. Thresholds in `IR_THRESHOLDS` config block.

---

## 7. Depth tower (energy + curvature)

```
function compute_depth_tower(clr_matrix, helmert_basis, carriers):
    L := list of levels, each a level dictionary
    h_current := clr_matrix
    for level in 0..DEPTH_MAX_LEVELS:
        e := energy_level(h_current)              # §7.1
        c := curvature_level(h_current)           # §7.2
        L.append({ "level": level, "energy": e, "curvature": c })
        if level_converged(L, level):  break       # §7.3
        h_current := decimate(h_current)           # §7.4 — coarse-grain by 2:1

    p2 := fit_p2_attractor(L)                     # §7.5 — period-2 attractor fit
    m2_sample := compute_m2_involution_sample(L)  # §7.6 — M² = I check

    return {
        "levels": L,
        "p2_attractor": p2,
        "m2_involution_sample": m2_sample,
    }
```

The depth tower is the multi-scale recursion that defines the framework's "depth" axis. At each level the trajectory is coarse-grained 2:1; the energy and curvature levels are computed; convergence is tested.

### 7.1 Energy level

```
function energy_level(h_matrix):
    return mean across t of ‖h[t]‖²
```

The mean squared CLR norm at the current level — the level's compositional "energy" in the Aitchison sense.

### 7.2 Curvature level

```
function curvature_level(h_matrix):
    # curvature composition uses 1/p_j² (the κ_jj diagonal), NOT 1/p_j (cf. CNT v2.0.1 fix)
    p_matrix := inverse_clr_back_to_closed(h_matrix)
    curv := mean across t of sum_j(1 / p_matrix[t,j]^2)
    return curv
```

The mean trace of κᴴˢ across the level — the level's compositional "curvature." The v2.0.1 fix is preserved: curvature uses `1/p²`, not `1/p`.

### 7.3 Level convergence

```
function level_converged(L, current_level):
    # Period-1 detection requires TWO consecutive level-pair convergences
    # (CNT v2.0.1 fix; was 1, produced false positives on USA EMBER and Ball/TAS)
    if current_level < 2:  return false
    return  approx_equal(L[-1].energy, L[-2].energy) AND
            approx_equal(L[-2].energy, L[-3].energy)
```

The two-consecutive-convergence test was added in CNT v2.0.1 to eliminate false-positive period-1 terminations.

### 7.4 Decimate

```
function decimate(h_matrix):
    # Block-average pairs of consecutive timesteps
    T := number of rows in h_matrix
    h_decimated := zeros((T//2, ncols))
    for k in 0..T//2-1:
        h_decimated[k] := 0.5 * (h_matrix[2k] + h_matrix[2k+1])
    return h_decimated
```

The 2:1 coarse-graining for the depth recursion. Half the rows; same number of columns.

### 7.5 Period-2 attractor fit

```
function fit_p2_attractor(L):
    if len(L) < TRIADIC_T_LIMIT_FOR_FIT:  return null
    # Fit a period-2 limit cycle: A cos(πk + ϕ) e^{-ζk}
    A, zeta := fit by least squares over the energy levels
    if convergence: termination := "LIMIT_CYCLE_P2"
    else:           termination := "NO_FIT"
    return { "amplitude": A, "damping": zeta, "termination": termination }
```

Period-2 attractor fit is the headline finding on Backblaze and Planck CMB photon power: `max_residual = 4.441 × 10⁻¹⁶`, IEEE float64 floor on physically unrelated D=4 datasets. The fit produces (A, ζ); convergence at IEEE floor is the conformance test.

### 7.6 M² = I involution sample

```
function compute_m2_involution_sample(L):
    # Sample the metric involution at each level to verify (q*)* = q identity
    samples := []
    for level in L:
        m := level.metric_tensor                   # if computed at this level
        m_squared := m @ m
        identity_residual := ‖m_squared - I‖_F
        samples.append({ "level": level.level, "residual": identity_residual })
    return samples
```

The M² = I check verifies that the metric tensor, applied twice, returns to the identity (cf. flagship Lemma 7's geometric interpretation; involution on S³ via quaternion conjugation).

---

## 8. Navigation 2D (v3.1.0+ addition)

```
function compute_navigation_2d(ilr_matrix):
    # PCA on the centred ILR trajectory
    X := ilr_matrix.T - mean(ilr_matrix.T, axis=row_axis)        # centre each column
    X_X := X.T @ X / (T - 1)                                      # covariance matrix
    eigvals, eigvecs := eigendecompose(X_X)
    PC1, PC2 := top-2 eigenvectors (sorted by eigenvalue)
    pc1_var := eigvals[0]
    pc2_var := eigvals[1]
    total_var := sum(eigvals)
    pc1_pct := 100 * pc1_var / total_var
    pc2_pct := 100 * pc2_var / total_var

    # Disk-scaled barycenter coordinates per Output Doctrine v1.0
    bary_xy := zeros((T, 2))
    bary_xy[:, 0] := PC1 · ilr_matrix.T      # project each timestep onto PC1
    bary_xy[:, 1] := PC2 · ilr_matrix.T      # project each timestep onto PC2
    max_norm := max over t of ‖bary_xy[t]‖
    bary_xy_scaled := 0.85 * bary_xy / max_norm     # scale to unit-disk fraction

    return {
        "PC1": PC1, "PC2": PC2,
        "pc1_var_pct": pc1_pct, "pc2_var_pct": pc2_pct,
        "pc1_plus_pc2_pct": pc1_pct + pc2_pct,
        "bary_xy": bary_xy_scaled,
    }
```

`compute_navigation_2d` was added in CNT v3.2.0 (the conference-window engine — note: v3.1.0 is the corpus-pinned version per the engine version policy). It produces the ILR-Helmert PCA barycenter trajectory used by the conference projector's BARY and ALIGN modes (CoDaWork 2026 manuscript Fig 6).

---

## 9. Diagnostics

### 9.1 Lock events

```
function detect_lock_events(clr_matrix, threshold = LOCK_CLR_THRESHOLD):
    # A lock event is a step where the maximum |Δclr| exceeds threshold
    events := []
    for t in 1..T-1:
        delta := max over j of |clr_matrix[t,j] - clr_matrix[t-1,j]|
        if delta > threshold:
            events.append({ "t": t, "max_delta": delta, "helmsman": argmax(delta) })
    return { "events": events, "count": len(events) }
```

Default `LOCK_CLR_THRESHOLD = 2.0` (nats). A lock event marks a structural compositional shift; the helmsman of the event is the carrier that drove it.

### 9.2 Degeneracy flags

```
function degeneracy_flags(rows_closed):
    flags := []
    if any p_i < DEGEN_THRESHOLD_LOW for all t:  flags.append("PERSISTENT_ZERO_CARRIER")
    if rank(rows_closed) < D - 1:                flags.append("RANK_DEFICIENT")
    if max_carrier_dominance > DEGEN_THRESHOLD_HIGH:  flags.append("HIGHLY_CONCENTRATED")
    return { "flags": flags }
```

Diagnostic flags surfacing cases where the CoDa assumptions are at risk.

### 9.3 EITT bench test

```
function eitt_bench_test(rows_closed):
    # Entropy-Invariant Time Transformer test (HUF-side; sibling of MC-4)
    # Test whether Shannon entropy is preserved under geometric-mean temporal compression
    H_orig := mean over t of shannon_entropy(rows_closed[t])
    rows_compressed_2to1 := geometric_mean_pairs(rows_closed)
    H_2to1 := mean over t of shannon_entropy(rows_compressed_2to1[t])
    invariance_pct := 100 * (1 - |H_orig - H_2to1| / max(H_orig, EPS))
    return { "H_original": H_orig, "H_2to1": H_2to1, "invariance_pct": invariance_pct }
```

EITT is HUF-side scientific contribution (papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md). The bench test checks that entropy is preserved (within ~0.2 %) under 2:1 geometric-mean temporal compression on compositional carriers.

---

## 10. Output JSON structure and `content_sha256`

The output JSON is structured for both CoDa-community readability and Hˢ-extension diagnostic depth:

```
output := {
    "metadata": {
        "engine_version": "3.1.0",
        "schema_version": "3.1.0",
        "engine_config": { ... config-block constants ... },
        "engine_signature": "sha256-hex of cnt.py source",
        "input_path": "...",
        "input_sha256": "sha256-hex of input CSV",
        "timestamp_utc": "...",
        "host_metadata": { ... },
        "content_sha256": null   # filled in last; see below
    },
    "input": {
        "n_records": T,
        "n_carriers": D,
        "carriers": [carrier names],
        "labels": [labels],
        "rows_raw": [...]        # only if INCLUDE_RAW_ROWS = true
    },
    "tensor": {
        "helmert_basis": { "coefficients": V },
        "timesteps": [
            { "label": ..., "coda_standard": {...}, "higgins_extensions": {...} },
            ... T entries ...
        ]
    },
    "stage1": { ... §6.1 output ... },
    "stage2": { ... §6.2 output ... },
    "stage3": { ... §6.3 output ... },
    "depth_tower": { ... §7 output ... },
    "navigation_2d": { ... §8 output, v3.1.0+ ... },
    "lock_events": { ... §9.1 output ... },
    "degeneracy": { ... §9.2 output ... },
    "eitt_bench": { ... §9.3 output ... }
}
```

### Content SHA-256 derivation

```
function compute_content_sha256(output):
    # Step 1: deep-copy output and zero out the content_sha256 field itself
    o := deepcopy(output)
    o.metadata.content_sha256 := ""

    # Step 2: also zero out non-deterministic fields per the determinism contract
    o.metadata.timestamp_utc := ""
    o.metadata.host_metadata := {}
    # Path fields that depend on cwd are reduced to their basename for stability:
    o.metadata.input_path := basename(o.metadata.input_path)

    # Step 3: canonical JSON serialization
    s := json.dumps(o,
        sort_keys=true,
        ensure_ascii=true,
        separators=(",", ":"),                # compact, no whitespace
        default=numpy_aware_json_encoder)     # convert numpy types to native Python

    # Step 4: SHA-256 of UTF-8 bytes
    return sha256(s.encode("utf-8")).hexdigest()
```

The content hash MUST be reproducible byte-identically across:
- Python and R reference implementations
- Linux, macOS, Windows
- Intel and ARM CPUs
- Any BLAS / LAPACK implementation that is IEEE-754 compliant

The IEEE-floor convergence on Backblaze and Planck CMB photon power (both D=4) produces bit-identical residuals `4.440892098500626e-16` — this is hardware float64 representation, not algorithmic noise. *That* is the determinism contract.

---

## 11. Determinism contract (the conformance test)

The engine satisfies the following invariants:

1. **Same input + same configuration → byte-identical `content_sha256`.** This is the central conformance test. If your re-implementation produces a different `content_sha256` on the same input CSV with the same engine config, one of the two implementations has a bug.

2. **`metadata.engine_config` echoes every config-block constant.** Different configuration values produce different hashes by design and by automated test (`tests/test_determinism.py`).

3. **`metadata.engine_signature` is the SHA-256 of `cnt.py` itself.** Modifying the engine source — even cosmetically — changes the signature. This is the audit chain anchor.

4. **Non-deterministic fields are zeroed before hashing** (timestamp, host_metadata, path-with-cwd). The implementation must zero exactly these fields and no others before computing the hash.

5. **Numerical precision is IEEE float64 throughout.** No higher-precision arithmetic; no random seeds; no SIMD-dependent reduction order in operations where order would matter (Kahan summation is NOT used; standard reduction order is canonical).

6. **The output JSON is sorted-keys canonical.** Any JSON serializer that produces sorted-keys + compact-separators + ensure_ascii + UTF-8 will match.

---

## 12. Reference inputs and their published `content_sha256` values

The three IEEE-floor confirmation datasets are pinned with their canonical hashes in `HCI-CNQ/experiments/`. Any conformant re-implementation should reproduce these hashes byte-identically:

| Dataset | Source | D | T | max_residual | termination | published parent_cnt_content_sha256 |
|---|---|---|---|---|---|---|
| Backblaze fleet | drive-failure compositions | 4 | 731 | 4.440892098500626e-16 | LIMIT_CYCLE_P2 | (see HCI-CNQ/experiments/backblaze/) |
| Planck CMB | photon power per multipole | 4 | 2499 | 4.440892098500626e-16 | LIMIT_CYCLE_P2 / OVERDAMPED_EXTREME | `3de7d4007866dc11c64d5342974d6c9d2dfc1906166627999194df3fe6a400c4` |
| SM neutrino | oscillation composition | 3 | 1000 | 3.330669073875470e-16 | LIMIT_CYCLE_P2 / LIGHTLY_DAMPED | `60d733d2219fbe3cf6ea5647d0f17139923d578ffee0d16a124fbe4eac526952` |

A re-implementation that produces these hashes on these inputs has passed the conformance test.

---

## 13. Configuration block — the constants

The following constants appear in the `USER CONFIGURATION` block at the top of `cnt.py` and are echoed in `metadata.engine_config` of every output:

```
ZERO_REPLACEMENT_EPS                = 1e-10
DEPTH_MAX_LEVELS                    = 20
TRIADIC_T_LIMIT_FOR_FIT             = 500
TRIADIC_T_LIMIT                     = 500        # CNT v2.0.1 fix: lowered from 1000
LOCK_CLR_THRESHOLD                  = 2.0
CONCENTRATION_HIGH_THRESHOLD        = 0.10
CONCENTRATION_LOW_THRESHOLD         = 0.05
DEGEN_THRESHOLD_LOW                 = 1e-6
DEGEN_THRESHOLD_HIGH                = 0.95
IR_THRESHOLDS = {
    "chaotic":             ...
    "lightly_damped":      ...
    "overdamped":          ...
    "overdamped_extreme":  ...
}
INCLUDE_RAW_ROWS                    = true
```

Exact values are pinned in `cnt.py`. Re-implementations must use the same values *or* echo their own values in `metadata.engine_config` (different values → different hash by design).

---

## 14. Cross-references

| If you want | Read |
|---|---|
| The mathematical foundations | [`../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) |
| The quaternion (CNQ) algorithm | [`../../HCI-CNQ/engine/CNQ_PSEUDOCODE.md`](../../HCI-CNQ/engine/CNQ_PSEUDOCODE.md) |
| The full unified formula and lemma chain | [`../../papers/flagship/GROUND_STATE_AND_TRACTION.md`](../../papers/flagship/GROUND_STATE_AND_TRACTION.md) v2.2 |
| The 7-phase reproducible runbook (end-to-end) | [`../../ai-refresh/CCTT_RUNBOOK.md`](../../ai-refresh/CCTT_RUNBOOK.md) |
| The Tensor Train I/O specification (HUF-STD-002) | [`../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json`](../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) |
| The vocabulary (~220-entry glossary) | [`../handbook/GLOSSARY.md`](../handbook/GLOSSARY.md) v3.0 |
| The verification path for skeptical users | [`../../TRUST_AND_VERIFICATION.md`](../../TRUST_AND_VERIFICATION.md) |
| The Stage 2 detailed algorithm | [`../conference_demo/cnt_demo/05_doctrine/STAGE2_PSEUDOCODE.md`](../conference_demo/cnt_demo/05_doctrine/STAGE2_PSEUDOCODE.md) |
| The anti-specification (what the engine MUST NOT do) | [`./ANTI_SPECIFICATION.md`](ANTI_SPECIFICATION.md) |

---

## 15. Versions and lineage

| Version | Engine status | Schema | Notes |
|---|---|---|---|
| 3.0.0 | Released — push #32 ground-up rebuild | 3.0.0 | CNT v3 architecture |
| 3.1.0 | Current Python canonical (push #50 stamp) | 3.1.0 | Helmsman family promoted PROPOSED → CANONICAL per schema 3.1.0 |
| 3.2.0 | Engine source-only (per engine-version policy) | 3.1.0 | Adds `compute_navigation_2d` for the conference projector |

R port (cnt.R): v3.0.0; v3.1.0 parity queued as EngPromo-2 post-conference.

Legacy CNT v2.0.x pseudocode is preserved at [`../../HCI/cnt_v2/CNT_PSEUDOCODE.md`](../../HCI/cnt_v2/CNT_PSEUDOCODE.md) for historical lineage.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line. The AI follows the same protocol.*
*Same input, same output, always. This is the algorithm.*
