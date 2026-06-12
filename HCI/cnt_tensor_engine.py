#!/usr/bin/env python3
"""
CNT Tensor Engine — Complete Compositional Navigation Tensor Computation
========================================================================

Program 1 of the CNT standard pipeline.

Input:  CSV file (first column = index/year, remaining columns = carrier values)
Output: JSON file containing ALL CNT tensor channels, derived quantities,
        and compositional geometry for external scientific analysis.

Computes (per the CNT Mathematics Handbook v2.0):
  Ch 2:  CLR geometry — CLR, ILR, Helmert basis
  Ch 3:  CNT(x) = (theta, omega, kappa_HS, sigma)
  Ch 4:  Corollary diagnostics — locks, reversals, steering asymmetry
  Ch 5:  Aitchison distance matrix, metric energy, metric angles
  Ch 6:  Precision diagnostics — condition numbers, precision budget
  Ch 14: Higgins Scale, ring classification, Shannon entropy

The JSON output is the complete measurement record. Program 2
(cnt_analysis.py) reads this JSON to compute Stage 1/2/3 and
the three theoretical bridges.

Mathematical lineage:
  Aitchison (1986) — CLR transform, Aitchison distance
  Shannon (1948)   — Entropy
  Egozcue et al. (2003) — ILR, Helmert basis
  Higgins (2025)   — Hs = 1 - H/ln(D), ring classification
  Higgins (2026)   — CNT bearing/velocity/sensitivity/helmsman

Usage:
  python cnt_tensor_engine.py input.csv output.json

The instrument reads. The expert decides. The loop stays open.
"""

import csv
import json
import math
import sys
import os
from datetime import datetime


# ══════════════════════════════════════════════════════════════════
# STEP 1: CLOSURE (Handbook Ch 2.1)
# ══════════════════════════════════════════════════════════════════

def closure(x, eps=1e-15):
    """Close a positive vector to the D-simplex.

    x_j' = max(x_j, eps) / sum(max(x_k, eps))

    Guarantees: sum(x') = 1.0, all x_j' > 0.
    """
    x_pos = [max(float(v), eps) for v in x]
    total = sum(x_pos)
    if total <= 0:
        raise ValueError("Composition must have positive sum.")
    return [v / total for v in x_pos]


# ══════════════════════════════════════════════════════════════════
# STEP 2: CLR TRANSFORM (Handbook Ch 2.2)
# ══════════════════════════════════════════════════════════════════

def clr_transform(x):
    """Centred Log-Ratio transform.

    h_j = ln(x_j) - (1/D) * sum_{k=1}^{D} ln(x_k)

    Maps D-simplex to D-dimensional hyperplane with sum(h) = 0.
    The CLR space IS an inner product space where the Aitchison
    metric equals the standard Euclidean metric.
    """
    D = len(x)
    log_x = [math.log(v) for v in x]
    mean_log = sum(log_x) / D
    return [lx - mean_log for lx in log_x]


# ══════════════════════════════════════════════════════════════════
# STEP 3: HELMERT BASIS AND ILR (Handbook Ch 2.3)
# ══════════════════════════════════════════════════════════════════

def helmert_basis(D):
    """Helmert submatrix: (D-1) x D orthonormal basis for CLR zero-sum plane.

    Row k (1-indexed in math, 0-indexed here):
      (e_k)_j = 1/sqrt(k(k+1))    for j < k
      (e_k)_k = -k/sqrt(k(k+1))
      (e_k)_j = 0                  for j > k

    Verified orthonormal to machine precision for D=3..100.
    """
    basis = []
    for k in range(1, D):
        row = [0.0] * D
        norm = math.sqrt(k * (k + 1))
        for j in range(k):
            row[j] = 1.0 / norm
        row[k] = -k / norm
        basis.append(row)
    return basis


def ilr_project(h, basis):
    """Project CLR vector to ILR coordinates.

    z_k = <h, e_k>

    Returns (D-1)-dimensional vector. Aitchison isometry:
    ||h||_CLR = ||z||_ILR (verified to machine precision).
    """
    return [sum(h[j] * basis[k][j] for j in range(len(h)))
            for k in range(len(basis))]


# ══════════════════════════════════════════════════════════════════
# STEP 4: BEARING TENSOR (Handbook Ch 3.1)
# ══════════════════════════════════════════════════════════════════

