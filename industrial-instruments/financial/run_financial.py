#!/usr/bin/env python3
"""
Financial instrument — Hˢ kinematic reading of a financial system's composition.

This is NOT statistics and NOT a forecast. It is a deterministic reading of how a
*composition* (parts of a whole, tracked in order) is moving: who steers, where the
weight flows, in how many directions, and where the system reorganises. The stats are
someone else's work; this complements them with the vector map the system itself
generates. Hˢ reads; the meaning and any decision stay the expert's. Not investment advice.

Drop in any sector-weight / allocation / holdings CSV (rows = dates, cols = parts that
sum to a whole) and it runs the same way. Default = the in-folder S&P 500 sector series.

numpy + stdlib; deterministic; hash-receipted. Author: Peter Higgins (human authorship
for claims); AI-assisted per HUF-STD-001.
"""
import numpy as np, csv, sys, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "Hs-Kinematics"))
import hs_kinematics_engine as eng

def load(p):
    rows = [r for r in open(p) if r.strip()]
    rd = list(csv.reader(rows)); names = rd[0][1:]
    M = np.array([[float(x) for x in r[1:]] for r in rd[1:]])
    return M, names

def main():
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sp500_sectors.csv")
    M, names = load(p)
    out = eng.run(M, names)
    k = out["kinematics_and_dynamics"]
    nav = out["navigation_reads"]
    spec = out["spectral_modes"]
    summary = {
        "input": {"file": os.path.basename(p), "rows_dates": int(M.shape[0]), "parts_D": int(M.shape[1]), "parts": names},
        "arrow_of_intent": k["arrow_of_intent_NAV__momentum_PHYS"],
        "path_efficiency": k["course_directness_NAV__path_efficiency_PHYS"],
        "effective_dimensionality": spec["degrees_of_freedom_NAV__effective_dimensionality_PHYS"],
        "regime_changes": nav["waypoints_NAV__phase_transitions_PHYS"],
        "content_hash": out["content_hash"],
    }
    print(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    main()
