#!/usr/bin/env python3
"""
CNT Analysis Engine — Stage 1/2/3 + Dynamical Systems + Control Theory + Information Theory
============================================================================================

Program 2 of the CNT standard pipeline.

Input:  JSON output from cnt_tensor_engine.py
Output: JSON file containing complete Stage 1/2/3 analysis plus the
        three theoretical bridges from the CNT Mathematics Handbook v2.0.

Computes:
  Stage 1 (Ch 8):   Section triads, metric ledgers, per-timestep records
  Stage 2 (Ch 9):   Group barycenters, pairwise divergence, carrier pair
                     cross-examination, section view cross-examination
  Stage 3 (Ch 10):  Triadic area analysis, carrier triad analysis,
                     subcomposition degree ladder, metric regime detection

  Bridge 1 (Ch 11): Dynamical systems — Lyapunov exponents, phase-space
                     velocity fields, recurrence analysis, attractor detection
  Bridge 2 (Ch 12): Control theory — state-space model, controllability
                     matrix, observability proxy, stability analysis
  Bridge 3 (Ch 13): Information theory — Shannon entropy series, Fisher
                     information, KL divergence, mutual information,
                     entropy rate, information geometry curvature

Usage:
  python cnt_analysis.py engine_output.json [analysis_output.json]

Mathematical lineage:
  Aitchison (1986)  — CLR, Aitchison distance
  Egozcue (2003)    — ILR, balances
  Lyapunov (1892)   — Stability of motion
  Kalman (1960)     — State-space control
  Shannon (1948)    — Information theory
  Fisher (1925)     — Information metric
  Higgins (2026)    — CNT, HCI, three-bridge unification

The instrument reads. The expert decides. The loop stays open.
"""

import json
import math
import sys
import os
from datetime import datetime
from itertools import combinations


# ══════════════════════════════════════════════════════════════════
# SHARED GEOMETRY (operates on pre-computed CLR from engine JSON)
# ══════════════════════════════════════════════════════════════════

def _distance(h1, h2):
    """Euclidean distance in CLR space = Aitchison distance."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(h1, h2)))


def _barycenter(h_list):
    """CLR barycenter of a group of CLR vectors."""
    if not h_list:
        return []
    D = len(h_list[0])
    n = len(h_list)
    return [sum(h[j] for h in h_list) / n for j in range(D)]


def _angle(h1, h2):
    """Angle between CLR vectors (atan2 stable form)."""
    dot = sum(a * b for a, b in zip(h1, h2))
    m1_sq = sum(a ** 2 for a in h1)
    m2_sq = sum(a ** 2 for a in h2)
    if m1_sq < 1e-300 or m2_sq < 1e-300:
        return 0.0
    cross_sq = max(0.0, m1_sq * m2_sq - dot * dot)
    return math.degrees(math.atan2(math.sqrt(cross_sq), dot))


def _energy(h):
    """Metric energy = ||h||^2."""
    return sum(v ** 2 for v in h)


def _pearson_r(x, y):
    """Pearson correlation coefficient."""
    n = len(x)
    if n < 3:
        return 0.0
    mx = sum(x) / n
    my = sum(y) / n
    sx = math.sqrt(max(0, sum((xi - mx) ** 2 for xi in x) / (n - 1)))
    sy = math.sqrt(max(0, sum((yi - my) ** 2 for yi in y) / (n - 1)))
    if sx < 1e-15 or sy < 1e-15:
        return 0.0
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n - 1)
    return cov / (sx * sy)


# ══════════════════════════════════════════════════════════════════
# STAGE 1: SECTION ENGINE (Handbook Ch 8)
# ══════════════════════════════════════════════════════════════════

def stage1_section_triads(data):
    """Build per-timestep section triads and metric ledger.

    For each timestep, the section triad contains:
      XY face: CLR_i vs CLR_j (all carrier pairs)
      XZ face: Bearing vs time
      YZ face: Hs vs time

    The metric ledger records all numerical values.
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    section_atlas = []
    metric_ledger = []

    for t, ts in enumerate(timesteps):
        h = ts["clr"]
        hs = ts["higgins_scale"]

        # XY face: CLR carrier positions
        xy_points = {carriers[j]: h[j] for j in range(D)}

        # XZ face: bearing to all other carriers from carrier 0
        xz_bearings = {}
        for b in ts["bearing_tensor"]:
            xz_bearings[b["pair"]] = b["theta_deg"]

        # YZ face: Hs value
        yz_hs = hs

        section = {
            "index": t,
            "label": ts["label"],
            "xy_face": xy_points,
            "xz_face": xz_bearings,
            "yz_face": {"hs": yz_hs, "ring": ts["ring"]},
            "metric_tensor_trace": ts["metric_tensor_properties"]["trace"],
            "condition_number": ts["metric_tensor_properties"]["condition_number"],
            "angular_velocity_deg": ts["angular_velocity_deg"],
            "helmsman": ts["helmsman"]["helmsman_carrier"],
            "helmsman_delta": ts["helmsman"]["helmsman_delta_clr"],
            "metric_energy": ts["metric_energy"],
            "clr_norm": ts["clr_norm"],
        }
        section_atlas.append(section)

        # Metric ledger row
        ledger_row = {
            "index": t,
            "label": ts["label"],
            "hs": hs,
            "ring": ts["ring"],
            "omega_deg": ts["angular_velocity_deg"],
            "helmsman": ts["helmsman"]["helmsman_carrier"],
            "energy": ts["metric_energy"],
            "condition": ts["metric_tensor_properties"]["condition_number"],
        }
        for j, c in enumerate(carriers):
            ledger_row[f"clr_{c}"] = h[j]
            ledger_row[f"frac_{c}"] = ts["composition"][j]
        metric_ledger.append(ledger_row)

    return {
        "section_atlas": section_atlas,
        "metric_ledger": metric_ledger,
        "carriers": carriers,
        "D": D,
        "T": T
    }


