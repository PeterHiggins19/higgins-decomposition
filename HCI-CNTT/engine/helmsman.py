"""CN-TT v4 — Helmsman rolling-window family (faithful port of hci_shared.helmsman)."""
from __future__ import annotations
import sys as _sys; from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
import numpy as np
import geometry as geo

def _detect_period_doubling(sigma_seq):
    n = len(sigma_seq)
    if n < 4: return None
    for depth in range(0, 4):
        period = 2 ** depth
        if period >= n: break
        m = (sigma_seq[:-period] == sigma_seq[period:])
        if m.size == 0: continue
        if float(m.mean()) >= 0.9: return depth
    return None

def compute_helmsman_family(rows, window=8):
    rows = geo.closure(np.asarray(rows, float)); T, D = rows.shape
    if T < 2:
        return {"sigma":[0]*T,"sign":[0]*T,"flips":{"total":0,"rolling":[],"rolling_window":int(window)},
                "stability_S_sigma":{"global":1.0,"rolling":[],"rolling_window":int(window)},
                "chaos_indicator":None,"torque_proxy":[0.0]*T}
    h = geo.clr(rows)
    delta = h[1:] - h[:-1]; abs_delta = np.abs(delta)
    sigma_internal = np.argmax(abs_delta, axis=1).astype(int)
    sigma = np.zeros(T, int); sigma[1:] = sigma_internal
    sign_arr = np.zeros(T, int)
    for t in range(1, T):
        d = delta[t-1, sigma[t]]
        sign_arr[t] = 1 if d > 0 else (-1 if d < 0 else 0)
    flips_per_t = np.zeros(T, int)
    for t in range(2, T):
        if sigma[t] != sigma[t-1]: flips_per_t[t] = 1
    flips_total = int(flips_per_t.sum())
    eff_window = max(2, min(int(window), max(T-1, 2)))
    n_windows = max(T-eff_window, 0)
    rolling_flips = np.array([int(flips_per_t[i:i+eff_window].sum()) for i in range(n_windows)], int)
    stability_global = 1.0 - flips_total / max(T-2, 1)
    rolling_stability = 1.0 - rolling_flips.astype(float) / max(eff_window-1, 1)
    torque = np.zeros(T, float)
    for t in range(1, T-1):
        torque[t] = float(abs(sigma[t+1] - 2*sigma[t] + sigma[t-1]))
    return {"sigma":[int(x) for x in sigma],"sign":[int(x) for x in sign_arr],
            "flips":{"total":flips_total,"rolling":[int(x) for x in rolling_flips],"rolling_window":eff_window},
            "stability_S_sigma":{"global":float(stability_global),"rolling":[float(x) for x in rolling_stability],"rolling_window":eff_window},
            "chaos_indicator":_detect_period_doubling(sigma_internal),"torque_proxy":[float(x) for x in torque]}
