#!/usr/bin/env python3
"""
Compositional deformation sensing on a sheet (skin) of patches.

Continuum mechanics: the local deformation gradient F polar-decomposes as F = R·U, where R in SO(3)
is the local rotation and U is the symmetric positive-definite stretch tensor. Hs reads both exactly:
  - R  -> a unit QUATERNION (the D=4 exact rung), the local rotation, to the IEEE floor;
  - U  -> its principal stretches are a SHAPE composition (which direction stretched most) + a SIZE
          (the volume change det U) -- the rotation/shape/size split of the blindness suite.
A sheet of such patches reads a surface's deformation field in detail (the "skin of sensors").
Deterministic; hash-receipted. Honest: polar decomposition is standard mechanics; the contribution is
the exact quaternion rotation read + the compositional strain read + the deterministic receipted field.
Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json, math
import numpy as np

rng = np.random.default_rng(5)
def axis_angle_quat(axis, ang):
    a = np.asarray(axis, float); a = a/np.linalg.norm(a)
    return np.array([math.cos(ang/2), *(math.sin(ang/2)*a)])
def R_from_quat(q):
    w, x, y, z = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def quat_from_R(R):
    w = math.sqrt(max(0, 1+R[0,0]+R[1,1]+R[2,2]))/2
    x = (R[2,1]-R[1,2])/(4*w); y = (R[0,2]-R[2,0])/(4*w); z = (R[1,0]-R[0,1])/(4*w)
    q = np.array([w, x, y, z]); return q/np.linalg.norm(q)
def polar(F):
    W, s, Vt = np.linalg.svd(F); R = W @ Vt
    if np.linalg.det(R) < 0:
        W[:, -1] *= -1; R = W @ Vt; s = s.copy(); s[-1] *= -1
    return R, s


def main():
    n = 8; xs = np.linspace(0, 1, n); ys = np.linspace(0, 1, n)
    rot_err = stretch_err = 0.0; field = []
    for x in xs:
        for y in ys:
            ang = 0.8*x; R = R_from_quat(axis_angle_quat([0, 1, 0], ang))   # planted bend
            bump = math.exp(-(((x-0.5)**2 + (y-0.5)**2)/0.06))
            lam = np.array([1.0+0.4*bump, 1.0-0.15*bump, 1.0+0.05*bump])     # planted stretch
            F = R @ np.diag(lam) + 0.001*rng.standard_normal((3, 3))
            Rh, s = polar(F); qh = quat_from_R(Rh)
            ang_h = 2*math.atan2(np.linalg.norm(qh[1:]), qh[0])
            rot_err = max(rot_err, abs(ang_h-ang))
            stretch_err = max(stretch_err, float(np.max(np.abs(np.sort(s)[::-1]-np.sort(lam)[::-1]))))
            sh = np.sort(s)[::-1]
            field.append({"x": round(x, 2), "y": round(y, 2), "rot_angle": round(ang_h, 4),
                          "shape_comp": [round(c, 3) for c in (sh/sh.sum())], "volume": round(float(np.prod(sh)), 4)})
    # exactness of the quaternion rotation read on a clean F
    ang = 0.6; Rc = R_from_quat(axis_angle_quat([0.3, 0.6, 0.74], ang))
    qh = quat_from_R(polar(Rc @ np.diag([1.2, 0.9, 1.05]))[0])
    out = {"experiment": "compositional_deformation_sheet", "patches": n*n,
           "clean_rotation_recovery_residual": float(abs(2*math.atan2(np.linalg.norm(qh[1:]), qh[0]) - ang)),
           "noisy_field_max_rotation_error_rad": round(rot_err, 4),
           "noisy_field_max_stretch_error": round(stretch_err, 4),
           "decomposition": "each patch = rotation (quaternion, exact) (+) shape (stretch composition) (+) size (volume det)",
           "sample_field": field[:3]}
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
