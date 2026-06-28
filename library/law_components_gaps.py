#!/usr/bin/env python3
"""
law_components_gaps.py -- Peter's method, made an instrument: "the system is under law -- measure the LAW and
the COMPONENTS and the GAPS, coherently." Don't chase the unanswerable (higher-dimensional control); instead
fit what IS lawful, read the components, and treat the RESIDUAL -- the part the law+components don't explain --
as the RETURN SIGNAL that says where to refine. Like BACK-EMF: the motor's own motion returns a voltage that
tells you its state and steers the control; here the system's own unexplained return tells you WHERE the gap
opened, and you work BACKWARDS to it and focus there.

Pipeline:
  1. LAW       : fit the smooth lawful trajectory of the composition (per-clr-component trend).
  2. COMPONENTS: read the clr components.
  3. GAP       : residual = clr(data) - clr(law).  <-- the back-EMF return signal.
  4. LOCALIZE  : which component carries the gap (energy argmax) and WHEN (the window) -- work backwards.
  5. COHERENCE : locate the gap by TWO independent statistics; they must agree (triad-style cross-check).
  6. REFINE    : feed the localized gap back into the law (absorb it); residual energy must drop sharply
                 (the back-EMF loop: read return -> correct -> re-read).

The point: you do NOT re-derive the known law; you attack the GAP, located by the return signal. That is the
diagnostic-constructive duality -- the same math that finds the flaw refines the system.

HONEST SCOPE: synthetic demonstrator of the METHOD; the "law" here is a fitted smooth model, real systems need
the domain's actual law; back-EMF is an analogy for the return signal, not a circuit claim. Deterministic;
receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26.
Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

rng=np.random.default_rng(7)
T,D=100,5
INJ_COMP=2; WIN=(40,61)   # the true gap: a bump in component 2 over t in [40,60]

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(M):
    M=closure(M); g=np.exp(np.mean(np.log(M),-1,keepdims=True)); return np.log(M/g)
def clr_inv(C): return closure(np.exp(C))

# --- the lawful system: a slow deterministic clr drift per component (the LAW) ---
t=np.arange(T)
law_clr=np.zeros((T,D))
slopes=np.array([0.6,-0.3,0.1,-0.2,-0.2])/T*6   # lawful linear trends in clr (sum ~ handled by clr centering)
inter=np.array([0.4,-0.2,0.3,-0.3,-0.2])
for j in range(D): law_clr[:,j]=inter[j]+slopes[j]*t
law_clr-=law_clr.mean(1,keepdims=True)          # keep in clr (sum-zero)
law=clr_inv(law_clr)

# --- the true data = law + an injected GAP in INJ_COMP over WIN + small noise ---
gap_true=np.zeros((T,D))
bump=np.zeros(T); bump[WIN[0]:WIN[1]]=0.9*np.hanning(WIN[1]-WIN[0])   # a localized anomaly
gap_true[:,INJ_COMP]=bump
noise=0.02*rng.standard_normal((T,D)); noise-=noise.mean(1,keepdims=True)
data_clr=law_clr+gap_true+noise
data=clr_inv(data_clr)

# --- 1-2. MEASURE THE LAW (fit per-component linear trend) + COMPONENTS ---
A=np.vstack([np.ones(T),t]).T
law_fit_clr=np.zeros((T,D))
for j in range(D):
    coef,_,_,_=np.linalg.lstsq(A,clr(data)[:,j],rcond=None)
    law_fit_clr[:,j]=A@coef
law_fit_clr-=law_fit_clr.mean(1,keepdims=True)

# --- 3. THE GAP = residual (the back-EMF return signal) ---
resid=clr(data)-law_fit_clr
energy_before=float(np.sum(resid**2))

# --- 4. LOCALIZE: which component (energy) and WHEN (window) ---
comp_energy=np.sum(resid**2,axis=0)
loc_comp_energy=int(np.argmax(comp_energy))
t_energy=np.sum(resid**2,axis=1)
thr=t_energy.mean()+t_energy.std()
flagged=np.where(t_energy>thr)[0]
loc_window=(int(flagged.min()),int(flagged.max())+1) if len(flagged) else (0,0)

# --- 5. COHERENCE: a SECOND, independent statistic must point to the same component ---
loc_comp_maxdev=int(np.argmax(np.max(np.abs(resid),axis=0)))   # max single-step deviation route
coherent=bool(loc_comp_energy==loc_comp_maxdev==INJ_COMP)

# --- 6. REFINE (back-EMF loop): absorb the localized gap into the law, re-read residual ---
refine=np.zeros((T,D))
seg=slice(loc_window[0],loc_window[1])
refine[seg,loc_comp_energy]=resid[seg,loc_comp_energy]        # model the located gap and subtract it
resid2=resid-refine
energy_after=float(np.sum(resid2**2))
drop=round(1-energy_after/energy_before,3)

checks={
 "gap_component_recovered": bool(loc_comp_energy==INJ_COMP),
 "two_routes_agree_coherent": coherent,
 "window_overlaps_truth": bool(loc_window[0]<WIN[1] and WIN[0]<loc_window[1]),
 "refinement_drops_residual": bool(energy_after < 0.4*energy_before),
}
verdict=("METHOD HOLDS: law fit, components read, the GAP (return signal) localized to the right component+"
         f"window by two coherent routes, and feeding it back refined the system (residual -{int(drop*100)}%).") \
        if all(checks.values()) else "METHOD CHECK FAILED"

out={"_meta":{"tool":"law_components_gaps.py","what":"measure law + components + gaps coherently; the return signal refines the system",
              "verdict":verdict,"T":T,"D":D},
     "truth":{"injected_component":INJ_COMP,"injected_window":list(WIN)},
     "law":"fitted per-component linear clr trend (the lawful, known part -- not re-derived, just measured)",
     "gap_localization":{"by_energy_component":loc_comp_energy,"by_maxdev_component":loc_comp_maxdev,
              "window":list(loc_window),"component_energy":[round(float(e),3) for e in comp_energy]},
     "back_emf_refinement":{"residual_energy_before":round(energy_before,3),"residual_energy_after":round(energy_after,3),
              "fraction_removed":drop,"reading":"the return signal, fed back, refined the law -- the gap is the lever"},
     "checks":checks,
     "the_method":("Don't re-derive the law and don't chase the unmeasurable. Fit the law, read the components, "
              "and let the GAP (residual = the back-EMF return signal) point to where to refine. Work BACKWARDS "
              "from the total to where the gap opened, focus there, and verify coherently with a second route."),
     "fence":("Synthetic demonstrator of the METHOD; the 'law' is a fitted smooth model (real systems need the "
              "domain's actual law); 'back-EMF' is an analogy for the return signal. The residual localizes a "
              "GAP, it does not name its CAUSE -- attributing the gap is the operator's leap (Breaker 16). "
              "Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(
    json.dumps({"loc":out["gap_localization"],"refine":out["back_emf_refinement"],"checks":checks},
               sort_keys=True,default=str).encode()).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2))
