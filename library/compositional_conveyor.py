#!/usr/bin/env python3
"""
compositional_conveyor.py -- the self-tagging 8-bit compositional conveyor + deterministic router.

Each data unit (one composition sample) packages ITSELF into 8-bit form and routes ITSELF through the
command chain, native to the existing pipeline and non-disruptive:

  * 7-bit payload : clr of the composition, quantized to 7 bits per part (the right-sized codec, G-239).
  * 8th bit       : an integrity / "how-to-use" flag per byte (XOR parity of the low 7 bits), stripped on
                    decode (b & 0x7F) -- the V∞Core 8th-bit idea.
  * unit tag      : SHA-256 of the packed bytes = the content address (the unit tags itself).
  * routing       : (a) HASH route = tag % lanes (dedup / load-balance; deterministic);
                    (b) STRUCTURAL route = the DIFFERENTIAL helmsman (argmax|clr - running_baseline|) -- the
                        unit self-sorts to the lane of its dominant REGIME deviation (content-aware,
                        deterministic given stream order, locality-preserving).
NON-DISRUPTIVE : a pass-through layer -- decode reproduces the original clr to the 7-bit floor; the source
                 read is preserved. The buffer is a ring (FIFO) the units flow through as conveyors.

HONEST: T1 = encode/decode + content-tag + deterministic routing (exact / reproducible). T2 = the streaming
buffer + the differential-routing baseline (modeled). T3 vision = native integration across ALL live projects
top-to-bottom without disruption. Overlaps message queues / content-addressable storage / self-describing
packets; the novelty is compositional (scale-invariant, regime-aware) routing + deterministic 8-bit
self-tagging. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-25. Peter is the sole gate; nothing posted.
"""
import numpy as np, hashlib, json, csv, collections, os, sys

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(v); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
LO,HI=-6.0,6.0; STEP=(HI-LO)/127.0

def pack_unit(comp):
    z=clr(comp); q=np.clip(np.round((z-LO)/STEP),0,127).astype(np.uint8)        # 7-bit payload
    par=np.array([bin(int(x)).count('1')&1 for x in q],dtype=np.uint8)          # XOR parity -> 8th bit
    b=((par<<7)|q).astype(np.uint8)                                             # the 8-bit data bunch
    tag=hashlib.sha256(b.tobytes()).hexdigest()[:16]                           # self-tag (content address)
    return b,tag,z
def unpack_unit(b):
    return LO+(b & 0x7F).astype(float)*STEP                                     # strip 8th bit (how-to-use)

class Conveyor:
    def __init__(self,lanes=8,bufsize=64):
        self.lanes=lanes; self.buf=collections.deque(maxlen=bufsize)
        self.routed=collections.Counter(); self.mean=None; self.kk=0
    def push(self,comp):
        b,tag,z=pack_unit(comp)
        base=self.mean if self.mean is not None else np.zeros_like(z)
        struct_route=int(np.argmax(np.abs(z-base)))                             # DIFFERENTIAL helmsman: self-sort by regime
        self.kk+=1; self.mean=z.copy() if self.mean is None else self.mean+(z-self.mean)/self.kk
        hash_route=int(tag,16)%self.lanes
        self.buf.append((tag,b)); self.routed[struct_route]+=1
        return tag,b,hash_route,struct_route

def load_comp(path,cols):
    with open(path) as f: lines=[l for l in f if not l.startswith('#')]
    rows=[]
    for d in csv.DictReader(lines):
        try:
            v=[float(d[c]) for c in cols]
            if all(x>0 for x in v): rows.append(v)
        except: pass
    return closure(np.array(rows))

def run(path,cols,name):
    X=load_comp(path,cols); n,D=X.shape
    conv=Conveyor(lanes=8); tags=[];routes=[];rt_err=0.0
    for i in range(n):
        tag,b,hr,sr=conv.push(X[i]); tags.append(tag); routes.append(sr)
        rt_err=max(rt_err,float(np.max(np.abs(unpack_unit(b)-clr(X[i])))))      # non-disruption: roundtrip clr error
    conv2=Conveyor(lanes=8); tags2=[];routes2=[]
    for i in range(n):
        tag,b,hr,sr=conv2.push(X[i]); tags2.append(tag); routes2.append(sr)
    det=(tags==tags2) and (routes==routes2)
    return {"project":name,"n_units":n,"D":D,"bytes_per_unit":D,
            "roundtrip_clr_max_error_7bit_floor":round(rt_err,4),
            "non_disruption_preserved":bool(rt_err<=STEP*1.01),
            "deterministic_tags_and_routes":bool(det),
            "self_sort_by_regime_lane_counts":dict(sorted(conv.routed.items())),
            "sample_unit_tag":tags[0]}

if __name__=="__main__":
    HS=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
    gpath=HS+"/collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv"
    with open(gpath) as f: hdr=[l for l in f if not l.startswith('#')][0].strip().split(',')
    xrf=[c for c in hdr if c not in ('depth_m','sample','id')][:4]
    geo=run(gpath,xrf,"GEO Frielingen-9 (terrestrial gather)")
    arr=run(HS+"/experiments/Hs-17_Backblaze/Hs-17_fleet_composition.csv",["Mechanical","Thermal","Age"],
            "ARRAY Backblaze fleet (remote sensor array)")
    out={"_meta":{"tool":"compositional_conveyor.py","xrf_cols":xrf,
                  "what":"8-bit self-tagging compositional conveyor + deterministic router, run top-down on two real projects"},
         "geo_project":geo,"remote_sensor_array":arr}
    out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()[:16]
    print(json.dumps(out,indent=2))
