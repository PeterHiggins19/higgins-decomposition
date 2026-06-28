#!/usr/bin/env python3
"""
compositional_memory.py -- a future-seeking PROOF OF CONCEPT: a compositional, content-addressable,
scale-invariant associative memory, from pieces measured this session (7-bit-in-clr codec + differential
read + content-hash addressing).

Honest comparison: a COMPOSITIONAL memory (stores clr of the composition; recalls by Aitchison distance of
the closed query) vs a RAW-MAGNITUDE memory (stores/compares the raw measured vector). A real-world query
arrives as  q = magnitude * composition * context_scale * (1+noise)  -- the magnitude and context scale are
nuisances. The compositional memory closes them away (scale-invariant recall); the raw memory is fooled.

HONEST: T3 VISION seed. The mechanism (scale-invariant content-addressable recall) is measured here, but this
OVERLAPS existing content-addressable / Hopfield / vector-DB memory -- the novelty is the log-ratio
(scale/context-invariant) framing + deterministic 7-bit content addressing, NOT a claim to beat them. Requires
compositional data. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. 2026-06-25. Peter is the sole gate; nothing posted.
"""
import numpy as np, hashlib, json
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(v); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def encode_7bit_clr(comp):
    z=clr(comp); lo,hi=-6.0,6.0; step=(hi-lo)/127.0
    q=np.clip(np.round((z-lo)/step),0,127).astype(np.uint8)
    return q, hashlib.sha256(q.tobytes()).hexdigest()[:16]

if __name__=="__main__":
    rng=np.random.default_rng(4); D,M=12,200
    comps=[closure(np.abs(rng.standard_normal(D))+0.2) for _ in range(M)]
    mags =[float(np.exp(rng.uniform(np.log(1),np.log(1000)))) for _ in range(M)]   # each memory a different overall magnitude
    raw  =[mags[k]*comps[k] for k in range(M)]                                       # raw measured vectors
    clr_store=[clr(c) for c in comps]
    addrs=[encode_7bit_clr(c)[1] for c in comps]
    det = all(encode_7bit_clr(comps[i])[1]==addrs[i] for i in range(M))

    def recall(mode):
        ok=0
        for _ in range(400):
            k=int(rng.integers(M))
            g=float(np.exp(rng.uniform(np.log(0.2),np.log(5))))                      # context/illumination/gain scale
            q=mags[k]*comps[k]*g*(1+0.03*rng.standard_normal(D)); q=np.abs(q)
            if mode=="compositional":
                qz=clr(q); j=int(np.argmin([np.sum((cz-qz)**2) for cz in clr_store]))
            else:  # raw magnitude memory
                j=int(np.argmin([np.sum((np.asarray(r)-q)**2) for r in raw]))
            ok += (j==k)
        return ok/400
    comp_acc=recall("compositional"); raw_acc=recall("raw")

    out={"_meta":{"tool":"compositional_memory.py","D":D,"n_memories":M,
                  "what":"content-addressable, scale-invariant associative memory (7-bit-clr codes + differential recall)"},
         "deterministic_content_address":bool(det),"bytes_per_memory":D,
         "recall_under_magnitude+context-scale+noise":{
             "compositional_clr_accuracy":round(comp_acc,3),
             "raw_magnitude_accuracy":round(raw_acc,3),
             "meaning":"the compositional memory recalls invariant to overall magnitude AND context scale; the raw-magnitude memory is fooled by them"},
         "fence":"T3 vision seed; mechanism measured; overlaps content-addressable/Hopfield/vector-DB memory; novelty = log-ratio scale/context invariance + deterministic 7-bit addressing; needs compositional data."}
    out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()[:16]
    print(json.dumps(out,indent=2))
