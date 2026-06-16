"""
E-21 — announced multi-method zero / degeneracy registry (CN-TT v4, additive).

Detects the zero/degeneracy type per carrier, applies the appropriate method, and
ANNOUNCES the choice (per-carrier `methods` + diagnostic codes). Data-driven,
multi-method, announced — see `HCI-CNTT/DATA_PATH_AND_CHANNELS.md`.

Per-carrier methods (the CoDa zeros taxonomy):
  - structural_zero (carrier identically zero across the series) -> DROP to the
    subcomposition + GD-ZRC-CAL. A structural zero is real information; never impute.
  - constant (carrier never moves) -> DROP from the trajectory + GD-CNC-CAL.
  - has_zeros (sporadic / below detection) -> by `policy`:
        policy='bayes'  : Bayesian-multiplicative replacement (count-aware, ratio-
                          preserving) + GD-ZBM-CAL  [the CoDaWork-preferred treatment]
        detection_limit : multiplicative replacement + GD-ZRP-CAL
        else (honest)   : FLAG, do not impute + GD-ZUN-WRN
  - active -> unchanged.

Matrix-level SPARSITY REGIME DETECTOR: when the zero fraction is high, the CLR/ILR
log-ratio geometry is *replacement-dominated* — the helmsman/quaternion reads become
an artifact of the replacement choice, not the data (demonstrated empirically at 90%
zeros: the dominant movers flip from real taxa to imputed noise as the replacement
delta shrinks; see experiments/sparsity_microbiome_2026-06/). Above `sparsity_warn_at`
the registry emits GD-SPZ-WRN and recommends densifying BEFORE the log-ratio step
(prevalence filter / agglomerate-to-balances / Bayesian-multiplicative). The
zero-robust reads (K_eff, TV, diversity, the deceptive-drift null) stay valid as-is.

Honest-broker default (`policy='honest'`): never silently impute. Claim tier: Tier 1
— implemented + self-tested. Additive: the frozen oracle is untouched.
Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.
"""
from __future__ import annotations
import numpy as np


def carrier_zero_health(M, dl=None):
    """Classify each carrier (column): active / structural_zero / constant / has_zeros."""
    M = np.asarray(M, float); out = {}
    for j in range(M.shape[1]):
        col = M[:, j]
        if np.allclose(col, 0):
            out[j] = "structural_zero"
        elif np.ptp(col) == 0:
            out[j] = "constant"
        elif (col <= (dl if dl is not None else 0)).any() and (col > 0).any():
            out[j] = "has_zeros"
        else:
            out[j] = "active"
    return out


def matrix_sparsity(M):
    """Zero fraction over the whole matrix, and the worst per-sample zero fraction."""
    M = np.asarray(M, float)
    return {"zero_fraction": float((M <= 0).mean()) if M.size else 0.0,
            "per_sample_zero_fraction_max": float((M <= 0).mean(axis=1).max()) if M.size else 0.0}


def bayesian_multiplicative(M, alpha=0.5, depth=None):
    """
    Bayesian-multiplicative zero replacement (Dirichlet posterior; Jeffreys alpha=0.5).
    Counts in M (or shares + a sequencing `depth` -> pseudo-counts). Zeros receive the
    posterior mass alpha/(n+D*alpha); non-zero RATIOS are preserved (subcompositional
    coherence). Returns closed compositions. The count-aware treatment the CoDa
    community favours for sparse / sequencing data (Palarea-Albaladejo & Martin-Fernandez).
    """
    M = np.asarray(M, float); out = np.zeros_like(M); D = M.shape[1]
    for t in range(M.shape[0]):
        row = M[t]; cnt = row * depth if depth is not None else row.copy()
        n = cnt.sum()
        if n <= 0:
            out[t] = row; continue
        post = (cnt + alpha) / (n + D * alpha)               # Dirichlet posterior mean
        zero = cnt <= 0
        if zero.any() and (~zero).any():
            rz = post[zero].sum(); obs = cnt[~zero] / n
            res = np.zeros(D); res[zero] = post[zero]; res[~zero] = obs * (1.0 - rz)
            out[t] = res / res.sum()
        else:
            out[t] = cnt / n
    return out


