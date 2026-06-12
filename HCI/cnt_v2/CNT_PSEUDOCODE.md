# CNT Engine — Pseudocode Reference

**Schema version:** 2.0.0
**Engine version:** 2.0.3 (current reference; cnt.R port at 2.0.2)
**Status:** Language-neutral algorithm reference. Reproducible in any
language with basic arithmetic (no special libraries required).

This document is the algorithm. The Python (`cnt.py`) and R (`cnt.R`)
implementations are reference instances; this is the contract they
implement. Anyone reading this can re-implement the engine in any
language.

## Engine fix log (within v2.0.x)

| Engine | Fix |
|---|---|
| 2.0.0 | Initial schema-2 layout (coda_standard / higgins_extensions split) |
| 2.0.1 | Period-1 detection now requires TWO consecutive level-pair convergences (was 1) — fixed false positives on USA EMBER and Ball/TAS where coincidental L_k ≈ L_{k-1} stopped the recursion prematurely. See §6.3 below. |
| 2.0.1 | Curvature composition uses 1/x_j² (the κ_jj diagonal), not 1/x_j. See §4.5 below. |
| 2.0.1 | TRIADIC_T_LIMIT default lowered 1000 → 500. |
| 2.0.2 | USER CONFIGURATION block at top of source file with documented constants, echoed in `metadata.engine_config` of every JSON output. |
| 2.0.3 | IR taxonomy refinement (Python `cnt.py` only): the legacy `DEGENERATE` class split into three more-informative classes: `ENERGY_STABLE_FIXED_POINT` (energy depth ≥ DEPTH_MAX_LEVELS with stable amplitude), `CURVATURE_VERTEX_FLAT` (curvature recursion driven to a vertex by a single dominant carrier), `D2_DEGENERATE` (genuine D=2 limitation; a single independent compositional axis). The R port at 2.0.2 retains the single `DEGENERATE` class. |

---

## Inputs

```
csv_path     : path to CSV file with first column = label, rest = D carriers
output_path  : path to write the JSON
ordering     : { is_temporal: bool, ordering_method: str, caveat: str|null }
                — required, declared by the user

eitt_M_sweep : list of compression ratios to bench-test (default: depend on T)
include_full_distance_matrix : bool (default: T <= 200)
```

---

## High-Level Flow

```
function CNT(csv_path, output_path, ordering):
    record_input_metadata(csv_path)              # source hash, file size, etc.
    records = ingest_csv(csv_path)               # close to simplex, replace zeros
    record_data_metadata(records, ordering)

    tensor_block = compute_tensor(records)        # §1
    stages_block = compute_stages(records, tensor_block)  # §2
    bridges_block = compute_bridges(records, tensor_block) # §3
    depth_block = compute_depth(records, tensor_block)     # §4
    diagnostics_block = compute_diagnostics(records, tensor_block, depth_block) # §5

    json = {
        metadata,
        input,
        tensor: tensor_block,
        stages: stages_block,
        bridges: bridges_block,
        depth: depth_block,
        diagnostics: diagnostics_block,
    }
    json.diagnostics.content_sha256 = sha256_of_normalized(json)
    write_json(json, output_path)
```

---

## §0 — Conventions

### Closure

```
function close(x):
    s = sum(x)
    return [v / s for v in x]
```

### CLR transform

```
function clr(x):
    D = length(x)
    log_x = [ln(v) for v in x]      # x must be all > 0
    mean_log = sum(log_x) / D
    return [lx - mean_log for lx in log_x]
```

### Helmert orthonormal basis

```
function helmert_basis(D):
    basis = []
    for k in 1 to D-1:
        row = [0] * D
        scale = sqrt(k / (k + 1))
        for j in 1 to k:
            row[j-1] = 1 / k
        row[k] = -1
        # normalize: each row scaled by sqrt(k / (k+1))
        for j in 1 to k+1:
            row[j-1] = row[j-1] * scale
        basis.append(row)
    return basis    # (D-1) x D matrix
```

### ILR projection

```
function ilr(h, basis):
    # h is the CLR vector (length D); basis is (D-1) x D
    return [dot(basis[k], h) for k in 0 to D-2]
```

### Aitchison distance

```
function aitchison_distance(x, y):
    return norm(clr(x) - clr(y))     # Euclidean norm of CLR difference
```

### Aitchison barycenter (geometric-mean of N closed compositions)

```
function aitchison_barycenter(rows):
    D = length(rows[0])
    log_means = []
    for j in 0 to D-1:
        s = sum(ln(r[j]) for r in rows)
        log_means.append(s / length(rows))
    g = [exp(lm) for lm in log_means]
    return close(g)
```

