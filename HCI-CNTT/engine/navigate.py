"""CN-TT v4 — navigation family (P2 parity port).
Stable angle uses 2*atan2(||u-v||,||u+v||) on unit vectors: numerically stable near
0 and pi in ANY dimension (agrees with the D=4 quaternion reading; the documented
improvement over the oracle's arccos)."""
from __future__ import annotations
import numpy as np

def shannon_entropy(p):
    p = np.asarray(p, float); s = np.where(p > 0, p * np.log(np.where(p > 0, p, 1.0)), 0.0)
    return float(-s.sum())

def k_eff(p):
    return float(np.exp(shannon_entropy(p)))

def higgins_scale(p):
    p = np.asarray(p, float); D = p.shape[-1]
    return 0.0 if D < 2 else float(1.0 - shannon_entropy(p) / np.log(D))

def tv_distance(a, b):
    return float(0.5 * np.sum(np.abs(np.asarray(a, float) - np.asarray(b, float))))

def aitchison_norm(clr_vec):
    return float(np.linalg.norm(clr_vec))

def aitchison_distance(a, b):
    return float(np.linalg.norm(np.asarray(a, float) - np.asarray(b, float)))

def stable_angle(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    na = np.linalg.norm(a); nb = np.linalg.norm(b)
    if na < 1e-300 or nb < 1e-300:
        return 0.0
    u = a / na; v = b / nb
    return float(2.0 * np.arctan2(np.linalg.norm(u - v), np.linalg.norm(u + v)))

def helmsman_index(clr_prev, clr_curr):
    d = np.asarray(clr_curr, float) - np.asarray(clr_prev, float)
    return int(np.argmax(np.abs(d)))

def ring_class(hs):
    for t, lbl in [(0.1,"Hs-1"),(0.3,"Hs-2"),(0.5,"Hs-3"),(0.7,"Hs-4"),(0.9,"Hs-5")]:
        if hs < t: return lbl
    return "Hs-6"

def concentration_regime(k_eff_yoy, tv_step, tv_median, threshold=0.05):
    if k_eff_yoy is None: return None
    if k_eff_yoy < -threshold:
        if tv_step is not None and tv_median is not None and tv_step <= tv_median:
            return "deceptive"
        return "tightening"
    if k_eff_yoy > threshold: return "loosening"
    return "stable"

def navigate(comp, clr, ilr, regime_k=2.0, regime_threshold=0.05):
    """comp/clr/ilr: (T,D)/(T,D)/(T,D-1) arrays. Returns the per-step + summary family."""
    comp = np.asarray(comp, float); clr = np.asarray(clr, float); ilr = np.asarray(ilr, float)
    T = comp.shape[0]
    keff = [k_eff(comp[t]) for t in range(T)]
    steps = []
    tv_series = []
    for t in range(T):
        tv = tv_distance(comp[t-1], comp[t]) if t > 0 else None
        tv_series.append(tv)
        steps.append({
            "k_eff": keff[t],
            "aitchison_norm": aitchison_norm(clr[t]),
            "higgins_scale": higgins_scale(comp[t]),
            "tv_step": tv,
            "aitchison_step": aitchison_distance(clr[t-1], clr[t]) if t > 0 else None,
            "angular_velocity": stable_angle(ilr[t-1], ilr[t]) if t > 0 else None,
            "helmsman": helmsman_index(clr[t-1], clr[t]) if t > 0 else None,
        })
    valid_tv = [v for v in tv_series if v is not None]
    tv_med = float(np.median(valid_tv)) if valid_tv else None
    for t in range(T):
        yoy = keff[t] - keff[t-1] if t > 0 else None
        steps[t]["k_eff_yoy"] = yoy
        steps[t]["regime"] = concentration_regime(yoy, tv_series[t], tv_med, regime_threshold)
        steps[t]["ring_class"] = ring_class(steps[t]["higgins_scale"])
    # regime boundaries on ilr step distance (mean + k*std)
    if T > 1:
        sd = np.linalg.norm(ilr[1:] - ilr[:-1], axis=1)
        thr = float(sd.mean() + regime_k * sd.std()) if sd.size > 1 else 0.0
        bnds = [int(i) for i in np.where(sd > thr)[0]] if sd.size > 1 else []
    else:
        thr, bnds = 0.0, []
    return {
        "n_steps": T,
        "k_eff": {"min": float(min(keff)), "max": float(max(keff)), "final": float(keff[-1])},
        "tv_median": tv_med,
        "regime_counts": {tag: sum(1 for s in steps if s["regime"] == tag)
                          for tag in ("tightening","loosening","deceptive","stable")},
        "regime_boundaries": {"threshold": thr, "indices": bnds},
        "steps": steps,
    }

# ---- additional parity quantities (ported from oracle for the Backblaze comparison) ----
def s_j_sensitivity(p):
    p = np.asarray(p, float); inv = 1.0 / p
    return (inv / inv.sum()).tolist()

def bearing_pairs(clr_vec, carriers):
    h = np.asarray(clr_vec, float); D = len(h); out = []
    for i in range(D):
        for j in range(i + 1, D):
            out.append({"i": carriers[i], "j": carriers[j],
                        "theta_deg": float(np.degrees(np.arctan2(h[j], h[i])))})
    return out

def kappa_hs_trace(p):
    p = np.asarray(p, float); D = len(p)
    K = (np.eye(D) - 1.0 / D) / np.outer(p, p)
    return float(np.trace(K))

def lock_events(clr_matrix, threshold=-10.0):
    h = np.asarray(clr_matrix, float); locked = h.min(axis=1) < threshold
    trans = []; in_lock = False
    for t in range(h.shape[0]):
        if locked[t] and not in_lock: trans.append({"t": int(t), "kind": "LOCK-ACQ"}); in_lock = True
        elif not locked[t] and in_lock: trans.append({"t": int(t), "kind": "LOCK-LOSS"}); in_lock = False
    return {"threshold_clr": threshold, "n_degen_timesteps": int(locked.sum()),
            "n_transitions": len(trans), "transitions": trans}

def degeneracy_flags(comp):
    rows = np.asarray(comp, float); T, D = rows.shape
    f = {"small_T": bool(T < 20), "small_D": bool(D < 3),
         "row_variance_below_threshold": bool(rows.std(axis=0).max() < 1e-6)}
    f["any_flag_set"] = any(f.values()); return f
