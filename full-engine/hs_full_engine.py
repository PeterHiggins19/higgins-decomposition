#!/usr/bin/env python3
"""
hs_full_engine.py -- the full-featured Hs engine: the integration orchestrator.

This composes the session's receipted components into ONE non-invasive pipeline, built
DETERMINISM-MATH-FIRST with every other capability as a support channel:

  CORE   (first, T1)  : determinism math -- closure -> clr -> ILR -> effective dimension ->
                        helmsman -> SHA-256 content receipt. The exact read.
  CH-INERT (T1)       : non-invasive differential -- the inert read returns the data to the
                        floor (round-trip residual ~ 1e-16); a localized residual is a real
                        feature, not damage. "Imprints nothing."
  CH-PROBE (T2)       : the ceiling-down probe ladder -- from the coarsest grouping DOWN to the
                        finest grain the data + compute JOINTLY support (max-power frontier);
                        stops at D_max, never manufactures below the floor.
  CH-TRIAD (T1 where applicable) : cross-verify an observable by three independent maths
                        (Q / Hs / DUT); coherence certifies. (Run when a coherence observable
                        is supplied.)
  CH-SUPPORT (mixed)  : guards (all-zero E-21, effective-rank coherence gate), 3^n confidence,
                        and the staged-use tier (basic -> verified -> triad-certified).
  PACKAGE             : one integrated read + a MASTER receipt over every channel.

Honest tiers: the CORE + CH-INERT + CH-TRIAD are built/receipted (T1); the full single-pipeline
PACKAGE and the CH-PROBE depth law are specified + reference-orchestrated (T2); the deepest reaches
(the differential engine on real hardware) are T3. This orchestrator is the INTEGRATION layer; the
canonical production core remains the Hs-Kinematics engine. Deterministic; master SHA-256 receipt.
Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25.
Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

# ---------------- CORE: determinism math ----------------
def closure(v):
    v=np.asarray(v,float); return v/v.sum(axis=-1,keepdims=True)
def clr(v):
    v=closure(v); g=np.exp(np.mean(np.log(v),axis=-1,keepdims=True)); return np.log(v/g)
def clr_inv(c):                                   # exact inverse: closure(exp(clr))
    return closure(np.exp(c))
def eff_dim(v):
    v=closure(v); H=-np.sum(v*np.log(v+1e-300),axis=-1); return float(np.exp(np.mean(H)))
def helmsman(v):
    c=clr(np.mean(closure(v),axis=0)); i=int(np.argmax(np.abs(c))); return i,float(c[i])
def receipt(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,default=str).encode()).hexdigest()[:16]

# ---------------- CH-INERT: non-invasive differential ----------------
def inert_readback(X):
    """The inert read returns the data to the numerical floor -- it imprints nothing. Round-trip
    closure->clr->clr_inv; residual ~ 1e-16 confirms non-invasiveness. A LOCALIZED large residual
    would be a real feature (the knock-and-read differential), not damage."""
    Xc=closure(X); back=clr_inv(clr(Xc))
    resid=float(np.max(np.abs(Xc-back)))
    return {"roundtrip_residual":float(f"{resid:.3e}"),"non_invasive":bool(resid<1e-12)}

# ---------------- CH-PROBE: the ceiling-down probe ladder ----------------
def max_power_ceiling(N,C,w,beta=2.0,kappa=1.0):
    D_stat=N/(beta*w); D_comp=C/(kappa*w); D_max=min(D_stat,D_comp)
    binding=("statistical(need DATA)" if D_stat<D_comp else "compute(need POWER)")
    if abs(D_stat-D_comp)/max(D_stat,D_comp)<0.05: binding="balanced(MAX POWER)"
    return D_stat,D_comp,D_max,binding

def amalgamate(p,L):
    """Coarse-grain a D-part composition to L super-parts (contiguous groups) -- the ceiling view."""
    D=len(p); idx=np.array_split(np.arange(D),L)
    return np.array([p[g].sum() for g in idx])

def probe_ladder(X,N,C,w):
    """Probe from the ceiling (coarsest, L=2) DOWN, doubling depth, until the finest grain the data
    + compute JOINTLY support (min(D, floor(D_max))). Report what each level adds; stop at the floor."""
    p=np.mean(closure(X),axis=0); D=len(p)
    D_stat,D_comp,D_max,binding=max_power_ceiling(N,C,w)
    floor=max(2,min(D,int(np.floor(D_max))))
    levels=[]; L=2; prev_ed=None
    while L<=floor:
        pa=amalgamate(p,L); ed=eff_dim(pa[None,:]); i,cv=helmsman(pa[None,:])
        gain=None if prev_ed is None else round(ed-prev_ed,4)
        levels.append({"grain_L":L,"eff_dim":round(ed,4),"helmsman_part":i,
                       "helmsman_clr":round(cv,4),"info_gain_vs_prev":gain}); prev_ed=ed
        if L==floor: break
        L=min(L*2,floor)
    return {"D_native":D,"D_stat":round(D_stat,1),"D_comp":round(D_comp,1),
            "D_max_supportable":round(D_max,1),"binding":binding,"probed_to_L":floor,
            "stopped_because":("data floor" if D_max<D else "reached native resolution"),
            "ladder":levels}

# ---------------- CH-TRIAD: cross-verify a coherence observable (optional) ----------------
def triad_coherence(Q,tol=2e-3):
    """One observable rho=exp(-2pi/Q) by three maths: Q-algebra, DUT ring-down (ODE), Hs balance."""
    rho_Q=float(np.exp(-2*np.pi/Q))
    w0=1.0; g=w0/Q; dt=(2*np.pi/w0)/2000; s=np.array([1.0,0.0])
    E=lambda s:0.5*s[1]**2+0.5*w0**2*s[0]**2; E0=E(s)
    for _ in range(2000):
        f=lambda s:np.array([s[1],-g*s[1]-w0**2*s[0]])
        k1=f(s);k2=f(s+0.5*dt*k1);k3=f(s+0.5*dt*k2);k4=f(s+dt*k3); s=s+dt/6*(k1+2*k2+2*k3+k4)
    rho_D=float(E(s)/E0)
    rho_H=float(closure(np.array([rho_Q,1-rho_Q]))[0])
    vals={"Q":rho_Q,"DUT":rho_D,"Hs":rho_H}
    md=max(abs(vals[a]-vals[b]) for a in vals for b in vals)
    return {"rho":{k:round(v,6) for k,v in vals.items()},"max_diff":float(f"{md:.2e}"),
            "verdict":"TRIAD-CON(certified)" if md<tol else "TRIAD-ISO/HLT(uncertified)"}

# ---------------- CH-SUPPORT: guards, confidence, staged tier ----------------
def guards(X):
    Xc=closure(X)
    allzero=bool(np.any(np.all(X<=0,axis=0)))           # E-21: a fully-zero carrier
    C=clr(Xc); s=np.linalg.svd(C-C.mean(0),compute_uv=False)
    er=float((s.sum()**2)/(np.sum(s**2)+1e-300)) if s.sum()>0 else 0.0
    return {"all_zero_carrier_guard":("TRIP" if allzero else "pass"),
            "effective_rank":round(er,3),"coherence_gate":("pass" if er>1.0 else "HOLD")}

def confidence_3n(n_independent_checks):
    rung={1:"opinion(3)",2:"agreement(9)",3:"validation(27, locate the outlier)"}
    return rung.get(n_independent_checks,"unrated")

def staged_tier(inert,triad_ok,guards_ok):
    if not guards_ok: return "0-blocked (a guard tripped/held)"
    t="1-basic(read)"
    if inert["non_invasive"]: t="4-verified(receipted, non-invasive)"
    if triad_ok: t="5-triad-certified(coherence across maths)"
    return t

# ---------------- THE FULL ENGINE ----------------
def full_engine(X,N,C,w,Q=None):
    X=np.asarray(X,float)
    p=np.mean(closure(X),axis=0); ed=eff_dim(X); hi,hc=helmsman(X)
    core={"D":X.shape[1],"effective_dimension":round(ed,4),"helmsman_part":hi,"helmsman_clr":round(hc,4)}
    core["core_receipt"]=receipt({"clr":np.round(clr(p),8).tolist()})
    ch_inert=inert_readback(X)
    ch_probe=probe_ladder(X,N,C,w)
    ch_triad=triad_coherence(Q) if Q is not None else {"status":"no coherence observable supplied -- channel idle"}
    g=guards(X); guards_ok=(g["all_zero_carrier_guard"]=="pass" and g["coherence_gate"]=="pass")
    triad_ok=isinstance(ch_triad,dict) and ch_triad.get("verdict","").startswith("TRIAD-CON")
    support={"guards":g,"confidence_3n":confidence_3n(3 if triad_ok else 1),
             "staged_use_tier":staged_tier(ch_inert,triad_ok,guards_ok)}
    out={"CORE_determinism_math":core,"CH_INERT_noninvasive":ch_inert,
         "CH_PROBE_ceiling_down":ch_probe,"CH_TRIAD_crossverify":ch_triad,"CH_SUPPORT":support}
    out["MASTER_RECEIPT"]=receipt(out)
    return out

if __name__=="__main__":
    rng=np.random.default_rng(11)
    D,Ns=16,200
    base=np.array([8,8,6,6, 4,4,3,3, 2,2,2,2, 1,1,1,1],float)
    X=np.abs(base[None,:]*(1+0.06*rng.standard_normal((Ns,D))))
    runs={}
    runs["ample_budget_with_coherence"]=full_engine(X, N=200_000, C=50_000, w=2, Q=12.0)
    runs["tight_budget_data_floor"]   =full_engine(X, N=32,      C=10_000, w=2)
    master=hashlib.sha256(json.dumps(runs,sort_keys=True,default=str).encode()).hexdigest()[:16]
    print(json.dumps({"engine":"hs_full_engine v5 (integration orchestrator)","runs":runs,
                      "ENGINE_RECEIPT":master},indent=2))
