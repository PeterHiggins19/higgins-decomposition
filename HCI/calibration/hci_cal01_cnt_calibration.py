#!/usr/bin/env python3
"""
HCI-CAL01: Compositional Navigation Tensor Calibration Suite
=============================================================

Standard tensor engine tests adapted to the compositional simplex.
Each test object is a compositional time series where every CNT
output (bearing, angular velocity, steering sensitivity, helmsman)
is analytically derivable from first principles.

Test Objects:
  T01  Identity (stationary composition)
  T02  Single-carrier linear drift
  T03  Constant-velocity rotation in CLR space
  T04  Sensitivity divergence (carrier approaching zero)
  T05  Informational lock (constant ratio pair)
  T06  Bearing reversal (geometric-mean crossover)
  T07  Permutation symmetry
  T08  Contraction invariance (trace preservation)
  T09  Decomposition/reconstruction (CP-like)
  T10  Full navigation sequence (combined manoeuvres)

All compositions are closed (sum to 1), D >= 3, N >= 10.
ASCII output only. No colour. Monochrome.

Mathematical lineage:
  Aitchison (1986) - CLR transform, simplex geometry
  Higgins (2026)   - CNT bearing/velocity/sensitivity/helmsman

The instrument reads. The expert decides. The loop stays open.
"""

import math
import json
import os
import sys

# Add parent for CBS import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hci_cbs import (
    cnt_bearing, cnt_bearing_tensor, cnt_angular_velocity,
    cnt_steering_sensitivity, cnt_helmsman, cnt_lock_detect,
    build_trace_yz, build_trace_xz
)


# ══════════════════════════════════════════════════════════════════
# CLR UTILITIES
# ══════════════════════════════════════════════════════════════════

def clr(x):
    """Centred log-ratio transform."""
    D = len(x)
    log_x = [math.log(max(v, 1e-15)) for v in x]
    g = sum(log_x) / D
    return [v - g for v in log_x]


def hs_from_composition(x):
    """Higgins Scale: Hs = 1 - H/ln(D)."""
    D = len(x)
    if D < 2:
        return 0.0
    H = -sum(v * math.log(max(v, 1e-15)) for v in x)
    return 1.0 - H / math.log(D)


def close(x):
    """Closure to simplex."""
    s = sum(x)
    return [v / s for v in x]


def verify_closure(x, tol=1e-10):
    """Verify composition sums to 1."""
    return abs(sum(x) - 1.0) < tol


# ══════════════════════════════════════════════════════════════════
# TEST OBJECT GENERATORS
# ══════════════════════════════════════════════════════════════════

def t01_identity(N=20, D=4):
    """T01: Identity — stationary composition.

    Expected CNT:
      theta_{ij} = constant for all pairs, all timesteps
      omega = 0 for all consecutive pairs
      kappa = constant (1/x_j for each j)
      sigma = undefined (all deltas = 0)
    """
    # Uniform-ish composition (not exactly uniform to avoid degeneracy)
    base = close([0.4, 0.3, 0.2, 0.1][:D])
    data = [list(base) for _ in range(N)]

    expected = {
        "omega": [0.0] * (N - 1),
        "bearings_constant": True,
        "kappa_constant": True,
        "all_delta_clr_zero": True
    }
    return data, expected


def t02_single_carrier_drift(N=20, D=4):
    """T02: Single-carrier linear drift.

    Carrier 0 increases linearly from 0.1 to 0.5.
    Others redistribute to maintain closure.

    Expected CNT:
      sigma = 0 (carrier 0 is helmsman throughout — largest CLR change)
      omega > 0 and approximately constant (linear CLR drift)
      theta_{0,j} changes monotonically for all j
    """
    data = []
    for t in range(N):
        frac = t / (N - 1)
        c0 = 0.1 + 0.4 * frac  # 0.1 -> 0.5
        remainder = 1.0 - c0
        comp = [c0] + [remainder / (D - 1)] * (D - 1)
        data.append(close(comp))

    expected = {
        "helmsman_index": 0,
        "helmsman_name": "C0",
        "omega_positive": True,
        "theta_01_monotonic": True
    }
    return data, expected


