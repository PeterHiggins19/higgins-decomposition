#!/usr/bin/env python3
"""
CNT Recursive Depth Sounder
=============================

Program 4 of the CNT standard pipeline.

Takes CNT tensor JSON output and iterates the tensor through itself:
at each level, derived compositions are constructed from the tensor
channels, fed back through the CNT math, and the information content
is measured. The process continues until the signal goes flat.

Three derived composition types are computed at each level:
  1. ENERGY composition:  e_j(t) = (Δh_j)² / Σ(Δh_k)²
     Kinetic energy distribution across carriers.
  2. CURVATURE composition:  c_j(t) = κ_jj(t) / Σ κ_kk(t)
     Steering sensitivity distribution (metric diagonal).
  3. SPECTRAL composition:  s_j(t) = P_j / Σ P_k
     Total FFT power per carrier channel.

Each derived composition is a valid element of S^D and can be
processed by the full CNT tensor math (CLR, bearing, velocity,
metric, helmsman). The iteration terminates when the angular
velocity variance drops below the noise floor.

The recursion depth — the number of productive levels before
exhaustion — is itself a diagnostic: the DYNAMICAL DEPTH of
the compositional system.

Mathematical structure:
  Level 0:  x(t) → CNT₀
  Level 1:  f(CNT₀) → CNT₁    (dynamics of dynamics)
  Level 2:  f(CNT₁) → CNT₂    (dynamics of dynamics of dynamics)
  Level k:  f(CNTₖ₋₁) → CNTₖ  (k-th order derivative structure)

This is the jet bundle J^k on the simplex: each level adds one
order of differential structure. The tower terminates naturally
when the signal is exhausted.

Key discovery: The metric composition map M(x)_j = (1/x_j)/Σ(1/x_k)
satisfies M² = Identity (involution). In CLR space: clr(M(x)) = -clr(x).
The metric dual is the antipodal reflection through the barycenter.
The only fixed point is x* = (1/D, ..., 1/D).

Usage:
  python cnt_depth_sounder.py engine_output.json [output.json]

The instrument reads. The expert decides. The loop stays open.
"""

import json
import math
import sys
import os
from datetime import datetime

import numpy as np


# ══════════════════════════════════════════════════════════════════
# CORE CNT MATH (from cnt_tensor_engine.py)
# ══════════════════════════════════════════════════════════════════

def closure(x, eps=1e-15):
    x_pos = [max(float(v), eps) for v in x]
    total = sum(x_pos)
    return [v / total for v in x_pos]


def clr_transform(x):
    D = len(x)
    log_x = [math.log(v) for v in x]
    mean_log = sum(log_x) / D
    return [lx - mean_log for lx in log_x]


def helmert_basis(D):
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
    return [sum(h[j] * basis[k][j] for j in range(len(h)))
            for k in range(len(basis))]


def bearing_pairwise(h, i, j):
    return math.degrees(math.atan2(h[j], h[i]))


def angular_velocity(h1, h2):
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


def metric_tensor_diag(x, eps=1e-15):
    """Diagonal of the Higgins Steering Metric Tensor: κ_jj = (1 - 1/D) / x_j²."""
    x = closure(x, eps=eps)
    D = len(x)
    return [(1.0 - 1.0 / D) / (x[j] ** 2) for j in range(D)]


def higgins_scale(x):
    D = len(x)
    if D < 2:
        return 1.0
    H = -sum(v * math.log(v) for v in x if v > 0)
    return 1.0 - H / math.log(D)


def aitchison_norm(x, eps=1e-15):
    h = clr_transform(closure(x, eps))
    return math.sqrt(sum(v ** 2 for v in h))


def helmsman_index(h1, h2):
    deltas = [abs(h2[j] - h1[j]) for j in range(len(h1))]
    return max(range(len(deltas)), key=lambda j: deltas[j])


# ══════════════════════════════════════════════════════════════════
# DERIVED COMPOSITION CONSTRUCTORS
# ══════════════════════════════════════════════════════════════════

