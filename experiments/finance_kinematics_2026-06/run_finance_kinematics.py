# Hs kinematics + diagnosis on a financial system (sector composition in motion).
# Drop in a REAL sector-weight CSV (rows=dates, cols=sectors) for present-conditions analysis.
import numpy as np, csv, sys
sys.path.insert(0, "../../Hs-Kinematics")
import hs_kinematics_engine as eng, hs_diagnosis as dx
p = sys.argv[1] if len(sys.argv)>1 else "../../HCI-CNT/experiments/extended/financial_sector/financial_sector_input.csv"
rows=[r for r in open(p) if r.strip()]; rd=list(csv.reader(rows)); nm=rd[0][1:]
M=np.array([[float(x) for x in r[1:]] for r in rd[1:]])
out=eng.run(M,nm); k=out["kinematics_and_dynamics"]
print("ARROW OF INTENT (momentum):", k["arrow_of_intent_NAV__momentum_PHYS"])
print("PATH EFFICIENCY (course directness):", k["course_directness_NAV__path_efficiency_PHYS"])
print("EFFECTIVE DIMENSIONALITY:", out["spectral_modes"]["degrees_of_freedom_NAV__effective_dimensionality_PHYS"])
print("WAYPOINTS (regime changes):", out["navigation_reads"]["waypoints_NAV__phase_transitions_PHYS"])
print("\nDIAGNOSIS:", dx.diagnose(M,nm)["narrative"])