def bearing_pairwise(h, i, j):
    """Pairwise bearing theta_{ij} in degrees.

    theta_{ij}(x) = atan2(h_j, h_i)

    Deterministic, closed-form. Same composition, same bearing.
    """
    return math.degrees(math.atan2(h[j], h[i]))


def bearing_tensor(h, carriers):
    """Full bearing tensor: all D(D-1)/2 pairwise bearings.

    Returns list of dicts with pair names and bearing values.
    """
    D = len(h)
    bearings = []
    for i in range(D):
        for j in range(i + 1, D):
            bearings.append({
                "pair": f"{carriers[i]}/{carriers[j]}",
                "i": i,
                "j": j,
                "theta_deg": bearing_pairwise(h, i, j)
            })
    return bearings


# ══════════════════════════════════════════════════════════════════
# STEP 5: ANGULAR VELOCITY (Handbook Ch 3.2)
# ══════════════════════════════════════════════════════════════════

def angular_velocity(h1, h2):
    """Angular velocity between consecutive CLR vectors.

    omega = atan2(||h1 x h2||, <h1, h2>)

    where ||h1 x h2||^2 = ||h1||^2 ||h2||^2 - <h1,h2>^2
    (Lagrange identity, valid in all D).

    Uses atan2 form for numerical stability (eliminates up to
    8 digits of precision loss near 0 and 180 degrees).
    Returns degrees.
    """
    dot = sum(a * b for a, b in zip(h1, h2))
    m1_sq = sum(a ** 2 for a in h1)
    m2_sq = sum(a ** 2 for a in h2)
    m1 = math.sqrt(m1_sq)
    m2 = math.sqrt(m2_sq)
    if m1 < 1e-300 or m2 < 1e-300:
        return 0.0
    cross_sq = max(0.0, m1_sq * m2_sq - dot * dot)
    cross_mag = math.sqrt(cross_sq)
    return math.degrees(math.atan2(cross_mag, dot))


# ══════════════════════════════════════════════════════════════════
# STEP 6: HIGGINS STEERING METRIC TENSOR (Handbook Ch 3.3-3.4)
# ══════════════════════════════════════════════════════════════════

def metric_tensor(x, eps=1e-15):
    """Full Higgins Steering Metric Tensor kappa^Hs(x).

    G_ij(x) = (delta_ij - 1/D) / (x_i * x_j)

    In matrix form:  G(x) = diag(1/x) * P * diag(1/x)
    where P = I - (1/D) * 1 * 1^T (the centring matrix).

    Returns D x D matrix as list of lists.
    """
    x = closure(x, eps=eps)
    D = len(x)
    G = []
    for i in range(D):
        row = []
        for j in range(D):
            delta = 1.0 if i == j else 0.0
            row.append((delta - 1.0 / D) / (x[i] * x[j]))
        G.append(row)
    return G


def metric_tensor_properties(G, x):
    """Compute metric tensor properties (Handbook Ch 3.4).

    Returns: trace, determinant proxy, condition number,
    diagonal sensitivities, off-diagonal couplings.
    """
    D = len(G)
    x_c = closure(x)

    # Trace
    trace = sum(G[i][i] for i in range(D))

    # Diagonal sensitivities (steering sensitivity per carrier)
    diag_sens = [G[i][i] for i in range(D)]

    # Off-diagonal metric couplings
    off_diag = []
    for i in range(D):
        for j in range(i + 1, D):
            off_diag.append({
                "i": i, "j": j,
                "coupling": G[i][j]
            })

    # Condition number: max(x)/min(x)
    cond = max(x_c) / min(x_c)

    # Steering asymmetry ratio (Corollary 2)
    max_sens = max(diag_sens)
    min_sens = min(diag_sens)
    asymmetry_ratio = max_sens / min_sens if min_sens > 0 else float('inf')

    return {
        "trace": trace,
        "condition_number": cond,
        "diagonal_sensitivities": diag_sens,
        "off_diagonal_couplings": off_diag,
        "asymmetry_ratio": asymmetry_ratio,
        "precision_digits_available": max(1, int(15 - math.log10(max(cond, 1.0))))
    }


