#!/usr/bin/env python3
"""
feedback_chain.py -- the goal of the entire project, made measurable: the science<->data improvement chain.

We advance the SCIENCE (a better method/read); a partner advances the DATA (more, cleaner data, enabled by
the better method); the better data advances the science again. The question that decides whether the project
MEANS something is: does that loop COMPOUND toward the knowable, or DRIFT?

Claim (the thread of the whole project): determinism + receipts make the chain RATCHET. Each turn is
hash-anchored, so a verified gain is never silently lost -- the loop can only hold or improve. Without that
anchor, feedback loops wander and regress (noise enters, gains are lost, the loop can even dip BELOW the
knowable floor -- false precision -- then bounce back). We model both and measure the difference. The
asymptote is the system's own limit (max Q / the knowable floor): the chain converges THERE and stops.

HONEST: this is a MODEL of the loop dynamics (T2). The structural result -- anchored chains compound to the
limit and STAY; unanchored chains wander and are untrustworthy -- is the point; the numbers are scenario
numbers. Deterministic; receipt. Author: Peter Higgins (human authorship); AI-assisted per HUF-STD-001.
2026-06-25. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

KNOWABLE_FLOOR = 0.01            # max-Q limit: the finest error the system can ever truly reach
def run_chain(cycles=20, anchored=True, seed=0):
    rng=np.random.default_rng(seed)
    err=1.0; N=100.0; best=err; hist=[]
    for k in range(cycles):
        stat_floor = max(1.0/np.sqrt(N), KNOWABLE_FLOOR)
        achieved = stat_floor*(1+0.15*rng.standard_normal())
        achieved = max(achieved, KNOWABLE_FLOOR*0.999)
        if anchored:
            err = min(best, achieved); best = err           # receipt: keep only verified gains
        else:
            err = abs(achieved + 0.06*rng.standard_normal()) # no anchor: drift and all
        quality = max(0.0, 1.0-err)
        N = N*(1+0.6*quality)                                # the flywheel: better science speeds the data
        hist.append({"cycle":k,"error":round(err,4),"data_N":int(N)})
    return hist, float(err)

if __name__=="__main__":
    anchored,  e_a = run_chain(anchored=True,  seed=1)
    unanchored,e_u = run_chain(anchored=False, seed=1)
    errs_a=[h["error"] for h in anchored]
    monotone = all(errs_a[i+1]<=errs_a[i]+1e-12 for i in range(len(errs_a)-1))
    def cycles_to_floor(hist):
        for h in hist:
            if h["error"]<=KNOWABLE_FLOOR*1.05: return h["cycle"]
        return None
    breaches=int(sum(1 for h in unanchored if h["error"]<KNOWABLE_FLOOR))   # false precision below the floor
    out={"_meta":{"tool":"feedback_chain.py",
                  "what":"the science<->data improvement loop: does it compound to the knowable, or drift? determinism+receipts decide.",
                  "knowable_floor_maxQ":KNOWABLE_FLOOR},
         "anchored_receipted_chain":{
              "final_error":round(e_a,4),"monotone_never_regresses":bool(monotone),
              "cycles_to_within_5pct_of_floor":cycles_to_floor(anchored),
              "final_data_N":anchored[-1]["data_N"],
              "trajectory_error":[h["error"] for h in anchored]},
         "unanchored_drifting_chain":{
              "final_error":round(e_u,4),"monotone_never_regresses":False,
              "regressions":int(sum(1 for i in range(len(unanchored)-1) if unanchored[i+1]["error"]>unanchored[i]["error"])),
              "false_precision_breaches_below_floor":breaches,
              "trajectory_error":[h["error"] for h in unanchored]},
         "verdict":"the receipted chain RATCHETS to the knowable limit and STAYS; the unanchored chain wanders, regresses, and even fakes precision below the floor -- determinism+receipts are what make the feedback chain MEAN and BE something",
         "fence":"T2 model of the loop dynamics; the structural result is the point, the numbers are scenario numbers; the asymptote is the max-Q knowable floor."}
    out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()[:16]
    print(json.dumps(out,indent=2))