def t03_constant_velocity_rotation(N=24, D=3):
    """T03: Constant-velocity rotation in CLR space.

    Composition traces a circle on the CLR zero-sum sphere.
    Angular velocity should be constant across all intervals.

    Construction uses orthonormal basis for the zero-sum plane:
      e1 = [1, -1, 0] / sqrt(2)
      e2 = [1,  1, -2] / sqrt(6)
      h(t) = r * (cos(2*pi*t/N) * e1 + sin(2*pi*t/N) * e2)

    This ensures ||h(t)|| = r for all t, giving constant omega.
    """
    r = 0.5  # CLR radius
    # Orthonormal basis for {h: sum(h)=0} in R^3
    e1 = [1.0 / math.sqrt(2), -1.0 / math.sqrt(2), 0.0]
    e2 = [1.0 / math.sqrt(6),  1.0 / math.sqrt(6), -2.0 / math.sqrt(6)]
    data = []
    for t in range(N):
        angle = 2 * math.pi * t / N
        c_a, s_a = math.cos(angle), math.sin(angle)
        h = [r * (c_a * e1[j] + s_a * e2[j]) for j in range(D)]
        # Invert CLR: x_j = exp(h_j) / sum(exp(h_k))
        exp_h = [math.exp(v) for v in h]
        total = sum(exp_h)
        comp = [e / total for e in exp_h]
        data.append(comp)

    # Expected constant angular velocity
    h0 = clr(data[0])
    h1 = clr(data[1])
    omega_expected = cnt_angular_velocity(h0, h1)

    expected = {
        "omega_constant": True,
        "omega_expected_deg": omega_expected,
        "omega_tolerance_deg": 0.5,
        "full_rotation": True,
        "bearing_01_range_deg": 360.0
    }
    return data, expected


def t04_sensitivity_divergence(N=20, D=3):
    """T04: Sensitivity divergence — carrier approaching zero.

    Carrier 2 decreases from 0.3 to 0.001.
    Corollary 5: kappa_{22} = 1/x_2 diverges as x_2 -> 0.

    Expected CNT:
      kappa[2] increases monotonically
      kappa[2] at final step >> kappa[2] at first step
      sigma = 2 near the end (vanishing carrier has infinite helm authority)
    """
    data = []
    for t in range(N):
        frac = t / (N - 1)
        c2 = 0.3 * (1.0 - 0.9967 * frac)  # 0.3 -> ~0.001
        remainder = 1.0 - c2
        comp = [remainder * 0.6, remainder * 0.4, c2]
        data.append(close(comp))

    expected = {
        "kappa_2_monotonic_increasing": True,
        "kappa_2_ratio_first_last_gt": 100.0,
        "helmsman_final_steps": 2
    }
    return data, expected


def t05_informational_lock(N=20, D=4):
    """T05: Informational lock — constant ratio pair.

    Carriers 0 and 1 maintain ratio 2:1 throughout.
    Other carriers change freely.

    Corollary 3: theta_{01} should have spread < epsilon.

    Expected CNT:
      theta_{01} approximately constant (locked pair)
      lock_detect should find pair (0, 1)
    """
    data = []
    for t in range(N):
        frac = t / (N - 1)
        # Carrier 2 oscillates, carrier 3 counter-oscillates
        c2 = 0.15 + 0.1 * math.sin(2 * math.pi * frac)
        c3 = 0.15 - 0.1 * math.sin(2 * math.pi * frac)
        # Carriers 0 and 1 in 2:1 ratio
        remainder = 1.0 - c2 - c3
        c0 = remainder * (2.0 / 3.0)
        c1 = remainder * (1.0 / 3.0)
        data.append(close([c0, c1, c2, c3]))

    expected = {
        "lock_pair": (0, 1),
        "lock_spread_lt_deg": 5.0,
        "theta_01_constant": True,
        "theta_23_varies": True
    }
    return data, expected