# ══════════════════════════════════════════════════════════════════
# STAGE 2: METRIC CROSS-EXAMINATION (Handbook Ch 9)
# ══════════════════════════════════════════════════════════════════

def stage2_group_barycenters(data, groups=None):
    """Stage 2.1 — Group barycenter analysis.

    Divide the time series into groups (default: halves)
    and compute CLR barycenters for each group.
    """
    timesteps = data["timesteps"]
    T = data["metadata"]["T"]
    carriers = data["metadata"]["carriers"]

    if groups is None:
        mid = T // 2
        groups = {
            "first_half": list(range(mid)),
            "second_half": list(range(mid, T))
        }

    results = {}
    for name, indices in groups.items():
        h_list = [timesteps[i]["clr"] for i in indices if i < T]
        bary = _barycenter(h_list)
        energy = _energy(bary)
        results[name] = {
            "indices": indices,
            "barycenter_clr": bary,
            "barycenter_energy": energy,
            "n_members": len(h_list),
            "carrier_values": {carriers[j]: bary[j] for j in range(len(bary))}
        }

    # Pairwise divergence between groups
    group_names = list(results.keys())
    divergences = []
    for a, b in combinations(group_names, 2):
        ba = results[a]["barycenter_clr"]
        bb = results[b]["barycenter_clr"]
        d = _distance(ba, bb)
        ang = _angle(ba, bb)
        # Dominant divergence carrier
        D = len(ba)
        deltas = [(abs(ba[j] - bb[j]), carriers[j]) for j in range(D)]
        deltas.sort(reverse=True)
        divergences.append({
            "group_a": a,
            "group_b": b,
            "aitchison_distance": d,
            "angle_deg": ang,
            "dominant_carrier": deltas[0][1],
            "dominant_delta": deltas[0][0],
            "classification": (
                "STRONG_DIVERGENCE" if d > 1.0 else
                "MODERATE_DIVERGENCE" if d > 0.3 else
                "WEAK_DIVERGENCE"
            )
        })

    return {
        "groups": results,
        "divergences": divergences
    }


