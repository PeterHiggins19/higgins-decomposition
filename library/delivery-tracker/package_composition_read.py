#!/usr/bin/env python3
"""
package_composition_read.py  --  Hs read on the delivery package itself (recursive: Hs-on-Hs).

Treats the whole deliverable (papers + concepts + instruments) as a composition and reads it with
the SAME machinery Hs uses on data: closure -> clr -> effective dimension -> helmsman -> per-item
Aitchison distance from the package barycenter (the ground state). The math (closure / clr /
effective dimension / distance) is EXACT (T1 mechanism); the INPUT weights are honest structural
estimates assembled from the corpus + the tracking log (T2 -- an organizational read, NOT measured
data). Fenced accordingly. Deterministic; emits a SHA-256 receipt of (inputs + outputs).

Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25.
Peter is the sole gate; nothing posted.
"""
import json, hashlib, math

# ---- the package: each item = (id, name, role, tier_weights (T1,T2,T3)) ------------------------
# role in {MATH (core theory), APP (application study), GOV (governance/doctrine),
#          COMM (communication/onboarding), INSTR (instrument/tooling/tracker)}
# tier_weights = honest split of how much of the item is measured(T1)/reasoned(T2)/vision(T3).
P = [
 ("P1","Exact D=4 quaternion tiling (arXiv)","MATH",(0.80,0.15,0.05)),
 ("P3","CN-TT deterministic engine (JOSS)","INSTR",(0.85,0.10,0.05)),
 ("P5","Compositional Character Space","APP",(0.55,0.35,0.10)),
 ("P6","Portfolio kinematics (finance)","APP",(0.55,0.30,0.15)),
 ("P7","Foundations / determinism boundary","MATH",(0.25,0.45,0.30)),
 ("P8_CMP","Compositional Message Principle","MATH",(0.60,0.30,0.10)),
 ("EITT","Entropy-invariant time transform","MATH",(0.45,0.35,0.20)),
 ("WI_micro","W-I microbiome witness","APP",(0.80,0.15,0.05)),
 ("WII_mud","W-II mudstone witness","APP",(0.80,0.15,0.05)),
 ("WIII_fleet","W-III Backblaze fleet witness","APP",(0.80,0.15,0.05)),
 ("blindness","The blindness suite","MATH",(0.55,0.30,0.15)),
 ("Q_conn","The Q (Quality Factor) connection","MATH",(0.30,0.45,0.25)),
 ("P2_diff","P2 dimensional differential engine (seed)","MATH",(0.20,0.30,0.50)),
 ("coherence","Coherence law / lasers","APP",(0.55,0.30,0.15)),
 ("fiber","Fiber x Hs future projects","APP",(0.35,0.35,0.30)),
 ("smt","SMT contact-point doctrine","APP",(0.50,0.30,0.20)),
 ("euv","EUV lithography x Hs","APP",(0.35,0.40,0.25)),
 ("constellation","SpaceX constellation proposal","APP",(0.30,0.35,0.35)),
 ("financial","Financial flagship case","APP",(0.55,0.30,0.15)),
 ("canada","Canada gov offering + open-data","GOV",(0.45,0.35,0.20)),
 ("world_money","World-monetary + COFER studies","APP",(0.65,0.25,0.10)),
 ("export_gov","Export/division governance","GOV",(0.30,0.45,0.25)),
 ("expert_sys","World expert system / library","INSTR",(0.55,0.30,0.15)),
 ("manuals","Manuals / theory-of-operation","COMM",(0.70,0.20,0.10)),
 ("induction","Induction map / gauge / onramp","COMM",(0.65,0.25,0.10)),
 ("tracker","This delivery tracker + glossary","INSTR",(0.60,0.25,0.15)),
]

ROLES=["MATH","APP","GOV","COMM","INSTR"]
TIERS=["T1","T2","T3"]

def closure(v):
    s=sum(v); return [x/s for x in v]
def clr(v):
    v=closure(v); g=math.exp(sum(math.log(x) for x in v)/len(v))
    return [math.log(x/g) for x in v]
def eff_dim(v):              # exp(Shannon entropy) of the closed share vector
    v=closure(v); H=-sum(x*math.log(x) for x in v if x>0); return math.exp(H)
def helmsman(v,labels):      # largest |clr| mover
    c=clr(v); i=max(range(len(c)),key=lambda k:abs(c[k])); return labels[i],c[i]
def aitchison_dist(a,b):
    ca,cb=clr(a),clr(b); return math.sqrt(sum((x-y)**2 for x,y in zip(ca,cb)))

# ---- package ROLE composition (mass = 1 per item) ----------------------------------------------
role_mass={r:0.0 for r in ROLES}
for _,_,role,_ in P: role_mass[role]+=1.0
role_vec=[role_mass[r] for r in ROLES]

# ---- package TIER composition (sum tier weights across all items) -------------------------------
tier_mass={t:0.0 for t in TIERS}
for _,_,_,tw in P:
    for t,w in zip(TIERS,tw): tier_mass[t]+=w
tier_vec=[tier_mass[t] for t in TIERS]
pkg_tier_share=closure(tier_vec)

# ---- per-item maturity read: distance from the package tier-barycenter --------------------------
items=[]
for iid,name,role,tw in P:
    d=aitchison_dist(list(tw),pkg_tier_share)
    dom=TIERS[max(range(3),key=lambda k:clr(list(tw))[k])]
    items.append({"id":iid,"name":name,"role":role,"tier_weights":dict(zip(TIERS,tw)),
                  "dom_tier":dom,"dist_from_pkg_barycenter":round(d,4)})
items.sort(key=lambda x:-x["dist_from_pkg_barycenter"])

role_h=helmsman(role_vec,ROLES)
tier_h=helmsman(tier_vec,TIERS)

out={
 "_meta":{"tool":"package_composition_read.py",
          "what":"Hs-on-Hs read of the delivery package (recursive). Math exact (T1); input weights structural estimates (T2).",
          "n_items":len(P)},
 "package_role_composition":{r:round(s,3) for r,s in zip(ROLES,closure(role_vec))},
 "package_role_effective_dimension":round(eff_dim(role_vec),3),
 "package_role_helmsman":{"role":role_h[0],"clr":round(role_h[1],3)},
 "package_tier_composition":{t:round(s,3) for t,s in zip(TIERS,pkg_tier_share)},
 "package_tier_effective_dimension":round(eff_dim(tier_vec),3),
 "package_tier_helmsman":{"tier":tier_h[0],"clr":round(tier_h[1],3)},
 "items_by_distance_from_barycenter":items,
}
blob=json.dumps({"inputs":P,"outputs":out},sort_keys=True,default=str).encode()
out["_meta"]["receipt_sha256"]=hashlib.sha256(blob).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2))