def energy_composition(clr_series):
    """Kinetic energy composition: e_j(t) = (Δh_j)² / Σ(Δh_k)².

    Distribution of CLR displacement energy across carriers at each step.
    Returns T-1 compositions.
    """
    T = len(clr_series)
    D = len(clr_series[0])
    compositions = []
    for t in range(T - 1):
        delta_sq = [(clr_series[t + 1][j] - clr_series[t][j]) ** 2
                     for j in range(D)]
        total = sum(delta_sq)
        if total < 1e-30:
            compositions.append([1.0 / D] * D)
        else:
            compositions.append([d / total for d in delta_sq])
    return compositions


def curvature_composition(comp_series):
    """Curvature composition: c_j(t) = κ_jj(t) / Σ κ_kk(t).

    Distribution of steering sensitivity across carriers.
    """
    compositions = []
    for x in comp_series:
        kappa = metric_tensor_diag(x)
        total = sum(kappa)
        if total < 1e-30:
            compositions.append([1.0 / len(x)] * len(x))
        else:
            compositions.append([k / total for k in kappa])
    return compositions


def spectral_composition(clr_series):
    """Spectral power composition: s_j = P_j / Σ P_k.

    Total FFT power per carrier, normalized to simplex.
    Single composition summarizing the entire signal.
    """
    D = len(clr_series[0])
    powers = []
    for j in range(D):
        signal = np.array([clr_series[t][j] for t in range(len(clr_series))])
        signal = signal - np.mean(signal)
        spectrum = np.fft.rfft(signal * np.hanning(len(signal)))
        powers.append(float(np.sum(np.abs(spectrum) ** 2)))
    total = sum(powers)
    if total < 1e-30:
        return [1.0 / D] * D
    return [p / total for p in powers]


# ══════════════════════════════════════════════════════════════════
# LEVEL COMPUTATION — full CNT at one recursion level
# ══════════════════════════════════════════════════════════════════

def compute_level(compositions, level_name, carrier_names):
    """Run full CNT tensor math on a time series of compositions.

    Returns a level report dict with all tensor channels and diagnostics.
    """
    T = len(compositions)
    D = len(compositions[0])

    # Close all compositions
    closed = [closure(x) for x in compositions]

    # CLR transform
    clr_series = [clr_transform(x) for x in closed]

    # Helmert basis for ILR
    basis = helmert_basis(D)
    ilr_series = [ilr_project(h, basis) for h in clr_series]

    # Higgins Scale series
    hs_series = [higgins_scale(x) for x in closed]

    # Aitchison norm series (distance from barycenter)
    norm_series = [aitchison_norm(x) for x in closed]

    # Angular velocity series
    omega_series = []
    for t in range(T - 1):
        omega_series.append(angular_velocity(clr_series[t], clr_series[t + 1]))

    # Helmsman series
    helmsman_series = []
    helmsman_freq = {}
    for t in range(T - 1):
        idx = helmsman_index(clr_series[t], clr_series[t + 1])
        name = carrier_names[idx] if idx < len(carrier_names) else f"C{idx}"
        helmsman_series.append(name)
        helmsman_freq[name] = helmsman_freq.get(name, 0) + 1

    # Metric tensor trace and condition number
    trace_series = []
    cond_series = []
    asymmetry_series = []
    for x in closed:
        kappa = metric_tensor_diag(x)
        trace_series.append(sum(kappa))
        max_k = max(kappa)
        min_k = min(kappa)
        cond_series.append(max_k / min_k if min_k > 0 else float('inf'))
        asymmetry_series.append(max_k / min_k if min_k > 0 else float('inf'))

    # Pairwise bearing spread (variance of bearings)
    bearing_spreads = []
    for t in range(T):
        bearings = []
        for i in range(D):
            for j in range(i + 1, D):
                bearings.append(bearing_pairwise(clr_series[t], i, j))
        if bearings:
            mean_b = sum(bearings) / len(bearings)
            var_b = sum((b - mean_b) ** 2 for b in bearings) / len(bearings)
            bearing_spreads.append(math.sqrt(var_b))
        else:
            bearing_spreads.append(0.0)

    # Information content metrics
    omega_mean = np.mean(omega_series) if omega_series else 0.0
    omega_var = np.var(omega_series) if omega_series else 0.0
    omega_max = max(omega_series) if omega_series else 0.0
    hs_mean = np.mean(hs_series)
    hs_var = np.var(hs_series)
    hs_range = max(hs_series) - min(hs_series)
    norm_mean = np.mean(norm_series)
    bearing_spread_mean = np.mean(bearing_spreads)

    # Spectral composition at this level
    spectral_comp = spectral_composition(clr_series)

    # Dominant helmsman
    dominant = max(helmsman_freq, key=helmsman_freq.get) if helmsman_freq else "N/A"
    dominant_pct = helmsman_freq.get(dominant, 0) / max(len(helmsman_series), 1) * 100

    return {
        "level_name": level_name,
        "T": T,
        "D": D,
        "carrier_names": carrier_names,
        "hs": {
            "mean": hs_mean,
            "variance": hs_var,
            "range": hs_range,
            "min": min(hs_series),
            "max": max(hs_series),
            "series": hs_series
        },
        "omega": {
            "mean": omega_mean,
            "variance": omega_var,
            "max": omega_max,
            "series": omega_series
        },
        "aitchison_norm": {
            "mean": norm_mean,
            "series": norm_series
        },
        "metric": {
            "trace_mean": np.mean(trace_series),
            "cond_mean": np.mean(cond_series),
            "asymmetry_mean": np.mean(asymmetry_series)
        },
        "bearing_spread": {
            "mean": bearing_spread_mean,
            "series": bearing_spreads
        },
        "helmsman": {
            "dominant": dominant,
            "dominant_pct": dominant_pct,
            "frequency": helmsman_freq
        },
        "spectral_composition": spectral_comp,
        "clr_series": clr_series,
        "compositions": [list(x) for x in closed]
    }