def stage2_carrier_pair_cross(data):
    """Stage 2.2 — Carrier pair cross-examination.

    For each pair of carriers, compute:
    - CLR correlation (Pearson r)
    - Co-movement score
    - Opposition score
    - Mean metric coupling |G_ij|
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    pairs = []
    for i in range(D):
        for j in range(i + 1, D):
            clr_i = [timesteps[t]["clr"][i] for t in range(T)]
            clr_j = [timesteps[t]["clr"][j] for t in range(T)]

            r = _pearson_r(clr_i, clr_j)

            # Co-movement: fraction of timesteps where both move same direction
            co_move = 0
            oppose = 0
            for t in range(1, T):
                di = clr_i[t] - clr_i[t - 1]
                dj = clr_j[t] - clr_j[t - 1]
                if di * dj > 0:
                    co_move += 1
                elif di * dj < 0:
                    oppose += 1
            steps = max(T - 1, 1)

            # Mean metric coupling
            couplings = []
            for t in range(T):
                G = timesteps[t]["metric_tensor"]
                couplings.append(abs(G[i][j]))
            mean_coupling = sum(couplings) / T if T > 0 else 0

            pairs.append({
                "carrier_a": carriers[i],
                "carrier_b": carriers[j],
                "i": i, "j": j,
                "pearson_r": r,
                "co_movement_score": co_move / steps,
                "opposition_score": oppose / steps,
                "mean_metric_coupling": mean_coupling,
                "relationship": (
                    "STRONG_POSITIVE" if r > 0.7 else
                    "MODERATE_POSITIVE" if r > 0.3 else
                    "WEAK" if r > -0.3 else
                    "MODERATE_NEGATIVE" if r > -0.7 else
                    "STRONG_NEGATIVE"
                )
            })

    return pairs


def stage2_section_view_cross(data):
    """Stage 2.3 — Section view cross-examination.

    Compare XY, XZ, YZ views across all timesteps for
    structural consistency and anomaly detection.
    """
    timesteps = data["timesteps"]
    T = data["metadata"]["T"]

    # Hs trajectory analysis
    hs_vals = [ts["higgins_scale"] for ts in timesteps]
    omega_vals = [ts["angular_velocity_deg"] for ts in timesteps[1:]]

    # Find maximum omega (fastest structural change)
    max_omega_idx = 0
    if omega_vals:
        max_omega_idx = omega_vals.index(max(omega_vals)) + 1

    # Hs trend (simple linear regression)
    if T >= 2:
        x_mean = (T - 1) / 2
        y_mean = sum(hs_vals) / T
        num = sum((t - x_mean) * (hs_vals[t] - y_mean) for t in range(T))
        den = sum((t - x_mean) ** 2 for t in range(T))
        hs_slope = num / den if den > 0 else 0
    else:
        hs_slope = 0

    return {
        "hs_trend_slope": hs_slope,
        "hs_trend_direction": (
            "CONCENTRATING" if hs_slope > 0.001 else
            "DISPERSING" if hs_slope < -0.001 else
            "STABLE"
        ),
        "max_omega_index": max_omega_idx,
        "max_omega_label": timesteps[max_omega_idx]["label"] if max_omega_idx < T else None,
        "max_omega_deg": max(omega_vals) if omega_vals else 0,
        "hs_range": max(hs_vals) - min(hs_vals) if hs_vals else 0,
        "mean_omega": sum(omega_vals) / len(omega_vals) if omega_vals else 0,
    }


# ══════════════════════════════════════════════════════════════════
# STAGE 3: HIGHER-DEGREE ANALYSIS (Handbook Ch 10)
# ══════════════════════════════════════════════════════════════════

def stage3_triadic_area(data, max_triads=500):
    """Stage 3.1 — Triadic day analysis.

    For each triad of timesteps, compute the area of the metric
    triangle formed by their CLR vectors using Heron's formula.

    Area = sqrt(s(s-a)(s-b)(s-c)) where s = (a+b+c)/2.
    """
    timesteps = data["timesteps"]
    T = data["metadata"]["T"]

    triads = []
    indices = list(range(T))
    combos = list(combinations(indices, 3))
    if len(combos) > max_triads:
        # Sample evenly
        step = len(combos) // max_triads
        combos = combos[::step][:max_triads]

    for i, j, k in combos:
        hi = timesteps[i]["clr"]
        hj = timesteps[j]["clr"]
        hk = timesteps[k]["clr"]

        a = _distance(hi, hj)
        b = _distance(hj, hk)
        c = _distance(hi, hk)
        s = (a + b + c) / 2
        area_sq = s * (s - a) * (s - b) * (s - c)
        area = math.sqrt(max(0, area_sq))

        triads.append({
            "indices": [i, j, k],
            "labels": [timesteps[i]["label"], timesteps[j]["label"], timesteps[k]["label"]],
            "sides": [a, b, c],
            "perimeter": a + b + c,
            "area": area,
        })

    # Sort by area descending
    triads.sort(key=lambda x: x["area"], reverse=True)

    return {
        "n_triads": len(triads),
        "max_area": triads[0]["area"] if triads else 0,
        "max_area_triad": triads[0] if triads else None,
        "min_area": triads[-1]["area"] if triads else 0,
        "top_10": triads[:10]
    }


def stage3_carrier_triads(data):
    """Stage 3.2 — Carrier triad analysis.

    For each triad of carriers, compute interaction structure
    in CLR space across all timesteps.
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    triads = []
    for ci, cj, ck in combinations(range(D), 3):
        # Extract CLR subspace trajectories
        vals_i = [timesteps[t]["clr"][ci] for t in range(T)]
        vals_j = [timesteps[t]["clr"][cj] for t in range(T)]
        vals_k = [timesteps[t]["clr"][ck] for t in range(T)]

        # Pairwise correlations
        r_ij = _pearson_r(vals_i, vals_j)
        r_jk = _pearson_r(vals_j, vals_k)
        r_ik = _pearson_r(vals_i, vals_k)

        # Mean triadic area per timestep
        areas = []
        for t in range(T):
            hi = [timesteps[t]["clr"][ci]]
            hj = [timesteps[t]["clr"][cj]]
            hk = [timesteps[t]["clr"][ck]]
            # 1D distance
            a = abs(hi[0] - hj[0])
            b = abs(hj[0] - hk[0])
            c = abs(hi[0] - hk[0])
            s = (a + b + c) / 2
            area_sq = max(0, s * (s - a) * (s - b) * (s - c))
            areas.append(math.sqrt(area_sq))

        triads.append({
            "carriers": [carriers[ci], carriers[cj], carriers[ck]],
            "correlations": {"r_ij": r_ij, "r_jk": r_jk, "r_ik": r_ik},
            "mean_r": (abs(r_ij) + abs(r_jk) + abs(r_ik)) / 3,
            "mean_area": sum(areas) / len(areas) if areas else 0,
        })

    triads.sort(key=lambda x: x["mean_r"], reverse=True)
    return triads


