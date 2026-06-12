"""
hci_shared.geometry — compositional algebra + quaternion algebra primitives

This module provides the mathematical operators used by the CNT v3 and CNQ v2
engines. Conventions follow Aitchison-Egozcue compositional data analysis
plus standard 3-D rotation algebra via unit quaternions:

    closure       : positive vector  ->  probability simplex
    clr           : centred log-ratio (closure-invariant Euclidean view)
    helmert_basis : orthonormal contrast matrix; rows form an orthonormal
                    basis of the (D-1)-dim subspace orthogonal to the all-ones
                    vector in R^D
    ilr           : isometric log-ratio = CLR  followed by  Helmert projection;
                    image is R^(D-1) Euclidean

The Helmert convention used here is the same as the legacy QD_round_2.py and
CNQ v1.0.0 conventions:

    H[k, :k+1] =  +1 / sqrt((k+1)*(k+2))   for k in range(D-1) and j in range(k+1)
    H[k, k+1] = -(k+1) / sqrt((k+1)*(k+2))

So row k has (k+1) entries of `+1/sqrt(n*(n+1))` followed by one entry
`-(k+1)/sqrt(n*(n+1))` at column (k+1), where n = k+1. Trailing columns
(k+2 .. D-1) are zero. Rows are orthonormal: H @ H.T = I_{D-1}.

Quaternion conventions (scalar-first, Hamilton product):

    q = (q_w, q_x, q_y, q_z)
    p * q  = Hamilton product, non-commutative
    q*     = (q_w, -q_x, -q_y, -q_z) is the conjugate
    rotate(q, v) = q * (0, v) * q*  for unit q and 3-vector v

These match Diebel 2006 and standard graphics / robotics conventions.

Atan2-stable rotation between unit 3-vectors:

    rotation_quaternion_between(u1, u2)

is built via atan2(||cross||, dot) for the rotation angle, with explicit
parallel and antiparallel branches. The eps threshold is 1e-15 by default
(machine epsilon for float64).
"""

from __future__ import annotations

from typing import Tuple

import numpy as np

from hci_shared.validation import (
    InvalidInputError,
    validate_dimension,
    validate_rows,
)


# ---------------------------------------------------------------------------
# Compositional algebra: closure, CLR, Helmert basis, ILR
# ---------------------------------------------------------------------------


def closure(x: np.ndarray, *, delta: float = 1e-15) -> np.ndarray:
    """Close a positive 1-D or 2-D array onto the probability simplex.

    For a 1-D input of length D, returns x / sum(x).
    For a 2-D input of shape (T, D), returns each row / its row sum.

    Parameters
    ----------
    x : array-like
        Positive values. Must be strictly positive (use validate_rows
        with allow_zero=False upstream to enforce this).
    delta : float, default 1e-15
        Floor applied to the row sum to avoid division by zero. If a row
        sum is below delta, the row is left unchanged (this is a defensive
        fallback; in practice validators upstream should reject such rows).

    Returns
    -------
    np.ndarray
        Same shape as `x`, with rows summing to 1.

    Notes
    -----
    Closure is the canonical map onto the simplex. It is idempotent
    (closure(closure(x)) == closure(x)) and scale-invariant
    (closure(k*x) == closure(x) for any k > 0).
    """

    arr = np.asarray(x, dtype=np.float64)

    if arr.ndim == 1:
        s = arr.sum()
        if s <= delta:
            return arr.copy()
        return arr / s

    if arr.ndim == 2:
        sums = arr.sum(axis=1, keepdims=True)
        # Where sums are tiny, fall back to identity (validator should have
        # caught this; this guard prevents NaN propagation in pathological
        # cases that bypass validation).
        sums = np.where(sums > delta, sums, 1.0)
        return arr / sums

    raise InvalidInputError(
        f"closure expects 1-D or 2-D input, got ndim={arr.ndim}"
    )


