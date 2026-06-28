#!/usr/bin/env python3
"""
tetrode_self_guided_map.py -- PROBE AND SEE, then DETERMINE A COURSE OF ACTION for the sensitive-study space,
and acquire/evolve it as log/log compositional memory for SELF-GUIDED MAPPING.

The tetrode standard (huf-gov/doctrine/THE_TETRODE_STANDARD_for_sensitive_studies.md) says every sensitive
medical study is FOUR independent studies of one topic. This tool maps that space:

  PROBE  : read each medical topic as a composition over the biological/measurement SYSTEMS it involves.
  SEE    : group topics by SCALE-INVARIANT compositional similarity (clr + Aitchison distance, the compositional
           memory feature) -- the cross-involved-systems grouping, not fooled by how "big" a topic is.
  DECIDE : assign each topic its TETRODE of 4 independent channels (the course of action), and name which topics
           share systems (joint cross-system testing).
  EVOLVE : store each topic's clr content-address in the compositional memory; re-running acquires/evolves the
           map (same receipt if unchanged -- the determinism-anchor cycle on the management layer / log/log).

HONEST: the systems-profiles are DESIGNED/illustrative (T2) -- the mechanism (scale-invariant grouping + 4-channel
assignment + deterministic addressing) is real; the specific profiles are a sketch to be refined with domain
experts. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-27. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-12,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def aitch(a,b): return float(np.linalg.norm(clr(a)-clr(b)))
def address(comp):                       # deterministic 7-bit-clr content address (scale-invariant)
    z=clr(comp); q=np.clip(np.round((z+6.0)/(12.0/127.0)),0,127).astype(np.uint8)
    return hashlib.sha256(q.tobytes()).hexdigest()[:12]
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]

# SYSTEMS axes (the involved biological/measurement systems)
AX=["cellular","hematologic","metabolic","imaging","epidemiologic","molecular"]
# TOPICS the project has touched, each a DESIGNED systems-profile (illustrative), + a proposed tetrode of 4 channels
TOPICS={
 "cancer-incidence epidemiology": {"profile":[2,1,1,1,8,3],
    "tetrode":["NCRP/ICMR registry","GLOBOCAN/IARC","hospital-based registry","population sub-cohort"]},
 "blood / CBC panel":             {"profile":[3,9,3,0.5,1,1],
    "tetrode":["analyzer A cohort","analyzer B cohort","reference lab","longitudinal sub-cohort"]},
 "microbiome":                    {"profile":[2,1,5,0.5,1,8],
    "tetrode":["16S run","shotgun run","second site/cohort","reprocessed pipeline"]},
 "respiratory gas (Southmedic)":  {"profile":[1,2,8,0.5,1,1],
    "tetrode":["monitor A","monitor B","independent capnograph","procedure-replicate"]},
 "MRI / neuroimaging":            {"profile":[3,0.5,2,9,1,1],
    "tetrode":["scanner A","scanner B","second protocol","re-test session"]},
}
names=list(TOPICS); P={n:closure(TOPICS[n]["profile"]) for n in names}

# SEE: scale-invariant grouping -- nearest cross-system partner + single-linkage clusters at a threshold
THR=2.3
def nn(n): return min((m for m in names if m!=n), key=lambda m: aitch(P[n],P[m]))
# clusters
import itertools
parent={n:n for n in names}
def find(x):
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
for a,b in itertools.combinations(names,2):
    if aitch(P[a],P[b])<THR: parent[find(a)]=find(b)
clusters={}
for n in names: clusters.setdefault(find(n),[]).append(n)
groups=[sorted(v) for v in clusters.values()]

topics_out={}
for n in names:
    topics_out[n]={"systems_profile":{AX[i]:round(float(P[n][i]),3) for i in range(len(AX))},
                   "content_address":address(P[n]),"tetrode_4_channels":TOPICS[n]["tetrode"],
                   "nearest_cross_system_partner":nn(n)}
# EVOLVE check: scale-invariance of the address (a topic scaled by any factor maps to the SAME address/cluster)
rng=np.random.default_rng(0)
scale_inv=all(address(P[n])==address(P[n]*float(np.exp(rng.uniform(-2,2)))) for n in names)

checks={
 "every_topic_is_a_tetrode_of_4": bool(all(len(t["tetrode_4_channels"])==4 for t in topics_out.values())),
 "addresses_deterministic_and_scale_invariant": bool(scale_inv),
 "grouping_nonempty": bool(len(groups)>=1 and sum(len(g) for g in groups)==len(names)),
}
master=sha({"t":{n:topics_out[n]["content_address"] for n in names},"g":groups,"c":checks})
course=("PROBE AND SEE -> COURSE OF ACTION: each sensitive topic is assigned a TETRODE of 4 independent channels "
   "(must do four). Topics that share involved systems are grouped for joint cross-system testing: "
   + " | ".join("{"+", ".join(g)+"}" for g in groups) + ". The map is stored as scale-invariant content "
   "addresses (compositional memory) and re-derives to the same receipt -- self-guided, evolvable.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"tetrode_self_guided_map.py","what":"self-guided map of the sensitive-study space; tetrode-of-4 + cross-system groups",
              "master_receipt":master,"verdict":course},
     "systems_axes":AX,"topics":topics_out,"cross_system_groups":groups,"checks":checks,"tetrode_threshold_aitchison":THR,
     "standard":"huf-gov/doctrine/THE_TETRODE_STANDARD_for_sensitive_studies.md -- four of the same topic, mandatory",
     "fence":("Systems-profiles are DESIGNED/illustrative (T2), to be refined with domain experts; the mechanism "
        "(scale-invariant grouping + 4-channel assignment + deterministic content addressing) is real. The four "
        "channels must be INDEPENDENT to help. Clinical fence unchanged (research/epidemiology, not diagnosis). "
        "Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