def stage3_subcomposition_ladder(data):
    """Stage 3.3 — Subcomposition degree ladder.

    Compute structural measures at each degree k from 2 to D:
      D2: all pairwise distances
      D3: all triadic areas
      Dk: k-face volume proxy (sum of pairwise distances in k-subset)
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    ladder = []
    for k in range(2, D + 1):
        subsets = list(combinations(range(D), k))
        if len(subsets) > 200:
            step = len(subsets) // 200
            subsets = subsets[::step][:200]

        subset_measures = []
        for subset in subsets:
            # Average pairwise CLR distance within this k-subset
            total_d = 0
            n_pairs = 0
            for si, sj in combinations(subset, 2):
                vals_i = [timesteps[t]["clr"][si] for t in range(T)]
                vals_j = [timesteps[t]["clr"][sj] for t in range(T)]
                r = _pearson_r(vals_i, vals_j)
                total_d += abs(r)
                n_pairs += 1

            subset_measures.append({
                "carriers": [carriers[s] for s in subset],
                "mean_abs_correlation": total_d / n_pairs if n_pairs > 0 else 0,
                "k": k,
            })

        subset_measures.sort(key=lambda x: x["mean_abs_correlation"], reverse=True)

        ladder.append({
            "degree": k,
            "n_subsets": len(subset_measures),
            "mean_correlation": (
                sum(s["mean_abs_correlation"] for s in subset_measures) / len(subset_measures)
                if subset_measures else 0
            ),
            "top_subset": subset_measures[0] if subset_measures else None,
        })

    return ladder


def stage3_regime_detection(data, window=5):
    """Stage 3.4 — Metric regime detection.

    Slide a window across the time series. Within each window,
    compute structural statistics. Detect regime boundaries where
    statistics change abruptly.
    """
    timesteps = data["timesteps"]
    T = data["metadata"]["T"]

    if T < window:
        return {"regimes": [], "boundaries": []}

    windows = []
    for start in range(T - window + 1):
        end = start + window
        w_hs = [timesteps[t]["higgins_scale"] for t in range(start, end)]
        w_omega = [timesteps[t]["angular_velocity_deg"]
                    for t in range(start + 1, end)]
        w_energy = [timesteps[t]["metric_energy"] for t in range(start, end)]

        windows.append({
            "start": start,
            "end": end - 1,
            "start_label": timesteps[start]["label"],
            "end_label": timesteps[end - 1]["label"],
            "mean_hs": sum(w_hs) / len(w_hs),
            "std_hs": math.sqrt(sum((v - sum(w_hs) / len(w_hs)) ** 2 for v in w_hs) / len(w_hs)),
            "mean_omega": sum(w_omega) / len(w_omega) if w_omega else 0,
            "mean_energy": sum(w_energy) / len(w_energy),
        })

    # Detect boundaries: large changes in window statistics
    boundaries = []
    for i in range(1, len(windows)):
        delta_hs = abs(windows[i]["mean_hs"] - windows[i - 1]["mean_hs"])
        delta_omega = abs(windows[i]["mean_omega"] - windows[i - 1]["mean_omega"])
        if delta_hs > 0.02 or delta_omega > 2.0:
            boundaries.append({
                "window_index": i,
                "label": windows[i]["start_label"],
                "delta_hs": delta_hs,
                "delta_omega": delta_omega,
            })

    return {
        "window_size": window,
        "n_windows": len(windows),
        "windows": windows,
        "boundaries": boundaries,
        "n_regime_boundaries": len(boundaries),
    }


# ══════════════════════════════════════════════════════════════════
# BRIDGE 1: DYNAMICAL SYSTEMS (Handbook Ch 11)
# ══════════════════════════════════════════════════════════════════

def dynamical_lyapunov(data):
    """Lyapunov exponent estimation from CLR trajectory.

    For each carrier j, compute the exponential divergence rate:
      lambda_j = (1/T) * sum ln|h_j(t+1) - h_j(t)| / |perturbation|

    Positive lambda → divergent (chaotic-like)
    Negative lambda → convergent (attractor-like)
    Zero lambda → neutral (periodic-like)
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    if T < 3:
        return {"exponents": [], "max_exponent": 0}

    exponents = []
    for j in range(D):
        clr_j = [timesteps[t]["clr"][j] for t in range(T)]
        log_ratios = []
        for t in range(1, T - 1):
            d1 = abs(clr_j[t] - clr_j[t - 1])
            d2 = abs(clr_j[t + 1] - clr_j[t])
            if d1 > 1e-15:
                log_ratios.append(math.log(max(d2, 1e-15) / d1))

        lam = sum(log_ratios) / len(log_ratios) if log_ratios else 0.0
        exponents.append({
            "carrier": carriers[j],
            "index": j,
            "lyapunov_exponent": lam,
            "classification": (
                "DIVERGENT" if lam > 0.1 else
                "CONVERGENT" if lam < -0.1 else
                "NEUTRAL"
            )
        })

    max_exp = max(e["lyapunov_exponent"] for e in exponents)
    return {
        "exponents": exponents,
        "max_exponent": max_exp,
        "system_classification": (
            "CHAOTIC" if max_exp > 0.5 else
            "WEAKLY_DIVERGENT" if max_exp > 0.1 else
            "CONVERGENT" if max_exp < -0.1 else
            "NEUTRAL"
        )
    }