### Shannon entropy (NOT scale-invariant — empirical use only)

```
function shannon_entropy(x):
    return - sum(v * ln(v) for v in x if v > 0)
```

### Higgins scale (HUF-specific; range [0, 1])

```
function higgins_scale(x):
    H = shannon_entropy(x)
    return 1 - H / ln(D)
```

### Metric dual involution

```
function M(x):
    return close([1 / v for v in x])
```

Theorem (verified to IEEE 754 floor): `M(M(x)) = x` for all x in the
open simplex. In CLR space, `clr(M(x)) = -clr(x)`. The fixed point is
the barycenter (1/D, ..., 1/D). See Math Handbook Ch 18.

### Higgins steering metric tensor (full D x D matrix)

```
function metric_tensor(x):
    D = length(x)
    K = D x D zero matrix
    for i in 0 to D-1:
        for j in 0 to D-1:
            if i == j:
                K[i][j] = (1 - 1/D) / (x[i] * x[i])
            else:
                K[i][j] = -1 / (D * x[i] * x[j])
    return K
```

### Bearing tensor (all D(D-1)/2 pairwise CLR-plane angles)

```
function bearing_tensor(h):
    D = length(h)
    pairs = []
    for i in 0 to D-2:
        for j in i+1 to D-1:
            theta = atan2(h[j], h[i])    # signed angle in [-pi, pi]
            pairs.append((i, j, theta_in_degrees))
    return pairs
```

### Angular velocity (Lagrange identity, atan2-stable)

```
function angular_velocity(h_prev, h):
    # |a x b|^2 = |a|^2 |b|^2 - <a,b>^2
    cross_sq = norm_sq(h_prev) * norm_sq(h) - dot(h_prev, h) ** 2
    if cross_sq < 0: cross_sq = 0
    cross_mag = sqrt(cross_sq)
    omega = atan2(cross_mag, dot(h_prev, h))
    return omega_in_degrees
```

### Helmsman (DCDI)

```
function helmsman(h_prev, h, carrier_names):
    deltas = [|h[j] - h_prev[j]| for j in 0 to D-1]
    j_max = argmax(deltas)
    return (carrier_names[j_max], deltas[j_max])
```

---

## §1 — `tensor` block

```
function compute_tensor(records):
    basis = helmert_basis(records.D)
    timesteps = []
    h_prev = null
    for i, rec in enumerate(records):
        x = close(rec.values)
        h = clr(x)
        ts = {
            index:                i,
            label:                rec.label,
            raw_values:           rec.values,
            composition:          x,
            clr:                  h,
            ilr:                  ilr(h, basis),
            shannon_entropy:      shannon_entropy(x),
            higgins_scale:        1 - shannon_entropy(x) / ln(D),
            aitchison_norm:       norm(h),
            bearing_tensor:       bearing_tensor(h),
            metric_tensor:        metric_tensor(x),
            metric_tensor_diagonal: [1/v for v in x],
            condition_number:     max(x) / min(x),
        }
        if h_prev is not null:
            ts.angular_velocity_deg     = angular_velocity(h_prev, h)
            ts.aitchison_distance_step  = norm(h - h_prev)
            ts.helmsman, ts.helmsman_delta = helmsman(h_prev, h, records.carriers)
        timesteps.append(ts)
        h_prev = h
    return { helmert_basis: basis, timesteps: timesteps }
```

---

## §2 — `stages` block

### Stage 1 — section atlas + metric ledger

```
function stage1(records, tensor):
    section_atlas = []
    metric_ledger = []
    for ts in tensor.timesteps:
        # Cube faces: XY = (clr_1, clr_2), XZ = (clr_1, clr_3), YZ = (clr_2, clr_3)
        # plus higher-order projections via PCA on the full D-vector
        section_atlas.append({
            index: ts.index,
            label: ts.label,
            xy_face: ts.clr[0:2],
            xz_face: [ts.clr[0], ts.clr[2]],
            yz_face: ts.clr[1:3],
            metric_tensor_trace: trace(ts.metric_tensor.matrix),
            condition_number: ts.condition_number,
            angular_velocity_deg: ts.angular_velocity_deg or 0,
        })
        metric_ledger.append({
            index: ts.index,
            label: ts.label,
            hs: ts.higgins_scale,
            ring: ring_classify(ts.higgins_scale),
            omega_deg: ts.angular_velocity_deg or 0,
            helmsman: ts.helmsman or "",
            energy: ts.aitchison_norm ** 2,
            condition: ts.condition_number,
        })
    return { section_atlas, metric_ledger }
```

