"""HCI-CNQ geometry primitives.

Aitchison closure, centred log-ratio, Helmert orthonormal contrast,
quaternion utilities (axis-angle, conjugate, Hamilton product, sandwich
rotation), and the rotation-quaternion-between-two-unit-vectors with
the atan2-stable axis/angle construction used throughout the framework.

Pure numpy. Functions are deterministic and side-effect-free.

Sign and basis conventions
--------------------------
1. Quaternions are stored as (w, x, y, z) — scalar first.
2. Helmert basis follows the convention used in QD_round_2.py
   (the legacy reference): row k has a (k+1)-block of 1/sqrt(k(k+1))
   followed by -k/sqrt(k(k+1)) and zeros. This matches the framework's
   existing CNT outputs and the published Backblaze/Planck residuals.
3. atan2-stable angle: angle = atan2(||cross||, dot). Always non-negative
   in [0, pi]. The rotation axis is cross(u1,u2)/||cross(u1,u2)|| with
   antiparallel fallback to a perpendicular construction.
"""
from __future__ import annotations

import math

import numpy as np


# ── Aitchison primitives ───────────────────────────────────────────────

def closure(x):
    """Aitchison closure: rescale a row to sum to 1.

    Args:
        x: 1-D array of strictly positive carriers.

    Returns:
        np.ndarray summing to 1.
    """
    x = np.asarray(x, dtype=float)
    return x / x.sum()


def clr(x):
    """Centred log-ratio of a closed (or unclosed but positive) row.

    clr(x)_i = log(x_i) - mean_j(log(x_j))

    The result sums to 0 by construction.
    """
    x = np.asarray(x, dtype=float)
    g = np.exp(np.log(x).mean())
    return np.log(x / g)


# ── Helmert orthonormal contrast ──────────────────────────────────────

def helmert_basis(D):
    """Return the (D-1) x D Helmert orthonormal contrast matrix.

    Each row is an orthonormal vector in R^D perpendicular to (1,1,...,1).
    Multiplying a CLR row vector by helmert_basis(D).T maps it from R^D
    (which sums to 0) into R^(D-1) (the ILR space).

    The convention here matches QD_round_2.py exactly so the residuals
    in this repo line up bit-identical with the legacy results.
    """
    H = np.zeros((D - 1, D))
    for k in range(D - 1):
        n = k + 1
        norm = 1.0 / math.sqrt(n * (n + 1))
        H[k, :n] = norm
        H[k, n] = -n * norm
    return H


def ilr_from_clr(clr_vector, H=None):
    """Project a CLR vector (sum-to-zero) into ILR space via Helmert basis.

    Args:
        clr_vector: 1-D array of length D, CLR-transformed and summing to 0.
        H: optional precomputed Helmert basis. If None, computed on demand.

    Returns:
        1-D array of length D-1 in ILR coordinates.
    """
    clr_vector = np.asarray(clr_vector, dtype=float)
    if H is None:
        H = helmert_basis(len(clr_vector))
    return clr_vector @ H.T


# ── Quaternion algebra ────────────────────────────────────────────────

def quat_from_axis_angle(axis, angle):
    """Unit quaternion (w, x, y, z) from rotation axis and angle (radians)."""
    axis = np.asarray(axis, dtype=float)
    n = np.linalg.norm(axis)
    if n < 1e-15:
        return np.array([1.0, 0.0, 0.0, 0.0])
    axis = axis / n
    half = angle / 2.0
    return np.array([
        math.cos(half),
        math.sin(half) * axis[0],
        math.sin(half) * axis[1],
        math.sin(half) * axis[2],
    ])


def quat_conj(q):
    """Quaternion conjugate."""
    q = np.asarray(q, dtype=float)
    return np.array([q[0], -q[1], -q[2], -q[3]])


def quat_mul(p, q):
    """Hamilton product of two quaternions stored (w, x, y, z)."""
    p0, p1, p2, p3 = p
    q0, q1, q2, q3 = q
    return np.array([
        p0 * q0 - p1 * q1 - p2 * q2 - p3 * q3,
        p0 * q1 + p1 * q0 + p2 * q3 - p3 * q2,
        p0 * q2 - p1 * q3 + p2 * q0 + p3 * q1,
        p0 * q3 + p1 * q2 - p2 * q1 + p3 * q0,
    ])


