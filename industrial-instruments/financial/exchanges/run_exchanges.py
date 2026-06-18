#!/usr/bin/env python3
"""
Cross-exchange diagnostic — run the Hs reading across several exchanges' sector/holdings compositions
and place each in Compositional Character Space. Drop one CSV per exchange (rows=dates, cols=parts
summing to one) into ./data/ and run. Same data -> same readings -> same hashes; descriptive, not
advice. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker.

Currently real: the in-repo US S&P 500 sector series (data/US_SP500_sectors.csv). Other exchanges are
staged — supply the public series named in DATA_SOURCES_EXCHANGES.md and re-run; they appear
automatically.
"""
import numpy as np, csv, os, sys, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
HS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HS, "Hs-Kinematics"))
import hs_kinematics_engine as eng

def load(p):
    rows = [r for r in open(p) if r.strip()]; rd = list(csv.reader(rows)); nm = rd[0][1:]
    M = np.array([[float(x) for x in r[1:]] for r in rd[1:]]); return M, nm

def character(coh, pe, rank):
    directed = 0.5 * (coh + pe)
    if directed >= 0.5 and rank < 2.5: return "Ballistic"
    if directed >= 0.30: return "Contested"
    if rank >= 3.0: return "Turbulent"
    return "Diffusive"

def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(DATA, "*.csv"))):
        M, nm = load(p); out = eng.run(M, nm); k = out["kinematics_and_dynamics"]; sp = out["spectral_modes"]
        arrow = k["arrow_of_intent_NAV__momentum_PHYS"]; coh = float(arrow["coherence"])
        pe = float(k["course_directness_NAV__path_efficiency_PHYS"]); rank = float(sp["degrees_of_freedom_NAV__effective_dimensionality_PHYS"])
        wp = out["navigation_reads"]["waypoints_NAV__phase_transitions_PHYS"]
        rows.append({"exchange": os.path.basename(p).replace(".csv", ""), "T": int(M.shape[0]), "D": int(M.shape[1]),
            "helmsman_to": arrow["to"][:2], "helmsman_from": arrow["from"][:2], "coherence": round(coh, 3),
            "path_eff": round(pe, 3), "eff_dim": round(rank, 2), "regimes": len(wp),
            "character": character(coh, pe, rank), "hash": out["content_hash"][:12]})
    print(f"{'exchange':28} {'T':>4} {'D':>3} {'coh':>5} {'p_eff':>6} {'eff_dim':>7} {'reg':>4}  character")
    for r in rows:
        print(f"{r['exchange']:28} {r['T']:>4} {r['D']:>3} {r['coherence']:>5.3f} {r['path_eff']:>6.3f} {r['eff_dim']:>7.2f} {r['regimes']:>4}  {r['character']}")
    json.dump(rows, open(os.path.join(HERE, "cross_exchange_results.json"), "w"), indent=2)
    return rows

if __name__ == "__main__":
    main()