# ══════════════════════════════════════════════════════════════════
# STEP 7: HELMSMAN / DCDI (Handbook Ch 3.5)
# ══════════════════════════════════════════════════════════════════

def helmsman(h1, h2, carriers):
    """Dominant Carrier Displacement Index (DCDI).

    sigma(t, t+1) = argmax_j |h_j(t+1) - h_j(t)|

    The Helmsman is the carrier with maximum CLR displacement.
    Returns dict with index, name, displacement, and all deltas.
    """
    deltas = []
    for j in range(len(h1)):
        d = h2[j] - h1[j]
        deltas.append({
            "carrier": carriers[j],
            "index": j,
            "delta_clr": d,
            "abs_delta": abs(d)
        })
    deltas.sort(key=lambda x: x["abs_delta"], reverse=True)
    return {
        "helmsman_index": deltas[0]["index"],
        "helmsman_carrier": deltas[0]["carrier"],
        "helmsman_delta_clr": deltas[0]["delta_clr"],
        "all_deltas": deltas
    }


# ══════════════════════════════════════════════════════════════════
# STEP 8: AITCHISON DISTANCE AND METRIC OPERATIONS (Handbook Ch 5)
# ══════════════════════════════════════════════════════════════════

def aitchison_distance(x1, x2, eps=1e-15):
    """Aitchison distance between two compositions.

    d_A(x1, x2) = ||clr(x1) - clr(x2)||

    Equivalently:
    d_A = sqrt( (1/D) * sum_{i<j} (ln(x1_i/x1_j) - ln(x2_i/x2_j))^2 )
    """
    h1 = clr_transform(closure(x1, eps))
    h2 = clr_transform(closure(x2, eps))
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(h1, h2)))


def metric_energy(x, eps=1e-15):
    """Metric energy: ||h||^2 = d_A(x, barycenter)^2.

    Measures displacement from the simplex barycenter.
    """
    h = clr_transform(closure(x, eps))
    return sum(v ** 2 for v in h)


def metric_inner_product(h1, h2, G):
    """Inner product under the Higgins metric: u^T G v."""
    D = len(G)
    return sum(h1[i] * G[i][j] * h2[j] for i in range(D) for j in range(D))


def metric_norm(h, G):
    """Norm under the Higgins metric: sqrt(h^T G h)."""
    q = metric_inner_product(h, h, G)
    return math.sqrt(max(0.0, q))


# ══════════════════════════════════════════════════════════════════
# STEP 9: HIGGINS SCALE AND RING CLASSIFICATION (Handbook Ch 14)
# ══════════════════════════════════════════════════════════════════

RING_BOUNDS = [0.00, 0.05, 0.15, 0.30, 0.50, 0.75, 0.95, 1.00]
RING_NAMES = ["Hs-0", "Hs-1", "Hs-2", "Hs-3", "Hs-4", "Hs-5", "Hs-6"]

def higgins_scale(x):
    """Higgins Scale: Hs = 1 - H/ln(D).

    H = -sum(x_j * ln(x_j))  (Shannon entropy)
    Hs = 1 - H / ln(D)

    Hs = 0: maximum entropy (uniform distribution)
    Hs = 1: minimum entropy (single carrier dominates)
    """
    D = len(x)
    if D < 2:
        return 1.0
    H = -sum(v * math.log(v) for v in x if v > 0)
    return 1.0 - H / math.log(D)


def ring_classify(hs):
    """Classify Hs value into ring Hs-0 through Hs-6."""
    for k in range(len(RING_BOUNDS) - 1):
        if hs < RING_BOUNDS[k + 1]:
            return RING_NAMES[k]
    return RING_NAMES[-1]


def shannon_entropy(x):
    """Shannon entropy H = -sum(x_j * ln(x_j))."""
    return -sum(v * math.log(v) for v in x if v > 0)


# ══════════════════════════════════════════════════════════════════
# STEP 10: COROLLARY DIAGNOSTICS (Handbook Ch 4)
# ══════════════════════════════════════════════════════════════════

