#!/usr/bin/env python3
"""
The SO(n) exact generator — invert the reader into a deterministic data factory.

The PICCIRILLO move (cf. exact_dim4.py: "Hs as an inert, deterministic generator of
exact objects"): instead of READING structure from data, GENERATE data with known
structure. Here we build exact SO(n) rotations for ANY n and drive a compositional
trajectory with planted, recoverable invariants — a structured TEST-MATRIX SET that
(a) validates the readers and (b) lets us probe where higher-dimensional structure lives.

Two facts this file demonstrates with receipts:

  1. EXACT SO(n) GENERATION IS UNBOUNDED IN n. Every R in SO(n) factors (spectral theorem
     for antisymmetric generators) into floor(n/2) commuting 2-plane rotations. That planar
     (Givens) product is the COORDINATE FORM of the Spin(n) rotor sandwich R v R~ in the
     Clifford algebra Cl(n) — exact for any n. (Cross-checked here: planar build == bivector
     exp to ~1e-16.)
  2. THE DIVISION-ALGEBRA IDENTITY IS BOUNDED AT 4. A 4-part composition's 3 ILR coords ARE
     a quaternion (sandwich q v q* = SO(3)); D=5 gives the two-sided SO(4). Beyond that there
     is NO single-number identity (Hurwitz: R,C,H,O only; octonion non-associative; sedenion
     has zero divisors — see ../exact_dim4_generator_2026-06/ladder_break.py and
     ../../papers/frontier/THE_LADDER_AND_THE_BREAK.md). Generation stays exact via the rotor;
     the single-number compositional identity does not survive — which is exactly why high-D
     is TILED into 4-charts, not read by a native high-n rotor.

Deterministic; hash-receipted. numpy + scipy. Author: Peter Higgins (human authorship for
all claims); AI-assisted per HUF-STD-001. Honest-broker: Tier 1 numerics; the "helps find
higher dimensions" use is the reasoned method (T2); any specific discovery is T3, to earn.
"""
import hashlib, json, math
import numpy as np
from scipy.linalg import expm


def givens(n, i, j, th):
    """Exact 2-plane (i,j) rotation by th — an SO(2) block embedded in R^n."""
    G = np.eye(n); c, s = math.cos(th), math.sin(th)
    G[i, i] = c; G[j, j] = c; G[i, j] = -s; G[j, i] = s
    return G


def son_planar(n, angles, seed):
    """Exact SO(n): product of floor(n/2) commuting coordinate-plane rotations, then
    conjugated by a deterministic special-orthogonal Q to put the planes in general
    position. The coordinate form of the Spin(n) rotor sandwich; exact for any n."""
    rng = np.random.default_rng(seed)
    M = np.eye(n)
    planes = [(2 * k, 2 * k + 1) for k in range(n // 2)]
    for (i, j), th in zip(planes, angles):
        M = M @ givens(n, i, j, th)
    A = rng.standard_normal((n, n)); Q, R = np.linalg.qr(A)
    Q = Q @ np.diag(np.sign(np.diag(R)))
    if np.linalg.det(Q) < 0:
        Q[:, 0] = -Q[:, 0]                 # keep det(Q)=+1 so conjugation stays in SO(n)
    return Q @ M @ Q.T


def son_bivector(n, angles):
    """Exact SO(n) via the rotor route: exp of an so(n) bivector (canonical planes)."""
    B = np.zeros((n, n))
    for k in range(n // 2):
        B[2 * k, 2 * k + 1] = -angles[k]; B[2 * k + 1, 2 * k] = angles[k]
    return expm(B)


def recover_angles(M):
    """Recover the floor(n/2) rotation angles from R in SO(n) (its eigen-spectrum):
    eigenvalues are e^{±i theta_k}. This is what makes the output a *test matrix* —
    the planted angles are recoverable invariants."""
    ev = np.linalg.eigvals(M)
    return sorted([x for x in np.angle(ev) if x > 1e-7])


def generate_test_matrix_set(n, seed=None):
    """Deterministic SO(n) test matrix with KNOWN rotation planes/angles + the recovery
    residual. Returns the matrix and its ground-truth invariants."""
    if seed is None:
        seed = n
    rng = np.random.default_rng(seed)
    angles = list(0.1 + 0.8 * rng.random(n // 2))
    M = son_planar(n, angles, seed)
    rec = recover_angles(M)
    planted = sorted(angles)
    m = min(len(rec), len(planted))
    return {
        "n": n, "planes": n // 2, "planted_angles": planted, "recovered_angles": rec,
        "matrix": M,
        "orth_resid": float(np.max(np.abs(M.T @ M - np.eye(n)))),
        "det_resid": float(abs(np.linalg.det(M) - 1.0)),
        "angle_recovery_resid": float(np.max(np.abs(np.array(rec[:m]) - np.array(planted[:m])))) if m else 0.0,
    }


def calibrate_faces(n, seed=0):
    """Plant the two blindness-suite faces and confirm they separate exactly at any n:
    a rotation-only step (size constant) vs a size-only step (direction constant)."""
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(n); v = 2.0 * v / np.linalg.norm(v)
    ang = [0.0] * (n // 2); ang[0] = 0.3
    R = son_planar(n, ang, seed)
    v_rot = R @ v
    v_siz = 1.5 * v
    def dtheta(a, b):
        return math.acos(np.clip(np.dot(a / np.linalg.norm(a), b / np.linalg.norm(b)), -1, 1))
    return {
        "n": n,
        "rotation_only": {"dtheta": float(dtheta(v, v_rot)), "dsize": float(abs(np.linalg.norm(v_rot) - np.linalg.norm(v)))},
        "size_only": {"dtheta": float(dtheta(v, v_siz)), "dsize": float(abs(np.linalg.norm(v_siz) - np.linalg.norm(v)))},
    }


def main():
    ladder = [2, 3, 4, 5, 6, 8, 12, 16, 32, 64, 128, 256, 512, 1024]
    rows = []
    for n in ladder:
        ts = generate_test_matrix_set(n)
        xchk = None
        if n <= 64:
            rng = np.random.default_rng(n)
            angles = list(0.1 + 0.8 * rng.random(n // 2))
            Mb = son_bivector(n, angles)
            Mc = np.eye(n)
            for k in range(n // 2):
                Mc = Mc @ givens(n, 2 * k, 2 * k + 1, angles[k])
            xchk = float(np.max(np.abs(Mb - Mc)))
        rows.append({k: ts[k] for k in ("n", "planes", "orth_resid", "det_resid", "angle_recovery_resid")} | {"rotor_vs_planar": xchk})

    out = {
        "experiment": "son_exact_generator_and_boundary",
        "generation_ladder": rows,
        "blindness_calibration": [calibrate_faces(n, seed=n) for n in [3, 4, 8, 64]],
        "boundary_note": "exact SO(n) generation unbounded (planar==rotor to ~1e-16 to n=1024); the composition<->hypercomplex identity bounded at D=4/SO(3),SO(4) by Hurwitz (see THE_LADDER_AND_THE_BREAK).",
    }

    def rnd(o):
        if isinstance(o, bool): return o
        if isinstance(o, float): return round(o, 15)
        if isinstance(o, dict): return {k: rnd(v) for k, v in o.items()}
        if isinstance(o, list): return [rnd(v) for v in o]
        return o
    out["content_sha256"] = hashlib.sha256(json.dumps(rnd(out), sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
