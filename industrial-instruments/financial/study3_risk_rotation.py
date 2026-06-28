#!/usr/bin/env python3
"""
Study 3 — risk rotation. Amalgamate the ten S&P sectors into the three Morningstar super-sectors
(Cyclical / Sensitive / Defensive) and read the macro risk balance with Hs. A different altitude on the
same real composition: where Study 1 reads ten sectors in detail, this reads the risk-on/risk-off balance
at the exact low-D end (D=3). Deterministic; hash-receipted; descriptive, not advice. Author: Peter
Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker.

Super-sector grouping (Morningstar):
  Cyclical  = Financials, Consumer Discretionary, Materials  (+ Real Estate, absent here)
  Sensitive = Communication Services, Energy, Industrials, Information Technology
  Defensive = Consumer Staples, Health Care, Utilities
"""
import numpy as np, csv, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
HS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HS, "Hs-Kinematics"))
import hs_kinematics_engine as eng

GROUPS = {
    "Cyclical":  ["Financials", "Cons Discretionary", "Materials"],
    "Sensitive": ["Comm Services", "Energy", "Industrials", "Information Tech"],
    "Defensive": ["Cons Staples", "Health Care", "Utilities"],
}

def main():
    rows = [r for r in open(os.path.join(HERE, "sp500_sectors.csv")) if r.strip()]
    rd = list(csv.reader(rows)); nm = rd[0][1:]; M = np.array([[float(x) for x in r[1:]] for r in rd[1:]])
    idx = {n: i for i, n in enumerate(nm)}
    names = list(GROUPS)
    S = np.column_stack([M[:, [idx[g] for g in GROUPS[k]]].sum(1) for k in names])
    out = eng.run(S, names); k = out["kinematics_and_dynamics"]; sp = out["spectral_modes"]; nav = out["navigation_reads"]
    ar = k["arrow_of_intent_NAV__momentum_PHYS"]
    summary = {
        "super_sectors": names,
        "shares_first": {n: round(float(S[0, i]), 4) for i, n in enumerate(names)},
        "shares_last": {n: round(float(S[-1, i]), 4) for i, n in enumerate(names)},
        "arrow_to": ar["to"], "arrow_from": ar["from"], "coherence": round(float(ar["coherence"]), 3),
        "path_eff": round(float(k["course_directness_NAV__path_efficiency_PHYS"]), 3),
        "eff_dim": round(float(sp["degrees_of_freedom_NAV__effective_dimensionality_PHYS"]), 2),
        "regimes": nav["waypoints_NAV__phase_transitions_PHYS"],
        "content_hash": out["content_hash"],
    }
    print(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    main()
