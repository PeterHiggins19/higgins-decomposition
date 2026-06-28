#!/usr/bin/env python3
"""
Sparsity scope boundary — what survives 90% zeros, and what does not.

Microbiome OTU tables are ~90% zeros. This demonstrates, on synthetic sparse data,
the boundary the engine must respect:

  * ZERO-ROBUST reads (K_eff, TV, the deceptive-drift null, diversity) survive 90%
    zeros — they take no logarithm (0*log0 = 0), so they need no imputation and are
    independent of any replacement choice.
  * The CLR LOG-RATIO geometry (helmsman / quaternion / CNQ) does NOT survive raw
    90% zeros: with a fixed-delta replacement the "structure" becomes an artifact of
    delta — as delta shrinks, the dominant movers flip from the real abundant taxa to
    imputed rare-taxa noise, and the CLR radius inflates. The replacement delta becomes
    a tuning knob that drives the answer.

Conclusion: at high sparsity, densify BEFORE the log-ratio step (prevalence filter /
agglomerate to phylogenetic balances / Bayesian-multiplicative). The registry now
detects this regime and emits GD-SPZ-WRN (HCI-CNTT/engine/zero_methods.py).

Deterministic. Author: Peter Higgins (human authorship for claims); AI-assisted per
HUF-STD-001. Honest-broker; claim tiers in RESULTS.md.
"""
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(7)
D, T, CORE = 200, 40, 8


def clr(P):
    P = np.clip(P, 1e-300, None); L = np.log(P); return L - L.mean(1, keepdims=True)


def k_eff(p):
    p = np.clip(p, 0, None); s = p.sum(); p = p / s if s > 0 else p; nz = p[p > 0]
    return float(np.exp(-(nz * np.log(nz)).sum()))


def make_sparse():
    M = np.zeros((T, D))
    for t in range(T):                                   # CORE abundant taxa carry the real drift
        base = rng.dirichlet(np.linspace(6, 2, CORE)); drift = 0.010 * t
        base[0] += drift; base[CORE - 1] = max(base[CORE - 1] - drift, 0.001)
        M[t, :CORE] = base / base.sum() * 0.6
    for j in range(CORE, D):                             # rare taxa: present in 0-3 random samples
        for t in rng.choice(T, size=rng.integers(0, 4), replace=False):
            M[t, j] = rng.uniform(0.0005, 0.01)
    return M / M.sum(1, keepdims=True)


def with_delta(M, frac):
    X = M.copy()
    for j in range(X.shape[1]):
        col = X[:, j]; pos = col[col > 0]
        if pos.size:
            X[col <= 0, j] = frac * pos.min()
    return X / X.sum(1, keepdims=True)


def top_movers(M):
    H = clr(M); dH = np.diff(H, axis=0); return list(np.argsort(-np.abs(dH).sum(0))[:5])


def main():
    M = make_sparse()
    print(f"D={D} taxa, T={T} samples | zeros = {(M==0).mean():.1%}")
    Mk = M[:, ~(M == 0).all(0)]
    print(f"after structural-zero drop: D={Mk.shape[1]} taxa, zeros = {(Mk==0).mean():.1%} (still ~90%)\n")
    print("CLR log-ratio 'structure' vs the imputation delta (the artifact):")
    print(f"  {'delta':>10}  {'top-5 movers':>22}  {'mean|CLR| radius':>16}")
    for frac in (0.65, 0.10, 0.01):
        Xf = with_delta(Mk, frac)
        print(f"  {frac:>10}  {str(top_movers(Xf)):>22}  {np.linalg.norm(clr(Xf),axis=1).mean():>16.2f}")
    keff = np.array([k_eff(Mk[t]) for t in range(T)])
    print(f"\nK_eff (zero-robust, delta-independent): {keff[0]:.2f} -> {keff[-1]:.2f}  (reads the real concentration)")
    tvs = np.array([0.5 * np.abs(Mk[t] - Mk[t - 1]).sum() for t in range(1, T)])
    dK = np.diff(keff); ranks = rankdata(tvs); conc = dK < 0; k = int(conc.sum())
    if 0 < k < len(tvs):
        obs = ranks[conc].mean(); r2 = np.random.default_rng(0)
        p = (1 + sum(ranks[r2.choice(len(tvs), k, replace=False)].mean() <= obs for _ in range(9999))) / 10000
        print(f"deceptive-drift label-null: runs fine at 90% zeros, p={p:.4f}")
    print("\nVerdict: zero-robust reads survive; the log-ratio geometry is delta-dominated -> densify first.")


if __name__ == "__main__":
    main()
