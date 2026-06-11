"""CN-TT v4 — period-2 attractor fit (faithful port of hci_shared.attractors)."""
from __future__ import annotations
import sys as _sys; from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
import numpy as np
import geometry as geo

def _ilr(rows):
    comp = geo.closure(np.asarray(rows, float)); H = geo.helmert_basis(comp.shape[1])
    ilr = geo.clr(comp) @ H.T
    return ilr, np.linalg.norm(ilr, axis=1)

def fit_attractor(rows, T_min=8, period_threshold=0.6, amplitude_threshold=1e-10):
    rows = geo.closure(np.asarray(rows, float)); T = rows.shape[0]; warnings = []
    def _unfit(reason):
        warnings.append(reason)
        return {"fitted":False,"period":1,"period_stability":0.0,"dominant_pair":{"axis_a":0,"axis_b":0},
                "contraction_lambda":0.0,"amplitude_A":0.0,"damping_zeta":0.0,
                "confidence":{"oscillation_ratio":0.0,"period_stability_score":0.0},"warnings":warnings}
    if T < T_min: return _unfit(f"trajectory too short for attractor fit (T={T} < T_min={T_min})")
    ilr, _ = _ilr(rows)
    centered = ilr - ilr.mean(axis=0, keepdims=True)
    var_per_axis = (centered**2).sum(axis=0); total_var = float(var_per_axis.sum())
    if total_var < amplitude_threshold: return _unfit("ILR variance below amplitude threshold; trajectory near fixed point")
    autocorr_lag1 = (centered[:-1]*centered[1:]).sum(axis=0)
    safe_var = np.where(var_per_axis > 1e-30, var_per_axis, 1.0)
    period_2_score = -autocorr_lag1 / safe_var
    max_var = float(var_per_axis.max())
    if max_var < amplitude_threshold: return _unfit("no axis has substantive variance; trajectory near fixed point")
    relative_floor = max(1e-12*max_var, 1e-30); valid_mask = var_per_axis > relative_floor
    if valid_mask.sum() < 1: return _unfit("no axes pass relative variance threshold")
    sorted_axes = np.argsort(period_2_score)[::-1]
    sorted_valid = [int(idx) for idx in sorted_axes if bool(valid_mask[idx])]
    if len(sorted_valid) == 0: return _unfit("no valid axes after filter")
    axis_a = sorted_valid[0]
    if len(sorted_valid) >= 2:
        axis_b = sorted_valid[1]
        period_stability = float(max(0.0, (period_2_score[axis_a]+period_2_score[axis_b])/2.0))
        pair_variance = float(var_per_axis[axis_a]+var_per_axis[axis_b])
        envelope = np.abs(centered[:, [axis_a, axis_b]]).sum(axis=1)
    else:
        axis_b = axis_a; period_stability = float(max(0.0, period_2_score[axis_a]))
        pair_variance = float(var_per_axis[axis_a]); envelope = np.abs(centered[:, axis_a])
        warnings.append("1-D limit cycle: only one ILR axis carries variance; axis_b = axis_a in dominant_pair")
    oscillation_ratio = pair_variance / max(total_var, 1e-30)
    amplitude_A = float(np.sqrt(pair_variance / T))
    log_env = np.log(np.maximum(envelope, 1e-15)); t_vec = np.arange(T, dtype=float)
    slope, _ = np.polyfit(t_vec, log_env, 1)
    contraction_lambda = float(slope); damping_zeta = float(-slope)
    if period_stability >= period_threshold and amplitude_A >= amplitude_threshold:
        fitted = True; period_value = 2
    else:
        fitted = False; period_value = 1
        if period_stability < period_threshold: warnings.append(f"period_stability {period_stability:.3f} below threshold {period_threshold}; no clean period-2 structure")
        if amplitude_A < amplitude_threshold: warnings.append(f"amplitude_A {amplitude_A:.3e} below threshold {amplitude_threshold:.3e}")
    return {"fitted":fitted,"period":period_value,"period_stability":period_stability,
            "dominant_pair":{"axis_a":axis_a,"axis_b":axis_b},"contraction_lambda":contraction_lambda,
            "amplitude_A":amplitude_A,"damping_zeta":damping_zeta,
            "confidence":{"oscillation_ratio":float(oscillation_ratio),"period_stability_score":period_stability},"warnings":warnings}
