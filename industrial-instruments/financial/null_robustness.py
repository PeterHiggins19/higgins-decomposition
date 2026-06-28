#!/usr/bin/env python3
"""
Composition-level time-permutation null for the regime changes — robustness for the study.

Question: are the regime changes more than time would produce by chance? We hold the composition
fixed and permute the ORDER of the days, destroying temporal structure, then re-detect regimes with
the same detector. If the real series has genuine temporal organisation, it shows more regime changes
than the permuted null.

RESULT (seed 7, 2000 permutations, mean+2sd step detector):
  REAL regime changes ............. 5
  NULL mean ....................... 2.19  (sd 1.53; 95th pct 5; 99th 6; max 8)
  exceedance p(null >= real) ...... 0.081

Honest reading: the real series carries MORE regime structure than a typical time-shuffle (2.2), and
sits at the null's 95th percentile — suggestive temporal organisation, NOT a strong anomaly
(p ~= 0.08). Consistent with a diffusive, rebalancing system: the value of the reading is in the
*dated locations* and the *directional motion* (arrow of intent), not in any claim of anomalous regime
density. Descriptive, not predictive; not advice. Reproducible: numpy + the engine; deterministic seed.

Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker.
"""
import numpy as np, csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
HS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HS, "Hs-Kinematics"))
import hs_kinematics_engine as eng

rows = [r for r in open(os.path.join(HERE, "sp500_sectors.csv")) if r.strip()]
rd = list(csv.reader(rows)); M = np.array([[float(x) for x in r[1:]] for r in rd[1:]])
real = len(eng.regimes(M))
rng = np.random.default_rng(7); cnt = np.array([len(eng.regimes(M[rng.permutation(M.shape[0])])) for _ in range(2000)])
print(f"REAL regime changes: {real}")
print(f"NULL (2000 time-permutations): mean {cnt.mean():.2f}  sd {cnt.std():.2f}  95th {np.percentile(cnt,95):.0f}  99th {np.percentile(cnt,99):.0f}  max {cnt.max()}")
print(f"exceedance p(null >= real): {np.mean(cnt>=real):.4f}")