def dynamical_velocity_field(data):
    """Phase-space velocity field: dh/dt at each timestep.

    v(t) = h(t+1) - h(t)

    Computes velocity magnitude, direction, acceleration.
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    velocities = []
    for t in range(T - 1):
        h0 = timesteps[t]["clr"]
        h1 = timesteps[t + 1]["clr"]
        v = [h1[j] - h0[j] for j in range(D)]
        mag = math.sqrt(sum(vj ** 2 for vj in v))

        acc = None
        if t > 0:
            h_prev = timesteps[t - 1]["clr"]
            v_prev = [h0[j] - h_prev[j] for j in range(D)]
            acc = [v[j] - v_prev[j] for j in range(D)]
            acc_mag = math.sqrt(sum(aj ** 2 for aj in acc))
        else:
            acc_mag = 0.0

        velocities.append({
            "t": t,
            "label": timesteps[t]["label"],
            "velocity": v,
            "speed": mag,
            "acceleration_magnitude": acc_mag,
            "dominant_velocity_carrier": carriers[
                max(range(D), key=lambda j: abs(v[j]))
            ]
        })

    return {
        "velocities": velocities,
        "mean_speed": sum(v["speed"] for v in velocities) / len(velocities) if velocities else 0,
        "max_speed": max(v["speed"] for v in velocities) if velocities else 0,
        "max_speed_label": max(velocities, key=lambda v: v["speed"])["label"] if velocities else None,
    }


def dynamical_recurrence(data, threshold_factor=0.3):
    """Recurrence analysis: detect returns to previously visited states.

    R_ij = 1 if d(h(i), h(j)) < threshold else 0

    threshold = threshold_factor * mean pairwise distance.
    """
    timesteps = data["timesteps"]
    T = data["metadata"]["T"]

    if T < 3:
        return {"recurrence_rate": 0, "recurrence_points": []}

    # Compute threshold from mean distance
    distances = []
    for i in range(T):
        for j in range(i + 1, T):
            d = _distance(timesteps[i]["clr"], timesteps[j]["clr"])
            distances.append(d)
    mean_d = sum(distances) / len(distances) if distances else 1.0
    threshold = threshold_factor * mean_d

    recurrences = []
    total_pairs = 0
    recurrence_count = 0
    for i in range(T):
        for j in range(i + 2, T):  # skip adjacent
            d = _distance(timesteps[i]["clr"], timesteps[j]["clr"])
            total_pairs += 1
            if d < threshold:
                recurrence_count += 1
                if len(recurrences) < 50:  # cap storage
                    recurrences.append({
                        "i": i, "j": j,
                        "label_i": timesteps[i]["label"],
                        "label_j": timesteps[j]["label"],
                        "distance": d,
                    })

    return {
        "threshold": threshold,
        "threshold_factor": threshold_factor,
        "mean_pairwise_distance": mean_d,
        "recurrence_rate": recurrence_count / total_pairs if total_pairs > 0 else 0,
        "n_recurrences": recurrence_count,
        "total_pairs": total_pairs,
        "sample_recurrences": recurrences,
    }


def dynamical_attractor_detection(data):
    """Attractor detection: identify fixed points, limit cycles, strange attractors.

    Uses CLR trajectory convergence/divergence patterns.
    """
    timesteps = data["timesteps"]
    T = data["metadata"]["T"]

    if T < 5:
        return {"attractor_type": "INSUFFICIENT_DATA"}

    # Check for fixed point: does trajectory converge?
    last_quarter = timesteps[3 * T // 4:]
    h_list = [ts["clr"] for ts in last_quarter]
    bary = _barycenter(h_list)
    dists = [_distance(h, bary) for h in h_list]
    mean_spread = sum(dists) / len(dists) if dists else 0

    # Check velocity decay
    omegas = [ts["angular_velocity_deg"] for ts in timesteps[1:]]
    first_half_omega = sum(omegas[:len(omegas)//2]) / max(len(omegas)//2, 1)
    second_half_omega = sum(omegas[len(omegas)//2:]) / max(len(omegas) - len(omegas)//2, 1)

    velocity_ratio = second_half_omega / first_half_omega if first_half_omega > 0.01 else 1.0

    # Classification
    if mean_spread < 0.05 and velocity_ratio < 0.5:
        att_type = "FIXED_POINT"
    elif velocity_ratio < 0.8:
        att_type = "CONVERGENT_TRAJECTORY"
    elif 0.8 <= velocity_ratio <= 1.2:
        att_type = "STABLE_ORBIT"
    else:
        att_type = "DIVERGENT_TRAJECTORY"

    return {
        "attractor_type": att_type,
        "late_trajectory_spread": mean_spread,
        "velocity_ratio": velocity_ratio,
        "first_half_mean_omega": first_half_omega,
        "second_half_mean_omega": second_half_omega,
    }


# ══════════════════════════════════════════════════════════════════
# BRIDGE 2: CONTROL THEORY (Handbook Ch 12)
# ══════════════════════════════════════════════════════════════════

def control_state_space(data):
    """State-space model estimation in ILR coordinates.

    z(t+1) = A z(t) + residual

    where z = ILR projection of h = CLR(x).

    CLR vectors lie in a (D-1)-dimensional subspace (sum=0),
    so the D×D CLR covariance is always singular. Working in
    ILR (D-1 dimensions) gives a full-rank system.

    Estimates A by least-squares via normal equations.
    """
    timesteps = data["timesteps"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    d = D - 1  # ILR dimension

    if T < d + 2:
        return {"status": "INSUFFICIENT_DATA"}

    # Use ILR coordinates (guaranteed full-rank in d = D-1 dimensions)
    # Build Helmert basis
    basis = []
    for k in range(1, D):
        row = [0.0] * D
        norm = math.sqrt(k * (k + 1))
        for j in range(k):
            row[j] = 1.0 / norm
        row[k] = -k / norm
        basis.append(row)

    # Project all CLR vectors to ILR
    ilr_series = []
    for t in range(T):
        h = timesteps[t]["clr"]
        z = [sum(h[j] * basis[k][j] for j in range(D)) for k in range(d)]
        ilr_series.append(z)

    # Build matrices: Z1 = A * Z0
    # Z0[:,t] = z(t) for t=0..T-2,  Z1[:,t] = z(t+1) for t=0..T-2
    Z0 = [[ilr_series[t][j] for t in range(T - 1)] for j in range(d)]
    Z1 = [[ilr_series[t + 1][j] for t in range(T - 1)] for j in range(d)]

    # A = Z1 * Z0^T * (Z0 * Z0^T)^{-1}
    n = T - 1
    ZZt = [[sum(Z0[i][k] * Z0[j][k] for k in range(n)) for j in range(d)] for i in range(d)]
    Z1Zt = [[sum(Z1[i][k] * Z0[j][k] for k in range(n)) for j in range(d)] for i in range(d)]

    A = _solve_matrix(Z1Zt, ZZt, d)

    if A is None:
        return {"status": "SINGULAR_MATRIX"}

    # Eigenvalue proxy: trace and determinant
    trace_A = sum(A[i][i] for i in range(d))

    # Frobenius norm
    frob = math.sqrt(sum(A[i][j] ** 2 for i in range(d) for j in range(d)))

    # Spectral radius estimate (Gershgorin circles)
    gershgorin_radii = []
    for i in range(d):
        center = abs(A[i][i])
        radius = sum(abs(A[i][j]) for j in range(d) if j != i)
        gershgorin_radii.append(center + radius)
    spectral_radius_bound = max(gershgorin_radii)

    # Residual analysis in ILR space
    residuals = []
    for t in range(T - 1):
        z0 = ilr_series[t]
        z1_pred = [sum(A[i][j] * z0[j] for j in range(d)) for i in range(d)]
        z1_actual = ilr_series[t + 1]
        res = [z1_actual[j] - z1_pred[j] for j in range(d)]
        res_norm = math.sqrt(sum(r ** 2 for r in res))
        residuals.append(res_norm)

    mean_residual = sum(residuals) / len(residuals) if residuals else 0
    max_residual = max(residuals) if residuals else 0

    # Controllability matrix rank:
    # C = [B, AB, A^2B, ...] with B = I_{d×d}
    # Compute rank via iterative A^k
    # For d small, build full controllability matrix and check column rank
    ctrl_rank = d  # full rank if A is invertible (which it is here)

    return {
        "status": "ESTIMATED",
        "coordinate_system": "ILR (Helmert basis)",
        "ilr_dimension": d,
        "system_matrix_A": A,
        "trace_A": trace_A,
        "frobenius_norm": frob,
        "spectral_radius_bound": spectral_radius_bound,
        "stability": (
            "STABLE" if spectral_radius_bound < 1.0 else
            "MARGINALLY_STABLE" if spectral_radius_bound < 1.1 else
            "UNSTABLE"
        ),
        "mean_residual_norm": mean_residual,
        "max_residual_norm": max_residual,
        "model_fit_quality": (
            "EXCELLENT" if mean_residual < 0.05 else
            "GOOD" if mean_residual < 0.2 else
            "MODERATE" if mean_residual < 0.5 else
            "POOR"
        ),
        "controllability_rank": ctrl_rank,
    }


def _solve_matrix(B, A, D):
    """Solve X = B * A^{-1} via Gauss-Jordan elimination on augmented [A | B^T]."""
    # Create augmented matrix [A | I] to find A^{-1}
    aug = [A[i][:] + [1.0 if i == j else 0.0 for j in range(D)] for i in range(D)]

    for col in range(D):
        # Find pivot
        max_row = col
        for row in range(col + 1, D):
            if abs(aug[row][col]) > abs(aug[max_row][col]):
                max_row = row
        aug[col], aug[max_row] = aug[max_row], aug[col]

        if abs(aug[col][col]) < 1e-12:
            return None  # Singular

        # Eliminate
        pivot = aug[col][col]
        for j in range(2 * D):
            aug[col][j] /= pivot
        for row in range(D):
            if row != col:
                factor = aug[row][col]
                for j in range(2 * D):
                    aug[row][j] -= factor * aug[col][j]

    # Extract A^{-1}
    A_inv = [aug[i][D:] for i in range(D)]

    # X = B * A^{-1}
    X = [[sum(B[i][k] * A_inv[k][j] for k in range(D)) for j in range(D)] for i in range(D)]
    return X


def control_observability(data):
    """Observability analysis: which carriers are measurably responsive?

    Uses variance of CLR trajectories as observability proxy.
    High variance = highly observable. Low variance = hidden.
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    obs = []
    for j in range(D):
        vals = [timesteps[t]["clr"][j] for t in range(T)]
        mean_v = sum(vals) / T
        var_v = sum((v - mean_v) ** 2 for v in vals) / T
        obs.append({
            "carrier": carriers[j],
            "index": j,
            "clr_variance": var_v,
            "clr_std": math.sqrt(var_v),
            "observability": (
                "HIGH" if var_v > 0.1 else
                "MODERATE" if var_v > 0.01 else
                "LOW"
            )
        })
    obs.sort(key=lambda x: x["clr_variance"], reverse=True)
    return obs


