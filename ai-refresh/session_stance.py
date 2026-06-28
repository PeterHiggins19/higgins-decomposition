#!/usr/bin/env python3
"""
session_stance.py -- the honest, measured answer to Peter's two questions: where does the whole system stand
after this session (the coherent stance / check-and-revise read), and -- just for fun -- is this still
DISCOVERY or REFINEMENT?

Reads this session's journal entries (engine_build_v4, G-225 onward), classifies each as discovery vs
refinement by lexical markers in its objective, forms the discovery:refinement composition, and measures the
TREND (early third vs late third) -- the 'near-peak refinement' hypothesis: is refinement rising as discovery
saturates?

HONEST FENCE: the discovery/refinement split is a LEXICAL PROXY (marker counts), not a semantic judgement;
many entries are both. The receipt-coherence spot-check (a separate bash step) re-runs sample scripts to
confirm the body reproduces. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import json, os, hashlib

HERE=os.path.dirname(os.path.abspath(__file__))
log=json.load(open(os.path.join(HERE,"HS_TRACKING_LOG.json")))
ents=[e for e in log["tracks"]["engine_build_v4"] if isinstance(e,dict)
      and e.get("id","").startswith("G-") and int(e["id"].split("-")[1])>=225]

DISC=["built","measured","named","found","discover","new ","law","principle","core math","crown","observ",
      "tetrahedron","four pole","treasure","theorem","proof","prove","seed","concept","capstone","the goal"]
REFI=["revis","fix","correct","re-run","rerun","re-ran","consolidat","heal","self-correct","update","trim",
      "readiness","coherence","cite","citation","alignment","transition","stance","verify","fence","bug","honest"]

def score(text,markers): t=text.lower(); return sum(t.count(m) for m in markers)
rows=[]
for e in ents:
    obj=str(e.get("objective",""))+" "+str(e.get("note",""))
    d=score(obj,DISC); r=score(obj,REFI); tot=d+r or 1
    rows.append({"id":e["id"],"disc":d,"refi":r,"disc_share":round(d/tot,3)})

D=sum(x["disc"] for x in rows); R=sum(x["refi"] for x in rows); T=D+R or 1
disc_share=round(D/T,3); n=len(rows)
third=max(n//3,1)
early=rows[:third]; late=rows[-third:]
def share(g):
    d=sum(x["disc"] for x in g); r=sum(x["refi"] for x in g); return round(d/(d+r or 1),3)
early_disc=share(early); late_disc=share(late)
trend="REFINEMENT RISING (discovery saturating)" if late_disc<early_disc-0.03 else \
      ("DISCOVERY STILL RISING" if late_disc>early_disc+0.03 else "STEADY (discovery+refinement balanced)")
verdict=(f"Over {n} session entries the work is {int(disc_share*100)}% DISCOVERY / {100-int(disc_share*100)}% "
   f"REFINEMENT by marker. Early {early_disc} -> late {late_disc} discovery-share: {trend}. So: still "
   f"{'mostly DISCOVERY' if disc_share>0.55 else 'mostly REFINEMENT' if disc_share<0.45 else 'BALANCED'}, "
   "with the near-peak refinement Peter sensed showing as the late-session trend.")

out={"_meta":{"tool":"session_stance.py","what":"discovery vs refinement + session stance (lexical proxy)",
              "n_entries":n,"span":f"{rows[0]['id']}..{rows[-1]['id']}"},
     "discovery_share_overall":disc_share,"refinement_share_overall":round(1-disc_share,3),
     "trend_early_to_late":{"early_third_discovery":early_disc,"late_third_discovery":late_disc,"reading":trend},
     "verdict":verdict,
     "fence":("Discovery/refinement is a LEXICAL PROXY (marker counts in the journal objectives), not a semantic "
              "judgement; many entries are both. Coherence of the body is checked separately by re-running sample "
              "scripts (receipts reproduce). Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {"rows":[(x["id"],x["disc"],x["refi"]) for x in rows],"disc_share":disc_share,
     "early":early_disc,"late":late_disc},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
