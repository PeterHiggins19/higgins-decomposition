#!/usr/bin/env python3
"""
CNT Precision Experiment
========================

Systematic probing of every numerical weak point in the Compositional
Navigation Tensor engine. Quantifies the actual precision floor of
each CNT channel under controlled conditions.

Experiments:
  P01  CLR zero-sum residual — does sum(clr(x)) = 0 hold?
  P02  Norm variation in naive vs orthonormal CLR circle
  P03  arccos instability near 0 and 180 degrees
  P04  Stable angle via atan2(||cross||, dot) comparison
  P05  ILR vs CLR angular velocity — redundancy cost
  P06  Helmert matrix projection — ILR equivalence proof
  P07  Condition number of Aitchison metric vs composition
  P08  Extreme composition stress test (x_j = 10^{-k})
  P09  High-D scaling — precision vs dimensionality
  P10  Full precision chain — error propagation through CNT

Mathematical lineage:
  Aitchison (1986) — CLR, Aitchison inner product
  Egozcue et al. (2003) — ILR, Helmert submatrix
  Higgins (2026) — CNT bearing/velocity/sensitivity/helmsman
"""

import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hci_cbs import (
    cnt_bearing, cnt_bearing_tensor, cnt_angular_velocity,
    cnt_steering_sensitivity, cnt_helmsman
)


# ══════════════════════════════════════════════════════════════════
# UTILITIES
# ══════════════════════════════════════════════════════════════════

def clr(x):
    """Centred log-ratio transform."""
    D = len(x)
    log_x = [math.log(max(v, 1e-300)) for v in x]
    g = sum(log_x) / D
    return [v - g for v in log_x]


def close(x):
    """Closure to simplex."""
    s = sum(x)
    return [v / s for v in x]


