#!/usr/bin/env python3
"""
HS-GOLD-1 — the standardized known-hash conformance fixture set.

A frozen, deterministic battery that any future build (any platform, numpy/scipy version,
or port) can re-run to PROVE it still computes the same answers. The fixtures hash
platform-STABLE quantities only — rounded signal (10 dp) and pass/structure flags — never
raw IEEE-floor residuals (which jitter in the last bits across BLAS builds). So the master
hash certifies the *meaning*, not the noise.

Five fixtures:
  F1  D=4 exact rung           — a fixed 4-part composition, its ILR, sandwich == SO(3).
  F2  SO(n) ladder             — n=3,4,8,16 generated, rotation angles recovered.
  F3  dual-quaternion pose     — fixed pose, translation recovered (the SO(4) module).
  F4  blindness faces          — rotation-only vs size-only separate exactly (n=8).
  F5  real-data anchor         — Backblaze day0/dayN ILR + the rotation between them.

Usage:
  python3 hs_gold_fixtures.py            # print fixtures + per-fixture + MASTER sha256
  python3 hs_gold_fixtures.py --verify   # recompute and assert == HS_GOLD_1.json (exit 0/1)

Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
Honest-broker; Tier 1. Extends the HS-EPS-1 determinism contract. Nothing posted; Peter is the sole gate.
"""
import csv, hashlib, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BB_CSV = os.environ.get("BB_CSV", os.path.join(
    HERE, "..", "Hs-CNT_2026-05", "codawork2026", "backblaze_fleet", "backblaze_fleet_input.csv"))


def helmert(D):
    B = np.zeros((D - 1, D))
    for i in range(1, D):
        B[i - 1, :i] = 1.0 / i; B[i - 1, i] = -1.0; B[i - 1] *= math.sqrt(i / (i + 1.0))
    return B
def clr(x): L = np.log(x); return L - L.mean()
def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
                     w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
def qconj(a): return np.array([a[0], -a[1], -a[2], -a[3]])
def Rq(q):
    w, x, y, z = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def givens(n, i, j, th):
    G = np.eye(n); c, s = math.cos(th), math.sin(th); G[i,i]=c; G[j,j]=c; G[i,j]=-s; G[j,i]=s; return G
def son_planar(n, angles, seed):
    rng = np.random.default_rng(seed); M = np.eye(n)
    for k, (i, j) in enumerate([(2*k, 2*k+1) for k in range(n//2)]): M = M @ givens(n, i, j, angles[k])
    A = rng.standard_normal((n, n)); Q, R = np.linalg.qr(A); Q = Q @ np.diag(np.sign(np.diag(R)))
    if np.linalg.det(Q) < 0: Q[:, 0] = -Q[:, 0]
    return Q @ M @ Q.T
def recover_angles(M): return sorted([x for x in np.angle(np.linalg.eigvals(M)) if x > 1e-7])
def dq_from_pose(q, t): return np.concatenate([q, 0.5 * qmul(np.array([0., t[0], t[1], t[2]]), q)])
def dq_pose(A): tq = 2.0 * qmul(A[4:], qconj(A[:4])); return A[:4], tq[1:]
def R10(v): return [round(float(x), 10) for x in np.atleast_1d(v)]
def dth(a, b): return math.acos(np.clip(np.dot(a/np.linalg.norm(a), b/np.linalg.norm(b)), -1, 1))


def fixture_hash(o):
    def rnd(x):
        if isinstance(x, bool): return x
        if isinstance(x, float): return round(x, 10)
        if isinstance(x, dict): return {k: rnd(v) for k, v in x.items()}
        if isinstance(x, list): return [rnd(v) for v in x]
        return x
    return hashlib.sha256(json.dumps(rnd(o), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build():
    fix = {}
    # F1 D=4 rung
    c = np.array([0.4, 0.3, 0.2, 0.1]); ilr = helmert(4) @ clr(c)
    q = np.array([math.cos(0.4), 0.0, 0.0, math.sin(0.4)])
    sand = qmul(qmul(q, np.array([0., *ilr])), qconj(q))[1:]
    fix["F1_D4_rung"] = {"comp": R10(c), "ilr": R10(ilr),
                         "sandwich_eq_SO3": bool(np.max(np.abs(sand - Rq(q) @ ilr)) < 1e-12), "ilr_rot": R10(sand)}
    # F2 SO(n) ladder
    f2 = {}
    for n in [3, 4, 8, 16]:
        rng = np.random.default_rng(n); ang = list(0.1 + 0.8 * rng.random(n // 2)); M = son_planar(n, ang, seed=n)
        f2[f"n{n}"] = {"planes": n // 2, "recovered_angles": [round(a, 9) for a in recover_angles(M)],
                       "orthogonal": bool(np.max(np.abs(M.T @ M - np.eye(n))) < 1e-9),
                       "det1": bool(abs(np.linalg.det(M) - 1) < 1e-9)}
    fix["F2_SOn_ladder"] = f2
    # F3 dual-quaternion pose
    q3 = np.array([math.cos(0.6), 0.0, math.sin(0.6), 0.0]); t3 = np.array([1.0, -2.0, 3.0])
    qr, tr = dq_pose(dq_from_pose(q3, t3))
    fix["F3_dualquat_pose"] = {"recovered_t": R10(tr), "roundtrip_exact": bool(np.max(np.abs(tr - t3)) < 1e-10)}
    # F4 blindness faces
    rng = np.random.default_rng(8); v = rng.standard_normal(8); v = 2 * v / np.linalg.norm(v)
    ang = [0.0] * 4; ang[0] = 0.3; Rm = son_planar(8, ang, seed=8); vr = Rm @ v; vs = 1.5 * v
    fix["F4_blindness_faces"] = {"rot_only_dtheta": round(dth(v, vr), 10),
                                 "rot_only_size_blind": bool(abs(np.linalg.norm(vr) - np.linalg.norm(v)) < 1e-9),
                                 "size_only_rot_blind": bool(dth(v, vs) < 1e-9),
                                 "size_only_dsize": round(float(abs(np.linalg.norm(vs) - np.linalg.norm(v))), 10)}
    # F5 real-data anchor
    rows = []
    with open(BB_CSV) as f:
        for r in csv.DictReader(f): rows.append([float(r["Mechanical"]), float(r["Thermal"]), float(r["Age"]), float(r["Errors"])])
    raw = np.array(rows); H4 = helmert(4)
    v0 = H4 @ clr(raw[0] / raw[0].sum()); vN = H4 @ clr(raw[-1] / raw[-1].sum())
    fix["F5_backblaze_anchor"] = {"day0_ilr": R10(v0), "dayN_ilr": R10(vN),
                                  "rotation_angle_day0_to_N": round(dth(v0, vN), 10), "days": len(raw)}
    per = {k: fixture_hash(v) for k, v in fix.items()}
    master = hashlib.sha256(json.dumps(per, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return fix, per, master


def main():
    fix, per, master = build()
    if "--verify" in sys.argv:
        gold = json.load(open(os.path.join(HERE, "HS_GOLD_1.json")))
        ok = (per == gold["per_fixture_sha256"]) and (master == gold["MASTER_sha256"])
        for k in per:
            tag = "PASS" if per[k] == gold["per_fixture_sha256"].get(k) else "FAIL"
            print(f"  [{tag}] {k}")
        print(f"\n  MASTER {'PASS' if master == gold['MASTER_sha256'] else 'FAIL'}  {master}")
        sys.exit(0 if ok else 1)
    print(json.dumps({"fixtures": fix, "per_fixture_sha256": per, "MASTER_sha256": master}, indent=2))


if __name__ == "__main__":
    main()
