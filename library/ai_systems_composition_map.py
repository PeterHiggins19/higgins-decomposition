#!/usr/bin/env python3
"""
ai_systems_composition_map.py -- turn the instrument on our OWN field: read the world of AI / expert-systems
development as a composition, place HUF/Hs in it, find who is NEAREST (allies to learn from) and FARTHEST,
and surface, per axis, WHO LEADS so we can compose their lessons into ours.

Five axes (each 0..1), chosen as Hs's own design values -- so Hs sits near the corner BY CONSTRUCTION; the
map's value is NOT 'we win', it is *who else is strong on each axis and what they do more maturely than us*:
  determinism   = outputs reproducible / machine-checkable, not a re-rolled guess
  compositional = built from explicit parts/structure that compose, not an opaque blob
  honesty       = calibrated uncertainty: knows when it doesn't know, abstains, tiers its claims
  grounding     = anchored in real domain structure/data, not free generation
  provenance    = content-addressed, re-computable audit trail (receipts)

Scores are REASONED ESTIMATES of SCHOOLS/APPROACHES (T2), from a 2026 landscape scan (sources in the
companion .md), NOT measurements of specific projects and NOT a ranking of teams. The math on them is
deterministic + receipted. Falsifier: score each school from a structured rubric survey of its literature and
refit. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26.
Peter is the sole gate; nothing posted.
"""
import json, hashlib, math

AX = ["determinism","compositional","honesty","grounding","provenance"]
# school: scores on AX + a one-line "what they do that we should learn"
S = {
 "HUF/Hs (ours)":                         ([0.95,0.95,0.90,0.90,0.95], "the baseline we are scoring against -- strong by design, thin in scale/community/proof-at-volume"),
 "Compositional Data Analysis (CoDa)":    ([0.60,0.95,0.65,0.90,0.55], "the home field + peer community: decades of method, real reviewers -- we owe it citation and a Q-node, not reinvention"),
 "Neuro-symbolic AI (3rd wave)":          ([0.70,0.90,0.55,0.60,0.45], "symbolic rules -> formal proof that violations are impossible; a mature 'symbolic layer' framing for our determinism"),
 "Formal NN verification (VNN-COMP)":     ([0.95,0.30,0.60,0.40,0.55], "an open, adversarial COMPETITION with shared benchmarks -- public falsification as a discipline we lack"),
 "RL w/ Verifiable Rewards (RLVR)":       ([0.85,0.35,0.55,0.55,0.60], "a DETERMINISTIC CHECKER generates unlimited training/eval data -- our receipts could be such a checker"),
 "Calibrated-uncertainty / abstention":   ([0.45,0.30,0.95,0.55,0.40], "explicit over- AND under-confidence penalties (Rewarding Doubt); span-level claim verification -- harden our margin gate"),
 "Reproducibility / provenance governance":([0.85,0.30,0.60,0.45,0.90], "AAAI/CVPR reproducibility checklists + compute reporting as a SHARED STANDARD -- adopt as our public on-ramp gate"),
 "Mainstream LLM / agentic foundation":   ([0.25,0.35,0.40,0.45,0.30], "scale, reach, fluency, adoption -- everything we are weak on; the far pole, but where the users already are"),
}

def dist(a,b): return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
ours = S["HUF/Hs (ours)"][0]
rows=[]
for name,(v,lesson) in S.items():
    if name=="HUF/Hs (ours)": continue
    d=dist(ours,v)
    rows.append({"school":name,"distance_from_Hs":round(d,3),"scores":dict(zip(AX,v)),
                 "nearest_axis":AX[max(range(5),key=lambda i:v[i])],"learn":lesson})
rows.sort(key=lambda r:r["distance_from_Hs"])

# per-axis: who (besides us) leads -> that's who to learn from on that axis
others={n:v for n,(v,_) in S.items() if n!="HUF/Hs (ours)"}
per_axis={}
for i,ax in enumerate(AX):
    leader=max(others,key=lambda n:others[n][i])
    per_axis[ax]={"external_leader":leader,"their_score":others[leader][i],"our_score":ours[i],
                  "gap_vs_us":round(others[leader][i]-ours[i],3)}

out={"_meta":{"tool":"ai_systems_composition_map.py",
              "what":"the AI/expert-systems world read as a composition; ours placed; nearest=allies, per-axis leaders=teachers",
              "axes":AX,"n_schools":len(S)},
     "nearest_to_farthest":[r["school"] for r in rows],
     "rows":rows,
     "per_axis_who_to_learn_from":per_axis,
     "honest_reflexive_note":("The axes ARE Hs's values, so Hs sits near the corner BY CONSTRUCTION -- that is "
        "NOT evidence we are best. The real reading: (1) nobody else is near all five at once (our actual "
        "niche), AND (2) on EVERY axis an external school is more battle-tested than us in scale, community, "
        "benchmarks, or proof-at-volume. The map says compose their maturity into our design, not that we win."),
     "fence":("T2 reasoned estimates of SCHOOLS, not measurements of projects or a ranking of teams; the math "
        "is deterministic + receipted. Falsifier: rubric-survey each school's literature and refit. We name "
        "allies to cite + learn from, never imply collaboration. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(
    json.dumps({"rows":rows,"per_axis":per_axis,"ours":ours},sort_keys=True,default=str).encode()).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2,ensure_ascii=False))