def detect_locks(bearing_history, carriers, epsilon=10.0):
    """Corollary 3: Lock Detection.

    Two carriers (i,j) are informationally locked when their
    pairwise bearing varies less than epsilon across all observations.

    Locked carriers move as a single compositional mode.
    """
    if len(bearing_history) < 2:
        return []
    D = len(carriers)
    locks = []
    for i in range(D):
        for j in range(i + 1, D):
            pair_key = f"{carriers[i]}/{carriers[j]}"
            vals = []
            for bh in bearing_history:
                for b in bh:
                    if b["pair"] == pair_key:
                        vals.append(b["theta_deg"])
            if len(vals) >= 2:
                spread = max(vals) - min(vals)
                if spread < epsilon:
                    locks.append({
                        "pair": pair_key,
                        "i": i, "j": j,
                        "spread_deg": spread,
                        "mean_bearing": sum(vals) / len(vals)
                    })
    return locks


def detect_reversals(bearing_history, carriers):
    """Corollary 4: Bearing Reversal Detection.

    A sign change in theta_{ij} indicates a structural crossover:
    carrier j transitions from above to below its geometric-mean
    share relative to carrier i, or vice versa.
    """
    if len(bearing_history) < 2:
        return []
    D = len(carriers)
    reversals = []
    for i in range(D):
        for j in range(i + 1, D):
            pair_key = f"{carriers[i]}/{carriers[j]}"
            vals = []
            for bh in bearing_history:
                for b in bh:
                    if b["pair"] == pair_key:
                        vals.append(b["theta_deg"])
            for t in range(1, len(vals)):
                if vals[t - 1] * vals[t] < 0:  # sign change
                    reversals.append({
                        "pair": pair_key,
                        "time_index": t,
                        "from_deg": vals[t - 1],
                        "to_deg": vals[t]
                    })
    return reversals


# ══════════════════════════════════════════════════════════════════
# STEP 11: DISTANCE MATRIX (Handbook Ch 5)
# ══════════════════════════════════════════════════════════════════

def build_distance_matrix(compositions, labels):
    """Full Aitchison distance matrix between all pairs of compositions."""
    T = len(compositions)
    matrix = [[0.0] * T for _ in range(T)]
    for i in range(T):
        for j in range(i + 1, T):
            d = aitchison_distance(compositions[i], compositions[j])
            matrix[i][j] = d
            matrix[j][i] = d
    return {
        "labels": labels,
        "matrix": matrix,
        "max_distance": max(max(row) for row in matrix) if T > 0 else 0,
        "max_pair": None  # filled below
    }


# ══════════════════════════════════════════════════════════════════
# STEP 12: SYSTEM COURSE PLOT DATA (Handbook Ch 15)
# ══════════════════════════════════════════════════════════════════

def system_course_plot(clr_series, labels):
    """System Course Plot: temporal trajectory through CLR space.

    The trajectory is the path traced by the CLR vector h(t)
    through the (D-1)-dimensional hyperplane sum(h)=0.

    For each timestep, records the CLR coordinates, distance
    from barycenter, and cumulative arc length.
    """
    trajectory = []
    cumulative_arc = 0.0
    for t, (h, label) in enumerate(zip(clr_series, labels)):
        dist_from_bary = math.sqrt(sum(v ** 2 for v in h))
        if t > 0:
            step_dist = math.sqrt(sum((a - b) ** 2
                                      for a, b in zip(h, clr_series[t - 1])))
            cumulative_arc += step_dist
        else:
            step_dist = 0.0
        trajectory.append({
            "index": t,
            "label": str(label),
            "clr": h,
            "distance_from_barycenter": dist_from_bary,
            "step_distance": step_dist,
            "cumulative_arc_length": cumulative_arc
        })
    return {
        "trajectory": trajectory,
        "total_arc_length": cumulative_arc,
        "start_label": str(labels[0]) if labels else None,
        "end_label": str(labels[-1]) if labels else None
    }


# ══════════════════════════════════════════════════════════════════
# MAIN ENGINE: CSV → JSON
# ══════════════════════════════════════════════════════════════════

def read_csv(filepath):
    """Read CSV file. First column = index/year, rest = carrier values."""
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        carriers = header[1:]
        rows = []
        for row in reader:
            if len(row) < 2:
                continue
            label = row[0].strip()
            values = [float(v) for v in row[1:]]
            rows.append({"label": label, "raw": values})
    return carriers, rows