def clr(x: np.ndarray) -> np.ndarray:
    """Centred log-ratio transform.

    For a vector x in the simplex, clr(x)_i = log(x_i / g(x)) where g(x)
    is the geometric mean. The CLR vector lies in the hyperplane sum=0 of
    R^D (the codomain of CLR is the (D-1)-dim subspace orthogonal to the
    all-ones direction).

    Properties:
        * sum(clr(x)) = 0  exactly (zero-mean)
        * clr(closure(k*x)) = clr(closure(x)) for k > 0  (scale-invariant)
        * clr is an isometry from the simplex (with Aitchison metric) to
          this zero-mean hyperplane (with Euclidean metric)

    Parameters
    ----------
    x : array-like
        Positive values, 1-D (D,) or 2-D (T, D). Must be strictly positive.

    Returns
    -------
    np.ndarray
        Same shape as `x`, with each row's CLR transform.
    """

    arr = np.asarray(x, dtype=np.float64)

    if arr.ndim == 1:
        log_x = np.log(arr)
        return log_x - log_x.mean()

    if arr.ndim == 2:
        log_x = np.log(arr)
        # Per-row geometric mean = mean of logs; broadcast subtraction.
        return log_x - log_x.mean(axis=1, keepdims=True)

    raise InvalidInputError(
        f"clr expects 1-D or 2-D input, got ndim={arr.ndim}"
    )


def helmert_basis(D: int) -> np.ndarray:
    """Orthonormal Helmert contrast matrix of shape (D-1, D).

    Each row k (for k = 0 .. D-2) is built as:

        H[k, j]   = +1 / sqrt(n*(n+1))   for j = 0 .. k
        H[k, k+1] = -n / sqrt(n*(n+1))
        H[k, j]   = 0                    for j > k+1

    where n = k + 1.

    The result satisfies:
        * H @ H.T = I_{D-1}        (rows are orthonormal)
        * H @ ones(D) = zeros(D-1) (rows orthogonal to all-ones)

    H provides the canonical isometric map from the CLR-zero-mean hyperplane
    to R^(D-1). Composing CLR with H gives the ILR transform.

    Parameters
    ----------
    D : int
        Number of carriers, D >= 2.

    Returns
    -------
    np.ndarray
        Helmert basis of shape (D-1, D).
    """

    D = validate_dimension(D, min_d=2)

    H = np.zeros((D - 1, D), dtype=np.float64)
    for k in range(D - 1):
        n = k + 1
        norm = 1.0 / np.sqrt(n * (n + 1))
        H[k, : n] = norm
        H[k, n] = -n * norm

    return H


def ilr_from_clr(clr_vec: np.ndarray, H: np.ndarray | None = None) -> np.ndarray:
    """Project a CLR vector (or batch of CLR vectors) into ILR space via H.

    The ILR transform is just CLR followed by an orthonormal contrast
    projection. With the Helmert basis from `helmert_basis`, the result
    is the canonical isometric image of the simplex in R^(D-1).

    Parameters
    ----------
    clr_vec : array-like
        CLR vectors, shape (D,) or (T, D).
    H : np.ndarray or None
        Helmert basis of shape (D-1, D). If None, computed automatically
        from D = clr_vec.shape[-1].

    Returns
    -------
    np.ndarray
        ILR coordinates, shape (D-1,) or (T, D-1).
    """

    clr_arr = np.asarray(clr_vec, dtype=np.float64)
    D = clr_arr.shape[-1]

    if H is None:
        H = helmert_basis(D)
    elif H.shape != (D - 1, D):
        raise InvalidInputError(
            f"ilr_from_clr: H shape {H.shape} does not match D={D} "
            f"(expected ({D-1}, {D}))"
        )

    if clr_arr.ndim == 1:
        return H @ clr_arr  # (D-1,)
    return clr_arr @ H.T  # (T, D-1)


