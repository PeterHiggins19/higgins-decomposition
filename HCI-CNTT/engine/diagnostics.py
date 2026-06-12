"""CN-TT v4 — depth tower, stage 1/2/3, EITT, nav-2D (faithful ports of cnt.py)."""
from __future__ import annotations
import sys as _sys; from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from itertools import combinations
import numpy as np
import geometry as geo
from attractors import fit_attractor

def variation_matrix(rows_closed):
    rows = np.asarray(rows_closed, float); T, D = rows.shape
    log_rows = np.log(rows); tau = np.zeros((D, D))
    for i in range(D):
        for j in range(D):
            if i == j: continue
            tau[i, j] = float(np.var(log_rows[:, i] - log_rows[:, j], ddof=0))
    return tau

def compute_stage1(clr_matrix, carriers):
    h = np.asarray(clr_matrix, float); T, D = h.shape; sections = []
    for i, j in combinations(range(D), 2):
        sections.append({"i":carriers[i],"j":carriers[j],"i_min":float(h[:,i].min()),"i_max":float(h[:,i].max()),
                         "j_min":float(h[:,j].min()),"j_max":float(h[:,j].max())})
    return {"n_sections":len(sections),"sections":sections}

def compute_stage2(rows_closed, clr_matrix, carriers):
    h = np.asarray(clr_matrix, float); T, D = h.shape; tau = variation_matrix(rows_closed); pe = []
    for i, j in combinations(range(D), 2):
        ci, cj = h[:, i], h[:, j]
        r = 0.0 if (np.std(ci, ddof=0) < 1e-15 or np.std(cj, ddof=0) < 1e-15) else float(np.corrcoef(ci, cj)[0, 1])
        bearings = np.degrees(np.arctan2(cj, ci)); spread = float(bearings.max() - bearings.min())
        pe.append({"i":carriers[i],"j":carriers[j],"pearson_r":r,"co_movement_score":max(0.0,r),
                   "opposition_score":max(0.0,-r),"bearing_spread_deg":spread,"locked_pair":bool(spread < 10.0)})
    return {"variation_matrix":{"carriers":list(carriers),"tau":tau.tolist()},"carrier_pair_examination":pe}

def compute_stage3(rows_closed, clr_matrix, carriers, triadic_t_limit=500, triadic_k=50, ladder_k_limit=200):
    h = np.asarray(clr_matrix, float); T, D = h.shape
    if T - 2 > triadic_t_limit:
        rng = np.random.default_rng(seed=42)
        sampled = sorted(rng.choice(T - 2, size=triadic_t_limit, replace=False).tolist())
        triadic_sampling = {"applied":True,"seed":42,"sample_size":triadic_t_limit,"total_triads_available":T-2}
    else:
        sampled = list(range(max(T - 2, 0))); triadic_sampling = {"applied":False}
    triads = []
    for t in sampled:
        a, b, c = h[t], h[t+1], h[t+2]
        area = 0.5 * abs((b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1]))
        triads.append({"t":int(t),"area":float(area),"sides":[float(np.linalg.norm(b-a)),float(np.linalg.norm(c-b)),float(np.linalg.norm(c-a))]})
    top_triads = sorted(triads, key=lambda x: x["area"], reverse=True)[:triadic_k]
    ladder = []
    for k in range(2, D):
        all_subsets = list(combinations(range(D), k)); n_total = len(all_subsets)
        scored = all_subsets[:ladder_k_limit] if n_total > ladder_k_limit else all_subsets
        correlations = []
        for subset in scored:
            sub = h[:, list(subset)]; sub_c = sub - sub.mean(axis=0, keepdims=True)
            stds = sub_c.std(axis=0, ddof=0); valid = stds > 1e-15
            if valid.sum() < 2: correlations.append(0.0); continue
            cm = np.corrcoef(sub_c[:, valid], rowvar=False); n = cm.shape[0]; mask = ~np.eye(n, dtype=bool)
            correlations.append(float(cm[mask].mean()) if mask.any() else 0.0)
        ladder.append({"degree":int(k),"n_subsets_total":n_total,"n_subsets_scored":len(scored),
                       "mean_correlation":float(np.mean(correlations)) if correlations else 0.0})
    if T > 1:
        sd = np.linalg.norm(h[1:] - h[:-1], axis=1)
        if sd.size > 1:
            threshold = float(sd.mean() + 2.0 * sd.std(ddof=0)); boundaries = np.where(sd > threshold)[0].tolist()
        else: threshold, boundaries = 0.0, []
    else: threshold, boundaries = 0.0, []
    return {"triadic_area":{"sampling":triadic_sampling,"n_kept":len(top_triads),"triads":top_triads},
            "subcomposition_ladder":{"ladder_k_limit":ladder_k_limit,"entries":ladder},
            "regime_detection":{"threshold":threshold,"n_boundaries":len(boundaries),"boundary_indices":[int(b) for b in boundaries]}}

