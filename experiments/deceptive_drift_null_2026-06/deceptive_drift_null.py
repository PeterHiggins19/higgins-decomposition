#!/usr/bin/env python3
"""
Deceptive-drift null model — the defensible classification for P2 / S1-7.

"Deceptive drift" = the energy mix CONCENTRATING (effective number of fuels K_eff
falling) while step-to-step motion (total-variation distance TV) stays QUIET.
The size/velocity view looks calm; the structure is shifting underneath.

The open question (Q3 / S1-7): you cannot call a country "deceptive" without a null
that separates a real concentration-while-quiet coupling from chance.

This module ships TWO nulls and shows why one is wrong:

  (A) NAIVE composition time-shuffle  -- permute the YEAR ORDER of the compositions
      and recompute. THIS IS BIASED: the true trajectory is the SMOOTHEST ordering
      (consecutive years are similar => low TV everywhere), so any TV-based statistic
      is confounded. Empirically every country returns p ~= 1. Kept here as a
      documented trap, not a result.

  (B) LABEL-PERMUTATION null (recommended) -- smoothness-invariant. Hold the TV
      values fixed; permute WHICH steps are labelled "concentration" (K_eff falling).
      Statistic = mean TV-rank of the concentration steps (low rank = concentration
      is quiet = deceptive). This tests exactly the deceptive hypothesis
      (concentration coupled to quietness) without the smoothness bias.

Deterministic (fixed seed) -> reproducible -> hash-receipted. Self-test included.

Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.
Honest-broker; claim tiers in RESULTS.md. K_eff and TV are zero-robust (no CLR),
so the early-years Solar/Wind structural zeros need no imputation here.
"""
from __future__ import annotations
import csv, os, json, hashlib
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "..", "data", "Energy", "EMBER_pipeline_ready"))
COUNTRIES = ["AUS", "CHN", "DEU", "FRA", "GBR", "IND", "JPN", "USA", "WLD"]
PRIOR_DECK = {"AUS", "CHN", "GBR", "IND", "JPN"}   # the deck's "5 of 9 present" (provenance inconsistent)
SEED, NPERM, ALPHA = 20260612, 9999, 0.05


def k_eff(p):
    p = np.clip(np.asarray(p, float), 0, None); s = p.sum()
    p = p / s if s > 0 else p; nz = p[p > 0]
    return float(np.exp(-(nz * np.log(nz)).sum()))          # exp(Shannon entropy) = effective # of fuels


def tv(a, b):
    return 0.5 * float(np.abs(np.asarray(a) - np.asarray(b)).sum())   # total-variation distance


def step_series(comp):
    T = comp.shape[0]
    dK = np.array([k_eff(comp[t]) - k_eff(comp[t - 1]) for t in range(1, T)])
    tvs = np.array([tv(comp[t], comp[t - 1]) for t in range(1, T)])
    return dK, tvs


def label_perm_null(dK, tvs, nperm=NPERM, seed=SEED):
    """Recommended, smoothness-invariant. Lower p => concentration steps are unusually quiet."""
    ranks = rankdata(tvs)                       # 1 = quietest step
    conc = dK < 0; k = int(conc.sum()); n = len(tvs)
    if k == 0 or k == n:
        return {"stat": None, "p": 1.0, "n_conc": k, "n_div": n - k}
    obs = float(ranks[conc].mean())
    rng = np.random.default_rng(seed); idx = np.arange(n); le = 0
    for _ in range(nperm):
        if ranks[rng.choice(idx, size=k, replace=False)].mean() <= obs:
            le += 1
    return {"stat": obs, "p": (1 + le) / (nperm + 1), "n_conc": k, "n_div": n - k}


def naive_timeshuffle_null(comp, nperm=NPERM, seed=SEED):
    """BIASED demo: smoothness confound makes p ~= 1. Do not use for classification."""
    def S(c):
        dK, tvs = step_series(c); med = np.median(tvs)
        return float((np.clip(-dK, 0, None) * (tvs <= med)).sum())
    rng = np.random.default_rng(seed); obs = S(comp); T = comp.shape[0]; ge = 0
    for _ in range(nperm):
        if S(comp[rng.permutation(T)]) >= obs:
            ge += 1
    return {"S": obs, "p": (1 + ge) / (nperm + 1)}


def load_ember(code):
    fn = [f for f in os.listdir(DATA) if f.startswith(f"ember_{code}_")][0]
    rows = []
    with open(os.path.join(DATA, fn)) as fh:
        r = csv.reader(fh); next(r)
        for row in r:
            v = np.array([float(x) for x in row[1:]]); s = v.sum()
            if s > 0:
                rows.append(v / s)                 # closure to the simplex
    return np.array(rows)


def self_test():
    rng = np.random.default_rng(7); ok = True
    cases = [
        ("planted-deceptive", np.r_[[-0.1] * 8, [0.1] * 12],
         np.r_[rng.uniform(0.005, 0.03, 8), rng.uniform(0.05, 0.15, 12)], True),
        ("loud-concentration", np.r_[[-0.1] * 8, [0.1] * 12],
         np.r_[rng.uniform(0.05, 0.15, 8), rng.uniform(0.005, 0.03, 12)], False),
        ("random", rng.normal(0, 0.1, 20), rng.uniform(0.01, 0.15, 20), False),
    ]
    for name, dK, tvs, expect in cases:
        r = label_perm_null(dK, tvs); got = r["p"] < ALPHA
        ok &= (got == expect)
        print(f"  [{'PASS' if got == expect else 'FAIL'}] {name:18} p={r['p']:.4f} -> {'PRESENT' if got else 'absent'} (expect {'PRESENT' if expect else 'absent'})")
    return ok


def main():
    print("=== self-test (label-permutation null) ===")
    assert self_test(), "self-test failed"
    print("\n=== EMBER 9 countries — deceptive-drift label-permutation null (annual, whole record) ===")
    print(f"{'cty':4} {'#conc':>5} {'#div':>4} {'meanTVrank':>10} {'p':>7}  class    prior(deck)")
    out = {}
    for c in COUNTRIES:
        comp = load_ember(c); dK, tvs = step_series(comp); r = label_perm_null(dK, tvs)
        cls = "PRESENT" if r["p"] < ALPHA else "absent"
        out[c] = {"p": r["p"], "stat": r["stat"], "n_conc": r["n_conc"], "n_div": r["n_div"], "class": cls}
        print(f"{c:4} {r['n_conc']:>5} {r['n_div']:>4} {r['stat']:>10.2f} {r['p']:>7.4f}  {cls:7}  {'present' if c in PRIOR_DECK else 'absent'}")
    present = sorted(c for c in COUNTRIES if out[c]["class"] == "PRESENT")
    print(f"\nlabel-null PRESENT (p<{ALPHA}): {present} ({len(present)} of 9)")
    print(f"prior deck '5 of 9'         : {sorted(PRIOR_DECK)}  (not null-robust at annual grain)")
    payload = json.dumps({"method": "label_permutation", "seed": SEED, "nperm": NPERM,
                          "alpha": ALPHA, "p": {c: out[c]["p"] for c in COUNTRIES}}, sort_keys=True)
    print("content_sha256:", hashlib.sha256(payload.encode()).hexdigest())
    return out


if __name__ == "__main__":
    main()