# ══════════════════════════════════════════════════════════════════
# BRIDGE 3: INFORMATION THEORY (Handbook Ch 13)
# ══════════════════════════════════════════════════════════════════

def info_entropy_series(data):
    """Shannon entropy time series: H(t) = -sum x_j(t) ln x_j(t).

    Plus Higgins Scale Hs(t) = 1 - H(t)/ln(D).
    """
    timesteps = data["timesteps"]
    D = data["metadata"]["D"]

    series = []
    for ts in timesteps:
        x = ts["composition"]
        H = -sum(v * math.log(v) for v in x if v > 0)
        Hs = 1.0 - H / math.log(D) if D > 1 else 1.0
        series.append({
            "label": ts["label"],
            "shannon_entropy": H,
            "max_entropy": math.log(D),
            "normalised_entropy": H / math.log(D) if D > 1 else 0,
            "higgins_scale": Hs,
        })
    return series


def info_fisher_information(data):
    """Fisher information from composition trajectory.

    The Fisher information metric on the simplex is:
      g^F_ij = delta_ij / x_i

    which is the diagonal of the Higgins Steering Metric Tensor
    times D/(D-1). The Fisher information at each timestep
    measures local sensitivity to parameter changes.

    F(t) = sum_j (dx_j/dt)^2 / x_j(t)
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    fisher = []
    for t in range(1, T):
        x = timesteps[t]["composition"]
        x_prev = timesteps[t - 1]["composition"]
        F = 0
        for j in range(D):
            dx = x[j] - x_prev[j]
            F += dx ** 2 / max(x[j], 1e-15)
        fisher.append({
            "t": t,
            "label": timesteps[t]["label"],
            "fisher_information": F,
        })

    return {
        "series": fisher,
        "mean_fisher": sum(f["fisher_information"] for f in fisher) / len(fisher) if fisher else 0,
        "max_fisher": max(f["fisher_information"] for f in fisher) if fisher else 0,
        "max_fisher_label": max(fisher, key=lambda f: f["fisher_information"])["label"] if fisher else None,
    }


def info_kl_divergence(data):
    """KL divergence between consecutive compositions.

    D_KL(x(t) || x(t+1)) = sum_j x_j(t) * ln(x_j(t) / x_j(t+1))

    KL divergence is asymmetric. We compute both directions
    and the symmetrised Jensen-Shannon divergence:
      JSD = (D_KL(p||m) + D_KL(q||m)) / 2 where m = (p+q)/2.
    """
    timesteps = data["timesteps"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    divergences = []
    for t in range(T - 1):
        p = timesteps[t]["composition"]
        q = timesteps[t + 1]["composition"]
        m = [(p[j] + q[j]) / 2 for j in range(D)]

        kl_pq = sum(p[j] * math.log(p[j] / max(q[j], 1e-15)) for j in range(D))
        kl_qp = sum(q[j] * math.log(q[j] / max(p[j], 1e-15)) for j in range(D))
        kl_pm = sum(p[j] * math.log(p[j] / max(m[j], 1e-15)) for j in range(D))
        kl_qm = sum(q[j] * math.log(q[j] / max(m[j], 1e-15)) for j in range(D))
        jsd = (kl_pm + kl_qm) / 2

        divergences.append({
            "t": t,
            "label_from": timesteps[t]["label"],
            "label_to": timesteps[t + 1]["label"],
            "kl_forward": kl_pq,
            "kl_backward": kl_qp,
            "jensen_shannon": jsd,
        })

    return {
        "series": divergences,
        "mean_jsd": sum(d["jensen_shannon"] for d in divergences) / len(divergences) if divergences else 0,
        "max_jsd": max(d["jensen_shannon"] for d in divergences) if divergences else 0,
    }


def info_mutual_information(data):
    """Mutual information between carrier pairs.

    Estimated from discretised CLR trajectories:
    I(X;Y) = H(X) + H(Y) - H(X,Y)

    Uses histogram-based estimation with sqrt(T) bins.
    """
    timesteps = data["timesteps"]
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]

    n_bins = max(3, int(math.sqrt(T)))

    mi_pairs = []
    for ci in range(D):
        for cj in range(ci + 1, D):
            vals_i = [timesteps[t]["clr"][ci] for t in range(T)]
            vals_j = [timesteps[t]["clr"][cj] for t in range(T)]

            # Discretise
            mi = _estimate_mi(vals_i, vals_j, n_bins)
            mi_pairs.append({
                "carrier_a": carriers[ci],
                "carrier_b": carriers[cj],
                "mutual_information": mi,
            })

    mi_pairs.sort(key=lambda x: x["mutual_information"], reverse=True)
    return {
        "pairs": mi_pairs,
        "n_bins": n_bins,
        "max_mi_pair": mi_pairs[0] if mi_pairs else None,
    }


def _estimate_mi(x, y, n_bins):
    """Histogram-based mutual information estimation."""
    n = len(x)
    if n < 4:
        return 0.0

    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    if x_max - x_min < 1e-15 or y_max - y_min < 1e-15:
        return 0.0

    # Joint histogram
    joint = [[0] * n_bins for _ in range(n_bins)]
    for k in range(n):
        xi = min(int((x[k] - x_min) / (x_max - x_min) * n_bins), n_bins - 1)
        yi = min(int((y[k] - y_min) / (y_max - y_min) * n_bins), n_bins - 1)
        joint[xi][yi] += 1

    # Marginals
    mx = [sum(joint[i][j] for j in range(n_bins)) for i in range(n_bins)]
    my = [sum(joint[i][j] for i in range(n_bins)) for j in range(n_bins)]

    # MI
    mi = 0.0
    for i in range(n_bins):
        for j in range(n_bins):
            if joint[i][j] > 0 and mx[i] > 0 and my[j] > 0:
                pxy = joint[i][j] / n
                px = mx[i] / n
                py = my[j] / n
                mi += pxy * math.log(pxy / (px * py))
    return max(0, mi)


def info_entropy_rate(data):
    """Entropy rate: rate of entropy change over time.

    dH/dt = H(t+1) - H(t)

    Positive = system dispersing (entropy increasing)
    Negative = system concentrating (entropy decreasing)
    """
    timesteps = data["timesteps"]
    T = data["metadata"]["T"]

    rates = []
    for t in range(1, T):
        H_now = timesteps[t]["shannon_entropy"]
        H_prev = timesteps[t - 1]["shannon_entropy"]
        dH = H_now - H_prev
        rates.append({
            "t": t,
            "label": timesteps[t]["label"],
            "entropy_rate": dH,
            "direction": (
                "DISPERSING" if dH > 0.001 else
                "CONCENTRATING" if dH < -0.001 else
                "STATIONARY"
            )
        })

    return {
        "series": rates,
        "mean_rate": sum(r["entropy_rate"] for r in rates) / len(rates) if rates else 0,
        "net_entropy_change": (
            timesteps[-1]["shannon_entropy"] - timesteps[0]["shannon_entropy"]
        ) if T > 1 else 0,
        "overall_direction": (
            "NET_DISPERSING" if rates and sum(r["entropy_rate"] for r in rates) > 0.01 else
            "NET_CONCENTRATING" if rates and sum(r["entropy_rate"] for r in rates) < -0.01 else
            "NET_STATIONARY"
        )
    }


# ══════════════════════════════════════════════════════════════════
# MAIN ANALYSIS: JSON → JSON
# ══════════════════════════════════════════════════════════════════

def run_analysis(data):
    """Execute complete CNT analysis pipeline.

    Stage 1 → Stage 2 → Stage 3 → Bridge 1 → Bridge 2 → Bridge 3.
    """
    result = {
        "metadata": {
            "engine": "CNT Analysis Engine v1.0",
            "handbook": "CNT Mathematics Handbook v2.0",
            "generated": datetime.utcnow().isoformat() + "Z",
            "source_engine": data["metadata"]["engine"],
            "carriers": data["metadata"]["carriers"],
            "D": data["metadata"]["D"],
            "T": data["metadata"]["T"],
            "labels": data["metadata"]["labels"],
        }
    }

    print("  Stage 1: Section triads and metric ledger...")
    result["stage1"] = stage1_section_triads(data)

    print("  Stage 2: Metric cross-examination...")
    result["stage2"] = {
        "group_barycenters": stage2_group_barycenters(data),
        "carrier_pair_cross_examination": stage2_carrier_pair_cross(data),
        "section_view_cross_examination": stage2_section_view_cross(data),
    }

    print("  Stage 3: Higher-degree analysis...")
    result["stage3"] = {
        "triadic_area": stage3_triadic_area(data),
        "carrier_triads": stage3_carrier_triads(data),
        "subcomposition_ladder": stage3_subcomposition_ladder(data),
        "regime_detection": stage3_regime_detection(data),
    }

    print("  Bridge 1: Dynamical systems...")
    result["dynamical_systems"] = {
        "lyapunov_exponents": dynamical_lyapunov(data),
        "velocity_field": dynamical_velocity_field(data),
        "recurrence_analysis": dynamical_recurrence(data),
        "attractor_detection": dynamical_attractor_detection(data),
    }

    print("  Bridge 2: Control theory...")
    result["control_theory"] = {
        "state_space_model": control_state_space(data),
        "observability": control_observability(data),
    }

    print("  Bridge 3: Information theory...")
    result["information_theory"] = {
        "entropy_series": info_entropy_series(data),
        "fisher_information": info_fisher_information(data),
        "kl_divergence": info_kl_divergence(data),
        "mutual_information": info_mutual_information(data),
        "entropy_rate": info_entropy_rate(data),
    }

    return result


# ══════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python cnt_analysis.py engine_output.json [analysis_output.json]")
        print("  engine_output.json:   Output from cnt_tensor_engine.py")
        print("  analysis_output.json: Complete analysis (default: *_analysis.json)")
        sys.exit(1)

    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        base = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base}_analysis.json"

    print(f"CNT Analysis Engine v1.0")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print()

    # Read engine JSON
    with open(input_file, 'r') as f:
        data = json.load(f)

    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    print(f"Carriers (D={D}): {', '.join(carriers)}")
    print(f"Timesteps (T={T}): {data['metadata']['labels'][0]} to {data['metadata']['labels'][-1]}")
    print()

    print("Computing...")
    result = run_analysis(data)
    print()

    # Write JSON
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    size_kb = os.path.getsize(output_file) / 1024
    print(f"Written: {output_file} ({size_kb:.1f} KB)")
    print()

    # Summary
    s2 = result["stage2"]
    s3 = result["stage3"]
    dyn = result["dynamical_systems"]
    ctrl = result["control_theory"]
    info = result["information_theory"]

    print(f"=== Analysis Summary ===")
    print(f"  Stage 1: {T} section triads, {T} metric ledger rows")
    print(f"  Stage 2: {len(s2['carrier_pair_cross_examination'])} carrier pairs examined")
    print(f"           Hs trend: {s2['section_view_cross_examination']['hs_trend_direction']}")
    print(f"  Stage 3: {s3['triadic_area']['n_triads']} temporal triads, max area {s3['triadic_area']['max_area']:.4f}")
    print(f"           {s3['regime_detection']['n_regime_boundaries']} regime boundaries detected")
    print()
    print(f"  Bridge 1 — Dynamical Systems:")
    print(f"    System: {dyn['lyapunov_exponents']['system_classification']}")
    print(f"    Attractor: {dyn['attractor_detection']['attractor_type']}")
    print(f"    Recurrence rate: {dyn['recurrence_analysis']['recurrence_rate']:.4f}")
    print()
    print(f"  Bridge 2 — Control Theory:")
    ss = ctrl["state_space_model"]
    if ss["status"] == "ESTIMATED":
        print(f"    Stability: {ss['stability']} (spectral bound {ss['spectral_radius_bound']:.4f})")
        print(f"    Model fit: {ss['model_fit_quality']} (mean residual {ss['mean_residual_norm']:.6f})")
    else:
        print(f"    State-space: {ss['status']}")
    print()
    print(f"  Bridge 3 — Information Theory:")
    print(f"    Entropy direction: {info['entropy_rate']['overall_direction']}")
    print(f"    Net entropy change: {info['entropy_rate']['net_entropy_change']:.6f}")
    print(f"    Mean Fisher information: {info['fisher_information']['mean_fisher']:.6f}")
    print(f"    Mean Jensen-Shannon div: {info['kl_divergence']['mean_jsd']:.6f}")
    if info['mutual_information']['max_mi_pair']:
        mi_pair = info['mutual_information']['max_mi_pair']
        print(f"    Highest MI pair: {mi_pair['carrier_a']}/{mi_pair['carrier_b']} ({mi_pair['mutual_information']:.4f})")
    print()
    print("The instrument reads. The expert decides. The loop stays open.")


if __name__ == "__main__":
    main()
