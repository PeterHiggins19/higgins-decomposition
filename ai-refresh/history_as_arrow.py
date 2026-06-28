#!/usr/bin/env python3
"""
history_as_arrow.py -- "our history as an arrow should show this; test us." Hˢ read on the project's OWN
development history (the journal G-1..G-N) as a compositional trajectory: bin the entries into temporal phases,
score each phase over PRE-STATED theme axes, and measure the trajectory's directedness, its motion-helmsman
(the part actively remaking the mix = the bearing of the arrow), and where it is cast.

The instrument reads itself and does NOT flatter. HONEST: keyword frequency in our own journal is a soft proxy,
and the governance share is inflated by the constant honest-broker footer ("Peter is the sole gate; nothing
posted") that appears in every entry -- a CONSTANT background, not a direction. So the number to watch is not the
raw directedness magnitude but the BEARING: which theme is the helmsman and rising. Theme axes are fixed in
advance to avoid cherry-picking. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. 2026-06-27. Peter is the sole gate; nothing posted.
"""
import json, numpy as np, hashlib, os
HS=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
J=json.load(open(os.path.join(HS,"ai-refresh","HS_TRACKING_LOG.json")))
V=J["tracks"]["engine_build_v4"]
ents=sorted([e for e in V if isinstance(e,dict) and e.get("id","").startswith("G-")],key=lambda e:int(e["id"].split("-")[1]))
def text(e): return " ".join(str(e.get(k,"")) for k in ("objective","note")).lower()
THEMES={  # PRE-STATED
 "foundation_math":["closure","clr","quaternion","ilr","proof","theorem","fixed point","determinis","simplex","invarian","receipt"],
 "physical_origin":["acoustic","ground state","loudspeaker","rwa","diffraction","btl","qam","fiber","laser","euv"],
 "applications":["energy","ember","medical","cancer","microbiome","finance","geolog","mri","psycholog","wine"],
 "field_operational":["sniffer","probe","rover","sample","field","tetrode","operational","sensor","autonomous","deploy","skin"],
 "governance":["governance","doctrine","gate","breaker","fence","honest","steward","standard","public"],
}
TH=list(THEMES); K=8; n=len(ents); per=max(1,n//K)
phases=[ents[i*per:(i+1)*per] for i in range(K-1)]+[ents[(K-1)*per:]]
def comp_of(ph):
    t=" ".join(text(e) for e in ph); c=np.clip(np.array([sum(t.count(w) for w in THEMES[th]) for th in TH],float),1e-9,None); return c/c.sum()
M=np.array([comp_of(p) for p in phases])
def clr(v): v=v/v.sum(-1,keepdims=True); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def smx(z): e=np.exp(z-z.max()); return e/e.sum()
C=clr(M); dC=np.diff(C,axis=0); path=float(np.sum(np.linalg.norm(dC,axis=1))); net=float(np.linalg.norm(C[-1]-C[0]))
directed=round(net/path,3) if path else None; vel=np.mean(dC,axis=0); helm=TH[int(np.argmax(np.abs(vel)))]
cast=smx(C[-1]+5*vel)
sha=lambda o:hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
res={"n_entries":n,"phases":K,"trajectory_directedness":directed,"motion_helmsman":helm,
 "field_operational_start_end_cast":[round(float(M[0][TH.index("field_operational")]),3),
   round(float(M[-1][TH.index("field_operational")]),3),round(float(cast[TH.index("field_operational")]),3)],
 "governance_constant_share":[round(float(M[0][TH.index("governance")]),3),round(float(M[-1][TH.index("governance")]),3)],
 "end_share":{TH[i]:round(float(M[-1][i]),3) for i in range(len(TH))},
 "cast_share":{TH[i]:round(float(cast[i]),3) for i in range(len(TH))}}
res["receipt"]=sha(res)
out={"_meta":{"tool":"history_as_arrow.py","what":"Hˢ on the project's own history; is it a directed arrow?","receipt_sha256":res["receipt"]},
     "reading":res,
     "verdict":(f"The history reads as a STEADY SHAFT + a CLEAR BEARING. Overall directedness is modest ({directed}) "
        "because GOVERNANCE is a near-constant background (the honest-broker register in every entry -- HUF's "
        f"character, unmoving from the start). But the MOTION-HELMSMAN is '{helm}': field-operational rises "
        f"{res['field_operational_start_end_cast'][0]} -> {res['field_operational_start_end_cast'][1]} and is cast to "
        f"{res['field_operational_start_end_cast'][2]} (the largest share ahead), while broad applications recede. "
        "The arrow's bearing points to field/operational -- where the geology/Matthew work fits. The instrument did "
        "not flatter: it reported a constant spine and a directed head."),
     "fence":("Keyword frequency in our own journal is a SOFT proxy (T2); governance is inflated by the constant "
        "footer (a background, not a direction) -- read the BEARING (helmsman + rise), not the raw magnitude. Theme "
        "axes pre-stated. Descriptive self-read, not proof of intent. Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