### Stage 2 — variation matrix + carrier-pair examination

```
function stage2(records, tensor):
    D = records.D
    # CoDa-standard variation matrix tau_ij = var(ln(x_i / x_j))
    variation_matrix = D x D zero matrix
    for i in 0 to D-1:
        for j in 0 to D-1:
            if i != j:
                ratios = [ln(rec.composition[i] / rec.composition[j]) for rec in records]
                variation_matrix[i][j] = variance(ratios)

    # Pairwise behaviour
    carrier_pairs = []
    for (i, j) in combinations(0..D-1, 2):
        h_i_series = [ts.clr[i] for ts in tensor.timesteps]
        h_j_series = [ts.clr[j] for ts in tensor.timesteps]
        carrier_pairs.append({
            carrier_a: records.carriers[i],
            carrier_b: records.carriers[j],
            pearson_r: pearson_correlation(h_i_series, h_j_series),
            co_movement_score: ...,
            opposition_score: ...,
            locked: variance(bearings_ij_over_time) < lock_epsilon,
        })

    return { variation_matrix, carrier_pair_examination: carrier_pairs }
```

### Stage 3 — higher-degree (subcompositions, regimes, triadic if T small)

```
function stage3(records, tensor):
    D = records.D
    T = records.T

    # Subcompositional ladder — all k-subsets for k = 2 .. D-1
    ladder = []
    for k in 2 to D-1:
        subsets = combinations(carriers, k)
        # for each, compute mean correlation among its parts
        ladder.append({ degree: k, n_subsets: len(subsets), ... })

    # Carrier triads
    carrier_triads = []
    for (i, j, k) in combinations(0..D-1, 3):
        carrier_triads.append({ carriers, mean_correlation, mean_area })

    # Triadic day-area analysis — capped to avoid C(T, 3) explosion
    triadic = { n_candidates: C(T, 3) }
    if T > 1000:
        triadic.selection_method = "none_T_too_large"
        triadic.results = []
    else:
        all_triads = combinations(0..T-1, 3)
        # compute area for each via Heron in CLR space
        results = []
        for (a, b, c) in all_triads:
            ba = tensor.timesteps[a].clr
            bb = tensor.timesteps[b].clr
            bc = tensor.timesteps[c].clr
            sides = [norm(ba-bb), norm(bb-bc), norm(bc-ba)]
            s = sum(sides) / 2
            area = sqrt(max(0, s * (s - sides[0]) * (s - sides[1]) * (s - sides[2])))
            results.append({ triad: (a,b,c), sides, area })
        results.sort(by area, descending)
        triadic.selection_method = "top_K_by_area"
        triadic.selection_K = 500
        triadic.n_returned = min(500, len(results))
        triadic.results = results[0:500]

    # Regime detection — find boundaries where Aitchison distance step exceeds threshold
    regimes = ...

    return { triadic_area: triadic, carrier_triads, subcomposition_ladder: ladder, regime_detection: regimes }
```

---

## §3 — `bridges` block

### Per-carrier Lyapunov exponents

```
function per_carrier_lyapunov(records, tensor):
    # Approximate sensitivity along each carrier axis from the CLR series
    exponents = []
    for j in 0 to D-1:
        h_j_series = [ts.clr[j] for ts in tensor.timesteps]
        # Lyapunov via mean log-divergence rate of nearby trajectories
        lyap = estimate_lyapunov_1d(h_j_series)
        exponents.append({
            carrier: records.carriers[j],
            lyapunov_exponent: lyap,
            classification: classify_lyapunov(lyap),
        })
    return exponents
```

### State-space + observability

```
function control_theory(records, tensor):
    # Fit linear model x(t+1) = A x(t) + B u(t)
    # via least squares on CLR series
    A, residual = ls_fit_AR1(tensor)
    state_space = {
        A_matrix: A,
        controllability_rank: rank(controllability_matrix(A, B)),
        observability_rank: rank(observability_matrix(A, C)),
        spectral_radius: max(|eigenvalues(A)|),
        stable: spectral_radius < 1,
        mean_residual: residual,
    }

    observability = []
    for j in 0 to D-1:
        observability.append({
            carrier: records.carriers[j],
            clr_variance: var([ts.clr[j] for ts in tensor.timesteps]),
            observability_score: ...,
        })
    return { state_space_model: state_space, observability }
```

### Information theory bridge