# ══════════════════════════════════════════════════════════════════
# FLATNESS DETECTION — when to stop
# ══════════════════════════════════════════════════════════════════

NOISE_FLOOR_OMEGA_VAR = 1e-6   # Angular velocity variance threshold
MIN_TIMESTEPS = 5               # Minimum useful signal length
MAX_LEVELS = 50                 # Safety bound
CONVERGENCE_PCT = 0.01          # 1% precision target for limit cycle detection


def is_flat(level_report):
    """Determine if a level has exhausted its information content.

    A level is flat when:
      1. Angular velocity variance < noise floor (no meaningful direction changes)
      2. Hs variance ≈ 0 (no entropy variation)
      3. Signal too short (< MIN_TIMESTEPS)
    """
    if level_report["T"] < MIN_TIMESTEPS:
        return True, "SIGNAL_EXHAUSTED"
    if level_report["omega"]["variance"] < NOISE_FLOOR_OMEGA_VAR:
        return True, "OMEGA_FLAT"
    if level_report["hs"]["variance"] < 1e-10:
        return True, "HS_FLAT"
    return False, "PRODUCTIVE"


def detect_limit_cycle(hs_trajectory, precision=CONVERGENCE_PCT):
    """Detect period-N limit cycle in Hs trajectory.

    Checks for period-1 (convergence) and period-2 (oscillation)
    within the specified precision target.

    Returns:
      (detected, period, residual, converged_at_level)
    """
    n = len(hs_trajectory)
    if n < 4:
        return False, 0, 1.0, n

    # Period-1: consecutive values within tolerance
    for k in range(2, n):
        if abs(hs_trajectory[k] - hs_trajectory[k-1]) / max(abs(hs_trajectory[k-1]), 1e-15) < precision:
            return True, 1, abs(hs_trajectory[k] - hs_trajectory[k-1]), k

    # Period-2: same-parity values within tolerance (even-even, odd-odd)
    for k in range(4, n):
        residual_even = abs(hs_trajectory[k] - hs_trajectory[k-2]) / max(abs(hs_trajectory[k-2]), 1e-15)
        if residual_even < precision:
            # Verify the other parity also converged
            if k >= 5:
                residual_odd = abs(hs_trajectory[k-1] - hs_trajectory[k-3]) / max(abs(hs_trajectory[k-3]), 1e-15)
                if residual_odd < precision:
                    return True, 2, max(residual_even, residual_odd), k
            else:
                return True, 2, residual_even, k

    return False, 0, 1.0, n