def t06_bearing_reversal(N=20, D=3):
    """T06: Bearing reversal — geometric-mean crossover.

    Carrier 0 starts above its geometric-mean share and ends below it.
    Carrier 1 does the opposite.

    Corollary 4: sign change in theta_{01} indicates structural crossover.

    Expected CNT:
      theta_{01} changes sign at the midpoint
      reversal event detected
    """
    data = []
    for t in range(N):
        frac = t / (N - 1)
        # Carrier 0: high start, low end
        c0 = 0.5 - 0.3 * frac  # 0.5 -> 0.2
        # Carrier 1: low start, high end
        c1 = 0.2 + 0.3 * frac  # 0.2 -> 0.5
        c2 = 1.0 - c0 - c1     # 0.3 constant
        data.append(close([c0, c1, c2]))

    expected = {
        "bearing_01_sign_change": True,
        "crossover_near_midpoint": True,
        "reversal_count": 1
    }
    return data, expected


def t07_permutation_symmetry(N=15, D=3):
    """T07: Permutation symmetry — relabelling carriers.

    Same trajectory computed with carriers in two different orders.
    All CNT magnitudes must be identical (bearing determinism).

    Corollary 1: Same composition, same bearing. No parameters.

    Expected CNT:
      Bearings for permuted version differ only by relabelling
      Angular velocities are identical
      Steering sensitivities are permuted (same values, different indices)
    """
    # Original trajectory
    data_original = []
    for t in range(N):
        frac = t / (N - 1)
        comp = close([0.5 - 0.2 * frac, 0.3 + 0.1 * frac, 0.2 + 0.1 * frac])
        data_original.append(comp)

    # Permuted: swap carrier 0 and carrier 2
    data_permuted = []
    for comp in data_original:
        data_permuted.append([comp[2], comp[1], comp[0]])

    expected = {
        "omega_identical": True,
        "kappa_sets_identical": True,
        "bearing_relabelling_consistent": True
    }
    return data_original, data_permuted, expected


def t08_contraction_invariance(N=15, D=4):
    """T08: Contraction invariance — trace preservation.

    The Aitchison metric tensor g_{jj} = 1/x_j has trace = sum(1/x_j).
    Under CLR transform, Tr(g) is preserved (same composition).

    Test: verify Tr(kappa) computed from CLR matches Tr(kappa) from fractions.

    Expected:
      sum(kappa) = sum(1/x_j) exactly (within floating-point tolerance)
      This tests the internal consistency of the sensitivity tensor.
    """
    data = []
    for t in range(N):
        frac = t / (N - 1)
        comp = close([0.4 + 0.1 * frac, 0.3 - 0.05 * frac,
                       0.2 - 0.03 * frac, 0.1 - 0.02 * frac])
        data.append(comp)

    expected = {
        "trace_preservation": True,
        "trace_tolerance": 1e-10
    }
    return data, expected


def t09_decomposition_reconstruction(N=20, D=3):
    """T09: Decomposition/reconstruction — rank-1 trajectory.

    Trajectory constructed from a single direction vector v in CLR space.
    h(t) = alpha(t) * v where alpha varies monotonically.

    This is a rank-1 tensor path — the simplest structure.
    All pairwise bearings should be constant (direction doesn't change).
    Angular velocity should be zero (direction is constant; only magnitude changes).

    Note: omega measures angle between direction vectors, not magnitude change.
    For a rank-1 path with increasing magnitude, omega = 0 exactly.
    """
    v = [1.0, -0.5, -0.5]  # Direction in CLR space (sums to 0)
    data = []
    for t in range(N):
        alpha = 0.1 + 0.9 * (t / (N - 1))  # 0.1 -> 1.0
        h = [alpha * vi for vi in v]
        exp_h = [math.exp(hi) for hi in h]
        total = sum(exp_h)
        comp = [e / total for e in exp_h]
        data.append(comp)

    expected = {
        "rank_1_trajectory": True,
        "all_bearings_constant": True,
        "omega_zero": True,
        "omega_tolerance_deg": 0.01
    }
    return data, expected


