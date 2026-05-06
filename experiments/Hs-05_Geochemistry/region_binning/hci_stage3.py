#!/usr/bin/env python3
"""
HCI Stage 3 — Higher-Degree Structural Analysis Engine
=======================================================

Extends analysis beyond pairwise into triadic, subcomposition,
and regime-level structural signatures.

Input:  Stage 1 data + Stage 2 results
Output: CSV ledgers + JSON ranked findings + TXT summary report

Degree ladder:
  D0: Point state
  D1: Temporal increment
  D2: Pairwise contrast (Stage 2)
  D3: Triadic structure (Stage 3)
  Dk: Subcomposition / k-face structure (Stage 3)

Mathematical lineage:
  Aitchison (1986) — CLR, Aitchison distance
  Egozcue et al. (2003) — ILR, balances, orthogonal subspaces
  Higgins (2026) — CNT, HCI, degree ladder analysis

The instrument reads. The expert decides. The loop stays open.
"""

import math
import csv
import json
import os
from itertools import combinations


# ══════════════════════════════════════════════════════════════════
# SHARED GEOMETRY (same as Stage 2 — uses the SAME coordinate frame)
# ══════════════════════════════════════════════════════════════════

def _closure(x, eps=1e-15):
    x_pos = [max(float(v), eps) for v in x]
    total = sum(x_pos)
    return [v / total for v in x_pos]


def _clr(x):
    D = len(x)
    log_x = [math.log(v) for v in x]
    mean_log = sum(log_x) / D
    return [lx - mean_log for lx in log_x]


def _metric_distance(h1, h2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(h1, h2)))


def _metric_energy(h):
    return sum(v ** 2 for v in h)


def _barycenter(h_list):
    if not h_list:
        return []
    D = len(h_list[0])
    n = len(h_list)
    return [sum(h[j] for h in h_list) / n for j in range(D)]


def _boundary_pressure(x, eps=1e-15):
    x = _closure(x, eps=eps)
    return max(1.0 / v for v in x)


# ══════════════════════════════════════════════════════════════════
# STAGE 3 METHODS
# ══════════════════════════════════════════════════════════════════