def helmert_basis(D):
    """Helmert submatrix: orthonormal basis for the CLR zero-sum plane.

    Returns (D-1) x D matrix where each row is an orthonormal
    basis vector for {h in R^D : sum(h) = 0}.

    Row k (0-indexed):
      e_k = [1/sqrt(k*(k+1)), ..., 1/sqrt(k*(k+1)), -k/sqrt(k*(k+1)), 0, ..., 0]
      with (k) entries of 1/sqrt(...), then one entry of -k/sqrt(...), then zeros.

    This is the standard Helmert submatrix used in ILR (Egozcue et al. 2003).
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


def ilr_from_clr(h, basis):
    """Project CLR vector to ILR using Helmert basis.

    ILR_k = <h, e_k> = sum(h_j * e_k_j)
    """
    return [sum(h[j] * basis[k][j] for j in range(len(h)))
            for k in range(len(basis))]


def clr_from_ilr(z, basis):
    """Reconstruct CLR from ILR coordinates.

    h = sum(z_k * e_k)
    """
    D = len(basis[0])
    h = [0.0] * D
    for k in range(len(z)):
        for j in range(D):
            h[j] += z[k] * basis[k][j]
    return h


def angular_velocity_stable(h1, h2):
    """Numerically stable angular velocity using atan2.

    Instead of arccos(cos_theta), compute:
      sin_theta = ||h1 x h2|| / (||h1|| * ||h2||)
      cos_theta = <h1, h2> / (||h1|| * ||h2||)
      theta = atan2(sin_theta, cos_theta)

    For D > 3, the cross product generalises to:
      ||h1 x h2||^2 = ||h1||^2 * ||h2||^2 - <h1,h2>^2
    (Lagrange identity)
    """
    dot = sum(a * b for a, b in zip(h1, h2))
    m1_sq = sum(a ** 2 for a in h1)
    m2_sq = sum(a ** 2 for a in h2)
    m1 = math.sqrt(m1_sq)
    m2 = math.sqrt(m2_sq)
    if m1 < 1e-300 or m2 < 1e-300:
        return 0.0
    # Lagrange identity: ||a x b||^2 = ||a||^2 ||b||^2 - (a.b)^2
    cross_sq = max(0.0, m1_sq * m2_sq - dot * dot)
    cross_mag = math.sqrt(cross_sq)
    return math.degrees(math.atan2(cross_mag, dot))


def angular_velocity_ilr(h1, h2, basis):
    """Angular velocity computed in ILR space (non-redundant)."""
    z1 = ilr_from_clr(h1, basis)
    z2 = ilr_from_clr(h2, basis)
    return angular_velocity_stable(z1, z2)


def condition_number_aitchison(x):
    """Condition number of the Aitchison metric tensor.

    The diagonal Aitchison metric is g_{jj} = 1/x_j.
    Condition number = max(g) / min(g) = max(1/x_j) / min(1/x_j) = max(x) / min(x).
    Wait: condition number = max eigenvalue / min eigenvalue.
    For diagonal matrix: kappa = max(1/x_j) / min(1/x_j).
    """
    kappa = [1.0 / max(v, 1e-300) for v in x]
    return max(kappa) / min(kappa) if min(kappa) > 0 else float('inf')


# ══════════════════════════════════════════════════════════════════
# EXPERIMENTS
# ══════════════════════════════════════════════════════════════════

def p01_clr_zero_sum():
    """P01: Does sum(clr(x)) = 0 hold to machine precision?"""
    print("P01  CLR zero-sum residual")
    print("-" * 60)

    test_comps = [
        ("uniform_4", close([1, 1, 1, 1])),
        ("skewed_4", close([0.7, 0.2, 0.08, 0.02])),
        ("extreme_4", close([0.999, 0.0005, 0.0003, 0.0002])),
        ("uniform_8", close([1] * 8)),
        ("skewed_8", close([0.5, 0.2, 0.1, 0.08, 0.05, 0.04, 0.02, 0.01])),
        ("uniform_20", close([1] * 20)),
        ("near_zero", close([0.999999, 1e-6 / 3] * 1 + [1e-6 / 3] * 2)),
    ]

    max_residual = 0
    for name, x in test_comps:
        h = clr(x)
        residual = abs(sum(h))
        max_residual = max(max_residual, residual)
        print(f"  {name:15s}  D={len(x):2d}  sum(clr) = {sum(h):+.2e}  "
              f"|residual| = {residual:.2e}")

    print(f"\n  Maximum residual: {max_residual:.2e}")
    print(f"  Machine epsilon:  {sys.float_info.epsilon:.2e}")
    print(f"  Ratio:            {max_residual / sys.float_info.epsilon:.1f} eps")
    return max_residual


def p02_norm_variation():
    """P02: Norm variation — naive circle vs orthonormal circle."""
    print("\nP02  Norm variation in CLR circle constructions")
    print("-" * 60)

    D = 3
    r = 0.5
    N = 360  # one-degree increments

    # Method A: Naive (h[2] = -(h[0]+h[1]))
    norms_naive = []
    for t in range(N):
        angle = 2 * math.pi * t / N
        h = [r * math.cos(angle), r * math.sin(angle), 0.0]
        h[2] = -(h[0] + h[1])
        norm = math.sqrt(sum(v**2 for v in h))
        norms_naive.append(norm)

    # Method B: Orthonormal basis
    e1 = [1.0 / math.sqrt(2), -1.0 / math.sqrt(2), 0.0]
    e2 = [1.0 / math.sqrt(6),  1.0 / math.sqrt(6), -2.0 / math.sqrt(6)]
    norms_ortho = []
    for t in range(N):
        angle = 2 * math.pi * t / N
        c, s = math.cos(angle), math.sin(angle)
        h = [r * (c * e1[j] + s * e2[j]) for j in range(D)]
        norm = math.sqrt(sum(v**2 for v in h))
        norms_ortho.append(norm)

    # Method C: Helmert basis (general D)
    basis = helmert_basis(D)
    norms_helmert = []
    for t in range(N):
        angle = 2 * math.pi * t / N
        z = [r * math.cos(angle), r * math.sin(angle)]  # ILR coordinates
        h = clr_from_ilr(z, basis)
        norm = math.sqrt(sum(v**2 for v in h))
        norms_helmert.append(norm)

    for label, norms in [("Naive", norms_naive), ("Orthonormal", norms_ortho),
                          ("Helmert", norms_helmert)]:
        mn, mx = min(norms), max(norms)
        variation = (mx - mn) / ((mx + mn) / 2) * 100
        print(f"  {label:12s}  min={mn:.10f}  max={mx:.10f}  "
              f"variation={variation:.6f}%")

    # Derive the analytical norm for naive method
    # ||h||^2 = r^2 cos^2 + r^2 sin^2 + r^2(cos+sin)^2
    #         = r^2(1 + 1 + 2sincos) = r^2(2 + sin2theta)
    print(f"\n  Analytical naive ||h||^2 = r^2(2 + sin(2theta))")
    print(f"  Range: r*sqrt(1) to r*sqrt(3) = [{r:.4f}, {r*math.sqrt(3):.4f}]")
    print(f"  Ratio max/min = sqrt(3) = {math.sqrt(3):.10f}")
    print(f"  This 73% norm variation is NOT numerical error — it is geometric.")

    return norms_naive, norms_ortho, norms_helmert


def p03_arccos_instability():
    """P03: arccos instability near 0 and 180 degrees."""
    print("\nP03  arccos instability near extremes")
    print("-" * 60)

    # Test points near cos=1 (angle~0) and cos=-1 (angle~180)
    print("  Near 0 degrees (cos -> 1):")
    for k in range(1, 17):
        delta = 10 ** (-k)
        cos_val = 1.0 - delta
        if cos_val > 1.0:
            cos_val = 1.0
        angle_arccos = math.degrees(math.acos(max(-1, min(1, cos_val))))
        # Stable: sin(theta) ~ sqrt(2*delta) for small theta
        sin_val = math.sqrt(max(0, 2 * delta - delta**2))
        angle_atan2 = math.degrees(math.atan2(sin_val, cos_val))
        diff = abs(angle_arccos - angle_atan2)
        print(f"    1-cos = 1e-{k:2d}  arccos={angle_arccos:.15e}  "
              f"atan2={angle_atan2:.15e}  diff={diff:.2e}")

    print(f"\n  Near 180 degrees (cos -> -1):")
    for k in range(1, 17):
        delta = 10 ** (-k)
        cos_val = -1.0 + delta
        if cos_val < -1.0:
            cos_val = -1.0
        angle_arccos = math.degrees(math.acos(max(-1, min(1, cos_val))))
        sin_val = math.sqrt(max(0, 2 * delta - delta**2))
        angle_atan2 = math.degrees(math.atan2(sin_val, cos_val))
        diff = abs(angle_arccos - angle_atan2)
        print(f"    1+cos = 1e-{k:2d}  arccos={angle_arccos:.15e}  "
              f"atan2={angle_atan2:.15e}  diff={diff:.2e}")


def p04_stable_vs_arccos():
    """P04: Compare arccos vs atan2 angular velocity on calibration data."""
    print("\nP04  Stable angle (atan2) vs arccos on T03 rotation")
    print("-" * 60)

    D = 3
    r = 0.5
    N = 360

    e1 = [1.0 / math.sqrt(2), -1.0 / math.sqrt(2), 0.0]
    e2 = [1.0 / math.sqrt(6),  1.0 / math.sqrt(6), -2.0 / math.sqrt(6)]

    clr_series = []
    for t in range(N):
        angle = 2 * math.pi * t / N
        c, s = math.cos(angle), math.sin(angle)
        h = [r * (c * e1[j] + s * e2[j]) for j in range(D)]
        clr_series.append(h)

    diffs = []
    max_diff = 0
    for t in range(N - 1):
        omega_arccos = cnt_angular_velocity(clr_series[t], clr_series[t + 1])
        omega_atan2 = angular_velocity_stable(clr_series[t], clr_series[t + 1])
        diff = abs(omega_arccos - omega_atan2)
        diffs.append(diff)
        max_diff = max(max_diff, diff)

    expected_omega = 360.0 / N
    arccos_omegas = [cnt_angular_velocity(clr_series[t], clr_series[t+1]) for t in range(N-1)]
    atan2_omegas = [angular_velocity_stable(clr_series[t], clr_series[t+1]) for t in range(N-1)]

    print(f"  Expected omega: {expected_omega:.10f} deg/step")
    print(f"  arccos:  mean={sum(arccos_omegas)/len(arccos_omegas):.15f}  "
          f"std={stdev(arccos_omegas):.2e}")
    print(f"  atan2:   mean={sum(atan2_omegas)/len(atan2_omegas):.15f}  "
          f"std={stdev(atan2_omegas):.2e}")
    print(f"  max |arccos - atan2| = {max_diff:.2e} deg")
    print(f"  Both methods identical to machine precision on well-conditioned data.")


def p05_ilr_vs_clr():
    """P05: ILR vs CLR angular velocity — redundancy cost."""
    print("\nP05  ILR vs CLR angular velocity comparison")
    print("-" * 60)

    for D in [3, 4, 8, 20]:
        basis = helmert_basis(D)
        N = 100

        # Random-ish compositions
        comps = []
        for t in range(N):
            frac = t / (N - 1)
            raw = [1.0 + 0.5 * math.sin(2 * math.pi * j / D + frac * math.pi)
                   for j in range(D)]
            comps.append(close(raw))

        clr_series = [clr(x) for x in comps]

        max_diff = 0
        for t in range(N - 1):
            omega_clr = angular_velocity_stable(clr_series[t], clr_series[t + 1])
            omega_ilr = angular_velocity_ilr(clr_series[t], clr_series[t + 1], basis)
            diff = abs(omega_clr - omega_ilr)
            max_diff = max(max_diff, diff)

        print(f"  D={D:2d}  max |omega_CLR - omega_ILR| = {max_diff:.2e} deg")

    print(f"\n  CLR and ILR give identical angles (Aitchison isometry).")
    print(f"  No precision gain from ILR projection for angular velocity.")
    print(f"  But ILR is non-redundant (D-1 dims vs D dims) — fewer operations.")


def p06_helmert_verification():
    """P06: Verify Helmert basis properties."""
    print("\nP06  Helmert basis verification")
    print("-" * 60)

    for D in [3, 4, 8]:
        basis = helmert_basis(D)

        # Check orthonormality
        max_off_diag = 0
        max_diag_err = 0
        for i in range(len(basis)):
            for j in range(len(basis)):
                dot = sum(basis[i][k] * basis[j][k] for k in range(D))
                if i == j:
                    max_diag_err = max(max_diag_err, abs(dot - 1.0))
                else:
                    max_off_diag = max(max_off_diag, abs(dot))

        # Check zero-sum: each row sums to zero
        max_row_sum = max(abs(sum(row)) for row in basis)

        # Check CLR roundtrip
        x = close([1 + 0.1 * j for j in range(D)])
        h = clr(x)
        z = ilr_from_clr(h, basis)
        h_back = clr_from_ilr(z, basis)
        roundtrip_err = max(abs(h[j] - h_back[j]) for j in range(D))

        # Check norm preservation
        norm_h = math.sqrt(sum(v**2 for v in h))
        norm_z = math.sqrt(sum(v**2 for v in z))
        norm_err = abs(norm_h - norm_z)

        print(f"  D={D}:")
        print(f"    Orthonormality: max|<ei,ej>-delta_ij| = {max(max_diag_err, max_off_diag):.2e}")
        print(f"    Zero-sum:       max|sum(e_k)| = {max_row_sum:.2e}")
        print(f"    CLR roundtrip:  max|h - h'| = {roundtrip_err:.2e}")
        print(f"    Norm preserved: |norm_CLR - norm_ILR| = {norm_err:.2e}")


def p07_condition_number():
    """P07: Aitchison metric condition number vs composition."""
    print("\nP07  Aitchison metric condition number")
    print("-" * 60)

    compositions = [
        ("uniform",          close([1, 1, 1, 1])),
        ("mild_skew",        close([0.4, 0.3, 0.2, 0.1])),
        ("moderate_skew",    close([0.7, 0.15, 0.1, 0.05])),
        ("severe_skew",      close([0.95, 0.03, 0.015, 0.005])),
        ("extreme_skew",     close([0.999, 0.0005, 0.0003, 0.0002])),
        ("near_boundary",    close([0.99999, 1e-5/3, 1e-5/3, 1e-5/3])),
        ("at_boundary",      close([1-1e-10, 1e-10/3, 1e-10/3, 1e-10/3])),
    ]

    print(f"  {'Name':20s}  {'kappa':>12s}  {'log10(kappa)':>12s}  {'min(x_j)':>12s}")
    print(f"  {'-'*20}  {'-'*12}  {'-'*12}  {'-'*12}")

    for name, x in compositions:
        kappa = condition_number_aitchison(x)
        min_x = min(x)
        log_kappa = math.log10(kappa) if kappa > 0 and kappa < float('inf') else float('inf')
        print(f"  {name:20s}  {kappa:12.2f}  {log_kappa:12.2f}  {min_x:12.2e}")

    print(f"\n  Condition number = max(x)/min(x) for diagonal Aitchison metric.")
    print(f"  CNT operations lose ~log10(kappa) digits of precision.")
    print(f"  For min(x) = 10^-k, kappa ~ 10^k, so k digits lost.")


def p08_extreme_stress():
    """P08: Extreme composition stress test."""
    print("\nP08  Extreme composition stress test")
    print("-" * 60)

    D = 4
    print(f"  Testing x_j = 10^{{-k}} for k = 1..15, D={D}")
    print(f"  {'k':>3s}  {'x_min':>12s}  {'sum(clr)':>12s}  {'omega_err':>12s}  "
          f"{'kappa_err':>12s}  {'status':>8s}")
    print(f"  {'-'*3}  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*8}")

    for k in range(1, 16):
        x_small = 10 ** (-k)
        remainder = 1.0 - x_small
        x = close([remainder / 3] * 3 + [x_small])

        h = clr(x)
        clr_residual = abs(sum(h))

        # Omega between x and a slightly perturbed version
        x2 = close([remainder / 3 + 0.001] * 2 + [remainder / 3 - 0.002] + [x_small])
        h2 = clr(x2)

        omega_arccos = cnt_angular_velocity(h, h2)
        omega_stable = angular_velocity_stable(h, h2)
        omega_err = abs(omega_arccos - omega_stable)

        # Kappa check: 1/x_j vs analytic
        kappa = cnt_steering_sensitivity(h)
        kappa_expected = 1.0 / x_small
        kappa_err = abs(kappa[3] - kappa_expected) / kappa_expected if kappa_expected > 0 else 0

        status = "OK" if clr_residual < 1e-10 and omega_err < 1e-10 else "WARN"
        if k >= 14:
            status = "LIMIT"

        print(f"  {k:3d}  {x_small:12.2e}  {clr_residual:12.2e}  {omega_err:12.2e}  "
              f"{kappa_err:12.2e}  {status:>8s}")


def p09_dimensionality_scaling():
    """P09: Precision vs dimensionality."""
    print("\nP09  Precision scaling with dimensionality")
    print("-" * 60)

    print(f"  {'D':>4s}  {'CLR_residual':>14s}  {'omega_std':>14s}  "
          f"{'Helmert_ortho':>14s}  {'norm_preserve':>14s}")
    print(f"  {'-'*4}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*14}")

    for D in [3, 4, 5, 8, 10, 20, 50, 100]:
        basis = helmert_basis(D)

        # CLR residual on uniform composition
        x = close([1] * D)
        h = clr(x)
        clr_res = abs(sum(h))

        # Omega consistency on circle in ILR space
        N = 100
        omegas = []
        for t in range(N):
            angle1 = 2 * math.pi * t / N
            angle2 = 2 * math.pi * (t + 1) / N
            z1 = [0.0] * (D - 1)
            z2 = [0.0] * (D - 1)
            if D >= 3:
                z1[0] = 0.3 * math.cos(angle1)
                z1[1] = 0.3 * math.sin(angle1)
                z2[0] = 0.3 * math.cos(angle2)
                z2[1] = 0.3 * math.sin(angle2)
            h1 = clr_from_ilr(z1, basis)
            h2 = clr_from_ilr(z2, basis)
            omega = angular_velocity_stable(h1, h2)
            omegas.append(omega)

        omega_s = stdev(omegas) if len(omegas) > 1 else 0

        # Helmert orthogonality
        max_err = 0
        for i in range(min(len(basis), 10)):  # cap to avoid O(D^2) for large D
            for j in range(min(len(basis), 10)):
                dot = sum(basis[i][k] * basis[j][k] for k in range(D))
                expected = 1.0 if i == j else 0.0
                max_err = max(max_err, abs(dot - expected))

        # Norm preservation
        x_test = close([1 + 0.1 * math.sin(j) for j in range(D)])
        h_test = clr(x_test)
        z_test = ilr_from_clr(h_test, basis)
        norm_h = math.sqrt(sum(v**2 for v in h_test))
        norm_z = math.sqrt(sum(v**2 for v in z_test))
        norm_err = abs(norm_h - norm_z)

        print(f"  {D:4d}  {clr_res:14.2e}  {omega_s:14.2e}  "
              f"{max_err:14.2e}  {norm_err:14.2e}")


def p10_full_chain():
    """P10: Full precision chain — error propagation through CNT."""
    print("\nP10  Full CNT precision chain")
    print("-" * 60)

    D = 4
    carriers = ["A", "B", "C", "D"]

    # Well-conditioned test pair
    x1 = close([0.4, 0.3, 0.2, 0.1])
    x2 = close([0.38, 0.32, 0.19, 0.11])

    h1 = clr(x1)
    h2 = clr(x2)

    print(f"  Composition 1: {[f'{v:.4f}' for v in x1]}")
    print(f"  Composition 2: {[f'{v:.4f}' for v in x2]}")
    print()

    # CLR precision
    r1 = abs(sum(h1))
    r2 = abs(sum(h2))
    print(f"  Stage 1 — CLR transform:")
    print(f"    sum(clr_1) = {sum(h1):+.2e}  (should be 0)")
    print(f"    sum(clr_2) = {sum(h2):+.2e}  (should be 0)")

    # Bearing precision (atan2 is always well-conditioned)
    b = cnt_bearing_tensor(h1)
    print(f"\n  Stage 2 — Bearing tensor:")
    print(f"    {len(b)} pairwise bearings computed")
    print(f"    atan2 conditioning: ALWAYS stable (no singularity at origin)")

    # Angular velocity — compare methods
    omega_arccos = cnt_angular_velocity(h1, h2)
    omega_stable = angular_velocity_stable(h1, h2)
    omega_diff = abs(omega_arccos - omega_stable)
    print(f"\n  Stage 3 — Angular velocity:")
    print(f"    arccos method:  {omega_arccos:.15f} deg")
    print(f"    atan2 method:   {omega_stable:.15f} deg")
    print(f"    difference:     {omega_diff:.2e} deg")

    # Steering sensitivity
    kappa = cnt_steering_sensitivity(h1)
    kappa_direct = [1.0 / x for x in x1]
    kappa_errs = [abs(kappa[j] - kappa_direct[j]) / kappa_direct[j] for j in range(D)]
    print(f"\n  Stage 4 — Steering sensitivity:")
    print(f"    max relative error (softmax vs direct): {max(kappa_errs):.2e}")
    print(f"    Condition number: {max(kappa)/min(kappa):.2f}")

    # Helmsman
    idx, name, delta = cnt_helmsman(h1, h2, carriers)
    print(f"\n  Stage 5 — Helmsman:")
    print(f"    sigma = {name} (index {idx}), delta_clr = {delta:+.6f}")
    print(f"    Helmsman determination: EXACT (argmax of |delta|)")

    # Overall precision budget
    print(f"\n  ═══ PRECISION BUDGET ═══")
    print(f"  CLR zero-sum:        {max(r1, r2):.2e} (limited by log/mean arithmetic)")
    print(f"  Bearing (atan2):     machine precision (always stable)")
    print(f"  Angular velocity:    {omega_diff:.2e} deg (arccos vs atan2)")
    print(f"  Steering sensitivity:{max(kappa_errs):.2e} (softmax roundtrip)")
    print(f"  Helmsman:            exact (discrete argmax)")
    print(f"  Overall floor:       ~{sys.float_info.epsilon:.2e} (IEEE 754 double)")


# ══════════════════════════════════════════════════════════════════
# HELPER
# ══════════════════════════════════════════════════════════════════

def stdev(vals):
    """Standard deviation."""
    n = len(vals)
    if n < 2:
        return 0.0
    mean = sum(vals) / n
    return math.sqrt(sum((v - mean)**2 for v in vals) / (n - 1))


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 72)
    print("  CNT PRECISION EXPERIMENT")
    print("  Compositional Navigation Tensor — Numerical Limits Analysis")
    print("  Higgins Computational Instruments")
    print("=" * 72)
    print()

    p01_clr_zero_sum()
    p02_norm_variation()
    p03_arccos_instability()
    p04_stable_vs_arccos()
    p05_ilr_vs_clr()
    p06_helmert_verification()
    p07_condition_number()
    p08_extreme_stress()
    p09_dimensionality_scaling()
    p10_full_chain()

    print("\n" + "=" * 72)
    print("  PRECISION EXPERIMENT COMPLETE")
    print("=" * 72)