def compute_depth_tower(rows_closed, clr_matrix, max_levels=50, precision=1e-2):
    h = np.asarray(clr_matrix, float); rows = np.asarray(rows_closed, float); T, D = h.shape
    energy_levels = []; energy_traj = h.copy()
    for ell in range(max_levels):
        if energy_traj.shape[0] < 2: break
        deltas_sq = (energy_traj[1:] - energy_traj[:-1]) ** 2 + 1e-15
        closed = deltas_sq / deltas_sq.sum(axis=1, keepdims=True)
        clr_next = np.log(closed) - np.log(closed).mean(axis=1, keepdims=True)
        energy_levels.append({"level":ell,"n_rows":int(closed.shape[0]),"norm_mean":float(np.linalg.norm(clr_next, axis=1).mean())})
        energy_traj = clr_next
    curvature_levels = []; curvature_traj = rows.copy()
    for ell in range(max_levels):
        if curvature_traj.shape[0] < 2: break
        inv_sq = 1.0 / (curvature_traj ** 2 + 1e-15); closed_curv = inv_sq / inv_sq.sum(axis=1, keepdims=True)
        clr_curv = np.log(closed_curv + 1e-30) - np.log(closed_curv + 1e-30).mean(axis=1, keepdims=True)
        curvature_levels.append({"level":ell,"n_rows":int(closed_curv.shape[0]),"norm_mean":float(np.linalg.norm(clr_curv, axis=1).mean())})
        curvature_traj = np.exp(clr_curv); curvature_traj = curvature_traj / curvature_traj.sum(axis=1, keepdims=True)
        if ell > 0 and abs(curvature_levels[-1]["norm_mean"] - curvature_levels[-2]["norm_mean"]) < precision: break
    attractor = fit_attractor(rows)
    if attractor.get("fitted") and attractor.get("period") == 2: termination_kind = "LIMIT_CYCLE_P2"
    elif energy_levels and energy_levels[-1]["norm_mean"] < precision: termination_kind = "FIXED_POINT"
    else: termination_kind = "EXHAUSTED"
    M_indices = sorted(set([0, T // 2, T - 1])) if T >= 1 else []
    involution_samples = []
    for t in M_indices:
        p = rows[t]; m1 = 1.0 / (p + 1e-30); m1 = m1 / m1.sum(); m2 = 1.0 / (m1 + 1e-30); m2 = m2 / m2.sum()
        involution_samples.append({"t":int(t),"max_residual_linf":float(np.max(np.abs(m2 - p)))})
    involution_max = max((s["max_residual_linf"] for s in involution_samples), default=0.0)
    A = float(attractor.get("amplitude_A") or 0.0); zeta = float(attractor.get("damping_zeta") or 0.0)
    if D == 2: ir_class = "D2_DEGENERATE"
    elif A < 0.1: ir_class = "CRITICALLY_DAMPED"
    elif abs(zeta) < 1e-6: ir_class = "UNDAMPED"
    elif 0 < zeta < 0.1: ir_class = "LIGHTLY_DAMPED"
    elif A > 0.7: ir_class = "OVERDAMPED_EXTREME"
    else: ir_class = "MODERATELY_DAMPED"
    return {"energy_levels":energy_levels,"curvature_levels":curvature_levels,
            "termination":{"kind":termination_kind,"level_index":len(energy_levels)-1 if energy_levels else None,
                           "period":attractor.get("period") if attractor.get("fitted") else None},
            "attractor":attractor,"involution_M_squared":{"samples":involution_samples,"max_residual_overall":involution_max,
            "verified_at_ieee_floor":involution_max < 1e-10},"ir_class":ir_class}

def eitt_bench_test(rows_closed, clr_matrix, gate_pct=5.0, m_sweep=(2,4,8,16,32,64,128)):
    h = np.asarray(clr_matrix, float); T = h.shape[0]; results = []
    for M in m_sweep:
        if M >= T: results.append({"M":int(M),"skipped_reason":"M >= T"}); continue
        seg_size = T // M; seg_norms = []
        for s in range(M):
            seg = h[s*seg_size:(s+1)*seg_size]
            if seg.shape[0] == 0: continue
            seg_norms.append(float(np.linalg.norm(seg, axis=1).mean()))
        if len(seg_norms) < 2: results.append({"M":int(M),"skipped_reason":"fewer than 2 segments"}); continue
        arr = np.array(seg_norms); rel = float(arr.std(ddof=0) / (abs(arr.mean()) + 1e-15) * 100.0)
        results.append({"M":int(M),"n_segments":len(seg_norms),"rel_variation_pct":rel,"pass_gate":bool(rel < gate_pct)})
    return {"gate_pct":gate_pct,"m_sweep":list(m_sweep),"results":results}

def compute_navigation_2d(ilr_matrix):
    X = np.asarray(ilr_matrix, float); T, K = X.shape; mu = X.mean(axis=0); Xc = X - mu
    if T < 2 or K < 2:
        return {"pc1_direction":[0.0]*K,"pc2_direction":[0.0]*K,"variance_explained":[0.0,0.0],
                "max_radius_pre_scale":0.0,"disk_scale_factor":0.85,"bary_xy":[[0.0,0.0] for _ in range(T)]}
    cov = (Xc.T @ Xc) / max(T - 1, 1); eigvals, eigvecs = np.linalg.eigh(cov)
    order = np.argsort(eigvals)[::-1]; eigvals = eigvals[order]; eigvecs = eigvecs[:, order]
    pc1 = eigvecs[:, 0]; pc2 = eigvecs[:, 1] if K >= 2 else np.zeros(K)
    total = float(np.clip(eigvals, 0.0, None).sum())
    ve = [float(eigvals[0]/total) if total > 0 else 0.0, float(eigvals[1]/total) if (total > 0 and K >= 2) else 0.0]
    raw = np.stack([Xc @ pc1, Xc @ pc2], axis=1); max_r = float(np.linalg.norm(raw, axis=1).max())
    scaled = (raw / max_r * 0.85).tolist() if max_r > 0 else [[0.0, 0.0] for _ in range(T)]
    return {"pc1_direction":pc1.tolist(),"pc2_direction":pc2.tolist(),"variance_explained":ve,
            "max_radius_pre_scale":max_r,"disk_scale_factor":0.85,
            "bary_xy":[[round(float(p[0]),6),round(float(p[1]),6)] for p in scaled]}
