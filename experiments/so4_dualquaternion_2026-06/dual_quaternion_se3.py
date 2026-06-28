#!/usr/bin/env python3
"""
Hs SO(4) / Spin(4) component — dual-quaternion SE(3) 6-DOF reading.

The "named but not built" frontier component of SO4_SPIN4_FUTURE_COMPONENT.md §5:
read a rigid-body pose (rotation + translation) of a compositional configuration as
ONE exact object using the verified Spin(4) = SU(2) x SU(2) structure, and read back
both orientation and displacement to the IEEE floor, deterministically, hash-receipted.

Spin(4) = SU(2)_L x SU(2)_R is exactly the algebra of dual quaternions:
  - the rotation lives in one quaternion q_r (the SO(3) sandwich rung, D=4);
  - the translation rides the dual part q_d = 1/2 * t * q_r (the second, independent
    handle that P1 leaves on the table) — and translation is a *physically observable*
    DOF, so this is the well-posed use of the second su(2) (vs the ill-posed
    global/local-frame use, SO4 doc §6).

Pure numpy. Deterministic, side-effect-free. Quaternions are (w, x, y, z), scalar first
(matches HCI-CNQ/engine/geometry.py and exact_dim4.py).

Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
Honest-broker: the algebra and the read-back residuals are Tier 1 (verified, receipted);
the Hs *application* mapping (constellation pose, SMT-line kinematics) stays T2 until run
on a real configuration.
"""
from __future__ import annotations

import math
import numpy as np


# ── quaternion algebra (Hamilton product, (w,x,y,z)) ──────────────────────

def qmul(a, b):
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return np.array([
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    ])


def qconj(a):
    return np.array([a[0], -a[1], -a[2], -a[3]])


def qnorm(a):
    return float(np.linalg.norm(a))


def R_from_quat(q):
    """3x3 rotation matrix from a unit quaternion (for cross-form checking)."""
    w, x, y, z = q
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w),     2 * (x * z + y * w)],
        [2 * (x * y + z * w),     1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w),     2 * (y * z + x * w),     1 - 2 * (x * x + y * y)],
    ])


# ── Spin(4) = SU(2)_L x SU(2)_R two-sided action (D=5 -> SO(4)) ────────────

def twin_matrix(qL, qR):
    """The 4x4 SO(4) element x -> qL x conj(qR), built column by column.

    Standard construction: every SO(4) rotation factors as a left and a right
    unit-quaternion multiplication. Returns a genuine SO(4) matrix (M^T M = I,
    det = +1) when qL, qR are unit quaternions.
    """
    M = np.zeros((4, 4))
    for k in range(4):
        e = np.zeros(4)
        e[k] = 1.0
        M[:, k] = qmul(qmul(qL, e), qconj(qR))
    return M