def quat_norm(q):
    """Quaternion norm sqrt(w^2 + x^2 + y^2 + z^2)."""
    return float(np.linalg.norm(q))


def quat_rotate(q, v):
    """Apply unit quaternion q to 3-vector v via the sandwich product.

    Returns the xyz part of (q . [0;v] . q*).
    """
    p = np.array([0.0, v[0], v[1], v[2]])
    rotated = quat_mul(quat_mul(q, p), quat_conj(q))
    return rotated[1:]


def rotation_quaternion_between(u1, u2, eps=1e-15):
    """Unit quaternion that rotates unit 3-vector u1 -> unit 3-vector u2.

    Uses the atan2-stable construction:
        angle = atan2(||cross||, dot)
        axis  = cross / ||cross||
    with the antiparallel fallback (dot ~ -1) picking a perpendicular axis.

    This matches QD_round_2.py exactly so the residuals reproduce the
    legacy Backblaze/Planck IEEE-floor results bit-for-bit.
    """
    u1 = np.asarray(u1, dtype=float)
    u2 = np.asarray(u2, dtype=float)
    u1 = u1 / np.linalg.norm(u1)
    u2 = u2 / np.linalg.norm(u2)
    dot = float(np.clip(np.dot(u1, u2), -1.0, 1.0))
    if dot > 1.0 - eps:
        return np.array([1.0, 0.0, 0.0, 0.0])
    if dot < -1.0 + eps:
        # antiparallel; pick any axis perpendicular to u1
        axis = np.cross(u1, np.array([1.0, 0.0, 0.0]))
        if np.linalg.norm(axis) < 1e-10:
            axis = np.cross(u1, np.array([0.0, 1.0, 0.0]))
        axis = axis / np.linalg.norm(axis)
        return quat_from_axis_angle(axis, math.pi)
    cross = np.cross(u1, u2)
    angle = math.atan2(np.linalg.norm(cross), dot)
    return quat_from_axis_angle(cross, angle)


# ── Composite operations used by the engine ───────────────────────────

def compositions_to_helmert_unit_vectors(rows, D):
    """Pipeline: closure -> CLR -> Helmert -> normalize to S^(D-2).

    Args:
        rows: iterable of D-vectors (positive carriers).
        D: explicit carrier dimension.

    Returns:
        (T, D-1) array of unit vectors, plus the (T,) array of radii
        before normalization. Useful for diagnostics.
    """
    closed = np.array([closure(r) for r in rows])
    clr_vecs = np.array([clr(c) for c in closed])
    H = helmert_basis(D)
    rN = clr_vecs @ H.T
    radii = np.linalg.norm(rN, axis=1)
    # Avoid divide-by-zero on degenerate rows (radius == 0 means
    # composition is the geometric centre — no direction).
    safe_radii = np.where(radii > 1e-15, radii, 1.0)
    units = rN / safe_radii[:, None]
    units[radii <= 1e-15] = 0.0
    return units, radii


def quaternion_sandwich_residuals(unit_vectors_3d):
    """For a (T, 3) array of unit vectors, compute per-step residuals
    between the next vector and the sandwich-product reconstruction.

    For each consecutive pair (u_t, u_{t+1}):
        q = rotation_quaternion_between(u_t, u_{t+1})
        u_reconstructed = quat_rotate(q, u_t)
        residual_t = max(|u_reconstructed - u_{t+1}|)

    Returns:
        residuals: (T-1,) array of L-infinity residuals per step.
        quaternions: (T-1, 4) array of per-step rotation quaternions.
        angles: (T-1,) array of rotation angles in radians.
    """
    units = np.asarray(unit_vectors_3d, dtype=float)
    T = units.shape[0]
    if T < 2:
        return np.zeros(0), np.zeros((0, 4)), np.zeros(0)

    residuals = np.zeros(T - 1)
    quats = np.zeros((T - 1, 4))
    angles = np.zeros(T - 1)
    for t in range(T - 1):
        q = rotation_quaternion_between(units[t], units[t + 1])
        u_rec = quat_rotate(q, units[t])
        residuals[t] = np.max(np.abs(u_rec - units[t + 1]))
        quats[t] = q
        angles[t] = 2.0 * math.atan2(np.linalg.norm(q[1:]), q[0])
    return residuals, quats, angles