def compositions_to_ilr(
    rows: np.ndarray, D: int | None = None
) -> Tuple[np.ndarray, np.ndarray]:
    """Full pipeline: rows -> closure -> CLR -> ILR.

    Parameters
    ----------
    rows : array-like
        Compositional rows, shape (T, D), strictly positive.
    D : int or None
        Carrier count; inferred from rows.shape[1] if None.

    Returns
    -------
    ilr : np.ndarray
        ILR coordinates, shape (T, D-1).
    radii : np.ndarray
        Per-row Euclidean norm of the ILR vector, shape (T,). The radial
        trajectory in ILR space — preserves magnitude information that the
        bearing trajectory (unit-vector view) discards.
    """

    rows_validated = validate_rows(rows, min_carriers=2)
    if D is None:
        D = rows_validated.shape[1]
    elif D != rows_validated.shape[1]:
        raise InvalidInputError(
            f"compositions_to_ilr: D={D} does not match rows.shape[1]"
            f"={rows_validated.shape[1]}"
        )

    closed = closure(rows_validated)
    clr_vecs = clr(closed)
    H = helmert_basis(D)
    ilr = clr_vecs @ H.T
    radii = np.linalg.norm(ilr, axis=1)

    return ilr, radii


def compositions_to_helmert_unit_vectors(
    rows: np.ndarray, D: int | None = None, *, eps: float = 1e-15
) -> Tuple[np.ndarray, np.ndarray]:
    """Pipeline: rows -> closure -> CLR -> ILR -> unit vectors in R^(D-1).

    The unit vectors live on the unit sphere S^(D-2) in ILR space. Together
    with the radii returned separately, they reconstruct the full ILR
    trajectory (bearing + radial decomposition).

    Rows whose ILR norm is below `eps` (i.e., rows at or near the
    compositional centroid) are returned as zero vectors; callers should
    flag these as degenerate steps and skip quaternion sandwich operations
    on them.

    Parameters
    ----------
    rows : array-like
        Compositional rows, shape (T, D), strictly positive.
    D : int or None
        Carrier count; inferred from rows.shape[1] if None.
    eps : float, default 1e-15
        Threshold below which the radial norm is considered degenerate.

    Returns
    -------
    units : np.ndarray
        Unit vectors in R^(D-1), shape (T, D-1).
    radii : np.ndarray
        Pre-normalisation radii, shape (T,).
    """

    ilr, radii = compositions_to_ilr(rows, D)
    safe = radii > eps
    units = np.zeros_like(ilr)
    units[safe] = ilr[safe] / radii[safe, None]
    return units, radii


def ilr_norms(rows: np.ndarray, D: int | None = None) -> np.ndarray:
    """Compute the per-step ILR-space radial norm trajectory.

    Convenience function for engines that need only the radial trajectory
    (the magnitude side of the bearing/radial decomposition). Equivalent
    to the second return of `compositions_to_ilr`.

    Returns
    -------
    np.ndarray
        Radii, shape (T,).
    """

    _, radii = compositions_to_ilr(rows, D)
    return radii


# ---------------------------------------------------------------------------
# Quaternion algebra (scalar-first, Hamilton convention)
# ---------------------------------------------------------------------------


def quat_from_axis_angle(axis: np.ndarray, angle: float) -> np.ndarray:
    """Construct a unit quaternion from a 3-axis and rotation angle.

    Returns q = (cos(angle/2), sin(angle/2)*ax, sin(angle/2)*ay,
    sin(angle/2)*az) where (ax, ay, az) is the unit-normalised axis.

    Returns the identity quaternion (1, 0, 0, 0) if the axis norm is below
    1e-15 (degenerate rotation).
    """

    axis = np.asarray(axis, dtype=np.float64)
    if axis.shape != (3,):
        raise InvalidInputError(
            f"quat_from_axis_angle: axis must be 3-vector, got shape {axis.shape}"
        )

    norm = np.linalg.norm(axis)
    if norm < 1e-15:
        return np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)

    unit_axis = axis / norm
    half = angle / 2.0
    s = np.sin(half)
    return np.array(
        [np.cos(half), s * unit_axis[0], s * unit_axis[1], s * unit_axis[2]],
        dtype=np.float64,
    )


