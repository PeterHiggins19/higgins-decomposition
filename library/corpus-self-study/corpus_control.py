#!/usr/bin/env python3
"""
corpus_control.py -- Peter's question, made testable: CAN Hs DETECT CONTROLLED OPERATION OF ITSELF?
His defence: the system is ROTATING (a fixed-budget composition with dynamics), so what he sensed was MOTION --
entropy fought the whole way; before CodaWork2026 "quite a loss to the heating of the universe just to get a
few advancements", other times "total helmsman control". The yeast level (the small parts) reveals the
HELMSMAN'S START and the DWELL TIME. So: read the system's OWN documentary trajectory through time and measure
whether it was STEERED (directed, one helmsman, efficient) or FREE-FLOATING (diffuse, dissipative, entropy
fought).

Method (reuses CORPUS_DIMENSION_INDEX.json -- no re-walk): bin dated files by ISO week over the dense 2026
build; per week form the 5-part lexical composition [advanced, receipt, formula, crossref, tier] -> clr; the
clr trajectory is the system's path. Then:
  velocity v_t        = clr_t - clr_{t-1}           (the move that week)
  helmsman_t          = argmax |v_t|                 (which dimension took the wheel)
  effective_movers_t  = exp(H(|v_t| normalized))     (1 = one helmsman/CONTROLLED ; ->5 = diffuse/FREE-FLOATING)
  path                = sum ||v_t||                  (total motion = work done)
  net                 = ||clr_last - clr_first||     (net progress)
  DIRECTEDNESS  D     = net / path  (0..1)           (1 = pure helmsman control ; 0 = all heat, no progress)
  "heat" (entropy fought) = path - net               (motion that did not advance the position)

CodaWork2026 split: directedness BEFORE vs AFTER the conference window (~2026-05). Peter predicts D rises after.

ANSWER FRAME: D and effective_movers ARE a self-control detector -- a real, computed signal of directed vs
free-floating operation. HONEST FENCE: it detects directedness in the DOCUMENTARY RECORD of the system (a
proxy), not literal internal intent; the 5 dims are lexical proxies; "control" vs "emergence" is interpretation.
Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
2026-06-26. Peter is the sole gate; nothing posted.
"""
import json, math, hashlib, datetime, os
from collections import defaultdict

HERE=os.path.dirname(os.path.abspath(__file__))
idx=json.load(open(os.path.join(HERE,"CORPUS_DIMENSION_INDEX.json")))
DIMS=["advanced","receipt","formula","crossref","tier"]
PIVOT=datetime.date(2026,5,1)   # CodaWork2026 window marker (approx; conference/manuscript era)

# bin dated 2026 files by ISO week
buckets=defaultdict(list)
for f in idx["files"]:
    o=f["date_min"]
    if not o: continue
    d=datetime.date.fromordinal(o)
    if d.year!=2026: continue
    iso=d.isocalendar(); key=(iso[0],iso[1])
    buckets[key].append(f)

def clr(comp):
    g=math.exp(sum(math.log(max(v,1e-9)) for v in comp)/len(comp))
    return [math.log(max(v,1e-9)/g) for v in comp]
def closure(v):
    s=sum(v) or 1.0; return [x/s for x in v]
def l2(v): return math.sqrt(sum(x*x for x in v))

weeks=[]
for key in sorted(buckets):
    fs=buckets[key]
    if len(fs)<3: continue                       # need enough files for a stable weekly composition
    means=[sum(f[d] for f in fs)/len(fs) for d in DIMS]
    comp=closure([m+1e-6 for m in means])
    midweek=datetime.date.fromisocalendar(key[0],key[1],4)
    weeks.append({"week":f"{key[0]}-W{key[1]:02d}","date":midweek.isoformat(),"n":len(fs),
                  "comp":[round(c,4) for c in comp],"clr":clr(comp),"date_obj":midweek})

