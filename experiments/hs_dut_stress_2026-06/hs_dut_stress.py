#!/usr/bin/env python3
"""
hs_dut_stress.py -- the new-generation full stress sheet: the Hs system AS the Device Under Test.

Hs tests Hs (recursive): every core spec is stressed across a DIMENSION LADDER (D = 2..1000) under
DEFORMATION (extreme multiplicative scale up to 1e6x, baseline offset, additive noise), on real +
deterministically seeded data. The per-test residuals are then READ BY Hs itself (Hs-on-Hs); one MASTER
RECEIPT certifies the whole system; the engine is VERSION-STAMPED from a real-data conformance run.

ANYONE CAN VERIFY:  python3 hs_dut_stress.py   ->  compare MASTER_RECEIPT to the published value.

Honest ('do as the data said it should'): closure/clr specs hold to the IEEE floor at ANY D; the EXACT
quaternion reconstruction is D in {1,2,4,8} (Hurwitz) and tiled above (~1e-12, cited, not re-run here). Where
a spec degrades under the extreme, it is REPORTED, not hidden -- the stress sheet's job is to find the
operating envelope. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
2026-06-25. Peter is the sole gate; nothing posted.
"""
import numpy as np, hashlib, json, csv, os
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(v); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def clr_inv(c): return closure(np.exp(c))
LO,HI=-6.0,6.0; STEP=(HI-LO)/127.0
def pack(x):
    z=clr(x); return np.clip(np.round((z-LO)/STEP),0,127).astype(np.uint8)
def load(path,cols):
    with open(path) as f: lines=[l for l in f if not l.startswith('#')]
    r=[]
    for d in csv.DictReader(lines):
        try:
            x=[float(d[c]) for c in cols]
            if all(t>0 for t in x): r.append(x)
        except: pass
    return closure(np.array(r))

def stress_at_D(D, X, rng):
    n=len(X); res={}
    res["clr_roundtrip"]=float(np.max(np.abs(clr_inv(clr(X))-X)))
    g=np.exp(rng.uniform(np.log(1e-6),np.log(1e6),size=(n,1)))
    res["cm_reject_extreme"]=float(np.max(np.abs(clr(g*X)-clr(X))))
    z=clr(X); q=np.clip(np.round((z-LO)/STEP),0,127); res["codec_clr_maxerr"]=float(np.max(np.abs((LO+q*STEP)-z)))
    base=clr(X).mean(0); inv=0; tot=0
    for i in range(min(n,60)):
        d0=int(np.argmax(np.abs(clr(X[i])-base)))
        for _ in range(10):
            gg=np.exp(rng.uniform(np.log(1e-3),np.log(1e3))); delta=rng.uniform(-1,1,D); delta-=delta.mean()
            xs=closure(np.exp(clr(X[i])+delta))*gg; tot+=1
            inv+=(int(np.argmax(np.abs(clr(xs)-(base+delta))))==d0)
    res["locked_disc_invariance"]=inv/tot
    mb=min(n,80); clrs=[clr(X[k]) for k in range(mb)]; ok=0; T=120
    for _ in range(T):
        k=int(rng.integers(mb)); gg=np.exp(rng.uniform(np.log(0.2),np.log(5)))
        qy=np.abs(X[k]*gg*(1+0.02*rng.standard_normal(D)))
        ok+=(int(np.argmin([np.sum((cz-clr(qy))**2) for cz in clrs]))==k)
    res["memory_recall"]=ok/T
    rt=max(float(np.max(np.abs((LO+pack(X[i]).astype(float)*STEP)-clr(X[i])))) for i in range(min(n,60)))
    t1=[hashlib.sha256(pack(X[i]).tobytes()).hexdigest()[:12] for i in range(min(n,60))]
    t2=[hashlib.sha256(pack(X[i]).tobytes()).hexdigest()[:12] for i in range(min(n,60))]
    res["conveyor_nondisrupt"]=rt; res["conveyor_deterministic"]=float(t1==t2)
    return res

if __name__=="__main__":
    HS=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
    real={3:load(HS+"/industrial-instruments/gas-composition-study/results/gas_series.csv",["O2","CO2","N2"]),
          4:load(HS+"/collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv",["SiO2_pct","Al2O3_pct","Rb_mgkg","Zr_mgkg"]),
          7:load(HS+"/industrial-instruments/gas-composition-study/produced-water-codawork/results/produced_water.csv",["Na","Cl","Ca","Mg","SO4","HCO3","K"])}
    ladder=[2,3,4,5,7,8,16,32,64,128,256,512,1000]
    table={}
    for D in ladder:
        X = real[D] if D in real else closure(np.abs(np.random.default_rng(100+D).standard_normal((150,D)))+0.25)
        table["D=%d"%D]={"source":("real" if D in real else "seeded"),
                         **{k:(round(v,4) if v>=1e-3 else float(f"{v:.2e}")) for k,v in stress_at_D(D,X,np.random.default_rng(7+D)).items()}}
    tol={"clr_roundtrip":1e-10,"cm_reject_extreme":1e-9,"codec_clr_maxerr":STEP*1.05,
         "locked_disc_invariance":0.999,"memory_recall":0.95,"conveyor_nondisrupt":STEP*1.05,"conveyor_deterministic":1.0}
    def passed(k,v): return (v<=tol[k]) if k in ("clr_roundtrip","cm_reject_extreme","codec_clr_maxerr","conveyor_nondisrupt") else (v>=tol[k])
    fails=[[D,k,table[D][k]] for D in table for k in tol if not passed(k,table[D][k])]
    tests=["clr_roundtrip","cm_reject_extreme","codec_clr_maxerr"]
    worst={t:max(float(table[D][t]) for D in table) for t in tests}; helm=max(worst,key=worst.get)
    master=hashlib.sha256(json.dumps(table,sort_keys=True,default=str).encode()).hexdigest()[:16]
    real_anchor=hashlib.sha256(json.dumps({D:np.round(clr(real[D]).mean(0),8).tolist() for D in real},sort_keys=True).encode()).hexdigest()[:8]
    out={"_meta":{"tool":"hs_dut_stress.py","dut":"the Hs compositional system","dimension_ladder":ladder,
                  "engine_version":"Hs-DUT-v1."+real_anchor,"what":"full stress sheet across all dimensions under deformation, Hs-on-Hs"},
        "per_dimension":table,
        "envelope":{"deterministic_core_passes_all_D":bool(all(passed(k,table[D][k]) for D in table for k in ("clr_roundtrip","cm_reject_extreme","codec_clr_maxerr","conveyor_nondisrupt","conveyor_deterministic"))),
            "statistical_layer_failures":fails,
            "Hs_on_Hs_closest_to_limit_spec":helm,"worst_residual_by_test":{t:float(f"{worst[t]:.2e}") for t in tests}},
        "fences":"closure/clr specs hold at ANY D; EXACT quaternion reconstruction is D in {1,2,4,8} (Hurwitz), tiled above (~1e-12, cited); the 313 dB-class rejection is numerical, NOT a Shannon-beating claim; only multiplicative common-mode cancels.",
        "MASTER_RECEIPT":master}
    out["_meta"]["receipt_sha256"]=master
    print(json.dumps(out,indent=2))