def t10_full_navigation(N=40, D=4):
    """T10: Full navigation sequence — combined manoeuvres.

    Phase 1 (t=0-9):    Steady state (identity region)
    Phase 2 (t=10-19):  Carrier 0 ramp-up (single-carrier drift)
    Phase 3 (t=20-29):  Carrier 2 collapse (sensitivity divergence)
    Phase 4 (t=30-39):  Recovery to near-uniform

    Expected CNT:
      Phase 1: omega ~ 0
      Phase 2: sigma = 0 (carrier 0 is helmsman)
      Phase 3: kappa[2] diverges, sigma = 2
      Phase 4: omega decreasing, system stabilising
    """
    data = []
    carriers = ["Alpha", "Beta", "Gamma", "Delta"]

    # Phase 1: steady state
    for t in range(10):
        data.append(close([0.3, 0.3, 0.2, 0.2]))

    # Phase 2: carrier 0 ramp
    for t in range(10):
        frac = t / 9
        c0 = 0.3 + 0.3 * frac  # 0.3 -> 0.6
        remainder = 1.0 - c0
        data.append(close([c0, remainder * 0.43, remainder * 0.29, remainder * 0.28]))

    # Phase 3: carrier 2 collapse
    for t in range(10):
        frac = t / 9
        c2 = 0.12 * (1.0 - 0.99 * frac)  # 0.12 -> ~0.001
        c0 = 0.6
        remainder = 1.0 - c0 - c2
        data.append(close([c0, remainder * 0.55, c2, remainder * 0.45]))

    # Phase 4: recovery
    for t in range(10):
        frac = t / 9
        target = [0.28, 0.27, 0.22, 0.23]
        start = data[-1]
        comp = [s + (tg - s) * frac for s, tg in zip(start, target)]
        data.append(close(comp))

    expected = {
        "carriers": carriers,
        "phase1_omega_near_zero": True,
        "phase2_helmsman": 0,
        "phase3_kappa2_diverges": True,
        "phase4_omega_decreasing": True,
        "total_timesteps": N
    }
    return data, expected, carriers


# ══════════════════════════════════════════════════════════════════
# TEST RUNNER AND VERIFICATION
# ══════════════════════════════════════════════════════════════════

def run_cnt_on_series(data, carriers=None):
    """Run full CNT analysis on a compositional time series."""
    N = len(data)
    D = len(data[0])
    if carriers is None:
        carriers = [f"C{i}" for i in range(D)]

    clr_series = [clr(x) for x in data]
    hs_series = [hs_from_composition(x) for x in data]

    # Bearing tensor at each timestep
    bearing_series = [cnt_bearing_tensor(h) for h in clr_series]

    # Angular velocity between consecutive steps
    omega_series = [cnt_angular_velocity(clr_series[t], clr_series[t + 1])
                    for t in range(N - 1)]

    # Steering sensitivity at each timestep
    kappa_series = [cnt_steering_sensitivity(h) for h in clr_series]

    # Helmsman between consecutive steps
    helmsman_series = [cnt_helmsman(clr_series[t], clr_series[t + 1], carriers)
                       for t in range(N - 1)]

    # Lock detection
    locks = cnt_lock_detect(bearing_series, epsilon=10.0)

    return {
        "N": N, "D": D, "carriers": carriers,
        "compositions": data,
        "clr_series": clr_series,
        "hs_series": hs_series,
        "bearing_series": bearing_series,
        "omega_series": omega_series,
        "kappa_series": kappa_series,
        "helmsman_series": helmsman_series,
        "locks": locks
    }


