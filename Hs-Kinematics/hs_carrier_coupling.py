#!/usr/bin/env python3
"""
Hˢ — H1 Step 5: ENTANGLED-CARRIER CLOSURE (the honest, classical reading).

CLAIM DISCIPLINE (read first): compositional data are CLASSICAL. Nothing here is quantum
entanglement. Two honest things ARE true and measurable:
  (1) CLOSURE COUPLES THE CARRIERS. Parts sum to a constant, so they cannot vary independently
      (Pearson 1897 spurious correlation). This is the real "entangled-carrier closure": the
      closure constraint forces a coupling among carriers. We report that forced baseline.
  (2) A CHSH-FORM COORDINATION INDEX. Borrowing the algebraic form of the CHSH/Bell statistic,
      we read pairwise carrier COORDINATION from deterministic +/-1 functions of the CLR
      trajectory. For classical data this statistic is BOUNDED BY 2 (the classical/LHV bound);
      it can NEVER reach the Tsirelson bound 2.828. A value near 2 = maximally coordinated pair;
      a value > 2 would indicate a CONSTRUCTION ERROR, not entanglement. We verify the bound.

Tier 3 (exploratory — a clue, never a claim). Builds on the D=8 twin-quaternion = Spin(4) =
SU(2)xSU(2) structure (a natural two-party algebra; that connection is itself Tier 3).
numpy + stdlib. Deterministic; hash-receipted. Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import numpy as np, hashlib, json

def closure(M): M=np.clip(np.asarray(M,float),0,None); s=M.sum(1,keepdims=True); s[s==0]=1; return M/s
def clr(P): P=np.clip(P,1e-12,None); L=np.log(P); return L-L.mean(1,keepdims=True)

def closure_baseline(M):
    """The coupling FORCED by closure: mean off-diagonal correlation of the closed parts
    (the spurious-correlation baseline). Negative by construction for closed data."""
    P=closure(M); C=np.corrcoef(P.T); D=P.shape[1]
    off=C[~np.eye(D,dtype=bool)]
    return {"mean_forced_correlation":round(float(off.mean()),4),
            "note":"negative by construction (closure forces parts to trade off); this is the baseline coordination, not signal"}

def _pm(x):  # deterministic +/-1
    s=np.sign(x); s[s==0]=1; return s

def chsh_pair(R, i, j):
    """CHSH-form coordination of carriers i,j from the CLR series R (T x D).
    Two settings per carrier: A0 = sign(level - own mean); A1 = sign(first difference).
    Returns max over the 4 CHSH sign-combinations of |E(a,b)+E(a,b')+E(a',b)-E(a',b')|, in [0,2]."""
    T=R.shape[0]
    Ai=_pm(R[:-1,i]-R[:,i].mean()); Aip=_pm(np.diff(R[:,i]))
    Bj=_pm(R[:-1,j]-R[:,j].mean()); Bjp=_pm(np.diff(R[:,j]))
    E=lambda a,b: float(np.mean(a*b))
    e00,e01,e10,e11=E(Ai,Bj),E(Ai,Bjp),E(Aip,Bj),E(Aip,Bjp)
    # the four CHSH sign patterns (one term negated); classical max is 2
    cands=[abs(e00+e01+e10-e11), abs(e00+e01-e10+e11), abs(e00-e01+e10+e11), abs(-e00+e01+e10+e11)]
    return min(float(max(cands)), 2.0+1e-12)  # report; flag if it ever exceeds 2

def coupling_matrix(M):
    R=clr(closure(M)); D=R.shape[1]; S=np.zeros((D,D))
    raw_max=0.0
    for i in range(D):
        for j in range(i+1,D):
            v=chsh_pair(R,i,j)
            # raw (unclamped) to detect any bound violation
            T=R.shape[0]; Ai=_pm(R[:-1,i]-R[:,i].mean()); Aip=_pm(np.diff(R[:,i]))
            Bj=_pm(R[:-1,j]-R[:,j].mean()); Bjp=_pm(np.diff(R[:,j]))
            E=lambda a,b: float(np.mean(a*b)); e00,e01,e10,e11=E(Ai,Bj),E(Ai,Bjp),E(Aip,Bj),E(Aip,Bjp)
            raw=max(abs(e00+e01+e10-e11),abs(e00+e01-e10+e11),abs(e00-e01+e10+e11),abs(-e00+e01+e10+e11))
            raw_max=max(raw_max,raw); S[i,j]=S[j,i]=round(v,4)
    return S, round(raw_max,4)

def run(M, names=None):
    M=np.asarray(M,float); names=list(names) if names is not None else [f"c{j}" for j in range(M.shape[1])]
    S,raw_max=coupling_matrix(M); D=M.shape[1]
    pairs=sorted([(S[i,j],names[i],names[j]) for i in range(D) for j in range(i+1,D)],reverse=True)
    out={
      "identity":"Hs carrier-coupling (H1 Step 5: entangled-carrier closure) — CLASSICAL, NOT quantum",
      "closure_coupling_baseline":closure_baseline(M),
      "chsh_form_classical_bound":2.0,
      "tsirelson_quantum_bound_for_reference_only":2.8284,
      "max_chsh_form_coupling_observed":round(float(max(p[0] for p in pairs)) if pairs else 0.0,4),
      "raw_max_before_clamp":raw_max,
      "classical_bound_respected":bool(raw_max<=2.0+1e-9),
      "most_coupled_pairs":[{"pair":[a,b],"chsh_form":round(s,4)} for s,a,b in pairs[:5]],
      "verdict":("classical bound (2) respected — coordination diagnostic behaving as it must for classical data; NO entanglement"
                 if raw_max<=2.0+1e-9 else
                 "BOUND VIOLATED (>2): construction error to fix — NOT evidence of entanglement"),
      "tier":"Tier 3 exploratory — a clue, never a claim; compositional data are classical; this is coordination structure, not quantum entanglement"}
    def nz(x):
        if isinstance(x,float): return round(x,12)
        if isinstance(x,dict): return {k:nz(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)): return [nz(v) for v in x]
        return x
    out["content_hash"]=hashlib.sha256(json.dumps(nz(out),sort_keys=True,default=str).encode()).hexdigest()
    return out

if __name__=="__main__":
    rng=np.random.default_rng(0); T=40
    base=np.array([.30,.22,.18,.12,.08,.04,.04,.02]); M=np.maximum(base+np.cumsum(rng.normal(0,.012,(T,8)),0),1e-4)
    print(json.dumps(run(M,[f"c{i}" for i in range(8)]),indent=1))
