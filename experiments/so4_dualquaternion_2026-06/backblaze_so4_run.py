#!/usr/bin/env python3
"""
SO(4) / dual-quaternion 6-DOF reading run on the LIVE Backblaze fleet data.

Self-contained (no imports beyond numpy) so it reproduces with no stale-cache risk.
The fleet's failure-mode budget (Mechanical, Thermal, Age, Errors) is D=4 -> the exact
rung. Each day is an ILR point v_t in R^3 = Im(H). Each step t->t+1 is read as ONE rigid
motion (R_t, tau_t):  v_{t+1} = R_t v_t + tau_t, encoded as a unit dual quaternion.

  R_t  = SO(3) sandwich rotating the DIRECTION u_t -> u_{t+1}  (the W-III relational
         "arrow of intent" drift — the existing read).
  tau_t = v_{t+1} - R_t v_t  — the radial / SIZE-budget change (moving-budget channel),
         now carried in the SAME exact object.
  screw decomposition exposes the PITCH (axial translation vs rotation) — a coupling
         invariant neither the rotation-only nor the size-only read computes.

Honest question: does the translation/screw channel reveal events the rotation-only read
misses, and do rotation and size couple (nonzero pitch) or stay orthogonal (pitch ~ 0)?

Reads public data, never copies it into a claim. Deterministic; hash-receipted.
Author: Peter Higgins; AI-assisted per HUF-STD-001. Honest-broker tiered.
"""
import csv, hashlib, json, math, os
import numpy as np

def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
                     w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
def qconj(a): return np.array([a[0], -a[1], -a[2], -a[3]])
def R_from_quat(q):
    w, x, y, z = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def dq_from_pose(q_r, t):
    q_d = 0.5*qmul(np.array([0.0, t[0], t[1], t[2]]), np.asarray(q_r, float))
    return np.concatenate([np.asarray(q_r, float), q_d])
def dq_mul(A, B):
    ar, ad, br, bd = A[:4], A[4:], B[:4], B[4:]
    return np.concatenate([qmul(ar, br), qmul(ar, bd)+qmul(ad, br)])
def dq_point_conj(A): return np.concatenate([qconj(A[:4]), -qconj(A[4:])])
def dq_pose(A):
    q_r = A[:4]; tq = 2.0*qmul(A[4:], qconj(q_r)); return q_r, tq[1:]
def dq_transform_point(A, p):
    P = np.concatenate([np.array([1.0,0,0,0]), np.array([0.0,p[0],p[1],p[2]])])
    return dq_mul(dq_mul(A, P), dq_point_conj(A))[4:][1:]
def dq_to_screw(A):
    q_r, t = dq_pose(A); w = float(np.clip(q_r[0], -1, 1))
    th = 2.0*math.acos(w); s = math.sqrt(max(0.0, 1.0-w*w))
    if s < 1e-12:
        nt = np.linalg.norm(t); l = t/nt if nt > 1e-15 else np.array([0.,0.,1.])
        return l, 0.0, float(nt)
    l = q_r[1:]/s; d = float(np.dot(t, l)); return l, float(th), d

CSV = os.environ.get("BB_CSV",
    "/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/Current-Repo/Hs/"
    "experiments/Hs-CNT_2026-05/codawork2026/backblaze_fleet/backblaze_fleet_input.csv")

def helmert(D):
    B = np.zeros((D-1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= math.sqrt(i/(i+1.0))
    return B

def load():
    rows, dates = [], []
    with open(CSV) as f:
        for r in csv.DictReader(f):
            dates.append(r["Date"])
            rows.append([float(r["Mechanical"]), float(r["Thermal"]), float(r["Age"]), float(r["Errors"])])
    return dates, np.array(rows)

def main():
    dates, raw = load()
    H4 = helmert(4)
    V = []
    for x in raw:
        c = x/x.sum(); clr = np.log(c)-np.log(c).mean(); V.append(H4 @ clr)
    V = np.array(V); T = len(V)

    recon = 0.0
    theta = np.zeros(T-1); tnorm = np.zeros(T-1); axial = np.zeros(T-1)
    for t in range(T-1):
        v0, v1 = V[t], V[t+1]
        r0, r1 = np.linalg.norm(v0), np.linalg.norm(v1)
        if r0 < 1e-12 or r1 < 1e-12: continue
        u0, u1 = v0/r0, v1/r1
        dot = float(np.clip(np.dot(u0, u1), -1, 1)); ax = np.cross(u0, u1); na = np.linalg.norm(ax)
        if na < 1e-15:
            q = np.array([1.0,0,0,0])
        else:
            ang = math.atan2(na, dot); ax = ax/na
            q = np.array([math.cos(ang/2), *(math.sin(ang/2)*ax)])
        R = R_from_quat(q); tau = v1 - R @ v0
        eta = dq_from_pose(q, tau)
        recon = max(recon, np.max(np.abs(dq_transform_point(eta, v0) - v1)))
        l, th, d = dq_to_screw(eta)
        theta[t] = th; tnorm[t] = np.linalg.norm(tau); axial[t] = abs(d)/(np.linalg.norm(tau)+1e-15)

    def mad_thr(x, k=3.0):
        med = np.median(x); mad = np.median(np.abs(x-med))+1e-15
        return med + k*1.4826*mad
    rot_thr, siz_thr = mad_thr(theta), mad_thr(tnorm)
    rot = set(int(i) for i in np.where(theta > rot_thr)[0])
    siz = set(int(i) for i in np.where(tnorm > siz_thr)[0])
    siz_only = sorted(siz - rot); rot_only = sorted(rot - siz); both = sorted(rot & siz)

    out = {
        "experiment": "backblaze_fleet_so4_dual_quaternion_6dof",
        "data": "backblaze_fleet_input.csv (Mechanical,Thermal,Age,Errors)",
        "days": T, "steps": T-1,
        "exactness_max_6dof_reconstruction_residual": float(recon),
        "channels": {
            "rotation_angle_rad_median": float(np.median(theta)), "rotation_angle_rad_max": float(theta.max()),
            "translation_size_median": float(np.median(tnorm)), "translation_size_max": float(tnorm.max()),
            "screw_axial_fraction_median": float(np.median(axial)), "screw_axial_fraction_max": float(axial.max()),
        },
        "events": {
            "rotation_threshold": float(rot_thr), "size_threshold": float(siz_thr),
            "rotation_events": len(rot), "size_events": len(siz),
            "both": len(both), "rotation_only": len(rot_only),
            "size_only_rotation_blind_NEW_class": len(siz_only),
            "size_only_example_dates": [dates[i+1] for i in siz_only[:8]],
        },
    }
    def rnd(o):
        if isinstance(o, bool): return o
        if isinstance(o, float): return round(o, 15)
        if isinstance(o, dict): return {k: rnd(v) for k, v in o.items()}
        if isinstance(o, list): return [rnd(v) for v in o]
        return o
    out["content_sha256"] = hashlib.sha256(json.dumps(rnd(out), sort_keys=True, separators=(",",":")).encode()).hexdigest()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
