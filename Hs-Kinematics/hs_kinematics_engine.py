#!/usr/bin/env python3
"""
Hˢ KINEMATICS ENGINE — the full system in one read, named for the navigator and the physicist,
revealed down to the computational floor.

This is the unified engine as now envisioned: it runs the complete Hˢ stack on a single
composition trajectory and emits the entire state — position, the lossless reconstruction,
the navigation reads, the full kinematic + dynamic tower (to its noise-bounded maximum), the
spectral modes, the honesty guards, the fringe/boundary (EITT in its new role) — every quantity
named TWICE (navigation / physics) per TERMINOLOGY_BRIDGE.md, every floor reported.

numpy + stdlib only. Deterministic; hash-receipted. Distilled (the frozen-oracle binary adds
the depth-tower/IR/CNQ recursion). Author: Peter Higgins (human authorship for claims);
AI-assisted per HUF-STD-001. Honest-broker; Tier 1 except the fringe layer (Tier 3, exploratory).
"""
import numpy as np, hashlib, json

# ---------------- geometry ----------------
def closure(M): M=np.clip(np.asarray(M,float),0,None); s=M.sum(1,keepdims=True); s[s==0]=1; return M/s
def clr(P): P=np.clip(P,1e-12,None); L=np.log(P); return L-L.mean(1,keepdims=True)
def helmert(D):
    B=np.zeros((D-1,D))
    for i in range(1,D): B[i-1,:i]=1.0/i; B[i-1,i]=-1.0; B[i-1]*=np.sqrt(i/(i+1.0))
    return B
def shannon_mean(P): P=closure(P); return float(-(P*np.log(np.clip(P,1e-12,None))).sum(1).mean())

# ---------------- E-21 carrier guard + zero treatment ----------------
def carrier_health(M):
    pos=(M>0); structural=[j for j in range(M.shape[1]) if not pos[:,j].any()]
    constant=[j for j in range(M.shape[1]) if np.ptp(M[:,j])==0 and j not in structural]
    active=[j for j in range(M.shape[1]) if j not in structural]
    return structural,constant,active
def treat_zeros(M):
    M=M.copy().astype(float)
    for j in range(M.shape[1]):
        p=M[M[:,j]>0,j]
        if p.size: M[M[:,j]<=0,j]=0.65*p.min()
    return M

# ---------------- lossless 4-part tiling ----------------
def tiling_lossless(P):
    T,D=P.shape
    if D<4: return None,True
    logP=np.log(np.clip(P,1e-12,None)); charts=[range(s,s+4) for s in range(D-3)]
    rows=[]; bij=[]
    for ch in charts:
        ch=list(ch)
        for ai in range(4):
            for ci in range(ai+1,4):
                i,j=ch[ai],ch[ci]; r=np.zeros(D); r[i]=1; r[j]=-1; rows.append(r); bij.append((i,j))
    A=np.vstack([np.array(rows),np.ones(D)]); errs=[]
    for t in range(min(T,50)):
        b=np.append([logP[t,i]-logP[t,j] for i,j in bij],0.0)
        rec,*_=np.linalg.lstsq(A,b,rcond=None); errs.append(np.max(np.abs(rec-clr(P[t:t+1])[0])))
    return float(max(errs)),True

# ---------------- navigation ----------------
def keff(P): P=np.clip(closure(P),1e-12,None); return np.exp(-(P*np.log(P)).sum(1))
def regimes(P,k=2.0):
    s=np.linalg.norm(np.diff(clr(P),axis=0),axis=1); thr=s.mean()+k*s.std(); return [int(i+1) for i,v in enumerate(s) if v>thr]
def deceptive(P):
    tv=0.5*np.abs(np.diff(closure(P),axis=0)).sum(1); dk=np.diff(keff(P)); return int(((dk<0)&(tv<=np.median(tv))).sum())

# ---------------- guards ----------------
def helmsman_guard(P,nm,floor=1e-6,tie=1e-3):
    tot=np.abs(np.diff(clr(P),axis=0)).sum(0); o=np.argsort(-tot); mag=float(tot[o[0]]); margin=float(tot[o[0]]-tot[o[1]]) if len(o)>1 else mag
    if mag<floor: return None,"HM-NUL-WRN"
    if margin<=tie*mag: return "TIE","HM-TIE-WRN"
    return nm[int(o[0])],None
def coherent_helmsman(P,nm):
    lP=np.log(np.clip(P,1e-12,None)); D=P.shape[1]; m=np.zeros(D)
    for i in range(D):
        for j in range(D):
            if i!=j: m[i]+=np.abs(np.diff(lP[:,i]-lP[:,j])).sum()
        m[i]/=(D-1)
    return nm[int(np.argmax(m))]