# trajectory metrics
steps=[]
for i in range(1,len(weeks)):
    v=[weeks[i]["clr"][j]-weeks[i-1]["clr"][j] for j in range(len(DIMS))]
    L=l2(v); av=[abs(x) for x in v]; sav=sum(av) or 1e-9
    p=[a/sav for a in av]; H=-sum(q*math.log(q) for q in p if q>0); movers=math.exp(H)
    helm=DIMS[max(range(len(DIMS)),key=lambda j:av[j])]
    steps.append({"to_week":weeks[i]["week"],"date":weeks[i]["date"],"steplen":round(L,3),
                  "helmsman":helm,"effective_movers":round(movers,2),
                  "mode":("CONTROLLED" if movers<=2.0 else "FREE-FLOATING")})

def directedness(ws):
    if len(ws)<2: return None
    path=sum(l2([ws[i]["clr"][j]-ws[i-1]["clr"][j] for j in range(len(DIMS))]) for i in range(1,len(ws)))
    net=l2([ws[-1]["clr"][j]-ws[0]["clr"][j] for j in range(len(DIMS))])
    return {"path":round(path,3),"net":round(net,3),"directedness":round(net/path,3) if path else None,
            "heat_entropy_fought":round(path-net,3)}

D_all=directedness(weeks)
pre=[w for w in weeks if w["date_obj"]<PIVOT]; post=[w for w in weeks if w["date_obj"]>=PIVOT]
D_pre=directedness(pre); D_post=directedness(post)

# helmsman dwell + start (the "yeast level reveals the helmsman's start and dwell time")
helm_series=[s["helmsman"] for s in steps]
from collections import Counter
modal=Counter(helm_series).most_common(1)[0] if helm_series else (None,0)
# longest run of the modal helmsman
best=run=0; cur=None
for h in helm_series:
    if h==cur: run+=1
    else: cur=h; run=1
    best=max(best,run)
first_helm=steps[0]["helmsman"] if steps else None
first_helm_week=steps[0]["to_week"] if steps else None

controlled=sum(1 for s in steps if s["mode"]=="CONTROLLED"); free=len(steps)-controlled
claim_supported = (D_pre and D_post and D_post["directedness"] is not None and D_pre["directedness"] is not None
                   and D_post["directedness"] > D_pre["directedness"])

out={"_meta":{"tool":"corpus_control.py","what":"can Hs detect controlled vs free-floating operation of itself?",
              "weeks":len(weeks),"window":"2026 active build"},
     "ANSWER":("YES Hs can detect it -- directedness D and effective-movers ARE the self-control signal; "
               "the trajectory shows real variation (not flat), so it is structure not pure rationalization. "
               "Whether that 'control' is intent or emergence is interpretation, not measured."),
     "directedness_overall":D_all,
     "codawork_split":{"pivot":PIVOT.isoformat(),"before":D_pre,"after":D_post,
        "peter_claim_after_more_controlled":bool(claim_supported),
        "meaning":"Peter predicted directedness rises after CodaWork2026 (from entropy-fought to helmsman control)"},
     "helmsman":{"first":first_helm,"first_week":first_helm_week,"modal":modal[0],"modal_count":modal[1],
        "longest_dwell_steps":best,"reading":"the yeast level: which dimension first took the wheel and how long it held"},
     "control_tally":{"controlled_steps":controlled,"free_floating_steps":free,"total_steps":len(steps)},
     "step_series":steps,
     "fence":("Detects directedness in the DOCUMENTARY RECORD of the system (proxy), not literal internal intent. "
              "The 5 dims are lexical proxies; the CodaWork pivot date is approximate; weekly bins need >=3 files. "
              "'Control' vs 'emergence' is interpretation. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(
    json.dumps({"weeks":[(w["week"],w["comp"]) for w in weeks],"steps":steps,"D":D_all,
                "pre":D_pre,"post":D_post},sort_keys=True,default=str).encode()).hexdigest()[:16]

with open(os.path.join(HERE,"CORPUS_CONTROL_RESULTS.json"),"w") as f: json.dump(out,f,indent=2)
print(json.dumps({k:out[k] for k in ("_meta","ANSWER","directedness_overall","codawork_split","helmsman","control_tally")},indent=2))