```
function information_theory(records, tensor):
    entropy_series = [{ label, shannon_entropy, normalised_entropy: H/ln(D), higgins_scale: 1 - H/ln(D) } for ts in tensor.timesteps]
    fisher = mean_fisher_information(records)
    kl = adjacent_pair_kl_divergence(records)
    mi = highest_mutual_information_pair(records)
    rate = entropy_rate(entropy_series)
    return { entropy_series, fisher_information: fisher, kl_divergence: kl, mutual_information: mi, entropy_rate: rate }
```

---

## §4 — `depth` block

The recursive depth sounder iterates the CNT through derived
compositions until signal exhaustion.

### Derived composition constructors

```
function energy_composition(tensor):
    # e_j(t) = (delta h_j)^2 / sum (delta h_k)^2
    energies = []
    for i in 1 to T-1:
        delta_h = tensor.timesteps[i].clr - tensor.timesteps[i-1].clr
        energies.append(close([d*d for d in delta_h]))
    return energies

function curvature_composition(tensor):
    # c_j(t) = kappa_jj(t) / sum kappa_kk(t)
    curvatures = []
    for ts in tensor.timesteps:
        diag = ts.metric_tensor.matrix[i][i] for i in 0..D-1
        curvatures.append(close(diag))
    return curvatures
```

### Depth sounder main loop

```
function depth_sounder(records, tensor):
    # Involution proof — sample at multiple t
    involution_proof = {
        samples: [],
    }
    for t in [0, T/2, T-1]:
        x = tensor.timesteps[t].composition
        Mx = M(x)
        MMx = M(Mx)
        residual = norm(array(MMx) - array(x))
        involution_proof.samples.append({ t, x, Mx, MMx, residual_M2: residual, ... })
    involution_proof.mean_residual = mean(s.residual_M2 for s in samples)
    involution_proof.verified = (involution_proof.mean_residual < 1e-10)

    # Level 0 — base statistics
    level_0 = base_statistics(tensor)

    # Energy tower
    energy_tower = []
    current_records = records
    current_tensor = tensor
    while not exhausted and len(energy_tower) < MAX_LEVELS:
        derived = energy_composition(current_tensor)
        if len(derived) < 5:
            status = "SIGNAL_SHORT"; break
        new_tensor = compute_tensor_for(derived)
        level_summary = summarise_level(new_tensor, level=len(energy_tower)+1)
        energy_tower.append(level_summary)
        if detect_flat(new_tensor):
            level_summary.status = "OMEGA_FLAT" or "HS_FLAT"; break
        if detect_period_2(energy_tower):
            level_summary.status = "LIMIT_CYCLE_P2"; break
        if detect_period_1(energy_tower):
            level_summary.status = "LIMIT_CYCLE_P1"; break
        current_tensor = new_tensor

    # Curvature tower — same loop with curvature_composition
    curvature_tower = ... (analogous)

    # Period-2 attractor
    curvature_traj = [lvl.hs_mean for lvl in curvature_tower]
    if attractor detected with period 2:
        tail = curvature_traj[-6:] (last 6 levels for stable estimate)
        c_even = mean of even-indexed entries in tail
        c_odd = mean of odd-indexed entries in tail
        amplitude = |c_even - c_odd|
        deltas = [traj[n] - (c_even if n even else c_odd) for n]
        contraction_ratios = [|deltas[n+2]| / |deltas[n]| for n]
        contraction_lyapunov = mean(ln(r) for r in contraction_ratios if r > 0)
        mean_contraction_ratio = mean(contraction_ratios)
        banach_satisfied = (mean_contraction_ratio < 1)

        depth_curvature_attractor = {
            period: 2,
            c_even, c_odd, amplitude,
            convergence_level, residual,
            contraction_lyapunov,
            mean_contraction_ratio,
            banach_satisfied,
        }
    else:
        depth_curvature_attractor = { period: 1 (or 0), ... }

    # Impulse response
    A_initial = |curvature_traj[1] - curvature_traj[0]|
    A_final = amplitude
    depth_delta = curvature_depth
    damping_zeta = -ln(A_final / A_initial) / depth_delta
    classification = classify_IR(amplitude, damping_zeta)

    depth_impulse_response = {
        amplitude_A: amplitude,
        depth_delta,
        damping_zeta,
        classification,
    }

    return {
        involution_proof,
        level_0,
        energy_tower,
        curvature_tower,
        curvature_attractor: depth_curvature_attractor,
        impulse_response: depth_impulse_response,
        summary: { energy_depth, curvature_depth, ... },
    }
```

### IR classification