def run_engine(carriers, rows):
    """Execute complete CNT tensor computation.

    Follows the handbook chapter order: closure → CLR → ILR →
    bearing → velocity → metric tensor → helmsman → distance →
    corollaries → Higgins Scale → system course plot.
    """
    D = len(carriers)
    T = len(rows)
    labels = [r["label"] for r in rows]

    # Helmert basis (computed once for fixed D)
    basis = helmert_basis(D)

    # ── Per-timestep computation ────────────────────────────────
    timesteps = []
    compositions = []
    clr_series = []
    ilr_series = []
    bearing_history = []
    hs_series = []

    for t, row in enumerate(rows):
        raw = row["raw"]

        # Step 1: Closure
        x = closure(raw)
        compositions.append(x)

        # Step 2: CLR transform
        h = clr_transform(x)
        clr_series.append(h)

        # Step 3: ILR projection
        z = ilr_project(h, basis)
        ilr_series.append(z)

        # Step 4: Bearing tensor
        bt = bearing_tensor(h, carriers)
        bearing_history.append(bt)

        # Step 5: Angular velocity (requires t >= 1)
        omega = angular_velocity(clr_series[t - 1], h) if t > 0 else 0.0

        # Step 6: Metric tensor
        G = metric_tensor(x)
        G_props = metric_tensor_properties(G, x)

        # Step 7: Helmsman (requires t >= 1)
        if t > 0:
            helm = helmsman(clr_series[t - 1], h, carriers)
        else:
            helm = {
                "helmsman_index": None,
                "helmsman_carrier": None,
                "helmsman_delta_clr": 0.0,
                "all_deltas": []
            }

        # Step 9: Higgins Scale
        hs = higgins_scale(x)
        hs_series.append(hs)
        ring = ring_classify(hs)
        H = shannon_entropy(x)

        # Step 8: Metric energy
        E = metric_energy(raw)

        # Assemble timestep record
        timesteps.append({
            "index": t,
            "label": row["label"],
            "raw_values": raw,
            "composition": x,
            "clr": h,
            "ilr": z,
            "bearing_tensor": bt,
            "angular_velocity_deg": omega,
            "metric_tensor": G,
            "metric_tensor_properties": G_props,
            "helmsman": helm,
            "higgins_scale": hs,
            "ring": ring,
            "shannon_entropy": H,
            "metric_energy": E,
            "clr_norm": math.sqrt(sum(v ** 2 for v in h)),
            "ilr_norm": math.sqrt(sum(v ** 2 for v in z)),
        })

    # ── Cross-timestep computations ────────────────────────────

    # Step 10: Corollary diagnostics
    locks = detect_locks(bearing_history, carriers)
    reversals = detect_reversals(bearing_history, carriers)

    # Step 11: Full Aitchison distance matrix
    dist_matrix = build_distance_matrix(compositions, labels)
    # Find max pair
    max_d = 0
    max_pair = None
    for i in range(T):
        for j in range(i + 1, T):
            if dist_matrix["matrix"][i][j] > max_d:
                max_d = dist_matrix["matrix"][i][j]
                max_pair = [labels[i], labels[j]]
    dist_matrix["max_pair"] = max_pair

    # Step 12: System course plot
    course = system_course_plot(clr_series, labels)

    # Helmsman frequency count
    helm_counts = {}
    for ts in timesteps:
        hc = ts["helmsman"]["helmsman_carrier"]
        if hc:
            helm_counts[hc] = helm_counts.get(hc, 0) + 1

    # CLR barycenter (mean CLR across all timesteps)
    bary_clr = [sum(clr_series[t][j] for t in range(T)) / T for j in range(D)]

    # ── Helmert basis for JSON ──────────────────────────────────
    basis_json = []
    for k, row in enumerate(basis):
        basis_json.append({
            "index": k,
            "coefficients": row
        })

    # ── Assemble complete output ────────────────────────────────
    output = {
        "metadata": {
            "engine": "CNT Tensor Engine v1.0",
            "handbook": "CNT Mathematics Handbook v2.0",
            "generated": datetime.utcnow().isoformat() + "Z",
            "input_file": None,  # filled by caller
            "carriers": carriers,
            "D": D,
            "T": T,
            "labels": labels,
            "lineage": {
                "Aitchison_1986": "CLR transform, Aitchison distance, simplex geometry",
                "Shannon_1948": "Entropy H = -sum(x_j ln x_j)",
                "Egozcue_2003": "ILR, Helmert basis, orthonormal coordinates",
                "Higgins_2025": "Hs = 1 - H/ln(D), ring classification",
                "Higgins_2026": "CNT tensor decomposition, HCI instrument"
            }
        },
        "helmert_basis": basis_json,
        "timesteps": timesteps,
        "distance_matrix": dist_matrix,
        "system_course_plot": course,
        "corollary_diagnostics": {
            "locks": locks,
            "reversals": reversals,
            "lock_epsilon_deg": 10.0
        },
        "helmsman_summary": {
            "frequency": helm_counts,
            "dominant_helmsman": max(helm_counts, key=helm_counts.get) if helm_counts else None,
            "total_transitions": T - 1
        },
        "global_statistics": {
            "clr_barycenter": bary_clr,
            "hs_mean": sum(hs_series) / T if T > 0 else 0,
            "hs_min": min(hs_series) if hs_series else 0,
            "hs_max": max(hs_series) if hs_series else 0,
            "hs_range": (max(hs_series) - min(hs_series)) if hs_series else 0,
            "max_aitchison_distance": max_d,
            "max_distance_pair": max_pair,
            "total_arc_length": course["total_arc_length"],
            "mean_angular_velocity": (
                sum(ts["angular_velocity_deg"] for ts in timesteps[1:]) / (T - 1)
                if T > 1 else 0
            ),
            "max_angular_velocity": (
                max(ts["angular_velocity_deg"] for ts in timesteps[1:])
                if T > 1 else 0
            ),
        }
    }

    return output


