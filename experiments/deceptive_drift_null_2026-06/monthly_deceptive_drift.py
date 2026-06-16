#!/usr/bin/env python3
"""
Monthly-grain deceptive-drift null (P2) — pipeline + self-test.

The annual-grain run (deceptive_drift_null.py) showed the deceptive (TV-quiet)
qualifier is GRAIN-DEPENDENT: at annual grain only Australia survives the null.
The packet's headline (Germany p = 0.0016) is a MONTHLY, deseasonalised, sliding-
window result. This module is that pipeline, built and self-tested, ready to run
the moment monthly EMBER data is supplied.

Pipeline:
  1. monthly compositions (T months x D fuels),
  2. deseasonalise the K_eff and TV series (remove month-of-year climatology),
  3. 6-month sliding-window smooth (sustained, not single-month, signal),
  4. the same smoothness-invariant LABEL-PERMUTATION null as the annual module
     (hold TV fixed; permute which steps are 'concentration'; statistic = mean
     TV-rank of concentration steps; low p => concentration is unusually quiet).

DATA NEEDED (not in the repo): monthly long-format EMBER generation per country
(Date + fuel columns). Drop it next to the annual CSVs and wire `load_monthly_ember`.
Until then the self-test validates the machinery on synthetic monthly data.

Self-test (PASS): deseasonalise removes the cycle; a planted deceptive signal is
detected after deseasonalising (p=0.0008); pure seasonality is NOT flagged (p=0.31).

Deterministic (fixed seed) -> hash-receipted. Author: Peter Higgins (human authorship
for claims); AI-assisted per HUF-STD-001. Honest-broker; claim tiers in RESULTS.md.
"""
from __future__ import annotations
import numpy as np
from scipy.stats import rankdata

SEED, NPERM, ALPHA = 20260612, 9999, 0.05


def k_eff(p):
    p = np.clip(p, 0, None); s = p.sum(); p = p / s if s > 0 else p; nz = p[p > 0]
    return float(np.exp(-(nz * np.log(nz)).sum()))


def tv(a, b):
    return 0.5 * float(np.abs(np.asarray(a) - np.asarray(b)).sum())


def deseasonalize(x, period=12):
    x = np.asarray(x, float); out = x.copy()
    for m in range(period):
        idx = np.arange(len(x)) % period == m
        out[idx] = x[idx] - x[idx].mean()           # remove month-of-year climatology
    return out


def rollmean(x, w=6):
    return np.convolve(np.asarray(x, float), np.ones(w) / w, mode="same")


def label_perm_null(dK, tvs, nperm=NPERM, seed=SEED):
    ranks = rankdata(tvs); conc = dK < 0; k = int(conc.sum()); n = len(tvs)
    if k == 0 or k == n:
        return None, 1.0
    obs = float(ranks[conc].mean()); rng = np.random.default_rng(seed); idx = np.arange(n); le = 0
    for _ in range(nperm):
        if ranks[rng.choice(idx, size=k, replace=False)].mean() <= obs:
            le += 1
    return obs, (1 + le) / (nperm + 1)


def deceptive_monthly(comp, window=6, deseason=True):
    """comp: (T months x D) monthly compositions -> (mean-TV-rank, p)."""
    T = comp.shape[0]
    keff = np.array([k_eff(comp[t]) for t in range(T)])
    tvs = np.array([tv(comp[t], comp[t - 1]) for t in range(1, T)])
    if deseason:
        keff = deseasonalize(keff); tvs = deseasonalize(np.r_[tvs[0], tvs])[1:]
    keff_s = rollmean(keff, window); tv_s = rollmean(np.r_[tvs[0], tvs], window)[1:]
    dK = np.diff(keff_s)
    return label_perm_null(dK, tv_s[:len(dK)])


def load_monthly_ember(path):
    """Stub for the real run: read a monthly long-format CSV (Date + fuel columns),
    closure-normalise each month, return (T x D). Wire when monthly EMBER lands."""
    import csv
    rows = []
    with open(path) as fh:
        r = csv.reader(fh); next(r)
        for row in r:
            v = np.array([float(x) for x in row[1:]]); s = v.sum()
            if s > 0:
                rows.append(v / s)
    return np.array(rows)


def _synth(planted, seed=0):
    rng = np.random.default_rng(seed); T, D = 144, 4    # 12 yrs monthly: [Coal, Gas, Solar, Wind]
    base = np.array([0.40, 0.30, 0.15, 0.15]); comps = []
    for t in range(T):
        p = base.copy()
        seas = 0.08 * np.sin(2 * np.pi * (t % 12) / 12)  # strong Solar seasonal cycle
        p[2] += seas; p[0] -= seas
        if planted and 84 <= t < 120:                    # pre-shock window: quiet concentration toward Coal
            sh = 0.004 * (t - 84); p[0] += sh; p[2] -= sh / 2; p[3] -= sh / 2
        p += rng.normal(0, 0.003, D); p = np.clip(p, 1e-4, None); comps.append(p / p.sum())
    return np.array(comps)


def self_test():
    ok = True
    x = np.tile(np.sin(2 * np.pi * np.arange(12) / 12), 12); d = deseasonalize(x)
    t0 = abs(d.mean()) < 1e-9 and np.std(d) < np.std(x)
    print(f"  [{'PASS' if t0 else 'FAIL'}] deseasonalize removes month-of-year cycle"); ok &= t0
    _, p = deceptive_monthly(_synth(True, 1)); t1 = p < ALPHA
    print(f"  [{'PASS' if t1 else 'FAIL'}] planted deceptive (deseason) p={p:.4f} -> {'PRESENT' if t1 else 'absent'} (expect PRESENT)"); ok &= t1
    _, p = deceptive_monthly(_synth(False, 2)); t2 = p >= ALPHA
    print(f"  [{'PASS' if t2 else 'FAIL'}] seasonal-only (deseason)    p={p:.4f} -> {'present' if p < ALPHA else 'absent'} (expect absent)"); ok &= t2
    return ok


if __name__ == "__main__":
    print("=== monthly deceptive-drift pipeline self-test ===")
    print("ALL PASS" if self_test() else "SELF-TEST FAILED")
    print("\nNOTE: supply monthly long-format EMBER data + wire load_monthly_ember() for the real P2 number.")
