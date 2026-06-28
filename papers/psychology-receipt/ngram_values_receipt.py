#!/usr/bin/env python3
"""
ngram_values_receipt.py -- a PROOF OF CONCEPT that a psychology-relevant claim can carry a hash receipt, on
public data anyone can re-pull. "Test the past, see the future" applied to two pre-stated compositions of a
real, public, 120-year cultural-psychology record (Google Books Ngram, en-2019, 1900-2019):

  A) VIRTUE VOCABULARY : {responsibility, courage, honesty, humility, gratitude, discipline} -- the relative
                         book-attention among six virtue terms, read as a composition over time.
  B) ORDER <-> CHAOS   : {order, chaos} -- Jordan Peterson's signature polarity, the balance over a century.

For each: the deterministic relational read (effective dimension, trajectory directedness, motion-helmsman over
the recent window) + the FORWARD CAST (extend the recent clr-velocity 20 years: a what-if, "see the future") +
a DATA FINGERPRINT (SHA-256 of the raw public values) so the receipt is anchored to data anyone can re-fetch and
re-verify. The leap: a psychology study handed a reproducible hash of proof-of-concept.

HONEST FENCE (firm): word-frequency in books is a LINGUISTIC / CULTURAL-ATTENTION proxy, NOT individual
psychology and NOT a measure of how much virtue, order, or chaos actually exist. "order"/"chaos" are polysemous
(chaos includes chaos-THEORY post-1975) -- the order/chaos arm is illustrative, heavily caveated. Descriptive,
not causal; the corpus has genre/OCR biases; the cast is an extrapolation, not a forecast. The contribution is
METHODOLOGICAL: determinism + a receipt for a psychology-adjacent claim, addressing the field's reproducibility
problem. Deterministic; numpy + stdlib. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-27. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib, os
HERE=os.path.dirname(os.path.abspath(__file__))
FLOOR=1e-12
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,FLOOR,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def softmax_clr(z): z=np.asarray(z,float); e=np.exp(z-z.max()); return e/e.sum()
def eff_dim(v): v=closure(v); H=-np.sum(v*np.log(v+1e-300),-1); return float(np.exp(np.mean(H)))
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]

def load_payload(fn):
    arr=json.load(open(os.path.join(HERE,fn)))
    names=[d["ngram"] for d in arr]; M=np.array([d["timeseries"] for d in arr]).T   # T x D (years x words)
    return names,M

def read_composition(name, names, M, H=20, K=25):
    T=M.shape[0]; X=closure(np.clip(M,FLOOR,None)); now=X[-1]
    C=clr(np.clip(M,FLOOR,None)); dC=np.diff(C,axis=0)
    path=float(np.sum(np.linalg.norm(dC,axis=1))); net=float(np.linalg.norm(C[-1]-C[0]))
    directed=round(net/path,3) if path else None
    vel_recent=np.mean(dC[-K:],axis=0)
    helm=names[int(np.argmax(np.abs(vel_recent)))]
    cast=softmax_clr(C[-1]+H*vel_recent)
    # per-part: now share, cast share, recent direction
    parts={names[j]:{"share_now":round(float(now[j]),4),"share_cast_%dy"%H:round(float(cast[j]),4),
                     "recent_direction":("rising" if vel_recent[j]>0 else "falling")} for j in range(len(names))}
    # data fingerprint: the raw public values, rounded to 12 sig-figs for cross-machine stability
    fp=sha([[float("%.12g"%x) for x in row] for row in M.tolist()])
    res={"composition":name,"n_years":T,"D_parts":len(names),
         "effective_dimension":round(eff_dim(np.mean(X,0)),3),"trajectory_directedness":directed,
         "motion_helmsman_recent":helm,"parts":parts,"data_fingerprint":fp}
    res["receipt"]=sha({k:res[k] for k in ("composition","effective_dimension","trajectory_directedness",
                                            "motion_helmsman_recent","parts","data_fingerprint")})
    return res

vn,vM=load_payload("ngram_virtues_raw.json")
on,oM=load_payload("ngram_order_chaos_raw.json")
A=read_composition("Virtue vocabulary (6 terms)",vn,vM)
B=read_composition("Order <-> Chaos polarity",on,oM)

# order-share specific read for B (the Peterson polarity, stated plainly)
order_now=B["parts"]["order"]["share_now"]; order_cast=B["parts"]["order"]["share_cast_20y"]
checks={
 "both_compositions_loaded": bool(A["n_years"]==120 and B["n_years"]==120),
 "valid_compositions": bool(abs(sum(p["share_now"] for p in A["parts"].values())-1.0)<1e-6),
 "directedness_measured": bool(A["trajectory_directedness"] is not None and B["trajectory_directedness"] is not None),
 "data_fingerprint_present": bool(len(A["data_fingerprint"])==16 and len(B["data_fingerprint"])==16),
}
master=sha({"A":A["receipt"],"B":B["receipt"],"checks":checks})
findings=(f"VIRTUE read: the 6-term composition is directed {A['trajectory_directedness']} over 120 yr; the recent "
   f"motion-helmsman is '{A['motion_helmsman_recent']}'. Per-term recent direction: "
   + ", ".join(f"{k} {v['recent_direction']}" for k,v in A["parts"].items()) + ". "
   f"ORDER<->CHAOS read: directed {B['trajectory_directedness']}; 'order' share {order_now} now -> {order_cast} on the "
   f"20-yr cast (the recent motion-helmsman is '{B['motion_helmsman_recent']}'). These are MEASURED on public data "
   "and reproduce to the data fingerprints below; the cast is a what-if, not a forecast.")
out={"_meta":{"tool":"ngram_values_receipt.py",
              "what":"proof of concept: a psychology-relevant compositional claim with a reproducible hash receipt, on public data",
              "master_receipt":master,"verdict":findings if all(checks.values()) else "CHECK FAILED"},
     "virtue_vocabulary":A,"order_chaos":B,"checks":checks,
     "the_leap":("psychology rarely ships a hash receipt; here a value/virtue claim does. Anyone can re-pull the "
        "documented public Ngram queries, recompute, and obtain the SAME data fingerprints and receipt -- "
        "determinism applied to a field defined by its reproducibility problem."),
     "fence":("Book word-frequency = cultural-attention PROXY, NOT individual psychology and NOT the prevalence of "
        "the things named. 'order'/'chaos' are polysemous (chaos-theory inflates 'chaos' post-1975) -- that arm is "
        "illustrative. Descriptive, not causal; corpus has genre/OCR bias; the cast is an extrapolation. The "
        "contribution is METHODOLOGICAL (determinism + receipt). Peter is the sole gate; nothing posted.")}
with open(os.path.join(HERE,"NGRAM_VALUES_RESULTS.json"),"w") as f: json.dump(out,f,indent=2)
if __name__=="__main__": print(json.dumps(out,indent=2))