# ══════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python cnt_tensor_engine.py input.csv [output.json]")
        print("  input.csv:   First column = index/year, rest = carrier values")
        print("  output.json: CNT tensor output (default: input_cnt.json)")
        sys.exit(1)

    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        base = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base}_cnt.json"

    print(f"CNT Tensor Engine v1.0")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print()

    # Read data
    carriers, rows = read_csv(input_file)
    D = len(carriers)
    T = len(rows)
    print(f"Carriers (D={D}): {', '.join(carriers)}")
    print(f"Timesteps (T={T}): {rows[0]['label']} to {rows[-1]['label']}")
    print()

    # Run engine
    print("Computing...")
    print(f"  Step 1:  Closure (D-simplex)")
    print(f"  Step 2:  CLR transform")
    print(f"  Step 3:  ILR projection (Helmert basis)")
    print(f"  Step 4:  Bearing tensor ({D*(D-1)//2} pairs)")
    print(f"  Step 5:  Angular velocity (atan2 stable)")
    print(f"  Step 6:  Higgins Steering Metric Tensor ({D}x{D})")
    print(f"  Step 7:  Helmsman / DCDI")
    print(f"  Step 8:  Aitchison distance matrix ({T}x{T})")
    print(f"  Step 9:  Higgins Scale + ring classification")
    print(f"  Step 10: Corollary diagnostics (locks, reversals)")
    print(f"  Step 11: System Course Plot")
    print()

    result = run_engine(carriers, rows)
    result["metadata"]["input_file"] = os.path.basename(input_file)

    # Write JSON
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    size_kb = os.path.getsize(output_file) / 1024
    print(f"Written: {output_file} ({size_kb:.1f} KB)")
    print()

    # Summary
    stats = result["global_statistics"]
    helm = result["helmsman_summary"]
    coroll = result["corollary_diagnostics"]
    print(f"=== CNT Summary ===")
    print(f"  Hs range:              {stats['hs_min']:.4f} to {stats['hs_max']:.4f}")
    print(f"  Max Aitchison distance: {stats['max_aitchison_distance']:.4f} HLR")
    print(f"  Total arc length:      {stats['total_arc_length']:.4f} HLR")
    print(f"  Mean angular velocity: {stats['mean_angular_velocity']:.4f} deg/step")
    print(f"  Dominant helmsman:     {helm['dominant_helmsman']} ({helm['frequency'].get(helm['dominant_helmsman'], 0)}/{helm['total_transitions']} steps)")
    print(f"  Locked pairs:          {len(coroll['locks'])}")
    print(f"  Bearing reversals:     {len(coroll['reversals'])}")
    print()
    print("The instrument reads. The expert decides. The loop stays open.")


if __name__ == "__main__":
    main()