def triadic_day_analysis(data):
    """Stage 3.1 — Evaluate all three-day combinations as metric triangles.

    For each triad of days, computes:
      - Three side lengths (Aitchison distance between day barycenters)
      - Metric triangle area (Heron's formula in CLR space)
      - Triadic imbalance (ratio of longest to shortest side)
      - Orientation score (cross product sign in first two CLR dimensions)
      - Dominant carrier (largest barycenter spread across the three days)
    """
    days = data.unique_days()
    if len(days) < 3:
        return []

    # Compute day barycenters
    day_barycenters = {}
    for day in days:
        pts = data.get_day_points(day)
        h_list = [data.h[i] for i in pts]
        day_barycenters[day] = _barycenter(h_list)

    triads = list(combinations(days, 3))
    results = []

    for triad_idx, (da, db, dc) in enumerate(triads):
        ba = day_barycenters[da]
        bb = day_barycenters[db]
        bc = day_barycenters[dc]

        # Side lengths
        side_ab = _metric_distance(ba, bb)
        side_bc = _metric_distance(bb, bc)
        side_ca = _metric_distance(bc, ba)

        # Heron's formula for triangle area
        s = (side_ab + side_bc + side_ca) / 2.0
        area_sq = s * (s - side_ab) * (s - side_bc) * (s - side_ca)
        area = math.sqrt(max(0.0, area_sq))

        # Triadic imbalance
        sides = [side_ab, side_bc, side_ca]
        min_side = min(sides)
        max_side = max(sides)
        imbalance = max_side / max(min_side, 1e-300)

        # Orientation score (2D cross product in first two CLR dimensions)
        if len(ba) >= 2:
            v1 = [bb[k] - ba[k] for k in range(len(ba))]
            v2 = [bc[k] - ba[k] for k in range(len(ba))]
            # Use first two dimensions for orientation
            cross = v1[0] * v2[1] - v1[1] * v2[0]
            orientation = 1.0 if cross > 0 else (-1.0 if cross < 0 else 0.0)
        else:
            orientation = 0.0

        # Dominant carrier: max barycenter spread across the three days
        D = len(ba)
        carrier_spreads = []
        for k in range(D):
            vals = [ba[k], bb[k], bc[k]]
            carrier_spreads.append((max(vals) - min(vals), k))
        carrier_spreads.sort(reverse=True)
        dom_carrier = data.carrier_names[carrier_spreads[0][1]]

        results.append({
            "triad_id": f"T{triad_idx + 1:03d}",
            "day_A": str(da),
            "day_B": str(db),
            "day_C": str(dc),
            "side_AB": side_ab,
            "side_BC": side_bc,
            "side_CA": side_ca,
            "metric_triangle_area": area,
            "triadic_imbalance": imbalance,
            "orientation_score": orientation,
            "dominant_carrier": dom_carrier,
            "rank": 0,
            "classification": "",
        })

    # Rank by metric triangle area (largest first)
    results.sort(key=lambda r: r["metric_triangle_area"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1
        if r["metric_triangle_area"] > 0.1:
            r["classification"] = "LARGE_TRIADIC_STRUCTURE"
        elif r["metric_triangle_area"] > 0.01:
            r["classification"] = "MODERATE_TRIADIC_STRUCTURE"
        else:
            r["classification"] = "COMPACT_TRIAD"

    return results


def carrier_triad_analysis(data):
    """Stage 3.2 — Evaluate three-carrier interaction structures.

    For each carrier triad, computes coupling and opposition
    across the full run.
    """
    D = data.D
    N = data.N
    if D < 3:
        return []

    carrier_triads = list(combinations(range(D), 3))
    results = []

    for triad_idx, (ci, cj, ck) in enumerate(carrier_triads):
        # Extract CLR increment series for each carrier
        if N < 2:
            continue

        dhi = [data.h[t + 1][ci] - data.h[t][ci] for t in range(N - 1)]
        dhj = [data.h[t + 1][cj] - data.h[t][cj] for t in range(N - 1)]
        dhk = [data.h[t + 1][ck] - data.h[t][ck] for t in range(N - 1)]

        T = len(dhi)

        # Triadic coupling: how much all three move together
        # Use average absolute correlation across all three pairs
        def _corr(a, b):
            ma = sum(a) / len(a)
            mb = sum(b) / len(b)
            cov = sum((a[t] - ma) * (b[t] - mb) for t in range(len(a)))
            va = sum((a[t] - ma) ** 2 for t in range(len(a)))
            vb = sum((b[t] - mb) ** 2 for t in range(len(b)))
            den = math.sqrt(max(va, 1e-300) * max(vb, 1e-300))
            return cov / den if den > 1e-300 else 0.0

        r_ij = _corr(dhi, dhj)
        r_jk = _corr(dhj, dhk)
        r_ik = _corr(dhi, dhk)

        coupling = (abs(r_ij) + abs(r_jk) + abs(r_ik)) / 3.0
        opposition = (max(0, -r_ij) + max(0, -r_jk) + max(0, -r_ik)) / 3.0

        # Dominant time window: which day has max combined carrier activity
        days = data.unique_days()
        day_activity = {}
        for day in days:
            pts = data.get_day_points(day)
            act = 0.0
            for t in pts:
                if t > 0 and data.day_ids[t - 1] == day:
                    act += abs(data.h[t][ci] - data.h[t - 1][ci])
                    act += abs(data.h[t][cj] - data.h[t - 1][cj])
                    act += abs(data.h[t][ck] - data.h[t - 1][ck])
            day_activity[day] = act

        dom_window = max(day_activity, key=day_activity.get) if day_activity else "---"

        results.append({
            "carrier_triad": f"{data.carrier_names[ci]}-{data.carrier_names[cj]}-{data.carrier_names[ck]}",
            "carrier_i": ci,
            "carrier_j": cj,
            "carrier_k": ck,
            "triadic_coupling_score": coupling,
            "triadic_opposition_score": opposition,
            "dominant_time_window": str(dom_window),
            "dominant_section_view": "XY",
            "rank": 0,
            "classification": "",
        })

    # Rank by triadic coupling score
    results.sort(key=lambda r: r["triadic_coupling_score"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1
        if r["triadic_coupling_score"] > 0.6:
            r["classification"] = "STRONG_TRIADIC_COUPLING"
        elif r["triadic_coupling_score"] > 0.3:
            r["classification"] = "MODERATE_TRIADIC_COUPLING"
        else:
            r["classification"] = "WEAK_TRIADIC_COUPLING"

    return results


def subcomposition_degree_ladder(data, max_degree=None):
    """Stage 3.3 — Analyze k-degree carrier subsets from degree 2 up.

    For each carrier subset of size k, computes:
      - Subcomposition metric energy
      - Boundary pressure within the subcomposition
      - Stability score (variance of energy across time)
    """
    D = data.D
    N = data.N

    if max_degree is None:
        max_degree = min(D, 6)  # cap for computational feasibility

    results = []
    subset_id = 0

    for k in range(2, max_degree + 1):
        subsets = list(combinations(range(D), k))

        for carriers in subsets:
            subset_id += 1

            # Extract subcomposition for each point
            sub_energies = []
            sub_pressures = []
            for t in range(N):
                # Subcomposition: extract and re-close
                sub_x = [data.x[t][c] for c in carriers]
                sub_x_closed = _closure(sub_x)
                sub_h = _clr(sub_x_closed)
                sub_energies.append(_metric_energy(sub_h))
                sub_pressures.append(_boundary_pressure(sub_x_closed))

            mean_energy = sum(sub_energies) / N
            max_pressure = max(sub_pressures)

            # Stability: inverse of energy variance
            var_energy = sum((e - mean_energy) ** 2 for e in sub_energies) / N
            stability = 1.0 / (1.0 + var_energy)

            # Dominant time window
            days = data.unique_days()
            day_energies = {}
            for day in days:
                pts = data.get_day_points(day)
                day_energies[day] = sum(sub_energies[t] for t in pts) / max(len(pts), 1)
            dom_window = max(day_energies, key=day_energies.get) if day_energies else "---"

            carrier_names_str = "-".join(data.carrier_names[c] for c in carriers)

            results.append({
                "degree_k": k,
                "subset_id": f"S{subset_id:04d}",
                "carrier_subset": carrier_names_str,
                "subset_metric_energy": mean_energy,
                "subset_boundary_pressure": max_pressure,
                "subset_stability_score": stability,
                "dominant_time_window": str(dom_window),
                "rank": 0,
                "classification": "",
            })

    # Rank by metric energy within each degree
    results.sort(key=lambda r: (r["degree_k"], -r["subset_metric_energy"]))
    rank_within_degree = {}
    for r in results:
        k = r["degree_k"]
        rank_within_degree[k] = rank_within_degree.get(k, 0) + 1
        r["rank"] = rank_within_degree[k]
        if r["subset_stability_score"] > 0.9:
            r["classification"] = "STABLE_SUBCOMPOSITION"
        elif r["subset_stability_score"] > 0.5:
            r["classification"] = "MODERATE_SUBCOMPOSITION"
        else:
            r["classification"] = "UNSTABLE_SUBCOMPOSITION"

    return results


def metric_regime_detection(data, min_regime_size=3):
    """Stage 3.4 — Detect time windows with internally similar metric structure.

    Uses a simple sequential scan: groups consecutive points with
    similar metric energy into regimes, then computes within-regime
    variance and between-regime distance.
    """
    N = data.N
    if N < min_regime_size * 2:
        return []

    # Compute per-point metric energy
    energies = data.energies

    # Sequential regime detection using energy threshold
    mean_energy = sum(energies) / N
    std_energy = math.sqrt(sum((e - mean_energy) ** 2 for e in energies) / N)
    threshold = max(std_energy * 0.5, 1e-6)

    # Build regimes by grouping consecutive points with similar energy
    regimes = []
    current_regime = [0]
    current_center = energies[0]

    for t in range(1, N):
        if abs(energies[t] - current_center) < threshold:
            current_regime.append(t)
            # Update running center
            current_center = sum(energies[i] for i in current_regime) / len(current_regime)
        else:
            if len(current_regime) >= min_regime_size:
                regimes.append(current_regime[:])
            current_regime = [t]
            current_center = energies[t]

    if len(current_regime) >= min_regime_size:
        regimes.append(current_regime[:])

    # If only one regime detected, try splitting at the midpoint
    if len(regimes) <= 1:
        mid = N // 2
        r1 = list(range(mid))
        r2 = list(range(mid, N))
        if len(r1) >= min_regime_size and len(r2) >= min_regime_size:
            regimes = [r1, r2]

    results = []
    for regime_idx, pts in enumerate(regimes):
        regime_energies = [energies[t] for t in pts]
        h_list = [data.h[t] for t in pts]
        bary = _barycenter(h_list)

        within_var = sum((e - sum(regime_energies) / len(regime_energies)) ** 2
                         for e in regime_energies) / len(regime_energies)

        # Dominant carriers in this regime
        carrier_activity = {}
        for t in pts:
            c = data.dcdi_carriers[t]
            if c is not None:
                carrier_activity[c] = carrier_activity.get(c, 0) + data.dcdi_deltas[t]

        dom_carriers = sorted(carrier_activity.items(), key=lambda x: x[1], reverse=True)
        dom_str = ";".join(f"{c}" for c, _ in dom_carriers[:3])

        results.append({
            "regime_id": f"R{regime_idx + 1:02d}",
            "time_window_start": str(data.day_ids[pts[0]]) + f"_pt{data.point_ids[pts[0]]}",
            "time_window_end": str(data.day_ids[pts[-1]]) + f"_pt{data.point_ids[pts[-1]]}",
            "member_points": len(pts),
            "within_regime_metric_variance": within_var,
            "between_regime_distance": 0.0,  # filled below
            "dominant_carriers": dom_str,
            "classification": "",
        })

    # Compute between-regime distances
    for i in range(len(results)):
        if i + 1 < len(results):
            bary_i = _barycenter([data.h[t] for t in regimes[i]])
            bary_j = _barycenter([data.h[t] for t in regimes[i + 1]])
            results[i]["between_regime_distance"] = _metric_distance(bary_i, bary_j)

    for r in results:
        if r["within_regime_metric_variance"] < 0.01:
            r["classification"] = "STABLE_REGIME"
        elif r["within_regime_metric_variance"] < 0.1:
            r["classification"] = "MODERATE_REGIME"
        else:
            r["classification"] = "VOLATILE_REGIME"

    return results


# ══════════════════════════════════════════════════════════════════
# OUTPUT WRITERS
# ══════════════════════════════════════════════════════════════════

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_day_triad_ledger(path, results):
    fieldnames = ["triad_id", "day_A", "day_B", "day_C",
                  "side_AB", "side_BC", "side_CA",
                  "metric_triangle_area", "triadic_imbalance",
                  "orientation_score", "dominant_carrier", "rank", "classification"]
    write_csv(path, results, fieldnames)


def write_carrier_triad_ledger(path, results):
    fieldnames = ["carrier_triad", "triadic_coupling_score",
                  "triadic_opposition_score", "dominant_time_window",
                  "dominant_section_view", "rank", "classification"]
    write_csv(path, results, fieldnames)


def write_subcomposition_ledger(path, results):
    fieldnames = ["degree_k", "subset_id", "carrier_subset",
                  "subset_metric_energy", "subset_boundary_pressure",
                  "subset_stability_score", "dominant_time_window",
                  "rank", "classification"]
    write_csv(path, results, fieldnames)


def write_regime_ledger(path, results):
    fieldnames = ["regime_id", "time_window_start", "time_window_end",
                  "member_points", "within_regime_metric_variance",
                  "between_regime_distance", "dominant_carriers", "classification"]
    write_csv(path, results, fieldnames)


def write_ranked_findings(path, day_triads, carrier_triads, subcomp, regimes):
    findings = {
        "stage": "Stage 3 — HCI Higher-Degree Analysis Engine",
        "top_day_triads": [
            {k: v for k, v in r.items() if k not in ("carrier_i", "carrier_j", "carrier_k")}
            for r in day_triads[:5]
        ],
        "top_carrier_triads": [
            {k: v for k, v in r.items() if k not in ("carrier_i", "carrier_j", "carrier_k")}
            for r in carrier_triads[:5]
        ],
        "subcomposition_summary": {
            "total_subsets": len(subcomp),
            "stable_count": sum(1 for r in subcomp if r["classification"] == "STABLE_SUBCOMPOSITION"),
            "unstable_count": sum(1 for r in subcomp if r["classification"] == "UNSTABLE_SUBCOMPOSITION"),
        },
        "regime_summary": [
            {k: v for k, v in r.items()}
            for r in regimes
        ],
    }
    with open(path, "w") as f:
        json.dump(findings, f, indent=2)


def write_summary_report(path, data, day_triads, carrier_triads, subcomp, regimes):
    lines = []
    lines.append("=" * 72)
    lines.append("HCI STAGE 3 — HIGHER-DEGREE STRUCTURAL ANALYSIS ENGINE")
    lines.append("Summary Report")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"  Carriers (D):         {data.D}")
    lines.append(f"  Observations (N):     {data.N}")
    lines.append(f"  Day triads:           {len(day_triads)}")
    lines.append(f"  Carrier triads:       {len(carrier_triads)}")
    lines.append(f"  Subcomposition sets:  {len(subcomp)}")
    lines.append(f"  Detected regimes:     {len(regimes)}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("TOP DAY TRIADS (by metric triangle area)")
    lines.append("-" * 72)
    for r in day_triads[:5]:
        lines.append(f"  Rank {r['rank']:3d}: Days {r['day_A']}-{r['day_B']}-{r['day_C']}  "
                     f"area={r['metric_triangle_area']:.6f}  imbal={r['triadic_imbalance']:.2f}  "
                     f"carrier={r['dominant_carrier']}  [{r['classification']}]")
    lines.append("")

    lines.append("-" * 72)
    lines.append("TOP CARRIER TRIADS (by coupling score)")
    lines.append("-" * 72)
    for r in carrier_triads[:5]:
        lines.append(f"  Rank {r['rank']:3d}: {r['carrier_triad']:>20s}  "
                     f"coupling={r['triadic_coupling_score']:.3f}  "
                     f"opposition={r['triadic_opposition_score']:.3f}  "
                     f"[{r['classification']}]")
    lines.append("")

    lines.append("-" * 72)
    lines.append("METRIC REGIMES")
    lines.append("-" * 72)
    for r in regimes:
        lines.append(f"  {r['regime_id']}: {r['time_window_start']} to {r['time_window_end']}  "
                     f"pts={r['member_points']}  within_var={r['within_regime_metric_variance']:.6f}  "
                     f"between_dist={r['between_regime_distance']:.4f}  "
                     f"[{r['classification']}]")
    lines.append("")

    lines.append("-" * 72)
    lines.append("The instrument reads. The expert decides. The loop stays open.")
    lines.append("-" * 72)

    with open(path, "w") as f:
        f.write("\n".join(lines))


# ══════════════════════════════════════════════════════════════════
# MAIN RUNNER
# ══════════════════════════════════════════════════════════════════

def run_stage3(data, output_dir="."):
    """Run complete Stage 3 higher-degree analysis.

    Args:
        data: Stage1Data object (from Stage 2 run)
        output_dir: directory for output files

    Returns:
        dict with all results
    """
    os.makedirs(output_dir, exist_ok=True)

    # 3.1 Triadic day analysis
    day_triads = triadic_day_analysis(data)

    # 3.2 Carrier triad analysis
    carrier_triads = carrier_triad_analysis(data)

    # 3.3 Subcomposition degree ladder
    subcomp = subcomposition_degree_ladder(data)

    # 3.4 Metric regime detection
    regimes = metric_regime_detection(data)

    # Write outputs
    write_day_triad_ledger(os.path.join(output_dir, "stage3_day_triad_ledger.csv"), day_triads)
    write_carrier_triad_ledger(os.path.join(output_dir, "stage3_carrier_triad_ledger.csv"), carrier_triads)
    write_subcomposition_ledger(os.path.join(output_dir, "stage3_subcomposition_degree_ledger.csv"), subcomp)
    write_regime_ledger(os.path.join(output_dir, "stage3_metric_regime_ledger.csv"), regimes)
    write_ranked_findings(os.path.join(output_dir, "stage3_ranked_structural_findings.json"),
                          day_triads, carrier_triads, subcomp, regimes)
    write_summary_report(os.path.join(output_dir, "stage3_summary_report.txt"),
                         data, day_triads, carrier_triads, subcomp, regimes)

    return {
        "day_triads": day_triads,
        "carrier_triads": carrier_triads,
        "subcomposition": subcomp,
        "regimes": regimes,
    }
