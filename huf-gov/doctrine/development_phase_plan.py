#!/usr/bin/env python3
"""
The two-phase development roadmap as a deterministic phase assignment (receipted).
  PHASE 1 (now)   : publish ALL the science -- principle + public-physics framings + receipted demos.
  PHASE 2 (later) : offer the REFINED TUNED versions to those who benefit the larger industry as a whole,
                    through a steward, on a broad-benefit criterion (export rules respected; defer upward).
  INTERNAL        : strategy/offer/value/political prose -- never the public surface; by choice.
Phase derives from the export disposition (OPEN -> Phase1; REVIEW/STEWARD applied -> Phase2; strategy -> Internal).
Author: Peter Higgins; AI-assisted per HUF-STD-001. Not legal/financial advice; Peter is the sole gate.
"""
import hashlib, json
import numpy as np

ASSETS = [  # (asset, stream, disposition, kind)
 ("principle / P-series math anchor",        "MATH","OPEN","science"),
 ("public-physics framings (coherence law, blindness suite, dim-is-the-message)","MATH","OPEN","science"),
 ("method + conformance (HS-EPS-1/GOLD-1)",  "MATH","OPEN","science"),
 ("EUV concept (public physics + method)",   "INDUSTRY","OPEN","science"),
 ("open-data composition demo",              "INDUSTRY","OPEN","science"),
 ("SMT / fiber / coherence demos",           "INDUSTRY","OPEN","science"),
 ("EUV tuned advanced-node yield recipe",    "GOVERNANCE","STEWARD","tuned_applied"),
 ("constellation/space-SSA tuned applied",   "GOVERNANCE","STEWARD","tuned_applied"),
 ("quantum-photonics / packaging tuned applied","INDUSTRY","REVIEW","tuned_applied"),
 ("fiber/6G/robotics tuned applied",         "INDUSTRY","REVIEW","tuned_applied"),
 ("the offer / email / package",             "GOVERNANCE","STEWARD","strategy"),
 ("value / political / world analyses",      "GOVERNANCE","STEWARD","strategy"),
]

def phase(disp, kind):
    if kind=="strategy": return "INTERNAL (by choice)"
    if disp=="OPEN": return "PHASE 1 -- publish now"
    return "PHASE 2 -- offer tuned, later, to broad-industry beneficiaries"

def main():
    rows=[{"asset":a[0],"stream":a[1],"phase":phase(a[2],a[3])} for a in ASSETS]
    out={
     "roadmap":"Two-phase development: PHASE 1 publish all the science now; PHASE 2 offer refined tuned versions later to those who benefit the larger industry as a whole.",
     "phase_1_now":[r["asset"] for r in rows if r["phase"].startswith("PHASE 1")],
     "phase_2_later":[r["asset"] for r in rows if r["phase"].startswith("PHASE 2")],
     "internal_by_choice":[r["asset"] for r in rows if r["phase"].startswith("INTERNAL")],
     "phase2_beneficiary_criterion":"'benefits the larger industry as a whole' = broad public/industry benefit (NOT narrow private capture), delivered THROUGH a legitimate steward (national governance / standards body / public-good institution), export rules respected (defer sensitive upward), favouring whoever advances the whole field's trust+quality layer.",
     "the_bridge":"Phase 1 enables Phase 2: publishing the science builds verifiable trust and starts the diffusion lead; the tuned versions then follow to broad benefit, and the early-mover/standard-layer logic (momentum model) means the head start compounds for the prepared steward without ever making the tuned how-to a free-for-all.",
     "governance":"Phase 1 is CLEARED to publish (fundamental-research/public-domain), but Peter executes the push -- no AI push. Phase 2 is steward-gated and broad-benefit. Nothing auto-pushed; Peter is the sole gate; not legal/financial advice."
    }
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