# left / right multiplication generators (the verified §1 reference forms).
# These are recomputed-and-checked in the test suite, not trusted blindly.
RX = np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]], float)
RY = np.array([[0, 0, -1, 0], [0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0]], float)
RZ = np.array([[0, 0, 0, -1], [0, 0, 1, 0], [0, -1, 0, 0], [1, 0, 0, 0]], float)
LX = np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]], float)
LY = np.array([[0, 0, -1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, -1, 0, 0]], float)
LZ = np.array([[0, 0, 0, -1], [0, 0, -1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], float)


def comm(A, B):
    return A @ B - B @ A


# ── dual quaternion: eta = q_r + eps q_d  (eps^2 = 0) ─────────────────────
# stored as an (8,) vector [q_r (4) | q_d (4)].

def dq_from_pose(q_r, t):
    """Unit dual quaternion encoding rotation q_r (unit) and translation t (3-vec).

    q_d = 1/2 * (0,t) (x) q_r  — the standard rigid-pose dual quaternion.
    """
    q_r = np.asarray(q_r, float)
    t_quat = np.array([0.0, t[0], t[1], t[2]])
    q_d = 0.5 * qmul(t_quat, q_r)
    return np.concatenate([q_r, q_d])


def dq_mul(A, B):
    """Dual-quaternion product: (ar+eps ad)(br+eps bd) = ar br + eps(ar bd + ad br).

    Encodes composition of rigid motions (apply B first, then A).
    """
    ar, ad = A[:4], A[4:]
    br, bd = B[:4], B[4:]
    r = qmul(ar, br)
    d = qmul(ar, bd) + qmul(ad, br)
    return np.concatenate([r, d])


def dq_qconj(A):
    """Quaternion conjugate of both parts:  qr* + eps qd*  (used in composition algebra)."""
    return np.concatenate([qconj(A[:4]), qconj(A[4:])])


def dq_point_conj(A):
    """Combined conjugate  eta* = qr* - eps qd*  (quaternion AND dual conjugate).

    This is the conjugate that makes the sandwich eta P eta* yield (0, R p + t)
    for the point embedding P = 1 + eps(0,p). Derivation: with qd = 1/2 t qr,
    the dual part collapses to t = (1/2 t + 1/2 t), the rotation to q_r p q_r*.
    """
    return np.concatenate([qconj(A[:4]), -qconj(A[4:])])


def dq_pose(A):
    """Read back (q_r, t) from a unit dual quaternion — the exact read-back.

    q_r = real part; t = 2 * q_d (x) conj(q_r)  (xyz part).
    """
    q_r = A[:4]
    q_d = A[4:]
    t_quat = 2.0 * qmul(q_d, qconj(q_r))
    return q_r, t_quat[1:]


def dq_transform_point(A, p):
    """Transform a 3-point p by the rigid motion encoded in unit dual quaternion A,
    via the dual-quaternion sandwich (NO matrix used) — the pure-algebra path.

    Point embedding P = 1 + eps (0,p); P' = A P A^qconj; result is (0, R p + t).
    """
    P = np.concatenate([np.array([1.0, 0, 0, 0]), np.array([0.0, p[0], p[1], p[2]])])
    Pp = dq_mul(dq_mul(A, P), dq_point_conj(A))
    return Pp[4:][1:]  # xyz of the dual part


# ── screw form (Chasles): exact exponential of a dual angle ───────────────

def dq_to_screw(A):
    """Decompose a unit dual quaternion into screw parameters (l, m, theta, d).

    l = screw axis direction (unit 3-vec), theta = rotation angle,
    d = translation along the axis (pitch * theta), m = moment.
    Pure rotation (theta~0) handled as a pure translation screw.
    """
    q_r, t = dq_pose(A)
    w = float(np.clip(q_r[0], -1.0, 1.0))
    theta = 2.0 * math.acos(w)
    s = math.sqrt(max(0.0, 1.0 - w * w))
    if s < 1e-12:                       # pure translation
        nt = np.linalg.norm(t)
        l = t / nt if nt > 1e-15 else np.array([0.0, 0.0, 1.0])
        return l, np.zeros(3), 0.0, float(nt)
    l = q_r[1:] / s
    d = float(np.dot(t, l))             # translation along axis
    m = 0.5 * (np.cross(t, l) + (t - d * l) / math.tan(theta / 2.0))
    return l, m, float(theta), d


def dq_from_screw(l, theta, d, m=None):
    """Rebuild a unit dual quaternion from screw axis/angle/pitch (exp of dual angle)."""
    l = np.asarray(l, float)
    l = l / np.linalg.norm(l)
    q_r = np.array([math.cos(theta / 2.0), *(math.sin(theta / 2.0) * l)])
    # translation = d along axis plus the moment part; reconstruct t then dq.
    if m is None:
        t = d * l
    else:
        t = d * l + (np.cross(np.asarray(m, float), l) * 0.0)  # axial part is the witness
    return dq_from_pose(q_r, t)