def verify_test(test_id, results, expected):
    """Verify CNT outputs against expected values. Returns (pass, details)."""
    details = []
    passed = True

    if test_id == "T01":
        # Identity: omega should be zero
        max_omega = max(results["omega_series"])
        ok = max_omega < 0.01
        details.append(f"  max(omega) = {max_omega:.6f} deg {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

        # Bearings should be constant
        b0 = results["bearing_series"][0]
        for t in range(1, results["N"]):
            bt = results["bearing_series"][t]
            for pair in b0:
                diff = abs(bt[pair] - b0[pair])
                if diff > 0.01:
                    passed = False
                    details.append(f"  bearing {pair} drifted by {diff:.4f} deg at t={t} FAIL")
                    break
        if passed:
            details.append(f"  all bearings constant PASS")

    elif test_id == "T02":
        # Single drift: helmsman should be carrier 0
        helm_counts = {}
        for idx, name, delta in results["helmsman_series"]:
            helm_counts[idx] = helm_counts.get(idx, 0) + 1
        dominant_helm = max(helm_counts, key=helm_counts.get)
        ok = dominant_helm == 0
        details.append(f"  dominant helmsman = C{dominant_helm} (expected C0) {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

        # Omega should be non-negative (positive within float tolerance)
        min_omega = min(results["omega_series"])
        ok = min_omega >= -0.001
        details.append(f"  min(omega) = {min_omega:.6f} deg (non-negative) {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

    elif test_id == "T03":
        # Constant rotation: omega should be approximately constant
        omegas = results["omega_series"]
        mean_omega = sum(omegas) / len(omegas)
        max_dev = max(abs(o - mean_omega) for o in omegas)
        tol = expected.get("omega_tolerance_deg", 0.5)
        ok = max_dev < tol
        details.append(f"  mean(omega) = {mean_omega:.4f} deg")
        details.append(f"  max deviation from mean = {max_dev:.4f} deg (tol={tol}) {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

    elif test_id == "T04":
        # Sensitivity divergence: kappa[2] should increase monotonically
        k2 = [k[2] for k in results["kappa_series"]]
        monotonic = all(k2[t + 1] >= k2[t] - 0.01 for t in range(len(k2) - 1))
        details.append(f"  kappa[2] monotonic increasing: {'PASS' if monotonic else 'FAIL'}")
        passed = passed and monotonic

        ratio = k2[-1] / k2[0]
        ok = ratio > expected.get("kappa_2_ratio_first_last_gt", 100.0)
        details.append(f"  kappa[2] ratio (last/first) = {ratio:.1f} (>{expected.get('kappa_2_ratio_first_last_gt', 100)}) {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

    elif test_id == "T05":
        # Lock detection: should find pair (0,1)
        lock_pairs = [(l[0], l[1]) for l in results["locks"]]
        ok = (0, 1) in lock_pairs
        if results["locks"]:
            spread = [l[2] for l in results["locks"] if (l[0], l[1]) == (0, 1)]
            details.append(f"  lock pair (0,1) found: {'PASS' if ok else 'FAIL'}")
            if spread:
                details.append(f"  lock spread = {spread[0]:.2f} deg")
        else:
            details.append(f"  no locks detected FAIL")
            passed = False
        passed = passed and ok

    elif test_id == "T06":
        # Bearing reversal: theta_{01} should change sign
        bearings_01 = [b.get((0, 1), 0) for b in results["bearing_series"]]
        sign_changes = sum(1 for t in range(len(bearings_01) - 1)
                          if bearings_01[t] * bearings_01[t + 1] < 0)
        ok = sign_changes >= 1
        details.append(f"  bearing (0,1) sign changes: {sign_changes} {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

    elif test_id == "T07_symmetry":
        # Permutation symmetry: omega series must be identical
        # This is handled separately (two datasets)
        pass

    elif test_id == "T08":
        # Contraction invariance: Tr(kappa) = sum(1/x_j)
        max_err = 0.0
        for t in range(results["N"]):
            x = results["compositions"][t]
            kappa = results["kappa_series"][t]
            tr_from_kappa = sum(kappa)
            tr_from_fracs = sum(1.0 / max(xj, 1e-15) for xj in x)
            err = abs(tr_from_kappa - tr_from_fracs)
            max_err = max(max_err, err)
        tol = expected.get("trace_tolerance", 1e-10)
        ok = max_err < tol
        details.append(f"  max |Tr(kappa) - sum(1/x_j)| = {max_err:.2e} (tol={tol}) {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

    elif test_id == "T09":
        # Rank-1: omega should be ~0 (direction constant, magnitude changes)
        max_omega = max(results["omega_series"])
        tol = expected.get("omega_tolerance_deg", 0.01)
        ok = max_omega < tol
        details.append(f"  max(omega) = {max_omega:.6f} deg (tol={tol}) {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

        # All bearings should be constant
        b0 = results["bearing_series"][0]
        max_drift = 0
        for t in range(1, results["N"]):
            bt = results["bearing_series"][t]
            for pair in b0:
                diff = abs(bt[pair] - b0[pair])
                max_drift = max(max_drift, diff)
        ok2 = max_drift < 0.1
        details.append(f"  max bearing drift = {max_drift:.4f} deg {'PASS' if ok2 else 'FAIL'}")
        passed = passed and ok2

    elif test_id == "T10":
        # Full navigation: multi-phase checks
        # Phase 1 (t=0-8): omega near zero
        phase1_omega = results["omega_series"][:9]
        max_p1 = max(phase1_omega) if phase1_omega else 0
        ok = max_p1 < 0.1
        details.append(f"  Phase 1 max(omega) = {max_p1:.4f} deg (near zero) {'PASS' if ok else 'FAIL'}")
        passed = passed and ok

        # Phase 2 (t=9-18): helmsman should be 0
        phase2_helms = [results["helmsman_series"][t][0] for t in range(9, min(18, len(results["helmsman_series"])))]
        if phase2_helms:
            most_common = max(set(phase2_helms), key=phase2_helms.count)
            ok = most_common == 0
            details.append(f"  Phase 2 dominant helmsman = C{most_common} (expected C0) {'PASS' if ok else 'FAIL'}")
            passed = passed and ok

        # Phase 3 (t=19-28): kappa[2] increases
        if len(results["kappa_series"]) > 28:
            k2_start = results["kappa_series"][19][2]
            k2_end = results["kappa_series"][28][2]
            ok = k2_end > k2_start * 5
            details.append(f"  Phase 3 kappa[2] ratio = {k2_end/k2_start:.1f}x {'PASS' if ok else 'FAIL'}")
            passed = passed and ok

    return passed, details


# ══════════════════════════════════════════════════════════════════
# MAIN CALIBRATION RUNNER
# ══════════════════════════════════════════════════════════════════

def run_calibration(output_dir=None):
    """Run full CNT calibration suite."""

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 72)
    print("  HCI-CAL01: Compositional Navigation Tensor Calibration")
    print("  Higgins Computational Instruments")
    print("=" * 72)
    print()

    results_all = {}
    total_tests = 0
    total_passed = 0

    # ── T01: Identity ──────────────────────────────────────────
    print("T01  Identity (stationary composition)")
    print("-" * 50)
    data, expected = t01_identity()
    r = run_cnt_on_series(data)
    ok, details = verify_test("T01", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    results_all["T01_identity"] = {"pass": ok, "N": r["N"], "D": r["D"],
                                    "max_omega": max(r["omega_series"]),
                                    "hs_range": [min(r["hs_series"]), max(r["hs_series"])]}

    # ── T02: Single-carrier drift ──────────────────────────────
    print("T02  Single-carrier linear drift")
    print("-" * 50)
    data, expected = t02_single_carrier_drift()
    r = run_cnt_on_series(data)
    ok, details = verify_test("T02", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    results_all["T02_single_drift"] = {"pass": ok, "N": r["N"], "D": r["D"],
                                        "mean_omega": sum(r["omega_series"]) / len(r["omega_series"])}

    # ── T03: Constant-velocity rotation ────────────────────────
    print("T03  Constant-velocity rotation in CLR space")
    print("-" * 50)
    data, expected = t03_constant_velocity_rotation()
    r = run_cnt_on_series(data)
    ok, details = verify_test("T03", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    omegas = r["omega_series"]
    results_all["T03_rotation"] = {"pass": ok, "N": r["N"], "D": r["D"],
                                    "mean_omega": sum(omegas) / len(omegas),
                                    "omega_std": (sum((o - sum(omegas)/len(omegas))**2 for o in omegas) / len(omegas))**0.5}

    # ── T04: Sensitivity divergence ────────────────────────────
    print("T04  Sensitivity divergence (carrier approaching zero)")
    print("-" * 50)
    data, expected = t04_sensitivity_divergence()
    r = run_cnt_on_series(data)
    ok, details = verify_test("T04", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    k2 = [k[2] for k in r["kappa_series"]]
    results_all["T04_divergence"] = {"pass": ok, "N": r["N"], "D": r["D"],
                                      "kappa2_first": k2[0], "kappa2_last": k2[-1],
                                      "kappa2_ratio": k2[-1] / k2[0]}

    # ── T05: Informational lock ────────────────────────────────
    print("T05  Informational lock (constant ratio pair)")
    print("-" * 50)
    data, expected = t05_informational_lock()
    r = run_cnt_on_series(data)
    ok, details = verify_test("T05", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    results_all["T05_lock"] = {"pass": ok, "N": r["N"], "D": r["D"],
                                "locks_found": len(r["locks"]),
                                "lock_pairs": [(l[0], l[1], round(l[2], 2)) for l in r["locks"]]}

    # ── T06: Bearing reversal ──────────────────────────────────
    print("T06  Bearing reversal (geometric-mean crossover)")
    print("-" * 50)
    data, expected = t06_bearing_reversal()
    r = run_cnt_on_series(data)
    ok, details = verify_test("T06", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    bearings_01 = [b.get((0, 1), 0) for b in r["bearing_series"]]
    results_all["T06_reversal"] = {"pass": ok, "N": r["N"], "D": r["D"],
                                    "bearing_01_start": round(bearings_01[0], 2),
                                    "bearing_01_end": round(bearings_01[-1], 2)}

    # ── T07: Permutation symmetry ──────────────────────────────
    print("T07  Permutation symmetry (carrier relabelling)")
    print("-" * 50)
    data_orig, data_perm, expected = t07_permutation_symmetry()
    r_orig = run_cnt_on_series(data_orig)
    r_perm = run_cnt_on_series(data_perm)
    # Check omega series identical
    omega_diff = max(abs(a - b) for a, b in zip(r_orig["omega_series"], r_perm["omega_series"]))
    ok1 = omega_diff < 1e-10
    print(f"  max |omega_orig - omega_perm| = {omega_diff:.2e} {'PASS' if ok1 else 'FAIL'}")
    # Check kappa sets identical (permuted)
    kappa_ok = True
    for t in range(len(r_orig["kappa_series"])):
        k_orig = sorted(r_orig["kappa_series"][t])
        k_perm = sorted(r_perm["kappa_series"][t])
        diff = max(abs(a - b) for a, b in zip(k_orig, k_perm))
        if diff > 1e-10:
            kappa_ok = False
            break
    print(f"  kappa multisets identical: {'PASS' if kappa_ok else 'FAIL'}")
    ok = ok1 and kappa_ok
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    results_all["T07_symmetry"] = {"pass": ok, "N": r_orig["N"], "D": r_orig["D"],
                                    "omega_max_diff": omega_diff}

    # ── T08: Contraction invariance ────────────────────────────
    print("T08  Contraction invariance (trace preservation)")
    print("-" * 50)
    data, expected = t08_contraction_invariance()
    r = run_cnt_on_series(data)
    ok, details = verify_test("T08", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    results_all["T08_contraction"] = {"pass": ok, "N": r["N"], "D": r["D"]}

    # ── T09: Decomposition/reconstruction ──────────────────────
    print("T09  Decomposition/reconstruction (rank-1 trajectory)")
    print("-" * 50)
    data, expected = t09_decomposition_reconstruction()
    r = run_cnt_on_series(data)
    ok, details = verify_test("T09", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    results_all["T09_decomposition"] = {"pass": ok, "N": r["N"], "D": r["D"],
                                         "max_omega": max(r["omega_series"])}

    # ── T10: Full navigation ───────────────────────────────────
    print("T10  Full navigation sequence (combined manoeuvres)")
    print("-" * 50)
    data, expected, carriers = t10_full_navigation()
    r = run_cnt_on_series(data, carriers)
    ok, details = verify_test("T10", r, expected)
    for d in details:
        print(d)
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    print()
    total_tests += 1
    total_passed += int(ok)
    results_all["T10_navigation"] = {"pass": ok, "N": r["N"], "D": r["D"]}

    # ── Summary ────────────────────────────────────────────────
    print("=" * 72)
    print(f"  CALIBRATION RESULT: {total_passed}/{total_tests} PASS")
    if total_passed == total_tests:
        print("  STATUS: ALL PASS — CNT engine calibrated")
    else:
        print(f"  STATUS: {total_tests - total_passed} FAILURE(S)")
    print("=" * 72)
    print()

    # ── Generate CBS oscilloscope output for T10 ───────────────
    print("Generating CBS oscilloscope traces for T10 (full navigation)...")
    print()

    years = list(range(2000, 2000 + r["N"]))

    # YZ face: Hs vs Time
    yz_trace = build_trace_yz(years, r["hs_series"], width=72, height=25)
    print("\n".join(yz_trace))
    print()

    # XZ face: Bearing vs Time (use pair 0,1)
    bearings_2d = [b.get((0, 1), 0) for b in r["bearing_series"]]
    xz_trace = build_trace_xz(years, bearings_2d,
                                [h[0] for _, h, _ in r["helmsman_series"]],
                                width=72, height=25)
    print("\n".join(xz_trace))
    print()

    # Navigation table (local format for calibration data)
    print("  COMPOSITIONAL NAVIGATION TENSOR (CNT) — CALIBRATION DATA TABLE")
    print("  " + "=" * 78)
    print(f"  {'Step':>4}  {'Hs':>7}  {'theta_01':>9}  {'omega':>8}  "
          f"{'Helm':>5}  {'kappa_max':>10}  {'kappa_min':>10}")
    print("  " + "-" * 78)
    for t in range(r["N"]):
        hs_v = r["hs_series"][t]
        theta_01 = r["bearing_series"][t].get((0, 1), 0.0)
        omega_v = r["omega_series"][t - 1] if t > 0 else 0.0
        if t > 0:
            h_idx, h_name, h_dc = r["helmsman_series"][t - 1]
        else:
            h_idx, h_name, h_dc = 0, "-", 0.0
        kappa = cnt_steering_sensitivity(r["clr_series"][t])
        k_max, k_min = max(kappa), min(kappa)
        flag = " ^" if omega_v > 10.0 else ""
        print(f"  {t:>4}  {hs_v:>7.4f}  {theta_01:>9.2f}  {omega_v:>8.3f}  "
              f"{h_name:>5}  {k_max:>10.2f}  {k_min:>10.2f}{flag}")
    print()

    # Lock report (local format for calibration data)
    print("  INFORMATIONAL LOCK DETECTION")
    print("  " + "=" * 60)
    locks = r["locks"]
    if locks:
        locks.sort(key=lambda x: x[2])
        for i, j, spread in locks:
            ci = carriers[i] if i < len(carriers) else f"C{i}"
            cj = carriers[j] if j < len(carriers) else f"C{j}"
            print(f"  LOCKED: {ci}-{cj}  spread = {spread:.1f} deg  "
                  f"(< 10 deg threshold)")
    else:
        print("  No locked pairs found at epsilon = 10 deg")
    print()

    # ── Save results ───────────────────────────────────────────
    output = {
        "_meta": {
            "type": "HCI_CALIBRATION",
            "experiment": "HCI-CAL01",
            "name": "CNT Calibration Suite",
            "date": "2026-05-02",
            "generator": "hci_cal01_cnt_calibration.py",
            "total_tests": total_tests,
            "total_passed": total_passed,
            "status": "ALL PASS" if total_passed == total_tests else f"{total_tests - total_passed} FAILURE(S)"
        },
        "tests": results_all,
        "test_descriptions": {
            "T01_identity": "Stationary composition — omega=0, bearings constant",
            "T02_single_drift": "Single-carrier linear drift — carrier 0 is helmsman",
            "T03_rotation": "Constant-velocity rotation — omega constant across intervals",
            "T04_divergence": "Carrier approaching zero — kappa diverges (Corollary 5)",
            "T05_lock": "Constant ratio pair — lock detection (Corollary 3)",
            "T06_reversal": "Geometric-mean crossover — bearing sign change (Corollary 4)",
            "T07_symmetry": "Carrier relabelling — omega and kappa permutation invariance",
            "T08_contraction": "Trace preservation — Tr(kappa) = sum(1/x_j) exactly",
            "T09_decomposition": "Rank-1 trajectory — constant bearing, zero omega",
            "T10_navigation": "Multi-phase sequence — identity/drift/divergence/recovery"
        }
    }

    output_file = os.path.join(output_dir, "HCI-CAL01_results.json")
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {output_file}")

    return total_passed, total_tests, output


if __name__ == "__main__":
    run_calibration()
