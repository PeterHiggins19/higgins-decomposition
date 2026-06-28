#!/usr/bin/env python3
"""
contact_length_model.py -- the theory, modeled honestly: ratio-blindness falls away with CONTACT TIME.
A user's comprehension of the compositional view accumulates with contact; below a 'seeing' threshold the
relational signature is below their noise (glazed eyes, the mountain); above it, it LOCKS (they 'see') and
ratio-blindness falls. The threshold is the same KNOWABLE-SAMPLE FLOOR the system shows everywhere (max-power
/ D*(N); the language demo: 5% of text = noise, 20%+ = the signature locks).

HONEST: this is a T3 HYPOTHESIS about communication ('or so goes the theory'). The curve shape is a model, not
measured on real users; it is FALSIFIABLE -- measure contact-time vs comprehension and see if a threshold
exists and where. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted
per HUF-STD-001. 2026-06-25. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
def sigmoid(x): return 1.0/(1.0+np.exp(-x))
def comprehension(t, t_star=6.0, width=1.5): return float(sigmoid((t-t_star)/width))
def ratio_blindness(t, **k): return float(max(0.0, 1.0-comprehension(t,**k)))

if __name__=="__main__":
    ts=[0.5,1,2,4,6,8,12,20]; t_star=6.0
    curve=[{"contact_t":t,"comprehension":round(comprehension(t),3),"ratio_blindness":round(ratio_blindness(t),3),
            "phase":("mountain (glazed)" if comprehension(t)<0.2 else
                     "basics useful" if comprehension(t)<0.5 else
                     "steps useful / SEEING" if comprehension(t)<0.85 else "sees (blindness fallen)")} for t in ts]
    out={"_meta":{"tool":"contact_length_model.py","tier":"T3 HYPOTHESIS (falsifiable)",
                  "what":"ratio-blindness falls with contact time past a 'seeing' threshold = the knowable-sample floor"},
        "seeing_threshold_t_star":t_star,"contact_comprehension_curve":curve,
        "design_objective":"maximize P(contact reaches t_star): the words/steps that keep a user engaged THROUGH the slow mountain phase are the lever -- contact length is the key.",
        "tie_in":"the threshold is the same knowable-sample floor measured elsewhere (language demo 5%->noise / 20%+->lock; max-power D*(N)); 'seeing' = the comprehension signature locking above the floor.",
        "falsifier":"measure real contact-time vs comprehension; if no threshold exists, or it is not preceded by a slow phase, the theory is wrong."}
    out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps({k:v for k,v in out.items() if k!='_meta'},sort_keys=True,default=str).encode()).hexdigest()[:16]
    print(json.dumps(out,indent=2))
