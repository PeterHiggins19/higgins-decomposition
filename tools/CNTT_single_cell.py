# ====================================================================================
#  CN-TT v4 — self-contained single cell (numpy only). Paste into a JupyterLab cell.
#  Engine core + lossless 4-part tiling + navigation + the 2026-06 guard layer.
#  Deterministic, hash-receipted. Author: Peter Higgins; AI-assisted per HUF-STD-001.
# ====================================================================================
import numpy as np, hashlib, json

# ---- geometry ----------------------------------------------------------------------
def closure(M):
    M = np.clip(np.asarray(M, float), 0, None); s = M.sum(1, keepdims=True); s[s==0]=1; return M/s
def clr(P):
    P = np.clip(P, 1e-12, None); L = np.log(P); return L - L.mean(1, keepdims=True)
def helmert(D):
    B = np.zeros((D-1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= np.sqrt(i/(i+1.0))
    return B
def ilr(P): return clr(P) @ helmert(P.shape[1]).T

# ---- E-21 carrier guard + zero treatment -------------------------------------------
def carrier_health(M):
    M = np.asarray(M, float); pos = (M > 0)
    structural = [j for j in range(M.shape[1]) if not pos[:, j].any()]      # never positive -> undefined in log-ratio
    constant   = [j for j in range(M.shape[1]) if np.ptp(M[:, j]) == 0 and j not in structural]
    active     = [j for j in range(M.shape[1]) if j not in structural]
    return structural, constant, active
def treat_zeros(M):                                                          # multiplicative replacement of sporadic zeros
    M = M.copy().astype(float)
    for j in range(M.shape[1]):
        pos = M[M[:, j] > 0, j]
        if pos.size: M[M[:, j] <= 0, j] = 0.65 * pos.min()
    return M

# ---- lossless 4-part tiling (overlap-3 sliding charts; reconstruct CLR; report error)
def tiling_lossless(P):
    T, D = P.shape
    if D < 4: return None, True                                            # tiling is for D>=4
    logP = np.log(np.clip(P, 1e-12, None))
    charts = [tuple(range(s, s+4)) for s in range(0, D-3)]                  # overlap = 3
    rows, b_all = [], []
    for ch in charts:                                                      # within-chart pairwise log-ratios (exact, closure-invariant)
        for a in range(4):
            for c in range(a+1, 4):
                i, j = ch[a], ch[c]; r = np.zeros(D); r[i] = 1; r[j] = -1
                rows.append(r); b_all.append(logP[:, i] - logP[:, j])
    A = np.array(rows); A = np.vstack([A, np.ones(D)])                      # + sum-zero constraint
    errs = []
    for t in range(min(T, 50)):
        b = np.append(np.array([bb[t] for bb in b_all]), 0.0)
        rec, *_ = np.linalg.lstsq(A, b, rcond=None)
        errs.append(np.max(np.abs(rec - clr(P[t:t+1])[0])))
    return float(max(errs)), True

# ---- navigation family --------------------------------------------------------------
def k_eff(P):
    P = np.clip(P, 1e-12, None); P = P/P.sum(1, keepdims=True); H = -(P*np.log(P)).sum(1); return np.exp(H)
def regimes(P, k=2.0):
    st = np.linalg.norm(np.diff(clr(P), axis=0), axis=1)
    thr = st.mean() + k*st.std(); return [int(i+1) for i, v in enumerate(st) if v > thr]
def deceptive(P):
    tv = 0.5*np.abs(np.diff(closure(P), axis=0)).sum(1); dk = np.diff(k_eff(P)); m = np.median(tv)
    return int(((dk < 0) & (tv <= m)).sum())

# ---- the 2026-06 guard layer (resolvability / coherence / rank / hold-lock) ---------
def helmsman_guard(P, names, motion_floor=1e-6, tie_rel=1e-3):
    tot = np.abs(np.diff(clr(P), axis=0)).sum(0); o = np.argsort(-tot)
    mag = float(tot[o[0]]); margin = float(tot[o[0]] - tot[o[1]]) if len(o) > 1 else mag
    if mag < motion_floor: return {"helmsman": None, "code": "HM-NUL-WRN", "margin": margin}
    if margin <= tie_rel*mag: return {"helmsman": "TIE", "code": "HM-TIE-WRN", "margin": margin}
    return {"helmsman": names[int(o[0])], "code": None, "margin": round(margin, 4)}
def coherent_helmsman(P, names):
    lP = np.log(np.clip(P, 1e-12, None)); D = P.shape[1]; m = np.zeros(D)
    for i in range(D):
        for j in range(D):
            if i != j: m[i] += np.abs(np.diff(lP[:, i]-lP[:, j])).sum()
        m[i] /= (D-1)
    return names[int(np.argmax(m))]
def effective_rank(P):
    X = clr(P); X = X - X.mean(0); s = np.linalg.svd(X, compute_uv=False); s = s[s > s.max()*1e-9] if s.max()>0 else s
    pr = float((s.sum()**2)/(s**2).sum()) if s.size else 0.0; maxr = min(P.shape[0]-1, P.shape[1]-1)
    return round(pr, 2), maxr, ("DG-RNK-WRN" if pr < 0.5*maxr else None)
def hold_lock(P, engine_floor=1e-9, k_up=4.0, k_down=2.0, struct_k=3.0):
    H = clr(P); st = np.linalg.norm(np.diff(H, axis=0), axis=1)
    if st.size < 2: return {"floor": 0.0, "events": []}
    med = np.median(st); mad = np.median(np.abs(st-med))*1.4826
    noise = max(engine_floor, max(np.quantile(st, 0.5)-mad, np.quantile(st, 0.25)), 1e-12)
    up, lo = k_up*noise, k_down*noise; s = "HOLD"; ev = []; ref = 0
    for t, m in enumerate(st):
        if s == "HOLD" and m > up: s = "MOVING"
        elif s == "MOVING" and m < lo:
            if np.linalg.norm(H[t+1]-H[ref]) >= struct_k*noise: ev.append(t+1); ref = t+1
            s = "HOLD"
    return {"floor": round(noise, 4), "events": ev}

# ---- deterministic content hash -----------------------------------------------------
def stable_hash(obj, dp=12):
    def norm(o):
        if isinstance(o, float): return round(o, dp)
        if isinstance(o, dict): return {k: norm(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [norm(v) for v in o]
        return o
    return hashlib.sha256(json.dumps(norm(obj), sort_keys=True, default=str).encode()).hexdigest()

# ---- the engine: composition matrix + names -> full payload ------------------------
def run_cntt(M, names=None):
    M = np.asarray(M, float); names = list(names) if names is not None else [f"c{j}" for j in range(M.shape[1])]
    structural, constant, active = carrier_health(M)
    guard = None
    if structural or constant:
        guard = {"excluded_structural_zero": [names[j] for j in structural],
                 "flagged_constant": [names[j] for j in constant],
                 "codes": (["GD-ZRC-CAL"] if structural else []) + (["GD-CNC-CAL"] if constant else [])}
        if structural: M = M[:, active]; names = [names[j] for j in active]
    sparsity = float((M <= 0).mean())
    M = treat_zeros(M); P = closure(M); recon, conn = tiling_lossless(P)
    res = helmsman_guard(P, names); rnk = effective_rank(P)
    codes = [c for c in (res["code"], rnk[2]) if c]
    payload = {
        "input": {"n_records": int(P.shape[0]), "n_carriers": int(P.shape[1]), "carriers": names,
                  "sparsity_pct": round(sparsity*100, 1)},
        "atlas": {"lossless": bool(conn and (recon is None or recon < 1e-6)), "reconstruction_max_err": recon},
        "navigation": {"k_eff_start": round(float(k_eff(P)[0]), 3), "k_eff_end": round(float(k_eff(P)[-1]), 3),
                       "helmsman_CLR": names[int(np.argmax(np.abs(np.diff(clr(P), axis=0)).sum(0)))],
                       "coherent_helmsman": coherent_helmsman(P, names),
                       "regime_boundaries": regimes(P), "deceptive_drift_steps": deceptive(P)},
        "guards": {"resolvability": res, "effective_rank": {"value": rnk[0], "max": rnk[1]},
                   "hold_lock": hold_lock(P), "sparsity_regime": ("GD-SPZ-WRN" if sparsity >= 0.5 else None),
                   "codes_fired": (codes + ([guard["codes"][0]] if guard else []))},
    }
    if guard: payload["input"]["carrier_guard"] = guard
    payload["cntt_content_sha256"] = stable_hash(payload)
    return payload

# ====================================================================================
#  DEMO — runs on paste. Replace `M, names` with your own (rows=time/sample, cols=parts).
# ====================================================================================
rng = np.random.default_rng(0); T, D = 60, 8
names = ["Coal", "Gas", "Hydro", "Nuclear", "Wind", "Solar", "Bio", "Other"]
base = np.array([0.30, 0.22, 0.18, 0.12, 0.08, 0.04, 0.04, 0.02])
M = np.maximum(base + np.cumsum(rng.normal(0, 0.01, (T, D)), 0) + rng.normal(0, 0.005, (T, D)), 1e-4)
out = run_cntt(M, names)
print(json.dumps(out, indent=2))
print("\nlossless:", out["atlas"]["lossless"], "| recon err:", out["atlas"]["reconstruction_max_err"],
      "| helmsman:", out["navigation"]["helmsman_CLR"], "(coherent:", out["navigation"]["coherent_helmsman"]+")",
      "| eff_rank:", out["guards"]["effective_rank"], "| hash:", out["cntt_content_sha256"][:12])
