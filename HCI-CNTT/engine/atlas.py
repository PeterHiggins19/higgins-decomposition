"""CN-TT v4 — L3 Tile/Atlas. The tile-native core.
numpy for chart logic; scipy.sparse confined behind solve_atlas()/reconstruct_clr()
(the documented port seam: a C/Rust backend can replace the solver)."""
from __future__ import annotations
import itertools
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import connected_components

def sliding_window_atlas(D, width=4, overlap=3):
    """Overlapping 4-part charts, overlap 3 (band co-occurrence, diameter ~ D)."""
    step = width - overlap
    charts = [tuple(range(i, i + width)) for i in range(0, D - width + 1, step)]
    if not charts:
        charts = [tuple(range(D))]
    if charts[-1][-1] != D - 1:
        charts.append(tuple(range(D - width, D)))
    return charts

def hierarchical_atlas(D, k=4):
    """Balanced k-ary tree of 4-part charts (representative chaining).
    Co-occurrence diameter O(log D) -> best conditioning. For microbiome this
    tree IS the phylogeny (sibling taxa share the low-level charts)."""
    charts = []; level = list(range(D))
    while len(level) > 1:
        nxt = []; n = len(level); s = 0
        while s < n:
            blk = level[s:s + k]
            if len(blk) < 2:
                if charts:
                    charts[-1] = tuple(dict.fromkeys(charts[-1] + tuple(blk)))
                nxt.append(blk[0]); s += k; continue
            charts.append(tuple(blk)); nxt.append(blk[0]); s += k
        level = nxt
    return charts

def edges_from_charts(charts):
    E = set()
    for c in charts:
        for a, b in itertools.combinations(c, 2):
            E.add((a, b) if a < b else (b, a))
    return np.array(sorted(E), dtype=np.int64)

def is_connected(D, edges):
    a = edges[:, 0]; b = edges[:, 1]
    L = sparse.csr_matrix((np.ones(2*len(edges)),
        (np.concatenate([a, b]), np.concatenate([b, a]))), shape=(D, D))
    ncomp, _ = connected_components(L, directed=False)
    return ncomp == 1, ncomp

def reconstruct_clr(D, edges, x_true):
    """Recover CLR(x) from chart-internal log-ratios log(x_i/x_j)=clr_i-clr_j.
    A^T A is the co-occurrence graph Laplacian; exact (up to centering) iff connected.
    Returns (clr_hat, recon_error_vs_true, n_components)."""
    a = edges[:, 0]; b = edges[:, 1]; m = len(edges)
    bvals = np.log(x_true[a]) - np.log(x_true[b])
    rows = np.repeat(np.arange(m), 2)
    cols = np.empty(2*m, np.int64); cols[0::2] = a; cols[1::2] = b
    data = np.empty(2*m); data[0::2] = 1.0; data[1::2] = -1.0
    A = sparse.csr_matrix((data, (rows, cols)), shape=(m, D))
    L = (A.T @ A).tocsr()
    ncomp, labels = connected_components(L, directed=False)
    Atb = A.T @ bvals; c = np.zeros(D)
    for comp in range(ncomp):
        idx = np.where(labels == comp)[0]
        if len(idx) == 1:
            continue
        rest = idx[1:]
        c[rest] = spsolve(L[rest][:, rest].tocsc(), Atb[rest])
    c -= c.mean()
    from geometry import clr
    err = float(np.max(np.abs(c - clr(x_true))))
    return c, err, int(ncomp)
