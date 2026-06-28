import hashlib, json, math
import numpy as np

# THE Q CONNECTION (Peter's keystone leap, captured + bridged). Q = Quality Factor = energy_stored/energy_dissipated
# per radian = a RATIO = the coherence of a resonator. Thiele-Small (Richard H. Small + Neville Thiele, ~1972):
# 1/Qts = 1/Qes + 1/Qms (electrical[magnet/coil] + mechanical[suspension] nodes combine RECIPROCALLY).
# BRIDGE (to the Hs coherence law, a5ceab9e): a resonator retains a coherent fraction rho = exp(-2*pi/Q) of its
# energy per cycle, so Q -> coherence rho -> Hs rejection (-10*log10(1-rho)). The loudspeaker's Q IS the coherence
# Hs reads. Deterministic; hash-receipted. T2 on the resonator physics; T3 on the compositional generalization.
def rho_per_cycle(Q): return math.exp(-2*math.pi/Q)
def rejection_dB(rho): return -10*math.log10(max(1-rho,1e-18))

def main():
    Qs=[2,5,10,50,200,1000,5000]
    ladder=[{"Q":Q,"coherent_fraction_rho_per_cycle":round(rho_per_cycle(Q),4),
             "Hs_rejection_dB(-10log10(1-rho))":round(rejection_dB(rho_per_cycle(Q)),1)} for Q in Qs]
    # node combination: electrical Qes + mechanical Qms -> total Qts (reciprocal sum); lowest-Q node dominates
    Qes,Qms=10.0,5.0; Qts=1/(1/Qes+1/Qms)
    out={
     "connection":"Q (Quality Factor) <-> coherence <-> the compositional log-ratio reading",
     "lineage":"Thiele-Small (Richard H. Small, Univ. Sydney + A.N. Thiele, ABC, ~1972): Q = energy stored / energy dissipated per radian = a RATIO; Qts total, Qes electrical (magnet/voice-coil), Qms mechanical (suspension); 1/Qts = 1/Qes + 1/Qms.",
     "the_leap":"Q is the universal QUALITY/COHERENCE ratio of a resonator across domains (electrical, mechanical, acoustic, OPTICAL cavity). The loudspeaker was assembled Q-by-Q node (magnetic->electrical->medium) until the chain was COHERENT. Hs generalizes this: read any system's Q-by-node composition and its coherence -- the same closure+log-ratio that reads the loudspeaker reads everything.",
     "Q_to_coherence_to_rejection (receipted bridge to a5ceab9e)":ladder,
     "node_combination":{
       "Qes_electrical":Qes,"Qms_mechanical":Qms,"Qts_total_reciprocal_sum":round(Qts,2),
       "reading":"Qts (3.33) is BELOW the lowest node -- the lossiest (lowest-Q) node DOMINATES the chain coherence (reciprocal sum = the min-Q / weakest-coherence node sets the whole, the helmsman of coherence). This is the compositional structure of Q-by-node assembly."
     },
     "falsifiable_tests":[
       "T1-able: derive Hs's coherence law -10log10(1-rho) from Q via rho=exp(-2pi/Q); confirm the resonator and the composition give the same rejection curve on real data.",
       "T2-able: read a real loudspeaker (or any chain of coupled resonators) as a composition of node-Qs; predict the system coherence from the min-Q rule; measure.",
       "Falsifier: if a system's measured coherence/rejection does NOT track its node-Q composition, the generalization fails there."
     ],
     "honest_note":"Q=energy ratio and rho=exp(-2pi/Q) are standard resonator physics (T2). The CONNECTION -- that Q is one instance of the compositional coherence Hs reads, and that the loudspeaker's Q-by-node assembly generalizes -- is Peter's leap, a tiered T3 SEED, falsifiable, not a claim. Richard H. Small credited as the lineage Peter extended."
    }
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
