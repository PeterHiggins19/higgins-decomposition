"""CN-TT v4 — L2 Geometry. Pure numpy, port-ready (no scipy, no I/O)."""
from __future__ import annotations
import numpy as np

def closure(x):
    x = np.asarray(x, float)
    return x / x.sum(axis=-1, keepdims=True)

def clr(x):
    """Centered log-ratio. x closed/positive."""
    L = np.log(np.asarray(x, float))
    return L - L.mean(axis=-1, keepdims=True)

def helmert_basis(D):
    """Standard ascending Helmert ILR contrast matrix, (D-1) x D, orthonormal rows.
    Row k (k=1..D-1): first k entries +1/sqrt(k(k+1)); entry k+1 = -k/sqrt(k(k+1)).
    (Matches the documented oracle signature; exact-oracle parity verified in P2.)"""
    H = np.zeros((D - 1, D), float)
    for k in range(1, D):
        c = 1.0 / np.sqrt(k * (k + 1.0))
        H[k - 1, :k] = c
        H[k - 1, k] = -k * c
    return H

def ilr(x, H=None):
    """ILR coordinates: clr(x) @ H^T -> R^(D-1)."""
    c = clr(x)
    D = c.shape[-1]
    if H is None:
        H = helmert_basis(D)
    return c @ H.T

def radial(ilr_vec):
    """Per-step ILR norm (radial trajectory), first-class output."""
    return np.linalg.norm(np.asarray(ilr_vec, float), axis=-1)

def carrier_health(M):
    """E-21 log-ratio admissibility triage for carriers (raw, pre-closure matrix M, T x D).

    A carrier with NO positive value across all records ('structural zero') is undefined
    under the CLR/ILR log-ratio map (log(0) -> -inf -> nan, which later breaks eigh in the
    PCA/navigation block) and must be EXCLUDED. A carrier whose values never change
    ('constant', positive) is admissible under the map and is RETAINED, only flagged for
    calibration. Pure: classifies, never mutates. Returns index lists into M's columns.
    On well-formed data structural_zero and constant are both empty -> callers are no-ops."""
    M = np.asarray(M, float)
    D = M.shape[1] if M.ndim == 2 else 0
    active, structural_zero, constant = [], [], []
    for j in range(D):
        col = M[:, j]
        if not np.any(col > 0):
            structural_zero.append(j)            # no positive value anywhere -> undefined in Aitchison geometry
        else:
            active.append(j)
            if float(np.ptp(col)) == 0.0:
                constant.append(j)               # admissible but informationally flat
    return {"active": active, "structural_zero": structural_zero, "constant": constant}
