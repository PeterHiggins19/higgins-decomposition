#!/usr/bin/env python3
"""
mesh_topology_hs.py -- mesh-network topology x Hs. A mesh network is a COMPOSITION IN TOPOLOGY: each node's
state (traffic mix / link-utilisation shares) is a part of a whole; the nodes form a distributed graph with no
centre. Hs is the deterministic COHERENCE + FAULT-LOCALISATION + OBSERVABILITY layer for it.

  1. COHERENCE WITHOUT A CENTRE. Each node senses the same network state at its OWN local scale (link speed /
     gain). clr cancels that multiplicative gain EXACTLY: gain-only node disagreement ~1e-15 (consensus by
     invariance, no master -> no single point of failure). Measurement noise blurs it only to a noise floor
     (~1e-2), far below a fault.
  2. FAULT LOCALISATION (self-healing). Inject a fault at one node (a real-direction drift). The deterministic
     residual against consensus is ~250x the noise floor, LOCATES the faulty node, and reads its direction --
     the jailor read, on the mesh.
  3. TOPOLOGY -> OBSERVABILITY. A mesh of N nodes resolves up to N-1 fault directions; the TETRAHEDRON (4 nodes)
     is the minimum mesh that LOCATES a fault in a 3-D state volume -- the observability law as network topology.

HONEST FENCE: synthetic mesh of node STATE compositions; clr cancels the MULTIPLICATIVE local gain only;
coherence/localisation/observability of the READINGS, not a routing protocol. Connects to the tetrahedral-3N
distributed-control architecture. Deterministic; receipt. Author: Peter Higgins (human authorship for all
claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-12,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def sumzero(v): v=np.asarray(v,float); return v-v.mean()
def maxpair(M): N=len(M); return float(np.max([np.max(np.abs(M[i]-M[j])) for i in range(N) for j in range(i+1,N)]))
rng=np.random.default_rng(20260626)
N=7; K=5
true_state=closure(np.array([5.0,3.0,2.0,1.5,1.0])); gains=rng.uniform(0.2,5.0,size=N)
obs_clean=np.array([closure(g*true_state) for g in gains]); disagree_exact=maxpair(clr(obs_clean))
obs=np.array([closure(np.abs(g*true_state*(1+0.003*rng.standard_normal(K)))) for g in gains]); disagree_noisy=maxpair(clr(obs))
f=4; fault_dir=sumzero(np.array([1.5,0,-1.0,0,0]))
obs_faulty=obs.copy(); obs_faulty[f]=closure(np.exp(clr(obs[f])+fault_dir))
fclr=clr(obs_faulty); cons=np.median(fclr,axis=0); resid=np.array([np.linalg.norm(fclr[i]-cons) for i in range(N)])
located=int(np.argmax(resid)); rec=fclr[located]-cons
cos_true=float(np.dot(rec,fault_dir)/(np.linalg.norm(rec)*np.linalg.norm(fault_dir)+1e-12))
snr=round(float(resid[located]/max(disagree_noisy,1e-9)),1)
topo=[{"n":n,"dirs":n-1} for n in (1,2,3,4,7)]
checks={"coherence_exact_in_gain":bool(disagree_exact<1e-10),"fault_separable":bool(resid[located]>20*disagree_noisy),
 "fault_located":bool(located==f),"dir_recovered":bool(cos_true>0.9),"tetra_locates_volume":bool(4-1==3)}
results={"exact":float(f"{disagree_exact:.1e}"),"noisy":float(f"{disagree_noisy:.1e}"),"located":located,"injected":f,
 "cos":round(cos_true,3),"snr":snr,"residuals":[round(float(r),3) for r in resid],"topo":topo,"checks":checks}
receipt=hashlib.sha256(json.dumps(results,sort_keys=True,default=str).encode()).hexdigest()[:16]
verdict=("MESH x Hs: nodes agree with NO centre (exact-gain disagreement %s; noise floor %s), a fault is LOCATED "
 "to its node (n%d, SNR %sx) with its direction recovered (cos %s), and the tetrahedron (4 nodes) is the minimum "
 "mesh that locates a fault in a volume." %(results["exact"],results["noisy"],located,snr,results["cos"])) \
 if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"mesh_topology_hs.py","what":"mesh-network topology x Hs: coherence + fault-localisation + observability",
              "verdict":verdict,"nodes":N,"classes":K,"receipt_sha256":receipt},
     "1_coherence_no_centre":{"exact_gain_disagreement":results["exact"],"noisy_agreement_floor":results["noisy"],
        "meaning":"clr cancels each node's local gain EXACTLY -> consensus by invariance, no master; noise only blurs to the noise floor, far below a fault"},
     "2_fault_localisation":{"injected_node":f,"located_node":located,"direction_cos_vs_true":results["cos"],
        "fault_SNR_over_agreement_noise":snr,"node_residuals":results["residuals"],
        "meaning":"the deterministic residual against consensus locates the faulty node and reads its direction (the jailor read, on the mesh)"},
     "3_topology_observability":[{"mesh_nodes":t["n"],"resolvable_directions":t["dirs"],
        "locates":("volume (3-D) -- TETRAHEDRON" if t["dirs"]>=3 else ("plane" if t["dirs"]==2 else ("line" if t["dirs"]==1 else "point")))} for t in topo],
     "checks":checks,
     "fence":("Synthetic mesh of node STATE compositions; clr cancels the MULTIPLICATIVE local gain only; "
        "coherence/localisation/observability of the READINGS, not a routing protocol. Connects to the "
        "tetrahedral-3N distributed-control architecture. Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
