#!/usr/bin/env python3
"""make_produced_water.py -- TRANSPARENT SYNTHETIC generator for Study 2
(the CoDaWork-2026-referenced oil & gas produced-water composition).
NOT real samples: a clearly-labelled, plausible Appalachian-Basin-style
produced-water major-ion composition (mg/L) ordered by sample DEPTH, used to
demonstrate the Hs (CN-TT) compositional read. Public verification target:
the USGS National Produced Waters Geochemical Database (Engle et al.), cited
in the study README. Models the structure described by Engle, Venzor Nava &
Sanchez, CoDaWork 2026 (p.18): produced water with major + trace ions, many
missing/censored values, becoming Na-Cl brine with depth across a formation
boundary. Fixed seed for reproducibility.

Carriers (major ions): Na Cl Ca Mg SO4 HCO3 K  (D=7), ordered shallow->deep.
A formation boundary near sample 24 (step change). A couple of below-detection
SO4 zeros in the deep brine to exercise the engine's zero-treatment.
"""
import numpy as np, csv, sys
rng = np.random.default_rng(20260611)
N = 40
rows = []
for i in range(N):
    f = i / (N - 1)                      # 0 (shallow) -> 1 (deep)
    form = 1.0 if i >= 24 else 0.0       # formation boundary step
    Na   = 8000 + 27000 * f + 4000 * form
    Cl   = 14000 + 76000 * f + 9000 * form
    Ca   = 800 + 11000 * f + 1500 * form
    Mg   = 300 + 1200 * f
    SO4  = max(0.0, 600 - 560 * f - 80 * form)     # falls to ~0 in deep brine
    HCO3 = max(1.0, 400 - 340 * f - 40 * form)
    K    = 120 + 580 * f
    vals = np.array([Na, Cl, Ca, Mg, SO4, HCO3, K], float)
    vals *= rng.lognormal(0, 0.04, vals.size)      # multiplicative noise
    if i in (33, 37):
        vals[4] = 0.0                              # below-detection SO4 (censored -> zero)
    rows.append([300 + 2700 * f] + [round(float(v), 2) for v in vals])

with open(sys.argv[1] if len(sys.argv) > 1 else "produced_water.csv", "w", newline="") as fp:
    w = csv.writer(fp); w.writerow(["depth_m", "Na", "Cl", "Ca", "Mg", "SO4", "HCO3", "K"])
    for r in rows: w.writerow(r)
print("wrote produced_water.csv", N, "samples; major ions mg/L; ordered by depth")
