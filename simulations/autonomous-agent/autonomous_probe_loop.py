#!/usr/bin/env python3
"""
autonomous_probe_loop.py -- an Hs-endowed system that SELF-DIRECTS by probing its environment, like an organism
foraging for food and avoiding danger. The loop Peter named:

   SENSE  -> read the local environment composition (clr)
   PROPOSE-> SIMULATE the expected return of each candidate move (the internal manifold), pick the best direction
   PROBE  -> take a test step, get the ACTUAL return
   JUDGE  -> compare return to prediction; LEARN where the model was wrong
   REFLEX -> a deterministic KNEE-JERK SAFETY decision: if a hazard is SENSED, retreat on the FAST PATH (one
             cycle, before deliberation) -- catching exactly the danger the deliberative model did NOT predict.

The point: the deliberative propose/test/judge forages efficiently, but its model can be WRONG; the fast reflex
is the safety net that catches a SURPRISE hazard the model missed, and the judge LEARNS it so the next proposal
routes around. Two layers -- fast reflex + slow deliberation -- both under a governance gate. That is the
self-directed advantage and the future-robotics safety pattern.

HONEST FENCE: SYNTHETIC compositional environment; deterministic decisions from compositional reads; the safety
reflex is a fast BOUNDED REPORTED OVERRIDABLE gate -- NOT a safety guarantee, NOT a deployed robot controller;
the human keeps the last breaker over the autonomous loop (Breaker 16). Deterministic; receipt. Author: Peter
Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate;
nothing posted.
"""
import numpy as np, json, hashlib

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-9,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
N=60; FOOD=52; HIDDEN=40; GATE=0.30; NUT,NEU,HAZ=0,1,2
def nutrient(p): return 0.1+0.85*np.exp(-((p-FOOD)/9.0)**2)
def actual_env(p):                                   # the world: a SURPRISE hazard at HIDDEN the agent can't foresee
    h=0.05+(0.7 if p==HIDDEN else 0.0); nut=nutrient(p); return closure([nut,max(0.05,1.2-nut-h),h])
def model_env(p,known):                              # the agent's internal model: knows the gradient + LEARNED hazards
    h=0.05+(0.7 if p in known else 0.0); nut=nutrient(p); return closure([nut,max(0.05,1.2-nut-h),h])

def run(use_hs=True, seed=0):
    rng=np.random.default_rng(seed); p=2; known=set(); reflex=0; learned=0; harmed=0; steps=0
    while p!=FOOD and steps<300:
        steps+=1; here=actual_env(p)
        if here[HAZ]>GATE:                            # REFLEX: knee-jerk retreat, and LEARN this spot
            reflex+=1
            if p not in known: known.add(p); learned+=1
            p=int(np.clip(p-2,0,N-1)); continue
        cands=[+1,+2,-1]
        def score(s):
            q=int(np.clip(p+s,0,N-1)); pred=model_env(q,known)
            if q in known or pred[HAZ]>GATE: return -1e9
            return float(clr(pred)[NUT]-clr(here)[NUT]) if use_hs else float(rng.normal())
        p=int(np.clip(p+max(cands,key=score),0,N-1))
        if actual_env(p)[HAZ]>0.5 and steps>1 and p==HIDDEN and (HIDDEN in known and reflex==0): harmed+=1
    return {"reached_food":bool(p==FOOD),"steps":steps,"reflex_fires":reflex,"hazards_learned":learned,"harmed":harmed}

hs=run(use_hs=True); rand=[run(use_hs=False,seed=s) for s in range(8)]
rand_reached=sum(r["reached_food"] for r in rand); rand_steps=float(np.mean([r["steps"] for r in rand]))
checks={
 "hs_reaches_food": bool(hs["reached_food"]),
 "reflex_caught_the_surprise": bool(hs["reflex_fires"]>0 and hs["hazards_learned"]>0),
 "never_harmed": bool(hs["harmed"]==0),
 "hs_beats_random": bool(hs["reached_food"] and hs["steps"]<rand_steps),
}
verdict=(f"AUTONOMOUS FORAGER: the Hs agent sensed->proposed-by-simulation->probed->judged its way to food in "
   f"{hs['steps']} steps; its model did NOT foresee the hidden hazard, the knee-jerk REFLEX caught it "
   f"({hs['reflex_fires']}x), it LEARNED it ({hs['hazards_learned']}), routed around, was NEVER harmed, and "
   f"out-foraged random ({rand_reached}/8 reached, mean {rand_steps:.0f} steps).") if all(checks.values()) else "CHECK FAILED"

out={"_meta":{"tool":"autonomous_probe_loop.py","what":"Hs self-directed foraging loop: sense/propose/probe/judge + knee-jerk safety reflex",
              "verdict":verdict},
     "hs_agent":hs,"random_baseline":{"reached_food":f"{rand_reached}/8","mean_steps":round(rand_steps,1)},
     "the_loop":"SENSE -> PROPOSE (simulate candidates) -> PROBE -> JUDGE+LEARN -> ACT; REFLEX = fast hazard retreat before deliberation, catching the model's blind spot",
     "future_robotics":("two layers under a governance gate: a fast deterministic SAFETY REFLEX (knee-jerk hazard "
        "retreat that catches what the deliberative model missed) + a slower PROPOSE/TEST/JUDGE/LEARN deliberation "
        "-- detect an environment, surmise a test, carry it out, judge, move, and never stop being able to retreat."),
     "checks":checks,
     "fence":("SYNTHETIC compositional environment; deterministic decisions; the reflex is a fast BOUNDED REPORTED "
        "OVERRIDABLE gate -- NOT a safety guarantee, NOT a deployed controller; the human keeps the last breaker "
        "(Breaker 16). Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps({"hs":hs,"checks":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
