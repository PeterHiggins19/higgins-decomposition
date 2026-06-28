#!/usr/bin/env python3
"""
corruption_detector_long_chain.py -- detect a TAKEN-OVER node in a long-chain system, by compositional coherence.
Big systems are corrupted by attacking ONE node and taking it over; if the attacker is careful to keep the
AGGREGATE metrics unchanged (the dashboards stay green), a totals monitor never sees it. But a stealthy takeover
that preserves the total necessarily changes the RATIOS -- and that is exactly the deceptive drift Hˢ is built
to catch. The full-system coherence check is, therefore, a corruption detector.

Demonstration on a real public substrate (Ball geochemistry, 10-oxide compositions; the nodes are real
compositions):
  * a chain of N coherent nodes (one legitimate relational state + small honest variation);
  * ONE node is taken over -- replaced with a DIFFERENT real composition, rescaled to preserve the chain's
    median TOTAL (the stealthy attack: the aggregate is untouched);
  * detector 1 = TOTALS monitor (flag a node whose total deviates) -> BLIND (total preserved);
  * detector 2 = Hˢ COHERENCE (Aitchison distance of each node's clr to the chain's clr-centroid; flag the
    outlier) -> detects AND localizes the corrupted node.

DEFENSIVE only -- this DETECTS tampering; it is not an attack tool. Deterministic; receipt. Author: Peter
Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. Peter is the sole gate;
nothing posted. Science is public; application to any specific named system is held separate and Peter-gated.
"""
import csv, os, numpy as np, hashlib, json
HS=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
rows=list(csv.reader(open(os.path.join(HS,"data","Geochemistry","ball_oxides_composition.csv"))))
X=np.array([[float(v) for v in r] for r in rows[1:] if all(float(v)>0 for v in r)])
xhash=hashlib.sha256(X.tobytes()).hexdigest()[:16]; D=X.shape[1]
def closure(v): v=np.clip(v,1e-9,None); return v/v.sum(-1,keepdims=True)
def clr(v): c=closure(v); return np.log(c)-np.log(c).mean(-1,keepdims=True)
def aitch(a,b): return float(np.linalg.norm(clr(a)-clr(b)))
def trial(seed,N=12):
    r=np.random.default_rng(seed)
    centroid=X[r.integers(len(X))]
    nodes=[centroid*np.exp(r.normal(0,0.05,D)) for _ in range(N)]
    med_total=float(np.median([n.sum() for n in nodes])); k=int(r.integers(N))
    intruder=X[r.integers(len(X))]
    while aitch(intruder,centroid)<0.5: intruder=X[r.integers(len(X))]
    nodes[k]=intruder/intruder.sum()*med_total                       # stealthy: preserve the total
    tt=np.array([n.sum() for n in nodes])
    tot_flag=int(np.argmax(np.abs(tt-med_total))) if np.max(np.abs(tt-med_total))>0.02*med_total else -1
    cc=np.mean([clr(n) for n in nodes],0); dist=np.array([np.linalg.norm(clr(n)-cc) for n in nodes])
    hs_flag=int(np.argmax(dist))
    return (hs_flag==k and dist[hs_flag]>3*np.median(np.delete(dist,hs_flag))), (tot_flag==k)
M=400; res=[trial(s) for s in range(M)]
hs=float(np.mean([r[0] for r in res])); tot=float(np.mean([r[1] for r in res]))
checks={"Hs_detects_and_localizes":bool(hs>0.9),"totals_monitor_is_blind":bool(tot<0.2),"Hs_beats_totals":bool(hs>tot+0.6)}
res_d={"substrate":"Ball geochemistry (real public, 10 oxides)","input_hash":xhash,"trials":M,"chain_nodes":12,
 "attack":"stealthy node takeover -- one node replaced, rescaled to preserve the chain's TOTAL (aggregate stays green)",
 "Hs_coherence_detection_rate":round(hs,3),"totals_monitor_detection_rate":round(tot,3)}
master=sha({"o":res_d,"c":checks})
verdict=(f"COHERENCE = CORRUPTION DETECTOR. A stealthy node takeover that preserves the aggregate is caught by Hˢ "
   f"compositional coherence {res_d['Hs_coherence_detection_rate']*100:.1f}% of the time and LOCALIZED to the node, "
   f"while a totals monitor catches {res_d['totals_monitor_detection_rate']*100:.0f}% -- it is blind because the "
   "total was preserved. A node-takeover that fools the dashboards cannot fool the ratios. The full-system "
   "coherence check is a corruption detector for any long-chain system.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"corruption_detector_long_chain.py","what":"detect a taken-over node in a long chain by compositional coherence",
              "receipt_sha256":master,"verdict":verdict},
     "result":res_d,"checks":checks,
     "long_chain_systems":["supply chains","power/energy grids","data pipelines","determinism receipt/hash chains",
        "distributed ledgers","sensor/fleet networks","the project's own journal chain"],
     "fence":("DEFENSIVE: this DETECTS tampering; not an attack tool. Synthetic chain over REAL compositions; the "
        "method assumes a coherent legitimate chain and strictly-positive parts (E-21). It catches stealthy "
        "(aggregate-preserving) takeover via the ratios; a takeover that also matches the relational structure is "
        "not separable. Science public; application to any specific named system is separate + Peter-gated. Peter "
        "is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
