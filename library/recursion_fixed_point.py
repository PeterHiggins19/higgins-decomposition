#!/usr/bin/env python3
"""
recursion_fixed_point.py -- agenda C1: what is the FIXED POINT of iterated self-reading? Hs reads Hs, the corpus
reads the corpus, the conference reads itself -- and the library note says "the read converges." Test it: iterate
a compositional self-map (read -> next state) and watch it converge to a fixed point.

Self-map: a system reads its own state and emits its next state via a compositional transition T (a coherent,
contractive read -- the system re-weights its parts by how each couples to the whole). Iterate x -> closure(T@x)
from any start. By the Perron-Frobenius / Banach picture this converges to a UNIQUE fixed point (the dominant
eigen-composition / the self-consistent read), independent of the start. We measure: convergence to the floor,
uniqueness (different starts -> same limit), and that the limit is a true fixed point (residual 0).

HONEST: a positive transition (coherent self-coupling) has a unique stationary composition; this demonstrates
the recursion CONVERGES and names its limit -- it does not claim every self-read map is contractive. Deterministic;
receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter
is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def aitch(a,b):
    ca=np.log(closure(a)); cb=np.log(closure(b)); ca-=ca.mean(); cb-=cb.mean(); return float(np.linalg.norm(ca-cb))
rng=np.random.default_rng(20260626); D=6
T=np.abs(rng.standard_normal((D,D)))+0.2                # coherent self-coupling (positive -> unique stationary)

def iterate(x0,iters=200):
    x=closure(x0); traj=[x.copy()]
    for _ in range(iters):
        x=closure(T@x); traj.append(x.copy())
    return np.array(traj)

starts=[closure(np.abs(rng.standard_normal(D))+0.05) for _ in range(5)]
limits=[iterate(s)[-1] for s in starts]
# convergence: step-to-step change at the end
conv=iterate(starts[0]); final_step=aitch(conv[-1],conv[-2])
# uniqueness: all starts reach the same limit
spread=max(aitch(limits[0],l) for l in limits[1:])
# fixed point: T applied to the limit returns the limit
fp_resid=aitch(closure(T@limits[0]),limits[0])
checks={
 "converges_to_floor": bool(final_step<1e-9),
 "unique_independent_of_start": bool(spread<1e-9),
 "limit_is_a_fixed_point": bool(fp_resid<1e-12),
}
verdict=(f"THE RECURSION HAS A FIXED POINT: iterated self-reading converges to a UNIQUE self-consistent "
   f"composition from any start (start-spread {spread:.0e}), it is an exact fixed point (T x* = x*, residual "
   f"{fp_resid:.0e}), reached to the floor (final step {final_step:.0e}). 'Hs reads Hs' converges -- and the "
   "limit is the eigen-composition the system settles into.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"recursion_fixed_point.py","what":"the fixed point of iterated self-reading (Hs on Hs converges)","verdict":verdict},
     "fixed_point":[round(float(x),4) for x in limits[0]],
     "convergence":{"final_step":float(f"{final_step:.0e}"),"uniqueness_spread":float(f"{spread:.0e}"),"fixed_point_residual":float(f"{fp_resid:.0e}")},
     "reading":"the recursion is a contraction to a unique stationary composition -- the self-consistent read the system converges to; the recursion does not run away, it settles.",
     "checks":checks,
     "fence":"A positive (coherent) self-coupling has a unique stationary composition; demonstrates the recursion CONVERGES + names its limit, not that every self-read map is contractive. Peter is the sole gate; nothing posted."}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps({"fp":out["fixed_point"],"conv":out["convergence"],"c":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