def quat_conj(q: np.ndarray) -> np.ndarray:
    """Quaternion conjugate: (w, x, y, z) -> (w, -x, -y, -z)."""

    q = np.asarray(q, dtype=np.float64)
    return np.array([q[0], -q[1], -q[2], -q[3]], dtype=np.float64)


def quat_mul(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Hamilton product p * q.

    Non-commutative; p*q != q*p in general. The product corresponds to
    composition of rotations: rotate-by-q, then rotate-by-p.
    """

    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)

    pw, px, py, pz = p
    qw, qx, qy, qz = q

    return np.array(
        [
            pw * qw - px * qx - py * qy - pz * qz,
            pw * qx + px * qw + py * qz - pz * qy,
            pw * qy - px * qz + py * qw + pz * qx,
            pw * qz + px * qy - py * qx + pz * qw,
        ],
        dtype=np.float64,
    )


def quat_norm(q: np.ndarray) -> float:
    """Quaternion magnitude sqrt(w^2 + x^2 + y^2 + z^2)."""

    q = np.asarray(q, dtype=np.float64)
    return float(np.linalg.norm(q))


def quat_rotate(q: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Rotate 3-vector v by unit quaternion q via the sandwich product.

    Computes q * (0, v) * q* and returns the imaginary part as a 3-vector.
    Caller should ensure q is a unit quaternion; non-unit q produces a
    rotation-and-scale, not a pure rotation.

    Parameters
    ----------
    q : array-like
        Unit quaternion, shape (4,).
    v : array-like
        3-vector to rotate, shape (3,).

    Returns
    -------
    np.ndarray
        Rotated 3-vector, shape (3,).
    """

    q = np.asarray(q, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)

    if v.shape != (3,):
        raise InvalidInputError(
            f"quat_rotate: v must be 3-vector, got shape {v.shape}"
        )

    v_quat = np.array([0.0, v[0], v[1], v[2]], dtype=np.float64)
    rotated = quat_mul(quat_mul(q, v_quat), quat_conj(q))
    return rotated[1:]  # imaginary part


def rotation_quaternion_between(
    u1: np.ndarray, u2: np.ndarray, *, eps: float = 1e-15
) -> np.ndarray:
    """Atan2-stable rotation quaternion mapping u1 to u2.

    Both inputs must be unit 3-vectors. Returns q such that
    `quat_rotate(q, u1) == u2` to within IEEE-754 tolerance for non-degenerate
    inputs.

    Implementation:
        * Compute dot = u1 . u2 and cross = u1 x u2.
        * If ||cross|| < eps:
            - If dot > 0: vectors aligned, return identity.
            - Else: vectors antiparallel, build a 180-degree rotation
              around any axis perpendicular to u1. Picks `cross(u1, ex)`
              when |u1.x| < 0.9, otherwise `cross(u1, ey)`.
        * Otherwise compute angle = atan2(||cross||, dot), axis = cross/||cross||,
          and build q via quat_from_axis_angle.

    The atan2 formulation is more numerically stable than the half-angle
    cosine formula for vectors near the antiparallel pole.

    Parameters
    ----------
    u1, u2 : array-like
        Unit 3-vectors. Caller is responsible for normalisation; if either
        has non-unit magnitude, the resulting quaternion may not be a pure
        rotation.
    eps : float, default 1e-15
        Threshold below which the cross-product magnitude is treated as
        degenerate (parallel/antiparallel branch).

    Returns
    -------
    np.ndarray
        Unit quaternion, shape (4,), scalar-first.
    """

    u1 = np.asarray(u1, dtype=np.float64)
    u2 = np.asarray(u2, dtype=np.float64)

    if u1.shape != (3,) or u2.shape != (3,):
        raise InvalidInputError(
            f"rotation_quaternion_between: inputs must be 3-vectors, got "
            f"{u1.shape} and {u2.shape}"
        )

    dot = float(np.dot(u1, u2))
    cross = np.cross(u1, u2)
    cross_norm = float(np.linalg.norm(cross))

    if cross_norm < eps:
        if dot > 0:
            # Aligned: identity rotation.
            return np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        # Antiparallel: 180-degree rotation around any perpendicular axis.
        ex = np.array([1.0, 0.0, 0.0])
        ey = np.array([0.0, 1.0, 0.0])
        if abs(u1[0]) < 0.9:
            axis = np.cross(u1, ex)
        else:
            axis = np.cross(u1, ey)
        axis_norm = np.linalg.norm(axis)
        if axis_norm < eps:
            # u1 is approximately parallel to BOTH ex and ey; impossible
            # in 3D for a unit vector unless u1 is degenerate. Fallback:
            # use ez.
            axis = np.cross(u1, np.array([0.0, 0.0, 1.0]))
            axis_norm = np.linalg.norm(axis)
        axis = axis / axis_norm
        # 180-degree rotation: cos(pi/2) = 0, sin(pi/2) = 1
        return np.array([0.0, axis[0], axis[1], axis[2]], dtype=np.float64)

    angle = np.arctan2(cross_norm, dot)
    axis = cross / cross_norm
    return quat_from_axis_angle(axis, angle)


def quaternion_sandwich_residuals(
    unit_vectors_3d: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute per-step quaternion sandwich residuals along a 3-D trajectory.

    For each consecutive pair (u_t, u_{t+1}) of unit 3-vectors, build the
    rotation quaternion q_t = rotation_quaternion_between(u_t, u_{t+1}),
    apply the sandwich product to u_t, and measure the L-infinity residual
    against u_{t+1}.

    For non-degenerate inputs the residuals should be at or near the IEEE
    machine epsilon (~ 4.44e-16) — this is a numerical sanity check on the
    quaternion arithmetic and the rotation_quaternion_between construction;
    it is NOT a discriminator between competing physical or compositional
    theories. Use it for engine numerical health, not for engineering
    verdicts.

    Parameters
    ----------
    unit_vectors_3d : np.ndarray
        Unit 3-vectors, shape (T, 3). Caller ensures unit normalisation.

    Returns
    -------
    residuals : np.ndarray
        L-infinity residuals, shape (T-1,). residuals[t] = max(|q_t v q_t* - u_{t+1}|).
    quats : np.ndarray
        Per-step quaternions, shape (T-1, 4).
    angles : np.ndarray
        Per-step rotation angles in radians, shape (T-1,). Computed via
        2 * atan2(||q_xyz||, q_w).
    """

    arr = np.asarray(unit_vectors_3d, dtype=np.float64)

    if arr.ndim != 2 or arr.shape[1] != 3:
        raise InvalidInputError(
            f"quaternion_sandwich_residuals: expected (T, 3), got {arr.shape}"
        )

    T = arr.shape[0]
    if T < 2:
        return (
            np.zeros((0,), dtype=np.float64),
            np.zeros((0, 4), dtype=np.float64),
            np.zeros((0,), dtype=np.float64),
        )

    residuals = np.empty(T - 1, dtype=np.float64)
    quats = np.empty((T - 1, 4), dtype=np.float64)
    angles = np.empty(T - 1, dtype=np.float64)

    for t in range(T - 1):
        u1 = arr[t]
        u2 = arr[t + 1]
        q = rotation_quaternion_between(u1, u2)
        quats[t] = q
        u_rotated = quat_rotate(q, u1)
        residuals[t] = np.max(np.abs(u_rotated - u2))
        angles[t] = 2.0 * np.arctan2(np.linalg.norm(q[1:]), q[0])

    return residuals, quats, angles
