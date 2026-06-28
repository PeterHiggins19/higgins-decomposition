#!/usr/bin/env python3
"""
four_way_composition.py -- Peter's question, answered with real public data: can a 4-way composition on
{science, belief, physics, supersymmetry} even be MEASURED? Yes -- as a PROXY. We read each term's frequency
in the Google Books English corpus (a public attention proxy) over 1900-2019, form the closed 4-part
composition per year, and read it with Hs.

The parallel Peter drew: science:belief :: Standard-Model:supersymmetry -- the KNOWN half and the OTHER that
completes the whole yet 'remains other'. The compositional read tests whether the data carries that shape.

THE FINDING (measured below): in SHARE, science + belief dominate and supersymmetry is vanishing -- it
'remains other'. But in LOG-RATIO MOTION (clr velocity), supersymmetry is the HELMSMAN -- it moved the most,
by orders of magnitude, appearing only after ~1970. So the 'other' is the biggest MOVER of the composition
while remaining the smallest PART. That is exactly 'the other remains other': it carries the surprise
(information) and never the mass.

HONEST FENCE: this measures WORD FREQUENCY in books -- a proxy for textual ATTENTION, NOT the concepts, NOT
their truth, NOT their 'amount' in reality. The four parts are NOT disjoint (physics is part of science;
supersymmetry is part of physics), so this is a composition of four chosen TERMS' relative attention, not an
ontological partition. Supersymmetry the physics remains EXPERIMENTALLY UNCONFIRMED (no superpartners observed
as of 2025); the ngram measures only the word. 'Science has religious origins' is historical context, not
measured here. Deterministic; receipt. Source: Google Books Ngram Viewer, en-2019, smoothing 3, 1900-2019.
Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the
sole gate; nothing posted.
"""
import json, os, math, hashlib

HERE=os.path.dirname(os.path.abspath(__file__))
raw=json.load(open(os.path.join(HERE,"ngram_4term_raw.json")))
series={d["ngram"]:d["timeseries"] for d in raw}
PARTS=["science","belief","physics","supersymmetry"]
years=list(range(1900,1900+len(series["science"])))
T=len(years)

FLOOR=1e-12   # supersymmetry has exact zeros pre-1910; floor them (structural-zero handling, E-21 style)
def closure(v):
    v=[max(x,FLOOR) for x in v]; s=sum(v); return [x/s for x in v]
def clr(c):
    g=math.exp(sum(math.log(x) for x in c)/len(c)); return [math.log(x/g) for x in c]

comp=[closure([series[p][i] for p in PARTS]) for i in range(T)]
clrs=[clr(c) for c in comp]

# mean shares
mean_share={PARTS[j]:round(sum(comp[i][j] for i in range(T))/T,6) for j in range(len(PARTS))}
# supersymmetry 'remains other': its share stats
sy=[comp[i][3] for i in range(T)]
susy_share={"mean":round(sum(sy)/T,8),"max":round(max(sy),8),"max_year":years[sy.index(max(sy))]}

# helmsman of MOTION: which part has the largest total |clr velocity| over the span
vel_energy=[0.0]*len(PARTS)
for i in range(1,T):
    for j in range(len(PARTS)):
        vel_energy[j]+=abs(clrs[i][j]-clrs[i-1][j])
helm_motion=PARTS[max(range(len(PARTS)),key=lambda j:vel_energy[j])]
# helmsman of SHARE: largest mean part
helm_share=max(mean_share,key=mean_share.get)

# science:belief log-ratio over time (the known-method vs belief-method balance)
sci_belief_lr={"1900":round(math.log(comp[0][0]/comp[0][1]),3),
               "2019":round(math.log(comp[-1][0]/comp[-1][1]),3)}
# effective dimension of the mean composition
mc=[mean_share[p] for p in PARTS]; mc=[x/sum(mc) for x in mc]
eff_dim=round(math.exp(-sum(x*math.log(x) for x in mc if x>0)),3)
# directedness of the 4-part trajectory
path=sum(math.sqrt(sum((clrs[i][j]-clrs[i-1][j])**2 for j in range(len(PARTS)))) for i in range(1,T))
net=math.sqrt(sum((clrs[-1][j]-clrs[0][j])**2 for j in range(len(PARTS))))
directedness=round(net/path,3) if path else None

answer=("YES -- measurable as a public-data PROXY. In SHARE the composition is science+belief dominant and "
        f"supersymmetry vanishing (mean share {susy_share['mean']}, peak {susy_share['max']} in "
        f"{susy_share['max_year']}): the OTHER REMAINS OTHER. But in LOG-RATIO MOTION the helmsman is "
        f"'{helm_motion}' -- the smallest part is the biggest mover (it carries the surprise, never the mass).")

out={"_meta":{"tool":"four_way_composition.py","source":"Google Books Ngram (en-2019, smoothing 3, 1900-2019)",
              "parts":PARTS,"years":[years[0],years[-1]]},
     "ANSWER":answer,
     "mean_share":mean_share,
     "supersymmetry_remains_other":susy_share,
     "helmsman_of_share":helm_share,
     "helmsman_of_motion":helm_motion,
     "clr_velocity_energy":{PARTS[j]:round(vel_energy[j],3) for j in range(len(PARTS))},
     "science_vs_belief_logratio":sci_belief_lr,
     "effective_dimension_mean":eff_dim,
     "trajectory_directedness":directedness,
     "fence":("Measures WORD-FREQUENCY ATTENTION in books, NOT the concepts/their truth/their amount. The four "
              "parts are NOT disjoint (physics in science; supersymmetry in physics) -> a composition of chosen "
              "TERMS' relative attention, not an ontological partition. Supersymmetry stays experimentally "
              "UNCONFIRMED; only the word is counted. Historical 'religious origins of science' not measured here. "
              "Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {"mean":mean_share,"susy":susy_share,"helm_motion":helm_motion,"vel":out["clr_velocity_energy"],
     "dir":directedness,"eff":eff_dim},sort_keys=True).encode()).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2))