def effective_rank(P):
    X=clr(P); X=X-X.mean(0); s=np.linalg.svd(X,compute_uv=False); s=s[s>s.max()*1e-9] if s.max()>0 else s
    pr=float((s.sum()**2)/(s**2).sum()) if s.size else 0.0; maxr=min(P.shape[0]-1,P.shape[1]-1)
    return round(pr,2),maxr,("DG-RNK-WRN" if pr<0.5*maxr else None),s
def hold_lock(P,engine_floor=1e-9):
    H=clr(P); st=np.linalg.norm(np.diff(H,axis=0),axis=1)
    if st.size<2: return engine_floor,[]
    md=np.median(st); mad=np.median(np.abs(st-md))*1.4826
    noise=max(engine_floor,max(np.quantile(st,0.5)-mad,np.quantile(st,0.25)),1e-12); up,lo=4*noise,2*noise
    s="HOLD"; ev=[]; ref=0
    for t,m in enumerate(st):
        if s=="HOLD" and m>up: s="MOVING"
        elif s=="MOVING" and m<lo:
            if np.linalg.norm(H[t+1]-H[ref])>=3*noise: ev.append(t+1); ref=t+1
            s="HOLD"
    return round(noise,5),ev

# ---------------- mechanics (jet to noise floor, dynamics, integrals) ----------------
def mechanics(P,nm,dt=1.0,noise_ratio=1.5):
    R=clr(P); lab=["position","velocity","acceleration","jerk","snap","crackle"]; d=[R]
    for _ in range(5):
        if len(d[-1])<3: break
        d.append(np.diff(d[-1],axis=0)/dt)
    mag=[float(np.linalg.norm(x,axis=1).mean()) for x in d]; order=1; ratios={}
    for k in range(2,len(d)):
        r=mag[k]/(mag[k-1]+1e-30); ratios[lab[k]]=round(r,2)
        if r<noise_ratio: order=k
        else: break
    v=d[1]; a=d[2] if len(d)>2 else np.zeros_like(v[:-1]); mass=(P[:-1]+P[1:])/2
    vv=v[:len(a)]; That=vv/(np.linalg.norm(vv,axis=1,keepdims=True)+1e-30)
    kappa=np.linalg.norm(a-np.sum(a*That,1,keepdims=True)*That,axis=1)/(np.linalg.norm(vv,axis=1)**2+1e-30)
    p=mass*v; F=np.diff(p,axis=0)/dt; T=0.5*(mass*v*v).sum(1)
    Pnet=p.sum(0); permag=np.linalg.norm(p,axis=1)
    coh=float(np.linalg.norm(p.sum(0))/(permag.sum()+1e-30)); o=np.argsort(-Pnet)
    L=np.array([np.linalg.norm(np.outer(R[t],p[t])-np.outer(p[t],R[t]))/np.sqrt(2) for t in range(len(p))])
    pathlen=float(np.linalg.norm(v,axis=1).sum())
    return {"derivative_magnitudes":{lab[k]:round(mag[k],4) for k in range(1,len(d))},"amplification_ratios":ratios,
            "max_meaningful_order_NAV_sensor_limit__PHYS_noise_floor":f"{order} ({lab[order]})",
            "turn_rate_NAV__curvature_PHYS":round(float(np.median(kappa)),4),
            "arrow_of_intent_NAV__momentum_PHYS":{"to":[nm[j] for j in o if Pnet[j]>0][:3],"from":[nm[j] for j in o[::-1] if Pnet[j]<0][:3],"coherence":round(coh,3)},
            "reshaping_pressure_NAV__force_PHYS_mean":round(float(np.linalg.norm(F,axis=1).mean()),4),
            "activity_NAV__kinetic_energy_PHYS_mean":round(float(T.mean()),5),
            "circulation_NAV__angular_momentum_PHYS_mean":round(float(L.mean()),4),
            "journey_NAV__path_length_PHYS":round(pathlen,3),"net_course_NAV__displacement_PHYS":round(float(np.linalg.norm(R[-1]-R[0])),3),
            "course_directness_NAV__path_efficiency_PHYS":round(float(np.linalg.norm(R[-1]-R[0])/(pathlen+1e-30)),3),
            "transit_effort_NAV__action_PHYS":round(float(T.sum()),3)}