def resolve_zeros(M, carriers=None, detection_limit=None, policy="honest",
                  sparsity_warn_at=0.5, bayes_alpha=0.5, depth=None):
    """
    Resolve zeros/degeneracies on a composition matrix M (rows=time/sample, cols=carriers).
    Returns (M_clean, kept_carriers, report). report['methods'] names the method per carrier;
    report['codes'] lists diagnostic codes; report['sparsity'] + report['sparsity_recommendation']
    carry the sparsity-regime verdict. policy in {'honest','engine'(via dl),'bayes'}.
    """
    M = np.asarray(M, float); D = M.shape[1]
    carriers = list(carriers) if carriers is not None else list(range(D))
    health = carrier_zero_health(M, detection_limit)
    methods, codes, keep = {}, [], []
    for j in range(D):
        h, name = health[j], carriers[j]
        if h == "structural_zero":
            methods[name] = "dropped:structural_zero"; codes.append("GD-ZRC-CAL")
        elif h == "constant":
            methods[name] = "dropped:constant"; codes.append("GD-CNC-CAL")
        else:
            keep.append(j)
            if h == "has_zeros":
                if policy == "bayes":
                    methods[name] = f"replaced:bayesian_multiplicative(alpha={bayes_alpha:g})"; codes.append("GD-ZBM-CAL")
                elif detection_limit is not None:
                    methods[name] = f"replaced:multiplicative(dl={detection_limit:g})"; codes.append("GD-ZRP-CAL")
                else:
                    methods[name] = "flagged:has_zeros_no_dl(not imputed)"; codes.append("GD-ZUN-WRN")
            else:
                methods[name] = "unchanged"
    Mk = M[:, keep]; kept = [carriers[j] for j in keep]
    spk = matrix_sparsity(Mk); recommendation = None
    if spk["zero_fraction"] >= sparsity_warn_at:                # sparsity-regime detector
        codes.append("GD-SPZ-WRN")
        recommendation = (
            f"sparsity {spk['zero_fraction']:.0%} (>= {sparsity_warn_at:.0%}) -- the CLR/ILR log-ratio geometry is "
            "REPLACEMENT-DOMINATED: helmsman/quaternion reads become an artifact of the replacement choice, not the data. "
            "Densify BEFORE the log-ratio step: (1) prevalence filter (keep parts present in >= X% of samples); "
            "(2) agglomerate / use phylogenetic balances (SBP / tree atlas); or (3) policy='bayes' (Bayesian-multiplicative, "
            "count-aware). The zero-robust reads (K_eff, TV, diversity, the deceptive-drift null) remain valid as-is.")
    if policy == "bayes" and Mk.size:
        Mk = bayesian_multiplicative(Mk, alpha=bayes_alpha, depth=depth)
    elif detection_limit is not None and Mk.size:
        dl = float(detection_limit); Mk = Mk.copy()
        for t in range(Mk.shape[0]):
            row = Mk[t]; z = row <= dl
            if z.any() and (~z).any():
                row[z] = dl; row[~z] = row[~z] * (1.0 - dl * z.sum() / max(row[~z].sum(), 1e-300))
            Mk[t] = row
    s = Mk.sum(axis=1, keepdims=True); s[s == 0] = 1.0; Mk = Mk / s
    report = {"methods": methods, "codes": sorted(set(codes)), "kept": kept,
              "dropped": [carriers[j] for j in range(D) if j not in keep],
              "policy": policy, "sparsity": spk, "sparsity_recommendation": recommendation}
    return Mk, kept, report


def _self_test():
    ok = True; rng = np.random.default_rng(0); C = [f"t{i}" for i in range(6)]
    clean = rng.dirichlet([3] * 6, size=10)
    Mk, kept, rep = resolve_zeros(clean, C)
    ok &= (kept == C) and all(v == "unchanged" for v in rep["methods"].values()) and np.allclose(Mk, clean)
    M = clean.copy(); M[:, 2] = 0.0; M = M / M.sum(1, keepdims=True)
    _, kept, rep = resolve_zeros(M, C); ok &= ("t2" not in kept) and "GD-ZRC-CAL" in rep["codes"]
    M = clean.copy(); M[:, 1] = 0.25
    _, kept, rep = resolve_zeros(M, C); ok &= ("t1" not in kept) and "GD-CNC-CAL" in rep["codes"]
    # sparse matrix -> GD-SPZ-WRN + bayes preserves nonzero ratios, no zeros, closed
    S = np.zeros((20, 6))
    for t in range(20):
        S[t, 0] = rng.uniform(.4, .6); S[t, 1] = rng.uniform(.3, .5)
        for j in range(2, 6):
            if rng.random() < 0.1:
                S[t, j] = rng.uniform(.01, .05)
    S = S / S.sum(1, keepdims=True)
    _, _, rep = resolve_zeros(S, C); ok &= "GD-SPZ-WRN" in rep["codes"] and rep["sparsity"]["zero_fraction"] > 0.5
    Mk, kept, rep = resolve_zeros(S, C, policy="bayes", depth=10000)
    nz = np.where(S[0] > 0)[0]
    pre = S[0][nz[0]] / S[0][nz[1]]; post = Mk[0][kept.index(C[nz[0]])] / Mk[0][kept.index(C[nz[1]])]
    ok &= (Mk > 0).all() and np.allclose(Mk.sum(1), 1) and np.isclose(pre, post, rtol=1e-6)
    _, _, rep = resolve_zeros(clean, C); ok &= "GD-SPZ-WRN" not in rep["codes"]
    return ok


if __name__ == "__main__":
    import sys
    print("zero_methods self-test:", "ALL PASS" if _self_test() else "FAILED")
    sys.exit(0 if _self_test() else 1)
