#!/usr/bin/env python3
"""
Hˢ moving-budget tracker — the SIZE trajectory the engine's closure throws away.

A composition has a SHAPE (the closed proportions, scale-free — what the kinematics engine reads)
and a SIZE (the total before closure — the budget). In a dynamic system the budget MOVES, and that
motion is information a control/test system needs: is the whole thing growing or shrinking, how fast,
is the growth steady or lurching, and does the mix move when the budget moves? This module reads the
moving budget with the same kinematic discipline the engine applies to the shape, and reports the
SIZE-SHAPE COUPLING. numpy+stdlib; deterministic; hash-receipted. Companion to hs_kinematics_engine.
Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker.
"""
import numpy as np, hashlib, json

def _clr_steps(M):
    P=np.clip(M,1e-12,None); P=P/P.sum(1,keepdims=True); L=np.log(P); C=L-L.mean(1,keepdims=True)
    return np.linalg.norm(np.diff(C,axis=0),axis=1)   # shape motion per step

def _hold_regimes(x, floor=1e-9):
    """discovered-floor + hysteresis on a 1-D log series (same logic as the engine's hold_lock)."""
    st=np.abs(np.diff(x))
    if st.size<2: return floor,[]
    md=np.median(st); mad=np.median(np.abs(st-md))*1.4826
    noise=max(floor,max(np.quantile(st,0.5)-mad,np.quantile(st,0.25)),1e-12); up,lo=4*noise,2*noise
    s="HOLD"; ev=[]; ref=0
    for t,m in enumerate(st):
        if s=="HOLD" and m>up: s="MOVING"
        elif s=="MOVING" and m<lo:
            if abs(x[t+1]-x[ref])>=3*noise: ev.append(t+1); ref=t+1
            s="HOLD"
    return round(noise,6),ev

def track_budget(M, names=None, dt=1.0):
    """Track the moving budget (total/size) of a raw, UN-closed matrix M [T x D]."""
    M=np.asarray(M,float); T=M.shape[0]
    N=M.sum(1)                                  # the budget: total per record
    Npos=np.clip(N,1e-30,None); logN=np.log(Npos)
    g=np.diff(logN)/dt                          # multiplicative growth rate (budget velocity)
    accel=np.diff(g)/dt if g.size>1 else np.array([0.0])
    coh=float(abs(g.sum())/(np.abs(g).sum()+1e-30))   # 1 = steady directed growth, 0 = churning size
    cagr=float(np.exp(logN[-1]-logN[0])**(1.0/max(T-1,1))-1.0)
    floor,regimes=_hold_regimes(logN)
    # size-shape coupling: does the mix move when the budget moves?
    shape=_clr_steps(M)
    g_abs=np.abs(g[:len(shape)]); sh=shape[:len(g_abs)]
    if g_abs.size>2 and g_abs.std()>0 and sh.std()>0:
        coupling=float(np.corrcoef(g_abs,sh)[0,1])
    else: coupling=0.0
    out={
      "identity":"Hs moving-budget tracker (the size trajectory; companion to the shape engine)",
      "budget_size_NAV__total_magnitude_PHYS":{"start":round(float(N[0]),4),"end":round(float(N[-1]),4),
            "total_growth_factor":round(float(N[-1]/(N[0]+1e-30)),4)},
      "budget_velocity_NAV__growth_rate_PHYS":{"mean_per_step":round(float(g.mean()),5),
            "CAGR_per_step":round(cagr,5),"end_minus_start_log":round(float(logN[-1]-logN[0]),4)},
      "budget_acceleration_PHYS":round(float(accel.mean()),6),
      "budget_coherence":round(coh,3),    # steady-growth(1) vs churning-size(0)
      "budget_regimes_at":regimes,        # where the GROWTH regime changed (hold-locked)
      "budget_noise_floor":floor,
      "size_shape_coupling":round(coupling,3),   # +1: mix moves most when budget moves; ~0: independent
      "reading":("steady growth" if coh>0.6 and g.mean()>0 else
                 "steady decline" if coh>0.6 and g.mean()<0 else
                 "volatile budget (churning size)")}
    def nz(x):
        if isinstance(x,float): return round(x,12)
        if isinstance(x,dict): return {k:nz(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)): return [nz(v) for v in x]
        return x
    out["content_hash"]=hashlib.sha256(json.dumps(nz(out),sort_keys=True,default=str).encode()).hexdigest()
    return out

if __name__=="__main__":
    # a budget that grows ~3% per step with a mid-series acceleration
    T=40; base=100*np.exp(np.cumsum(np.r_[np.full(20,0.02),np.full(19,0.05)]))
    shares=np.array([.4,.3,.2,.1]); M=np.outer(base,shares)*(1+0.01*np.sin(np.arange(T))[:,None])
    print(json.dumps(track_budget(M,["a","b","c","d"]),indent=1))
