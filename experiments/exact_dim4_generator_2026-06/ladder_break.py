#!/usr/bin/env python3
"""
The division-algebra ladder, and where it breaks — an experimental-mathematics construction.

Cayley-Dickson doubling R -> C -> H -> O -> S (dim 1,2,4,8,16), measured at each rung:
associativity defect, norm-multiplicativity defect, non-commutativity. Plus an explicit sedenion
zero divisor, and an honest transcendental: orbit closure on S^3 (a rational rotation angle closes;
an irrational one never does — Weyl equidistribution). numpy + stdlib; deterministic (seed 4);
hash-receipted. The point is to PUSH THE BOUNDS AND SEE WHAT BREAKS — and the breaks are real
theorems (Hurwitz; Cayley-Dickson; equidistribution), not numerical coincidence. They are also the
reason the Hs engine lives at D=4 and tiles, rather than building a native high-D quaternion.

Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker.
"""
import numpy as np, hashlib, json, math
rng = np.random.default_rng(4)

def conj(x):
    n = len(x)
    if n == 1: return x.copy()
    m = n // 2; return np.concatenate([conj(x[:m]), -x[m:]])

def mul(x, y):
    n = len(x)
    if n == 1: return x * y
    m = n // 2; a, b, c, d = x[:m], x[m:], y[:m], y[m:]
    return np.concatenate([mul(a, c) - mul(conj(d), b), mul(d, a) + mul(b, conj(c))])

def norm(x): return float(np.sqrt(np.sum(x * x)))
def rnd(n): return rng.standard_normal(n)

names = {1: "R (real)", 2: "C (complex)", 4: "H (quaternion)", 8: "O (octonion)", 16: "S (sedenion)"}
res = {}
for n in (1, 2, 4, 8, 16):
    assoc = normmult = comm = 0.0
    for _ in range(400):
        x, y, z = rnd(n), rnd(n), rnd(n)
        assoc = max(assoc, norm(mul(mul(x, y), z) - mul(x, mul(y, z))))
        normmult = max(normmult, abs(norm(mul(x, y)) - norm(x) * norm(y)))
        comm = max(comm, norm(mul(x, y) - mul(y, x)))
    res[names[n]] = {"associativity_defect": assoc, "norm_mult_defect": normmult, "noncommutativity": comm}

def e(i, n=16):
    v = np.zeros(n); v[i] = 1.0; return v
zero_div = None
for i in range(1, 16):
    for j in range(i + 1, 16):
        a = e(i) + e(j)
        for k in range(1, 16):
            for l in range(k + 1, 16):
                if norm(mul(a, e(k) + e(l))) < 1e-9 and not zero_div:
                    zero_div = {"a": f"e{i}+e{j}", "b": f"e{k}+e{l}", "abs_a": round(norm(a), 3),
                                "abs_b": round(norm(e(k) + e(l)), 3), "abs_ab": float(norm(mul(a, e(k) + e(l))))}
        if zero_div: break
    if zero_div: break

def axis_quat(theta):
    ax = np.array([0, 0.6, 0.8]); return np.concatenate([[np.cos(theta / 2)], np.sin(theta / 2) * ax])
def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])
def orbit(theta, N=2000, eps=1e-6):
    q = axis_quat(theta); cur = q.copy(); best = 9.9; ret = None
    for nstep in range(1, N + 1):
        d = min(norm(cur - np.array([1., 0, 0, 0])), norm(cur + np.array([1., 0, 0, 0])))
        best = min(best, d)
        if d < eps and ret is None: ret = nstep
        cur = qmul(cur, q)
    return {"returned_at": ret, "min_dist": round(best, 4)}

out = {"ladder": res, "sedenion_zero_divisor": zero_div,
       "orbit_rational_2pi_over_7": orbit(2 * math.pi / 7),
       "orbit_irrational_2pi_sqrt2": orbit(2 * math.pi * (math.sqrt(2) % 1))}
canon = json.dumps(out, sort_keys=True, default=lambda o: round(o, 12) if isinstance(o, float) else o)
out["content_sha256"] = hashlib.sha256(canon.encode()).hexdigest()
print(json.dumps(out, indent=2))
