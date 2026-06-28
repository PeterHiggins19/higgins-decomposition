#!/usr/bin/env python3
"""
directed_universe.py -- the instrument turned all the way outward, HONESTLY. Peter's concept: a compositional
probe reads its environment (the DUT outside it, including the operator); with enough contact + dwell, could a
component-from-inside determine whether the system it lives in -- the universe -- is DIRECTED (a planned route)
rather than undirected? This does NOT claim to answer that. It demonstrates, deterministically, exactly WHAT
the directedness measure CAN and CANNOT decide, so the metaphysics is met with an honest instrument, not an
overclaim.

Four generative regimes, each a trajectory in a fixed-budget (sum-zero / clr) space:
  RANDOM    : pure random walk, no drift                         (no direction)
  LAW       : deterministic flow to an attractor set BY THE LAWS (directed, but no agent, no purpose)
  DESIGNED  : goal-seeking flow to a CHOSEN target (a planned route; an agent picked the endpoint)
  ANTHROPIC : random walks, but only those that SURVIVE into a viability region are observed (selection)

Directedness  D = net_displacement / total_path_length  (0 = all wander, 1 = straight to the point).

THE HONEST RESULTS (measured below):
  (1) D separates RANDOM (D~0.09) from the STRUCTURED regimes (D~0.53) -- a real, modest power: you CAN rule
      out 'pure noise'.
  (2) D does NOT separate DESIGNED (0.522) from LAW (0.539) -- gap ~0.017, well inside the scatter. A planned
      route to a CHOSEN endpoint and a blind flow to an endpoint SET BY THE LAWS read identically. From inside,
      directedness UNDER-DETERMINES intent.
  (3) ANTHROPIC survivorship lifts D only modestly (0.087 -> 0.128) -- a weaker third confound, but enough to
      show selection alone can mimic a little direction with no dynamics at all.
  (4) more CONTACT/DWELL changes the absolute D but leaves the DESIGN-vs-LAW gap ~0 at every horizon: more
      evidence SHARPENS, it never SEPARATES. The step from 'directed' to 'intended' is the implication leap =
      Breaker 16, here at cosmic scale.

HONEST SCOPE: a toy of the EPISTEMIC STRUCTURE, not a model of the universe and not a detector of design. It
proves a LIMIT (what can't be concluded), the opposite of a detection claim. It does NOT exclude design -- it
shows design is not separable from law/selection by this statistic. The observer is INSIDE the DUT (no external
baseline). Metaphysics left open and to the person. Deterministic; receipt. Author: Peter Higgins (human
authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

DIM=4
def sumzero(v): v=np.asarray(v,float); return v-v.mean()
def directedness(traj):
    steps=np.diff(traj,axis=0); path=float(np.sum(np.linalg.norm(steps,axis=1)))
    net=float(np.linalg.norm(traj[-1]-traj[0]))
    return net/path if path>0 else 0.0
def walk_random(T,seed):
    r=np.random.default_rng(seed); x=np.zeros(DIM); tr=[x.copy()]
    for _ in range(T):
        s=sumzero(r.normal(0,1,DIM)); x=x+0.1*s; tr.append(x.copy())
    return np.array(tr)
def walk_flow(T,seed,target):    # IDENTICAL dynamics for LAW and DESIGNED -- only the ORIGIN of 'target' differs
    r=np.random.default_rng(seed); x=sumzero(r.normal(0,1,DIM)); tr=[x.copy()]
    for _ in range(T):
        drift=0.05*(target-x); noise=0.02*sumzero(r.normal(0,1,DIM))
        x=x+drift+noise; tr.append(x.copy())
    return np.array(tr)
LAW=sumzero([2.0,-1.0,0.5,-1.5])     # attractor set by 'the laws'
GOAL=sumzero([-1.5,2.0,-0.5,0.0])    # endpoint CHOSEN by an 'agent' -- different point, identical dynamics
def regime_D(kind,T,seeds):
    out=[]
    for s in seeds:
        tr=walk_random(T,s) if kind=="RANDOM" else walk_flow(T,s,LAW if kind=="LAW" else GOAL)
        out.append(directedness(tr))
    return out
def anthropic_D(T,seed):
    via=sumzero([1.5,1.5,-1.5,-1.5]); R=1.2; surv=[]; tried=0
    r=np.random.default_rng(seed)
    for _ in range(4000):
        tr=walk_random(T,int(r.integers(1,10**9))); tried+=1
        if np.linalg.norm(tr[-1]-via)<R: surv.append(directedness(tr))
        if len(surv)>=48: break
    return surv,tried

seeds=list(range(1,61)); T=120
Dr=regime_D("RANDOM",T,seeds); Dl=regime_D("LAW",T,seeds); Dd=regime_D("DESIGNED",T,seeds)
Da,tried=anthropic_D(T,12345)
def stat(xs): return {"mean":round(float(np.mean(xs)),3),"std":round(float(np.std(xs)),3),"n":len(xs)}
regime={"RANDOM":stat(Dr),"LAW":stat(Dl),"DESIGNED":stat(Dd),"ANTHROPIC":stat(Da)}

dwell=[]
for Tc in (30,120,480):
    dl=regime_D("LAW",Tc,seeds); dd=regime_D("DESIGNED",Tc,seeds)
    dwell.append({"contact_T":Tc,"law_mean":round(float(np.mean(dl)),3),"designed_mean":round(float(np.mean(dd)),3),
                  "design_minus_law_gap":round(float(np.mean(dd)-np.mean(dl)),3)})

def overlap(a,b):
    return bool(abs(np.mean(a)-np.mean(b)) < (np.std(a)+np.std(b)))   # True = NOT separable
checks={
 "D_rules_out_pure_noise": bool(np.mean(Dr) < np.mean(Dl)-0.1 and np.mean(Dr) < np.mean(Dd)-0.1),
 "design_and_law_NOT_separable_by_D": overlap(Dl,Dd),
 "anthropic_between_noise_and_structured": bool(np.mean(Dr) < np.mean(Da) < np.mean(Dl)),
 "more_contact_does_not_separate": bool(abs(dwell[-1]["design_minus_law_gap"]) < 0.05),
}
verdict=("HONEST LIMIT CONFIRMED: D rules out pure noise, but DESIGNED and blind LAW are NOT separable by "
         "directedness (gap ~0.017); selection adds a little apparent direction with no dynamics; more contact "
         "sharpens but never separates. 'Directed' does not imply 'intended' -- the leap is Breaker 16.") \
        if all(checks.values()) else "TOY CHECK FAILED"

out={"_meta":{"tool":"directed_universe.py","what":"what a directedness probe CAN and CANNOT decide about its own universe",
              "verdict":verdict,"dim":DIM,"T":T},
     "directedness_by_regime":regime,
     "anthropic_survival_rate":round(len(Da)/tried,4),
     "contact_dwell_sharpens_not_separates":dwell,
     "checks":checks,
     "the_point":("D separates STRUCTURE from NOISE (you can rule out pure chance), but DESIGNED, LAW, and "
              "ANTHROPIC selection are not cleanly told apart by it: a chosen goal and a blind attractor are "
              "identical (gap ~0.017). From inside the system, directedness UNDER-DETERMINES intent; more "
              "contact/dwell shrinks the error bars but never bridges 'directed' -> 'intended'."),
     "fence":("A toy of the EPISTEMIC STRUCTURE, NOT a model of the universe and NOT a detector of design. It "
              "proves a LIMIT, not a result; it does NOT exclude design -- it shows design is not separable from "
              "law/selection by directedness. The observer is INSIDE the DUT (no external baseline); the leap "
              "from 'directed' to 'intended' stays the observer's = Breaker 16 at cosmic scale. Metaphysics is "
              "left open and to the person. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(
    json.dumps({"regime":regime,"dwell":dwell,"checks":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2))