```
function classify_IR(A, zeta):
    if A < 0.1:
        return "CRITICALLY_DAMPED"
    if zeta > 0 and zeta < 0.1:
        return "LIGHTLY_DAMPED"
    if abs(zeta) < 1e-6:
        return "UNDAMPED"
    if A > 0.7:
        return "OVERDAMPED_EXTREME"
    return "MODERATELY_DAMPED"
```

---

## §5 — `diagnostics` block

### EITT residuals

```
function eitt_bench_test(records):
    H_full = mean(shannon_entropy(rec.composition) for rec in records)
    M_sweep = []
    for M in [2, 4, 8, 16, 32, 64, 128, ceil(T/101)]:
        if M >= T: continue
        decimated = []
        for b in range(0, T, M):
            block = records[b : b+M]
            if len(block) >= 2:
                decimated.append(aitchison_barycenter([r.composition for r in block]))
            elif len(block) == 1:
                decimated.append(block[0].composition)
        H_decimated = mean(shannon_entropy(c) for c in decimated)
        variation = abs(H_decimated - H_full) / H_full * 100
        M_sweep.append({ M, n_blocks: len(decimated), H_mean_decimated: H_decimated, variation_pct: variation, pass_5pct: variation < 5 })
    return {
        H_mean_full: H_full,
        M_sweep,
        gate_pct: 5.0,
        note: "Empirical observation of trajectory smoothness, not geometric theorem.",
    }
```

### Lock events

```
function detect_lock_events(records, tensor):
    events = []
    DEGEN_THRESHOLD = 1e-4   # CLR spread
    LOCK_CLR_THRESHOLD = -10
    for i, ts in enumerate(tensor.timesteps):
        clr_spread = max(ts.clr) - min(ts.clr)
        if clr_spread < DEGEN_THRESHOLD:
            events.append({
                event_type: "DEGEN",
                timestep_index: i,
                label: ts.label,
                carrier: null,
                clr_value: clr_spread,
                context: "Composition collapsed to barycenter",
            })
        for j, h in enumerate(ts.clr):
            if h < LOCK_CLR_THRESHOLD:
                # determine if this is LOCK-ACQ (transition from valid -> degen) or LOCK-LOSS (degen -> valid)
                event_type = "LOCK-ACQ" if (i > 0 and tensor.timesteps[i-1].clr[j] >= LOCK_CLR_THRESHOLD) else "LOCK-LOSS"
                events.append({
                    event_type,
                    timestep_index: i,
                    label: ts.label,
                    carrier: records.carriers[j],
                    clr_value: h,
                    context: f"{records.carriers[j]} approached zero (CLR={h:.2f})",
                })
    return events
```

### Degeneracy flags

```
function degeneracy_flags(records, tensor):
    flags = []
    if records.T < 20:
        flags.append({
            flag: "small_T",
            severity: "warning",
            message: "Trajectory too short for stable depth-tower estimation",
            condition: f"T = {records.T} < 20",
        })
    if records.D < 3:
        flags.append({
            flag: "small_D",
            severity: "warning",
            ...
        })
    # Pre-aligned: monotonic in any single carrier
    for j in 0..D-1:
        series = [rec.composition[j] for rec in records]
        if is_monotonic(series):
            flags.append({
                flag: "pre_aligned_compositionally",
                severity: "warning",
                message: f"Records appear sorted by carrier {records.carriers[j]} — depth recursion may be degenerate",
                condition: f"composition[{j}] is monotonic across all records",
            })
    return flags
```

### Content SHA-256

```
function content_sha256(json):
    j = deep_copy(json)
    delete j.metadata.generated
    delete j.metadata.wall_clock_ms
    delete j.metadata.environment
    delete j.diagnostics.content_sha256        # avoid self-reference
    canonical = json_dumps(j, sort_keys=true, separators=(',',':'))
    return sha256(canonical.encode('utf-8'))
```

---

## §6 — Determinism Test

The engine's output must be content-stable under re-run.

```
function determinism_test(csv_path):
    json_a = CNT(csv_path)
    json_b = CNT(csv_path)
    assert json_a.diagnostics.content_sha256 == json_b.diagnostics.content_sha256
```

The test passes if and only if the engine is deterministic. Two
implementations (Python vs R) need not produce bit-identical
content_sha256 due to floating-point differences, but they must
produce values that agree to working precision (typically 1e-10) on
all numerical fields.

---

*This pseudocode is the contract. The Python and R implementations
follow it. Re-implementations in any language are welcome and need
only honour this document and the schema.*