# ══════════════════════════════════════════════════════════════════
# METRIC DUAL VERIFICATION (M² = I proof)
# ══════════════════════════════════════════════════════════════════

def metric_dual(x, eps=1e-15):
    """Metric dual composition: M(x)_j = (1/x_j) / Σ(1/x_k).

    Property: M(M(x)) = x (involution, M² = Identity).
    Property: clr(M(x)) = -clr(x) (CLR negation).
    Fixed point: x* = (1/D, ..., 1/D) (barycenter).
    """
    x = closure(x, eps)
    inv = [1.0 / v for v in x]
    total = sum(inv)
    return [v / total for v in inv]


def verify_involution(x, eps=1e-15):
    """Verify M² = I for a given composition."""
    m = metric_dual(x, eps)
    mm = metric_dual(m, eps)
    x_c = closure(x, eps)
    residual = math.sqrt(sum((a - b) ** 2 for a, b in zip(x_c, mm)))
    return {
        "x": x_c,
        "M(x)": m,
        "M(M(x))": mm,
        "residual_norm": residual,
        "involution_verified": residual < 1e-10,
        "clr_x": clr_transform(x_c),
        "clr_Mx": clr_transform(m),
        "clr_sum_norm": math.sqrt(sum((a + b) ** 2
                        for a, b in zip(clr_transform(x_c), clr_transform(m)))),
        "duality_distance": 2.0 * aitchison_norm(x_c)
    }


# ══════════════════════════════════════════════════════════════════
# MAIN RECURSION ENGINE
# ══════════════════════════════════════════════════════════════════