# ---------------- fringe / boundary (EITT new role, Tier 3) ----------------
def eitt_boundary(P,levels=(1,2,4),gate=0.01):
    def gm(k):
        Pc=closure(P); Tn=(len(Pc)//k)*k; G=[np.exp(np.log(Pc[i:i+k]).mean(0)) for i in range(0,Tn,k)]
        return closure(np.array(G)) if G else Pc[:1]
    Hs=[shannon_mean(gm(k)) for k in levels if len(P)//k>=2]; drift=(max(Hs)-min(Hs))/(abs(np.mean(Hs))+1e-12) if Hs else 0.0
    return {"entropy_by_level":[round(h,4) for h in Hs],"relative_drift":round(drift,4),
            "verdict":"within-regime (EITT holds; coherent structure)" if drift<gate else "BOUNDARY (edge of analysable structure)",
            "code":None if drift<gate else "FR-BND-INF","tier":"Tier 3 fringe -- a clue, never a claim"}

def stable_hash(o,dp=12):
    def nz(x):
        if isinstance(x,float): return round(x,dp)
        if isinstance(x,dict): return {k:nz(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)): return [nz(v) for v in x]
        return x
    return hashlib.sha256(json.dumps(nz(o),sort_keys=True,default=str).encode()).hexdigest()

# ================= the engine =================
def run(M,names=None,dt=1.0):
    M=np.asarray(M,float); names=list(names) if names is not None else [f"c{j}" for j in range(M.shape[1])]
    struct,const,active=carrier_health(M); guard=None
    if struct or const:
        guard={"excluded_structural_zero":[names[j] for j in struct],"flagged_constant":[names[j] for j in const],
               "codes":(["GD-ZRC-CAL"] if struct else [])+(["GD-CNC-CAL"] if const else [])}
        if struct: M=M[:,active]; names=[names[j] for j in active]
    sparsity=float((M<=0).mean()); M=treat_zeros(M); P=closure(M)
    recon,conn=tiling_lossless(P); helm,hcode=helmsman_guard(P,names); er=effective_rank(P); floor,ev=hold_lock(P)
    codes=[c for c in (hcode,er[2]) if c]+([f"GD-SPZ-WRN"] if sparsity>=0.5 else [])+(guard["codes"] if guard else [])
    payload={
      "identity":"Hs kinematics engine (distilled; named for navigator + physicist; to the computational floor)",
      "input":{"records":int(P.shape[0]),"carriers":int(P.shape[1]),"names":names,"sparsity_pct":round(sparsity*100,1)},
      "dead_reckoning_NAV__lossless_reconstruction_PHYS":{"exact":bool(conn and (recon is None or recon<1e-6)),"reconstruction_error":recon},
      "navigation_reads":{
        "effective_spread_NAV__entropy_diversity_PHYS":{"start":round(float(keff(P)[0]),3),"end":round(float(keff(P)[-1]),3)},
        "helmsman_steerer_NAV__fastest_coordinate_PHYS":{"clr":names[int(np.argmax(np.abs(np.diff(clr(P),axis=0)).sum(0)))],"resolvable":helm,"coherent_robust":coherent_helmsman(P,names)},
        "waypoints_NAV__phase_transitions_PHYS":regimes(P),
        "silent_drift_NAV__adiabatic_drift_PHYS":deceptive(P)},
      "kinematics_and_dynamics":mechanics(P,names,dt),
      "spectral_modes":{"motion_mode_singulars":[round(float(x),3) for x in er[3][:5]],"degrees_of_freedom_NAV__effective_dimensionality_PHYS":er[0]},
      "station_keeping_NAV__equilibrium_hold_PHYS":{"discovered_noise_floor":floor,"structural_changes_at":ev},
      "guards_codes_fired":codes,
      "fringe_boundary_TIER3":eitt_boundary(P),
      "computational_floors":{"ieee_reconstruction_floor":recon,"determinism_decimals":12,"discovered_noise_floor":floor,
                              "max_meaningful_derivative_order":mechanics(P,names,dt)["max_meaningful_order_NAV_sensor_limit__PHYS_noise_floor"]}}
    if guard: payload["input"]["carrier_guard"]=guard
    payload["content_hash"]=stable_hash(payload)
    return payload

if __name__=="__main__":
    rng=np.random.default_rng(0); T,D=60,8
    names=["Coal","Gas","Hydro","Nuclear","Wind","Solar","Bio","Other"]
    base=np.array([.30,.22,.18,.12,.08,.04,.04,.02])
    M=np.maximum(base+np.cumsum(rng.normal(0,.01,(T,D)),0)+rng.normal(0,.005,(T,D)),1e-4)
    print(json.dumps(run(M,names),indent=1))
