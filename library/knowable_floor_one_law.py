#!/usr/bin/env python3
"""
knowable_floor_one_law.py -- agenda C2: is the knowable-sample floor ONE law? Honest version, after a first
attempt revealed a real distinction:

  PRECISION floor (averaging): relative error ~ sigma/sqrt(N), roughly INDEPENDENT of dimension -- NOT linear.
  IDENTIFIABILITY floor: to determine a d-parameter relational signature you need N >= d independent samples;
    below d it is under-determined (manufactured), at/above d it locks. THIS is linear in d, slope ~1, and it is
    the floor the project keeps meeting (the observability 'resolution = mesh-1', the language read 5%->20%, the
    stress sheet, max-power): a signature of intrinsic dimension d needs ~d looks to be knowable.

So the unifying law is the IDENTIFIABILITY floor N*(d) ~ d (one law); precision is a separate, dimension-flat
axis (the dwell x contact term). Measured floors {3:3,5:5,8:7,12:11,20:19,30:28}; slope 0.934; R^2 0.999;
receipt 15c13d43b16fb8cf. HONEST: synthetic; demonstrates the shared SHAPE, not a re-derivation of each domain's
constant. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26.
Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
rng=np.random.default_rng(20260626); LOCK=0.30
def floor_for(d):
    beta=rng.standard_normal(d)
    for N in range(1,4*d+20):
        errs=[]
        for _ in range(20):
            A=rng.standard_normal((N,d)); y=A@beta+0.05*rng.standard_normal(N)
            est=np.linalg.lstsq(A,y,rcond=None)[0]
            errs.append(float(np.linalg.norm(est-beta)/(np.linalg.norm(beta)+1e-9)))
        if np.median(errs)<LOCK: return N
    return None
dims=[3,5,8,12,20,30]; floors={d:floor_for(d) for d in dims}
ds=np.array([d for d in dims if floors[d]]); ns=np.array([floors[d] for d in dims if floors[d]],float)
A=np.vstack([ds,np.ones_like(ds)]).T; slope,intercept=np.linalg.lstsq(A,ns,rcond=None)[0]
pred=A@np.array([slope,intercept]); ss_res=float(np.sum((ns-pred)**2)); ss_tot=float(np.sum((ns-ns.mean())**2)); r2=1-ss_res/ss_tot
checks={"floor_each":bool(all(floors[d] for d in dims)),"linear":bool(r2>0.97),"slope_near_1":bool(0.8<slope<1.5)}
res={"floors":{int(d):floors[d] for d in dims},"slope":round(float(slope),3),"r2":round(float(r2),3),"checks":checks}
receipt=hashlib.sha256(json.dumps({"f":res["floors"],"s":res["slope"],"c":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
verdict=("ONE LAW: the IDENTIFIABILITY floor N*(d) is LINEAR in intrinsic dimension at slope %.3f/dim (R^2 %.3f) "
   "with a sharp lock near N=d; precision (averaging) is the separate, dimension-flat dwell x contact axis." %(slope,r2)) \
   if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"knowable_floor_one_law.py","what":"the knowable-sample floor as one law (identifiability ~ d)",
              "verdict":verdict,"receipt_sha256":receipt},
     "identifiability_floor_by_dimension":res["floors"],"slope_per_dim":res["slope"],"linearity_R2":res["r2"],
     "two_axes":"DIMENSION sets the identifiability floor N*~d (one law); SAMPLES/contact set precision ~sigma/sqrt(N) (dimension-flat).",
     "honest_note":"a first attempt tested the PRECISION floor (averaging) and correctly found it dimension-independent; the linear law is identifiability.",
     "checks":checks,
     "fence":"Synthetic; demonstrates the shared SHAPE, not a re-derivation of each domain's constant. Peter is the sole gate; nothing posted."}
if __name__=="__main__": print(json.dumps(out,indent=2))
