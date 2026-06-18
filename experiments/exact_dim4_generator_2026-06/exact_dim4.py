#!/usr/bin/env python3
"""
Exact native-dimension-four example generation for compositional data.

Designed around a simple, recognisable idea from experimental mathematics: settle or
represent a hard object by constructing an exact, *adjacent* one. Here Hs is used as an
inert, deterministic generator of exact dimension-four (S^3 = SU(2)) objects, their
Spin(4) = SO(4) twins at D=8, and a lossless tiling of arbitrarily high-dimensional
compositions into overlapping dimension-four charts.

numpy + scipy; deterministic (fixed seed); hash-receipted. Author: Peter Higgins
(human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker:
the numerics are Tier 1 (verified); any relevance to a research programme is the
reader's call. Inspiration cited in the companion note.
"""
import numpy as np, hashlib, json
from scipy import sparse
from scipy.sparse.linalg import spsolve

rng = np.random.default_rng(4)

# ---- shared geometry (mirrors hs_kinematics_engine.py) ----
def helmert(D):
    B = np.zeros((D - 1, D))
    for i in range(1, D):
        B[i - 1, :i] = 1.0 / i; B[i - 1, i] = -1.0; B[i - 1] *= np.sqrt(i / (i + 1.0))
    return B
def clr_vec(x): L = np.log(x); return L - L.mean()

# ---- quaternion algebra ----
def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])
def qconj(a): return np.array([a[0], -a[1], -a[2], -a[3]])
def rand_unit_quat():
    q = rng.standard_normal(4); return q / np.linalg.norm(q)
def R_from_quat(q):
    w, x, y, z = q
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w),     2 * (x * z + y * w)],
        [2 * (x * y + z * w),     1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w),     2 * (y * z + x * w),     1 - 2 * (x * x + y * y)]])

# === Construction 1: D=4 -> S^3 = SU(2) = Spin(3), exact ===
# A 4-part composition's 3 ILR coordinates are a point in R^3 = Im(H); an Aitchison
# rotation is the sandwich q v q*. Check it equals the SO(3) rotation, at the floor.
res1 = []
for _ in range(2000):
    v = rng.standard_normal(3)
    q = rand_unit_quat()
    sand = qmul(qmul(q, np.array([0.0, *v])), qconj(q))[1:]   # q v q*
    rot = R_from_quat(q) @ v
    res1.append(np.max(np.abs(sand - rot)))
d4_resid = float(np.max(res1))
# a real 4-part composition's ILR sits in R^3 and its norm is preserved under rotation
H4 = helmert(4)
comp = rng.dirichlet(np.ones(4))
ilr = H4 @ clr_vec(comp)
q = rand_unit_quat()
ilr_rot = qmul(qmul(q, np.array([0.0, *ilr])), qconj(q))[1:]
d4_norm = float(abs(np.linalg.norm(ilr_rot) - np.linalg.norm(ilr)))

# === Construction 2: D=8 -> Spin(4) = SU(2)xSU(2) = double cover of SO(4) ===
# twin quaternion (qL,qR) acts on R^4 = H by x -> qL x conj(qR). Build the 4x4
# matrix, check orthogonality and det = +1 (a genuine SO(4) element).
def twin_matrix(qL, qR):
    M = np.zeros((4, 4))
    for k in range(4):
        e = np.zeros(4); e[k] = 1.0
        M[:, k] = qmul(qmul(qL, e), qconj(qR))
    return M
orth = []; dets = []
for _ in range(2000):
    qL = rand_unit_quat(); qR = rand_unit_quat()
    M = twin_matrix(qL, qR)
    orth.append(np.max(np.abs(M.T @ M - np.eye(4))))
    dets.append(np.linalg.det(M))
d8_orth = float(np.max(orth)); d8_detdev = float(np.max(np.abs(np.array(dets) - 1.0)))

# === Construction 3: reverse case — tile a high-D composition into overlapping
# 4-part (S^3) charts and reconstruct the whole clr losslessly. ===
def path_edges(D):
    E = set()
    for s in range(D - 3):
        ch = range(s, s + 4)
        for i in ch:
            for j in ch:
                if i < j: E.add((i, j))
    return np.array(sorted(E), dtype=np.int64)
def reconstruct(D, edges, x):
    a = edges[:, 0]; b = edges[:, 1]; m = len(edges); bv = np.log(x[a]) - np.log(x[b])
    rows = np.repeat(np.arange(m), 2); cols = np.empty(2 * m, np.int64); cols[0::2] = a; cols[1::2] = b
    data = np.empty(2 * m); data[0::2] = 1.0; data[1::2] = -1.0
    A = sparse.csr_matrix((data, (rows, cols)), shape=(m, D)); L = (A.T @ A).tocsr(); Atb = A.T @ bv
    rest = np.arange(1, D); c = np.zeros(D); c[rest] = spsolve(L[rest][:, rest].tocsc(), Atb[rest]); c -= c.mean()
    return float(np.max(np.abs(c - clr_vec(x))))
tiling = []
for D in [16, 64, 256, 1024, 4096]:
    x = rng.dirichlet(np.ones(D) * 0.3); x = x / x.sum()
    e = path_edges(D); err = reconstruct(D, e, x)
    tiling.append({"D": D, "charts": D - 3, "edges": int(len(e)), "recon_residual": err})

results = {
    "experiment": "exact_native_dim4_example_generation",
    "seed": 4,
    "construction_1_D4_S3_SU2": {"sandwich_vs_SO3_max_residual": d4_resid, "ilr_norm_preservation": d4_norm, "trials": 2000},
    "construction_2_D8_Spin4_SO4": {"orthogonality_max_residual": d8_orth, "det_deviation_from_+1": d8_detdev, "trials": 2000},
    "construction_3_reverse_tiling": tiling,
}

def rnd(o):
    if isinstance(o, float): return round(o, 15)
    if isinstance(o, dict): return {k: rnd(v) for k, v in o.items()}
    if isinstance(o, list): return [rnd(v) for v in o]
    return o
canon = json.dumps(rnd(results), sort_keys=True, separators=(', ', ': '))
results["content_sha256"] = hashlib.sha256(canon.encode()).hexdigest()
print(json.dumps(results, indent=2))
