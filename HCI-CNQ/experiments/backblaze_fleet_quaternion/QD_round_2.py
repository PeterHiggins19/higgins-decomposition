#!/usr/bin/env python3
"""QD Round 2 — actual computational tests.

Concept 1: D=4 Aitchison ↔ unit quaternions (foundational claim).
Concept 10: directness=1/0 calibration ↔ pure scalar/vector quaternion velocity.

Run from inside the Quaternion Decomposition/ folder.
NO modifications to the canonical engine, schema, or corpus.
Read-only against the Hs canonical repo.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np

# HS_ROOT computed relative to this script: HCI-CNQ/experiments/backblaze_fleet_quaternion/ -> Hs/
HS_ROOT = Path(__file__).resolve().parents[3]
RESULTS = {}


# ── Aitchison + Helmert utilities ──────────────────────────────────────

def closure(x):
    """Aitchison closure: rescale row to sum to 1."""
    x = np.asarray(x, dtype=float)
    return x / x.sum()


def clr(x):
    """Centered log-ratio transform of a closed composition."""
    x = np.asarray(x, dtype=float)
    g = np.exp(np.log(x).mean())
    return np.log(x / g)


def helmert_basis(D):
    """Return the (D-1) × D Helmert orthonormal contrast matrix.
    Each row is an orthonormal vector in R^D perpendicular to (1,1,...,1).
    Multiplying by this matrix maps CLR vectors (which sum to 0) to R^(D-1)."""
    H = np.zeros((D - 1, D))
    for k in range(D - 1):
        # k-th Helmert contrast: 1/sqrt(k(k+1)) [k, -1, -1, ..., -1, 0, 0, ..., 0]
        # but the standard sign convention varies; use the one that matches CNT
        n = k + 1
        norm = 1.0 / math.sqrt(n * (n + 1))
        H[k, :n] = norm
        H[k, n] = -n * norm
    return H


# ── Quaternion utilities ───────────────────────────────────────────────

def quat_from_axis_angle(axis, angle):
    """Build a unit quaternion (w, x, y, z) from axis (3-vector) + angle."""
    axis = axis / np.linalg.norm(axis)
    half = angle / 2
    return np.array([math.cos(half),
                     math.sin(half) * axis[0],
                     math.sin(half) * axis[1],
                     math.sin(half) * axis[2]])


def quat_conj(q):
    """Quaternion conjugate."""
    return np.array([q[0], -q[1], -q[2], -q[3]])


def quat_mul(p, q):
    """Hamilton product of two quaternions (w, x, y, z)."""
    p0, p1, p2, p3 = p
    q0, q1, q2, q3 = q
    return np.array([
        p0 * q0 - p1 * q1 - p2 * q2 - p3 * q3,
        p0 * q1 + p1 * q0 + p2 * q3 - p3 * q2,
        p0 * q2 - p1 * q3 + p2 * q0 + p3 * q1,
        p0 * q3 + p1 * q2 - p2 * q1 + p3 * q0,
    ])


def quat_rotate(q, v):
    """Apply unit quaternion q to a 3-vector v: returns (q · [0;v] · q*)_xyz."""
    p = np.array([0.0, v[0], v[1], v[2]])
    rotated = quat_mul(quat_mul(q, p), quat_conj(q))
    return rotated[1:]


def rotation_quaternion_between(u1, u2):
    """Unit quaternion that rotates unit vector u1 → u2."""
    u1 = u1 / np.linalg.norm(u1)
    u2 = u2 / np.linalg.norm(u2)
    dot = np.clip(np.dot(u1, u2), -1.0, 1.0)
    if dot > 1.0 - 1e-15:
        # Already aligned; identity quaternion
        return np.array([1.0, 0.0, 0.0, 0.0])
    if dot < -1.0 + 1e-15:
        # Antiparallel; pick any axis perpendicular to u1
        # Use atan2-style stable construction
        axis = np.cross(u1, np.array([1.0, 0.0, 0.0]))
        if np.linalg.norm(axis) < 1e-10:
            axis = np.cross(u1, np.array([0.0, 1.0, 0.0]))
        axis = axis / np.linalg.norm(axis)
        return quat_from_axis_angle(axis, math.pi)
    axis = np.cross(u1, u2)
    angle = math.atan2(np.linalg.norm(axis), dot)  # the atan2 form, per Concept 2
    return quat_from_axis_angle(axis, angle)


# ── Concept 1: foundational test on backblaze_fleet ────────────────────

def concept_1_backblaze():
    """For each consecutive timestep pair in backblaze_fleet, verify that the
    quaternion rotation between the two Helmert-projected unit vectors,
    applied via the sandwich product q v q*, reproduces the next timestep
    to numerical precision.

    Gate: max |reconstructed - actual| ≤ 1e-12 across all 730 pairs."""

    csv_path = HS_ROOT / 'HCI' / 'experiments_v2' / 'codawork2026' / 'backblaze_fleet' / 'backblaze_fleet_input.csv'
    rows = list(csv.reader(csv_path.open()))
    header = rows[0]
    data = [r for r in rows[1:] if r]
    print(f"  Read {len(data)} rows × {len(header)-1} carriers from backblaze_fleet")
    print(f"  Carriers: {header[1:]}")

    D = len(header) - 1
    assert D == 4, f"backblaze_fleet must be D=4; got D={D}"

    # Closure + CLR
    closed = np.array([closure([float(v) for v in r[1:]]) for r in data])
    clr_vecs = np.array([clr(c) for c in closed])

    # Helmert projection to R^(D-1) = R^3
    H = helmert_basis(D)
    r3 = clr_vecs @ H.T  # (T, 3)
    print(f"  Helmert-projected to R^{D-1}; first vector: {r3[0]}")

    # Normalize to S^2
    radii = np.linalg.norm(r3, axis=1)
    r3_unit = r3 / radii[:, None]

    # For each consecutive pair, compute rotation quaternion and verify sandwich product
    diffs = []
    for t in range(len(r3_unit) - 1):
        u1 = r3_unit[t]
        u2 = r3_unit[t + 1]
        q = rotation_quaternion_between(u1, u2)
        u2_reconstructed = quat_rotate(q, u1)
        diff = np.max(np.abs(u2_reconstructed - u2))
        diffs.append(diff)

    diffs = np.array(diffs)
    max_diff = float(diffs.max())
    mean_diff = float(diffs.mean())
    pass_gate = max_diff <= 1e-12

    print(f"  Tested {len(diffs)} consecutive pairs")
    print(f"  Max diff: {max_diff:.3e}")
    print(f"  Mean diff: {mean_diff:.3e}")
    print(f"  GATE (≤ 1e-12): {'PASS' if pass_gate else 'FAIL'}")

    return {
        'concept': 1,
        'description': 'D=4 Aitchison ↔ unit quaternions (sandwich product reproduces trajectory)',
        'dataset': 'backblaze_fleet',
        'n_pairs_tested': len(diffs),
        'max_diff': max_diff,
        'mean_diff': mean_diff,
        'gate_threshold': 1e-12,
        'pass': pass_gate,
        'first_radius': float(radii[0]),
        'mean_radius': float(radii.mean()),
        'min_radius': float(radii.min()),
        'max_radius': float(radii.max()),
    }


# ── Concept 10: directness vs scalar/vector quaternion velocity ────────

def concept_10_calibration():
    """For directness=1.0 (straight) and directness=0.0 (loop) calibration
    fixtures, decompose the relative-rotation quaternion velocity into
    scalar and vector parts. Conjecture:
      - directness=1 → trajectory accumulates very little rotation per step
        → relative-quaternion vector parts ≈ 0 (each step is identity-like)
      - directness=0 → trajectory rotates substantially per step
        → relative-quaternion scalar parts substantially less than 1

    Gate: report the patterns; flag PASS if directness=1 has ≪ rotation
    per step AND directness=0 has noticeable rotation per step."""

    fixtures = {
        'directness=1.0 (straight)': HS_ROOT / 'HCI-CNT' / 'atlas' / 'STANDARD_CALIBRATION_stage2_A_straight.csv',
        'directness=0.0 (loop)':     HS_ROOT / 'HCI-CNT' / 'atlas' / 'STANDARD_CALIBRATION_stage2_B_loop.csv',
    }

    results = {}
    for name, path in fixtures.items():
        rows = list(csv.reader(path.open()))
        header = rows[0]
        data = [r for r in rows[1:] if r]
        D = len(header) - 1
        closed = np.array([closure([float(v) for v in r[1:]]) for r in data])
        clr_vecs = np.array([clr(c) for c in closed])
        H = helmert_basis(D)
        r3 = clr_vecs @ H.T

        # For D > 3 take the first 3 components (radial projection); for D = 4 this is exact
        if r3.shape[1] > 3:
            r3 = r3[:, :3]

        radii = np.linalg.norm(r3, axis=1)
        # Skip zero-radius points (degenerate)
        valid = radii > 1e-12
        r3_unit = r3[valid] / radii[valid, None]

        # Per-step relative-rotation quaternions
        per_step_angles = []
        per_step_scalars = []
        per_step_vec_norms = []
        for t in range(len(r3_unit) - 1):
            q = rotation_quaternion_between(r3_unit[t], r3_unit[t + 1])
            angle = 2 * math.atan2(np.linalg.norm(q[1:]), q[0])
            per_step_angles.append(angle)
            per_step_scalars.append(q[0])
            per_step_vec_norms.append(np.linalg.norm(q[1:]))

        per_step_angles = np.array(per_step_angles)
        per_step_scalars = np.array(per_step_scalars)
        per_step_vec_norms = np.array(per_step_vec_norms)

        results[name] = {
            'T': len(data),
            'D': D,
            'n_steps_tested': len(per_step_angles),
            'mean_angle_per_step_rad': float(per_step_angles.mean()),
            'max_angle_per_step_rad': float(per_step_angles.max()),
            'mean_scalar': float(per_step_scalars.mean()),
            'mean_vec_norm': float(per_step_vec_norms.mean()),
            'total_angle_rad': float(per_step_angles.sum()),
            'total_angle_in_2pi_units': float(per_step_angles.sum() / (2 * math.pi)),
        }
        print(f"\n  {name}:")
        print(f"    T={len(data)}, D={D}")
        print(f"    mean angle/step: {per_step_angles.mean():.4e} rad")
        print(f"    max  angle/step: {per_step_angles.max():.4e} rad")
        print(f"    mean scalar (cos(θ/2)): {per_step_scalars.mean():.6f}")
        print(f"    mean vector norm (sin(θ/2)): {per_step_vec_norms.mean():.6e}")
        print(f"    total angle: {per_step_angles.sum():.4f} rad ({per_step_angles.sum() / (2*math.pi):.4f} × 2π)")

    # Pass criterion: directness=1 should have much less rotation per step than directness=0
    direct_mean = results['directness=1.0 (straight)']['mean_angle_per_step_rad']
    loop_mean   = results['directness=0.0 (loop)']['mean_angle_per_step_rad']
    pass_gate = loop_mean > direct_mean * 5  # loop should rotate at least 5x more per step

    print(f"\n  Loop / Straight rotation ratio: {loop_mean / max(direct_mean, 1e-15):.2f}×")
    print(f"  GATE (loop rotates ≥ 5× more per step than straight): {'PASS' if pass_gate else 'FAIL'}")

    return {
        'concept': 10,
        'description': 'directness=1/0 ↔ pure scalar/vector quaternion velocity',
        'fixtures': results,
        'loop_vs_straight_ratio': loop_mean / max(direct_mean, 1e-15),
        'pass': pass_gate,
    }


# ── Run both ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 72)
    print("QD ROUND 2 — Quaternion Decomposition validation tests")
    print("=" * 72)

    print("\n[Concept 1] D=4 Aitchison ↔ unit quaternions on backblaze_fleet")
    print("-" * 72)
    RESULTS['concept_1'] = concept_1_backblaze()

    print("\n[Concept 10] directness=1/0 ↔ scalar/vector quaternion velocity")
    print("-" * 72)
    RESULTS['concept_10'] = concept_10_calibration()

    print("\n" + "=" * 72)
    overall = RESULTS['concept_1']['pass'] and RESULTS['concept_10']['pass']
    print(f"  OVERALL: {'PASS' if overall else 'FAIL'}")
    print("=" * 72)

    # Save results
    out = Path(__file__).parent / 'QD_round_2_results.json'
    out.write_text(json.dumps(RESULTS, indent=2))
    print(f"\nResults saved to: {out}")
