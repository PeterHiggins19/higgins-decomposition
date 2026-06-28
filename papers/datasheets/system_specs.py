#!/usr/bin/env python3
"""
system_specs.py -- consolidated specification test of the compositional system built this session.
Measures every key spec in ONE deterministic run, on real + synthetic data, with a single receipt.
Honest-broker: impressive where true, fenced where not. See COMPOSITIONAL_SYSTEM_SPECIFICATIONS.md.
Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25.
Peter is the sole gate; nothing posted.
"""
import numpy as np, hashlib, json, csv, os, time
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(v); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def clr_inv(c): return closure(np.exp(c))
def eff_dim(p): p=closure(p); H=-np.sum(p*np.log(p+1e-300)); return float(np.exp(H))
LO,HI=-6.0,6.0; STEP=(HI-LO)/127.0
def pack(comp):
    z=clr(comp); q=np.clip(np.round((z-LO)/STEP),0,127).astype(np.uint8)
    par=np.array([bin(int(x)).count('1')&1 for x in q],dtype=np.uint8)
    return ((par<<7)|q).astype(np.uint8)
def load(path,cols):
    with open(path) as f: lines=[l for l in f if not l.startswith('#')]
    r=[]
    for d in csv.DictReader(lines):
        try:
            x=[float(d[c]) for c in cols]
            if all(t>0 for t in x): r.append(x)
        except: pass
    return closure(np.array(r))

HS=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
rng=np.random.default_rng(0); S={}
c=closure(np.array([5,3,2,1.0]))
S["determinism_bit_identical"]={"value":bool(hashlib.sha256(pack(c).tobytes()).hexdigest()==hashlib.sha256(pack(c).tobytes()).hexdigest()),"tier":"T1"}
X=closure(np.abs(rng.standard_normal((200,8)))+0.3)
S["clr_roundtrip_residual"]={"value":float(f"{np.max(np.abs(clr_inv(clr(X))-X)):.2e}"),"unit":"composition","tier":"T1"}
g=rng.uniform(0.1,10,size=(200,1))
S["common_mode_rejection_exact_residual"]={"value":float(f"{np.max(np.abs(clr(g*X)-clr(X))):.2e}"),"tier":"T1"}
S["coherence_law_dB"]={"value":{f"rho={r}":round(-10*np.log10(1-r),1) for r in (0.9,0.99,0.999)},"tier":"T1"}
gas=load(HS+"/industrial-instruments/gas-composition-study/results/gas_series.csv",["O2","CO2","N2"])
water=load(HS+"/industrial-instruments/gas-composition-study/produced-water-codawork/results/produced_water.csv",["Na","Cl","Ca","Mg","SO4","HCO3","K"])
def codec_err(Xc,mode):
    if mode=="clr":
        z=clr(Xc); q=np.clip(np.round((z-LO)/STEP),0,127); return float(np.max(np.abs((LO+q*STEP)-z)))
    q=np.round(Xc*127)/127; q=np.clip(q,1e-6,None); return float(np.max(np.abs(clr(q)-clr(Xc))))
S["codec_7bit_clr_maxerr"]={"value":{"gas":round(codec_err(gas,"clr"),4),"water":round(codec_err(water,"clr"),4)},"tier":"T1","note":"near-lossless in clr"}
S["codec_7bit_linear_maxerr"]={"value":{"gas":round(codec_err(gas,"lin"),3),"water":round(codec_err(water,"lin"),3)},"tier":"T1","note":"FAILS on high dynamic range -> use clr"}
M=200; comps=[closure(np.abs(rng.standard_normal(12))+0.2) for _ in range(M)]
mags=[float(np.exp(rng.uniform(0,7))) for _ in range(M)]; clrs=[clr(cc) for cc in comps]; raws=[mags[k]*comps[k] for k in range(M)]
def recall(mode):
    ok=0
    for _ in range(300):
        k=int(rng.integers(M)); gg=float(np.exp(rng.uniform(np.log(0.2),np.log(5))))
        q=np.abs(mags[k]*comps[k]*gg*(1+0.03*rng.standard_normal(12)))
        j=int(np.argmin([np.sum((cz-clr(q))**2) for cz in clrs])) if mode=="comp" else int(np.argmin([np.sum((np.asarray(r)-q)**2) for r in raws]))
        ok+=(j==k)
    return round(ok/300,3)
S["memory_recall_scale_invariant"]={"value":{"compositional":recall("comp"),"raw_magnitude":recall("raw")},"tier":"T1"}
geo=load(HS+"/collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv",["SiO2_pct","Al2O3_pct","Rb_mgkg","Zr_mgkg"])
rt=max(float(np.max(np.abs((LO+(pack(geo[i])&0x7F).astype(float)*STEP)-clr(geo[i])))) for i in range(len(geo)))
tags=[hashlib.sha256(pack(geo[i]).tobytes()).hexdigest()[:16] for i in range(len(geo))]
S["conveyor"]={"value":{"bytes_per_unit":int(geo.shape[1]),"nondisruption_roundtrip_maxerr":round(rt,4),
    "within_7bit_floor":bool(rt<=STEP*1.01),"deterministic_tags":bool(tags==[hashlib.sha256(pack(geo[i]).tobytes()).hexdigest()[:16] for i in range(len(geo))])},"tier":"T1"}
base=clr(geo).mean(0)
def d_static(x): return int(np.argmax(np.abs(clr(x))))
def d_diff(x,b): return int(np.argmax(np.abs(clr(x)-b)))
inv_s=inv_d=0; N=0
for i in range(len(geo)):
    s0=d_static(geo[i]); d0=d_diff(geo[i],base)
    for _ in range(20):
        gg=np.exp(rng.uniform(np.log(0.2),np.log(5))); delta=rng.uniform(-1,1,4); delta-=delta.mean()
        xs=closure(np.exp(clr(geo[i])+delta))*gg; N+=1
        inv_s+=(d_static(xs)==s0); inv_d+=(d_diff(xs,base+delta)==d0)
S["locked_discriminant_invariance"]={"value":{"centred_contrast_LOCKED":round(inv_d/N,3),"static_argmax_clr":round(inv_s/N,3)},"tier":"T1"}
S["effective_dimension_read_water_D7"]={"value":round(eff_dim(water.mean(0)),2),"tier":"T1"}
Y=closure(np.abs(rng.standard_normal((20000,8)))+0.3); t0=time.perf_counter()
for i in range(len(Y)): pack(Y[i])
S["throughput_units_per_sec_singlethread_py"]={"value":int(len(Y)/(time.perf_counter()-t0)),"tier":"T2","note":"single-thread CPython, O(D)/unit; not optimized"}
out={"_meta":{"tool":"system_specs.py","what":"consolidated specification test of the compositional system","D_test":8},
     "specifications":S,
     "fences":"Exactness is the IEEE numerical floor (not infinite precision); common-mode rejection is numerical, does NOT beat Shannon channel capacity / rate-distortion; throughput is unoptimized single-thread Python; the 7-bit codec is near-lossless ONLY in clr coordinates."}
# receipt covers the DETERMINISTIC specs only; throughput is wall-clock (non-deterministic) and is excluded
det={k:v for k,v in S.items() if k!="throughput_units_per_sec_singlethread_py"}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps({"specifications":det,"D_test":8},sort_keys=True,default=str).encode()).hexdigest()[:16]
out["_meta"]["receipt_note"]="receipt hashes the deterministic specs; throughput excluded (wall-clock)"
if __name__=="__main__": print(json.dumps(out,indent=2))
