#!/usr/bin/env python3
"""
canada_energy_governance.py -- the governance application, on data Canada already collects (EMBER, public).
A. FULL EMBER READ (all countries + Canada): where each grid STANDS (latest mix, dominant source, clean vs
   fossil, effective dimension) and the DIRECTION it takes (directedness + motion-helmsman).
B. GRID-STEERING MANIFOLD SIMULATOR: candidate policy levers on Canada's mix -> resulting mix + LEVER
   EFFICIENCY (compositional move per TWh) = the deterministic control manifold.
VALUE: method marginal cost ~0 (reads data already collected); the steerable system is sized FROM the data
(generation TWh x a stated wholesale price) -- a $ on the SCALE steered, not a fabricated saving.

HONEST: public EMBER data; $ illustrative with a STATED price (not a forecast/saving); simulator is a
deterministic COMPOSITIONAL what-if (no grid-physics/reliability/price model); Ontario/provincial needs the
public IESO plug-in (named pilot); direction measured, the policy choice is the operator's leap (Breaker 16).
Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, csv, json, hashlib, os
HS=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
EMB=os.path.join(HS,"data","Energy","EMBER_pipeline_ready")
FLOOR=1e-9
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,FLOOR,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def eff_dim(v): v=closure(v); H=-np.sum(v*np.log(v+1e-300),-1); return float(np.exp(np.mean(H)))
def receipt(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
FOSSIL={"Coal","Gas","Other Fossil"}
def load(path):
    with open(path) as f: rows=list(csv.reader(f))
    hdr=rows[0]; src=hdr[1:]; years=[]; M=[]
    for r in rows[1:]:
        try: years.append(int(r[0])); M.append([float(x) for x in r[1:]])
        except (ValueError,IndexError): pass
    return src,years,np.clip(np.array(M),0,None)
def country_read(path):
    src,years,M=load(path); latest=M[-1]; tot=float(latest.sum()); share=closure(np.clip(latest,FLOOR,None))
    dom=src[int(np.argmax(share))]; fossil=float(sum(share[i] for i,s in enumerate(src) if s in FOSSIL))
    C=clr(np.clip(M,FLOOR,None)); path_len=float(np.sum(np.linalg.norm(np.diff(C,axis=0),axis=1))); net=float(np.linalg.norm(C[-1]-C[0]))
    vel=np.sum(np.abs(np.diff(C,axis=0)),axis=0); mover=src[int(np.argmax(vel))]
    return {"years":[years[0],years[-1]],"generation_TWh_latest":round(tot,1),"dominant_source":dom,
            "fossil_share":round(fossil,3),"clean_share":round(1-fossil,3),"effective_dimension":round(eff_dim(share),2),
            "directedness":round(net/path_len,3) if path_len else None,"motion_helmsman":mover,"_src":src,"_latest":latest}
files=sorted(f for f in os.listdir(EMB) if f.endswith(".csv")); allc={}
for f in files:
    code=f.split("_")[1]; r=country_read(os.path.join(EMB,f)); allc[code]={k:v for k,v in r.items() if not k.startswith("_")}
    if code=="CAN": can_full=r
src=can_full["_src"]; base=can_full["_latest"].copy(); idx={s:i for i,s in enumerate(src)}
def apply_levers(base,lev):
    x=base.astype(float).copy()
    for s,d in lev.items(): x[idx[s]]=max(x[idx[s]]+d,0.0)
    return x
def mix_metrics(x):
    sh=closure(np.clip(x,FLOOR,None)); foss=float(sum(sh[i] for i,s in enumerate(src) if s in FOSSIL))
    return {"generation_TWh":round(float(x.sum()),1),"fossil_share":round(foss,3),"clean_share":round(1-foss,3),"dominant":src[int(np.argmax(sh))]}
LEVERS={"+15 TWh Solar":{"Solar":15.0},"+15 TWh Wind":{"Wind":15.0},"-15 TWh Gas":{"Gas":-15.0},"+10 Solar +10 Wind -15 Gas":{"Solar":10.0,"Wind":10.0,"Gas":-15.0}}
base_m=mix_metrics(base); base_clr=clr(np.clip(base,FLOOR,None)); sim=[]
for name,lev in LEVERS.items():
    x=apply_levers(base,lev); m=mix_metrics(x); move=float(np.linalg.norm(clr(np.clip(x,FLOOR,None))-base_clr)); tw=sum(abs(v) for v in lev.values())
    sim.append({"lever":name,"result":m,"fossil_share_delta":round(m["fossil_share"]-base_m["fossil_share"],3),"compositional_move":round(move,4),"efficiency_move_per_TWh":round(move/tw,5)})
sim.sort(key=lambda s:-s["efficiency_move_per_TWh"])
PRICE_USD_PER_MWh=50.0; can_twh=can_full["generation_TWh_latest"]
system_flow_usd_bn=round(can_twh*1e6*PRICE_USD_PER_MWh/1e9,1)
canf={k:v for k,v in can_full.items() if not k.startswith("_")}
value={"method_marginal_cost":"~0 (reads data already collected)","canada_generation_TWh":can_twh,
       "price_assumption_USD_per_MWh":PRICE_USD_PER_MWh,"steerable_system_flow_USD_billion_per_year":system_flow_usd_bn,
       "framing":"a $ on the SCALE of the system better steering acts on -- NOT a claimed saving"}
out={"_meta":{"tool":"canada_energy_governance.py","source":"EMBER public generation data (TWh by source)","n_countries":len(allc)},
     "A_where_each_stands_and_direction":allc,"CANADA_focus":canf,
     "B_grid_steering_manifold":{"current_mix":base_m,"levers_ranked_by_efficiency":sim,
        "reading":"efficiency = compositional move per TWh acted -- the deterministic control manifold"},
     "value":value,
     "fence":("Public EMBER data; $ figures ILLUSTRATIVE with a STATED price (not a forecast/guaranteed saving); "
        "simulator is a deterministic COMPOSITIONAL what-if (no grid-physics/reliability/price-response model); "
        "Ontario/provincial needs the public IESO provincial-generation plug-in (named pilot). Direction measured; "
        "the policy choice is the operator's leap (Breaker 16). Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=receipt({"all":allc,"can":canf,"sim":sim,"value":value})
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"CANADA_ENERGY_GOVERNANCE_RESULTS.json"),"w") as f:
    json.dump(out,f,indent=2)
if __name__=="__main__": print(json.dumps(out,indent=2))
