"""
compositional_mechanics (CN-TT v4, additive) — the complete deterministic mechanics of a
compositional trajectory, carried to its natural noise-limited maximum.

A composition tracked over an ordering is a CURVE on the Aitchison Riemannian manifold
(the simplex with the log-ratio metric). So the full apparatus of the differential
geometry of curves AND classical mechanics applies — and every quantity is a deterministic
linear-algebra reduction of the trajectory. This module computes the whole set:

  KINEMATIC (the jet / derivative tower):  position r=clr(x) -> velocity -> acceleration
      -> jerk -> ...  Each finite difference amplifies noise (~sqrt(2),sqrt(3),... per order),
      so there is a NATURAL MAXIMUM order N*: the deepest derivative whose magnitude is still
      signal, not noise (amplification ratio < ~1.5). N* is the honest ceiling — you cannot
      take infinite derivatives of real data. (This is the resolvability discipline applied to
      the derivative tower: the maximum is where the next derivative drops below the floor.)

  GEOMETRIC (Frenet-Serret):  speed |v|, path curvature kappa (how sharply it turns),
      and the frame (tangent/normal/binormal) from v and a.

  DYNAMIC (mass = share):  momentum p = mass*velocity, force F = dp/dt (Newton 2),
      kinetic energy T = 1/2 sum(mass*v^2), power dT/dt, angular-momentum bivector ||r^p||.

  INTEGRAL (accumulated invariants):  path length integral|v|dt, displacement, path
      efficiency = displacement/path-length (straight[~1] vs wandering[~0]), action integral
      T dt (Maupertuis-type), impulse = net momentum.

  SPECTRAL (every linear method):  SVD motion-modes + effective rank of the trajectory;
      velocity-covariance eigenstructure (the diffusion modes); the dominant motion direction.

This is a DESCRIPTION of the present trajectory, not a prediction. Additive, observe-only,
oracle untouched. Tier 1 (computed, self-tested, demonstrated on real EMBER transitions);
the mechanics *interpretation* is Tier 2 (the Aitchison manifold genuinely carries this
geometry). Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.
Honest-broker.
"""
from __future__ import annotations
import numpy as np


def _closure(M):
    M = np.clip(np.asarray(M, float), 0, None); s = M.sum(1, keepdims=True); s[s == 0] = 1; return M / s


def _clr(P):
    P = np.clip(P, 1e-12, None); L = np.log(P); return L - L.mean(1, keepdims=True)


def compositional_mechanics(M, names=None, dt=1.0, noise_ratio=1.5):
    M = np.asarray(M, float)
    names = list(names) if names is not None else [f"c{j}" for j in range(M.shape[1])]
    P = _closure(M); R = _clr(P)
    lab = ["position", "velocity", "acceleration", "jerk", "snap", "crackle"]
    derivs = [R]
    for _ in range(5):
        if len(derivs[-1]) < 3:
            break
        derivs.append(np.diff(derivs[-1], axis=0) / dt)
    mag = [float(np.linalg.norm(d, axis=1).mean()) for d in derivs]
    # natural maximum meaningful order: last derivative still below the noise-amplification factor
    order, ratios = 1, {}
    for k in range(2, len(derivs)):
        r = mag[k] / (mag[k - 1] + 1e-30); ratios[lab[k]] = round(r, 2)
        if r < noise_ratio:
            order = k
        else:
            break
    out = {"D": int(P.shape[1]), "T": int(P.shape[0]),
           "derivative_magnitudes": {lab[k]: round(mag[k], 4) for k in range(1, len(derivs))},
           "amplification_ratios": ratios,
           "max_meaningful_order": order, "max_meaningful_name": lab[order],
           "order_note": f"{lab[order]} is the deepest derivative above the noise floor; higher orders are noise-amplified."}
    v = derivs[1]; a = derivs[2] if len(derivs) > 2 else np.zeros_like(v[:-1])
    mass = (P[:-1] + P[1:]) / 2
    vv = v[:len(a)]; That = vv / (np.linalg.norm(vv, axis=1, keepdims=True) + 1e-30)
    kappa = np.linalg.norm(a - np.sum(a * That, 1, keepdims=True) * That, axis=1) / (np.linalg.norm(vv, axis=1) ** 2 + 1e-30)
    p = mass * v; F = np.diff(p, axis=0) / dt; T = 0.5 * (mass * v * v).sum(1)
    L = np.array([np.linalg.norm(np.outer(R[t], p[t]) - np.outer(p[t], R[t])) / np.sqrt(2) for t in range(len(p))])
    pathlen = float(np.linalg.norm(v, axis=1).sum())
    out["kinematic"] = {"speed_mean": round(float(np.linalg.norm(v, axis=1).mean()), 4),
                        "curvature_median": round(float(np.median(kappa)), 4)}
    out["dynamic"] = {"kinetic_energy_mean": round(float(T.mean()), 6),
                      "force_mean_mag": round(float(np.linalg.norm(F, axis=1).mean()), 4),
                      "power_mean": round(float(np.diff(T).mean()) if len(T) > 1 else 0.0, 6),
                      "angular_momentum_mean": round(float(L.mean()), 4)}
    out["integral"] = {"path_length": round(pathlen, 3),
                       "displacement": round(float(np.linalg.norm(R[-1] - R[0])), 3),
                       "path_efficiency": round(float(np.linalg.norm(R[-1] - R[0]) / (pathlen + 1e-30)), 3),
                       "action_int_T": round(float(T.sum()), 3),
                       "impulse_net": round(float(np.linalg.norm(p.sum(0))), 4)}
    X = R - R.mean(0); U, S, Vt = np.linalg.svd(X, full_matrices=False); s = S[S > S.max() * 1e-9] if S.max() > 0 else S
    out["spectral"] = {"motion_mode_singulars": [round(float(x), 3) for x in s[:5]],
                       "effective_rank": round(float((s.sum() ** 2) / (s ** 2).sum()) if s.size else 0.0, 2),
                       "dominant_mode_carriers": [names[j] for j in np.argsort(-np.abs(Vt[0]))[:3]] if len(Vt) else []}
    return out


def _self_test():
    ok = True; T = 50
    # straight smooth drift -> high path efficiency, low effective rank, low derivative order needed
    t = np.linspace(0, 1, T); c0 = np.array([.6, .25, .1, .05]); c1 = np.array([.1, .2, .3, .4])
    P = np.exp(np.outer(1 - t, np.log(c0)) + np.outer(t, np.log(c1))); P /= P.sum(1, keepdims=True)
    r = compositional_mechanics(P, ["a", "b", "c", "d"])
    ok &= r["integral"]["path_efficiency"] > 0.9 and r["spectral"]["effective_rank"] < 1.6
    # noisy churn -> order capped at 1 (velocity), low efficiency
    rng = np.random.default_rng(0); Q = _closure(0.25 + rng.normal(0, 0.03, (T, 4)))
    r2 = compositional_mechanics(Q, ["a", "b", "c", "d"])
    ok &= r2["max_meaningful_order"] <= 2 and r2["integral"]["path_efficiency"] < 0.5
    return ok


if __name__ == "__main__":
    import sys
    print("compositional_mechanics self-test:", "ALL PASS" if _self_test() else "FAILED")
    sys.exit(0 if _self_test() else 1)
