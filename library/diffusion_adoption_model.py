#!/usr/bin/env python3
"""
diffusion_adoption_model.py -- "let entropy do the work", made honest. The war-game intuition translated:
adoption is NOT conquest, it is DIFFUSION down a real gradient. Model it with the conquest terms removed and
see what survives:

  - There is NO coercion term. Nothing pushes a field to adopt.
  - The ONLY drivers are CONTACT (dwell time) and the REAL, MEASURED advantage gradient, which exists only
    where the data is actually compositional (need > door). Where there is no gradient, there is NO spread --
    the friendly door is automatic, not enforced.
  - So adoption equilibrates (like heat) toward high uptake WHERE there is a genuine advantage, and stays put
    where there isn't. Entropy equilibrates; it does not conquer. Saturation is DWELL-TIME-LIMITED.

The "win by attrition / the other guy's bad choices cost him" idea is reported honestly as STANDING UNREALIZED
ADVANTAGE = the value a non-adopter leaves on the table where their data IS compositional -- self-chosen, never
imposed by us. We apply zero force; the gradient is the data's, the choice is theirs.

HONEST SCOPE: a T3 ILLUSTRATIVE model of a social process, deterministic so it is inspectable, NOT a prediction
of adoption or "domination". Falsifier: measure real adoption vs dwell time vs data-compositionality; if uptake
rises without a compositional gradient, or fields with no gradient still convert, the model is wrong. Author:
Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole
gate; nothing posted.
"""
import numpy as np, json, hashlib

DOOR = 0.45                       # below this 'need', data isn't compositional -> no real gradient (the door)
def advantage_gradient(need):     # the ONLY pull: the measured asymmetry, zero below the door
    return max(0.0, need - DOOR)

# three representative fields (from the world-composition map): far/high-need, near/mid, off-door
fields = {"far_high_need (e.g. clinical labs)": 0.82,
          "near_mid (e.g. energy mix)":         0.66,
          "off_door (e.g. timing/latency)":     0.19}

CONTACT = 0.15                    # dwell-time / contact rate per step (the lever) -- same for all, no targeting
STEPS = 40
COERCION = 0.0                    # there is no force term. stated explicitly and kept zero.

def run(need, a0=0.05):
    g = advantage_gradient(need); a = a0; traj=[round(a,4)]
    for _ in range(STEPS):
        # pure gradient diffusion toward saturation; + COERCION (which is 0); no push when g==0
        a = a + CONTACT*g*(1.0-a) + COERCION*(1.0-a)
        traj.append(round(a,4))
    standing_unrealized = round(g*(1.0-a), 4)   # value left on the table by non-adopters where data IS compositional
    return {"final_adoption": round(a,3), "gradient": round(g,3),
            "standing_unrealized_advantage": standing_unrealized,
            "trajectory_every10":[traj[i] for i in (0,10,20,30,40)]}

res = {name: run(need) for name,need in fields.items()}
total_force = COERCION * STEPS * len(fields)    # = 0 by construction

# dwell-time-to-threshold: how much contact a high-need field needs to cross 0.95 (Peter: "dwell time is the problem")
def steps_to(need, thr=0.95, a0=0.05):
    g=advantage_gradient(need); a=a0
    for k in range(1,5000):
        a=a+CONTACT*g*(1.0-a)
        if a>=thr: return k
    return None
dwell_to_sat = steps_to(0.82)

checks = {
 "off_door_did_not_convert": res["off_door (e.g. timing/latency)"]["final_adoption"] <= 0.06,
 "high_need_rose_substantially": res["far_high_need (e.g. clinical labs)"]["final_adoption"] >= 0.85,
 "saturation_is_dwell_time_limited": dwell_to_sat is not None and dwell_to_sat > STEPS,
 "zero_force_applied": total_force == 0.0,
 "no_gradient_no_spread": res["off_door (e.g. timing/latency)"]["gradient"] == 0.0,
}
verdict = ("DIFFUSION, NOT CONQUEST: spreads only where a real gradient exists, equilibrates with dwell time, "
           "zero force, no gradient -> no spread") if all(checks.values()) else "MODEL CHECK FAILED"

out = {"_meta":{"tool":"diffusion_adoption_model.py",
                "what":"adoption as gradient diffusion (let entropy do the work) -- coercion term removed and kept zero",
                "verdict":verdict,"door_threshold":DOOR,"coercion_term":COERCION,"total_force_applied":total_force},
       "by_field":res,
       "dwell_time_to_saturation_steps":dwell_to_sat,
       "checks":checks,
       "honest_reading":("Entropy EQUILIBRATES, it does not conquer. Adoption rises only where the data carries a "
                "real advantage gradient and only with contact/dwell time; off-door fields correctly do NOT "
                "convert (the friendly door, automatic). 'Attrition' = standing unrealized advantage a non-adopter "
                "leaves on the table where their data is compositional -- their self-chosen cost, never our force."),
       "fence":("T3 illustrative model of a social process, deterministic for inspectability; NOT a prediction of "
                "adoption or domination. The shape is assumed, not measured. Falsifier: measure real adoption vs "
                "dwell time vs compositionality. Adoption is by merit + invitation; the human keeps the gate. "
                "Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(
    json.dumps({"by_field":res,"checks":checks,"door":DOOR,"coercion":COERCION},sort_keys=True,default=str).encode()).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2))
