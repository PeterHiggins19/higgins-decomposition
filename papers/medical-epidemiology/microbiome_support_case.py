#!/usr/bin/env python3
"""
microbiome_support_case.py -- the MICROBIOME leg of the medical-quality tetrode (medical support case #2).
Real public data already in hand: the coda4microbiome Crohn dataset (Calle, Pujolassos & Susin 2023, BMC
Bioinformatics 24:82) -- 975 samples, 48 genera, 662 Crohn (CD) vs 313 control. The instrument is Hˢ; the data
and its biological interpretation belong to the domain (coda4microbiome / the original studies).

The reading that makes it a support case: a totals/diversity view of the gut is NEAR-NULL for disease state,
while the RELATIONAL (log-ratio / clr) view separates -- the message is in the ratios (the Compositional Message
Principle). Measured here on a deterministic held-out split:
  * diversity (Shannon) AUC ~ null;  * relational (clr nearest-centroid) AUC clearly higher, held out.
The proper CV-validated relational read (logistic regression on ILR, the CMP analysis) reaches AUC 0.832; this
support case confirms the DIRECTION with a simple, fully deterministic discriminant and a receipt -- and the
input-data hash matches the CMP record exactly (same data, same hash).

HONEST: research / methods only, NOT clinical or diagnostic; +0.5 pseudocount zero-treatment (E-21); the
nearest-centroid AUC is conservative vs the CV logistic number; the biology is the domain's. Deterministic;
receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. Peter
is the sole gate; nothing posted.
"""
import csv, os, numpy as np, hashlib, json
HERE=os.path.dirname(os.path.abspath(__file__))
CROHN=os.path.normpath(os.path.join(HERE,"..","..","experiments","microbiome_real_2026-06","crohn.csv"))
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
def closure(M): M=np.clip(M+0.5,1e-9,None); return M/M.sum(1,keepdims=True)   # +0.5 pseudocount (E-21)
def clr(M): C=closure(M); L=np.log(C); return L-L.mean(1,keepdims=True)
def shannon(M): C=closure(M); return -(C*np.log(C)).sum(1)
def auc(score,lab):
    order=np.argsort(score); ranks=np.empty(len(score)); ranks[order]=np.arange(1,len(score)+1)
    n1=lab.sum(); n0=len(lab)-n1; return float((ranks[lab==1].sum()-n1*(n1+1)/2)/(n1*n0))

rows=list(csv.reader(open(CROHN))); data=rows[1:]
y=np.array([1 if "CD" in r[0] else 0 for r in data])
X=np.array([[float(v) for v in r[1:]] for r in data])
xhash=hashlib.sha256(X.tobytes()).hexdigest()[:16]
idx=np.arange(len(y)); tr=idx%2==0; te=~tr                                   # deterministic held-out split
div=auc(shannon(X[te]),y[te]); div=max(div,1-div)
C=clr(X); d=C[tr][y[tr]==1].mean(0)-C[tr][y[tr]==0].mean(0)
rel=auc(C[te]@d,y[te]); rel=max(rel,1-rel)
res={"leg":"microbiome (medical tetrode support case)",
 "dataset":"coda4microbiome Crohn (Calle, Pujolassos & Susin 2023, BMC Bioinformatics 24:82)",
 "N":len(y),"D":int(X.shape[1]),"n_CD":int(y.sum()),"n_control":int((y==0).sum()),"input_hash_X":xhash,
 "diversity_shannon_auc_heldout":round(div,3),"relational_clr_auc_heldout":round(rel,3),
 "cited_CMP_relational_cv_auc":0.832,"cited_CMP_diversity_auc":0.505}
checks={"diversity_is_near_null":bool(div<0.60),"relational_separates":bool(rel>0.65),
 "relational_beats_diversity":bool(rel>div+0.15),"input_hash_matches_CMP_record":bool(xhash=="0b1daa0f9edee6b8")}
master=sha({"res":res,"checks":checks})
verdict=(f"MICROBIOME LEG CONFIRMED. On real Crohn data (N={len(y)}, input hash {xhash} -- matches the message-"
   f"principle record), the diversity view is near-null (held-out AUC {res['diversity_shannon_auc_heldout']}) "
   f"while the RELATIONAL clr read separates ({res['relational_clr_auc_heldout']} held out; the CV-validated "
   "logistic read reaches 0.832). The message is in the ratios -- a deterministic, receipted compositional read "
   "of a hard-to-study system. This is support case #2 of the medical-quality tetrode.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"microbiome_support_case.py","what":"microbiome leg of the medical-quality tetrode","receipt_sha256":master,"verdict":verdict},
     "result":res,"checks":checks,
     "fence":("Research / methods only -- NOT clinical or diagnostic. The data + biology belong to the domain "
        "(coda4microbiome / original studies); Hˢ provides the instrument. +0.5 pseudocount zero-treatment (E-21); "
        "the nearest-centroid AUC is conservative vs the CV logistic number. Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