def run_depth_sounder(data):
    """Execute the full recursive depth sounding.

    Takes CNT engine JSON, constructs derived compositions at each level,
    iterates until flat.

    Returns the complete sounding report.
    """
    carriers = data["metadata"]["carriers"]
    D = data["metadata"]["D"]
    T = data["metadata"]["T"]
    ts_data = data["timesteps"]

    # Extract Level 0 compositions and CLR
    compositions_L0 = [ts_data[t]["composition"] for t in range(T)]
    clr_L0 = [ts_data[t]["clr"] for t in range(T)]

    print(f"\n{'='*60}")
    print(f"CNT RECURSIVE DEPTH SOUNDER")
    print(f"{'='*60}")
    print(f"Input: D={D}, T={T}, carriers={carriers}")
    print()

    # ── Metric Dual Verification ──
    print("── Metric Dual Involution Proof ──")
    sample_x = compositions_L0[T // 2]  # mid-series sample
    inv_proof = verify_involution(sample_x)
    print(f"  Sample composition (t={T//2}): {[f'{v:.6f}' for v in inv_proof['x']]}")
    print(f"  M(x):                          {[f'{v:.6f}' for v in inv_proof['M(x)']]}")
    print(f"  M(M(x)):                       {[f'{v:.6f}' for v in inv_proof['M(M(x))']]}")
    print(f"  ||M²(x) - x|| = {inv_proof['residual_norm']:.2e}  {'✓ INVOLUTION VERIFIED' if inv_proof['involution_verified'] else '✗ FAILED'}")
    print(f"  ||clr(x) + clr(M(x))|| = {inv_proof['clr_sum_norm']:.2e}  (should be ~0)")
    print(f"  Duality distance d_A(x, M(x)) = {inv_proof['duality_distance']:.4f} HLR")
    print()

    # ── Level 0: Original data ──
    print("── Level 0: ORIGINAL COMPOSITION ──")
    level0 = compute_level(compositions_L0, "L0_original", carriers)
    flat0, reason0 = is_flat(level0)
    print(f"  T={level0['T']}, D={level0['D']}")
    print(f"  Hs: {level0['hs']['mean']:.4f} ± {math.sqrt(level0['hs']['variance']):.4f}")
    print(f"  ω:  {level0['omega']['mean']:.4f} ± {math.sqrt(level0['omega']['variance']):.4f} deg/step")
    print(f"  Helmsman: {level0['helmsman']['dominant']} ({level0['helmsman']['dominant_pct']:.0f}%)")
    print(f"  Status: {reason0}")
    print()

    # Storage for all levels
    all_levels = [level0]
    tower = {
        "energy": [],
        "curvature": [],
        "spectral": []
    }

    def run_tower(tower_name, composition_fn, comp_input, clr_input, carrier_prefix):
        """Generic tower runner with limit cycle detection.

        composition_fn: function(input) → list of compositions
        comp_input: initial compositions or CLR for the composition_fn
        clr_input: initial CLR series (for energy tower which needs CLR)
        carrier_prefix: prefix for carrier names at each level
        """
        print(f"── {tower_name.upper()} TOWER ──")
        current_comp = comp_input
        current_clr = clr_input
        levels = []
        hs_trajectory = [level0["hs"]["mean"]]
        level_num = 1

        while level_num <= MAX_LEVELS:
            # Construct derived composition
            if tower_name == "energy":
                derived = composition_fn(current_clr)
            else:
                derived = composition_fn(current_comp)

            if len(derived) < MIN_TIMESTEPS:
                print(f"  Level {level_num}: T={len(derived)} — SIGNAL_EXHAUSTED")
                levels.append({"level": level_num, "T": len(derived),
                               "status": "SIGNAL_EXHAUSTED"})
                break

            cnames = [f"{carrier_prefix}_{c}" for c in carriers]
            lev = compute_level(derived, f"L{level_num}_{tower_name}", cnames)
            flat, reason = is_flat(lev)

            hs_trajectory.append(lev["hs"]["mean"])

            # Check for limit cycle convergence (1% precision)
            cycle_detected, cycle_period, cycle_residual, conv_level = \
                detect_limit_cycle(hs_trajectory, CONVERGENCE_PCT)

            if cycle_detected and level_num >= 4:
                reason = f"LIMIT_CYCLE_P{cycle_period}"
                flat = True

            print(f"  Level {level_num}: T={lev['T']}, "
                  f"Hs={lev['hs']['mean']:.4f}, "
                  f"ω={lev['omega']['mean']:.4f}±{math.sqrt(lev['omega']['variance']):.4f}, "
                  f"helmsman={lev['helmsman']['dominant']}, "
                  f"status={reason}")

            level_entry = {
                "level": level_num,
                "T": lev["T"],
                "hs_mean": lev["hs"]["mean"],
                "hs_var": lev["hs"]["variance"],
                "omega_mean": lev["omega"]["mean"],
                "omega_var": lev["omega"]["variance"],
                "omega_max": lev["omega"]["max"],
                "helmsman": lev["helmsman"]["dominant"],
                "helmsman_pct": lev["helmsman"]["dominant_pct"],
                "bearing_spread": lev["bearing_spread"]["mean"],
                "metric_trace": lev["metric"]["trace_mean"],
                "spectral_comp": lev["spectral_composition"],
                "status": reason
            }

            if cycle_detected:
                level_entry["cycle_period"] = cycle_period
                level_entry["cycle_residual"] = cycle_residual
                level_entry["converged_at_level"] = conv_level

            levels.append(level_entry)
            all_levels.append(lev)

            if flat:
                break
            current_comp = lev["compositions"]
            current_clr = lev["clr_series"]
            level_num += 1

        depth = level_num
        termination = reason

        # Compute residuals at termination
        residuals = {}
        if len(hs_trajectory) >= 3:
            residuals["final_hs_delta"] = abs(hs_trajectory[-1] - hs_trajectory[-2])
            if len(hs_trajectory) >= 4:
                residuals["final_hs_p2_delta"] = abs(hs_trajectory[-1] - hs_trajectory[-3])
                residuals["final_hs_p2_pct"] = residuals["final_hs_p2_delta"] / max(abs(hs_trajectory[-3]), 1e-15)

        # Limit cycle characterization
        cycle_info = detect_limit_cycle(hs_trajectory, CONVERGENCE_PCT)
        if cycle_info[0]:
            if cycle_info[1] == 2 and len(hs_trajectory) >= 4:
                residuals["attractor_even"] = hs_trajectory[-2]
                residuals["attractor_odd"] = hs_trajectory[-1]
                residuals["attractor_amplitude"] = abs(hs_trajectory[-1] - hs_trajectory[-2])
            elif cycle_info[1] == 1:
                residuals["attractor_fixed"] = hs_trajectory[-1]

        print(f"  → {tower_name.upper()} DEPTH: {depth} levels, termination: {termination}")
        if residuals:
            for k, v in residuals.items():
                print(f"     {k}: {v:.6f}" if isinstance(v, float) else f"     {k}: {v}")
        print()

        return {
            "levels": levels,
            "depth": depth,
            "termination": termination,
            "hs_trajectory": hs_trajectory,
            "residuals": residuals,
            "cycle_detected": cycle_info[0],
            "cycle_period": cycle_info[1],
            "cycle_residual": cycle_info[2],
            "convergence_level": cycle_info[3]
        }

    # ── Run all three towers ──
    energy_result = run_tower("energy", energy_composition,
                               compositions_L0, clr_L0, "E")
    tower["energy"] = energy_result["levels"]
    energy_depth = energy_result["depth"]

    curvature_result = run_tower("curvature", curvature_composition,
                                  compositions_L0, clr_L0, "K")
    tower["curvature"] = curvature_result["levels"]
    curvature_depth = curvature_result["depth"]

    # ── Cross-level analysis ──
    print("── CROSS-LEVEL ANALYSIS ──")

    # Use Hs trajectories from run_tower() results
    energy_hs_trajectory = energy_result["hs_trajectory"]
    curvature_hs_trajectory = curvature_result["hs_trajectory"]

    # Convergence rate: how fast does Hs change per level?
    if len(energy_hs_trajectory) > 1:
        hs_diffs = [abs(energy_hs_trajectory[i+1] - energy_hs_trajectory[i])
                    for i in range(len(energy_hs_trajectory)-1)]
        energy_convergence = np.mean(hs_diffs)
    else:
        energy_convergence = 0.0

    if len(curvature_hs_trajectory) > 1:
        hs_diffs = [abs(curvature_hs_trajectory[i+1] - curvature_hs_trajectory[i])
                    for i in range(len(curvature_hs_trajectory)-1)]
        curvature_convergence = np.mean(hs_diffs)
    else:
        curvature_convergence = 0.0

    # Metric dual verification on Level 0 compositions
    dual_distances = []
    for x in compositions_L0:
        dual_distances.append(2.0 * aitchison_norm(x))
    mean_dual_dist = np.mean(dual_distances)

    print(f"  Energy Hs trajectory:    {' → '.join(f'{v:.4f}' for v in energy_hs_trajectory)}")
    print(f"  Curvature Hs trajectory: {' → '.join(f'{v:.4f}' for v in curvature_hs_trajectory)}")
    print(f"  Energy convergence rate: {energy_convergence:.6f} Hs/level")
    print(f"  Curvature convergence:   {curvature_convergence:.6f} Hs/level")
    print(f"  Mean duality distance:   {mean_dual_dist:.4f} HLR")

    # Report cycle detection results
    if energy_result["cycle_detected"]:
        print(f"  Energy cycle: period-{energy_result['cycle_period']}, "
              f"residual={energy_result['cycle_residual']:.2e}, "
              f"converged at level {energy_result['convergence_level']}")
    if curvature_result["cycle_detected"]:
        print(f"  Curvature cycle: period-{curvature_result['cycle_period']}, "
              f"residual={curvature_result['cycle_residual']:.2e}, "
              f"converged at level {curvature_result['convergence_level']}")
    print()

    # ── Summary ──
    max_depth = max(energy_depth, curvature_depth)
    print(f"{'='*60}")
    print(f"DEPTH SOUNDING COMPLETE")
    print(f"{'='*60}")
    print(f"  Energy depth:    {energy_depth} levels")
    print(f"  Curvature depth: {curvature_depth} levels")
    print(f"  Maximum depth:   {max_depth} levels")
    print(f"  Dynamical depth: {max_depth}")
    print(f"  M² = I verified: {inv_proof['involution_verified']}")
    print()
    print(f"The instrument reads. The expert decides. The loop stays open.")

    # Build output report
    report = {
        "metadata": {
            "program": "CNT Recursive Depth Sounder v1.0",
            "generated": datetime.utcnow().isoformat() + "Z",
            "input_D": D,
            "input_T": T,
            "carriers": carriers
        },
        "involution_proof": {
            "sample_t": T // 2,
            "x": inv_proof["x"],
            "Mx": inv_proof["M(x)"],
            "MMx": inv_proof["M(M(x))"],
            "residual": inv_proof["residual_norm"],
            "verified": inv_proof["involution_verified"],
            "clr_negation_residual": inv_proof["clr_sum_norm"],
            "duality_distance": inv_proof["duality_distance"]
        },
        "level_0": {
            "T": level0["T"],
            "D": level0["D"],
            "hs_mean": level0["hs"]["mean"],
            "hs_var": level0["hs"]["variance"],
            "omega_mean": level0["omega"]["mean"],
            "omega_var": level0["omega"]["variance"],
            "helmsman": level0["helmsman"]["dominant"],
            "helmsman_pct": level0["helmsman"]["dominant_pct"]
        },
        "energy_tower": tower["energy"],
        "curvature_tower": tower["curvature"],
        "depth_summary": {
            "energy_depth": energy_depth,
            "curvature_depth": curvature_depth,
            "max_depth": max_depth,
            "energy_hs_trajectory": energy_hs_trajectory,
            "curvature_hs_trajectory": curvature_hs_trajectory,
            "energy_convergence_rate": energy_convergence,
            "curvature_convergence_rate": curvature_convergence,
            "energy_termination": energy_result["termination"],
            "curvature_termination": curvature_result["termination"],
            "energy_cycle": {
                "detected": energy_result["cycle_detected"],
                "period": energy_result["cycle_period"],
                "residual": energy_result["cycle_residual"],
                "convergence_level": energy_result["convergence_level"]
            },
            "curvature_cycle": {
                "detected": curvature_result["cycle_detected"],
                "period": curvature_result["cycle_period"],
                "residual": curvature_result["cycle_residual"],
                "convergence_level": curvature_result["convergence_level"]
            },
            "energy_residuals": energy_result["residuals"],
            "curvature_residuals": curvature_result["residuals"],
            "mean_duality_distance": mean_dual_dist,
            "convergence_precision": CONVERGENCE_PCT,
            "noise_floor_omega_var": NOISE_FLOOR_OMEGA_VAR,
            "min_timesteps": MIN_TIMESTEPS,
            "max_levels": MAX_LEVELS,
            "interpretation": (
                f"This system supports {max_depth} levels of recursive tensor analysis "
                f"before the signal exhausts. Energy tower reaches depth {energy_depth} "
                f"(termination: {energy_result['termination']}), "
                f"curvature tower reaches depth {curvature_depth} "
                f"(termination: {curvature_result['termination']}). "
                f"Convergence precision target: {CONVERGENCE_PCT*100:.0f}%. "
                f"The dynamical depth measures the system's compositional complexity: "
                f"how many orders of derivative structure contain non-trivial information."
            )
        }
    }

    return report


# ══════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python cnt_depth_sounder.py engine_output.json [output.json]")
        sys.exit(1)

    input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        base = os.path.splitext(os.path.basename(input_path))[0]
        output_path = base.replace("_cnt", "_depth") + "_depth.json"

    with open(input_path) as f:
        data = json.load(f)

    report = run_depth_sounder(data)

    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\nWritten: {output_path} ({os.path.getsize(output_path) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
